#!/usr/bin/env python3
"""MoAI scaffolds: convention-compliant skeletons from a short JSON specification.

The MoWare conventions live in this generator; the specification only says what is specific. The tool writes
blueprints (checked against the structure export), method bodies as Java with markers (for text2of.py) and a plan
with the MCP steps in order. It calls no MPS itself. Call with `python3 -I`.

  scaffold.py domain SPEC [-o DIR]      aggregate: entities, status, persistence description, aggregate repository,
                                        <Aggregat>Service with one method per state transition
  scaffold.py tests SPEC [-o DIR]       the same specification: service TestDaten (baue<X>, erzeuge<X> with
                                        CS.COMMIT) and <Bereich>Tests (per transition success and rejection,
                                        persistence read back in a fresh custom session)
  scaffold.py suche SPEC [-o DIR]       search: <X>Filter and <X>SucheRepo (unit.read), SEARCH_CMD with page
                                        panes (unit); up to 3 criteria one page (form over table, ISSUE
                                        UPDATE, conclusions Suchen/Aktualisieren), more a wizard; result list of
                                        entities, taken over by an any cmd term handler with session merge
  scaffold.py commands SPEC [-o DIR]    owner, edit and transition commands with page panes (unit): <X> anlegen,
                                        <X> bearbeiten (key only, checkout, DISABLED form over the positions),
                                        GRAPH_EDIT_CMDs for head data and positions, one owner command per
                                        transition; with "suche" also the search page panes with the menu entries
  scaffold.py configs SPEC DUMP... [-o DIR]
                                        OFXConfigs from the wbkit templates (DUMP: print_node deep=true of
                                        baseconfig and of each wanted config in
                                        org.modellwerkstatt.wbkit.shared.configuration): firma.app replaced,
                                        sections not included dropped, database overwrites; Static Ressources
                                        AppRessourcen (platform RICH, labels and hotkeys of the conventions)

Specification (domain):
  {"firma": "org.firma", "app": "fuhrpark", "bereich": "rechnung",
   "aggregat": {"name": "Rechnung",
                "properties": [PROPERTY, ...],
                "status": {"name": "RechnungStatus",
                           "werte": [["ERFASST", "E", "Erfasst", "Rechnung ist erfasst"], ...]},   first = on creation
                "positionen": {"property": "positionen", "kurz": "Positionen",
                               "entity": {"name": "Rechnungsposition", "properties": [PROPERTY, ...]}}},
   "uebergaenge": [{"name": "freigeben", "von": ["ERFASST"], "nach": "FREIGEGEBEN"[, "meldung": "..."]}],
   "namen": {"repo": "RechnungsRepo", "service": "...", "persistenz": "...", "modell": "..."},   all optional
   "persistenzVorhanden": true,   further aggregate of the area: its mappings go into the existing description
   "testConfig": "Test",          tests: the test OFXConfig of the suite
   "suche": {"kriterien": [...], "spalten": [...], "ausschliessen": ["STORNIERT"][, "name": "Rechnungen suchen"]
             [, "ergebnisLabel": "Rechnungen"]},   search: property names of the aggregate (status included)
   "commands": {"bearbeitbar": ["ERFASST"][, "anlegen"|"bearbeiten"|"kopf"|"positionBearbeiten"
                |"positionHinzufuegen": "command name"]},   commands: status in which edit commands are enabled
   "configs": ["Test", "FX8"],    configs: templates to copy (default Test, FX8)
   "datenbank": {"url": "jdbc:mysql://...", "username": "...", "password": "..."}}   configs: overwrites

  PROPERTY: {"name": "rechnungsnummer", "typ": TYPE[, "kurz": "Rechnungsnr."][, "lang": "..."]
             [, "laenge": [1, 20]] (string) [, "bereich": [0, 365]] (int) [, "spalte": "RECHNUNGSNUMMER"]
             [, "felder": {"betrag": "BETRAG", ...}] (value object: column per component)
             [, "verweis": true] (cross reference to another aggregate's entity, column <NAME>_ID)
             [, "beispiel": "BD(\\"12.50\\")"] (tests: test value as Java with markers)}
  TYPE: string | int | LocalDate | DateTime | BigDecimal | name of a value object or entity (with felder / verweis)

Conventions applied: model <firma>.<app>.<bereich>.domain; names <Aggregat>Repo, <Aggregat>Service,
<Bereich>Persistenz (recommendations, overridable in "namen"); technical key `id` with sequence S_<TABLE>;
positions carry the parent key <aggregat>Id and are loaded explicitly; no delete method (objects are not
deleted physically, a status marks them); every transition checks its source status with a precondition
and then sets the target status.
"""
import sys

sys.dont_write_bytecode = True  # write nothing into the package (moai/ is a submodule in projects)

import json
import os
import re
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blueprint import Checker, Structure, expand, report  # noqa: E402

JODA = "37fdf88a-1025-4d01-864a-0bf987f72e6f/java:org.joda.time(org.modellwerkstatt.manmap.runtime/)/~"
STUB_TYPES = {"LocalDate": JODA + "LocalDate", "DateTime": JODA + "DateTime",
              "BigDecimal": "6354ebe7-c22a-4a0f-ac54-50b52ab9b065/java:java.math(JDK/)/~BigDecimal"}
PUBLIC = "PublicVisibility"


class SpecError(Exception):
    pass


def column(name):
    return re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name).upper()


def cap(name):
    return name[:1].upper() + name[1:]


def lower(name):
    return name[:1].lower() + name[1:]


def literal(text):
    return {"concept": "StringLiteral", "properties": {"value": text}}


# ---- blueprints ------------------------------------------------------------------------------------
def prop_type(p, where):
    t = p.get("typ")
    if t == "string":
        return "StringType"
    if t == "int":
        return "IntegerType"
    if t in STUB_TYPES:
        return {"concept": "ClassifierType", "references": {"classifier": STUB_TYPES[t]}}
    if t == "boolean":
        raise SpecError(f"{where}: boolean is no Business Property type; model a yes/no as a status")
    if isinstance(t, str) and t[:1].isupper() and ("felder" in p or p.get("verweis")):
        return {"concept": "ClassifierType", "references": {"classifier": t}}
    raise SpecError(f"{where}: type '{t}' unknown; a value object needs 'felder', an entity 'verweis': true")


def business_property(name, type_node, kurz, lang, options=()):
    return {"concept": "BusinessProperty",
            "properties": {"propertyName": name, "name": name},
            "children": {"shortDesc": literal(kurz), "longDesc": literal(lang), "type": type_node,
                         "propertyImplementation": {"concept": "DefaultPropertyImplementation", "children": {
                             "defaultGetAccessor": "DefaultGetAccessor",
                             "defaultSetAccessor": {"concept": "DefaultSetAccessor", "children": {"visibility": PUBLIC}}}},
                         "visibility": PUBLIC,
                         "propertyOption": list(options)}}


def spec_property(p, where):
    if not p.get("name"):
        raise SpecError(f"{where}: property needs a name")
    opts = []
    if "laenge" in p:
        opts.append({"concept": "LengthOption", "properties": {"min": str(p["laenge"][0]), "max": str(p["laenge"][1])}})
    if "bereich" in p:
        opts.append({"concept": "IRangeOption", "properties": {"start": str(p["bereich"][0]), "stop": str(p["bereich"][1])}})
    kurz = p.get("kurz", cap(p["name"]))
    return business_property(p["name"], prop_type(p, where), kurz, p.get("lang", kurz), opts)


def key_property(entity, table):
    return business_property("id", "IntegerType", "Id", f"Technischer Schlüssel {entity}",
                             ["KeyOption", {"concept": "AutoidOption", "children": {"sequenceName": literal("S_" + table)}}])


def entity(name, props, status=None, concept="Entity"):
    return {"concept": concept,
            "properties": {"isStatic": "true", "nestedName": name, "name": name, "resolveInfo": name},
            "children": {"visibility": PUBLIC,
                         "member": {"concept": "ConstructorDeclaration",
                                    "properties": {"nestedName": name, "name": name, "resolveInfo": name},
                                    "children": {"returnType": "VoidType", "body": "StatementList", "visibility": PUBLIC}},
                         **({"status": status} if status else {}),
                         "businessProperties": props}}


def status_decl(s, where):
    werte = s.get("werte") or []
    if not s.get("name") or not werte:
        raise SpecError(f"{where}: status needs a name and werte")
    elems = []
    for i, w in enumerate(werte):
        if not isinstance(w, list) or len(w) < 2:
            raise SpecError(f"{where}.werte[{i}]: [NAME, wert, kurz?, lang?]")
        kurz = w[2] if len(w) > 2 else cap(w[0].lower())
        e = {"concept": "StatusElement", "properties": {"value": w[1], "name": w[0]},
             "children": {"shortDescNew": literal(kurz), "longDescNew": literal(w[3] if len(w) > 3 else kurz)}}
        if i == 0:
            e["children"]["options"] = "OnCreationStatusElemOption"
        elems.append(e)
    return {"concept": "StatusDeclaration", "properties": {"name": s["name"]}, "children": {"element": elems}}


def field(prop, col):
    return {"concept": "FieldMapping", "references": {"property": prop}, "children": {"fieldName": literal(col)}}


def atom(p):
    col = p.get("spalte", column(p["name"]))
    if "felder" in p:
        return {"concept": "EmbeddedMapping", "references": {"property": p["name"]},
                "children": {"atomMpig": [field(k, v) for k, v in p["felder"].items()]}}
    if p.get("verweis"):
        return {"concept": "ReferenceMapping", "references": {"property": p["name"]},
                "children": {"keyMapping": field("id", p.get("spalte", column(p["name"]) + "_ID"))}}
    return field(p["name"], col)


def entity_mapping(name, ent, table, atoms):
    return {"concept": "EntityMapping", "properties": {"name": name}, "references": {"classConcept": ent},
            "children": {"tableName": literal(table), "tableOption": "OptimisticOption", "atomMpig": atoms}}


# ---- Java with markers -------------------------------------------------------------------------------
def repository_java(agg, var, pos):
    m = "Map" + agg
    lines = []
    for meth, ro in (("get", "true"), ("checkout", "false")):
        lines.append(f"public {agg} {meth}(int id) {{")
        lines.append(f'  {agg} {var} = GET("{m}", id, {ro});')
        if pos:
            pm, sort = "Map" + pos["entity"], pos["sort"]
            lines.append(f'  {var}.{pos["property"]} = WHERE("{pm}", {ro}, FIELD("{pm}", "{pos["key"]}") == id)'
                         f'.SORTBY(FIELD("{pm}", "{sort}"), true);')
        lines.append(f"  return {var};")
        lines.append("}")
    lines.append(f"public void checkin({agg} {var}) {{")
    lines.append(f'  SAVE("{m}", {var});')
    if pos:
        lines.append(f'  for ({pos["entity"]} p : {var}.{pos["property"]}) {{')
        lines.append(f'    p.{pos["key"]} = {var}.id;')
        lines.append(f'    SAVE("Map{pos["entity"]}", p);')
        lines.append("  }")
    lines.append("}")
    return "\n".join(lines) + "\n"


def service_java(agg, var, status, transitions, where):
    names = {w[0] for w in status["werte"]} if status else set()
    lines = []
    for i, t in enumerate(transitions):
        w = f"{where}[{i}]"
        if not status:
            raise SpecError(f"{w}: transitions need a status")
        if not t.get("name") or not t.get("von") or not t.get("nach"):
            raise SpecError(f"{w}: transition needs name, von, nach")
        for s in list(t["von"]) + [t["nach"]]:
            if s not in names:
                raise SpecError(f"{w}: status element '{s}' is not declared")
        von = ", ".join(f'"{s}"' for s in t["von"])
        msg = t.get("meldung", f"{cap(t['name'])} ist im Status %st nicht möglich.")
        lines += [f"public void {t['name']}({agg} {var}) {{",
                  "  if (VALIDATION()) {",
                  f'    PRE(OF({var}.status, {von}), "{msg}", {var}.status);',
                  "  }",
                  f'  {var}.status = STATUS("{status["name"]}", "{t["nach"]}");',
                  "}"]
    return "\n".join(lines) + "\n" if lines else ""


# ---- domain ------------------------------------------------------------------------------------------
def domain(spec):
    for k in ("firma", "app", "bereich", "aggregat"):
        if not spec.get(k):
            raise SpecError(f"$.{k} is missing")
    a, namen = spec["aggregat"], spec.get("namen", {})
    agg, var = a.get("name"), lower(a.get("name") or "")
    if not agg:
        raise SpecError("$.aggregat.name is missing")
    model = namen.get("modell", f"{spec['firma']}.{spec['app']}.{spec['bereich']}.domain")
    repo = namen.get("repo", agg + "Repo")
    service = namen.get("service", agg + "Service")
    persistenz = namen.get("persistenz", cap(spec["bereich"]) + "Persistenz")
    table = column(agg)

    props = [spec_property(p, f"$.aggregat.properties[{i}]") for i, p in enumerate(a.get("properties", []))]
    atoms = [field("id", "ID")] + [atom(p) for p in a.get("properties", [])]
    status = a.get("status")
    sdecl = None
    if status:
        sdecl = status_decl(status, "$.aggregat.status")
        props.append(business_property("status", {"concept": "StatusType", "references": {"status": status["name"]}},
                                       "Status", f"Status {agg}"))
        atoms.append(field("status", "STATUS"))
    pos = None
    roots = []
    if a.get("positionen"):
        pspec = a["positionen"]
        pe = pspec.get("entity") or {}
        if not pe.get("name") or not pspec.get("property"):
            raise SpecError("$.aggregat.positionen needs property and entity.name")
        ptable = column(pe["name"])
        key = var + "Id"
        pprops_spec = pe.get("properties", [])
        pprops = [key_property(pe["name"], ptable),
                  business_property(key, "IntegerType", cap(agg), f"Schlüssel {agg}")]
        pprops += [spec_property(p, f"$.aggregat.positionen.entity.properties[{i}]") for i, p in enumerate(pprops_spec)]
        patoms = [field("id", "ID"), field(key, table + "_ID")] + [atom(p) for p in pprops_spec]
        kurz = pspec.get("kurz", cap(pspec["property"]))
        props.append(business_property(pspec["property"],
                                       {"concept": "ListType", "children": {"elementType": {
                                           "concept": "ClassifierType", "references": {"classifier": pe["name"]}}}},
                                       kurz, pspec.get("lang", kurz)))
        atoms.append({"concept": "ListMapping", "references": {"property": pspec["property"]},
                      "children": {"mappedfieldRef": {"concept": "KeyOnlyReferenceMapping",
                                                      "references": {"entityMapping": "Map" + pe["name"], "keyOnlyRef": key}}}})
        sort = next((p["name"] for p in pprops_spec if p.get("typ") == "int" and "nummer" in p["name"].lower()), "id")
        pos = {"entity": pe["name"], "property": pspec["property"], "key": key, "sort": sort,
               "mapping": entity_mapping("Map" + pe["name"], pe["name"], ptable, patoms)}
        roots.append(("position", entity(pe["name"], pprops)))
    roots.insert(0, ("entity", entity(agg, [key_property(agg, table)] + props, sdecl)))
    mappings = [entity_mapping("Map" + agg, agg, table, atoms)] + ([pos["mapping"]] if pos else [])
    if spec.get("persistenzVorhanden"):
        # element mappings first: the list mapping of the aggregate refers to them
        roots += [("mapping", m, persistenz) for m in reversed(mappings)]
    else:
        roots.append(("persistence", {"concept": "PersistenceDescription", "properties": {"name": persistenz},
                                      "children": {"persistenceMapping": mappings}}))
    roots.append(("repository", {"concept": "Repository",
                                 "properties": {"name": repo, "nestedName": repo, "resolveInfo": repo, "isStatic": "true"},
                                 "children": {"visibility": PUBLIC}}))
    sjava = service_java(agg, var, status, spec.get("uebergaenge", []), "$.uebergaenge")
    if sjava:
        roots.append(("service", {"concept": "Service",
                                  "properties": {"isStatic": "true", "nestedName": service, "name": service,
                                                 "resolveInfo": service},
                                  "children": {"visibility": PUBLIC}}))
    java = [("repository", repository_java(agg, var, pos),
             f"{repo}: parse as CLASS_CONTENT into its member role; text2of.py --repo-type checkout=CHECKOUT"
             " --repo-type checkin=CHECKIN")]
    if sjava:
        java.append(("service", sjava, f"{service}: parse as CLASS_CONTENT into its member role; text2of.py"))
    notes = ["Import the models of referenced value objects and entities (e.g. sharedvalues).",
             "Then add the business logic: further preconditions, dependent values, rules."]
    return model, roots, java, notes


# ---- tests -------------------------------------------------------------------------------------------
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


def tests(spec):
    model, roots, _, _ = domain(spec)   # validates the specification the same way
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
            val = "nummer" if param and p["name"] == param else sample(p)
            if val is None:
                open_values.append(f"{name}.{p['name']}")
                continue
            lines.append(f"  {v}.{p['name']} = {val};")
        lines += [f"  {x}" for x in extra] + [f"  return {v};", "}"]
        return lines

    pos = a.get("positionen")
    extra = []
    java = []
    if pos:
        pe = pos["entity"]
        pnum = next((p["name"] for p in pe.get("properties", []) if p.get("typ") == "int" and "nummer" in p["name"].lower()), None)
        java += builder(pe["name"], pe.get("properties", []), param=pnum or "_")
        extra = [f"{var}.{pos['property']}.add(baue{pe['name']}({n}));" for n in (1, 2)]
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
        set_from = [] if t["von"][0] == names[0] else [f'{var}.status = STATUS("{status["name"]}", "{t["von"][0]}");']
        cases.append((f"{agg} {t['name']}", [f'{agg} {var} = CALL("TestDaten", "baue{agg}");', *set_from,
                                             f'CALL("{service}", "{t["name"]}", {var});',
                                             f'assert OF({var}.status, "{t["nach"]}");']))
        wrong = next((s for s in names if s not in t["von"] and s != t["nach"]), None)
        if wrong:
            kurz = next((w[2] for w in status["werte"] if w[0] == wrong and len(w) > 2), cap(wrong.lower()))
            cases.append((f"{agg} {t['name']} im Status {kurz} wird abgelehnt",
                          [f'{agg} {var} = CALL("TestDaten", "baue{agg}");',
                           f'{var}.status = STATUS("{status["name"]}", "{wrong}");',
                           'FAIL_IN("OFXAbortedException");',
                           f'CALL("{service}", "{t["name"]}", {var});']))
    check = [f'{agg} gelesen = CALL_WITH(CALL("CS", "CREATE"), "{repo}", "get", gespeichert.id);',
             "assert gelesen != null;"]
    if pos:
        check.append(f"assert gelesen.{pos['property']}.size() == 2;")
    first = next((p["name"] for p in a.get("properties", []) if p.get("typ") == "string"), None)
    if first:
        check.append(f"assert EQ(gelesen.{first}, gespeichert.{first});")
    cases.append((f"{agg} speichern und in frischer Session zurücklesen",
                  [f'{agg} gespeichert = CALL_WITH(CALL("CS", "CREATE"), "TestDaten", "erzeuge{agg}");',
                   "assert gespeichert.id > 0;", *check]))

    config = spec.get("testConfig")
    troots = [("testdaten", {"concept": "Service", "properties": {"isStatic": "true", "nestedName": "TestDaten",
                                                                    "name": "TestDaten", "resolveInfo": "TestDaten"},
                             "children": {"visibility": PUBLIC}}),
              ("testsuite", {"concept": "OFXTestSuit", "properties": {"name": suite},
                             **({"references": {"configuration": config}} if config else {}),
                             "children": {"content": [{"concept": "OFXTestMethod", "properties": {"name": n},
                                                       "children": {"returnType": "VoidType", "body": "StatementList"}}
                                                      for n, _ in cases]}})]
    jfiles = [("testdaten", "\n".join(java) + "\n", "TestDaten: parse as CLASS_CONTENT into its member role; text2of.py")]
    for i, (n, body) in enumerate(cases, 1):
        jfiles.append((f"test-{i:02d}", "\n".join(body) + "\n",
                       f"'{n}': parse as STATEMENTS into the body of this test method"))
    jfiles.append(("", "", f"then text2of.py on the printed {suite} (one row per test body)"))
    notes = [f"Imports of {tmodel}: {model}, org.modellwerkstatt.wbkit.shared.testing (CS),"
             " org.modellwerkstatt.objectflow.runtime (OFXAbortedException); module dependency"
             " org.modellwerkstatt.wbkit."]
    if not config:
        notes.append(f"{suite} has no configuration yet: set it to the test OFXConfig (conventions: CS must be found).")
    if open_values:
        notes.append("No test value for " + ", ".join(open_values) + ": set them in TestDaten (\"beispiel\" in the spec).")
    return tmodel, troots, jfiles, notes


# ---- search ------------------------------------------------------------------------------------------
DELEGATES = {"string": "StringDelegate", "int": "IntegerDelegate", "LocalDate": "LocalDateDelegate",
             "DateTime": "DateTimeDelegate", "BigDecimal": "BigDecimalDelegate", "status": "StatusDelegate"}


def delegate(name, typ, options=()):
    if typ not in DELEGATES:
        raise SpecError(f"no delegate for '{name}' of type {typ}; only {', '.join(DELEGATES)}")
    return {"concept": DELEGATES[typ], "children": {"boundTo": {"concept": "DuxLocalPropertyReference",
                                                                "references": {"property": name}},
                                                    "option": list(options)}}


def menu(names):
    return {"concept": "MenuSub", "children": {"menuItems": [{"concept": "MenuAction", "references": {"command": n}}
                                                             for n in names]}}


def suche(spec, menus=None):
    model, _, _, _ = domain(spec)   # validates the specification the same way
    a, namen, s = spec["aggregat"], spec.get("namen", {}), spec.get("suche") or {}
    agg = a["name"]
    base = model.rsplit(".", 1)[0]
    rmodel, umodel = namen.get("unitreadmodell", base + ".unit.read"), namen.get("unitmodell", base + ".unit")
    props = {p["name"]: p for p in a.get("properties", [])}
    status = a.get("status")
    if status:
        props["status"] = {"name": "status", "typ": "status", "kurz": "Status"}
    kriterien, spalten = s.get("kriterien") or [], s.get("spalten") or []
    if not kriterien or not spalten:
        raise SpecError("$.suche needs kriterien and spalten (property names of the aggregate)")
    for n in kriterien + spalten:
        if n not in props:
            raise SpecError(f"$.suche: '{n}' is no property of {agg}")
    for x in s.get("ausschliessen", []):
        if not status or x not in [w[0] for w in status["werte"]]:
            raise SpecError(f"$.suche.ausschliessen: '{x}' is no status element")
    flt, repo = f"{agg}Filter", namen.get("sucherepo", agg + "SucheRepo")
    cmd = s.get("name", f"{agg} suchen")
    m = "Map" + agg

    fprops = []
    for n in kriterien:
        p = dict(props[n])
        if p["typ"] == "status":
            fprops.append(business_property(n, {"concept": "StatusType", "references": {"status": status["name"]}},
                                            "Status", f"Status {agg}"))
            continue
        if p["typ"] == "string":
            p["laenge"] = [0, (p.get("laenge") or [0, 200])[1]]
        p.pop("bereich", None)
        fprops.append(spec_property(p, f"$.suche.kriterien({n})"))
    fprops.append(business_property("ergebnisse", {"concept": "ListType", "children": {"elementType": {
        "concept": "ClassifierType", "references": {"classifier": agg}}}}, "Ergebnisse", f"Gefundene {agg}"))
    roots = [("filter", entity(flt, fprops, concept="DTO")),
             ("sucherepo", {"concept": "Repository",
                            "properties": {"name": repo, "nestedName": repo, "resolveInfo": repo, "isStatic": "true"},
                            "children": {"visibility": PUBLIC}})]

    pre, preds = [], []
    for n in kriterien:
        typ = props[n]["typ"]
        if typ == "string":
            pre += [f"String {n}Muster = null;",
                    f"if (filter.{n} != null && filter.{n}.trim().length() > 0) {{",
                    f'  {n}Muster = "%" + filter.{n}.trim() + "%";', "}"]
            preds.append(f'OPTIONAL(LIKE(FIELD("{m}", "{n}"), {n}Muster))')
        else:
            preds.append(f'OPTIONAL(FIELD("{m}", "{n}") == filter.{n})')
    preds += [f'FIELD("{m}", "status") != STATUS("{status["name"]}", "{x}")' for x in s.get("ausschliessen", [])]
    rjava = "\n".join([f"public List<{agg}> suche({flt} filter) {{", *[f"  {x}" for x in pre],
                       f'  return WHERE("{m}", true, {" && ".join(preds)})'
                       f'.SORTBY(FIELD("{m}", "{spalten[0]}"), true);', "}"]) + "\n"

    wizard = len(kriterien) > 3
    width = str(max(5, 100 // len(spalten)))
    crit_opts = {"LocalDate": ["OptionalDOption", "PickerDOption"], "DateTime": ["OptionalDOption", "PickerDOption"],
                 "BigDecimal": ["OptionalDOption"], "status": ["OptionalDOption"], "int": [], "string": []}
    crits = [delegate(n, props[n]["typ"], crit_opts.get(props[n]["typ"], []) + ([] if wizard else ["IssueUpdateDOption"]))
             for n in kriterien]
    form = {"concept": "DelegateForm", "references": {"boundClassifier": flt},
            "children": {"colWeights": ["OneWeight"] * (1 if wizard else len(kriterien)), "delegates": crits,
                         "options": []}}   # empty role: no factory LABEL without text
    table = {"concept": "Table", "references": {"boundClassifier": flt, "boundProperty": "ergebnisse"},
             "children": {"options": (["SelectFirstFOption"] if wizard else
                                      [{"concept": "LabelFOption", "children": {"expression": literal(s.get("ergebnisLabel", "Ergebnisse"))}},
                                       "SelectFirstFOption"]),
                          "delegates": [delegate(n, props[n]["typ"], [{"concept": "WidthDOption", "properties": {"percent": width}}])
                                        for n in spalten],
                          "menuItems": menu((menus or {}).get("tabelle", []))}}

    def pane(name, child, actions=False):
        pp = {"concept": "PagePane", "properties": {"name": name, "isNamed": "true"},
              "references": {"boundClassifier": flt}, "children": {"uxChild": child}}
        if actions and (menus or {}).get("pane"):
            pp["children"]["menuItems"] = menu(menus["pane"])
        return pp

    def page(name, title, panes, conclusions, handler=False):
        ch = {"pageInit": {"concept": "PageInitConceptFunc", "children": {"body": "StatementList"}},
              "conclusion": [{"concept": "PageConclusion", "references": {"label": lab},
                              "children": {"function": {"concept": "CommandVoidStatementList",
                                                        "children": {"body": "StatementList"}}}} for lab in conclusions],
              "pagePaneActionProviderLink": [{"concept": "PagePaneActionProviderLink",
                                              "references": {"actionProviderPagePane": x}} for x in panes],
              "dynamicPageTitle": literal(title)}
        if handler:
            ch["cmdTermHandler"] = {"concept": "PageCmdTermHandler", "properties": {"cmdTermType": "AnyCmdTerminated"},
                                    "references": {"classifier": agg},
                                    "children": {"func": {"concept": "PageCmdTermConceptFunction",
                                                          "children": {"body": "StatementList"}}}}
        return {"concept": "PageCrtl", "properties": {"name": name}, "references": {"boundObject": flt}, "children": ch}

    search = [f'filter.ergebnisse = CALL("{repo}", "suche", filter);', "return filter;"]
    handler = ["if (TERM_OK()) {", '  MERGE(PUSHED(), filter.ergebnisse, "entity", "list", "readonly");', "}"]
    if wizard:
        panes = [("kriterienpane", pane(f"{agg}SuchkriterienPP", form)), ("ergebnispane", pane(f"{agg}SuchergebnisPP", table, True))]
        pages = [page("Suchkriterien", cmd, [f"{agg}SuchkriterienPP"], ["Weiter"]),
                 page("Suchergebnisse", f"{cmd}: Ergebnisse", [f"{agg}SuchergebnisPP"], ["Zurueck", "Aktualisieren"], True)]
        bodies = [("page init 'Suchkriterien'", ["return filter;"]),
                  ("conclusion 'Weiter'", ['PAGE("Suchergebnisse");']),
                  ("page init 'Suchergebnisse'", search),
                  ("conclusion 'Zurueck'", ['PAGE("Suchkriterien");']),
                  ("conclusion 'Aktualisieren'", ['PAGE("Suchergebnisse");'])]
    else:
        grid = {"concept": "GridLayout", "children": {"rowWeights": ["MinWeight", "OneWeight"], "colWeights": ["OneWeight"],
                                                       "uxChild": [form, table]}}
        panes = [("suchepane", pane(f"{agg}SuchePP", grid, True))]
        pages = [page("Suche", cmd, [f"{agg}SuchePP"], ["Suchen", "Aktualisieren"], True)]
        bodies = [("page init 'Suche'", search),
                  ("conclusion 'Suchen'", ['PAGE("Suche");']),
                  ("conclusion 'Aktualisieren'", ['PAGE("Suche");'])]
    bodies = [("command init", [f"filter = new {flt}();"])] + bodies + [("cmdTermHandler", handler)]
    command = {"concept": "Command", "properties": {"name": cmd, "newCommandType": "SEARCH_CMD"},
               "children": {"variable": {"concept": "ContainerVariable", "properties": {"name": "filter"},
                                         "children": {"type": {"concept": "ClassifierType",
                                                               "references": {"classifier": flt}}}},
                            "commandInit": {"concept": "CommandVoidStatementList", "children": {"body": "StatementList"}},
                            "pages": pages,
                            # NEWSTYLE_CMD_TERM_HANDLING: required for the any cmd term handler, preferred pattern
                            "options": "CommandNoPushNewTermOption"}}
    if menus is not None:
        return panes
    roots += panes + [("command", command)]
    java = [("sucherepo", rjava, f"{repo}: parse as CLASS_CONTENT into its member role; text2of.py")]
    for i, (where, body) in enumerate(bodies, 1):
        java.append((f"cmd-{i:02d}", "\n".join(body) + "\n", f"'{cmd}' {where}: parse as STATEMENTS into its body"))
    java.append(("", "", f"then text2of.py on the printed command '{cmd}' (one row per function body)"))
    notes = [f"Models: {flt} and {repo} belong in {rmodel} (imports {model}); page panes and command in {umodel}"
             f" (imports {rmodel}, {model} and the base model with AppRessourcen for the labels).",
             "The table menu is an empty Submenu: add the actions once the commands exist (scaffold step owner/edit)."]
    return umodel, roots, java, notes


# ---- owner, edit and transition commands -----------------------------------------------------------
def ref(concept, role, target):
    return {"concept": concept, "references": {role: target}}


def dot(operand, prop):
    return {"concept": "DotExpression", "children": {"operand": operand,
                                                      "operation": ref("PropertyReference", "property", prop)}}


def ctype(cls):
    return ref("ClassifierType", "classifier", cls)


def func():
    return {"concept": "CommandVoidStatementList", "children": {"body": "StatementList"}}


def commands(spec):
    model, _, _, _ = domain(spec)   # validates the specification the same way
    a, namen, c = spec["aggregat"], spec.get("namen", {}), spec.get("commands") or {}
    agg, var = a["name"], lower(a["name"])
    repo, service = namen.get("repo", agg + "Repo"), namen.get("service", agg + "Service")
    umodel = namen.get("unitmodell", model.rsplit(".", 1)[0] + ".unit")
    status, pos = a.get("status"), a.get("positionen")
    snames = [w[0] for w in status["werte"]] if status else []
    bearbeitbar = c.get("bearbeitbar", [])
    for x in bearbeitbar:
        if x not in snames:
            raise SpecError(f"$.commands.bearbeitbar: '{x}' is no status element")

    def editable(props):
        ok = [p for p in props if p.get("typ") in DELEGATES and not p.get("verweis") and "felder" not in p]
        return ok, [p["name"] for p in props if p not in ok]

    aprops, askip = editable(a.get("properties", []))
    n_new, n_edit = c.get("anlegen", f"{agg} anlegen"), c.get("bearbeiten", f"{agg} bearbeiten")
    n_head = c.get("kopf", f"{agg} Kopfdaten bearbeiten")
    n_trans = [(t, f"{agg} {t['name']}") for t in spec.get("uebergaenge", [])]

    def form(cls, props, disabled=False, label=None, numbered=None):
        ds = []
        for p in props:
            opts = []
            if disabled is False and p["typ"] in ("LocalDate", "DateTime"):
                opts.append("PickerDOption")
            if disabled is False and p["name"] == numbered:
                opts.append("DisabledDOption")
            ds.append(delegate(p["name"], p["typ"], opts))
        options = []
        if disabled:
            options.append("DisabledFOption")
        if label:
            options.append({"concept": "LabelFOption", "children": {"expression": literal(label)}})
        return {"concept": "DelegateForm", "references": {"boundClassifier": cls},
                "children": {"colWeights": ["OneWeight"], "delegates": ds, "options": options}}

    def pane(name, cls, child, actions=None):
        pp = {"concept": "PagePane", "properties": {"name": name, "isNamed": "true"},
              "references": {"boundClassifier": cls}, "children": {"uxChild": child}}
        if actions:
            pp["children"]["menuItems"] = menu(actions)
        return pp

    def page(name, cls, pane_name, label, title):
        return {"concept": "PageCrtl", "properties": {"name": name}, "references": {"boundObject": cls},
                "children": {"pageInit": {"concept": "PageInitConceptFunc", "children": {"body": "StatementList"}},
                             "conclusion": {"concept": "PageConclusion", "references": {"label": label},
                                            "children": {"function": func()}},
                             "pagePaneActionProviderLink": ref("PagePaneActionProviderLink",
                                                               "actionProviderPagePane", pane_name),
                             "dynamicPageTitle": literal(title)}}

    def command(name, typ=None, params=(), variables=(), init=False, pages=(), ok=False, final=None,
                enabled=None, revert=None, hotkey=None):
        props = {"name": name}
        if typ:
            props["newCommandType"] = typ
        if hotkey:
            props["defaultHotkey"] = hotkey
        ch = {"parameter": [{"concept": "ContainerParameter", "properties": {"name": n},
                             "children": {"type": ty, "initializer": ini}} for n, ty, ini in params],
              "variable": [{"concept": "ContainerVariable", "properties": {"name": n}, "children": {"type": ctype(cl)}}
                           for n, cl in variables],
              "pages": list(pages)}
        if init:
            ch["commandInit"] = func()
        if ok:
            ch["okConclusionStatements"] = func()
        if final:
            ch["finalOkSelection"] = ref("ContainerVariableReference", "variableDeclaration", final)
        if enabled:
            ch["andIsEnabledNew"] = enabled
        if revert:
            ch["reverts"] = ref("ContainerParamReference", "variableDeclaration", revert)
        return {"concept": "Command", "properties": props, "children": {k: v for k, v in ch.items() if v != []}}

    def status_of(operand, names):
        return {"concept": "StatusOfOperator", "children": {
            "statusLeftSide": dot(operand, "status"),
            "statusElements": [ref("StatusElementReference", "statusElement", x) for x in names]}}

    sel = lambda cls: ref("SelectedObject", "object", cls)
    par = lambda n: ref("ContainerParamReference", "variableDeclaration", n)
    edit_enabled = status_of(par(var), bearbeitbar) if bearbeitbar else None
    roots, bodies = [], []
    checkin = [f'CALL("{repo}", "checkin", {var});']

    # <X> anlegen: GRAPH_OWNER_CMD with an editable form, saved in FINAL OK, pushed for the search
    roots.append(("anlegenpane", pane(f"{agg}AnlegenPP", agg, form(agg, aprops))))
    roots.append(("anlegen", command(n_new, "GRAPH_OWNER_CMD", variables=[(var, agg)], init=True, ok=True, final=var,
                                     pages=[page("Neu", agg, f"{agg}AnlegenPP", "SpeichernUndSchliessen", n_new)])))
    bodies.append((n_new, [("command init", [f"{var} = new {agg}();"]), ("page init", [f"return {var};"]),
                           ("conclusion 'Speichern & Schließen'", ["DONE();"]), ("FINAL OK", checkin)]))

    # <X> bearbeiten: GRAPH_OWNER_CMD with the key only, checkout in command init, DISABLED form
    shown = aprops + ([{"name": "status", "typ": "status"}] if status else [])
    head = form(agg, shown, disabled=True, label=agg if pos else None)
    if pos:
        pe = pos["entity"]["name"]
        pprops, pskip = editable(pos["entity"].get("properties", []))
        pnum = next((p["name"] for p in pprops if p["typ"] == "int" and "nummer" in p["name"].lower()), None)
        n_pedit, n_padd = c.get("positionBearbeiten", f"{pe} bearbeiten"), c.get("positionHinzufuegen", f"{pe} hinzufügen")
        width = str(max(5, 100 // max(1, len(pprops))))
        table = {"concept": "Table", "references": {"boundClassifier": agg, "boundProperty": pos["property"]},
                 "children": {"options": [{"concept": "LabelFOption", "children": {"expression": literal(
                     pos.get("kurz", cap(pos["property"])))}}, "SelectFirstFOption"],
                              "delegates": [delegate(p["name"], p["typ"], [{"concept": "WidthDOption",
                                                                             "properties": {"percent": width}}])
                                            for p in pprops],
                              "menuItems": menu([n_pedit, n_padd])}}
        child = {"concept": "GridLayout", "children": {"rowWeights": ["MinWeight", "OneWeight"],
                                                        "colWeights": ["OneWeight"], "uxChild": [head, table]}}
    else:
        pskip = []
        child = head
    roots.append(("bearbeitenpane", pane(f"{agg}PP", agg, child, [n_head])))
    roots.append(("bearbeiten", command(n_edit, "GRAPH_OWNER_CMD", hotkey="ENTER",
                                        params=[(var + "Id", "IntegerType", dot(sel(agg), "id"))],
                                        variables=[(var, agg)], init=True, ok=True, final=var,
                                        pages=[page(agg, agg, f"{agg}PP", "SpeichernUndSchliessen", agg)])))
    bodies.append((n_edit, [("command init", [f'{var} = CALL("{repo}", "checkout", {var}Id);']),
                            ("page init", [f"return {var};"]), ("conclusion 'Speichern & Schließen'", ["DONE();"]),
                            ("FINAL OK", checkin)]))

    # GRAPH_EDIT_CMDs: editable forms, opened from the owner's menus; revert the aggregate on cancel
    roots.append(("kopfpane", pane(f"{agg}KopfPP", agg, form(agg, aprops))))
    roots.append(("kopf", command(n_head, params=[(var, ctype(agg), sel(agg))], enabled=edit_enabled, revert=var,
                                  pages=[page("Kopfdaten", agg, f"{agg}KopfPP", "OK", n_head)])))
    bodies.append((n_head, [("page init", [f"return {var};"]), ("conclusion 'OK'", ["DONE();"])]))
    if pos:
        pvar = lower(pe)
        roots.append(("positionpane", pane(f"{pe}PP", pe, form(pe, pprops, numbered=pnum))))
        roots.append(("positionbearbeiten", command(
            n_pedit, hotkey="ENTER", params=[(var, ctype(agg), sel(agg)), (pvar, ctype(pe), sel(pe))],
            enabled=edit_enabled, revert=var, pages=[page(pe, pe, f"{pe}PP", "OK", n_pedit)])))
        bodies.append((n_pedit, [("page init", [f"return {pvar};"]), ("conclusion 'OK'", ["DONE();"])]))
        add = [f"{pvar} = new {pe}();"]
        if pnum:
            add.append(f"{pvar}.{pnum} = {var}.{pos['property']}.size() + 1;")
        add.append(f"{var}.{pos['property']}.add({pvar});")
        roots.append(("positionhinzufuegen", command(
            n_padd, params=[(var, ctype(agg), sel(agg))], variables=[(pvar, pe)], init=True,   # GRAPH_EDIT_CMD pushes nothing
            enabled=edit_enabled, revert=var, pages=[page("Neu", pe, f"{pe}PP", "OK", n_padd)])))
        bodies.append((n_padd, [("command init", add), ("page init", [f"return {pvar};"]),
                                ("conclusion 'OK'", ["DONE();"])]))

    # one GRAPH_OWNER_CMD per transition, no page: generally enabled reads the status of the selection
    for t, n in n_trans:
        roots.append(("uebergang", command(
            n, "GRAPH_OWNER_CMD", params=[("auswahl", ctype(agg), sel(agg))], variables=[(var, agg)], init=True,
            ok=True, final=var, enabled=status_of(par("auswahl"), t["von"]))))
        bodies.append((n, [("command init", [f'{var} = CALL("{repo}", "checkout", auswahl.id);',
                                             f'CALL("{service}", "{t["name"]}", {var});', "DONE();"]),
                           ("FINAL OK", checkin)]))

    search = []
    if spec.get("suche"):
        search = [(k, sp, "=replace") for k, sp in suche(spec, {"tabelle": [n_edit] + [n for _, n in n_trans],
                                                                 "pane": [n_new]})]
    java = []
    for name, fs in bodies:
        for i, (where, lines) in enumerate(fs, 1):
            plain = name.lower().translate(str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}))
            stem = re.sub(r"[^a-z0-9]+", "-", plain).strip("-")
            java.append((f"{stem}-{i}", "\n".join(lines) + "\n", f"'{name}' {where}: parse as STATEMENTS into its body"))
    java.append(("", "", "then text2of.py on each printed command (one row per function body)"))
    notes = [f"Model {umodel} imports {model}, the unit.read model of the search and the base model (labels).",
             "Business checks belong in the conclusions: call the service methods that validate (conventions:"
             " the service checks, the form only takes input)."]
    if askip or pskip:
        notes.append("Not in the forms (value objects, cross references): " + ", ".join(askip + pskip)
                     + "; add delegates with a path (e.g. betrag.betrag) or a selection by hand.")
    if pos:
        notes.append(f"'{n_padd}' adds the position in command init; move it into a list helper of {agg} or the"
                     f" service if adding has business rules.")
    return umodel, search + roots, java, notes


# ---- configs -----------------------------------------------------------------------------------------
LABELS = [("Weiter", "Weiter", "F4"), ("Zurueck", "Zurück", "F3"), ("Aktualisieren", "Aktualisieren", "F12"),
          ("OK", "OK", "F12"), ("SpeichernUndSchliessen", "Speichern & Schließen", "F12"),
          ("Suchen", "Suchen", "SCAN_UPDATE")]


def configs(spec, dumps):
    from copyroot import Copier, load, model_of
    for k in ("firma", "app"):
        if not spec.get(k):
            raise SpecError(f"$.{k} is missing")
    namen = spec.get("namen", {})
    model = namen.get("basismodell", f"{spec['firma']}.{spec['app']}.base")
    wanted = spec.get("configs", ["Test", "FX8"])
    roots = {}
    for d in dumps:
        r = load(d)
        roots[r.get("name")] = r
    missing = [n for n in ["baseconfig"] + wanted if n not in roots]
    if missing:
        raise SpecError("dumps missing for " + ", ".join(missing) +
                        " (print_node deep=true of the roots in org.modellwerkstatt.wbkit.shared.configuration)")
    used = set()
    for n in wanted:
        for ch in roots[n].get("children", []):
            for x in ch.get("nodes", []):
                if x.get("concept") == "OFXConfigInclude":
                    used |= {r.get("target") for r in x.get("references", [])}
    sections = [x.get("name") for ch in roots["baseconfig"].get("children", []) for x in ch.get("nodes", [])
                if x.get("concept") == "OFXConfigSection"]
    drop = [s for s in sections if s not in used]
    cp = Copier([("firma.app", f"{spec['firma']}.{spec['app']}")], drop, False)
    chosen = [roots["baseconfig"]] + [roots[n] for n in wanted]
    for r in chosen:
        cp.collect(r)
    source = {model_of(r.get("reference")) for r in chosen}
    try:
        out = [(r.get("name"), cp.node(r, source, r.get("name"))) for r in chosen]
    except ValueError as e:
        raise SpecError(str(e))
    db = spec.get("datenbank")
    if db:
        for name, bp in out[1:]:
            for ch in bp.get("children", []):
                for x in ch["nodes"]:
                    if x["concept"].endswith(".OFXConfigInclude") and any(
                            r["target"].startswith("LocalDB_") for r in x.get("references", [])):
                        x.setdefault("children", []).append({"role": "properties", "nodes": [
                            {"concept": "org.modellwerkstatt.objectflow.structure.OFXConfigPropOverwrite",
                             "references": [{"role": "property", "target": k}],
                             "children": [{"role": "value", "nodes": [expand_literal(v)]}]}
                            for k, v in db.items()]})
    res = {"concept": "StaticRessources", "properties": {"name": "AppRessourcen"},
           "children": {"platforms": {"concept": "PlatformDeclaration", "properties": {"name": "RICH"}},
                        "labels": [{"concept": "Label", "properties": {"name": n},
                                    "children": {"specification": {"concept": "LabelSpecification",
                                                                   "properties": {"hotkey": k},
                                                                   "children": {"text": literal(text)}}}}
                                   for n, text, k in LABELS]}}
    troots = [("config", bp) for _, bp in out] + [("ressourcen", res)]
    notes = ["Model content: only OFXConfigs and Static Ressources; it imports nothing (conventions)."]
    notes += [f"dropped (not included by {', '.join(wanted)}): {d}" for d in cp.dropped]
    notes += [f"will not resolve: {o}" for o in cp.outside]
    if not db:
        notes.append("No \"datenbank\" in the spec: the LocalDB section keeps ${DB_URL}/${DB_USERNAME}/${DB_PASSWORD}.")
    return model, troots, [], notes


def expand_literal(text):
    return {"concept": "jetbrains.mps.baseLanguage.structure.StringLiteral",
            "properties": [{"name": "value", "value": text}]}


def write(st, model, roots, java, notes, out_dir):
    out_dir = os.path.abspath(out_dir or tempfile.mkdtemp(prefix="moai-scaffold-"))
    os.makedirs(out_dir, exist_ok=True)
    chk = Checker(st)
    files = []
    for i, (kind, spec, *into) in enumerate(roots, 1):
        bp = expand(st, spec, f"{kind}")
        chk.node(bp, kind)
        path = os.path.join(out_dir, f"{i:02d}-{kind}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(bp, f, ensure_ascii=False, separators=(",", ":"))
        files.append((into[0] if into else None, next((x["value"] for x in bp.get("properties", []) if x["name"] == "name"), kind), path))
    if report(chk):
        return 1
    jlines = []
    for stem, text, how in java:
        if not stem:
            jlines.append(f"  {how}")
            continue
        path = os.path.join(out_dir, f"{stem}.java")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        jlines.append(f"  {path}: {how}")
    plan = [f"Model {model} (create it if missing, DevKit org.modellwerkstatt.MoWareWerkbank).",
            "Insert the roots in this order (mps_mcp_insert_root_node_from_json, json = file path),",
            "check fixReferences.stillBroken = 0 after each:"]
    plan += [f"  {name}: {path}" if into is None else
             f"  {name}: {path} (replace the existing root: mps_mcp_update_root_node_from_json)" if into == "=replace" else
             f"  {name}: {path} (ADD CHILD into the existing {into}, role persistenceMapping)" for into, name, path in files]
    if jlines:
        plan.append("Write the method bodies (moai:objectflow-dsl, workflows.md, \"Write method bodies and command functions\"):")
        plan += jlines
        plan.append("After the last SET CHILD of a root: FIX_REFERENCES on that root.")
    plan += notes
    plan.append("Check the model (mps_mcp_check_root_node_problems, model reference, perRoot=true).")
    text = "\n".join(plan) + "\n"
    with open(os.path.join(out_dir, "plan.txt"), "w", encoding="utf-8") as f:
        f.write(text)
    print(text, end="")
    return 0


def main(argv):
    if len(argv) < 3 or argv[1] in ("-h", "--help") or argv[1] not in ("domain", "tests", "configs", "suche", "commands"):
        print(__doc__)
        return 0 if len(argv) > 1 and argv[1] in ("-h", "--help") else 2
    out = argv[argv.index("-o") + 1] if "-o" in argv else None
    args = [a for i, a in enumerate(argv[2:], 2) if a != "-o" and argv[i - 1] != "-o"]
    with open(args[0], encoding="utf-8") as f:
        spec = json.load(f)
    try:
        if argv[1] == "configs":
            model, roots, java, notes = configs(spec, args[1:])
        else:
            model, roots, java, notes = {"domain": domain, "tests": tests, "suche": suche, "commands": commands}[argv[1]](spec)
    except SpecError as e:
        print("error:", e, file=sys.stderr)
        return 1
    return write(Structure(), model, roots, java, notes, out)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
