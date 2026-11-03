"""Calls, session and references"""
from ..knoten import BL, OF, Stop, node
from ..registry import marker


def _call(conv, sess, rest, what):
    return node(OF + "OperationCall", children={"actualArgument": [conv.fix(a) for a in rest[2:]],
                                                "sessionExpression": conv.fix(sess) if sess else None},
                refs={"runtimeHandledObject": conv.string(rest[0], what), "baseMethodDeclaration": conv.string(rest[1], what)})


@marker("CALL", 'CALL("Comp","m",args)', "# Comp.m(..)", args=(2, None))
def call(conv, args, what):
    return _call(conv, None, args, what)


@marker("CALL_WITH", 'CALL_WITH(sess,"Comp","m",args)', "#+ with sess Comp.m(..); `session` is the session of the context", args=(3, None))
def call_with(conv, args, what):
    return _call(conv, args[0], args[1:], what)


@marker("SESSION_OP", 'SESSION_OP("Comp","m","text",args)', "session operation add # Comp.m(..) // 'text'", args=(3, None), statement=True)
def session_op(conv, args, what):
    call_node = node(OF + "OperationCall", children={"actualArgument": [conv.fix(a) for a in args[3:]]},
                     refs={"runtimeHandledObject": conv.string(args[0], "SESSION_OP component"),
                           "baseMethodDeclaration": conv.string(args[1], "SESSION_OP method")})
    return node(OF + "SessionOperationAdd", children={
        "operationCall": call_node, "message": node(BL + "StringLiteral", {"value": conv.string(args[2], "SESSION_OP text")})})


@marker("ISNULLKEY", "ISNULLKEY(KEY(x.ref))", "x.ref#Key.isNullKey", args=1)
def is_null_key(conv, args, what):
    return node(BL + "DotExpression", children={"operand": conv.fix(args[0]), "operation": node(OF + "IsNull")})


def _on_property(conv, args, what, concept):
    operand, prop_name = conv.split_property(args[0], what)
    return node(BL + "DotExpression", children={"operand": operand, "operation": node(OF + concept, refs={"businessProperty": prop_name})})


@marker("KEY", "KEY(x.ref)", "x.ref#Key", args=1)
def key(conv, args, what):
    return _on_property(conv, args, what, "BPRefIdReference")


@marker("META", "META(x.prop).setEnabled(..)", "x.prop#Meta.setEnabled(..)", args=1)
def meta(conv, args, what):
    return _on_property(conv, args, what, "BPMetaReference")


@marker("ROLE", 'ROLE("Name")', "role Name()", args=1)
def role(conv, args, what):
    return node(OF + "PermissionHasReference", refs={"evaluatePermission": conv.string(args[0], what)})


@marker("SELECTED", 'SELECTED("Type"[,true])', "getSelected(Type) (+ derived)", args=(1, 2))
def selected(conv, args, what):
    props = {"andDerived": conv.boolean(args[1], what)} if len(args) > 1 else None
    return node(OF + "SelectedObject", props, refs={"object": conv.string(args[0], what)})


SESSION_MODES = {"checked_out": "checked_out", "keys_of_checked_out": "ckecked_out_keys", "all": "all", "keys_of_all": "all_keys"}


@marker("SESSION_ENTITIES", 'SESSION_ENTITIES("Type","all")', "session entities (checked_out|keys_of_checked_out|all|keys_of_all)", args=(1, 2))
def session_entities(conv, args, what):
    mode = conv.string(args[1], what) if len(args) > 1 else "checked_out"
    if mode not in SESSION_MODES:
        raise Stop(f"{what}: mode must be one of {', '.join(SESSION_MODES)}")
    return node(OF + "CheckedOutEntities", {"mode": SESSION_MODES[mode]}, refs={"entity": conv.string(args[0], what)})


MERGE_KINDS = {"entity", "list", "ref"}
MERGE_SESSION = {"readonly": "session_readonly", "checkedout": "session_checkedout", "none": "not_consider_session"}


@marker("MERGE", 'MERGE(src,dest,"entity","list","readonly"[,sess])', "session merge (entity|list|ref; readonly|checkedout|none)", args=(5, 6))
def merge(conv, args, what):
    src, dest, skind, dkind, integ = args[0], args[1], conv.string(args[2], what), conv.string(args[3], what), conv.string(args[4], what)
    if skind not in MERGE_KINDS or dkind not in MERGE_KINDS or integ not in MERGE_SESSION:
        raise Stop(f"{what}: kinds are entity|list|ref, session is readonly|checkedout|none")
    return node(OF + "MergeInto", {"sourceObjType": skind, "destObjType": dkind, "sessionIntegration": MERGE_SESSION[integ]},
                {"source": conv.fix(src), "destination": conv.fix(dest), "session": conv.fix(args[5]) if len(args) > 5 else None})
