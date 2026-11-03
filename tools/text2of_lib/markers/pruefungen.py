"""Conditions, checks and log"""
from ..knoten import BL, OF, Stop, fq, kid, kids, node
from ..methoden import STRING_CONTAINS
from ..registry import form, marker, rewrite


def fmt(conv, args, what):
    if not args:
        raise Stop(f"{what}: a format string is missing")
    return node(OF + "MultiString", children={
        "formatString": node(OF + "StringFormatString", {"formatStringValue": conv.string(args[0], what)}),
        "arguments": [conv.fix(a) for a in args[1:]]})


@marker("OF", 'OF(x,"A","B")', "x of A, B", args=(2, None))
def status_of(conv, args, what):
    return node(OF + "StatusOfOperator", children={
        "statusLeftSide": conv.fix(args[0]),
        "statusElements": [node(OF + "StatusElementReference", refs={"statusElement": conv.string(a, what)}) for a in args[1:]]})


def _npe(conv, concept, args):
    return node(BL + concept, children={"leftExpression": conv.fix(args[0]), "rightExpression": conv.fix(args[1])})


@marker("EQ", "EQ(a,b)", "a :eq: b", args=2)
def eq(conv, args, what):
    return _npe(conv, "NPEEqualsExpression", args)


@marker("NE", "NE(a,b)", "a :ne: b", args=2)
def ne(conv, args, what):
    return _npe(conv, "NPENotEqualsExpression", args)


@rewrite(BL + "NotExpression")
def not_npe(conv, n):
    """!EQ(a,b): the checker wants parentheses around :eq: and :ne:."""
    inner = kid(n, "expression")
    if conv.marker(inner)[0] not in ("EQ", "NE"):
        return None
    return node(BL + "NotExpression", children={"expression": node(BL + "ParenthesizedExpression", children={"expression": conv.fix(inner)})})


def _on_string(conv, concept, args):
    return node(BL + "DotExpression", children={"operand": conv.fix(args[0]), "operation": node(BL + concept)})


@marker("ISEMPTY", "ISEMPTY(s)", "s.isEmpty on a string (s.isEmpty() is the list operation)", args=1)
def is_empty(conv, args, what):
    return _on_string(conv, "IsEmptyOperation", args)


@marker("ISNOTEMPTY", "ISNOTEMPTY(s)", "s.isNotEmpty on a string", args=1)
def is_not_empty(conv, args, what):
    return _on_string(conv, "IsNotEmptyOperation", args)


@marker("CONTAINS", 'CONTAINS(s,"x")', "s.contains(x) on a string (s.contains() is the list operation)", args=2)
def contains(conv, args, what):
    return node(BL + "DotExpression", children={
        "operand": conv.fix(args[0]),
        "operation": node(BL + "InstanceMethodCallOperation", refs={"baseMethodDeclaration": STRING_CONTAINS},
                          children={"actualArgument": conv.fix(args[1])})})


@marker("FMT", 'FMT("fmt",args)', "'fmt'%(args)", args=(1, None))
def fmt_marker(conv, args, what):
    return fmt(conv, args, what)


def _precondition(conv, args, name, warning):
    cond = None if fq(args[0]) == BL + "NullLiteral" else conv.fix(args[0])
    ch = {"condition": cond, "problemdesc": node(OF + "ProblemMessage", children={"problem": fmt(conv, args[1:], name)})}
    if warning:
        ch["options"] = node(OF + "CheckOptionRef", refs={"option": "WARNING_HINT"})
    return node(OF + "Precondition", children=ch)


@marker("PRE", 'PRE(cond,"fmt",args)', "precondition; PRE(null,..) is always raised", args=(2, None), statement=True)
def pre(conv, args, what):
    return _precondition(conv, args, what, False)


@marker("PREW", 'PREW(cond,"fmt",args)', "precondition, WARNING_HINT", args=(2, None), statement=True)
def prew(conv, args, what):
    return _precondition(conv, args, what, True)


@marker("GUARD", 'GUARD(cond,"fmt",args)', "guard", args=(2, None), statement=True)
def guard(conv, args, what):
    cond = None if fq(args[0]) == BL + "NullLiteral" else conv.fix(args[0])
    return node(OF + "Guard", children={"condition": cond, "desc": node(OF + "ProblemMessage", children={"problem": fmt(conv, args[1:], what)})})


LOG_LEVELS = {"TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL"}


@marker("LOG", 'LOG("INFO","fmt",args)', "log", args=(2, None), statement=True)
def log(conv, args, what):
    level = conv.string(args[0], "LOG level")
    if level not in LOG_LEVELS:
        raise Stop(f"LOG level '{level}' is not one of {', '.join(sorted(LOG_LEVELS))}")
    return node(OF + "LogStatement", {"logLevel": level}, {"exp": fmt(conv, args[1:], what)})


form("VALIDATION", "if (VALIDATION()) { ... }", "validation { ... }", __name__)


@rewrite(BL + "IfStatement")
def validation(conv, n):
    if conv.marker(kid(n, "condition"))[0] != "VALIDATION":
        return None
    if kid(n, "ifFalseStatement") is not None or kids(n, "elsifClauses"):
        raise Stop("if (VALIDATION()) must not have an else branch")
    return node(OF + "ValidationStatement", children={"statements": conv.fix(kid(n, "ifTrue"))})


form("STATUS_SWITCH", 'switch (STATUS_SWITCH(x)) { case "A": ...; break; case "B": case "C": ...; break; default: ... }',
     "status switch (no default: every element must be handled)", __name__)


def _switch_body(conv, body):
    out = conv.fix(body)
    stmts = [c for c in out.get("children", []) if c["role"] == "statement"]
    if stmts and stmts[0]["nodes"] and stmts[0]["nodes"][-1]["concept"] == BL + "BreakStatement":
        stmts[0]["nodes"].pop()
    return out


@rewrite(BL + "SwitchStatement")
def status_switch(conv, n):
    if conv.marker(kid(n, "expression"))[0] != "STATUS_SWITCH":
        return None
    _, args = conv.marker(kid(n, "expression"))
    cases, labels, default = [], [], None
    for case in kids(n, "case"):
        labels.append(case)
        body = kid(case, "body")
        stmts = kids(body, "statement") if body is not None else []
        if not stmts:
            continue  # fall-through: the next case with statements takes this label too
        elems = [node(OF + "StatusElementReference", refs={"statusElement": conv.string(kid(c, "expression"), "STATUS_SWITCH case")})
                 for c in labels]
        cases.append(node(OF + "OnStatementCase", children={"status": elems, "statementList": _switch_body(conv, body)}))
        labels = []
    if labels:
        raise Stop("STATUS_SWITCH: the last case has no statements")
    if kid(n, "defaultBlock") is not None:
        default = _switch_body(conv, kid(n, "defaultBlock"))
    return node(OF + "OnStatement", children={"sourceStatusExpression": conv.fix(args[0]),
                                             "onStatementCase": cases, "defaultStatementList": default})


form("FAIL_IN", 'FAIL_IN("Ex"[,"text"]);', "FAIL IN Ex on the following statement (tests)", __name__)
