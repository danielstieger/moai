"""scaffold.py configs: OFXConfigs from the wbkit templates, Static Ressources."""
from .bausteine import SpecError, literal
from .registry import Ergebnis, generator

LABELS = [("Weiter", "Weiter", "F4"), ("Zurueck", "Zurück", "F3"), ("Aktualisieren", "Aktualisieren", "F12"),
          ("OK", "OK", "F12"), ("SpeichernUndSchliessen", "Speichern & Schließen", "F12"),
          ("Suchen", "Suchen", "SCAN_UPDATE")]
OF = "org.modellwerkstatt.objectflow.structure."


def production_packages(spec):
    """What the application config scans: the productive packages. <firma>.<app> would also take in *.tests, whose TestDaten
    need CS: NoSuchBeanDefinitionException at app start."""
    root = f"{spec['firma']}.{spec['app']}"
    areas = spec.get("bereiche") or ([spec["bereich"]] if spec.get("bereich") else [])
    return [f"{root}.{b}.{x}" for b in areas for x in ("domain", "read", "unit")] + [f"{root}.rollen", f"{root}.app"]


def _scan_only(config, packages):
    for ch in config.get("children", []):
        if ch["role"] == "dependencyResolution":
            for n in ch["nodes"]:
                if n["concept"].endswith(".ComponentsScanning"):
                    n["children"] = [{"role": "componentBaseName", "nodes": [expand_literal(p) for p in packages]}]


def expand_literal(text):
    return {"concept": "jetbrains.mps.baseLanguage.structure.StringLiteral",
            "properties": [{"name": "value", "value": text}]}


def ressourcen():
    return {"concept": "StaticRessources", "properties": {"name": "AppRessourcen"},
            "children": {"platforms": {"concept": "PlatformDeclaration", "properties": {"name": "RICH"}},
                         "labels": [{"concept": "Label", "properties": {"name": n},
                                     "children": {"specification": {"concept": "LabelSpecification",
                                                                    "properties": {"hotkey": k},
                                                                    "children": {"text": literal(text)}}}}
                                    for n, text, k in LABELS]}}


@generator("configs", "scaffold.py configs SPEC DUMP... [-o DIR]",
           "OFXConfigs from the wbkit templates (DUMP: print_node deep=true of baseconfig and of each wanted config in "
           "org.modellwerkstatt.wbkit.shared.configuration): firma.app replaced, sections not included dropped, database "
           "overwrites; Static Ressources AppRessourcen (platform RICH, labels and hotkeys of the conventions)")
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
    test_config = spec.get("testConfig", "Test")
    packages = production_packages(spec)
    for name, bp in out[1:]:
        if name != test_config and spec.get("bereiche", spec.get("bereich")):
            _scan_only(bp, packages)
    db = spec.get("datenbank")
    if db:
        for name, bp in out[1:]:
            for ch in bp.get("children", []):
                for x in ch["nodes"]:
                    if x["concept"].endswith(".OFXConfigInclude") and any(
                            r["target"].startswith("LocalDB_") for r in x.get("references", [])):
                        x.setdefault("children", []).append({"role": "properties", "nodes": [
                            {"concept": OF + "OFXConfigPropOverwrite",
                             "references": [{"role": "property", "target": k}],
                             "children": [{"role": "value", "nodes": [expand_literal(v)]}]}
                            for k, v in db.items()]})
    troots = [("config", bp) for _, bp in out] + [("ressourcen", ressourcen())]
    notes = ["Model content: only OFXConfigs and Static Ressources; it imports nothing (conventions)."]
    notes += [f"dropped (not included by {', '.join(wanted)}): {d}" for d in cp.dropped]
    notes += [f"will not resolve: {o}" for o in cp.outside]
    if not db:
        notes.append("No \"datenbank\" in the spec: the LocalDB section keeps ${DB_URL}/${DB_USERNAME}/${DB_PASSWORD}.")
    elif "serverTimezone=UTC" in db.get("url", ""):
        notes.append("serverTimezone=UTC with a JVM in another time zone shifts every LocalDate by a day: set the zone of the"
                     " JVM, e.g. serverTimezone=Europe/Vienna.")
    if spec.get("bereiche", spec.get("bereich")):
        notes.append(f"Application configs scan only {', '.join(packages)}: add new areas to \"bereiche\".")
    else:
        notes.append("No \"bereiche\": the application configs scan all of firma.app, also the tests; list the areas.")
    return Ergebnis(model, troots, [], notes)
