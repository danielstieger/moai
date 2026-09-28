---
name: baselanguage-collections-dsl
description: Use when creating, editing, validating, or inspecting jetbrains.mps.baseLanguage.collections types, creators, collection operations, map/list access, or collection foreach statements in MPS models.
---

# BaseLanguage Collections DSL

`jetbrains.mps.baseLanguage.collections` extends BaseLanguage with typed sequences, lists, sets, maps, collection creators, query-like operations, and collection-aware iteration. Its everyday expression, statement, and type concepts are nested inside BaseLanguage or another host DSL. The one rootable concept, `CustomContainers`, is a specialized registry for defining custom collection implementations.

## Source authority and portability

- Treat the installed `jetbrains.mps.baseLanguage.collections` runtime descriptors as the authority for concepts, features, cardinalities, and assignability.
- Use the packaged solution `org.modellwerkstatt.dataux.tests` for stable examples listed in [references/sandbox.md](references/sandbox.md).
- Determine the target MPS project dynamically with `mps_mcp_list_open_projects`; never persist a project path or IDE-session state.
- Never copy model, root, or node references from an application project. Patterns learned elsewhere must be anonymized and use explicit `TARGET_*` placeholders.
- All links in this skill are relative and stay inside the distributed package.

## Critical rules

- Use MPS MCP tools; never hand-edit serialized `.mps` or `.mpl` XML.
- Query concepts with `mps_mcp_get_concept_details` and `l:83888646-71ce-4f1c-9c53-c54016f6ad4f:jetbrains.mps.baseLanguage.collections`, not the module-style reference.
- Use fully qualified concept names in JSON blueprints.
- Collections operations are usually the `operation` child of a BaseLanguage `DotExpression`; do not insert them as standalone expressions.
- Every `InferredClosureParameterDeclaration` needs a required `type` child. Use `jetbrains.mps.baseLanguage.structure.UndefinedType` when inference should determine the real type.
- Prefer a small host skeleton followed by subtree insertion when the surrounding BaseLanguage code is large or uncertain.
- Replace every `TARGET_*` placeholder with a resolvable destination-model reference before writing.
- Validate the changed containing root with `mps_mcp_check_root_node_problems`; build or generate when the task requires it.

## Quick start

1. Call `mps_mcp_list_open_projects` and choose the intended MPS project dynamically.
2. Inspect the destination model with `mps_mcp_get_project_structure`; confirm that BaseLanguage, Collections, and—when closures are used—BaseLanguage Closures are available.
3. Load [references/concepts.md](references/concepts.md), then select a recipe from [references/workflows.md](references/workflows.md).
4. Inspect a packaged example from [references/sandbox.md](references/sandbox.md) if a concrete AST shape is needed.
5. Start from [references/blueprints/](references/blueprints/), and replace all placeholders.
6. Dry-run ordinary Collections subtrees with the matching node-update operation against a host node. For the specialized `CustomContainers` root, dry-run [its root skeleton](references/blueprints/custom-containers-root-skeleton.json) with `mps_mcp_insert_root_node_from_json`; use the BaseLanguage skill for other host-language roots.
7. Insert or replace the smallest subtree possible and preserve existing node IDs.
8. Run `mps_mcp_check_root_node_problems` on the containing root and any task-required make/generation checks.

## Stable references

- Language module: `83888646-71ce-4f1c-9c53-c54016f6ad4f(jetbrains.mps.baseLanguage.collections)`
- Concept-tools language ref: `l:83888646-71ce-4f1c-9c53-c54016f6ad4f:jetbrains.mps.baseLanguage.collections`
- Runtime solution: `9b80526e-f0bf-4992-bdf5-cee39c1833f3(collections.runtime)`
- Packaged example solution: `3c6ef8ca-6366-4c8b-8839-0277eaca1f7e(org.modellwerkstatt.dataux.tests)`
- The language builds on BaseLanguage and BaseLanguage Closures. Load [the BaseLanguage skill](../mps-baselanguage/SKILL.md) for host Java nodes and [the model-manipulation skill](../mps-model-manipulation/SKILL.md) for combined Collections/Closures/smodel code.

## References

- [Concepts and verified AST roles](references/concepts.md)
- [Packaged examples](references/sandbox.md)
- [Creation and editing workflows](references/workflows.md)
- [Gotchas and diagnostics](references/gotchas.md)
- [Blueprint index](references/blueprints.md)
