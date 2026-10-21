---
name: manmap-dsl
description: "Use when creating, editing, validating, or inspecting MoWare ManMap persistence (org.modellwerkstatt.manmap): table and column mappings, keys and auto IDs, repositories, loading queries (get/where, joins), checkout, saving and deleting object graphs, custom SQL and read models."
---

# ManMap DSL

ManMap models relational persistence and read models for MoWare applications. `PersistenceDescription` maps ObjectFlow entities and value objects to tables and columns; `Repository` contains mapped queries, explicit save/delete operations, reusable row mappers, no-key read-only mappers, and direct SQL. Loading, graph persistence, session identity, and transaction boundaries are explicit rather than implicit.

## Critical Rules

- Use MPS MCP tools; never read or edit raw `.mps` / `.mpl` XML (rule and fallback: [`MPS_AGENT_GUIDE.md`](../../MPS_AGENT_GUIDE.md#never-read-raw-mps-model-files)).
- Never persist a project path or IDE-session state.
- Conventions are referenced by name, e.g. conventions `anwendungsaufbau` (file `mw-anwendungsaufbau_v1.md`); the project's `AGENTS.md` states where they are and which ones it changes. This skill does not repeat their content.
- Database schemas: conventions `allgemein`.
- Discover the language by its qualified name `org.modellwerkstatt.manmap`. Query concepts with `l:5aaa957f-3447-4783-b1f7-b301fa3e0394:org.modellwerkstatt.manmap` or the plain language name in `languageRefs`, not the module reference syntax; one `languageRefs` call with `detail="shape"` covers all concepts. Enum literals (`sqlType`, `repoMethodType`): `mps_mcp_query_structure` `GET_ENUMERATION_LITERALS`.
- Use the `qualifiedName` as `concept` in blueprints (`moai:mps-mcp-workflow`, `references/node-editing-rules.md`).
- Treat every `$TARGET_*` value in a blueprint as a required target-model placeholder. Resolve it by scope or replace it with a persistent `r:` node reference from the target model immediately before insertion. The dry-run does not reliably report a forgotten placeholder: search the blueprint text for `TARGET_` before every write and stop on any match.
- Never copy persistent references from an application example into another model. The stable references in [sandbox.md](references/sandbox.md) are read-only navigation and verification anchors, not insertion values.
- Prefer skeleton-plus-subtree construction for persistence descriptions and repositories. Preserve existing node IDs with surgical updates.
- No lazy loading, no cascading save/delete; references and lists are loaded explicitly (separate queries or `refJoin`/`listJoin`): see [Explizites Laden](../../docu/manmap.md#explizites-laden) and [Referenzen, eingebettete Werte und Listen](../../docu/manmap.md#referenzen-eingebettete-werte-und-listen).
- In a blueprint, set `MappingReference.mappingSource` to the name of the query's `EntityMapping`; it resolves to the enclosing query even within the same blueprint. See [mapped query workflow](references/workflows.md#build-a-mapped-query).
- New `QueryFromMap` nodes default to `readOnly = true`. Set `readOnly = false` deliberately for queries that check out data for editing.
- After every real write, `fixReferences.stillBroken` must be 0. Validate with `mps_mcp_check_root_node_problems`: the single changed root, or after work on several roots the model reference with `perRoot=true`. Evaluate `warnings`, `details.uncheckedSubtrees`, `rules[].statement` and `quickFixes`; then run task-required generation or build checks.
- Node factories run on insert and fill roles the blueprint omits; a named role, even `{"role":"…","nodes":[]}`, replaces the factory's content. See [Node factories](references/gotchas.md#node-factories).
- Load `moai:mps-baselanguage` and `moai:mps-node-editing` before constructing repository methods or expression/statement subtrees.

## Unknown construct

Do not infer a shape from dumps, and do not write your own tools for it. Follow this order:

1. Find the projection in the documentation's [chapter map (Kapitellandkarte)](../../docu/manmap.md), or search name and alias offline with `python3 -I moai/tools/blueprint.py find <text>`; both give the concept and its FQ name.
2. Read roles, cardinalities, enum values and the concrete concepts that fit each child role offline with `blueprint.py concept <Name>`. Use `mps_mcp_get_concept_details` only for a concept the tool does not know.
3. Find a real instance in the packaged examples ([sandbox.md](references/sandbox.md)): `mps_mcp_query_nodes` `FIND_INSTANCES` with `scope:"models"` and `sampleOnly:true`.
4. Print it and read large results with `mps_dump.py` (`moai:mps-mcp-workflow`, Scripts) instead of opening the file; search a dump by concept, name or unresolved reference with `python3 -I moai/tools/dump.py grep`.
5. Write the blueprint as a short spec and expand it with `blueprint.py build`; it checks roles, cardinality, assignability, enum values and placeholders. Then dry-run it (`dryRun:true`).

## Quick Start

1. Pass `projectPath` in every call (`moai:mps-mcp-workflow`, "Which project the tools act on"). If it is unknown, use the current directory on the first call, then take the path from the rejection and reuse it. If the project list is empty, ask the user to open the project.
2. Resolve the editable target model and its ObjectFlow entity/property declarations.
3. Start with a JSON file from [references/blueprints](references/blueprints) and replace every `$TARGET_*` placeholder. Search the result for `TARGET_`; any match stops the write. Or write a short spec and expand it with `python3 -I moai/tools/blueprint.py build SPEC` (format: `blueprint.py --help`); check a filled template with `blueprint.py check`.
4. Send the blueprint inline (up to 4 KB) or copy it to `${TMPDIR:-/tmp}` and pass the copy's absolute path; the server rejects files under `skills/`.
5. Dry-run a new root with `mps_mcp_insert_root_node_from_json`. It checks concepts, roles and assignability only: names are not looked up ("is a name, not looked up" is expected) and node factories do not run.
6. Insert the root, then add `persistenceMapping`, `atomMpig`, or `member` subtrees incrementally with `mps_mcp_update_node`. After each real write, `fixReferences.stillBroken` must be 0.
7. Compare the inserted node with its blueprint: `mps_mcp_print_node` (`deep=true`) of the new node, then `python3 -I moai/tools/verify.py node BLUEPRINT PRINTOUT`. Fix every deviation; read what it lists as "added" (node-factory effects). Validate after each substantial subtree and after the finished root (several roots: model reference with `perRoot=true`). Read a large report with `python3 -I moai/tools/dump.py problems FILE` (one line per problem).
8. Review every changed root against the applicable conventions. A shape copied from a blueprint, a packaged example, or the project itself does not prove compliance.
9. Generate or build the owning solution when semantic or generated-code correctness matters. After generation, or when a call reports `ok` but the effect is missing, check `mps_mcp_read_ide_log` (`sinceMinutes`, `minLevel="WARN"`).

## Stable Package References

- Language module: `5aaa957f-3447-4783-b1f7-b301fa3e0394(org.modellwerkstatt.manmap)`
- Concept-tools language ref: `l:5aaa957f-3447-4783-b1f7-b301fa3e0394:org.modellwerkstatt.manmap`
- Structure model: `r:0099bcb7-afa1-43de-901e-d5e48f4490ca(org.modellwerkstatt.manmap.structure)`
- Runtime solution: `37fdf88a-1025-4d01-864a-0bf987f72e6f(org.modellwerkstatt.manmap.runtime)`
- Shipped examples/tests module: `3c6ef8ca-6366-4c8b-8839-0277eaca1f7e(org.modellwerkstatt.dataux.tests)`

The shipped examples module may be globally visible rather than part of the selected project's dependency closure. Resolve it with an explicit module/model reference or with `includeStubModules=true`, and keep it read-only unless the task explicitly targets that module.

## Related Languages and Documentation

ManMap references ObjectFlow entities, value objects, DTOs, and properties; repository bodies use BaseLanguage and may use closures and collections. DataUX consumes the commands and read models built above this persistence layer. Use these package documents for domain semantics and ownership boundaries:

- [ManMap documentation](../../docu/manmap.md)
- [ObjectFlow documentation](../../docu/objectflow.md)
- [DataUX documentation](../../docu/dataux.md)
- [MoWare Workbench overview](../../docu/moware-werkbank.md)

## Reference Guide

- [Concept and role map](references/concepts.md)
- [Shipped examples and verified anchors](references/sandbox.md)
- [Creation and editing workflows](references/workflows.md)
- [Runtime and modeling gotchas](references/gotchas.md)
- [Blueprint index and placeholder contract](references/blueprints.md)
