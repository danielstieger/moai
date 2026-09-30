---
name: manmap-dsl
description: "Use when creating, editing, validating, or inspecting MoWare ManMap persistence (org.modellwerkstatt.manmap): table and column mappings, keys and auto IDs, repositories, loading queries (get/where, joins), checkout, saving and deleting object graphs, custom SQL and read models."
---

# ManMap DSL

ManMap models relational persistence and read models for MoWare applications. `PersistenceDescription` maps ObjectFlow entities and value objects to tables and columns; `Repository` contains mapped queries, explicit save/delete operations, reusable row mappers, no-key read-only mappers, and direct SQL. Loading, graph persistence, session identity, and transaction boundaries are explicit rather than implicit.

## Critical Rules

- Use MPS MCP tools. Never read or edit serialized `.mps` or `.mpl` XML.
- Determine the target MPS project dynamically with `mps_mcp_list_open_projects`; never reuse a path recorded by this skill.
- Discover the language by its qualified name `org.modellwerkstatt.manmap`. Query concepts with `l:5aaa957f-3447-4783-b1f7-b301fa3e0394:org.modellwerkstatt.manmap`, not the module reference syntax.
- Use fully qualified concept names in JSON blueprints.
- Treat every `$TARGET_*` value in a blueprint as a required target-model placeholder. Resolve it by scope or replace it with a persistent `r:` node reference from the target model immediately before insertion.
- Never copy persistent references from an application example into another model. The stable references in [sandbox.md](references/sandbox.md) are read-only navigation and verification anchors, not insertion values.
- Prefer skeleton-plus-subtree construction for persistence descriptions and repositories. Preserve existing node IDs with surgical updates.
- A mapping never implies lazy loading, cascading save, or cascading delete. Load references and lists with separate queries; use `refJoin`/`listJoin` only when the query filters or sorts on the joined mapping. [Explicit loading](../../docu/manmap.md#explizites-laden)
- In a blueprint, set `MappingReference.mappingSource` to the name of the query's `EntityMapping`; it resolves to the enclosing query even within the same blueprint. See [mapped query workflow](references/workflows.md#build-a-mapped-query).
- New `QueryFromMap` nodes default to `readOnly = true`. Set `readOnly = false` deliberately for queries that check out data for editing.
- Validate changed roots with `mps_mcp_check_root_node_problems`; then run task-required generation or build checks.
- Load `mps-baselanguage` and `mps-node-editing` before constructing repository methods or expression/statement subtrees.

## Quick Start

1. Call `mps_mcp_list_open_projects` and select the intended target project from the user's task or editor focus. Ask when multiple candidates remain ambiguous.
2. Resolve the editable target model and its ObjectFlow entity/property declarations.
3. Start with a JSON file from [references/blueprints](references/blueprints) and replace every `$TARGET_*` placeholder.
4. Dry-run a new root with `mps_mcp_insert_root_node_from_json`.
5. Insert the root, then add `persistenceMapping`, `atomMpig`, or `member` subtrees incrementally with `mps_mcp_update_node`.
6. Validate after each substantial subtree and after the finished root.
7. Generate or build the owning solution when semantic or generated-code correctness matters.

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
