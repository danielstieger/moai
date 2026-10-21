#!/usr/bin/env python3
"""MoAI blueprint builder: look up concepts, build and check MPS JSON blueprints offline.

Works on the structure export in tools/data/structure (one file per language). Call with `python3 -I`.

  find TEXT...           Concepts whose name or alias contains every TEXT (case-insensitive).
  concept NAME           Roles of a concept: properties (type, enum values), references and children
                         (target, cardinality) and the concrete concepts that fit each child role.
  build SPEC [-o OUT]    Expand a short spec into a full blueprint and check it. Writes OUT
                         (default: a file in the system temp directory) and prints its path.
  check BLUEPRINT [--placeholders]
                         Check a full blueprint (or a top-level array of them). With --placeholders,
                         remaining TARGET_ placeholders are warnings (for checking templates).

Short spec (build):
  {"concept": "BusinessProperty",            short or fully qualified concept name
   "properties": {"name": "menge"},          values are written as strings
   "references": {"role": "TargetName"},      a name (resolved in scope by MPS) or an r:/i: reference
   "children": {"type": "IntegerType",        a node, a list of nodes, or [] for a named empty role
                "propertyOption": []}}        (an empty role suppresses node-factory content)
  A plain string stands for a node without properties, references and children.
  A node in full blueprint form (lists of properties/references/children) is taken as it is and checked.

Errors stop the build (exit code 1). Warnings (missing mandatory roles that a node factory may fill,
deprecated concepts or roles) are printed; check the inserted node afterwards.
"""
import sys

sys.dont_write_bytecode = True  # write nothing into the package (moai/ is a submodule in projects)

import json
import os
import re
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data", "structure")
FEATURE_ID = re.compile(r"^[0-9a-f]{8}-[0-9a-f-]{27}/\d+/\d+$")
SINGLE = ("0..1", "1")
MANDATORY = ("1", "1..n")


class Structure:
    def __init__(self, path=DATA):
        self.concepts = {}
        for name in sorted(os.listdir(path)):
            full = os.path.join(path, name)
            if name == "version.json":
                with open(full, encoding="utf-8") as f:
                    self.version = json.load(f)
            elif name.endswith(".json"):
                with open(full, encoding="utf-8") as f:
                    for c in json.load(f)["concepts"]:
                        self.concepts[c["name"]] = c
        self.by_short = {}
        for fq in self.concepts:
            self.by_short.setdefault(fq.rsplit(".", 1)[-1], []).append(fq)
        self._ancestors = {}

    def resolve(self, name):
        """Short or FQ concept name -> FQ name; raises ValueError with candidates."""
        if name in self.concepts:
            return name
        hits = self.by_short.get(name, [])
        if len(hits) == 1:
            return hits[0]
        if hits:
            raise ValueError(f"concept '{name}' is ambiguous: {', '.join(sorted(hits))}")
        raise ValueError(f"unknown concept '{name}'" + suggest(name, self.by_short))

    def ancestors(self, fq):
        """The concept itself, all super-concepts and all (transitive) interfaces."""
        if fq not in self._ancestors:
            seen, todo = set(), [fq]
            while todo:
                c = todo.pop()
                if c in seen or c not in self.concepts:
                    continue
                seen.add(c)
                d = self.concepts[c]
                todo += ([d["super"]] if d.get("super") else []) + d.get("interfaces", [])
            self._ancestors[fq] = seen
        return self._ancestors[fq]

    def fits(self, fq, target):
        return target in self.ancestors(fq)

    def concrete_for(self, target):
        return sorted(c for c, d in self.concepts.items()
                      if not d["abstract"] and not d["interface"] and not d.get("deprecated")
                      and self.fits(c, target))

    def role(self, fq, name):
        d = self.concepts[fq]
        hits = [(kind, f) for kind in ("properties", "references", "children")
                for f in d.get(kind, []) if f["name"] == name]
        hits.sort(key=lambda h: bool(h[1].get("deprecated")))  # a live duplicate wins over a deprecated one
        return hits[0] if hits else (None, None)


def suggest(name, by_short):
    low = name.lower()
    near = sorted(s for s in by_short if low in s.lower() or s.lower() in low)[:8]
    return f"; did you mean: {', '.join(near)}" if near else ""


def short(fq):
    return fq.rsplit(".", 1)[-1]


class Checker:
    def __init__(self, st, placeholders=False):
        self.st = st
        self.placeholders = placeholders
        self.errors, self.warnings = [], []

    def err(self, path, msg):
        self.errors.append(f"{path}: {msg}")

    def warn(self, path, msg):
        self.warnings.append(f"{path}: {msg}")

    def text(self, path, value):
        if isinstance(value, str) and "TARGET_" in value:
            (self.warn if self.placeholders else self.err)(path, f"unreplaced placeholder '{value}'")

    def node(self, bp, path, role_target=None):
        """Check one full blueprint node."""
        if not isinstance(bp, dict) or "concept" not in bp:
            self.err(path, "node needs a 'concept'")
            return
        try:
            fq = self.st.resolve(bp["concept"])
        except ValueError as e:
            self.err(path, str(e))
            return
        d = self.st.concepts[fq]
        where = f"{path}({short(fq)})"
        if d["abstract"] or d["interface"]:
            alts = self.st.concrete_for(fq)[:10]
            self.err(where, f"{'interface' if d['interface'] else 'abstract'} concept cannot be instantiated"
                     + (f"; concrete: {', '.join(short(a) for a in alts)}" if alts else ""))
        if d.get("deprecated"):
            self.warn(where, "deprecated concept")
        if role_target and not self.st.fits(fq, role_target):
            self.err(where, f"does not fit the role target {short(role_target)}")
        given = set()
        for p in bp.get("properties", []):
            name, value = p.get("name"), p.get("value")
            given.add(name)
            kind, f = self.st.role(fq, name)
            if kind != "properties":
                self.err(where, f"unknown property '{name}'")
                continue
            self.property(f"{where}.{name}", f, value)
        for r in bp.get("references", []):
            name, target = r.get("role"), r.get("target")
            given.add(name)
            kind, f = self.st.role(fq, name)
            if kind != "references":
                self.err(where, f"unknown reference role '{name}'")
                continue
            if f.get("deprecated"):
                self.warn(f"{where}.{name}", "deprecated role")
            self.reference(f"{where}.{name}", target)
        for ch in bp.get("children", []):
            name, nodes = ch.get("role"), ch.get("nodes", [])
            given.add(name)
            kind, f = self.st.role(fq, name)
            if kind != "children":
                self.err(where, f"unknown child role '{name}'")
                continue
            if f.get("deprecated"):
                self.warn(f"{where}.{name}", "deprecated role")
            if f["card"] in SINGLE and len(nodes) > 1:
                self.err(f"{where}.{name}", f"cardinality {f['card']} allows one child, got {len(nodes)}")
            for i, n in enumerate(nodes):
                self.node(n, f"{where}.{name}[{i}]", f["target"])
        for kind in ("references", "children"):
            for f in d.get(kind, []):
                if f["card"] in MANDATORY and f["name"] not in given:
                    self.warn(where, f"mandatory {kind[:-1] if kind == 'references' else 'child'} role "
                              f"'{f['name']}' not given (a node factory may fill it; check after insert)")

    def property(self, path, f, value):
        if value is None:
            return
        value = str(value)
        self.text(path, value)
        if f.get("enum"):
            if value not in f["enum"]:
                self.err(path, f"'{value}' is not one of {', '.join(f['enum'])}")
        elif f["type"] == "boolean" and value not in ("true", "false"):
            self.err(path, f"boolean expected, got '{value}'")
        elif f["type"] == "integer" and not re.fullmatch(r"-?\d+", value):
            self.err(path, f"integer expected, got '{value}'")
        if f.get("deprecated"):
            self.warn(path, "deprecated property")

    def reference(self, path, target):
        if not isinstance(target, str) or not target:
            self.err(path, "reference target must be a non-empty string")
            return
        self.text(path, target)
        if target.startswith("c:"):
            self.err(path, "a c: concept reference is not a node reference; use the declaration's r: ref (sourceNode)")
        elif FEATURE_ID.match(target):
            self.err(path, "a featureId is not a node reference; use the feature's sourceNode")


def expand(st, spec, path="$"):
    """Short spec -> full blueprint (unchecked; check() does the checking)."""
    if isinstance(spec, str):
        spec = {"concept": spec}
    if not isinstance(spec, dict) or "concept" not in spec:
        raise ValueError(f"{path}: node needs a 'concept'")
    if any(isinstance(spec.get(k), list) for k in ("properties", "references", "children")):
        return spec  # already a full blueprint node (e.g. from copyroot.py); check() validates it
    try:
        fq = st.resolve(spec["concept"])
    except ValueError as e:
        raise ValueError(f"{path}: {e}")
    out = {"concept": fq}
    unknown = set(spec) - {"concept", "properties", "references", "children"}
    if unknown:
        raise ValueError(f"{path}: unknown key(s) {', '.join(sorted(unknown))}")
    props = spec.get("properties", {})
    if props:
        out["properties"] = [{"name": k, "value": v if isinstance(v, str) else json.dumps(v)}
                             for k, v in props.items()]
    refs = spec.get("references", {})
    if refs:
        out["references"] = [{"role": k, "target": v} for k, v in refs.items()]
    kids = spec.get("children", {})
    if kids:
        out["children"] = []
        for role, nodes in kids.items():
            nodes = nodes if isinstance(nodes, list) else [nodes]
            out["children"].append({"role": role, "nodes": [
                expand(st, n, f"{path}.{short(fq)}.{role}[{i}]") for i, n in enumerate(nodes)]})
    return out


def report(chk):
    for w in chk.warnings:
        print("warning:", w, file=sys.stderr)
    for e in chk.errors:
        print("error:", e, file=sys.stderr)
    return 1 if chk.errors else 0


def cmd_check(st, path, placeholders=False):
    with open(path, encoding="utf-8") as f:
        bp = json.load(f)
    if isinstance(bp, dict) and "data" in bp and "ok" in bp:
        bp = bp["data"]
    chk = Checker(st, placeholders)
    for i, n in enumerate(bp if isinstance(bp, list) else [bp]):
        chk.node(n, f"$[{i}]" if isinstance(bp, list) else "$")
    rc = report(chk)
    print(f"{path}: {len(chk.errors)} error(s), {len(chk.warnings)} warning(s)")
    return rc


def cmd_build(st, spec_path, out=None):
    with open(spec_path, encoding="utf-8") as f:
        spec = json.load(f)
    try:
        bp = [expand(st, s, f"$[{i}]") for i, s in enumerate(spec)] if isinstance(spec, list) else expand(st, spec)
    except ValueError as e:
        print("error:", e, file=sys.stderr)
        return 1
    chk = Checker(st)
    for i, n in enumerate(bp if isinstance(bp, list) else [bp]):
        chk.node(n, f"$[{i}]" if isinstance(bp, list) else "$")
    rc = report(chk)
    if rc:
        return rc
    text = json.dumps(bp, ensure_ascii=False, separators=(",", ":"))
    if out is None:
        fd, out = tempfile.mkstemp(prefix="moai-bp-", suffix=".json")
        os.close(fd)
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)
    print(out)
    print(f"{len(text.encode('utf-8'))} bytes ({'inline ok' if len(text.encode('utf-8')) <= 4096 else 'pass the file path'})",
          file=sys.stderr)
    return 0


def cmd_find(st, words):
    words = [w.lower() for w in words]
    hits = [fq for fq, d in st.concepts.items()
            if all(w in fq.rsplit(".", 1)[-1].lower() or w in d.get("alias", "").lower() for w in words)]
    for fq in sorted(hits):
        d = st.concepts[fq]
        flags = [x for x in ("abstract", "interface", "rootable", "deprecated") if d.get(x)]
        alias = f"  alias '{d['alias']}'" if d.get("alias") else ""
        print(f"{fq}{alias}{'  [' + ', '.join(flags) + ']' if flags else ''}")
    if not hits:
        print("no match")


def cmd_concept(st, name):
    fq = st.resolve(name)
    d = st.concepts[fq]
    flags = [x for x in ("abstract", "interface", "rootable", "deprecated") if d.get(x)]
    print(f"{fq}" + (f"  alias '{d['alias']}'" if d.get("alias") else "") + (f"  [{', '.join(flags)}]" if flags else ""))
    if d.get("super"):
        print(f"  super: {d['super']}")
    if d.get("interfaces"):
        print(f"  interfaces: {', '.join(short(i) for i in d['interfaces'])}")
    skip = {"shortDescription", "virtualPackage", "smodelAttribute"}
    live = {f["name"] for f in d.get("properties", []) if not f.get("deprecated")}
    for f in d.get("properties", []):
        if f["name"] in skip or (f.get("deprecated") and f["name"] in live):
            continue
        extra = f"  one of {', '.join(f['enum'])}" + (f" (default {f['default']})" if f.get("default") else "") if f.get("enum") else ""
        print(f"  property  {f['name']}: {f['type']}{extra}{'  [deprecated]' if f.get('deprecated') else ''}")
    for f in d.get("references", []):
        print(f"  reference {f['name']} [{f['card']}] -> {f['target']}{'  [deprecated]' if f.get('deprecated') else ''}")
    for f in d.get("children", []):
        if f["name"] in skip:
            continue
        fits = st.concrete_for(f["target"])
        shown = ", ".join(short(c) for c in fits[:12]) + (f", … ({len(fits)})" if len(fits) > 12 else "")
        print(f"  child     {f['name']} [{f['card']}] {short(f['target'])}: {shown or '-'}"
              f"{'  [deprecated]' if f.get('deprecated') else ''}")


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    st = Structure()
    cmd, args = argv[1], argv[2:]
    try:
        if cmd == "find" and args:
            cmd_find(st, args)
        elif cmd == "concept" and len(args) == 1:
            cmd_concept(st, args[0])
        elif cmd == "check" and args and len([a for a in args if a != "--placeholders"]) == 1:
            return cmd_check(st, [a for a in args if a != "--placeholders"][0], "--placeholders" in args)
        elif cmd == "build" and args:
            out = args[args.index("-o") + 1] if "-o" in args else None
            return cmd_build(st, args[0], out)
        else:
            print(__doc__)
            return 2
    except ValueError as e:
        print("error:", e, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
