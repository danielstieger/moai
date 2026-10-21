#!/usr/bin/env python3
"""MoAI target/actual comparison: did MPS keep what the blueprint said?

  node BLUEPRINT ACTUAL     BLUEPRINT is the full blueprint of the insert (as written by blueprint.py);
                            ACTUAL is `mps_mcp_print_node` of the inserted node with deep=true (the temp
                            file or its envelope). For `ADD CHILD`, print the new child; for a root, the root.

Reported:
  deviation  a property the blueprint set has another value; a reference is unresolved or points to
             another name; a role the blueprint named has another number of children or another concept.
             Exit code 1.
  added      properties and roles that only MPS set (node factories, constructors). Read them: most are
             harmless (resolveInfo, an id key), some change meaning (DateLiteral fromServer=true).

A blueprint value equal to the property's default (false, 0, empty, the enum default) may be missing in
ACTUAL, because MPS does not store defaults; that is not a deviation. Call with `python3 -I`.
"""
import sys

sys.dont_write_bytecode = True  # write nothing into the package (moai/ is a submodule in projects)

import json
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blueprint import Structure  # noqa: E402


def load(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "ok" in data and "data" in data:
        data = data["data"]
    if isinstance(data, str):
        return load(data)
    return data


def fq_of(actual):
    ref = actual.get("conceptReference", "")
    return ref.rsplit(":", 1)[-1] if ref else actual.get("concept")


def default_of(st, fq, name):
    _, f = st.role(fq, name) if fq in st.concepts else (None, None)
    if not f:
        return {"", "false", "0"}
    if f.get("default"):
        return {f["default"]}
    return {"boolean": {"false"}, "integer": {"0"}, "string": {""}}.get(f.get("type"), set())


class Comparison:
    def __init__(self, st):
        self.st = st
        self.deviations, self.added = [], []

    def node(self, bp, act, path):
        fq_bp = self.st.resolve(bp["concept"]) if bp["concept"] in self.st.concepts or "." not in bp["concept"] else bp["concept"]
        fq_act = fq_of(act)
        short = fq_act.rsplit(".", 1)[-1]
        where = f"{path}({short})"
        if fq_bp != fq_act:
            self.deviations.append(f"{where}: concept {fq_bp} expected, {fq_act} found")
            return
        # properties
        act_props = {p["name"]: p.get("value") for p in act.get("properties", [])}
        bp_props = {p["name"]: p.get("value") for p in bp.get("properties", [])}
        for name, value in bp_props.items():
            if value is None:
                continue
            if name not in act_props:
                if str(value) not in default_of(self.st, fq_act, name):
                    self.deviations.append(f"{where}.{name}: '{value}' expected, not stored")
            elif str(act_props[name]) != str(value):
                self.deviations.append(f"{where}.{name}: '{value}' expected, '{act_props[name]}' found")
        for name, value in act_props.items():
            if name not in bp_props:
                self.added.append(f"{where}.{name} = '{value}'")
        # references
        act_refs = {r["role"]: r for r in act.get("references", [])}
        bp_refs = {r["role"]: r.get("target") for r in bp.get("references", [])}
        for role, target in bp_refs.items():
            r = act_refs.get(role)
            if not r or not r.get("targetReference") or str(r.get("targetReference")).startswith("null"):
                self.deviations.append(f"{where}.{role}: reference to '{target}' is unresolved")
            elif target.startswith(("r:", "i:")) or "/" in target:
                if r["targetReference"] != target and not r["targetReference"].endswith(target):
                    self.deviations.append(f"{where}.{role}: '{target}' expected, '{r['targetReference']}' found")
            elif r.get("target") != target and r.get("target") != target.rsplit(".", 1)[-1]:
                self.deviations.append(f"{where}.{role}: '{target}' expected, '{r.get('target')}' found")
        for role, r in act_refs.items():
            if role not in bp_refs:
                self.added.append(f"{where}.{role} -> '{r.get('target')}'")
        # children
        act_kids = {c["role"]: c.get("nodes", []) for c in act.get("children", [])}
        bp_kids = {c["role"]: c.get("nodes", []) for c in bp.get("children", [])}
        for role, nodes in bp_kids.items():
            found = act_kids.get(role, [])
            if len(found) != len(nodes):
                self.deviations.append(f"{where}.{role}: {len(nodes)} child(ren) expected, {len(found)} found "
                                       f"({', '.join(fq_of(n).rsplit('.', 1)[-1] for n in found) or 'none'})")
                continue
            for i, (b, a) in enumerate(zip(nodes, found)):
                self.node(b, a, f"{where}.{role}[{i}]")
        for role, nodes in act_kids.items():
            if role not in bp_kids and nodes:
                self.added.append(f"{where}.{role}: {', '.join(fq_of(n).rsplit('.', 1)[-1] + (' ' + repr(n['name']) if n.get('name') and n['name'] != n.get('concept') else '') for n in nodes)}")


def main(argv):
    if len(argv) != 4 or argv[1] != "node":
        print(__doc__)
        return 2
    st = Structure()
    bp, act = load(argv[2]), load(argv[3])
    cmp = Comparison(st)
    cmp.node(bp, act, "$")
    for d in cmp.deviations:
        print("deviation:", d)
    for a in cmp.added:
        print("added:", a)
    print(f"{len(cmp.deviations)} deviation(s), {len(cmp.added)} added")
    return 1 if cmp.deviations else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
