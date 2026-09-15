---
name: manmap-dsl
description: Use when creating, editing, validating, or inspecting org.modellwerkstatt.manmap models, persistence mappings, repositories, mapped queries, saves, or direct SQL.
---

# ManMap DSL

ManMap (`manual map`) is a domain-specific object-relational mapper. It primarily maps ObjectFlow `Entity` and `ValueObject` concepts to SQL data. An `EntityMapping` describes a table mapping; repositories use mappings to query and assemble objects or to save and delete entities. Object trees follow an explicitly chosen loading strategy. `C2SqlBlock` also supports direct SQL.

Use `QueryFromMap` for ORM queries through an `EntityMapping`, and `C2SqlBlock` for direct SQL. For C2 results, use an inline row-mapping closure or `RowMapperFieldRef` for a small scalar result and `NoKeyMapperField` for a result without a usable key, often an aggregate mapped to an ObjectFlow DTO. A `NoKeyMapperField` can map fields itself or reuse an existing `EntityMapping` through `IncludeMapping`; `MappingReference` cannot point directly to `EntityMapping`.

## Critical Rules

- Use MPS MCP tools. Never read or edit serialized `.mps` or `.mpl` XML directly.
- Query concepts with `l:5aaa957f-3447-4783-b1f7-b301fa3e0394:org.modellwerkstatt.manmap`, not the module reference `5aaa957f-3447-4783-b1f7-b301fa3e0394(org.modellwerkstatt.manmap)`.
- The permanent ManMap test models may be global libraries outside the open project dependency closure. Resolve them with `mps_mcp_get_project_structure(startingPoint="org.modellwerkstatt.objectflow.tests.manmap.Domain", includeStubModules=true)` or use explicit model references; a name search with `scope="all"` may return no roots.
- Use fully qualified concept names from [concepts.md](references/concepts.md) in JSON blueprints.
- Prefer a root skeleton followed by role-specific subtree insertion for large persistence descriptions and repositories.
- Preserve existing node IDs when editing. Use surgical node updates instead of deleting and recreating nodes.
- `SaveWithMap` writes the owning entity's mapped reference key, but never saves referenced entities or list elements automatically; see [mapped operations](references/mapped-operations.md).
- Validate every changed root with `mps_mcp_check_root_node_problems`; run generation/build checks required by the task.
- Repository methods contain BaseLanguage, closures, collections, and references to mapping nodes. Load `mps-baselanguage` and `mps-node-editing` before constructing them.

## Quick Start

1. Use `org.modellwerkstatt.objectflow.tests.manmap.Domain` as the main example model. Use `XNokeys` for no-key/custom mapper cases and `ZMixedNewer` for small blob/list examples.
2. Start from [references/blueprints](references/blueprints) and replace every `<...>` placeholder with a real property value or persistent node reference.
3. Dry-run root JSON with `mps_mcp_insert_root_node_from_json`.
4. Insert the root, then add `persistenceMapping` or `member` subtrees incrementally.
5. Resolve mapping/class/property references from the target model; do not copy references blindly from the sandbox.
6. Run `mps_mcp_check_root_node_problems`, then make/generate the affected solution when requested.

## Stable References

Discover the open MPS project with `mps_mcp_list_open_projects` and pass its actual `mpsProjectBaseDirectory` as `projectPath`; checkout paths vary.

- Language module: `5aaa957f-3447-4783-b1f7-b301fa3e0394(org.modellwerkstatt.manmap)`
- Concept-tools language ref: `l:5aaa957f-3447-4783-b1f7-b301fa3e0394:org.modellwerkstatt.manmap`
- Structure model: `r:0099bcb7-afa1-43de-901e-d5e48f4490ca(org.modellwerkstatt.manmap.structure)`
- Runtime solution: `37fdf88a-1025-4d01-864a-0bf987f72e6f(org.modellwerkstatt.manmap.runtime)`
- Permanent examples module: `3c6ef8ca-6366-4c8b-8839-0277eaca1f7e(org.modellwerkstatt.dataux.tests)`

## Related Languages

ManMap roots and references are tightly integrated with `jetbrains.mps.baseLanguage`; query bodies also use closures and collections. The dataux examples map and query `org.modellwerkstatt.objectflow` entities, so load the [ObjectFlow DSL skill](../objectflow-dsl/SKILL.md) when the task creates or changes those entity/property targets.

## References

- [Concepts](references/concepts.md)
- [Explicit loading](references/loading.md)
- [Diagnose: nicht geladene Referenz](references/troubleshooting.md)
- [Diagnose SQL- und Mapping-Fehler](references/sql-troubleshooting.md)
- [Direct SQL and C2 result mapping](references/direct-sql.md)
- [C2 SQL values and named parameters](references/c2-parameters.md)
- [Mapped queries, saves, and deletes](references/mapped-operations.md)
- [Mapped query operators](references/query-operators.md)
- [Keys and Save decision](references/keys.md)
- [Session identity and read-only results](references/session-behavior.md)
- [Mapping composition and list back-references](references/mapping-composition.md)
- [Optimistic locking, audit, batch, and archive options](references/advanced-options.md)
- [Sandbox examples](references/sandbox.md)
- [Permanent test index](references/test-index.md)
- [Workflows](references/workflows.md)
- [Gotchas](references/gotchas.md)
- [Blueprints](references/blueprints)
