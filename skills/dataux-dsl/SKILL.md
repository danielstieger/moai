---
name: dataux-dsl
description: "Use when creating, editing, validating, or inspecting MoWare DataUX user interfaces (org.modellwerkstatt.dataux): page panes, forms and input fields (delegates), tables and columns, layouts and tabs, master-detail, binding and selection, menus and actions, application modules (AppUI) and batch jobs."
---

# DataUX UI DSL

DataUX describes the presentation and UI interaction layer of a MoWare application and its executable entry points. This skill covers the UI part of `org.modellwerkstatt.dataux` (`PagePane`, forms, tables, layouts, binding paths, delegates, reusable includes, and menus) and the two module roots `AppUI Module` (`AppUiModule`) and `BatchJob Module` (`BatchJobModule`). ObjectFlow owns domain meaning, commands, pages, selections, producer/consumer pairs, and session behavior; ManMap owns loading and persistence.

## Source authority and portability

- Treat the live `org.modellwerkstatt.dataux` language as the technical authority for concepts, roles, cardinalities, reference targets, and assignability.
- Use the package documentation for semantics and runtime behavior; start with [DataUX UI modeling](../../docu/dataux.md#teil-i--ui-modellierung) and the [MoWare responsibility map](../../docu/moware-werkbank.md#wo-gehört-eine-änderung-hin).
- The shipped solution `org.modellwerkstatt.dataux.tests` supplies the stable examples recorded in [references/sandbox.md](references/sandbox.md). It is useful but does not cover every UI shape.
- Never persist a project path, editor-session state, or references from an application project.
- Conventions are referenced by name, e.g. conventions `oberflaeche`; the project provides them (see its `AGENTS.md`). This skill does not repeat their content.
- For target-model classifiers, properties, commands, the `OFXConfig`, and reusable UI roots, replace the explicit `TARGET_MODEL.*` placeholders immediately before insertion.

## Critical rules

- Use MPS MCP tools; never read or edit raw `.mps` / `.mpl` XML (rule and fallback: [`MPS_AGENT_GUIDE.md`](../../MPS_AGENT_GUIDE.md#never-read-raw-mps-model-files)).
- Query concepts with `mps_mcp_get_concept_details` and `l:64adc67c-5fcf-45f5-82db-6a6771963d93:org.modellwerkstatt.dataux`, not the module-style reference; `languageRefs` also takes the plain language name, and one `languageRefs` call with `detail="shape"` replaces per-concept calls. Enum literals (e.g. `OFXRunCmdPage.boundObjectType`): `mps_mcp_query_structure` `GET_ENUMERATION_LITERALS`, whose `enumerationRef` takes the qualified enum name. Never write an empty enum value `""`; omit the property.
- Use the `qualifiedName` as `concept` in blueprints (`moai:mps-mcp-workflow`, `references/node-editing-rules.md`).
- `PagePane.uxChild` is exactly one (`1`); composition with `GridLayout`/`TabLayout`: see [Page Panes](../../docu/dataux.md#page-panes).
- Binding does not load data: see [Datenbindung und Selektion](../../docu/dataux.md#datenbindung-und-selektion) and [Explizites Laden](../../docu/manmap.md#explizites-laden).
- Table binding (`boundClassifier` = list owner, `boundProperty` = list property, delegates on the row type; typed-only tables only as top element or in a first-level layout; no Value Object lists): see [Tabellenbindung und Selektion](../../docu/dataux.md#tabellenbindung-und-selektion) and [gotchas](references/gotchas.md#owning-classifier-list-property-and-row-type-differ).
- Prefer a root skeleton followed by surgical `ADD CHILD` operations for large or uncertain roots. Preserve existing node IDs.
- Before writing, search the blueprint text for `TARGET_`; every hit stops the write. The dry-run checks concepts, roles, and assignability only: it does not look up names ("is a name, not looked up" is expected for every plain name) and runs no node factories. After the real write, `fixReferences.stillBroken` must be 0; then run `mps_mcp_check_root_node_problems` on the changed root, or on the model reference with `perRoot=true` after work on several roots. Generate or build when the task requires it.
- Inner forms, tables, and layouts stay unnamed (`isNamed = false`, `name = "#"`); JSON insertion sets exactly that for inner elements and names only roots, and explicit values in a blueprint are kept. Name an element only when it is a root reused with `Include`. See [inner UI elements](references/gotchas.md#inner-ui-elements-must-stay-unnamed).
- Node factories run on every real insert and fill only the roles a blueprint omits; a named role, even an empty `{"role":"options","nodes":[]}`, replaces the factory content. A `DelegateForm` that is not a direct PagePane child, and a root `DelegateForm` or `Table`, get a factory `LabelFOption` unless `options` is named: see [node factories](references/gotchas.md#node-factories).
- `OPTIONAL`, `LENGTH`/`RANGE`, empty input and `null`: see [Pflichtwerte, leere Eingaben und `null`](../../docu/dataux.md#pflichtwerte-leere-eingaben-und-null).
- Main table action with hotkey `ENTER` (double-click/Enter): see [Menüs und Command-Aktionen](../../docu/dataux.md#menüs-und-command-aktionen); placement: conventions `oberflaeche`.
- Module placement and the location of the referenced `OFXConfig`: conventions `anwendungsaufbau`. Both module kinds require `configuration`, `isAuthenticated`, and one `VERSION`; a `BatchJob Module` additionally requires an exception strategy ending with a default rule and exactly one `CONSUMERS` per pair with a consumer. Never create `onStartup`/`onShutdown`. See [module gotchas](references/gotchas.md#modules-need-a-configuration-and-a-version) and [executable modules](../../docu/dataux.md#teil-ii--anwendung-und-batchjob).
- Keep business rules out of UI expressions. DataUX should remain presentation-oriented “CheapCode”; see the [MoWare development principles](../../docu/moware-werkbank.md#grundprinzipien-für-die-anwendungsentwicklung).

## Quick start

1. Pass `projectPath` in every call. If it is unknown, use the current directory on the first call, take the path from the rejection, and reuse it; if the project list is empty, ask the user to open the project (`moai:mps-mcp-workflow`, "Which project the tools act on").
2. Resolve the destination model and inspect its used languages and dependencies with `mps_mcp_get_project_structure`.
3. Load [references/concepts.md](references/concepts.md), then select the relevant recipe in [references/workflows.md](references/workflows.md).
4. Inspect a stable package example from [references/sandbox.md](references/sandbox.md) when its shape matches the task. Use application models only as transient evidence and never retain their names or references.
5. Start from [references/blueprints/](references/blueprints/). Replace every `TARGET_MODEL.*` value with a name or persistent node reference resolved in the destination model, then search the text for `TARGET_`; every hit stops.
6. Send the blueprint inline (up to 4 KB; every shipped blueprint fits minified) or copy it to `${TMPDIR:-/tmp}` and pass the absolute path of the copy; files under `skills/` are rejected by the server.
7. Dry-run roots with `mps_mcp_insert_root_node_from_json`; dry-run subtrees with `mps_mcp_update_node` using `ADD CHILD`. Name warnings are expected; factories do not run in the dry-run.
8. Insert the skeleton, add non-trivial subtrees incrementally, and use surgical updates for later edits. After each real write `fixReferences.stillBroken` must be 0; `mps_mcp_print_node` the result where a node factory acts ([node factories](references/gotchas.md#node-factories)).
9. Review every changed root against the applicable conventions. A shape copied from a blueprint, a packaged example, or the project itself does not prove compliance.
10. Run `mps_mcp_check_root_node_problems` on the changed root, or on the model reference with `perRoot=true` after work on several roots. Read `warnings`, `details.uncheckedSubtrees`, and each problem's `rules[].statement`; apply offered `quickFixes` with `autoApplyQuickFixes=true` (node/root references) or `mps_mcp_list_node_intentions` / `mps_mcp_apply_intention`. Repair references with `mps_mcp_alter_nodes FIX_REFERENCES` only when `stillBroken` stays above 0, and perform the task-required make/generation checks.

## Stable package references

- Language module: `64adc67c-5fcf-45f5-82db-6a6771963d93(org.modellwerkstatt.dataux)`
- Concept-tools language ref: `l:64adc67c-5fcf-45f5-82db-6a6771963d93:org.modellwerkstatt.dataux`
- Structure model: `r:29bd6c27-4b8b-45de-826b-b6e588367a39(org.modellwerkstatt.dataux.structure)`
- Runtime solution: `bd230cc8-9f23-4d08-88ae-92ff30662c34(org.modellwerkstatt.dataux.runtime)`
- Shipped examples/tests solution: `3c6ef8ca-6366-4c8b-8839-0277eaca1f7e(org.modellwerkstatt.dataux.tests)`

The shipped examples solution may be globally visible instead of belonging to the selected project's dependency closure. Resolve it explicitly or use `includeStubModules=true`, and treat it as read-only unless the task explicitly targets it.

## Related DSL skills

- Load `moai:objectflow-dsl` when creating or changing the command, page, classifier, property, selection, conclusion, or expressions that a UI references, and for the producer/consumer commands and `OFXConfig` a module references.
- Load `moai:manmap-dsl` when UI data is missing, read-only unexpectedly, or must be loaded/saved differently. DataUX binding is not a persistence mechanism.
- Load `moai:mps-baselanguage` before authoring label, color, formatting, condition, argument, or custom-element expression subtrees.
- Load `moai:mps-node-editing` before inserting or restructuring nodes.

## Documentation map

- [DataUX Page Panes and UI composition](../../docu/dataux.md#page-panes)
- [DataUX binding and shared selection](../../docu/dataux.md#datenbindung-und-selektion)
- [Forms, tables, delegates, and options](../../docu/dataux.md#formulare-tabellen-und-delegates)
- [Layouts, tabs, includes, and custom elements](../../docu/dataux.md#layouts-tabs-und-wiederverwendung)
- [Menus and command actions](../../docu/dataux.md#menüs-und-command-aktionen)
- [Typical UI modeling workflow](../../docu/dataux.md#typischer-ui-modellierungsablauf)
- [AppUI Module: navigation, tiles, isAuthenticated](../../docu/dataux.md#anwendung-mit-appui-module)
- [BatchJob Module: pairs, options, exception strategy](../../docu/dataux.md#batchjob-mit-batchjob-module)
- [ObjectFlow Pages and Page Conclusions](../../docu/objectflow.md#pages-und-page-conclusions)
- [MoWare DSL interaction](../../docu/moware-werkbank.md#zusammenspiel-der-dsls)

## References

- [Concepts and verified AST roles](references/concepts.md)
- [Packaged examples and provenance rules](references/sandbox.md)
- [Creation and editing workflows](references/workflows.md)
- [Gotchas and diagnostics](references/gotchas.md)
- [Blueprint index and placeholder contract](references/blueprints.md)
