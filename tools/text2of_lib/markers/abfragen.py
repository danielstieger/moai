"""ManMap: queries, save and delete"""
from ..knoten import BL, MM, Stop, fq, kid, kids, node, prop
from ..registry import marker, rewrite


def _query(conv, name, args, chain):
    if name == "GET":
        mapping, key, ro = args
        ops = [node(MM + "GetQuery", children={"argument": conv.fix(key)})]
    else:
        mapping, ro, flt = args
        ops = [node(MM + "WhereQuery", children={"filter": conv.fix(flt)})]
    for callee, cargs in chain:
        if callee == "SORTBY":
            direction = "ASC" if conv.boolean(cargs[1], "SORTBY direction") else "DESC"
            ops.append(node(MM + "SortByQuery", {"sortDirection": direction}, {"toComparable": conv.fix(cargs[0])}))
        elif callee == "LIMIT":
            ops.append(node(MM + "LimitQuery", children={"count": conv.fix(cargs[0])}))
        else:
            raise Stop(f"unknown query operation .{callee}(); use .SORTBY(FIELD(..), asc) or .LIMIT(n)")
    return node(MM + "QueryFromMap", {"readOnly": conv.boolean(ro, f"{name} read-only flag")},
                {"queryOperation": ops}, {"entityMapping": conv.string(mapping, f"{name} mapping")})


@marker("GET", 'GET("Map",key,ro)', "Map get(key), ro = true (read-only) / false (checkout)", args=3)
def get(conv, args, what):
    return _query(conv, "GET", args, [])


@marker("WHERE", 'WHERE("Map",ro,filter) .SORTBY(FIELD,asc) .LIMIT(n)', "Map where(filter) sortBy limit", args=3)
def where(conv, args, what):
    return _query(conv, "WHERE", args, [])


@rewrite(BL + "UnknownInstanceMethodCall", BL + "DotExpression")
def query_chain(conv, n):
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
    name, args = conv.marker(n)
    return _query(conv, name, args, chain) if name in ("GET", "WHERE") else None


@marker("FIELD", 'FIELD("Map","field")',
        "field of a mapping, in a filter or sort; --persistenz DUMP binds it directly (`id` is ambiguous next to a reference mapping)",
        args=2)
def field(conv, args, what):
    mapping, name = conv.string(args[0], what), conv.string(args[1], what)
    return node(MM + "MappingReference", refs={"mappingSource": mapping, "fieldMapping": conv.fields.get((mapping, name), name)})


@marker("LIKE", "LIKE(a,b)", "a like b", args=2)
def like(conv, args, what):
    return node(MM + "LikeOperator", children={"operand": conv.fix(args[0]), "target": conv.fix(args[1])})


@marker("IN", "IN(FIELD(..),list)", "field in list", args=2)
def in_(conv, args, what):
    return node(MM + "InOperation", children={"operand": conv.fix(args[0]), "targetList": conv.fix(args[1])})


@marker("OPTIONAL", "OPTIONAL(pred)", "predicate dropped when its operand is null", args=1)
def optional(conv, args, what):
    return node(MM + "OptionalOperator", children={"expression": conv.fix(args[0])})


SAVE_OPTIONS = {"INSERT": "InsertSaveOption", "UPDATE": "UpdateSaveOption", "BATCH": "BatchSaveOption"}


def _save(conv, name, concept, args):
    opts = []
    for a in args[2:]:
        o = conv.string(a, f"{name} option")
        if o not in SAVE_OPTIONS:
            raise Stop(f"{name} option '{o}' is not one of INSERT, UPDATE, BATCH")
        opts.append(node(MM + SAVE_OPTIONS[o]))
    return node(MM + concept, children={"expression": conv.fix(args[1]), "options": opts},
                refs={"entityMapping": conv.string(args[0], f"{name} mapping")})


@marker("SAVE", 'SAVE("Map",x[,"INSERT"|"UPDATE"|"BATCH"])', "save with Map x", args=(2, None), statement=True)
def save(conv, args, what):
    return _save(conv, "SAVE", "SaveWithMap", args)


@marker("DELETE", 'DELETE("Map",x)', "delete with Map x", args=(2, None), statement=True)
def delete(conv, args, what):
    return _save(conv, "DELETE", "DeleteWithMap", args)
