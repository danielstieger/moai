#!/usr/bin/env python3
"""MoAI Text -> ObjectFlow: turn Java text with markers into ObjectFlow / ManMap nodes.

Workflow (see the DSL skills):
  1. Insert the methods as Java text with `mps_mcp_parse_java_and_insert` (featureKind CLASS_CONTENT or METHOD,
     insert.mode child into the root's `member` role). The parser leaves the markers unresolved; that is expected.
  2. `mps_mcp_print_node` (deep=true) of the root.
  3. python3 -I moai/tools/text2of.py ROOTDUMP [--repo-type METHOD=TYPE]... [--only NAME]...
     writes one blueprint per member into the system temp directory and prints a table:
       name | reference of the node to replace (SET CHILD childNodeRef) | file
     Constructors and test methods are replaced through their body only, so references to them stay valid.
  4. `mps_mcp_update_node` SET CHILD per row, then FIX_REFERENCES on the root (calls between replaced members
     bind to the old node until the last row is set), `moai/tools/verify.py node` and the model check.

The kind of method follows the root: methods of a Service become service methods, of a Repository repository
methods (`--repo-type name=CHECKOUT|CHECKIN|DELETE`, default READONLY), otherwise plain instance methods.

Markers (Java text -> result):
  plain Java property access x.prop / own prop  -> business property reference (no marker)
  String, List<T>, new ArrayList<T>()            -> string, list<T>, new arraylist<T>
  coll.where(l) select any all findFirst translate foldLeft(seed,l) sortBy(l,asc) size() isEmpty() isNotEmpty()
      first() last() toList() distinct() add(e) remove(e) contains(e)    -> collections operations
      (add/remove/contains on a BigDecimal-looking operand or argument -> BigDecimal method; otherwise list;
       a lambda parameter becomes an inferred closure parameter)
  BD("1.50") SERVERDATE() SERVERDATETIME() DATE(y,m,d) DATETIME(y,m,d,h,mi,s)   -> literals (fixed: fromServer=false)
  STATUS("Decl","ELEM")  OF(x,"A","B")          -> Decl.ELEM, x of A, B
  EQ(a,b)  NE(a,b)                               -> a :eq: b, a :ne: b
  FMT("fmt", args)                               -> 'fmt'%(args)
  PRE(cond,"fmt",args) PREW(..) PRE(null,..)     -> precondition (WARNING_HINT / always raised)
  GUARD(cond,"fmt",args)                         -> guard
  if (VALIDATION()) { ... }                      -> validation { ... }
  LOG("INFO","fmt",args)                         -> log
  CALL("Comp","m",args)  CALL_WITH(sess,"Comp","m",args)   -> # Comp.m(..), #+ with sess Comp.m(..)
      session                                    -> session (the session of the current context)
  SESSION_OP("Comp","m","text",args)             -> session operation add # Comp.m(..) // 'text'
  KEY(x.ref)  ISNULLKEY(KEY(x.ref))              -> x.ref#Key, x.ref#Key.isNullKey
  SAVE("Map",x[,"INSERT"|"UPDATE"|"BATCH"])  DELETE("Map",x)   -> save with Map x, delete with Map x
  GET("Map",key,ro)                              -> Map get(key), ro = true (read-only) / false (checkout)
  WHERE("Map",ro,filter) .SORTBY(FIELD,asc) .LIMIT(n)   -> Map where(filter) sortBy limit
      in the filter: FIELD("Map","field"), LIKE(a,b), IN(FIELD(..),list), OPTIONAL(pred)
  FAIL_IN("Ex"[,"text"]);                        -> FAIL IN Ex on the following statement
  switch (STATUS_SWITCH(x)) { case "A": ...; break; case "B": case "C": ...; break; default: ... }
                                                 -> status switch (no default: every element must be handled)
  META(x.prop).setEnabled(..)                    -> x.prop#Meta.setEnabled(..)
  ROLE("Name")  SELECTED("Type"[,true])          -> role Name(), getSelected(Type) (+ derived)
  SESSION_ENTITIES("Type","all")                 -> session entities (checked_out|keys_of_checked_out|all|keys_of_all)
  MERGE(src,dest,"entity","list","readonly"[,sess])  -> session merge (entity|list|ref; readonly|checkedout|none)
  SQL("QUERY"|"STATEMENT","text\\nnext line",[MAPPER("m")|ROWMAPPER("m")|lambda])
      in the text: :var, :var.prop (bound parameters), {Decl.ELEM} (status constant)
Command bodies (command init, page init, scopes, conclusions, final conclusions, termination handlers):
  DONE()  PAGE("Name")  PUSH(x)  QUEUE_NEXT("Command", args)   -> done, page Name, pushSelection(x), queue next command
  TERM_OK()  PUSHED()  WAS_CHILD()               -> terminatedInFinalOk, pushed, wasChild (termination handler)
  command parameters and variables are written by name; page init ends with `return x;`
Anything else that stays unresolved stops the tool with its location.
"""
import sys

sys.dont_write_bytecode = True  # write nothing into the package (moai/ is a submodule in projects)

import json
import os
import re
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blueprint import Checker, Structure, report  # noqa: E402

BL = "jetbrains.mps.baseLanguage.structure."
COL = "jetbrains.mps.baseLanguage.collections.structure."
CLO = "jetbrains.mps.baseLanguage.closures.structure."
OF = "org.modellwerkstatt.objectflow.structure."
MM = "org.modellwerkstatt.manmap.structure."
SKIP_PROPS = {"resolveInfo", "shortDescription", "virtualPackage"}
BIGDEC = "6354ebe7-c22a-4a0f-ac54-50b52ab9b065/java:java.math(JDK/)/~BigDecimal"
BIGDEC_METHODS = {  # overloaded stub methods need persistent refs
    "add": BIGDEC + ".add%28java.math.BigDecimal%29",
    "subtract": BIGDEC + ".subtract%28java.math.BigDecimal%29",
    "multiply": BIGDEC + ".multiply%28java.math.BigDecimal%29",
    "compareTo": BIGDEC + ".compareTo%28java.math.BigDecimal%29",
    "negate": BIGDEC + ".negate%28%29",
    "abs": BIGDEC + ".abs%28%29",
}
COLL_CLOSURE = {"where": "WhereOperation", "select": "SelectOperation", "any": "AnyOperation", "all": "AllOperation",
                "findFirst": "FindFirstOperation", "translate": "TranslateOperation"}
COLL_NOARG = {"size": "GetSizeOperation", "isEmpty": "IsEmptyOperation", "isNotEmpty": "IsNotEmptyOperation",
              "first": "GetFirstOperation", "last": "GetLastOperation", "toList": "ToListOperation",
              "distinct": "DistinctOperation"}
COLL_ONEARG = {"add": "AddElementOperation", "remove": "RemoveElementOperation", "contains": "ContainsOperation"}
LOG_LEVELS = {"TRACE", "DEBUG", "INFO", "WARN", "ERROR", "FATAL"}
TXT = "jetbrains.mps.lang.text.structure."
MERGE_KINDS = {"entity", "list", "ref"}
MERGE_SESSION = {"readonly": "session_readonly", "checkedout": "session_checkedout", "none": "not_consider_session"}
SESSION_MODES = {"checked_out": "checked_out", "keys_of_checked_out": "ckecked_out_keys", "all": "all", "keys_of_all": "all_keys"}
SQL_PART = re.compile(r"(:[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)?|\{[A-Za-z_]\w*\.[A-Za-z_]\w*\})")


TERM_PARAMS = {"TERM_OK": "PageCmdTermConceptFuntionParamTermOk", "PUSHED": "PageCmdTermConceptFuntionParamPushed",
               "WAS_CHILD": "PageCmdTermConceptFuntionParamChild"}

class Stop(Exception):
    pass


def fq(n):
    return n["conceptReference"].rsplit(":", 1)[1]


def node(concept, props=None, children=None, refs=None):
    d = {"concept": concept}
    if props:
        d["properties"] = [{"name": k, "value": str(v).lower() if isinstance(v, bool) else str(v)} for k, v in props.items()]
    ch = []
    for role, v in (children or {}).items():
        nodes = [x for x in (v if isinstance(v, list) else [v]) if x is not None]
        if nodes:
            ch.append({"role": role, "nodes": nodes})
    if ch:
        d["children"] = ch
    if refs:
        d["references"] = [{"role": r, "target": t} for r, t in refs.items()]
    return d


def kids(n, role):
    for c in n.get("children", []):
        if c["role"] == role:
            return c.get("nodes", [])
    return []


def kid(n, role):
    k = kids(n, role)
    return k[0] if k else None


def ref(n, role):
    for r in n.get("references", []):
        if r["role"] == role:
            return r
    return None


def unresolved(r):
    return r is not None and (not r.get("target") or str(r.get("targetReference")).startswith("null"))


def prop(n, name):
    for p in n.get("properties", []):
        if p["name"] == name:
            return p.get("value")
    return None


def walk(n):
    yield n
    for c in n.get("children", []):
        for x in c.get("nodes", []):
            yield from walk(x)


def short(n):
    return f"{n.get('name') or fq(n).rsplit('.', 1)[-1]} ({fq(n).rsplit('.', 1)[-1]}, {n.get('reference', '')})"


class Converter:
    def __init__(self, member, root_refs, replaced, bigdec_props, containers=None):
        self.member = member
        self.inside = {x["reference"] for x in walk(member)}
        self.root_refs = root_refs          # every node reference of the root -> concept
        self.replaced = replaced            # references of nodes this run re-creates (new IDs): refer by name
        self.bigdec_props = bigdec_props    # BigDecimal business properties of the root
        self.containers = containers or {}  # command parameters / variables: name -> (reference, concept of the reference)
        self.locals = {x.get("name") for x in walk(member)
                       if fq(x) in (BL + "ParameterDeclaration", BL + "LocalVariableDeclaration")}
        self.bigdec_names = set()           # parameters / locals / closure params known as BigDecimal
        for x in walk(member):
            if fq(x) in (BL + "ParameterDeclaration", BL + "LocalVariableDeclaration"):
                t = kid(x, "type")
                if t is not None and fq(t) == BL + "ClassifierType" and (ref(t, "classifier") or {}).get("target") == "BigDecimal":
                    self.bigdec_names.add(x.get("name"))

    # ---- helpers -----------------------------------------------------------------------------------
    def string(self, n, what):
        if n is None or fq(n) != BL + "StringLiteral":
            raise Stop(f"{what}: a string literal is expected, found {short(n) if n else 'nothing'}")
        return prop(n, "value") or ""

    def integer(self, n, what):
        if n is None or fq(n) != BL + "IntegerConstant":
            raise Stop(f"{what}: an integer literal is expected, found {short(n) if n else 'nothing'}")
        return int(prop(n, "value") or 0)

    def boolean(self, n, what):
        if n is None or fq(n) != BL + "BooleanConstant":
            raise Stop(f"{what}: true or false is expected, found {short(n) if n else 'nothing'}")
        return (prop(n, "value") or "false") == "true"

    def marker(self, n):
        """(name, args) for an unresolved call written as a marker, else (None, None)."""
        if n is None:
            return None, None
        c = fq(n)
        if c in (BL + "LocalMethodCall", BL + "LocalStaticMethodCall", BL + "LocalInstanceMethodCall") \
                and unresolved(ref(n, "baseMethodDeclaration")):
            return n.get("name"), kids(n, "actualArgument")
        if c == BL + "UnknownLocalCall":
            return prop(n, "callee"), kids(n, "actualArgument")
        return None, None

    def split_property(self, n, what):
        """x.prop written inside a marker -> (operand node, property name)."""
        c = fq(n)
        if c == BL + "DotExpression" and fq(kid(n, "operation")) == BL + "FieldReferenceOperation":
            return self.fix(kid(n, "operand")), kid(n, "operation").get("name")
        if c == BL + "UnknownNameRef":
            tokens = prop(n, "tokens") or ""
            if "." in tokens:
                head, _, last = tokens.rpartition(".")
                return self.tokens(head), last
        raise Stop(f"{what}: x.property is expected, found {short(n)}")

    def sql(self, args, what):
        kind = self.string(args[0], what)
        if kind not in ("QUERY", "STATEMENT"):
            raise Stop(f"{what}: kind must be QUERY or STATEMENT, not '{kind}'")
        lines = []
        sql_text = self.string(args[1], what).replace("\\n", "\n")  # the parser keeps \n as two characters
        for text in sql_text.split("\n"):
            elements = []
            for word in text.split():
                for part in SQL_PART.split(word):
                    if not part:
                        continue
                    if part.startswith(":"):
                        var, _, field = part[1:].partition(".")
                        ref_node = node(MM + "C2SqlWordVarReference", refs={"varDecl": var})
                        elements.append(node(MM + "C2Dot", children={"operand": ref_node, "operation": node(
                            MM + "C2PropertyReference", refs={"property": field})}) if field else ref_node)
                    elif part.startswith("{"):
                        decl, _, elem = part[1:-1].partition(".")
                        elements.append(node(MM + "C2SqlStatusReference", children={"primConstant": node(
                            OF + "StatusConstReference", refs={"status": decl},
                            children={"operation": node(OF + "StatusElementReference", refs={"statusElement": elem})})}))
                    else:
                        elements.append(node(TXT + "Word", {"value": part}))
            if elements:
                lines.append(node(TXT + "Line", children={"elements": elements}))
        if not lines:
            raise Stop(f"{what}: the SQL text is empty")
        mapping = None
        if len(args) > 2:
            mname, margs = self.marker(args[2])
            if mname == "MAPPER":
                mapping = node(MM + "NoKeyMapperFieldRef", refs={"noKeyMapperField": self.string(margs[0], what)})
            elif mname == "ROWMAPPER":
                mapping = node(MM + "RowMapperFieldRef", refs={"rowMapperField": self.string(margs[0], what)})
            else:
                mapping = self.fix(args[2])  # an inline lambda
        if kind == "STATEMENT" and mapping is not None:
            raise Stop(f"{what}: a STATEMENT has no result mapping")
        out = node(MM + "C2SqlBlock", {"sqlType": kind},
                   {"statements": node(BL + "StatementList", children={"statement": node(MM + "C2SqlText", children={"lines": lines})}),
                    "mapping": mapping})
        if kind == "STATEMENT":
            out["children"].append({"role": "mapping", "nodes": []})  # suppress the factory's row closure
        return out

    def status_switch(self, n):
        """switch (STATUS_SWITCH(x)) { case "A": ...; break; ... default: ... }"""
        _, args = self.marker(kid(n, "expression"))
        cases, labels, default = [], [], None
        for case in kids(n, "case"):
            labels.append(case)
            body = kid(case, "body")
            stmts = kids(body, "statement") if body is not None else []
            if not stmts:
                continue  # fall-through: the next case with statements takes this label too
            elems = [node(OF + "StatusElementReference", refs={"statusElement": self.string(kid(c, "expression"), "STATUS_SWITCH case")})
                     for c in labels]
            cases.append(node(OF + "OnStatementCase", children={"status": elems, "statementList": self.switch_body(body)}))
            labels = []
        if labels:
            raise Stop("STATUS_SWITCH: the last case has no statements")
        if kid(n, "defaultBlock") is not None:
            default = self.switch_body(kid(n, "defaultBlock"))
        return node(OF + "OnStatement", children={"sourceStatusExpression": self.fix(args[0]),
                                                 "onStatementCase": cases, "defaultStatementList": default})

    def switch_body(self, body):
        out = self.fix(body)
        stmts = [c for c in out.get("children", []) if c["role"] == "statement"]
        if stmts and stmts[0]["nodes"] and stmts[0]["nodes"][-1]["concept"] == BL + "BreakStatement":
            stmts[0]["nodes"].pop()
        return out

    def fmt(self, args, what):
        if not args:
            raise Stop(f"{what}: a format string is missing")
        return node(OF + "MultiString", children={
            "formatString": node(OF + "StringFormatString", {"formatStringValue": self.string(args[0], what)}),
            "arguments": [self.fix(a) for a in args[1:]]})

    def is_bigdec(self, n):
        if n is None:
            return False
        name, _ = self.marker(n)
        if name == "BD":
            return True
        c = fq(n)
        if c == BL + "VariableReference" and n.get("name") in self.bigdec_names:
            return True
        r = ref(n, "variableDeclaration")
        if c == BL + "VariableReference" and r is not None and r.get("target") in self.bigdec_names:
            return True
        if c == BL + "VariableReference" and unresolved(r) and n.get("name") in self.bigdec_props:
            return True  # own business property written as a bare name
        if c == BL + "DotExpression":
            op = kid(n, "operation")
            if op is not None and fq(op) == BL + "FieldReferenceOperation" and op.get("name") in self.bigdec_props:
                return True
        return False

    # ---- collections and BigDecimal ----------------------------------------------------------------
    def method_op(self, callee, operand, args):
        if callee in BIGDEC_METHODS and (callee not in COLL_ONEARG or self.is_bigdec(operand)
                                         or any(self.is_bigdec(a) for a in args)):
            return node(BL + "InstanceMethodCallOperation", refs={"baseMethodDeclaration": BIGDEC_METHODS[callee]},
                        children={"actualArgument": [self.fix(a) for a in args]})
        if callee in COLL_CLOSURE:
            return node(COL + COLL_CLOSURE[callee], children={"closure": self.fix(args[0])})
        if callee in COLL_NOARG:
            return node(COL + COLL_NOARG[callee])
        if callee in COLL_ONEARG:
            return node(COL + COLL_ONEARG[callee], children={"argument": self.fix(args[0])})
        if callee == "foldLeft":
            seed, closure = args
            if self.is_bigdec(seed):  # the accumulator of a BigDecimal fold is a BigDecimal
                params = kids(closure, "parameter")
                if params:
                    self.bigdec_names.add(params[0].get("name"))
            return node(COL + "FoldLeftOperation", children={"seed": self.fix(seed), "closure": self.fix(closure)})
        if callee == "sortBy":
            return node(COL + "SortOperation", children={"closure": self.fix(args[0]), "ascending": self.fix(args[1])})
        return node(BL + "InstanceMethodCallOperation", refs={"baseMethodDeclaration": callee},
                    children={"actualArgument": [self.fix(a) for a in args]})

    # ---- ManMap ------------------------------------------------------------------------------------
    def query(self, name, args, chain):
        if name == "GET":
            mapping, key, ro = args
            ops = [node(MM + "GetQuery", children={"argument": self.fix(key)})]
        else:
            mapping, ro, flt = args
            ops = [node(MM + "WhereQuery", children={"filter": self.fix(flt)})]
        for callee, cargs in chain:
            if callee == "SORTBY":
                direction = "ASC" if self.boolean(cargs[1], "SORTBY direction") else "DESC"
                ops.append(node(MM + "SortByQuery", {"sortDirection": direction}, {"toComparable": self.fix(cargs[0])}))
            elif callee == "LIMIT":
                ops.append(node(MM + "LimitQuery", children={"count": self.fix(cargs[0])}))
            else:
                raise Stop(f"unknown query operation .{callee}(); use .SORTBY(FIELD(..), asc) or .LIMIT(n)")
        return node(MM + "QueryFromMap", {"readOnly": self.boolean(ro, f"{name} read-only flag")},
                    {"queryOperation": ops}, {"entityMapping": self.string(mapping, f"{name} mapping")})

    def query_chain(self, n):
        """WHERE(..).SORTBY(..).LIMIT(..) is parsed as calls on the marker call."""
        chain = []
        while fq(n) == BL + "UnknownInstanceMethodCall" or (fq(n) == BL + "DotExpression"
                                                           and fq(kid(n, "operation")) == BL + "InstanceMethodCallOperation"):
            if fq(n) == BL + "UnknownInstanceMethodCall":
                chain.insert(0, (prop(n, "callee"), kids(n, "actualArgument")))
                n = kid(n, "operand")
            else:
                op = kid(n, "operation")
                chain.insert(0, (op.get("name"), kids(op, "actualArgument")))
                n = kid(n, "operand")
        name, args = self.marker(n)
        return (name, args, chain) if name in ("GET", "WHERE") else (None, None, None)

    # ---- statements --------------------------------------------------------------------------------
    def statement_list(self, n):
        out, pending = [], None
        for st in kids(n, "statement"):
            if fq(st) == BL + "ExpressionStatement":
                name, args = self.marker(kid(st, "expression"))
                if name == "FAIL_IN":
                    ch = {"contains": node(BL + "StringLiteral", {"value": self.string(args[1], "FAIL_IN text")})} if len(args) > 1 else None
                    pending = node(OF + "OFXTestFailInAttribue", children=ch,
                                   refs={"classifier": self.string(args[0], "FAIL_IN exception")})
                    continue
            f = self.fix(st)
            if pending is not None:
                f.setdefault("children", []).append({"role": "smodelAttribute", "nodes": [pending]})
                pending = None
            out.append(f)
        if pending is not None:
            raise Stop("FAIL_IN must be followed by a statement")
        return node(BL + "StatementList", children={"statement": out})

    def statement_marker(self, name, args):
        if name in ("PRE", "PREW"):
            cond = None if fq(args[0]) == BL + "NullLiteral" else self.fix(args[0])
            ch = {"condition": cond, "problemdesc": node(OF + "ProblemMessage", children={"problem": self.fmt(args[1:], name)})}
            if name == "PREW":
                ch["options"] = node(OF + "CheckOptionRef", refs={"option": "WARNING_HINT"})
            return node(OF + "Precondition", children=ch)
        if name == "GUARD":
            cond = None if fq(args[0]) == BL + "NullLiteral" else self.fix(args[0])
            return node(OF + "Guard", children={"condition": cond, "desc": node(OF + "ProblemMessage", children={"problem": self.fmt(args[1:], name)})})
        if name == "LOG":
            level = self.string(args[0], "LOG level")
            if level not in LOG_LEVELS:
                raise Stop(f"LOG level '{level}' is not one of {', '.join(sorted(LOG_LEVELS))}")
            return node(OF + "LogStatement", {"logLevel": level}, {"exp": self.fmt(args[1:], name)})
        if name == "SESSION_OP":
            call = node(OF + "OperationCall", children={"actualArgument": [self.fix(a) for a in args[3:]]},
                        refs={"runtimeHandledObject": self.string(args[0], "SESSION_OP component"),
                              "baseMethodDeclaration": self.string(args[1], "SESSION_OP method")})
            return node(OF + "SessionOperationAdd", children={
                "operationCall": call, "message": node(BL + "StringLiteral", {"value": self.string(args[2], "SESSION_OP text")})})
        if name == "QUEUE_NEXT":
            call = node(OF + "CommandCallBasis", children={"actualArgument": [self.fix(a) for a in args[1:]]},
                        refs={"command": self.string(args[0], "QUEUE_NEXT command")})
            return node(OF + "SessionQueueNextCommand", children={"commandCall": call})
        if name == "DONE":
            return node(OF + "DoneCommand")
        if name == "PAGE":
            return node(OF + "PageCommand", refs={"page": self.string(args[0], "PAGE name")})
        if name == "PUSH":
            return node(OF + "PushObject", children={"exp": self.fix(args[0])})
        if name in ("SAVE", "DELETE"):
            opts = []
            for a in args[2:]:
                o = self.string(a, f"{name} option")
                if o not in ("INSERT", "UPDATE", "BATCH"):
                    raise Stop(f"{name} option '{o}' is not one of INSERT, UPDATE, BATCH")
                opts.append(node(MM + {"INSERT": "InsertSaveOption", "UPDATE": "UpdateSaveOption", "BATCH": "BatchSaveOption"}[o]))
            return node(MM + ("SaveWithMap" if name == "SAVE" else "DeleteWithMap"),
                        children={"expression": self.fix(args[1]), "options": opts},
                        refs={"entityMapping": self.string(args[0], f"{name} mapping")})
        return None

    # ---- main dispatch -----------------------------------------------------------------------------
    def fix(self, n):
        c = fq(n)
        if c == BL + "StatementList":
            return self.statement_list(n)
        if c == BL + "ExpressionStatement":
            name, args = self.marker(kid(n, "expression"))
            st = self.statement_marker(name, args) if name else None
            if st is not None:
                return st
        if c == BL + "SwitchStatement" and self.marker(kid(n, "expression"))[0] == "STATUS_SWITCH":
            return self.status_switch(n)
        if c == BL + "IfStatement":
            name, _ = self.marker(kid(n, "condition"))
            if name == "VALIDATION":
                if kid(n, "ifFalseStatement") is not None or kids(n, "elsifClauses"):
                    raise Stop("if (VALIDATION()) must not have an else branch")
                return node(OF + "ValidationStatement", children={"statements": self.fix(kid(n, "ifTrue"))})

        name, args = self.marker(n)
        if name is not None:
            return self.expression_marker(name, args, n)

        qname, qargs, chain = self.query_chain(n) if c in (BL + "UnknownInstanceMethodCall", BL + "DotExpression") else (None, None, None)
        if qname:
            return self.query(qname, qargs, chain)

        if c == BL + "UnknownInstanceMethodCall":
            operand = kid(n, "operand")
            return node(BL + "DotExpression", children={
                "operand": self.fix(operand),
                "operation": self.method_op(prop(n, "callee"), operand, kids(n, "actualArgument"))})
        if c == BL + "UnknownDotCall":
            tokens = prop(n, "tokens") or ""
            callee, args = prop(n, "callee"), kids(n, "actualArgument")
            if tokens.rsplit(".", 1)[-1] in self.bigdec_props | self.bigdec_names and callee in BIGDEC_METHODS:
                op = node(BL + "InstanceMethodCallOperation", refs={"baseMethodDeclaration": BIGDEC_METHODS[callee]},
                          children={"actualArgument": [self.fix(a) for a in args]})
            else:
                op = self.method_op(callee, None, args)
            return node(BL + "DotExpression", children={"operand": self.tokens(tokens), "operation": op})
        if c == BL + "UnknownNameRef":
            return self.tokens(prop(n, "tokens"))
        if c.startswith(BL + "Unknown"):
            raise Stop(f"the parser could not read {short(n)}; rewrite the expression")

        if c == BL + "DotExpression":
            op, operand = kid(n, "operation"), kid(n, "operand")
            if fq(op) == BL + "FieldReferenceOperation" and unresolved(ref(op, "fieldDeclaration")):
                return node(BL + "DotExpression", children={
                    "operand": self.fix(operand), "operation": node(BL + "PropertyReference", refs={"property": op.get("name")})})
            if fq(op) == BL + "InstanceMethodCallOperation" and unresolved(ref(op, "baseMethodDeclaration")):
                return node(BL + "DotExpression", children={
                    "operand": self.fix(operand), "operation": self.method_op(op.get("name"), operand, kids(op, "actualArgument"))})

        if c == BL + "VariableReference":
            r = ref(n, "variableDeclaration")
            for target, concept in self.containers.values():
                if r is not None and r.get("targetReference") == target:
                    return node(concept, refs={"variableDeclaration": target})
            if unresolved(r) and n.get("name") == "session":
                return node(OF + "Session")
            if unresolved(r):
                return node(BL + "LocalPropertyReference", refs={"property": n.get("name")})
            if r["targetReference"] not in self.inside and r["targetReference"] in self.replaced:
                # bound to a declaration of another member (parser): rebind by name in this member
                return node(BL + "VariableReference", refs={"variableDeclaration": r.get("target")})

        if c == BL + "ClassifierType":
            r = ref(n, "classifier") or {}
            tr = r.get("targetReference") or ""
            if tr.endswith("~String") or r.get("target") == "String":
                return node(BL + "StringType")
            params = kids(n, "parameter")
            if tr.endswith(("~List", "~ArrayList", "~Collection")) or (unresolved(r) and n.get("name", "").startswith("List") and len(params) == 1) \
                    or (unresolved(r) and len(params) == 1):
                return node(COL + "ListType", children={"elementType": self.fix(params[0])})

        if c == BL + "GenericNewExpression":
            cr = kid(n, "creator")
            if fq(cr) == BL + "ClassCreator" and "~ArrayList" in json.dumps(cr.get("references", [])):
                return node(BL + "GenericNewExpression", children={"creator": node(COL + "ListCreatorWithInit", children={
                    "elementType": [self.fix(x) for x in kids(cr, "typeParameter")]})})

        if c == CLO + "ClosureLiteral":
            params = []
            for p in kids(n, "parameter"):
                params.append(node(CLO + "InferredClosureParameterDeclaration", {"name": p.get("name"), "resolveInfo": p.get("name")},
                                   {"type": node(BL + "UndefinedType")}))
            return node(CLO + "ClosureLiteral", children={"parameter": params, "body": self.fix(kid(n, "body"))})

        return self.copy(n)

    def expression_marker(self, name, args, n):
        what = f"{name}(..) at {n.get('reference', '')}"
        if name == "BD":
            v = self.string(args[0], what).strip()
            v = v[:-2] if v.endswith("bd") else v
            try:
                float(v)
            except ValueError:
                raise Stop(f"{what}: '{v}' is no decimal number")
            if "." not in v:  # the stored form always has a decimal point: 0.0bd
                v += ".0"
            return node(OF + "DezimalLiteral", {"value": v + "bd"})
        if name == "SERVERDATE":
            return node(OF + "DateLiteral", {"fromServer": True})
        if name == "SERVERDATETIME":
            return node(OF + "DateTimeLiteral", {"fromServer": True})
        if name == "DATE":
            return node(OF + "DateLiteral", {"fromServer": False, "year": self.integer(args[0], what),
                                             "month": self.integer(args[1], what), "day": self.integer(args[2], what)})
        if name == "DATETIME":
            keys = ("year", "month", "day", "hour", "minute", "second")
            vals = {k: self.integer(a, what) for k, a in zip(keys, args)}
            return node(OF + "DateTimeLiteral", dict(fromServer=False, **vals))
        if name == "STATUS":
            return node(OF + "StatusConstReference", children={
                "operation": node(OF + "StatusElementReference", refs={"statusElement": self.string(args[1], what)})},
                refs={"status": self.string(args[0], what)})
        if name == "OF":
            return node(OF + "StatusOfOperator", children={
                "statusLeftSide": self.fix(args[0]),
                "statusElements": [node(OF + "StatusElementReference", refs={"statusElement": self.string(a, what)}) for a in args[1:]]})
        if name in ("EQ", "NE"):
            return node(BL + ("NPEEqualsExpression" if name == "EQ" else "NPENotEqualsExpression"),
                        children={"leftExpression": self.fix(args[0]), "rightExpression": self.fix(args[1])})
        if name == "FMT":
            return self.fmt(args, what)
        if name in ("CALL", "CALL_WITH"):
            sess, rest = (args[0], args[1:]) if name == "CALL_WITH" else (None, args)
            return node(OF + "OperationCall", children={"actualArgument": [self.fix(a) for a in rest[2:]],
                                                        "sessionExpression": self.fix(sess) if sess else None},
                        refs={"runtimeHandledObject": self.string(rest[0], what), "baseMethodDeclaration": self.string(rest[1], what)})
        if name == "ISNULLKEY":
            return node(BL + "DotExpression", children={"operand": self.fix(args[0]), "operation": node(OF + "IsNull")})
        if name in ("KEY", "META"):
            operand, prop_name = self.split_property(args[0], what)
            op = node(OF + ("BPRefIdReference" if name == "KEY" else "BPMetaReference"), refs={"businessProperty": prop_name})
            return node(BL + "DotExpression", children={"operand": operand, "operation": op})
        if name == "ROLE":
            return node(OF + "PermissionHasReference", refs={"evaluatePermission": self.string(args[0], what)})
        if name in TERM_PARAMS:
            return node(OF + TERM_PARAMS[name])
        if name == "SELECTED":
            props = {"andDerived": self.boolean(args[1], what)} if len(args) > 1 else None
            return node(OF + "SelectedObject", props, refs={"object": self.string(args[0], what)})
        if name == "SESSION_ENTITIES":
            mode = self.string(args[1], what) if len(args) > 1 else "checked_out"
            if mode not in SESSION_MODES:
                raise Stop(f"{what}: mode must be one of {', '.join(SESSION_MODES)}")
            return node(OF + "CheckedOutEntities", {"mode": SESSION_MODES[mode]}, refs={"entity": self.string(args[0], what)})
        if name == "MERGE":
            src, dest, skind, dkind, integ = args[0], args[1], self.string(args[2], what), self.string(args[3], what), self.string(args[4], what)
            if skind not in MERGE_KINDS or dkind not in MERGE_KINDS or integ not in MERGE_SESSION:
                raise Stop(f"{what}: kinds are entity|list|ref, session is readonly|checkedout|none")
            return node(OF + "MergeInto", {"sourceObjType": skind, "destObjType": dkind, "sessionIntegration": MERGE_SESSION[integ]},
                        {"source": self.fix(src), "destination": self.fix(dest), "session": self.fix(args[5]) if len(args) > 5 else None})
        if name == "SQL":
            return self.sql(args, what)
        if name == "FIELD":
            return node(MM + "MappingReference", refs={"mappingSource": self.string(args[0], what), "fieldMapping": self.string(args[1], what)})
        if name == "LIKE":
            return node(MM + "LikeOperator", children={"operand": self.fix(args[0]), "target": self.fix(args[1])})
        if name == "IN":
            return node(MM + "InOperation", children={"operand": self.fix(args[0]), "targetList": self.fix(args[1])})
        if name == "OPTIONAL":
            return node(MM + "OptionalOperator", children={"expression": self.fix(args[0])})
        if name in ("GET", "WHERE"):
            return self.query(name, args, [])
        if name in ("PRE", "PREW", "GUARD", "LOG", "SESSION_OP", "SAVE", "DELETE", "VALIDATION", "FAIL_IN", "DONE", "PAGE", "PUSH", "QUEUE_NEXT"):
            raise Stop(f"{what} is a statement marker; write it as a statement of its own")
        raise Stop(f"unknown marker or unresolved method {what}")

    def tokens(self, text):
        parts = (text or "").split(".")
        if parts[0] in self.locals or parts[0] in self.bigdec_names:
            e = node(BL + "VariableReference", refs={"variableDeclaration": parts[0]})
        elif parts[0] in self.containers:
            target, concept = self.containers[parts[0]]
            e = node(concept, refs={"variableDeclaration": target})
        else:
            e = node(BL + "LocalPropertyReference", refs={"property": parts[0]})
        for p in parts[1:]:
            e = node(BL + "DotExpression", children={"operand": e, "operation": node(BL + "PropertyReference", refs={"property": p})})
        return e

    def copy(self, n):
        d = {"concept": fq(n)}
        props = [{"name": p["name"], "value": p["value"]} for p in n.get("properties", [])
                 if p.get("value") is not None and p["name"] not in SKIP_PROPS and p.get("declared", True) is not False
                 and not p.get("isDefault")]
        if props:
            d["properties"] = props
        refs = []
        for r in n.get("references", []):
            if unresolved(r):
                raise Stop(f"unresolved {r['role']} -> '{r.get('target')}' at {short(n)}")
            tr = r["targetReference"]
            by_name = tr in self.inside or tr in self.replaced
            refs.append({"role": r["role"], "target": r.get("target") if by_name else tr})
        if refs:
            d["references"] = refs
        ch = []
        for c in n.get("children", []):
            nodes = [self.fix(x) for x in c.get("nodes", [])]
            if nodes:
                ch.append({"role": c["role"], "nodes": nodes})
        if ch:
            d["children"] = ch
        return d


def load(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    if isinstance(d, dict) and "ok" in d and "data" in d:
        d = d["data"]
    return load(d) if isinstance(d, str) else d


def convert_root(root, repo_types, only):
    root_refs = {x["reference"]: fq(x) for x in walk(root)}
    rc = fq(root)
    rows, errors = [], []
    members = [m for m in kids(root, "member") + kids(root, "content") if not only or m.get("name") in only]
    replaced = set()
    for m in members:
        if fq(m) in (BL + "ConstructorDeclaration", OF + "OFXTestMethod"):
            replaced |= {x["reference"] for x in walk(kid(m, "body"))}
        elif fq(m).endswith("MethodDeclaration"):
            replaced |= {x["reference"] for x in walk(m)}
    bigdec_props = set()
    for bp in kids(root, "businessProperties"):
        t = kid(bp, "type")
        if t is not None and fq(t) == BL + "ClassifierType" and (ref(t, "classifier") or {}).get("target") == "BigDecimal":
            bigdec_props.add(bp.get("name"))
    if rc == OF + "Command":
        return convert_command(root, root_refs)
    for m in kids(root, "member") + kids(root, "content"):
        mc = fq(m)
        if only and m.get("name") not in only:
            continue
        if not (mc.endswith("MethodDeclaration") or mc in (BL + "ConstructorDeclaration", OF + "OFXTestMethod")):
            continue
        try:
            conv = Converter(m, root_refs, replaced, bigdec_props)
            if mc in (BL + "ConstructorDeclaration", OF + "OFXTestMethod"):
                body = kid(m, "body")
                rows.append((m.get("name") + " (body)", body["reference"], conv.fix(body)))
                continue
            out = conv.fix(m)
            if mc == BL + "InstanceMethodDeclaration":
                if rc == OF + "Service":
                    out["concept"] = OF + "ServiceInstanceMethodDeclaration"
                elif rc == MM + "Repository":
                    out["concept"] = MM + "RepositoryInstanceMethodDeclaration"
                    out.setdefault("properties", []).append({"name": "repoMethodType", "value": repo_types.get(m.get("name"), "READONLY")})
            rows.append((m.get("name"), m["reference"], out))
        except Stop as e:
            errors.append(f"{m.get('name')}: {e}")
    return rows, errors


def convert_command(root, root_refs):
    """Replace the body of every function of a command (command init, page init, scopes, conclusions, ...)."""
    st = Structure()
    containers = {}
    for role, concept in (("parameter", OF + "ContainerParamReference"), ("variable", OF + "ContainerVariableReference")):
        for d in kids(root, role):
            containers[d.get("name")] = (d["reference"], concept)
    functions = [x for x in walk(root) if x is not root and kid(x, "body") is not None
                 and st.fits(fq(x), BL + "ConceptFunction")]
    replaced = {y["reference"] for f in functions for y in walk(kid(f, "body"))}
    rows, errors = [], []
    for f in functions:
        body = kid(f, "body")
        if not kids(body, "statement"):
            continue
        label = f.get("name") or fq(f).rsplit(".", 1)[-1]
        try:
            conv = Converter(f, root_refs, replaced, set(), containers)
            rows.append((f"{label} (body)", body["reference"], conv.fix(body)))
        except Stop as e:
            errors.append(f"{label}: {e}")
    return rows, errors


def main(argv):
    args, repo_types, only = argv[1:], {}, set()
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 0 if args else 2
    dump = args.pop(0)
    while args:
        a = args.pop(0)
        if a == "--repo-type":
            k, _, v = args.pop(0).partition("=")
            repo_types[k] = v
        elif a == "--only":
            only.add(args.pop(0))
        else:
            print(f"unknown option {a}", file=sys.stderr)
            return 2
    root = load(dump)
    rows, errors = convert_root(root, repo_types, only)
    for e in errors:
        print("error:", e, file=sys.stderr)
    st = Structure()
    rc = 1 if errors else 0
    outdir = tempfile.mkdtemp(prefix="moai-text2of-")
    for name, target, bp in rows:
        chk = Checker(st)
        chk.node(bp, f"{name}")
        if report(chk):
            rc = 1
            continue
        path = os.path.join(outdir, target.rsplit("/", 1)[-1] + ".json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(bp, f, ensure_ascii=False, separators=(",", ":"))
        print(f"{name} | {target} | {path}")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
