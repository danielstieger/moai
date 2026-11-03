"""Direct SQL. In the text: :var, :var.prop, :var.ref#KEY, :var.method() (bound parameters), {Decl.ELEM} (status constant);
quoted SQL strings stay text as written, ' ' needs no CHAR(32)"""
import re

from ..knoten import BL, CLO, MM, OF, Stop, TXT, fq, kid, kids, node
from ..registry import form, marker

QUOTED = re.compile(r"('[^']*')")
SQL_PART = re.compile(r"(:[A-Za-z_]\w*(?:\.[A-Za-z_]\w*(?:#KEY|\(\))?)?|\{[A-Za-z_]\w*\.[A-Za-z_]\w*\})")


def _operation(field):
    """The part after the dot of a bound parameter: prop, ref#KEY or method()."""
    if field.endswith("#KEY"):
        return node(MM + "C2EntityKeyPropReference", refs={"property": field[:-4]})
    if field.endswith("()"):
        return node(MM + "C2MethodReference", refs={"method": field[:-2]})
    return node(MM + "C2PropertyReference", refs={"property": field})


def _elements(line):
    """A line of SQL text -> [(is_text, part)]. The generator joins the words with one blank, so a word holds no blank
    (the language says so too): ' ' is the two words ' and '. Only a blank run inside a quoted string needs a word with
    blanks, it would be lost otherwise. A quoted string is text even where it looks like :x or {A.B}."""
    out, word = [], ""

    def flush():
        nonlocal word
        if word:
            out.append((True, word))
        word = ""

    for piece in QUOTED.split(line):
        if piece.startswith("'"):
            atoms = [piece] if "  " in piece else piece.split(" ")
            word += atoms[0]
            for atom in atoms[1:]:
                flush()
                word = atom
            continue
        for token in re.split(r"(\s+)", piece):
            if token.isspace():
                flush()
                continue
            for part in SQL_PART.split(token):
                if SQL_PART.fullmatch(part):
                    flush()
                    out.append((False, part))
                else:
                    word += part
    flush()
    return out


def sql_text(conv, n, what):
    """A string literal with SQL text -> one C2SqlText."""
    lines = []
    text_all = conv.string(n, what).replace("\\n", "\n")  # the parser keeps \n as two characters
    if text_all.count("'") % 2:
        raise Stop(f"{what}: unbalanced ' in the SQL text")
    for text in text_all.split("\n"):
        elements = []
        for is_text, part in _elements(text):
            if is_text:
                elements.append(node(TXT + "Word", {"value": part}))
            elif part.startswith(":"):
                var, _, field = part[1:].partition(".")
                ref_node = node(MM + "C2SqlWordVarReference", refs={"varDecl": var})
                elements.append(node(MM + "C2Dot", children={"operand": ref_node, "operation": _operation(field)})
                                if field else ref_node)
            else:
                decl, _, elem = part[1:-1].partition(".")
                elements.append(node(MM + "C2SqlStatusReference", children={"primConstant": node(
                    OF + "StatusConstReference", refs={"status": decl},
                    children={"operation": node(OF + "StatusElementReference", refs={"statusElement": elem})})}))
        if elements:
            lines.append(node(TXT + "Line", children={"elements": elements}))
    if not lines:
        raise Stop(f"{what}: the SQL text is empty")
    return node(MM + "C2SqlText", children={"lines": lines})


def _block(conv, closure, what):
    """SQL(kind, () -> { ... }, ..): the block of a dynamic SQL statement."""
    if kids(closure, "parameter"):
        raise Stop(f"{what}: the SQL block takes no parameters")
    body = kid(closure, "body")
    if body is None or fq(body) != BL + "StatementList":
        raise Stop(f"{what}: the SQL block must be a block: () -> {{ SQLTEXT(..); }}")
    statements = kids(body, "statement")
    if len(statements) == 1 and fq(statements[0]) == BL + "BlockStatement":  # the parser wraps a lambda's block
        body = kid(statements[0], "statements")
    outer, conv.in_sql_block = conv.in_sql_block, True
    try:
        out = conv.fix(body)
    finally:
        conv.in_sql_block = outer
    if not any(x["concept"] == MM + "C2SqlText" for x in _blueprint_nodes(out)):
        raise Stop(f"{what}: the SQL block contains no SQLTEXT")
    return out


def _blueprint_nodes(n):
    yield n
    for c in n.get("children", []):
        for x in c.get("nodes", []):
            yield from _blueprint_nodes(x)


@marker("SQL", 'SQL("QUERY"|"STATEMENT","text\\\\nnext line",[MAPPER("m")|ROWMAPPER("m")|lambda])', "SQL block", args=(2, 3))
def sql(conv, args, what):
    kind = conv.string(args[0], what)
    if kind not in ("QUERY", "STATEMENT"):
        raise Stop(f"{what}: kind must be QUERY or STATEMENT, not '{kind}'")
    if fq(args[1]) == CLO + "ClosureLiteral":
        statements = _block(conv, args[1], what)
    else:
        statements = node(BL + "StatementList", children={"statement": sql_text(conv, args[1], what)})
    mapping = None
    if len(args) > 2:
        mname, margs = conv.marker(args[2])
        if mname == "MAPPER":
            mapping = node(MM + "NoKeyMapperFieldRef", refs={"noKeyMapperField": conv.string(margs[0], what)})
        elif mname == "ROWMAPPER":
            mapping = node(MM + "RowMapperFieldRef", refs={"rowMapperField": conv.string(margs[0], what)})
        else:
            mapping = conv.fix(args[2])  # an inline lambda
    if kind == "STATEMENT" and mapping is not None:
        raise Stop(f"{what}: a STATEMENT has no result mapping")
    out = node(MM + "C2SqlBlock", {"sqlType": kind}, {"statements": statements, "mapping": mapping})
    if kind == "STATEMENT":
        out["children"].append({"role": "mapping", "nodes": []})  # suppress the factory's row closure
    return out


form("SQL block", 'SQL("QUERY"|"STATEMENT",() -> { SQLTEXT("text"); if (c) { String x = ..; SQLTEXT("AND A = :x"); } },[mapping])',
     "dynamic SQL: the block is Java; every reached SQLTEXT adds its fragment, in execution order", __name__)


@marker("SQLTEXT", 'SQLTEXT("text")', "a fragment, only inside a SQL block", args=1, statement=True)
def sqltext(conv, args, what):
    if not conv.in_sql_block:
        raise Stop('SQLTEXT is valid only inside a SQL block: SQL("QUERY", () -> { SQLTEXT(..); }, ..)')
    return sql_text(conv, args[0], "SQLTEXT")
