"""scaffold.py ux: page panes, commands, DTOs and read repositories that fit no aggregate scheme, written in JSON.

The form of the free parts of an application: what would otherwise be a script over the building blocks.
Every function body is Java with markers; the plan names it by its selector, text2of.py --bodies gives its owner.
"""
import re

from .bausteine import (DELEGATES, SpecError, command, delegate, dto, form, grid, id_param, java_lines, mapper, page, pane,
                        param_ref, path_delegate, reference_delegate, repository, ro, rw, selected_param,
                        spec_property, status_of, table, var, width)
from .registry import Ergebnis, Java, generator

OPTIONS = {"OPTIONAL": "OptionalDOption", "PICKER": "PickerDOption", "ISSUE": "IssueUpdateDOption", "DISABLED": "DisabledDOption"}


def _feld(f, where):
    """{"feld": "stand", "typ": "int", "optionen": ["PICKER"], "breite": 20}; {"pfad": "lenker.nachname", "typ": "string"};
    {"feld": "lenker", "typ": "verweis", "zeigt": ["nachname", "vorname"]}."""
    opts = []
    for o in f.get("optionen", []):
        if o not in OPTIONS:
            raise SpecError(f"{where}: option '{o}' is not one of {', '.join(OPTIONS)}")
        opts.append(OPTIONS[o])
    if "breite" in f:
        opts.append(width(f["breite"]))
    if f.get("typ") == "verweis":
        if not f.get("feld") or not f.get("zeigt"):
            raise SpecError(f'{where}: typ verweis needs "feld" and "zeigt": properties shown in the selection')
        return reference_delegate(f["feld"], f["zeigt"], opts)
    if f.get("typ") not in DELEGATES:
        raise SpecError(f"{where}: typ '{f.get('typ')}' is not one of {', '.join(DELEGATES)}, verweis")
    if "pfad" in f:
        first, _, second = f["pfad"].partition(".")
        if not second:
            raise SpecError(f"{where}: pfad is a.b")
        return path_delegate(first, second, f["typ"], opts)
    if not f.get("feld"):
        raise SpecError(f'{where}: needs "feld" or "pfad"')
    return delegate(f["feld"], f["typ"], opts)


def _layout(x, cls, where):
    """{"form": [FELD], "disabled": true, "label": "..", "spalten": 2} | {"tabelle": "property", "felder": [FELD], "label": ..,
    "menue": [..]} | {"grid": [LAYOUT]}; "an": the class, if not the one of the pane."""
    cls = x.get("an", cls)
    if "form" in x:
        return form(cls, [_feld(f, f"{where}.form[{i}]") for i, f in enumerate(x["form"])],
                    disabled=x.get("disabled", False), label=x.get("label"), cols=x.get("spalten", 1))
    if "tabelle" in x:
        return table(cls, x["tabelle"], [_feld(f, f"{where}.felder[{i}]") for i, f in enumerate(x.get("felder", []))],
                     label=x.get("label"), actions=x.get("menue", []))
    if "grid" in x:
        return grid(*[_layout(k, cls, f"{where}.grid[{i}]") for i, k in enumerate(x["grid"])])
    raise SpecError(f'{where}: a layout has "form", "tabelle" or "grid"')


def _param(p, where):
    """{"name": "auswahl", "auswahl": "Klasse"} selection; {"name": "xId", "id": "Klasse"} only its key."""
    if not p.get("name"):
        raise SpecError(f"{where}: needs a name")
    if "auswahl" in p:
        return selected_param(p["name"], p["auswahl"])
    if "id" in p:
        return id_param(p["name"], p["id"])
    raise SpecError(f'{where}: a parameter has "auswahl" or "id"')


def _stem(name):
    plain = name.lower().translate(str.maketrans({"ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss"}))
    return re.sub(r"[^a-z0-9]+", "-", plain).strip("-")


def _command(c, where, java):
    """{"name", "typ", "rechte": {"rw": [..], "ro": [..]}, "parameter": [..], "variablen": {"x": "Klasse"}, "aktiv":
    {"parameter": "auswahl", "status": [..], "property": "status"}, "zuruecksetzen": "x", "finalOk": "x", "hotkey": "ENTER",
    "init": JAVA, "ok": JAVA, "seiten": [{"name", "an", "pane", "titel", "init": JAVA, "scopes": JAVA,
    "abschluesse": [{"label", "java"}], "term": {"klasse", "java"}}]}."""
    if not c.get("name"):
        raise SpecError(f"{where}: needs a name")
    name = c["name"]
    bodies = []
    pages = []
    for i, s in enumerate(c.get("seiten", [])):
        w = f"{where}.seiten[{i}]"
        for k in ("name", "an", "pane"):
            if not s.get(k):
                raise SpecError(f"{w}: needs {k}")
        concs = s.get("abschluesse", [])
        pages.append(page(s["name"], s["an"], [s["pane"]], [x["label"] for x in concs], s.get("titel", name),
                          term=(s.get("term") or {}).get("klasse"), scopes="scopes" in s))
        if "init" in s:
            bodies.append((f"page:{s['name']}:init", s["init"]))
        if "scopes" in s:
            bodies.append((f"page:{s['name']}:scopes", s["scopes"]))
        bodies += [(f"page:{s['name']}:conc:{j}", x["java"]) for j, x in enumerate(concs) if "java" in x]
        if s.get("term"):
            bodies.append((f"page:{s['name']}:term", s["term"]["java"]))
    if "init" in c:
        bodies.append(("init", c["init"]))
    if "ok" in c:
        bodies.append(("ok", c["ok"]))
    aktiv = c.get("aktiv")
    node = command(name, c.get("typ"), params=[_param(p, f"{where}.parameter") for p in c.get("parameter", [])],
                   variables=[var(n, k) for n, k in c.get("variablen", {}).items()], init="init" in c, ok="ok" in c,
                   pages=pages, final=c.get("finalOk"), revert=c.get("zuruecksetzen"), hotkey=c.get("hotkey"),
                   enabled=status_of(param_ref(aktiv["parameter"]), aktiv["status"], aktiv.get("property", "status")) if aktiv else None,
                   no_term=any(s.get("term") for s in c.get("seiten", [])),
                   permissions=[rw(r) for r in (c.get("rechte") or {}).get("rw", [])] + [ro(r) for r in (c.get("rechte") or {}).get("ro", [])])
    for sel, text in bodies:
        java.append(Java(f"{_stem(name)}-{_stem(sel)}", java_lines(text.splitlines()), f"'{name}' {sel}: parse as STATEMENTS into its body"))
    return node


@generator("ux", "scaffold.py ux SPEC [-o DIR]",
           "free page panes, commands, DTOs and read repositories in JSON (\"ux\", help: scaffold_lib/ux.py): everything "
           "that fits no aggregate scheme; roots in the order dtos, repos, panes, commands")
def ux(spec, args=()):
    u = spec.get("ux") or {}
    if not u.get("modell"):
        raise SpecError("$.ux.modell is missing")
    roots, java = [], []
    for i, d in enumerate(u.get("dtos", [])):
        w = f"$.ux.dtos[{i}]"
        if not d.get("name"):
            raise SpecError(f"{w}: needs a name")
        roots.append(("dto", dto(d["name"], [spec_property(p, f"{w}.properties[{j}]") for j, p in enumerate(d.get("properties", []))])))
        if d.get("java"):
            java.append(Java(f"dto-{_stem(d['name'])}", java_lines(d["java"].splitlines()),
                             f"{d['name']}: parse as CLASS_CONTENT into its member role; text2of.py"))
    for i, r in enumerate(u.get("repos", [])):
        w = f"$.ux.repos[{i}]"
        if not r.get("name"):
            raise SpecError(f"{w}: needs a name")
        roots.append(("repo", repository(r["name"], [mapper(m["name"], m["dto"], m["felder"]) for m in r.get("mapper", [])])))
        if r.get("java"):
            java.append(Java(f"repo-{_stem(r['name'])}", java_lines(r["java"].splitlines()),
                             f"{r['name']}: parse as CLASS_CONTENT into its member role; text2of.py"))
    for i, p in enumerate(u.get("panes", [])):
        w = f"$.ux.panes[{i}]"
        for k in ("name", "an", "inhalt"):
            if not p.get(k):
                raise SpecError(f"{w}: needs {k}")
        roots.append(("pane", pane(p["name"], p["an"], _layout(p["inhalt"], p["an"], f"{w}.inhalt"), p.get("menue"))))
    for i, c in enumerate(u.get("commands", [])):
        roots.append(("command", _command(c, f"$.ux.commands[{i}]", java)))
    if u.get("commands"):
        java.append(Java("", "", "then text2of.py on each printed command (one row per function body)"))
    return Ergebnis(u["modell"], roots, java, u.get("hinweise", []))
