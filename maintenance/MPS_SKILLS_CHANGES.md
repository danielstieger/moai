# Changes to the JetBrains MPS Skills

For MoAI maintainers. Agents working in an application project do not need this file.

The `mps-*` skills in `skills/` derive from the generic MPS skills JetBrains ships with the MPS MCP
(`mps_mcp_initialize_project_for_agents`). MoAI adapts them. When JetBrains releases a new version,
this list says which MoAI changes to carry over and why.

Changes before 2026-10-21 are not recorded here; compare against the JetBrains originals of
MPS 2026.2 for them.

| Date | Skill / file | Change | Reason |
| --- | --- | --- | --- |
| 2026-10-21 | `mps-node-editing/SKILL.md` (Critical Directives) | New rule "Set references by name": persistent refs only for stubs, overloads, ambiguous targets in other models and long property chains over foreign entities; repair order `stillBroken` → `FIX_REFERENCES` → quick-fixes; harvest only as last resort. | Harvesting refs with `print_node` was the default and cost many calls; refs harvested before a `SET CHILD` are dead afterwards. Resolution by name worked better in practice (runs 3 and 4). |
| 2026-10-21 | `mps-node-editing/SKILL.md` (Critical Directives) | New rule "Replace referenced members through their body": constructors and test methods only via `body`; methods that call each other are replaced together. | `SET CHILD` assigns new IDs and breaks persistent refs to the replaced member. |
| 2026-10-21 | `mps-node-editing/SKILL.md` (Node factories) | New point: factories may add model imports without the module dependency; check and add it. | Observed: a model import of `manmap.runtime` without the module dependency. |
| 2026-10-21 | `mps-node-editing/references/staged-construction.md` | Step "Harvest refs" renamed to "Read child refs" (refs for the following `ADD`/`SET CHILD` calls); references between nodes by name. | Consistency with the reference rule. |
| 2026-10-21 | `mps-baselanguage/SKILL.md`, `references/json-ast-workflow.md`, `critical-rules.md`, `troubleshooting.md`, `stub-references.md` | Harvesting replaced by the reference rule of `mps-node-editing`; former steps "Auto-resolution" and "Repair" merged into "References". | The skills contradicted each other (harvest vs. names); one rule in one place. |
