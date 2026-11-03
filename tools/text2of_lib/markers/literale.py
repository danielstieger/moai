"""Literals and constants"""
from ..knoten import OF, Stop, node
from ..registry import marker


@marker("BD", 'BD("1.50")', "decimal literal", args=1)
def bd(conv, args, what):
    v = conv.string(args[0], what).strip()
    v = v[:-2] if v.endswith("bd") else v
    try:
        float(v)
    except ValueError:
        raise Stop(f"{what}: '{v}' is no decimal number")
    if "." not in v:  # the stored form always has a decimal point: 0.0bd
        v += ".0"
    return node(OF + "DezimalLiteral", {"value": v + "bd"})


@marker("SERVERDATE", "SERVERDATE()", "date of the server")
def server_date(conv, args, what):
    return node(OF + "DateLiteral", {"fromServer": True})


@marker("SERVERDATETIME", "SERVERDATETIME()", "date and time of the server")
def server_datetime(conv, args, what):
    return node(OF + "DateTimeLiteral", {"fromServer": True})


@marker("DATE", "DATE(y,m,d)", "fixed date (fromServer=false)", args=3)
def date(conv, args, what):
    return node(OF + "DateLiteral", {"fromServer": False, "year": conv.integer(args[0], what),
                                     "month": conv.integer(args[1], what), "day": conv.integer(args[2], what)})


@marker("DATETIME", "DATETIME(y,m,d,h,mi,s)", "fixed date and time", args=(3, 6))
def datetime(conv, args, what):
    keys = ("year", "month", "day", "hour", "minute", "second")
    vals = {k: conv.integer(a, what) for k, a in zip(keys, args)}
    return node(OF + "DateTimeLiteral", dict(fromServer=False, **vals))


@marker("STATUS", 'STATUS("Decl","ELEM")', "Decl.ELEM", args=2)
def status(conv, args, what):
    return node(OF + "StatusConstReference", children={
        "operation": node(OF + "StatusElementReference", refs={"statusElement": conv.string(args[1], what)})},
        refs={"status": conv.string(args[0], what)})
