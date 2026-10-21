#!/usr/bin/env python3
"""MoAI additions to mps_dump.py: read check reports, blueprints and dumps in a few lines.

mps_dump.py (skills/mps-mcp-workflow/scripts) stays the JetBrains tool for roots, models, node, tree,
shape and count; this script adds what MoAI work needs on top of it. Call with `python3 -I`.

  problems FILE            One line per problem of a `mps_mcp_check_root_node_problems` report (model,
                           module or node form, flat or full tree): severity, root, node, feature,
                           message, reporting rule, quick-fix ids. Then a count per message.
  bp FILE [--depth N]      A blueprint (full form, single or array) as an indented tree.
  grep FILE [--concept C] [--name N] [--ref TEXT] [--unresolved]
                           Nodes of a print_node / get_project_structure dump at any depth: by concept
                           (short or FQ), by name, by a reference target containing TEXT; --unresolved
                           lists references that do not resolve.

Output is plain text on stdout; exit code 0, 2 for usage, 3 for unreadable input.
"""
import sys

sys.dont_write_bytecode = True  # write nothing into the package (moai/ is a submodule in projects)

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "skills", "mps-mcp-workflow", "scripts"))
import mps_dump  # noqa: E402


def short(concept):
    return (concept or "?").rsplit(":", 1)[-1].rsplit(".", 1)[-1]


def label(node):
    name = node.get("name")
    c = short(node.get("conceptReference") or node.get("concept"))
    return f"{name} ({c})" if name and name != c else c


# --- problems -------------------------------------------------------------------------------

def walk_report(obj, root, path, out):
    """Collect problems from any check-report shape."""
    if isinstance(obj, list):
        for x in obj:
            walk_report(x, root, path, out)
        return
    if not isinstance(obj, dict):
        return
    if "root" in obj and "name" in obj:  # one root entry of a model report
        root = obj["name"]
        path = []
    is_node = "concept" in obj and ("reference" in obj or "conceptReference" in obj)
    here = path + [label(obj)] if is_node and obj.get("name") != root else path
    for p in obj.get("problems", []) or []:
        out.append((root, here, None, p))
    for kind in ("properties", "references", "children"):
        for f in obj.get(kind, []) or []:
            if not isinstance(f, dict):
                continue
            feature = f.get("name") or f.get("role")
            for p in f.get("problems", []) or []:
                out.append((root, here, feature, p))
            if kind == "children":
                walk_report(f.get("nodes", []), root, here, out)
    for key in ("roots", "nodes", "models", "tree"):
        walk_report(obj.get(key, []), root, path if key != "nodes" else here, out)


def cmd_problems(path):
    data = mps_dump.load(path)
    if data == "no problems found" or (isinstance(data, str) and data.startswith("no problems found")):
        print(data)
        return 0
    found = []
    walk_report(data, None, [], found)
    counts = {}
    for root, here, feature, p in found:
        msg = p.get("message", "").replace("\n", " ")
        rule = (p.get("rules") or [{}])[0].get("rule")
        fixes = [q.get("id") for q in p.get("quickFixes", []) or []]
        where = " > ".join(here) + (f".{feature}" if feature else "")
        print(f"{p.get('severity', '?'):7} {root or '-'} | {where or '(root)'}: {msg}"
              + (f"  [rule {rule}]" if rule else "") + (f"  [fix {', '.join(fixes)}]" if fixes else ""))
        key = (p.get("severity", "?"), re.sub(r"\b(?:r:\S+|\d{6,})", "…", msg))
        counts[key] = counts.get(key, 0) + 1
    print(f"-- {len(found)} problem(s)")
    for (sev, msg), n in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"{n:4}  {sev:7} {msg}")
    return 0


# --- bp -------------------------------------------------------------------------------------

def bp_lines(node, role, level, depth, lines):
    if depth is not None and level > depth:
        return
    props = " ".join(f"{p['name']}={p.get('value')!r}" for p in node.get("properties", []))
    refs = " ".join(f"{r['role']}->{r.get('target')}" for r in node.get("references", []))
    lines.append("  " * level + (f"{role}: " if role else "") + short(node.get("concept"))
                 + (f"  {props}" if props else "") + (f"  {refs}" if refs else ""))
    for ch in node.get("children", []):
        nodes = ch.get("nodes", [])
        if not nodes:
            lines.append("  " * (level + 1) + f"{ch['role']}: (empty)")
        for n in nodes:
            bp_lines(n, ch["role"], level + 1, depth, lines)


def cmd_bp(path, depth):
    data = mps_dump.load(path)
    lines = []
    for n in data if isinstance(data, list) else [data]:
        bp_lines(n, None, 0, depth, lines)
    print("\n".join(lines))
    size = len(json.dumps(data, separators=(",", ":")).encode("utf-8"))
    print(f"-- {len(lines)} node(s), {size} bytes minified")
    return 0


# --- grep -----------------------------------------------------------------------------------

def walk_nodes(obj, path, out):
    if isinstance(obj, list):
        for x in obj:
            walk_nodes(x, path, out)
        return
    if not isinstance(obj, dict):
        return
    is_node = "concept" in obj and ("reference" in obj or "conceptReference" in obj)
    here = path + [label(obj)] if is_node else path
    if is_node:
        out.append((here, obj))
    for ch in obj.get("children", []) or []:
        if isinstance(ch, dict):
            walk_nodes(ch.get("nodes", []) or ch.get("children", []), here, out)
    for key in ("modules", "models", "rootNodes", "roots", "nodes"):
        walk_nodes(obj.get(key, []), here, out)


def cmd_grep(path, concept, name, ref, unresolved):
    data = mps_dump.load(path)
    nodes = []
    walk_nodes(data, [], nodes)
    hits = 0
    for here, n in nodes:
        c = n.get("conceptReference") or n.get("concept") or ""
        if concept and short(c) != short(concept) and not c.endswith(":" + concept):
            continue
        if name and n.get("name") != name:
            continue
        refs = n.get("references", []) or []
        if ref:
            refs = [r for r in refs if ref in str(r.get("target")) or ref in str(r.get("targetReference"))]
            if not refs:
                continue
        if unresolved:
            refs = [r for r in refs if not r.get("targetReference") or str(r["targetReference"]).startswith("null")]
            if not refs:
                continue
        hits += 1
        detail = " ".join(f"{r.get('role')}->{r.get('target')}" for r in refs) if (ref or unresolved) else ""
        print(" > ".join(here) + f"  {n.get('reference', '')}" + (f"  {detail}" if detail else ""))
    print(f"-- {hits} node(s)")
    return 0


def main(argv):
    if len(argv) < 3 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 2
    cmd, path, rest = argv[1], argv[2], argv[3:]

    def opt(flag):
        return rest[rest.index(flag) + 1] if flag in rest else None
    try:
        if cmd == "problems":
            return cmd_problems(path)
        if cmd == "bp":
            return cmd_bp(path, int(opt("--depth")) if opt("--depth") else None)
        if cmd == "grep":
            return cmd_grep(path, opt("--concept"), opt("--name"), opt("--ref"), "--unresolved" in rest)
    except (OSError, ValueError, SystemExit) as e:
        print(f"cannot read {path}: {e}", file=sys.stderr)
        return 3
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
