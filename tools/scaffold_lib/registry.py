"""Where generators register themselves.

New generator: a module in this folder (found automatically) with one function:

    @generator("rollen", "scaffold.py rollen SPEC [-o DIR]", "RolesAndPermissions with one static role per name")
    def rollen(spec, args):
        return Ergebnis(model, roots, java, notes)

`spec` is the parsed specification, `args` the further command-line files (configs: the dumps). The result:
  model  name of the target model;
  roots  (kind, short spec) in insertion order, or (kind, short spec, "=replace" | name of an existing root to add into);
  java   Java(stem, text, how): a file with method bodies and how to parse it; Java("", "", text): only a line of the plan;
  notes  further lines of the plan.
Short specs are the form of `blueprint.py build`, built with bausteine.py. Every root is expanded and checked against
the structure of the languages when it is written (ausgabe.py).
"""
from collections import namedtuple

Ergebnis = namedtuple("Ergebnis", "model roots java notes")
Java = namedtuple("Java", "stem text how")
GENERATORS = {}


def generator(name, usage, summary):
    def register(fn):
        GENERATORS[name] = (fn, usage, summary)
        return fn
    return register
