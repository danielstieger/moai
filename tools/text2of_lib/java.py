"""Plain Java the parser leaves unresolved: property access, String, List<T>, new ArrayList<T>(), lambdas.

Loaded after markers/: handlers of the same concept run in import order.
"""
import json

from .knoten import BL, CLO, COL, OF, Stop, fq, kid, kids, node, prop, ref, short, unresolved
from .methoden import BIGDEC_METHODS, bigdec_call, method_op
from .registry import rewrite


@rewrite(BL + "StatementList")
def statement_list(conv, n):
    """Statement list with FAIL_IN: the attribute goes on the following statement."""
    out, pending = [], None
    for st in kids(n, "statement"):
        if fq(st) == BL + "ExpressionStatement":
            name, args = conv.marker(kid(st, "expression"))
            if name == "FAIL_IN":
                ch = {"contains": node(BL + "StringLiteral", {"value": conv.string(args[1], "FAIL_IN text")})} if len(args) > 1 else None
                pending = node(OF + "OFXTestFailInAttribue", children=ch,
                               refs={"classifier": conv.string(args[0], "FAIL_IN exception")})
                continue
        f = conv.fix(st)
        if pending is not None:
            f.setdefault("children", []).append({"role": "smodelAttribute", "nodes": [pending]})
            pending = None
        out.append(f)
    if pending is not None:
        raise Stop("FAIL_IN must be followed by a statement")
    return node(BL + "StatementList", children={"statement": out})


@rewrite(BL + "ExpressionStatement")
def expression_statement(conv, n):
    name, args = conv.marker(kid(n, "expression"))
    return conv.statement_marker(name, args) if name else None


@rewrite(BL + "UnknownInstanceMethodCall")
def unknown_instance_call(conv, n):
    operand = kid(n, "operand")
    return node(BL + "DotExpression", children={
        "operand": conv.fix(operand),
        "operation": method_op(conv, prop(n, "callee"), operand, kids(n, "actualArgument"))})


@rewrite(BL + "UnknownDotCall")
def unknown_dot_call(conv, n):
    tokens = prop(n, "tokens") or ""
    callee, args = prop(n, "callee"), kids(n, "actualArgument")
    if tokens.rsplit(".", 1)[-1] in conv.bigdec_props | conv.bigdec_names and callee in BIGDEC_METHODS:
        op = bigdec_call(conv, callee, args)
    else:
        op = method_op(conv, callee, None, args)
    return node(BL + "DotExpression", children={"operand": conv.tokens(tokens), "operation": op})


@rewrite(BL + "UnknownNameRef")
def unknown_name(conv, n):
    return conv.tokens(prop(n, "tokens"))


@rewrite(BL + "UnknownNew")
def unknown_new(conv, n):
    """new ArrayList<T>() the parser could not resolve (java.util not visible in the model)."""
    if (prop(n, "className") or "").rsplit(".", 1)[-1] != "ArrayList":
        return None
    types = kids(n, "typeParameter") or kids(n, "typeArgument")
    if len(types) != 1:
        raise Stop(f"new ArrayList needs its element type, new ArrayList<T>(): {short(n)}")
    if kids(n, "actualArgument"):
        raise Stop(f"new ArrayList with arguments is not supported, only new ArrayList<T>(): {short(n)}")
    return node(BL + "GenericNewExpression", children={"creator": node(COL + "ListCreatorWithInit", children={
        "elementType": conv.fix(types[0])})})


@rewrite(BL + "DotExpression")
def dot_expression(conv, n):
    op, operand = kid(n, "operation"), kid(n, "operand")
    if fq(op) == BL + "FieldReferenceOperation" and unresolved(ref(op, "fieldDeclaration")):
        return node(BL + "DotExpression", children={
            "operand": conv.fix(operand), "operation": node(BL + "PropertyReference", refs={"property": op.get("name")})})
    if fq(op) == BL + "InstanceMethodCallOperation" and unresolved(ref(op, "baseMethodDeclaration")):
        return node(BL + "DotExpression", children={
            "operand": conv.fix(operand), "operation": method_op(conv, op.get("name"), operand, kids(op, "actualArgument"))})
    return None


@rewrite(BL + "VariableReference")
def variable_reference(conv, n):
    r = ref(n, "variableDeclaration")
    for target, concept in conv.containers.values():
        if r is not None and r.get("targetReference") == target:
            return node(concept, refs={"variableDeclaration": target})
    if unresolved(r) and n.get("name") == "session":
        return node(OF + "Session")
    if unresolved(r):
        return node(BL + "LocalPropertyReference", refs={"property": n.get("name")})
    target = r["targetReference"]
    if target not in conv.inside and conv.root_refs.get(target) in (BL + "ParameterDeclaration", BL + "LocalVariableDeclaration"):
        # the parser bound the name to a declaration of another member, e.g. a constructor parameter named like a property
        if n.get("name") in conv.locals or r.get("target") in conv.locals:
            return node(BL + "VariableReference", refs={"variableDeclaration": r.get("target")})
        if r.get("target") in conv.root_props:
            return node(BL + "LocalPropertyReference", refs={"property": r.get("target")})
        raise Stop(f"'{r.get('target')}' at {short(n)} is bound to a variable of another member and is neither a local "
                   "nor a property of this root")
    if target not in conv.inside and target in conv.replaced:
        # bound to a declaration of another member (parser): rebind by name in this member
        return node(BL + "VariableReference", refs={"variableDeclaration": r.get("target")})
    return None


@rewrite(BL + "ClassifierType")
def classifier_type(conv, n):
    r = ref(n, "classifier") or {}
    tr = r.get("targetReference") or ""
    if tr.endswith("~String") or r.get("target") == "String":
        return node(BL + "StringType")
    params = kids(n, "parameter")
    if tr.endswith(("~List", "~ArrayList", "~Collection")) or (unresolved(r) and n.get("name", "").startswith("List") and len(params) == 1) \
            or (unresolved(r) and len(params) == 1):
        return node(COL + "ListType", children={"elementType": conv.fix(params[0])})
    return None


@rewrite(BL + "GenericNewExpression")
def new_arraylist(conv, n):
    cr = kid(n, "creator")
    if fq(cr) == BL + "ClassCreator" and "~ArrayList" in json.dumps(cr.get("references", [])):
        return node(BL + "GenericNewExpression", children={"creator": node(COL + "ListCreatorWithInit", children={
            "elementType": [conv.fix(x) for x in kids(cr, "typeParameter")]})})
    return None


@rewrite(CLO + "ClosureLiteral")
def closure(conv, n):
    params = []
    for p in kids(n, "parameter"):
        params.append(node(CLO + "InferredClosureParameterDeclaration", {"name": p.get("name"), "resolveInfo": p.get("name")},
                           {"type": node(BL + "UndefinedType")}))
    return node(CLO + "ClosureLiteral", children={"parameter": params, "body": conv.fix(kid(n, "body"))})
