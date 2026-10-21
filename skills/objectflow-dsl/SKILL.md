---
name: objectflow-dsl
description: "Use when creating, editing, validating, or inspecting MoWare ObjectFlow models (org.modellwerkstatt.objectflow): domain model with entities, value objects, DTOs, status and business properties; services, business rules, validations and preconditions; commands (search, create, edit), pages, page conclusions and use-case flow; tests with test suites and run command; OFX configuration, roles and permissions."
---

# ObjectFlow DSL

ObjectFlow models domain structures, domain/application logic, command-driven use cases, tests, configuration, permissions, and shared resources. It cooperates with ManMap for persistence and DataUX for presentation and executable modules; use ObjectFlow for business meaning and control flow, not SQL mappings or UI layout.

## Source authority and portability

- Treat the live `org.modellwerkstatt.objectflow` language as the technical authority for concepts, features, cardinalities, and assignability.
- Use the packaged solution `org.modellwerkstatt.dataux.tests` for stable examples. Its verified model and node references are in [references/sandbox.md](references/sandbox.md).
- Use the package documentation for semantics and runtime behavior; start with the [ObjectFlow scope](../../docu/objectflow.md#modellierungsumfang-und-ausdrucksmöglichkeiten) and the [MoWare responsibility map](../../docu/moware-werkbank.md#wo-gehört-eine-änderung-hin).
- Never persist a project path, editor-session state, or references from an application project.
- Conventions are referenced by name, e.g. conventions `commands` (file `mw-commands_v1.md`); the project's `AGENTS.md` states where they are and which ones it changes. This skill does not repeat their content.
- For targets outside the packaged solution, use explicit placeholders such as `TARGET_OFX_CONFIG`, then resolve them before writing. The destination model imports the model that holds the `OFXConfig`s (conventions `anwendungsaufbau`) and references the config; it never holds its own copy.

## Critical rules

- Use MPS MCP tools; never read or edit raw `.mps` / `.mpl` XML (rule and fallback: [`MPS_AGENT_GUIDE.md`](../../MPS_AGENT_GUIDE.md#never-read-raw-mps-model-files)).
- Query concepts with `mps_mcp_get_concept_details` and `l:ec097fca-5b84-41f2-847d-6a5690cae277:org.modellwerkstatt.objectflow`, not the module-style reference.
- Use the `qualifiedName` as `concept` in blueprints (`moai:mps-mcp-workflow`, `references/node-editing-rules.md`).
- Prefer a root skeleton followed by surgical `ADD CHILD` operations for large or uncertain roots.
- Before writing, search the blueprint text for `TARGET_`; every hit stops the write. The dry-run checks concepts, roles, and assignability only: it does not look up names (each name gets "is a name, not looked up", existing or not, so a forgotten `TARGET_OFX_CONFIG` passes) and runs no node factories.
- After a real write, `fixReferences.stillBroken` must be 0. Then run `mps_mcp_check_root_node_problems` on the changed root, or after work on several roots once on the model reference with `perRoot=true`. Read `warnings`, `details.uncheckedSubtrees`, `rules[].statement`, and `quickFixes` (apply with `mps_mcp_apply_intention`, see `mps_mcp_list_node_intentions`, or `autoApplyQuickFixes=true`). Build or generate when the task requires it.
- Node factories run on every real insert and fill the roles a blueprint omits; Entity and Value Object skeletons are not complete without follow-up edits. See [Node factories](references/gotchas.md#node-factories).
- Never infer that a successful insert is semantically valid.
- Methods on data structures (no `OperationCall`, no reloading): see [Methoden an Datenstrukturen](../../docu/objectflow.md#methoden-an-datenstrukturen).
- Validate before mutating (Precondition, `validation`, Guard): see [Preconditions, Validation, Guards und Exceptions](../../docu/objectflow.md#preconditions-validation-guards-und-exceptions).
- Value Objects (immutable style, `equalProperties`): see [Entity, Value Object und DTO](../../docu/objectflow.md#entity-value-object-und-dto) and [Value-Object-Gleichheit](../../docu/objectflow.md#value-object-gleichheit).
- Comparison operators depend on the ObjectFlow type (`==` vs `:eq:`/`:ne:`, `of` / `status switch` for Status, no object comparison for DTOs): see [Null-Werte in Datenstrukturen](../../docu/objectflow.md#null-werte-in-datenstrukturen). Entity references: `#Key` and `isNullKey`, see [Beziehungen und Objektgraphen](../../docu/objectflow.md#beziehungen-und-objektgraphen). When the type of an operand is unclear, ask `mps_mcp_query_types` or `mps_mcp_query_nodes` `GET_TYPE` (`moai:mps-mcp-workflow`, `references/type-queries.md`) instead of guessing. ManMap `where` filters follow their own rules (`==`/`!=`, `<` … `>=`, `in`, `like`, `optional`; no `:eq:`), see [Filterausdrücke](../../docu/manmap.md#spezifikum---filterausdrücke-und-gemappte-felder). The "always `:eq:`" rule of `moai:mps-baselanguage` applies to SNode comparisons in MPS code only, not to ObjectFlow expressions.
- No lazy loading, no cascading save/delete: see [Grundprinzipien für die Anwendungsentwicklung](../../docu/moware-werkbank.md#grundprinzipien-für-die-anwendungsentwicklung) and [Explizites Laden](../../docu/manmap.md#explizites-laden).

## Quick start

1. Pass `projectPath` in every call (`moai:mps-mcp-workflow`, "Which project the tools act on"). If it is unknown, use the current directory on the first call, take the path from the rejection, and reuse it; if the project list is empty, ask the user to open the project. For a new application module, follow [From modeling to execution](../../docu/moware-werkbank.md#von-der-modellierung-zur-ausführung) and wire it with `mps_mcp_module_dependency` and `mps_mcp_model_used_language`.
2. Inspect the destination model's dependencies and used languages with `mps_mcp_get_project_structure`.
3. Load [references/concepts.md](references/concepts.md) and the task-specific recipe in [references/workflows.md](references/workflows.md).
4. Inspect a packaged reference root from [references/sandbox.md](references/sandbox.md) when a concrete shape is needed.
5. Start from [references/blueprints/](references/blueprints/). Replace names and every `TARGET_*` placeholder, then search the text for `TARGET_` (any hit: stop). Send the JSON inline (≤ 4 KB, true for every blueprint here) or copy it to `${TMPDIR:-/tmp}` and pass the copy's absolute path; files under `skills/` are rejected.
6. Dry-run a root with `mps_mcp_insert_root_node_from_json`; dry-run a subtree with `mps_mcp_update_node` using `ADD CHILD`. Name warnings are expected.
7. Insert the skeleton, check `fixReferences.stillBroken` = 0, and `print_node` the result (factory effects). Add large subtrees incrementally and preserve existing node IDs with surgical updates.
8. Review every changed root against the applicable conventions. A shape copied from a blueprint, a packaged example, or the project itself does not prove compliance.
9. Run `mps_mcp_check_root_node_problems` on the changed root (several roots: the model reference with `perRoot=true`) and run the task-required make/generation checks. If a call reports `ok` but the effect is missing, or after make/generation, read `mps_mcp_read_ide_log(sinceMinutes, minLevel="WARN")` (`moai:mps-mcp-workflow`, `references/ide-log.md`).

## Stable project references

- Language module: `ec097fca-5b84-41f2-847d-6a5690cae277(org.modellwerkstatt.objectflow)`
- Concept-tools language ref: `l:ec097fca-5b84-41f2-847d-6a5690cae277:org.modellwerkstatt.objectflow`
- Structure model: `r:5abca60f-e29b-478e-90f5-405db58d17d2(org.modellwerkstatt.objectflow.structure)`
- Packaged example solution: `3c6ef8ca-6366-4c8b-8839-0277eaca1f7e(org.modellwerkstatt.dataux.tests)`
- ObjectFlow extends ManMap, BaseLanguage, and `jetbrains.mps.execution.util`. Load the `moai:manmap-dsl` skill when persistence mappings, repository operations, or SQL are involved.

## Documentation map

- [ObjectFlow domain structures](../../docu/objectflow.md#teil-i--fachliche-datenmodellierung)
- [ObjectFlow services and domain logic](../../docu/objectflow.md#teil-ii--services-und-domänenlogik)
- [ObjectFlow commands and use cases](../../docu/objectflow.md#teil-iii--commands-und-anwendungsabläufe)
- [ObjectFlow tests](../../docu/objectflow.md#teil-iv--tests-mit-objectflow)
- [ObjectFlow cross-cutting concerns](../../docu/objectflow.md#teil-v--querschnittsthemen)
- [ManMap persistence](../../docu/manmap.md#die-zwei-zugriffswege-im-überblick)
- [DataUX UI and executable modules](../../docu/dataux.md#modellierungsumfang-und-ausdrucksmöglichkeiten)
- [MoWare architecture and DSL responsibilities](../../docu/moware-werkbank.md#zusammenspiel-der-dsls)

## References

- [Concepts and verified AST roles](references/concepts.md)
- [Packaged examples](references/sandbox.md)
- [Creation and editing workflows](references/workflows.md)
- [Gotchas and diagnostics](references/gotchas.md)
- [Blueprint index](references/blueprints.md)
