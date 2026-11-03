"""Collections and BigDecimal operations written as Java method calls: coll.where(l), a.add(b), ...

New operation: add it to one of the tables; a call that is in no table stays a plain method call by name.
"""
from .knoten import BL, COL, Stop, kids, node

BIGDEC = "6354ebe7-c22a-4a0f-ac54-50b52ab9b065/java:java.math(JDK/)/~BigDecimal"
STRING_CONTAINS = "6354ebe7-c22a-4a0f-ac54-50b52ab9b065/java:java.lang(JDK/)/~String.contains%28java.lang.CharSequence%29"
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


def bigdec_call(conv, callee, args):
    return node(BL + "InstanceMethodCallOperation", refs={"baseMethodDeclaration": BIGDEC_METHODS[callee]},
                children={"actualArgument": [conv.fix(a) for a in args]})


def _need(callee, args, count, form):
    if len(args) != count:
        raise Stop(f".{callee}: {len(args)} argument(s) given, write {form}")


def method_op(conv, callee, operand, args):
    """The operation of `operand.callee(args)`."""
    if callee in BIGDEC_METHODS and (callee not in COLL_ONEARG or conv.is_bigdec(operand)
                                     or any(conv.is_bigdec(a) for a in args)):
        return bigdec_call(conv, callee, args)
    if callee in COLL_CLOSURE:
        _need(callee, args, 1, f"coll.{callee}(x -> ..)")
        return node(COL + COLL_CLOSURE[callee], children={"closure": conv.fix(args[0])})
    if callee in COLL_NOARG:
        return node(COL + COLL_NOARG[callee])
    if callee in COLL_ONEARG:
        _need(callee, args, 1, f"coll.{callee}(element); on a string use CONTAINS(s,x)" if callee == "contains" else f"coll.{callee}(element)")
        return node(COL + COLL_ONEARG[callee], children={"argument": conv.fix(args[0])})
    if callee == "foldLeft":
        _need(callee, args, 2, "coll.foldLeft(seed, (acc, x) -> ..)")
        seed, closure = args
        if conv.is_bigdec(seed):  # the accumulator of a BigDecimal fold is a BigDecimal
            params = kids(closure, "parameter")
            if params:
                conv.bigdec_names.add(params[0].get("name"))
        return node(COL + "FoldLeftOperation", children={"seed": conv.fix(seed), "closure": conv.fix(closure)})
    if callee == "sortBy":
        _need(callee, args, 2, "coll.sortBy(x -> .., true)")
        return node(COL + "SortOperation", children={"closure": conv.fix(args[0]), "ascending": conv.fix(args[1])})
    return node(BL + "InstanceMethodCallOperation", refs={"baseMethodDeclaration": callee},
                children={"actualArgument": [conv.fix(a) for a in args]})
