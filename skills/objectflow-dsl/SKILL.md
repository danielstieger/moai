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
- Determine the active MPS target dynamically with `mps_mcp_list_open_projects`. Never persist a project path, editor-session state, or references from an application project.
- For targets outside the packaged solution, use explicit placeholders such as `TARGET_OFX_CONFIG`, then resolve them in the destination model before writing.

## Critical rules

- Use MPS MCP tools; never hand-edit serialized `.mps` or `.mpl` XML.
- Query concepts with `mps_mcp_get_concept_details` and `l:ec097fca-5b84-41f2-847d-6a5690cae277:org.modellwerkstatt.objectflow`, not the module-style reference.
- Use fully qualified concept names in JSON blueprints.
- Prefer a root skeleton followed by surgical `ADD CHILD` operations for large or uncertain roots.
- Dry-run JSON first and inspect warnings. After real changes, run `mps_mcp_check_root_node_problems` on each changed root; build or generate when the task requires it.
- Never infer that a successful insert is semantically valid.
- Keep domain methods free of repository/service `OperationCall`s; load facts first and coordinate infrastructure in a service or command. See [Services and domain logic](../../docu/objectflow.md#service-komponenten).
- Validate all expected business failures before mutating a graph. See [Preconditions, validation, guards, and exceptions](../../docu/objectflow.md#preconditions-validation-guards-und-exceptions).
- Treat Value Objects immutably and use their selected equality properties deliberately. See [Entity, Value Object, and DTO](../../docu/objectflow.md#entity-value-object-und-dto) and [Value Object equality](../../docu/objectflow.md#value-object-gleichheit).
- Choose the comparison operator by type: `==` for `int`, `boolean`, `BigDecimal`, and Entities; `of` / `status switch` for Status; `:eq:` / `:ne:` for `string`, `LocalDate`, `DateTime`, Value Objects, and other non-DTO objects. `==` on a `string` compiles to `equals` but is no longer to be used; on the other `:eq:` types it compiles to an identity check. ManMap `where` filters accept only `==` / `!=`, for every type; see [filter expressions](../../docu/manmap.md#spezifikum---filterausdrücke-und-gemappte-felder). `==` on Entities compares the instance, which is unique per identity only for session-integrated Entities; otherwise compare keys. DTOs have no meaningful object comparison; compare individual properties. The "always `:eq:`" rule of `moai:mps-baselanguage` applies only to MPS nodes. See [comparison rules](../../docu/objectflow.md#null-werte-in-datenstrukturen).
- Do not assume lazy loading or cascading persistence. See [explicit graph loading](../../docu/moware-werkbank.md#grundprinzipien-für-die-anwendungsentwicklung) and the [ManMap relationship rules](../../docu/manmap.md#referenzen-eingebettete-werte-und-listen).

## Quick start

1. Call `mps_mcp_list_open_projects` and select the intended MPS project dynamically. For a new application module, follow [From modeling to execution](../../docu/moware-werkbank.md#von-der-modellierung-zur-ausführung) and wire it with `mps_mcp_module_dependency` and `mps_mcp_model_used_language`.
2. Inspect the destination model's dependencies and used languages with `mps_mcp_get_project_structure`.
3. Load [references/concepts.md](references/concepts.md) and the task-specific recipe in [references/workflows.md](references/workflows.md).
4. Inspect a packaged reference root from [references/sandbox.md](references/sandbox.md) when a concrete shape is needed.
5. Start from [references/blueprints/](references/blueprints/). Replace names and every `TARGET_*` placeholder.
6. Dry-run a root with `mps_mcp_insert_root_node_from_json`; dry-run a subtree with `mps_mcp_update_node` using `ADD CHILD`.
7. Insert the skeleton, add large subtrees incrementally, and preserve existing node IDs with surgical updates.
8. Run `mps_mcp_check_root_node_problems` on each changed root, repair resolvable references if needed, and run the task-required make/generation checks.

## Stable project references

- Language module: `ec097fca-5b84-41f2-847d-6a5690cae277(org.modellwerkstatt.objectflow)`
- Concept-tools language ref: `l:ec097fca-5b84-41f2-847d-6a5690cae277:org.modellwerkstatt.objectflow`
- Structure model: `r:5abca60f-e29b-478e-90f5-405db58d17d2(org.modellwerkstatt.objectflow.structure)`
- Packaged example solution: `3c6ef8ca-6366-4c8b-8839-0277eaca1f7e(org.modellwerkstatt.dataux.tests)`
- ObjectFlow extends ManMap, BaseLanguage, and `jetbrains.mps.execution.util`. Load the [ManMap DSL skill](../manmap-dsl/SKILL.md) when persistence mappings, repository operations, or SQL are involved.

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
