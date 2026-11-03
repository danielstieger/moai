"""scaffold.py commands: owner, edit and transition commands with page panes."""
import re

from .bausteine import (DELEGATES, SpecError, cap, command, delegate, form, grid, id_param, java_lines, lower, page, pane,
                        param_ref, ro, rw, selected_param, status_of, table, var, width)
from .domain import domain, positions_of
from .registry import Ergebnis, Java, generator
from .suche import result_type, search_panes


def editable(props):
    """(properties a form can show, names of the others)."""
    ok = [p for p in props if p.get("typ") in DELEGATES and not p.get("verweis") and "felder" not in p and not p.get("virtuell")]
    return ok, [p["name"] for p in props if p not in ok and not p.get("virtuell")]


def spec_form(cls, props, disabled=False, label=None, numbered=None):
    ds = []
    for p in props:
        opts = []
        if p.get("optional"):
            opts.append("OptionalDOption")
        if disabled is False and p["typ"] in ("LocalDate", "DateTime"):
            opts.append("PickerDOption")
        if disabled is False and p["name"] == numbered:
            opts.append("DisabledDOption")
        ds.append(delegate(p["name"], p["typ"], opts))
    return form(cls, ds, disabled=disabled, label=label)


def _concluded(service, method, var_name, also=()):
    """The lines of a conclusion: the service method that validates, if named, then done."""
    call = [f'CALL("{service}", "{method}", {", ".join([var_name, *also])});'] if method else []
    return call + ["DONE();"]


@generator("commands", "scaffold.py commands SPEC [-o DIR]",
           "owner, edit and transition commands with page panes (unit): <X> anlegen, <X> bearbeiten (key only, checkout, "
           "DISABLED form over the positions), GRAPH_EDIT_CMDs for head data and positions, one owner command per "
           "transition, with a confirmation page if asked; with \"suche\" also the search page panes with the menu entries")
def commands(spec, args=()):
    model = domain(spec).model   # validates the specification the same way
    a, namen, c = spec["aggregat"], spec.get("namen", {}), spec.get("commands") or {}
    agg, v = a["name"], lower(a["name"])
    repo, service = namen.get("repo", agg + "Repo"), namen.get("service", agg + "Service")
    umodel = namen.get("unitmodell", model.rsplit(".", 1)[0] + ".unit")
    status, positions = a.get("status"), positions_of(a)
    snames = [w[0] for w in status["werte"]] if status else []
    bearbeitbar = c.get("bearbeitbar", [])
    for x in bearbeitbar:
        if x not in snames:
            raise SpecError(f"$.commands.bearbeitbar: '{x}' is no status element")
    auswahl_status = c.get("statusAuswahl", [])
    for x in auswahl_status:
        if x not in snames:
            raise SpecError(f"$.commands.statusAuswahl: '{x}' is no status element")

    aprops, askip = editable(a.get("properties", []))
    n_new, n_edit = c.get("anlegen", f"{agg} anlegen"), c.get("bearbeiten", f"{agg} bearbeiten")
    n_head = c.get("kopf", f"{agg} Kopfdaten bearbeiten")
    transitions = spec.get("uebergaenge", [])
    n_trans = [(t, t.get("command", f"{agg} {t['name']}")) for t in transitions]
    rechte = c.get("rechte") or {}
    write = [rw(r) for r in rechte.get("schreiben", [])]
    selection = result_type(spec) if spec.get("suche") else agg
    owner_type = "GRAPH_OWNER_CMD_MODAL" if c.get("modal") else "GRAPH_OWNER_CMD"

    edit_enabled = status_of(param_ref(v), bearbeitbar) if bearbeitbar else None
    roots, bodies = [], []
    checkin = [f'CALL("{repo}", "checkin", {v});']

    # <X> anlegen: owner with an editable form, saved in FINAL OK, pushed for the search
    new_props = aprops + ([{"name": "status", "typ": "status"}] if auswahl_status else [])
    roots.append(("anlegenpane", pane(f"{agg}AnlegenPP", agg, spec_form(agg, new_props))))
    roots.append(("anlegen", command(n_new, owner_type, variables=[var(v, agg)], init=True, ok=True, final=v, permissions=write,
                                     pages=[page("Neu", agg, [f"{agg}AnlegenPP"], ["SpeichernUndSchliessen"], n_new,
                                                 scopes=bool(auswahl_status))])))
    # a status starts with its on-creation element; "leer": the user has to choose
    new_init = [f"{v} = new {agg}();"] + [f"{v}.{p['name']} = null;" for p in aprops if p.get("leer")]
    new_bodies = [("init", new_init), ("page:Neu:init", [f"return {v};"])]
    if auswahl_status:
        elems = ", ".join(f'STATUS("{status["name"]}", "{x}")' for x in auswahl_status)
        new_bodies.append(("page:Neu:scopes", [f"META({v}.status).setElements({elems});"]))
    new_bodies += [("page:Neu:conc:0", _concluded(service, c.get("anlegenService"), v)), ("ok", checkin)]
    bodies.append((n_new, new_bodies))

    # <X> bearbeiten: GRAPH_OWNER_CMD with the key only, checkout in command init, DISABLED form
    shown = aprops + ([{"name": "status", "typ": "status"}] if status else [])
    head = spec_form(agg, shown, disabled=True, label=agg if positions else None)
    pos_rows, pskip, pos_parts = [], [], []
    for pos in positions:
        pe = pos["entity"]["name"]
        pprops, skipped = editable(pos["entity"].get("properties", []))
        pskip += skipped
        pnum = next((p["name"] for p in pprops if p["typ"] == "int" and "nummer" in p["name"].lower()), None)
        one = len(positions) == 1
        n_pedit = c.get("positionBearbeiten", f"{pe} bearbeiten") if one else f"{pe} bearbeiten"
        n_padd = c.get("positionHinzufuegen", f"{pe} hinzufügen") if one else f"{pe} hinzufügen"
        pct = max(5, 100 // max(1, len(pprops)))
        pos_rows.append(table(agg, pos["property"], [delegate(p["name"], p["typ"], [width(pct)]) for p in pprops],
                              label=pos.get("kurz", cap(pos["property"])), actions=[n_pedit, n_padd]))
        pos_parts.append((pos, pe, pprops, pnum, n_pedit, n_padd))
    child = grid(head, *pos_rows) if pos_rows else head
    roots.append(("bearbeitenpane", pane(f"{agg}PP", agg, child, [n_head])))
    roots.append(("bearbeiten", command(n_edit, owner_type if c.get("bearbeitenModal") else "GRAPH_OWNER_CMD", hotkey="ENTER",
                                        permissions=write + [ro(r) for r in rechte.get("lesen", [])],
                                        params=[id_param(v + "Id", selection)],
                                        variables=[var(v, agg)], init=True, ok=True, final=v,
                                        pages=[page(agg, agg, [f"{agg}PP"], ["SpeichernUndSchliessen"], agg)])))
    bodies.append((n_edit, [("init", [f'{v} = CALL("{repo}", "checkout", {v}Id);']),
                            (f"page:{agg}:init", [f"return {v};"]), (f"page:{agg}:conc:0", ["DONE();"]),
                            ("ok", checkin)]))

    # GRAPH_EDIT_CMDs: editable forms, opened from the owner's menus; revert the aggregate on cancel
    roots.append(("kopfpane", pane(f"{agg}KopfPP", agg, spec_form(agg, aprops))))
    roots.append(("kopf", command(n_head, params=[selected_param(v, agg)], enabled=edit_enabled, revert=v, permissions=write,
                                  pages=[page("Kopfdaten", agg, [f"{agg}KopfPP"], ["OK"], n_head)])))
    bodies.append((n_head, [("page:Kopfdaten:init", [f"return {v};"]),
                            ("page:Kopfdaten:conc:0", _concluded(service, c.get("kopfService"), v))]))
    for pos, pe, pprops, pnum, n_pedit, n_padd in pos_parts:
        pvar = lower(pe)
        roots.append(("positionpane", pane(f"{pe}PP", pe, spec_form(pe, pprops, numbered=pnum))))
        roots.append(("positionbearbeiten", command(
            n_pedit, hotkey="ENTER", params=[selected_param(v, agg), selected_param(pvar, pe)], permissions=write,
            enabled=edit_enabled, revert=v, pages=[page(pe, pe, [f"{pe}PP"], ["OK"], n_pedit)])))
        bodies.append((n_pedit, [(f"page:{pe}:init", [f"return {pvar};"]), (f"page:{pe}:conc:0", ["DONE();"])]))
        add = [f"{pvar} = new {pe}();"]
        if pnum:
            add.append(f"{pvar}.{pnum} = {v}.{pos['property']}.size() + 1;")
        add.append(f"{v}.{pos['property']}.add({pvar});")
        roots.append(("positionhinzufuegen", command(
            n_padd, params=[selected_param(v, agg)], variables=[var(pvar, pe)], init=True, permissions=write,   # GRAPH_EDIT_CMD pushes nothing
            enabled=edit_enabled, revert=v, pages=[page("Neu", pe, [f"{pe}PP"], ["OK"], n_padd)])))
        bodies.append((n_padd, [("init", add), ("page:Neu:init", [f"return {pvar};"]), ("page:Neu:conc:0", ["DONE();"])]))

    # one GRAPH_OWNER_CMD per transition: generally enabled reads the status of the selection; no page, or a confirmation
    confirm_pane = False
    for t, n in n_trans:
        perms = [rw(r) for r in t["rechte"]] if "rechte" in t else write
        call = f'CALL("{service}", "{t["name"]}", {", ".join([v, *t.get("argumente", [])])});'
        checkout = f'{v} = CALL("{repo}", "checkout", auswahl.id);'
        enabled = status_of(param_ref("auswahl"), t["von"])
        params = [selected_param("auswahl", selection)]
        if t.get("bestaetigen"):
            if not confirm_pane:
                roots.append(("bestaetigenpane", pane(f"{agg}BestaetigenPP", agg, spec_form(agg, shown, disabled=True))))
                confirm_pane = True
            roots.append(("uebergang", command(
                n, "GRAPH_OWNER_CMD_MODAL", params=params, variables=[var(v, agg)], init=True, ok=True, final=v, enabled=enabled,
                permissions=perms, pages=[page("Bestaetigen", agg, [f"{agg}BestaetigenPP"], ["SpeichernUndSchliessen"], t["bestaetigen"])])))
            bodies.append((n, [("init", [checkout]), ("page:Bestaetigen:init", [f"return {v};"]),
                               ("page:Bestaetigen:conc:0", [call, "DONE();"]), ("ok", checkin)]))
        else:
            roots.append(("uebergang", command(n, "GRAPH_OWNER_CMD", params=params, variables=[var(v, agg)], init=True,
                                               ok=True, final=v, enabled=enabled, permissions=perms)))
            bodies.append((n, [("init", [checkout, call, "DONE();"]), ("ok", checkin)]))

    search = []
    if spec.get("suche"):
        search = [(k, sp, "=replace") for k, sp in search_panes(spec, {"tabelle": [n_edit] + [n for _, n in n_trans],
                                                                        "pane": [n_new]})]
    java = []
    for name, fs in bodies:
        for i, (where, lines) in enumerate(fs, 1):
            plain = name.lower().translate(str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}))
            stem = re.sub(r"[^a-z0-9]+", "-", plain).strip("-")
            java.append(Java(f"{stem}-{i}", java_lines(lines), f"'{name}' {where}: parse as STATEMENTS into its body"))
    java.append(Java("", "", "then text2of.py on each printed command (one row per function body)"))
    notes = [f"Model {umodel} imports {model}, the unit.read model of the search and the base model (labels).",
             "Business checks belong in the conclusions: call the service methods that validate (conventions:"
             " the service checks, the form only takes input)."]
    if askip or pskip:
        notes.append("Not in the forms (value objects, cross references): " + ", ".join(askip + pskip)
                     + "; add delegates with a path (e.g. betrag.betrag) or a selection: scaffold.py ux.")
    if positions:
        added = [pos["entity"]["name"] for pos in positions]
        notes.append(f"Adding {', '.join(added)} happens in command init; move it into a list helper of {agg} or the"
                     f" service if adding has business rules.")
    if not rechte:
        notes.append("No \"commands.rechte\": the commands have no permissions yet (conventions: CAN_OPEN_RW/RO with roles).")
    return Ergebnis(umodel, search + roots, java, notes)
