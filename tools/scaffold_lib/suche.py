"""scaffold.py suche: filter, search repository, SEARCH_CMD with page panes; the result is a list of entities or of DTOs."""
from .bausteine import (SpecError, business_property, cap, column, command, delegate, dto, entity, form, grid, java_lines,
                        list_type, lower, mapper, page, pane, repository, rw, spec_property, status_type, table, var, width)
from .domain import domain
from .registry import Ergebnis, Java, generator

CRITERION_OPTIONS = {"LocalDate": ["OptionalDOption", "PickerDOption"], "DateTime": ["OptionalDOption", "PickerDOption"],
                     "BigDecimal": ["OptionalDOption"], "status": ["OptionalDOption"], "int": [], "string": []}


def _columns(props, names):
    return [props[n].get("spalte", column(n)) for n in names]


def _sql_java(agg, flt, result, mapper_name, props, s, status):
    """Custom SQL search: a fragment per set criterion in the control flow (mw-lesemodelle)."""
    t, al = column(agg), agg[0].upper()
    kriterien, spalten, extras = s["kriterien"], s["spalten"], (s.get("dto") or {}).get("extra", [])
    cols = [f"{al}.ID"] + [f"{al}.{c}" for c in _columns(props, spalten)] + [f"{e['sql']} AS {column(e['name'])}" for e in extras]
    excluded = [f'SQLTEXT("AND {al}.STATUS <> {{{status["name"]}.{x}}}");' for x in s.get("ausschliessen", [])] if status else []
    lines = [f"public List<{result}> suche({flt} filter) {{",
             '  return SQL("QUERY", () -> {',
             f'    SQLTEXT("SELECT {", ".join(cols)}\\nFROM {t} {al} WHERE 1 = 1");']
    if "status" in kriterien and excluded:
        lines += ["    if (filter.status == null) {", *[f"      {x}" for x in excluded], "    } else {",
                  f'      SQLTEXT("AND {al}.STATUS = :filter.status");', "    }"]
    else:
        lines += [f"    {x}" for x in excluded]
    such = s.get("suchbegriff")
    if such:
        tests = " OR ".join(f"UPPER({al}.{c}) LIKE UPPER(:muster)" for c in _columns(props, such["felder"]))
        lines += ["    if (ISNOTEMPTY(filter.suchbegriff)) {",
                  '      String muster = "%" + filter.suchbegriff.trim() + "%";',
                  f'      SQLTEXT("AND ({tests})");', "    }"]
    for n in kriterien:
        if n == "status" and excluded:
            continue
        col, typ = _columns(props, [n])[0], props[n]["typ"]
        if typ == "string":
            lines += [f"    if (ISNOTEMPTY(filter.{n})) {{",
                      f'      String {n}Muster = "%" + filter.{n}.trim() + "%";',
                      f'      SQLTEXT("AND UPPER({al}.{col}) LIKE UPPER(:{n}Muster)");', "    }"]
        else:
            lines += [f"    if (filter.{n} {'!= 0' if typ == 'int' else '!= null'}) {{",
                      f'      SQLTEXT("AND {al}.{col} = :filter.{n}");', "    }"]
    lines += [f'    SQLTEXT("ORDER BY {al}.{_columns(props, spalten)[0]}");', f'  }}, MAPPER("{mapper_name}"));', "}"]
    return java_lines(lines)


def _takeover_java(agg, result, s):
    """uebernehmen: the values of the pushed aggregate go into the DTO of the result list (mw-commands)."""
    d = s["dto"]
    lines = [f"public void uebernehmen({agg} gepusht) {{",
             f"  {result} treffer = ergebnisse.findFirst(t -> t.id == gepusht.id);",
             "  if (treffer == null) {", f"    treffer = new {result}();", "    ergebnisse.add(treffer);", "  }"]
    lines += [f"  {x}" for x in d.get("vorlauf", [])]
    lines += [f"  treffer.{n} = gepusht.{n};" for n in ["id"] + s["spalten"]]
    lines += [f"  treffer.{e['name']} = {e['uebernahme']};" for e in d.get("extra", []) if e.get("uebernahme")]
    lines.append("}")
    return java_lines(lines)


def result_type(spec):
    """The class of a row of the result list: what a command gets as its selection."""
    s, a = spec.get("suche") or {}, spec["aggregat"]
    return (s.get("dto") or {}).get("name") or a["name"]


def _build(spec, menus=None):
    """Result and page panes. menus: command names for the table and the pane (from `commands`)."""
    model = domain(spec).model   # validates the specification the same way
    a, namen, s = spec["aggregat"], spec.get("namen", {}), spec.get("suche") or {}
    agg = a["name"]
    base = model.rsplit(".", 1)[0]
    rmodel, umodel = namen.get("unitreadmodell", base + ".unit.read"), namen.get("unitmodell", base + ".unit")
    props = {p["name"]: p for p in a.get("properties", [])}
    status = a.get("status")
    if status:
        props["status"] = {"name": "status", "typ": "status", "kurz": "Status", "status": status, "lang": f"Status {agg}"}
    kriterien, spalten = s.get("kriterien") or [], s.get("spalten") or []
    such, dto_spec = s.get("suchbegriff"), s.get("dto")
    if not (kriterien or such) or not spalten:
        raise SpecError("$.suche needs kriterien and spalten (property names of the aggregate)")
    for n in kriterien + spalten + (such or {}).get("felder", []):
        if n not in props:
            raise SpecError(f"$.suche: '{n}' is no property of {agg}")
    for x in s.get("ausschliessen", []):
        if not status or x not in [w[0] for w in status["werte"]]:
            raise SpecError(f"$.suche.ausschliessen: '{x}' is no status element")
    if such and not dto_spec:
        raise SpecError('$.suche.suchbegriff searches several columns with custom SQL: it needs "dto"')
    if dto_spec and not dto_spec.get("name"):
        raise SpecError("$.suche.dto needs a name")
    if dto_spec:
        for n in spalten:
            if props[n].get("verweis") or "felder" in props[n]:
                raise SpecError(f"$.suche.spalten: '{n}' is no column of its own; add it as dto.extra with its SQL")
    flt, repo = f"{agg}Filter", namen.get("sucherepo", agg + "SucheRepo")
    result = result_type(spec)
    cmd = s.get("name", f"{agg} suchen")
    m = "Map" + agg
    extras = (dto_spec or {}).get("extra", [])

    fprops = []
    if such:
        fprops.append(spec_property({"name": "suchbegriff", "typ": "string", "kurz": such.get("kurz", "Suchbegriff"),
                                     "laenge": [0, such.get("laenge", 60)]}, "$.suche.suchbegriff"))
    for n in kriterien:
        p = dict(props[n])
        if p["typ"] == "status":
            kurz = p.get("kurz", cap(n))
            fprops.append(business_property(n, status_type(p["status"]["name"]), kurz, p.get("lang", kurz)))
            continue
        if p["typ"] == "string":
            p["laenge"] = [0, (p.get("laenge") or [0, 200])[1]]
        p.pop("bereich", None)
        p.pop("unique", None)
        fprops.append(spec_property(p, f"$.suche.kriterien({n})"))
    fprops.append(business_property("ergebnisse", list_type(result), "Ergebnisse", f"Gefundene {agg}"))
    roots = []
    java = []
    if dto_spec:
        rows = [{"name": "id", "typ": "int", "kurz": "Id"}] + [{k: v for k, v in props[n].items() if k in ("name", "typ", "kurz", "status")} for n in spalten]
        rows += [{k: v for k, v in e.items() if k in ("name", "typ", "kurz", "status")} for e in extras]
        map_name = lower(result) + "Map"
        fields = {"id": "ID", **dict(zip(spalten, _columns(props, spalten))), **{e["name"]: column(e["name"]) for e in extras}}
        roots.append(("ergebnisdto", dto(result, [spec_property(r, f"$.suche.dto({r['name']})") for r in rows])))
        roots += [("filter", entity(flt, fprops, concept="DTO")), ("sucherepo", repository(repo, [mapper(map_name, result, fields)]))]
        rjava = _sql_java(agg, flt, result, map_name, props, s, status)
        java.append(Java("filter", _takeover_java(agg, result, s), f"{flt}: parse as CLASS_CONTENT into its member role; text2of.py"))
    else:
        roots += [("filter", entity(flt, fprops, concept="DTO")), ("sucherepo", repository(repo))]
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
        rjava = java_lines([f"public List<{agg}> suche({flt} filter) {{", *[f"  {x}" for x in pre],
                            f'  return WHERE("{m}", true, {" && ".join(preds)})'
                            f'.SORTBY(FIELD("{m}", "{spalten[0]}"), true);', "}"])

    wizard = len(kriterien) + (1 if such else 0) > 3
    shown = [(n, props[n]["typ"]) for n in spalten] + [(e["name"], e["typ"]) for e in extras]
    pct = max(5, 100 // len(shown))
    crits = [delegate("suchbegriff", "string", [] if wizard else ["IssueUpdateDOption"])] if such else []
    crits += [delegate(n, props[n]["typ"], CRITERION_OPTIONS.get(props[n]["typ"], []) + ([] if wizard else ["IssueUpdateDOption"]))
              for n in kriterien]
    crit_form = form(flt, crits, cols=1 if wizard else len(crits))
    result_table = table(flt, "ergebnisse", [delegate(n, t, [width(pct)]) for n, t in shown],
                         label=None if wizard else s.get("ergebnisLabel", "Ergebnisse"), actions=(menus or {}).get("tabelle", []))
    pane_actions = (menus or {}).get("pane")

    search = [f'filter.ergebnisse = CALL("{repo}", "suche", filter);']
    if s.get("keinTreffer"):
        search.append(f'PREW(!filter.ergebnisse.isEmpty(), "{s["keinTreffer"]}");')
    search.append("return filter;")
    takeover = "filter.uebernehmen(PUSHED());" if dto_spec else 'MERGE(PUSHED(), filter.ergebnisse, "entity", "list", "readonly");'
    handler = ["if (TERM_OK()) {", f"  {takeover}", "}"]
    if wizard:
        panes = [("kriterienpane", pane(f"{agg}SuchkriterienPP", flt, crit_form)),
                 ("ergebnispane", pane(f"{agg}SuchergebnisPP", flt, result_table, pane_actions))]
        pages = [page("Suchkriterien", flt, [f"{agg}SuchkriterienPP"], ["Weiter"], cmd),
                 page("Suchergebnisse", flt, [f"{agg}SuchergebnisPP"], ["Zurueck", "Aktualisieren"], f"{cmd}: Ergebnisse", term=agg)]
        bodies = [("page:Suchkriterien:init", ["return filter;"]),
                  ("page:Suchkriterien:conc:0", ['PAGE("Suchergebnisse");']),
                  ("page:Suchergebnisse:init", search),
                  ("page:Suchergebnisse:conc:0", ['PAGE("Suchkriterien");']),
                  ("page:Suchergebnisse:conc:1", ['PAGE("Suchergebnisse");']),
                  ("page:Suchergebnisse:term", handler)]
    else:
        panes = [("suchepane", pane(f"{agg}SuchePP", flt, grid(crit_form, result_table), pane_actions))]
        pages = [page("Suche", flt, [f"{agg}SuchePP"], ["Suchen", "Aktualisieren"], cmd, term=agg)]
        bodies = [("page:Suche:init", search),
                  ("page:Suche:conc:0", ['PAGE("Suche");']),
                  ("page:Suche:conc:1", ['PAGE("Suche");']),
                  ("page:Suche:term", handler)]
    # a status starts with its on-creation element; `optional` drops a criterion only when it is null
    init = [f"filter = new {flt}();"] + [f"filter.{n} = null;" for n in kriterien if props[n]["typ"] == "status"]
    bodies = [("init", init)] + bodies
    rechte = s.get("rechte")
    if rechte is None:
        r = (spec.get("commands") or {}).get("rechte") or {}
        rechte = r.get("schreiben", []) + r.get("lesen", [])
    # NEWSTYLE_CMD_TERM_HANDLING: required for the any cmd term handler, preferred pattern
    cmd_node = command(cmd, "SEARCH_CMD", variables=[var("filter", flt)], init=True, pages=pages, no_term=True,
                       permissions=[rw(x) for x in rechte])
    roots += panes + [("command", cmd_node)]
    java.append(Java("sucherepo", rjava, f"{repo}: parse as CLASS_CONTENT into its member role; text2of.py"))
    for i, (where, body) in enumerate(bodies, 1):
        java.append(Java(f"cmd-{i:02d}", java_lines(body), f"'{cmd}' {where}: parse as STATEMENTS into its body"))
    java.append(Java("", "", f"then text2of.py on the printed command '{cmd}' (one row per function body)"))
    notes = [f"Models: {flt} and {repo} belong in {rmodel} (imports {model}); page panes and command in {umodel}"
             f" (imports {rmodel}, {model} and the base model with AppRessourcen for the labels).",
             "The table menu is an empty Submenu: add the actions once the commands exist (scaffold step owner/edit)."]
    return Ergebnis(umodel, roots, java, notes), panes


def search_panes(spec, menus):
    """The page panes of the search with the menu entries of the commands."""
    return _build(spec, menus)[1]


@generator("suche", "scaffold.py suche SPEC [-o DIR]",
           "search: <X>Filter and <X>SucheRepo (unit.read), SEARCH_CMD with page panes (unit); up to 3 criteria one page "
           "(form over table, ISSUE UPDATE, conclusions Suchen/Aktualisieren), more a wizard; result list of entities, "
           "taken over by an any cmd term handler with session merge; with \"dto\" a list of DTOs from custom SQL, taken "
           "over by <X>Filter.uebernehmen")
def suche(spec, args=()):
    return _build(spec)[0]
