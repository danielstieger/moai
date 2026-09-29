# Packaged examples and provenance rules

## Stable packaged source

The following examples are part of the shipped solution `org.modellwerkstatt.dataux.tests` (`3c6ef8ca-6366-4c8b-8839-0277eaca1f7e(org.modellwerkstatt.dataux.tests)`) and may be cited and inspected.

Model: `r:04e6a6ad-5d6d-449f-aceb-0afb0d6dad9e(org.modellwerkstatt.objectflow.tests.OrderDocumentUi)`

- `MainDocPP`: `r:04e6a6ad-5d6d-449f-aceb-0afb0d6dad9e(org.modellwerkstatt.objectflow.tests.OrderDocumentUi)/8255348026214777103`
  - Verified composition: `PagePane -> GridLayout -> DelegateForm + Table`.
  - Useful for required grid/form weights, direct and nested property paths, a table bound through a list property, `SELECT FIRST`, labels, and a submenu action.
- `CasesPP`: `r:04e6a6ad-5d6d-449f-aceb-0afb0d6dad9e(org.modellwerkstatt.objectflow.tests.OrderDocumentUi)/1729845510732620937`
  - Verified composition: `PagePane -> Table` with ordinary and compound menu actions.
  - Useful for `MenuCompoundAction`, `PageConclusionReference`, selected-object arguments, and table menus.

Both roots resolved and passed `mps_mcp_check_root_node_problems` when this skill was generated. Re-check before relying on them after a package upgrade.

These examples illustrate shape, not universal domain semantics. Interpret them through [DataUX UI modeling](../../../docu/dataux.md#teil-i--ui-modellierung) and the [ObjectFlow Page lifecycle](../../../docu/objectflow.md#pages-und-page-conclusions).

## Coverage limits

The shipped tests do not provide representative roots for every UI construct. In particular, no packaged `TabLayout`, `Include`, or `CustomElement` instance was found during generation. Portable blueprints for tabs and includes were therefore derived from live language descriptors plus anonymized structural observations. They contain no application model names, identifiers, or persistent references.

Do not cite or persist references from non-package application models. If a task requires a shape absent from the packaged examples:

1. Inspect a suitable target/application node transiently with `mps_mcp_print_node`.
2. Retain only the generalized concept/role structure.
3. Replace every name and reference with a neutral value or a `TARGET_MODEL.*` placeholder.
4. Re-check all roles and cardinalities against the live language descriptors.
5. Validate the resulting node in the actual destination model.

## Verification protocol

1. Determine the target MPS project dynamically.
2. Resolve the packaged solution or model explicitly; use `includeStubModules=true` if needed.
3. Shallow-print the chosen root first.
4. Deep-print only the subtree needed for the task.
5. Re-query concept details for required roles/cardinalities.
6. Never use a packaged example's domain references as insertion values in another model.
