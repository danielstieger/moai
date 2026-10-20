---
name: baselanguage-collections-dsl
description: Collections and closures. Use when creating, editing, validating, or inspecting jetbrains.mps.baseLanguage.collections types, creators, collection operations (`.where`, `.select`, `.translate`, …), map/list access, collection foreach statements, `downcast`, or jetbrains.mps.baseLanguage.closures closure literals, function types, `yield`/`skip`/`stop` and SAM conversion in MPS models.
---

# BaseLanguage Collections and Closures

`jetbrains.mps.baseLanguage.collections` extends BaseLanguage with typed sequences, lists, sets, maps, collection creators, query-like operations, and collection-aware iteration. It builds on `jetbrains.mps.baseLanguage.closures`, which supplies closure literals (`{ it => … }`), function types, `yield` and SAM conversion; both are covered here. Its everyday expression, statement, and type concepts are nested inside BaseLanguage or another host DSL. The one rootable concept, `CustomContainers`, is a specialized registry for defining custom collection implementations.

## Source authority and portability

- Treat the installed `jetbrains.mps.baseLanguage.collections` and `jetbrains.mps.baseLanguage.closures` runtime descriptors as the authority for concepts, features, cardinalities, and assignability.
- Use the packaged solution `org.modellwerkstatt.dataux.tests` for stable examples listed in [references/sandbox.md](references/sandbox.md).
- Never persist a project path or IDE-session state.
- Never copy model, root, or node references from an application project. Patterns learned elsewhere must be anonymized and use explicit `TARGET_*` placeholders.
- All links in this skill are relative and stay inside the distributed package.

## Critical rules

- Use MPS MCP tools; never read or edit raw `.mps` / `.mpl` XML (rule and fallback: [`MPS_AGENT_GUIDE.md`](../../MPS_AGENT_GUIDE.md#never-read-raw-mps-model-files)).
- Query concepts with `mps_mcp_get_concept_details` and `l:83888646-71ce-4f1c-9c53-c54016f6ad4f:jetbrains.mps.baseLanguage.collections` (closures: `l:fd392034-7849-419d-9071-12563d152375:jetbrains.mps.baseLanguage.closures`), not the module-style reference.
- Use the `qualifiedName` as `concept` in blueprints (`moai:mps-mcp-workflow`, `references/node-editing-rules.md`).
- Collections operations are usually the `operation` child of a BaseLanguage `DotExpression`; do not insert them as standalone expressions.
- Operations with a predicate/selector take exactly one `ClosureLiteral` in role `closure` (not `parameter`); every closure parameter needs a `type` child (`UndefinedType`) — [references/closures-catalog.md](references/closures-catalog.md).
- A `sequence` is not a `list`: lazy operations return `sequence<T>`; materialize with `.toList` where a `list` is required — [references/gotchas.md](references/gotchas.md).
- A closure body uses either `return` or `yield`, never both; `skip`/`stop` only inside enumerating closures (`selectMany`/`translate`/`forEach`/sequence initializer) — [references/concepts.md](references/concepts.md#control-flow-within-closures).
- Runtime solutions: generated closures code needs `jetbrains.mps.baseLanguage.closures.runtime`, collections code `collections.runtime`; a missing closures runtime shows as `NoClassDefFoundError` for `_FunctionTypes$...` at load time — [references/closures-catalog.md](references/closures-catalog.md#runtime-dependency).
- When the choice depends on a type (IsEmpty family, foreach family, `list` vs `sequence`, a closure against a SAM target), ask `mps_mcp_query_types` (`OPERATION_TYPE`, `IS_SUBTYPE`) instead of reasoning about typesystem rules — `moai:mps-mcp-workflow` (`references/type-queries.md`).
- Prefer a small host skeleton followed by subtree insertion when the surrounding BaseLanguage code is large or uncertain.
- Replace every `$TARGET_X$` placeholder with a resolvable destination-model reference before writing; the dry-run does not look names up, so search the text for `TARGET_` first.
- Validate the changed containing root with `mps_mcp_check_root_node_problems` (several roots: the model reference with `perRoot=true`); build or generate when the task requires it.

## Quick start

1. Pass `projectPath` in every call (`moai:mps-mcp-workflow`, "Which project the tools act on"). If it is unknown, use the current directory on the first call, take the path from the rejection, and reuse it; if the project list is empty, ask the user to open the project.
2. Inspect the destination model with `mps_mcp_get_project_structure`; in a MoWare model the DevKit `org.modellwerkstatt.MoWareWerkbank` provides BaseLanguage, Collections and Closures (see `moai:mps-node-editing`).
3. Load [references/concepts.md](references/concepts.md), then select a recipe from [references/workflows.md](references/workflows.md).
4. Inspect a packaged example from [references/sandbox.md](references/sandbox.md) if a concrete AST shape is needed.
5. Start from [references/blueprints/](references/blueprints/). Replace every `$TARGET_X$` placeholder, then search the text for `TARGET_` (any hit: stop). Send the JSON inline (≤ 4 KB, true for every blueprint here) or copy it to `${TMPDIR:-/tmp}` and pass the copy's absolute path; files under `skills/` are rejected (`moai:mps-node-editing`, File-Path Semantics).
6. Dry-run ordinary Collections subtrees with `mps_mcp_update_node` (`ADD CHILD`) against a host node. For the specialized `CustomContainers` root, dry-run [its root skeleton](references/blueprints/custom-containers-root-skeleton.json) with `mps_mcp_insert_root_node_from_json`; use the BaseLanguage skill for other host-language roots. The dry-run checks concepts, roles and assignability only; name warnings ("is a name, not looked up") are expected.
7. Insert or replace the smallest subtree possible, check `fixReferences.stillBroken` = 0, and preserve existing node IDs.
8. Run `mps_mcp_check_root_node_problems` on the containing root (several roots: the model reference with `perRoot=true`) and any task-required make/generation checks.

## Stable references

- Language module: `83888646-71ce-4f1c-9c53-c54016f6ad4f(jetbrains.mps.baseLanguage.collections)`
- Concept-tools language ref: `l:83888646-71ce-4f1c-9c53-c54016f6ad4f:jetbrains.mps.baseLanguage.collections`
- Runtime solution: `9b80526e-f0bf-4992-bdf5-cee39c1833f3(collections.runtime)`
- Closures language: `fd392034-7849-419d-9071-12563d152375(jetbrains.mps.baseLanguage.closures)`; concept-tools ref `l:fd392034-7849-419d-9071-12563d152375:jetbrains.mps.baseLanguage.closures`; runtime `jetbrains.mps.baseLanguage.closures.runtime`
- Packaged example solution: `3c6ef8ca-6366-4c8b-8839-0277eaca1f7e(org.modellwerkstatt.dataux.tests)`
- The language builds on BaseLanguage and BaseLanguage Closures. Load `moai:mps-baselanguage` for host Java nodes and `moai:mps-model-manipulation` for the smodel side (node receivers such as `node.descendants<C>`, casts, property/link access) that closure bodies call.

## References

- [Concepts and verified AST roles](references/concepts.md)
- [Closures: literals, parameters, function types, `yield`, SAM conversion, runtime](references/closures-catalog.md)
- [Two `foreach` concepts, with blueprints](references/foreach-statements.md)
- [`downcast expr` — collection value to Java interface](references/downcast-expression.md)
- [Packaged examples](references/sandbox.md)
- [Creation and editing workflows](references/workflows.md)
- [Gotchas and diagnostics](references/gotchas.md)
- [Blueprint index](references/blueprints.md)
