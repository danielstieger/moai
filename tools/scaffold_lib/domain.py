"""scaffold.py domain: aggregate with entities, status, persistence description, repository, service."""
from .bausteine import (SpecError, business_property, cap, column, entity, java_lines, key_property, list_type, lower,
                        property_status, repository, service, spec_property, status_decl, status_type, value_object)
from .persistenz import atom, entity_mapping, field, repository_java
from .registry import Ergebnis, Java, generator


def positions_of(a):
    """The position lists of an aggregate: "positionen" is one object or a list of them."""
    p = a.get("positionen") or []
    return p if isinstance(p, list) else [p]


def transition_params(t):
    """Further parameters of the service method, as Java: ", LocalDate heute"."""
    return "".join(", " + x for x in t.get("parameter", []))


def check_status_names(a):
    """A declaration exists once; the property `status` of an aggregate with a life cycle is taken."""
    props = a.get("properties", [])
    pos_props = [p for ps in positions_of(a) for p in (ps.get("entity") or {}).get("properties", [])]
    if a.get("status") and any(p.get("name") == "status" for p in props):
        raise SpecError("$.aggregat.properties: 'status' is the life cycle of the aggregate (aggregat.status); name the property differently")
    names = [a["status"].get("name")] if a.get("status") else []
    names += [p["status"].get("name") for p in props + pos_props if p.get("typ") == "status" and isinstance(p.get("status"), dict)]
    twice = sorted({n for n in names if names.count(n) > 1})
    if twice:
        raise SpecError(f"$.aggregat: status {', '.join(map(str, twice))} is declared more than once")


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
        lines += [f"public void {t['name']}({agg} {var}{transition_params(t)}) {{",
                  "  if (VALIDATION()) {",
                  f'    PRE(OF({var}.status, {von}), "{msg}", {var}.status);',
                  "  }",
                  f'  {var}.status = STATUS("{status["name"]}", "{t["nach"]}");',
                  "}"]
    return java_lines(lines) if lines else ""


def value_object_java(v):
    """Immutable style: constructor over all properties, with<Property> for each."""
    name, props = v["name"], v.get("properties", [])
    jtype = {"string": "String", "int": "int"}
    types = [jtype.get(p.get("typ"), p.get("typ")) for p in props]
    params = [f"{n}Wert" for n in (p["name"] for p in props)]  # not named like the property: see parameter names in text2of
    lines = [f"public {name}({', '.join(f'{t} {x}' for t, x in zip(types, params))}) {{"]
    lines += [f"  {p['name']} = {x};" for p, x in zip(props, params)] + ["}"]
    for p, t in zip(props, types):
        args = ", ".join("val" if q is p else q["name"] for q in props)
        lines += [f"public {name} with{cap(p['name'])}({t} val) {{", f"  return new {name}({args});", "}"]
    return java_lines(lines)


def getters_java(agg, props):
    return [Java(f"get-{p['name']}", java_lines(p["virtuell"].splitlines()),
                 f"{agg}.{p['name']} get:{p['name']}: parse as STATEMENTS, role statementList of its GetAccessor")
            for p in props if p.get("virtuell")]


@generator("domain", "scaffold.py domain SPEC [-o DIR]",
           "aggregate: value objects, entities, status, persistence description, aggregate repository, <Aggregat>Service "
           "with one method per state transition")
def domain(spec, args=()):
    for k in ("firma", "app", "bereich", "aggregat"):
        if not spec.get(k):
            raise SpecError(f"$.{k} is missing")
    a, namen = spec["aggregat"], spec.get("namen", {})
    agg, var = a.get("name"), lower(a.get("name") or "")
    if not agg:
        raise SpecError("$.aggregat.name is missing")
    model = namen.get("modell", f"{spec['firma']}.{spec['app']}.{spec['bereich']}.domain")
    repo = namen.get("repo", agg + "Repo")
    service_name = namen.get("service", agg + "Service")
    persistenz = namen.get("persistenz", cap(spec["bereich"]) + "Persistenz")
    table = column(agg)
    aprops = a.get("properties", [])

    props = [spec_property(p, f"$.aggregat.properties[{i}]") for i, p in enumerate(aprops)]
    atoms = [field("id", "ID")] + [atom(p) for p in aprops if not p.get("virtuell")]
    check_status_names(a)
    status = a.get("status")
    sdecl = property_status(aprops, "$.aggregat.properties")
    if status:
        sdecl.insert(0, status_decl(status, "$.aggregat.status"))
        props.append(business_property("status", status_type(status["name"]), "Status", f"Status {agg}"))
        atoms.append(field("status", "STATUS"))
    pos_list, position_roots, pos_mappings, getters = [], [], [], getters_java(agg, aprops)
    for i, pspec in enumerate(positions_of(a)):
        where = "$.aggregat.positionen" + (f"[{i}]" if isinstance(a["positionen"], list) else "")
        pe = pspec.get("entity") or {}
        if not pe.get("name") or not pspec.get("property"):
            raise SpecError(f"{where} needs property and entity.name")
        ptable = column(pe["name"])
        key = var + "Id"
        pprops_spec = pe.get("properties", [])
        pprops = [key_property(pe["name"], ptable),
                  business_property(key, "IntegerType", cap(agg), f"Schlüssel {agg}")]
        pprops += [spec_property(p, f"{where}.entity.properties[{j}]") for j, p in enumerate(pprops_spec)]
        patoms = [field("id", "ID"), field(key, table + "_ID")] + [atom(p) for p in pprops_spec if not p.get("virtuell")]
        kurz = pspec.get("kurz", cap(pspec["property"]))
        props.append(business_property(pspec["property"], list_type(pe["name"]), kurz, pspec.get("lang", kurz)))
        atoms.append({"concept": "ListMapping", "references": {"property": pspec["property"]},
                      "children": {"mappedfieldRef": {"concept": "KeyOnlyReferenceMapping",
                                                      "references": {"entityMapping": "Map" + pe["name"], "keyOnlyRef": key}}}})
        sort = next((p["name"] for p in pprops_spec if p.get("typ") == "int" and "nummer" in p["name"].lower()), "id")
        pos_list.append({"entity": pe["name"], "property": pspec["property"], "key": key, "sort": sort})
        pos_mappings.append(entity_mapping("Map" + pe["name"], pe["name"], ptable, patoms))
        position_roots.append(("position", entity(pe["name"], pprops, property_status(pprops_spec, f"{where}.entity.properties"))))
        getters += getters_java(pe["name"], pprops_spec)

    werte = spec.get("werteobjekte", [])
    roots = []
    wjava = []
    for i, v in enumerate(werte):
        if not v.get("name") or not v.get("properties"):
            raise SpecError(f"$.werteobjekte[{i}] needs name and properties")
        vprops = [spec_property(p, f"$.werteobjekte[{i}].properties[{j}]") for j, p in enumerate(v["properties"])]
        roots.append(("werteobjekt", value_object(v["name"], vprops, v.get("gleich") or [p["name"] for p in v["properties"]])))
        wjava.append(Java(f"werteobjekt-{v['name']}", value_object_java(v),
                          f"{v['name']}: parse as CLASS_CONTENT into its member role; text2of.py"))
    roots.append(("entity", entity(agg, [key_property(agg, table)] + props, sdecl)))
    roots += position_roots
    mappings = [entity_mapping("Map" + agg, agg, table, atoms)] + pos_mappings
    if spec.get("persistenzVorhanden"):
        # element mappings first: the list mapping of the aggregate refers to them
        roots += [("mapping", m, persistenz) for m in reversed(mappings)]
    else:
        roots.append(("persistence", {"concept": "PersistenceDescription", "properties": {"name": persistenz},
                                      "children": {"persistenceMapping": mappings}}))
    roots.append(("repository", repository(repo)))
    sjava = service_java(agg, var, status, spec.get("uebergaenge", []), "$.uebergaenge")
    if sjava:
        roots.append(("service", service(service_name)))
    java = wjava + [Java("repository", repository_java(agg, var, pos_list),
                         f"{repo}: parse as CLASS_CONTENT into its member role; text2of.py --repo-type checkout=CHECKOUT"
                         " --repo-type checkin=CHECKIN")]
    if sjava:
        java.append(Java("service", sjava, f"{service_name}: parse as CLASS_CONTENT into its member role; text2of.py"))
    java += getters
    notes = ["Import the models of referenced value objects and entities (e.g. sharedvalues).",
             "Then add the business logic: further preconditions, dependent values, rules."]
    if any(p.get("verweis") for ps in positions_of(a) for p in (ps.get("entity") or {}).get("properties", [])):
        notes.append("A position with a cross reference: FIELD(\"Map..\", \"id\") is ambiguous; run text2of.py with --persistenz.")
    if any(p.get("verweis") for p in aprops) and pos_list:
        notes.append("FIELD(\"Map..\", \"id\") next to a reference mapping is ambiguous; run text2of.py with --persistenz.")
    return Ergebnis(model, roots, java, notes)
