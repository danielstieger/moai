# Creation and editing workflows

## Resolve context before editing

1. Call `mps_mcp_list_open_projects`; select the intended target from the user's task or current editor focus.
2. Resolve the destination model with `mps_mcp_get_project_structure`, including dependencies and used languages.
3. Confirm that DataUX, ObjectFlow, and any needed BaseLanguage expressions are available.
4. Resolve every target-model classifier, property, command, conclusion, label, and reusable UI root. Do not carry references across projects.
5. Inspect an existing destination root before editing it; preserve persistent node IDs with surgical operations.

This separation follows the [MoWare ownership map](../../../../docu/moware-werkbank.md#wo-gehört-eine-änderung-hin): ObjectFlow owns use-case state/control flow, ManMap owns loading/persistence, and DataUX owns presentation.

## Create a PagePane with a form

1. Identify the ObjectFlow Page's bound Entity/DTO and ensure Page Init returns the corresponding object. [Page Init and data preparation](../../../../docu/objectflow.md#page-init-und-datenbereitstellung)
2. Copy [page-pane-form-skeleton.json](blueprints/page-pane-form-skeleton.json).
3. Replace `TARGET_MODEL.RootClassifier` and `TARGET_MODEL.textProperty` from the destination model.
4. Adjust the delegate concept to the property's actual type and add only valid options. [Delegate type rules](../../../../docu/dataux.md#formulare-tabellen-und-delegates)
5. Dry-run, insert, then link the ObjectFlow Page to the new PagePane in the ObjectFlow model.
6. Validate both the PagePane root and the owning Command root.

Use a direct `DelegateForm` as `uxChild` only when it is the sole visible element. `PagePane.uxChild` has cardinality `1`. [UI composition](../../../../docu/dataux.md#kapitellandkarte-ui-komposition)

## Create a table over a list property

1. Ensure the owner object and list are already populated; UI binding never loads them. [Binding does not load](../../../../docu/dataux.md#page-panes)
2. Confirm that the list element is an Entity or DTO, not a Value Object. [Table binding restrictions](../../../../docu/dataux.md#tabellenbindung-und-selektion)
3. Use [table-subtree.json](blueprints/table-subtree.json).
4. Set `TARGET_MODEL.TableOwnerClassifier` to the classifier owning the list and `TARGET_MODEL.items` to the list property.
5. Set each delegate path to a property of the row type, such as `TARGET_MODEL.rowText`.
6. Add `SelectFirstFOption` only when the first row should initialize the shared row-type selection.
7. Add the subtree under an `uxChild` role, then validate the containing root.

Do not set `boundClassifier` to the row type when `boundProperty` belongs to a different owner. This is a frequent source of misleading bindings.

## Build master-detail UI

1. Decide the page root type, master list property, and row/detail type.
2. Ensure the command loads the complete master/detail graph before showing the Page. [Explicit loading](../../../../docu/manmap.md#domänenmodell-laden-bearbeiten-und-speichern)
3. Use [grid-master-detail-subtree.json](blueprints/grid-master-detail-subtree.json).
4. Bind the table to the owner/list property and the detail form to the row classifier.
5. Keep `SelectFirstFOption` only when an initial detail selection is desired.
6. Add delegates for the master and detail types. The selected table row updates the PagePane-wide selection for its type.
7. Validate behavior for empty lists and cleared selection. [Empty selection](../../../../docu/dataux.md#leere-selektion) and [master-detail behavior](../../../../docu/dataux.md#master-detail)

## Add tabs

1. Use [tab-layout-subtree.json](blueprints/tab-layout-subtree.json).
2. Keep at least one `Tab`; each Tab requires exactly one label expression and one `uxChild`.
3. Use string literals for static labels or load `mps-baselanguage` for dynamic expressions.
4. Put composite content inside a GridLayout; do not add multiple `uxChild` nodes to one Tab.
5. Validate target-device suitability. Distinct device classes may require distinct PagePanes or conditional PagePane links. [Layouts and target devices](../../../../docu/dataux.md#layouts-tabs-und-wiederverwendung) and [multiple PagePanes](../../../../docu/objectflow.md#mehrere-page-panes)

## Reuse UI with Include

1. Ensure the reusable target is a declared bindable UI root.
2. Use [include-subtree.json](blueprints/include-subtree.json).
3. Resolve `TARGET_MODEL.ReusableUiRoot` in the destination model.
4. Omit binding overrides to inherit the surrounding context, or set both override references deliberately.
5. Remember that Include creates neither data nor an independent selection space. It may override menus at the usage site. [Include semantics](../../../../docu/dataux.md#layouts-tabs-und-wiederverwendung)

## Add menus and command actions

1. Determine whether the action belongs to the full PagePane context or a table row context.
2. Resolve the ObjectFlow Command and confirm its required/default parameters, permissions, and enabled conditions. [Command parameters and selection](../../../../docu/objectflow.md#parameter-defaults-und-selektion)
3. Start with [menu-submenu-subtree.json](blueprints/menu-submenu-subtree.json) when command defaults are sufficient.
4. Add explicit argument expressions only after resolving the correct selection type; use `getSelected()`/`getSelectedObjects()` deliberately.
5. Use `MenuCompoundAction` only after confirming Graph Owner/Edit and conclusion semantics. [Compound action behavior](../../../../docu/dataux.md#menüs-und-command-aktionen)
6. Validate the DataUX root and the referenced Command root.

Prefer an overflow submenu. Reserve top-level actions for a small number of unusually important operations. [Menu placement](../../../../docu/dataux.md#menüs-und-command-aktionen)

## Choose full-root JSON versus staged construction

- Use a full root only for a small new PagePane whose complete structure is understood.
- Use a skeleton plus `mps_mcp_update_node ADD CHILD` for grids, tab sets, large delegate lists, or menus with expressions.
- Use `SET CHILD`, property updates, or reference updates for existing roots; do not rewrite the entire root for one change.
- Dry-run every non-trivial blueprint. A successful insert does not prove semantic validity.
- After real changes, run `mps_mcp_check_root_node_problems`; then generate/build when runtime or generated-code behavior matters.

## Diagnose a UI that shows no or wrong data

1. Check whether Page Init/Command actually supplies and loads the data. [Data preparation](../../../../docu/objectflow.md#page-init-und-datenbereitstellung)
2. Check owner classifier versus list property versus row type.
3. Check the shared selection by runtime type and account for an empty selection.
4. Check each delegate path, especially every operand/operation step of a `PathDot`.
5. Check read-only/session provenance if editing unexpectedly fails. [ManMap read-only and session identity](../../../../docu/manmap.md#read-only-checkout-und-session-identität)
6. Run MPS validation on both UI and command roots.
7. Compare with the [DataUX diagnostic checklist](../../../../docu/dataux.md#häufige-fehler-und-diagnose).
