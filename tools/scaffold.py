#!/usr/bin/env python3
"""MoAI scaffolds: convention-compliant skeletons from a short JSON specification.

The MoWare conventions live in this generator; the specification only says what is specific. The tool writes
blueprints (checked against the structure export), method bodies as Java with markers (for text2of.py) and a plan
with the MCP steps in order. It calls no MPS itself. Call with `python3 -I`.

{generators}

Specification (domain):
  {"firma": "org.firma", "app": "fuhrpark", "bereich": "rechnung",
   "aggregat": {"name": "Rechnung",
                "properties": [PROPERTY, ...],
                "status": {"name": "RechnungStatus",
                           "werte": [["ERFASST", "E", "Erfasst", "Rechnung ist erfasst"], ...]},   first = on creation
                "positionen": {"property": "positionen", "kurz": "Positionen",   or a list of these
                               "entity": {"name": "Rechnungsposition", "properties": [PROPERTY, ...]}}},
   "uebergaenge": [{"name": "freigeben", "von": ["ERFASST"], "nach": "FREIGEGEBEN"[, "meldung": "..."]
                    [, "parameter": ["LocalDate heute"], "argumente": ["SERVERDATE()"]] (further arguments of the service
                    method and of its calls) [, "command": "name"] [, "rechte": ["Rolle"]]
                    [, "bestaetigen": "Page title?"] (modal with a DISABLED form, the service runs in the conclusion)}],
   "namen": {"repo": "RechnungsRepo", "service": "...", "persistenz": "...", "modell": "..."},   all optional
   "werteobjekte": [{"name": "Zeitraum", "properties": [PROPERTY, ...], "gleich": ["beginn", "ende"]}],   domain
   "persistenzVorhanden": true,   further aggregate of the area: its mappings go into the existing description
   "testConfig": "Test",          tests: the test OFXConfig of the suite
   "testDatum": [2026, 11, 15, 12, 0, 0],   tests: DEFAULT_DATETIME
   "testfaelle": [{"name": "..", "java": "..."}],   tests: further test methods, Java with markers
   "suche": {"kriterien": [...], "spalten": [...], "ausschliessen": ["STORNIERT"][, "name": "Rechnungen suchen"]
             [, "ergebnisLabel": "Rechnungen"]   search: property names of the aggregate (status included)
             [, "keinTreffer": "Keine Rechnung gefunden."] [, "rechte": ["Rolle"]]
             [, "suchbegriff": {"felder": ["nummer", "kunde"], "kurz": "Suchbegriff", "laenge": 60}]   one field over several columns
             [, "dto": {"name": "RechnungTreffer", "vorlauf": ["Java;"], "extra": [{"name": "summe", "typ": "int",
                        "kurz": "..", "sql": "SQL expression", "uebernahme": "Java expression"}]}]},   list of DTOs from custom SQL
   "commands": {"bearbeitbar": ["ERFASST"][, "anlegen"|"bearbeiten"|"kopf"|"positionBearbeiten"
                |"positionHinzufuegen": "command name"]   commands: status in which edit commands are enabled
                [, "rechte": {"schreiben": ["Rolle"], "lesen": ["Rolle"]}] (CAN_OPEN_RW / RO; lesen only on bearbeiten)
                [, "modal": true] (anlegen is GRAPH_OWNER_CMD_MODAL) [, "statusAuswahl": ["ERFASST", "AKTIV"]] (anlegen shows
                the status, limited to these) [, "anlegenService"|"kopfService": "method that validates in the conclusion"]},
   "configs": ["Test", "FX8"],    configs: templates to copy (default Test, FX8)
   "bereiche": ["rechnung"],      configs: areas; application configs scan their productive packages only
   "rollen": {..}, "anwendung": {..}, "ux": {..}   see the generators above
   "datenbank": {"url": "jdbc:mysql://...", "username": "...", "password": "..."}}   configs: overwrites

  PROPERTY: {"name": "rechnungsnummer", "typ": TYPE[, "kurz": "Rechnungsnr."][, "lang": "..."]
             [, "laenge": [1, 20]] (string) [, "bereich": [0, 365]] (int) [, "spalte": "RECHNUNGSNUMMER"]
             [, "felder": {"betrag": "BETRAG", ...}] (value object: column per component)
             [, "verweis": true] (cross reference to another aggregate's entity, column <NAME>_ID)
             [, "beispiel": "BD(\\"12.50\\")"] (tests: test value as Java with markers)
             [, "unique": true] [, "optional": true] (form: may stay empty) [, "leer": true] (status: anlegen starts empty)
             [, "virtuell": "return ...;"] (not persisted, get accessor as Java; also typ liste, "von": element type)}
  TYPE: string | int | LocalDate | DateTime | BigDecimal | name of a value object or entity (with felder / verweis)
        | status, with "status": {"name": .., "werte": [..]} as above; also on positions (e.g. "fahrzeugklasse").
          "aggregat.status" stays the life cycle with its "uebergaenge"; such a property has no transitions

Conventions applied: model <firma>.<app>.<bereich>.domain; names <Aggregat>Repo, <Aggregat>Service,
<Bereich>Persistenz (recommendations, overridable in "namen"); technical key `id` with sequence S_<TABLE>;
positions carry the parent key <aggregat>Id and are loaded explicitly; no delete method (objects are not
deleted physically, a status marks them); every transition checks its source status with a precondition
and then sets the target status.

This tool is the project's own copy: change it whenever it does not fit. It may break, it has no test suite and needs
none: blueprint.py checks every generated blueprint and the MPS checker checks the model, so a mistake shows up at once.
A limit of this tool is no limit of the language: do not change the model to suit it and do not write a separate
script. Extend this tool with the smallest change, without weakening its checks ("Unknown construct" in the DSL skills).

Where to change it (scaffold_lib/): an option = the generator that reads it (domain.py, tests_gen.py, suche.py,
commands.py, configs.py); a new generator = a new module with @generator, it is found automatically and listed above
(registry.py shows the form); nodes = bausteine.py, the public building blocks every generator uses; output = ausgabe.py.
Free page panes and commands need no code: scaffold.py ux. What a script would do belongs in a generator here.
"""
import sys

sys.dont_write_bytecode = True  # write no bytecode into the project or the package

import importlib
import json
import os
import pkgutil
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blueprint import Structure  # noqa: E402
from scaffold_lib.ausgabe import write  # noqa: E402
from scaffold_lib.bausteine import SpecError  # noqa: E402
from scaffold_lib.registry import GENERATORS  # noqa: E402

for _m in sorted(m.name for m in pkgutil.iter_modules([os.path.join(os.path.dirname(os.path.abspath(__file__)), "scaffold_lib")])):
    importlib.import_module(f"scaffold_lib.{_m}")


def usage():
    """The list of generators, generated from the registered ones."""
    out = []
    for _, line, summary in GENERATORS.values():
        out.append(f"  {line}")
        out += textwrap.wrap(summary, 100, initial_indent="        ", subsequent_indent="        ")
    return "\n".join(out)


def main(argv):
    if len(argv) < 3 or argv[1] in ("-h", "--help") or argv[1] not in GENERATORS:
        print(__doc__.replace("{generators}", usage()))
        return 0 if len(argv) > 1 and argv[1] in ("-h", "--help") else 2
    out = argv[argv.index("-o") + 1] if "-o" in argv else None
    args = [a for i, a in enumerate(argv[2:], 2) if a != "-o" and argv[i - 1] != "-o"]
    with open(args[0], encoding="utf-8") as f:
        spec = json.load(f)
    try:
        result = GENERATORS[argv[1]][0](spec, args[1:])
    except SpecError as e:
        print("error:", e, file=sys.stderr)
        print("hint: if the specification cannot express what the model needs, that is a limit of this tool, not of the "
              "language; change this tool, it is the project's own copy and blueprint.py and the MPS checker show "
              "mistakes at once (\"Unknown construct\" in the DSL skills)", file=sys.stderr)
        return 1
    return write(Structure(), result, out)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
