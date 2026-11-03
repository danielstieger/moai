"""scaffold.py tests: TestDaten and the test suite of an aggregate."""
from .bausteine import cap, lower
from .domain import domain, positions_of
from .registry import Ergebnis, Java, generator


def sample(p):
    """Readable test value as Java with markers, or None (the developer sets it)."""
    if "beispiel" in p:
        return p["beispiel"]
    t = p.get("typ")
    if t == "string":
        lo = (p.get("laenge") or [0, 0])[0]
        return '"' + (p.get("kurz", cap(p["name"])) + " 1").ljust(lo, "x") + '"'
    if t == "int":
        return str(max(1, (p.get("bereich") or [1, 1])[0]))
    return {"LocalDate": "SERVERDATE()", "DateTime": "SERVERDATETIME()", "BigDecimal": 'BD("10.00")'}.get(t)


@generator("tests", "scaffold.py tests SPEC [-o DIR]",
           "the same specification: service TestDaten (baue<X>, erzeuge<X> with CS.COMMIT) and <Bereich>Tests (per "
           "transition success and rejection, persistence read back in a fresh custom session; \"testfaelle\" adds your own)")
def tests(spec, args=()):
    model = domain(spec).model   # validates the specification the same way
    a, namen = spec["aggregat"], spec.get("namen", {})
    agg, var = a["name"], lower(a["name"])
    repo, service = namen.get("repo", agg + "Repo"), namen.get("service", agg + "Service")
    suite = namen.get("testsuite", cap(spec["bereich"]) + "Tests")
    tmodel = namen.get("testmodell", model.rsplit(".", 1)[0] + ".tests")
    open_values = []

    def builder(name, props, extra=(), param=None):
        v = lower(name)
        lines = [f"public {name} baue{name}({'int nummer' if param else ''}) {{", f"  {name} {v} = new {name}();"]
        for p in props:
            if p.get("typ") == "status" and "beispiel" not in p:
                continue  # the on-creation element is a valid test value
            val = "nummer" if param and p["name"] == param else sample(p)
            if val is None:
                open_values.append(f"{name}.{p['name']}")
                continue
            lines.append(f"  {v}.{p['name']} = {val};")
        lines += [f"  {x}" for x in extra] + [f"  return {v};", "}"]
        return lines

    positions = positions_of(a)
    extra = []
    java = []
    for pos in positions:
        pe = pos["entity"]
        pnum = next((p["name"] for p in pe.get("properties", []) if p.get("typ") == "int" and "nummer" in p["name"].lower()), None)
        java += builder(pe["name"], pe.get("properties", []), param=pnum or "_")
        extra += [f"{var}.{pos['property']}.add(baue{pe['name']}({n}));" for n in (1, 2)]
    java = builder(agg, a.get("properties", []), extra) + java
    java += [f"public {agg} erzeuge{agg}() {{",
             f"  final {agg} {var} = baue{agg}();",
             f'  SESSION_OP("{repo}", "checkin", "Testdaten {agg}", {var});',
             '  CALL("CS", "COMMIT");',
             f"  return {var};", "}"]

    status = a.get("status")
    cases = []
    names = [w[0] for w in status["werte"]] if status else []
    for t in spec.get("uebergaenge", []):
        call_args = "".join(", " + x for x in [var] + t.get("argumente", []))
        set_from = [] if t["von"][0] == names[0] else [f'{var}.status = STATUS("{status["name"]}", "{t["von"][0]}");']
        cases.append((f"{agg} {t['name']}", [f'{agg} {var} = CALL("TestDaten", "baue{agg}");', *set_from,
                                             f'CALL("{service}", "{t["name"]}"{call_args});',
                                             f'assert OF({var}.status, "{t["nach"]}");']))
        wrong = next((s for s in names if s not in t["von"] and s != t["nach"]), None)
        if wrong:
            kurz = next((w[2] for w in status["werte"] if w[0] == wrong and len(w) > 2), cap(wrong.lower()))
            cases.append((f"{agg} {t['name']} im Status {kurz} wird abgelehnt",
                          [f'{agg} {var} = CALL("TestDaten", "baue{agg}");',
                           f'{var}.status = STATUS("{status["name"]}", "{wrong}");',
                           'FAIL_IN("OFXAbortedException");',
                           f'CALL("{service}", "{t["name"]}"{call_args});']))
    check = [f'{agg} gelesen = CALL_WITH(CALL("CS", "CREATE"), "{repo}", "get", gespeichert.id);',
             "assert gelesen != null;"]
    check += [f"assert gelesen.{pos['property']}.size() == 2;" for pos in positions]
    first = next((p["name"] for p in a.get("properties", []) if p.get("typ") == "string"), None)
    if first:
        check.append(f"assert EQ(gelesen.{first}, gespeichert.{first});")
    cases.append((f"{agg} speichern und in frischer Session zurücklesen",
                  [f'{agg} gespeichert = CALL_WITH(CALL("CS", "CREATE"), "TestDaten", "erzeuge{agg}");',
                   "assert gespeichert.id > 0;", *check]))
    cases += [(f["name"], f["java"].splitlines()) for f in spec.get("testfaelle", [])]

    config = spec.get("testConfig")
    datum = spec.get("testDatum")  # [y, m, d, h, mi, s]: DEFAULT_DATETIME, the date the tests run on
    options = {"options": {"concept": "OFXTestSuitDefaultDateTimeOption", "properties": dict(zip(
        ("year", "month", "day", "hour", "minute", "second"), map(str, datum)))}} if datum else {}
    troots = [("testdaten", {"concept": "Service", "properties": {"isStatic": "true", "nestedName": "TestDaten",
                                                                    "name": "TestDaten", "resolveInfo": "TestDaten"},
                             "children": {"visibility": "PublicVisibility"}}),
              ("testsuite", {"concept": "OFXTestSuit", "properties": {"name": suite},
                             **({"references": {"configuration": config}} if config else {}),
                             "children": {**options, "content": [{"concept": "OFXTestMethod", "properties": {"name": n},
                                                       "children": {"returnType": "VoidType", "body": "StatementList"}}
                                                      for n, _ in cases]}})]
    jfiles = [Java("testdaten", "\n".join(java) + "\n", "TestDaten: parse as CLASS_CONTENT into its member role; text2of.py")]
    for i, (n, body) in enumerate(cases, 1):
        jfiles.append(Java(f"test-{i:02d}", "\n".join(body) + "\n",
                           f"'{n}': parse as STATEMENTS into the body of this test method"))
    jfiles.append(Java("", "", f"then text2of.py on the printed {suite} (one row per test body)"))
    notes = [f"Imports of {tmodel}: {model}, org.modellwerkstatt.wbkit.shared.testing (CS),"
             " org.modellwerkstatt.objectflow.runtime (OFXAbortedException); module dependency"
             " org.modellwerkstatt.wbkit."]
    if not config:
        notes.append(f"{suite} has no configuration yet: set it to the test OFXConfig (conventions: CS must be found).")
    if open_values:
        notes.append("No test value for " + ", ".join(open_values) + ": set them in TestDaten (\"beispiel\" in the spec).")
    return Ergebnis(tmodel, troots, jfiles, notes)
