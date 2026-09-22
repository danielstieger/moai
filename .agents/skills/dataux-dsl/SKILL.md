---
name: dataux-dsl
description: Use when creating, editing, validating, or inspecting org.modellwerkstatt.dataux UI models, PagePanes, applications, or batchjobs.
---

# DataUX DSL

DataUX models the user-interface side of ObjectFlow pages and the executable module around an application or batchjob. `PagePane` binds forms, tables, layouts, menus, and custom elements to ObjectFlow entities or DTOs. `AppUiModule` supplies navigation and UI lifecycle, while `BatchJobModule` supplies producer/consumer execution and scheduling.

## Critical rules

- Use MPS MCP tools. Never read or edit serialized `.mps` or `.mpl` XML directly.
- Query concepts with `l:64adc67c-5fcf-45f5-82db-6a6771963d93:org.modellwerkstatt.dataux`, not the module reference `64adc67c-5fcf-45f5-82db-6a6771963d93(org.modellwerkstatt.dataux)`.
- Use fully qualified concept names from [concepts.md](references/concepts.md) in JSON blueprints.
- Resolve every bound classifier, property, command, label, configuration, and producer/consumer pair in the target model. Sandbox references are examples, not reusable targets.
- Prefer a small root skeleton followed by role-specific subtree insertion for `PagePane`, application, and batchjob roots.
- Preserve persistent node IDs when editing existing roots. Use surgical node updates instead of deleting and recreating roots.
- A UI binding does not load data. Commands and repositories must provide the required entities, DTOs, references, and lists.
- All tables with the same row type inside one `PagePane` share the selection of that type.
- Validate every changed root with `mps_mcp_check_root_node_problems`; run generation/build checks required by the task.
- Load `mps-baselanguage` and `mps-node-editing` before constructing embedded expressions or non-trivial node subtrees.

## Quick start

1. Discover the open project with `mps_mcp_list_open_projects` and pass its exact `mpsProjectBaseDirectory` as `projectPath`.
2. Use the recorded `simpleone` models in [sandbox.md](references/sandbox.md) for representative UI, application, and batchjob examples.
3. Start from [references/blueprints](references/blueprints), and replace every `<...>` placeholder with a real value or persistent target reference.
4. Dry-run root JSON with `mps_mcp_insert_root_node_from_json(dryRun=true)`.
5. Insert the root, then add delegates, menu items, layouts, or module content incrementally with `mps_mcp_update_node`.
6. Check selection and binding semantics against [workflows.md](references/workflows.md) and [gotchas.md](references/gotchas.md).
7. Run `mps_mcp_check_root_node_problems`, then make/generate the affected solution when requested.

## Project references

- Language module: `64adc67c-5fcf-45f5-82db-6a6771963d93(org.modellwerkstatt.dataux)`
- Concept-tools language ref: `l:64adc67c-5fcf-45f5-82db-6a6771963d93:org.modellwerkstatt.dataux`
- Structure model: `r:29bd6c27-4b8b-45de-826b-b6e588367a39(org.modellwerkstatt.dataux.structure)`
- Runtime solution: `bd230cc8-9f23-4d08-88ae-92ff30662c34(org.modellwerkstatt.dataux.runtime)`
- Discovery project: `/home/rocketdan/migration/2026_1/simpleone`
- Primary editable example module: `f6ea4529-b826-49cb-a717-2ac43f8ba5f5(org.modellwerkstatt.simple)`
- Primary application model: `r:579ac6f7-5136-4b5d-93d4-60d7664141bd(org.modellwerkstatt.simple.app)`
- Rich UI model: `r:9a5d071c-824e-4204-b68c-cfe03dc3bd00(org.modellwerkstatt.simple.order.unitOrderHandling)`

## Related DSL skills

- [ObjectFlow DSL](../objectflow-dsl/SKILL.md): load for bound entities/DTOs, Commands, Pages, configurations, and producer/consumer pairs.
- [ManMap DSL](../manmap-dsl/SKILL.md): load when the UI or batch workflow depends on mapped queries, explicit loading, saving, or SQL-backed DTOs.
- `mps-baselanguage`: load for DataUX expressions, authentication bodies, lifecycle statements, dynamic colors/labels, and command arguments.
- `mps-node-editing`: load before creating or restructuring MPS nodes from JSON.

## References

- [Concepts](references/concepts.md)
- [Simpleone examples and stable refs](references/sandbox.md)
- [Workflows](references/workflows.md)
- [Gotchas](references/gotchas.md)
- [Blueprints](references/blueprints)

