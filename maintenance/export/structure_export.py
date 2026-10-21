#!/usr/bin/env python3
"""Normalize and compare the MoAI structure export.

The raw input is the result of `mps_mcp_get_concept_details` with `languageRefs` and `detail: "full"`
(the temp file the tool returns, envelope or plain list). This script only reads and writes files;
the MCP calls are made by the maintainer's agent (see maintenance/RELEASE.md).

  normalize OUTDIR RAW.json [RAW.json ...] --mps-build BUILD
      Writes OUTDIR/<language>.json (one file per language, stably sorted) and OUTDIR/version.json,
      then lists the languages that are referenced (super-concepts, super-interfaces, role targets)
      but not yet exported. Export those too and run normalize again until none is missing.

  missing OUTDIR
      Lists referenced but not exported languages only.

  diff OLDDIR NEWDIR
      Reports new, removed and changed concepts and roles between two exports.

Standard library only; call with `python3 -I`.
"""
import json
import os
import sys


def fq(ref):
    """'c:<uuid>/<id>:<fq.Name>' or 'i:…' -> 'fq.Name'; a plain FQ name stays as it is."""
    if not ref:
        return None
    return ref.rsplit(":", 1)[-1] if ref[:2] in ("c:", "i:") else ref


def language_of(concept_fq):
    """'org.x.lang.structure.Concept' -> 'org.x.lang'."""
    head, _, _ = concept_fq.rpartition(".")
    return head[: -len(".structure")] if head.endswith(".structure") else head


def is_deprecated(value):
    return isinstance(value, str) and value.startswith("true")


def load_raw(path):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict):
        data = data.get("data", data)
    if isinstance(data, str):  # envelope pointing to another file
        return load_raw(data)
    if not isinstance(data, list):
        sys.exit(f"{path}: expected a list of concepts")
    return data


def feature(entry, kind):
    out = {"name": entry["name"]}
    if kind == "properties":
        out["type"] = entry.get("type")
        if entry.get("enumerationValues"):
            out["enum"] = entry["enumerationValues"]
        if entry.get("enumerationDefault"):
            out["default"] = entry["enumerationDefault"]
    else:
        out["target"] = entry.get("targetConcept")
        out["card"] = entry.get("cardinality")
    if is_deprecated(entry.get("deprecated")):
        out["deprecated"] = True
    return out


def concept(c):
    if c.get("descriptorStatus"):
        sys.exit(f"{c.get('qualifiedName')}: descriptor is {c['descriptorStatus']} - broken installation, stop")
    out = {
        "name": c["qualifiedName"],
        "abstract": bool(c.get("isAbstract")),
        "interface": bool(c.get("isInterfaceConcept")),
        "rootable": bool(c.get("isRootable")),
    }
    if c.get("conceptAlias"):
        out["alias"] = c["conceptAlias"]
    if c.get("superConcept"):
        out["super"] = fq(c["superConcept"])
    if c.get("superInterfaces"):
        out["interfaces"] = sorted(fq(i) for i in c["superInterfaces"])
    if is_deprecated(c.get("deprecated")):
        out["deprecated"] = True
    for kind in ("properties", "references", "children"):
        items = [feature(e, kind) for e in c.get(kind, [])]
        if items:
            out[kind] = sorted(items, key=lambda x: x["name"])
    return out


def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, sort_keys=True, ensure_ascii=False)
        f.write("\n")


def read_dir(outdir):
    langs = {}
    for name in sorted(os.listdir(outdir)):
        if name.endswith(".json") and name != "version.json":
            with open(os.path.join(outdir, name), encoding="utf-8") as f:
                lang = json.load(f)
            langs[lang["language"]] = lang
    return langs


def missing(outdir):
    langs = read_dir(outdir)
    known = {c["name"] for l in langs.values() for c in l["concepts"]}
    needed = {}
    for l in langs.values():
        for c in l["concepts"]:
            refs = [c.get("super")] + c.get("interfaces", [])
            for kind in ("references", "children"):
                refs += [f["target"] for f in c.get(kind, [])]
            for r in refs:
                if r and r not in known:
                    needed.setdefault(language_of(r), set()).add(r)
    return needed


def cmd_normalize(args):
    if "--mps-build" not in args:
        sys.exit("normalize needs --mps-build BUILD")
    i = args.index("--mps-build")
    build = args[i + 1]
    args = args[:i] + args[i + 2:]
    outdir, raws = args[0], args[1:]
    os.makedirs(outdir, exist_ok=True)
    by_lang = {}
    for raw in raws:
        for c in load_raw(raw):
            lang = c.get("languageReference", "").rsplit(":", 1)[-1] or language_of(c["qualifiedName"])
            by_lang.setdefault(lang, {})[c["qualifiedName"]] = concept(c)
    for lang, concepts in by_lang.items():
        write_json(os.path.join(outdir, lang + ".json"),
                   {"language": lang, "concepts": [concepts[k] for k in sorted(concepts)]})
        print(f"{lang}: {len(concepts)} concepts")
    langs = read_dir(outdir)
    write_json(os.path.join(outdir, "version.json"),
               {"mpsBuild": build, "languages": {k: len(v["concepts"]) for k, v in langs.items()}})
    report_missing(outdir)


def report_missing(outdir):
    needed = missing(outdir)
    if not needed:
        print("closed: every referenced concept is exported")
        return
    print("missing languages (export them, then normalize again):")
    for lang in sorted(needed):
        print(f"  {lang}  ({len(needed[lang])} concepts, e.g. {sorted(needed[lang])[0]})")


def cmd_diff(old, new):
    a, b = read_dir(old), read_dir(new)
    ca = {c["name"]: c for l in a.values() for c in l["concepts"]}
    cb = {c["name"]: c for l in b.values() for c in l["concepts"]}
    changes = 0
    for lang in sorted(set(a) | set(b)):
        if lang not in a:
            print(f"+ language {lang}")
        elif lang not in b:
            print(f"- language {lang}")
    for name in sorted(set(ca) - set(cb)):
        print(f"- concept {name}"); changes += 1
    for name in sorted(set(cb) - set(ca)):
        print(f"+ concept {name}"); changes += 1
    for name in sorted(set(ca) & set(cb)):
        x, y = ca[name], cb[name]
        for key in ("abstract", "interface", "rootable", "super", "interfaces", "deprecated"):
            if x.get(key) != y.get(key):
                print(f"~ {name}: {key} {x.get(key)} -> {y.get(key)}"); changes += 1
        for kind in ("properties", "references", "children"):
            fx = {f["name"]: f for f in x.get(kind, [])}
            fy = {f["name"]: f for f in y.get(kind, [])}
            for f in sorted(set(fx) - set(fy)):
                print(f"- {name}.{kind}.{f}"); changes += 1
            for f in sorted(set(fy) - set(fx)):
                print(f"+ {name}.{kind}.{f} {json.dumps(fy[f], sort_keys=True)}"); changes += 1
            for f in sorted(set(fx) & set(fy)):
                if fx[f] != fy[f]:
                    print(f"~ {name}.{kind}.{f} {json.dumps(fx[f], sort_keys=True)} -> {json.dumps(fy[f], sort_keys=True)}")
                    changes += 1
    print(f"{changes} change(s)")


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__); return
    cmd, args = argv[1], argv[2:]
    if cmd == "normalize" and len(args) >= 4:
        cmd_normalize(args)
    elif cmd == "missing" and len(args) == 1:
        report_missing(args[0])
    elif cmd == "diff" and len(args) == 2:
        cmd_diff(*args)
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
