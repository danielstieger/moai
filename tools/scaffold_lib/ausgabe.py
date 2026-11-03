"""Write the blueprints, the Java files and the plan; every root is checked against the structure here."""
import json
import os
import tempfile

from blueprint import Checker, expand, report


def write(st, result, out_dir):
    out_dir = os.path.abspath(out_dir or tempfile.mkdtemp(prefix="moai-scaffold-"))
    os.makedirs(out_dir, exist_ok=True)
    chk = Checker(st)
    files = []
    for i, (kind, spec, *into) in enumerate(result.roots, 1):
        bp = expand(st, spec, f"{kind}")
        chk.node(bp, kind)
        path = os.path.join(out_dir, f"{i:02d}-{kind}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(bp, f, ensure_ascii=False, separators=(",", ":"))
        files.append((into[0] if into else None, next((x["value"] for x in bp.get("properties", []) if x["name"] == "name"), kind), path))
    if report(chk):
        return 1
    jlines = []
    for stem, text, how in result.java:
        if not stem:
            jlines.append(f"  {how}")
            continue
        path = os.path.join(out_dir, f"{stem}.java")
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        jlines.append(f"  {path}: {how}")
    plan = [f"Model {result.model} (create it if missing, DevKit org.modellwerkstatt.MoWareWerkbank).",
            "Insert the roots in this order (mps_mcp_insert_root_node_from_json, json = file path),",
            "check fixReferences.stillBroken = 0 after each:"]
    plan += [f"  {name}: {path}" if into is None else
             f"  {name}: {path} (replace the existing root: mps_mcp_update_root_node_from_json)" if into == "=replace" else
             f"  {name}: {path} (ADD CHILD into the existing {into}, role persistenceMapping)" for into, name, path in files]
    if jlines:
        plan.append("Write the method bodies (moai:objectflow-dsl, workflows.md, \"Write method bodies and command functions\"):")
        plan.append("  Selectors (init, ok, page:NAME:init, page:NAME:conc:N, ...): text2of.py ROOTDUMP --bodies gives owner and role.")
        plan += jlines
        plan.append("After the last SET CHILD of a root: FIX_REFERENCES on that root.")
    plan += result.notes
    plan.append("Check the model (mps_mcp_check_root_node_problems, model reference, perRoot=true).")
    text = "\n".join(plan) + "\n"
    with open(os.path.join(out_dir, "plan.txt"), "w", encoding="utf-8") as f:
        f.write(text)
    print(text, end="")
    return 0
