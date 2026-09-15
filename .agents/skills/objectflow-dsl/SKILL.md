---
name: objectflow-dsl
description: Use when creating, editing, validating, or inspecting org.modellwerkstatt.objectflow entities, DTOs, value objects, services, commands, and configuration.
---

# ObjectFlow DSL

ObjectFlow defines MoWare domain objects and application flows. `Entity`, `ValueObject`, and `DTO` roots carry typed business properties; `Service` roots hold operations; `Command` roots coordinate parameters, pages, and actions. This skill draws on live MPS concept descriptors and examples in the open `eFWWS` project.

## Critical rules

- Use MPS MCP tools for models. Never read or edit serialized `.mps` or `.mpl` files directly.
- Query concepts with `l:ec097fca-5b84-41f2-847d-6a5690cae277:org.modellwerkstatt.objectflow`, not the module reference `ec097fca-5b84-41f2-847d-6a5690cae277(org.modellwerkstatt.objectflow)`.
- Use fully qualified concept names in JSON blueprints. Resolve model and node references in the currently open MPS project before editing.
- Prefer a small root skeleton followed by role-specific subtrees for objects and commands with many members.
- Preserve persistent node IDs when editing existing roots. Validate each changed root with `mps_mcp_check_root_node_problems`.

## Quick start

1. Open the intended MPS project and call `mps_mcp_list_open_projects`; pass its exact `mpsProjectBaseDirectory` as `projectPath`.
2. Use the [example models](references/sandbox.md) to inspect known shapes. The recorded examples currently resolve through `/home/rocketdan/migration/2026_1/eFWWS`.
3. Start from [blueprints](references/blueprints/), replace sample names, and resolve any reference targets in the target model.
4. Dry-run a new root with `mps_mcp_insert_root_node_from_json(dryRun=true)`, then insert it. Add larger child-role subtrees incrementally with `mps_mcp_update_node`.
5. Run `mps_mcp_check_root_node_problems` on the resulting root and make/generate the affected module when the task requires it.

## Project references

- Language module: `ec097fca-5b84-41f2-847d-6a5690cae277(org.modellwerkstatt.objectflow)`
- Concept-tools language ref: `l:ec097fca-5b84-41f2-847d-6a5690cae277:org.modellwerkstatt.objectflow`
- Discovery project: `/home/rocketdan/migration/2026_1/eFWWS`; skill directory: `/home/rocketdan/migration/2026_1/moai_ware/.agents/skills/objectflow-dsl/`.
- Representative example modules: `82cc755e-9c8a-4114-aa86-1ede76bbe483(at.mpreis.erp.stammdaten)`, `b5a345bc-324f-40f7-84c2-544a1bb955b1(at.hafina.filiale.wws)`, `3fdd65e5-0951-488c-bc9c-57c6ce7f6c28(at.mpreis.erp.tech)`.

## Related skills

- [ManMap DSL](../manmap-dsl/SKILL.md): load when an Entity property has persistence options, or a workflow needs repositories and mappings.
- `mps-baselanguage` and `mps-node-editing`: load when building typed properties, methods, expressions, and MPS JSON subtrees.
- DataUX supplies UI roots such as `PagePane` and `Table` commonly used with ObjectFlow commands. Inspect its concepts through MPS MCP until a project-local DataUX skill exists.

## References

- [Concepts](references/concepts.md)
- [Example models and stable refs](references/sandbox.md)
- [Workflows](references/workflows.md)
- [Gotchas](references/gotchas.md)
- [Blueprints](references/blueprints/)
