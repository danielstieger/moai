#!/usr/bin/env python3
"""MoAI root copy: turn roots of another model into one insertable blueprint.

The MPS MCP copies only within one model (`COPY_NODE`). This tool takes `mps_mcp_print_node` dumps
(deep=true) of one or more roots, typically templates in a library model, and writes a blueprint
that `mps_mcp_insert_root_node_from_json` inserts into the target model. Call with `python3 -I`.

  copyroot.py DUMP [DUMP ...] [-o OUT] [--replace OLD=NEW]... [--drop NAME]... [--keep-defaults]

  --replace OLD=NEW   replace text in every property value (e.g. firma.app=org.firma.fuhrpark);
                      applies to root names and reference names as well
  --drop NAME         leave out every node with this name (e.g. a config section you do not need)
  --keep-defaults     keep properties printed with "isDefault": true (left out by default)

References:
  - into one of the copied nodes: written as the target's name, so it resolves in the target model;
  - to another model or a stub: kept as the persistent reference; the target model must import that model;
  - into the source model but outside the copy: reported, because it will not resolve.
The result is checked with blueprint.py; the tool prints the output path and its report.
"""
import sys

sys.dont_write_bytecode = True  # write nothing into the package (moai/ is a submodule in projects)

import json
import os
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from blueprint import Checker, Structure, report  # noqa: E402


def load(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "ok" in data and "data" in data:
        data = data["data"]
    if isinstance(data, str):
        return load(data)
    return data


def model_of(ref):
    return ref.split("/", 1)[0] if isinstance(ref, str) and ref.startswith("r:") else None


def fq_of(node):
    ref = node.get("conceptReference", "")
    return ref.rsplit(":", 1)[-1] if ref else node["concept"]


class Copier:
    def __init__(self, replace, drop, keep_defaults):
        self.replace, self.drop, self.keep_defaults = replace, set(drop), keep_defaults
        self.copied = {}       # node reference -> name, for every copied node
        self.outside, self.foreign, self.dropped = [], {}, []

    def text(self, value):
        for old, new in self.replace:
            value = value.replace(old, new)
        return value

    def collect(self, node):
        if node.get("name") in self.drop:
            return
        if node.get("reference"):
            self.copied[node["reference"]] = node.get("name")
        for ch in node.get("children", []):
            for n in ch.get("nodes", []):
                self.collect(n)

    def node(self, node, source_models, path):
        if node.get("conceptLoaded") is False:
            raise ValueError(f"{path}: concept of '{node.get('name')}' is not loaded; cannot copy")
        out = {"concept": fq_of(node)}
        props = []
        for p in node.get("properties", []):
            if p.get("declared") is False or (p.get("isDefault") and not self.keep_defaults):
                continue
            if p.get("value") is not None:
                props.append({"name": p["name"], "value": self.text(str(p["value"]))})
        if props:
            out["properties"] = props
        refs = []
        for r in node.get("references", []):
            if r.get("declared") is False:
                continue
            tref = r.get("targetReference")
            where = f"{path}.{r['role']}"
            if not tref or str(tref).startswith("null"):
                self.outside.append(f"{where}: unresolved already in the source ('{r.get('target')}')")
                continue
            if tref in self.copied:
                refs.append({"role": r["role"], "target": self.text(str(self.copied[tref] or r.get("target")))})
            elif model_of(tref) in source_models:
                self.outside.append(f"{where}: points to '{r.get('target')}' in the source model, which is not copied")
                refs.append({"role": r["role"], "target": self.text(str(r.get("target")))})
            else:
                refs.append({"role": r["role"], "target": tref})
                m = model_of(tref) or tref.split("/", 1)[0]
                self.foreign[m] = self.foreign.get(m, 0) + 1
        if refs:
            out["references"] = refs
        kids = []
        for ch in node.get("children", []):
            if ch.get("declared") is False:
                continue
            nodes = []
            for i, n in enumerate(ch.get("nodes", [])):
                if n.get("name") in self.drop:
                    self.dropped.append(f"{path}.{ch['role']}: {n.get('name')}")
                    continue
                nodes.append(self.node(n, source_models, f"{path}.{ch['role']}[{i}]"))
            if nodes:
                kids.append({"role": ch["role"], "nodes": nodes})
        if kids:
            out["children"] = kids
        return out


def main(argv):
    args, dumps, replace, drop, out, keep = argv[1:], [], [], [], None, False
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("-h", "--help"):
            print(__doc__)
            return 0
        if a == "-o":
            out, i = args[i + 1], i + 2
        elif a == "--replace":
            old, _, new = args[i + 1].partition("=")
            replace.append((old, new))
            i += 2
        elif a == "--drop":
            drop.append(args[i + 1])
            i += 2
        elif a == "--keep-defaults":
            keep, i = True, i + 1
        else:
            dumps.append(a)
            i += 1
    if not dumps:
        print(__doc__)
        return 2
    roots = [load(p) for p in dumps]
    cp = Copier(replace, drop, keep)
    for r in roots:
        cp.collect(r)
    source_models = {model_of(r.get("reference")) for r in roots}
    try:
        bp = [cp.node(r, source_models, f"$[{i}]({r.get('name')})") for i, r in enumerate(roots)]
    except ValueError as e:
        print("error:", e, file=sys.stderr)
        return 1
    bp = bp if len(bp) > 1 else bp[0]
    chk = Checker(Structure())
    for i, n in enumerate(bp if isinstance(bp, list) else [bp]):
        chk.node(n, f"$[{i}]" if isinstance(bp, list) else "$")
    rc = report(chk)
    for d in cp.dropped:
        print("dropped:", d, file=sys.stderr)
    for o in cp.outside:
        print("will not resolve:", o, file=sys.stderr)
    for m, n in sorted(cp.foreign.items()):
        print(f"import needed: {m} ({n} reference(s))", file=sys.stderr)
    text = json.dumps(bp, ensure_ascii=False, separators=(",", ":"))
    if out is None:
        fd, out = tempfile.mkstemp(prefix="moai-copy-", suffix=".json")
        os.close(fd)
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)
    print(out)
    print(f"{len(text.encode('utf-8'))} bytes ({'inline ok' if len(text.encode('utf-8')) <= 4096 else 'pass the file path'})",
          file=sys.stderr)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
