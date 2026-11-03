#!/usr/bin/env python3
"""MoAI Text -> ObjectFlow: turn Java text with markers into ObjectFlow / ManMap nodes.

Workflow (see the DSL skills):
  1. Insert the methods as Java text with `mps_mcp_parse_java_and_insert` (featureKind CLASS_CONTENT or METHOD,
     insert.mode child into the root's `member` role). The parser leaves the markers unresolved; that is expected.
  2. `mps_mcp_print_node` (deep=true) of the root.
  3. python3 -I moai_plugin/tools/text2of.py ROOTDUMP [--repo-type METHOD=TYPE]... [--only NAME]... [--persistenz DUMP]
     writes one blueprint per member into the system temp directory and prints a table:
       name | reference of the node to replace (SET CHILD childNodeRef) | file
     Constructors and test methods are replaced through their body only, so references to them stay valid.
     Commands, AppUI modules and roles: one row per function with statements, named by its selector (--only selector):
       init, ok, auth, page:NAME:init, page:NAME:scopes, page:NAME:term, page:NAME:conc:N, role:NAME:is; virtual
       properties: get:NAME.
     --persistenz DUMP (print_node deep=true of the PersistenceDescription): FIELD binds to the mapping's own field, for
       a name that is ambiguous next to a reference mapping (`id`).
  4. `mps_mcp_update_node` SET CHILD per row, then FIX_REFERENCES on the root (calls between replaced members
     bind to the old node until the last row is set), `moai_plugin/tools/verify.py node` and the model check.
     A replaced method has a new id: FIX_REFERENCES on the roots that call it too; the checker stays quiet about those,
     the compiler reports `<identifier> expected`. Do not pass postProcess.resolveReferences:false to the parser: `new X()`
     stays unresolved then.

  text2of.py ROOTDUMP --bodies   where Java text goes: selector | owner (parentRef) | role | body. Replaces searching a
     dump for the owner of a function: mps_mcp_parse_java_and_insert, insert.mode child, parentRef = owner, role.

The kind of method follows the root: methods of a Service become service methods, of a Repository repository
methods (`--repo-type name=CHECKOUT|CHECKIN|DELETE`, default READONLY), otherwise plain instance methods.

Plain Java:
  x.prop / own prop                              -> business property reference (no marker)
  String, List<T>, new ArrayList<T>()            -> string, list<T>, new arraylist<T>
  coll.where(l) select(l) any(l) all(l) findFirst(l) translate(l) foldLeft(seed,l) sortBy(l,asc) size() isEmpty()
      isNotEmpty() first() last() toList() distinct() add(e) remove(e) contains(e)    -> collections operations
      (add/remove/contains on a BigDecimal-looking operand or argument -> BigDecimal method; otherwise list; on a string
       write ISEMPTY(s), ISNOTEMPTY(s), CONTAINS(s,x); a lambda parameter becomes an inferred closure parameter)
Anything else that stays unresolved stops the tool with its location.

{markers}
This tool is the project's own copy: change it whenever it does not fit. It may break, it has no test suite and needs
none: the blueprint write and the MPS checker show what does not fit, so a mistake shows up at once.
A limit of this tool is no limit of the language: do not change the model to suit it and do not write a separate
script. Extend this tool with the smallest change, without weakening its checks ("Unknown construct" in the DSL skills).

Where to change it (text2of_lib/): a marker = a function with @marker in markers/<topic>.py, the list above is generated
from it, a new file there is found automatically (registry.py shows the form); collections and BigDecimal operations =
tables in methoden.py; plain Java the parser leaves unresolved = java.py; which nodes of a root are converted = wurzeln.py.
"""
import sys

sys.dont_write_bytecode = True  # write no bytecode into the project or the package

import json
import os
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blueprint import Checker, Structure, report  # noqa: E402
from text2of_lib.knoten import load  # noqa: E402
from text2of_lib.registry import TOPICS  # noqa: E402
from text2of_lib.wurzeln import bodies, convert_root, field_refs  # noqa: E402

TOOL_LIMIT = ("hint: a limit of this tool is no limit of the language; do not change the model to suit it, change "
              "this tool, it is the project's own copy and the MPS checker shows mistakes at once "
              "(\"Unknown construct\" in the DSL skills)")


def marker_help():
    """The marker list, generated from the registered markers."""
    out = []
    for module, rows in sorted(TOPICS.items()):
        title = (sys.modules[module].__doc__ or module).strip()
        out.append(title + ":")
        out += [f"  {syntax:<46} -> {result}" for syntax, result in rows]
    return "\n".join(out)


def main(argv):
    args, repo_types, only = argv[1:], {}, set()
    if not args or args[0] in ("-h", "--help"):
        print(__doc__.replace("{markers}", marker_help()))
        return 0 if args else 2
    dump = args.pop(0)
    fields, list_bodies = None, False
    while args:
        a = args.pop(0)
        if a == "--repo-type":
            k, _, v = args.pop(0).partition("=")
            repo_types[k] = v
        elif a == "--only":
            only.add(args.pop(0))
        elif a == "--persistenz":
            fields = field_refs(load(args.pop(0)))
        elif a == "--bodies":
            list_bodies = True
        else:
            print(f"unknown option {a}", file=sys.stderr)
            return 2
    root = load(dump)
    if list_bodies:
        for row in bodies(root):
            print(" | ".join(row))
        return 0
    rows, errors = convert_root(root, repo_types, only, fields)
    for e in errors:
        print("error:", e, file=sys.stderr)
    if errors:
        print(TOOL_LIMIT, file=sys.stderr)
    st = Structure()
    rc = 1 if errors else 0
    outdir = tempfile.mkdtemp(prefix="moai-text2of-")
    for name, target, bp in rows:
        chk = Checker(st)
        chk.node(bp, f"{name}")
        if report(chk):
            rc = 1
            continue
        path = os.path.join(outdir, target.rsplit("/", 1)[-1] + ".json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(bp, f, ensure_ascii=False, separators=(",", ":"))
        print(f"{name} | {target} | {path}")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
