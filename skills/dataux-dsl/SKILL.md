---
name: dataux-dsl
description: "Use when creating, editing, validating, or inspecting MoWare DataUX user interfaces (org.modellwerkstatt.dataux): page panes, forms and input fields (delegates), tables and columns, layouts and tabs, master-detail, binding and selection, menus and actions, application modules (AppUI) and batch jobs."
---

# DataUX UI DSL

DataUX describes the presentation and UI interaction layer of a MoWare application. This skill deliberately covers only the UI-facing part of `org.modellwerkstatt.dataux`: `PagePane`, forms, tables, layouts, binding paths, delegates, reusable includes, and menus. ObjectFlow owns domain meaning, commands, pages, selections, and session behavior; ManMap owns loading and persistence.

## Source authority and portability

- Treat the live `org.modellwerkstatt.dataux` language as the technical authority for concepts, roles, cardinalities, reference targets, and assignability.
- Use the package documentation for semantics and runtime behavior; start with [DataUX UI modeling](../../docu/dataux.md#teil-i--ui-modellierung) and the [MoWare responsibility map](../../docu/moware-werkbank.md#wo-gehört-eine-änderung-hin).
- The shipped solution `org.modellwerkstatt.dataux.tests` supplies the stable examples recorded in [references/sandbox.md](references/sandbox.md). It is useful but does not cover every UI shape.
- Determine the target MPS project dynamically with `mps_mcp_list_open_projects`. Never persist a project path, editor-session state, or references from an application project.
- For target-model classifiers, properties, commands, conclusions, labels, and reusable UI roots, replace the explicit `TARGET_MODEL.*` placeholders immediately before insertion.

## Critical rules

- Use MPS MCP tools; never read or edit serialized `.mps` or `.mpl` XML.
- Query concepts with `mps_mcp_get_concept_details` and `l:64adc67c-5fcf-45f5-82db-6a6771963d93:org.modellwerkstatt.dataux`, not the module-style reference.
- Use fully qualified concept names in JSON blueprints.
- A `PagePane` has exactly one `uxChild`. Use a `GridLayout` or `TabLayout` to compose several elements. See [UI composition](../../docu/dataux.md#kapitellandkarte-ui-komposition).
- Binding never loads data. Ensure the ObjectFlow command/repository has already supplied the full data needed by the UI. See [binding and selection](../../docu/dataux.md#datenbindung-und-selektion) and [explicit graph loading](../../docu/manmap.md#modellierungsumfang-und-ausdrucksmöglichkeiten).
- A table over a list property binds `boundClassifier` to the property owner and `boundProperty` to that list property; its delegates address properties of the row type. Lists of Value Objects are not valid DataUX table models. See [table binding](../../docu/dataux.md#tabellenbindung-und-selektion).
- Prefer a root skeleton followed by surgical `ADD CHILD` operations for large or uncertain roots. Preserve existing node IDs.
- Dry-run JSON first and inspect warnings. After a real change, run `mps_mcp_check_root_node_problems` on each changed root; generate or build when the task requires it.
- Inner forms, tables, and layouts need `isNamed = false` and `name = "#"`; JSON insertion sets `isNamed = true`. Name an element only when it is reused with `Include`. See [inner UI elements](references/gotchas.md#inner-ui-elements-must-stay-unnamed).
- Do not put `OPTIONAL` on a `StringDelegate` (it yields `null` instead of `""`); control required strings with `LENGTH` and do not repeat `LENGTH`/`RANGE` limits as `validation`. See [required values](../../docu/dataux.md#pflichtwerte-leere-eingaben-und-null).
- Keep business rules out of UI expressions. DataUX should remain presentation-oriented “CheapCode”; see the [MoWare development principles](../../docu/moware-werkbank.md#grundprinzipien-für-die-anwendungsentwicklung).

## Quick start

1. Call `mps_mcp_list_open_projects` and select the intended target dynamically. If several projects remain plausible, ask the user.
2. Resolve the destination model and inspect its used languages and dependencies with `mps_mcp_get_project_structure`.
3. Load [references/concepts.md](references/concepts.md), then select the relevant recipe in [references/workflows.md](references/workflows.md).
4. Inspect a stable package example from [references/sandbox.md](references/sandbox.md) when its shape matches the task. Use application models only as transient evidence and never retain their names or references.
5. Start from [references/blueprints/](references/blueprints/). Replace every `TARGET_MODEL.*` value with a name or persistent node reference resolved in the destination model.
6. Dry-run roots with `mps_mcp_insert_root_node_from_json`; dry-run subtrees with `mps_mcp_update_node` using `ADD CHILD`.
7. Insert the skeleton, add non-trivial subtrees incrementally, and use surgical updates for later edits.
8. Run `mps_mcp_check_root_node_problems` on each changed root, repair resolvable references if needed, and perform the task-required make/generation checks.

## Stable package references

- Language module: `64adc67c-5fcf-45f5-82db-6a6771963d93(org.modellwerkstatt.dataux)`
- Concept-tools language ref: `l:64adc67c-5fcf-45f5-82db-6a6771963d93:org.modellwerkstatt.dataux`
- Structure model: `r:29bd6c27-4b8b-45de-826b-b6e588367a39(org.modellwerkstatt.dataux.structure)`
- Runtime solution: `bd230cc8-9f23-4d08-88ae-92ff30662c34(org.modellwerkstatt.dataux.runtime)`
- Shipped examples/tests solution: `3c6ef8ca-6366-4c8b-8839-0277eaca1f7e(org.modellwerkstatt.dataux.tests)`

The shipped examples solution may be globally visible instead of belonging to the selected project's dependency closure. Resolve it explicitly or use `includeStubModules=true`, and treat it as read-only unless the task explicitly targets it.

## Related DSL skills

- Load [ObjectFlow DSL](../objectflow-dsl/SKILL.md) when creating or changing the command, page, classifier, property, selection, conclusion, or expressions that a UI references.
- Load [ManMap DSL](../manmap-dsl/SKILL.md) when UI data is missing, read-only unexpectedly, or must be loaded/saved differently. DataUX binding is not a persistence mechanism.
- Load `mps-baselanguage` before authoring label, color, formatting, condition, argument, or custom-element expression subtrees.
- Load `mps-node-editing` before inserting or restructuring nodes.

## Documentation map

- [DataUX Page Panes and UI composition](../../docu/dataux.md#page-panes)
- [DataUX binding and shared selection](../../docu/dataux.md#datenbindung-und-selektion)
- [Forms, tables, delegates, and options](../../docu/dataux.md#formulare-tabellen-und-delegates)
- [Layouts, tabs, includes, and custom elements](../../docu/dataux.md#layouts-tabs-und-wiederverwendung)
- [Menus and command actions](../../docu/dataux.md#menüs-und-command-aktionen)
- [Typical UI modeling workflow](../../docu/dataux.md#typischer-ui-modellierungsablauf)
- [DataUX diagnostics](../../docu/dataux.md#häufige-fehler-und-diagnose)
- [ObjectFlow Pages and Page Conclusions](../../docu/objectflow.md#pages-und-page-conclusions)
- [MoWare DSL interaction](../../docu/moware-werkbank.md#zusammenspiel-der-dsls)

## References

- [Concepts and verified AST roles](references/concepts.md)
- [Packaged examples and provenance rules](references/sandbox.md)
- [Creation and editing workflows](references/workflows.md)
- [Gotchas and diagnostics](references/gotchas.md)
- [Blueprint index and placeholder contract](references/blueprints.md)
