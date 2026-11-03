"""Read printed nodes, build blueprint nodes. No knowledge of markers."""
import json

BL = "jetbrains.mps.baseLanguage.structure."
COL = "jetbrains.mps.baseLanguage.collections.structure."
CLO = "jetbrains.mps.baseLanguage.closures.structure."
OF = "org.modellwerkstatt.objectflow.structure."
MM = "org.modellwerkstatt.manmap.structure."
TXT = "jetbrains.mps.lang.text.structure."


class Stop(Exception):
    """The text cannot be converted; the message names the location."""


def fq(n):
    return n["conceptReference"].rsplit(":", 1)[1]


def node(concept, props=None, children=None, refs=None):
    """A blueprint node. A child value may be a node, a list or None (left out)."""
    d = {"concept": concept}
    if props:
        d["properties"] = [{"name": k, "value": str(v).lower() if isinstance(v, bool) else str(v)} for k, v in props.items()]
    ch = []
    for role, v in (children or {}).items():
        nodes = [x for x in (v if isinstance(v, list) else [v]) if x is not None]
        if nodes:
            ch.append({"role": role, "nodes": nodes})
    if ch:
        d["children"] = ch
    if refs:
        d["references"] = [{"role": r, "target": t} for r, t in refs.items()]
    return d


def kids(n, role):
    for c in n.get("children", []):
        if c["role"] == role:
            return c.get("nodes", [])
    return []


def kid(n, role):
    k = kids(n, role)
    return k[0] if k else None


def ref(n, role):
    for r in n.get("references", []):
        if r["role"] == role:
            return r
    return None


def unresolved(r):
    return r is not None and (not r.get("target") or str(r.get("targetReference")).startswith("null"))


def prop(n, name):
    for p in n.get("properties", []):
        if p["name"] == name:
            return p.get("value")
    return None


def walk(n):
    """Every node of a printed node or of a blueprint."""
    yield n
    for c in n.get("children", []):
        for x in c.get("nodes", []):
            yield from walk(x)


def short(n):
    return f"{n.get('name') or fq(n).rsplit('.', 1)[-1]} ({fq(n).rsplit('.', 1)[-1]}, {n.get('reference', '')})"


def load(path):
    """A printed root: the file of mps_mcp_print_node, with or without its envelope."""
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    if isinstance(d, dict) and "ok" in d and "data" in d:
        d = d["data"]
    return load(d) if isinstance(d, str) else d
