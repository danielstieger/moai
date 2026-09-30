# Blueprint index and placeholder contract

All files use the unified MPS JSON blueprint format and fully qualified concept names. They are portable structural templates, not self-contained application models.

## Placeholder contract

Every JSON string beginning with `TARGET_MODEL.` is intentionally unresolved and must be replaced in the destination model immediately before dry-run/insertion. The qualified form deliberately avoids ambiguity with MPS XML short IDs.

| Placeholder | Required destination target |
| --- | --- |
| `TARGET_MODEL.RootClassifier` | ObjectFlow Entity/DTO used as the PagePane root binding |
| `TARGET_MODEL.textProperty` | Direct text property of the current binding type |
| `TARGET_MODEL.TableOwnerClassifier` | Classifier owning the table's list property |
| `TARGET_MODEL.items` | Entity/DTO list property shown by the table |
| `TARGET_MODEL.RowClassifier` | Entity/DTO element type of the table list |
| `TARGET_MODEL.rowText` | Displayed property of the table row type |
| `TARGET_MODEL.detail` | Property displayed in the detail form |
| `TARGET_MODEL.nestedObject` | Direct property used as the left side of a nested path |
| `TARGET_MODEL.nestedText` | Property reached after the path dot |
| `TARGET_MODEL.referenceProperty` | Entity-typed property selected by a reference delegate |
| `TARGET_MODEL.targetTypeProperty` | Property of the referenced type shown as the choice text |
| `TARGET_MODEL.ReusableUiRoot` | Bindable DataUX root referenced by Include |
| `TARGET_MODEL.Command` | ObjectFlow Command referenced by a menu action |

Prefer persistent `r:` references when the destination target has been resolved uniquely. Plain names are acceptable only when they are unambiguous in the role's scope.

## Files

- [page-pane-form-skeleton.json](blueprints/page-pane-form-skeleton.json): small complete PagePane root with a single form.
- [table-subtree.json](blueprints/table-subtree.json): table over an owner list property with one column and `SELECT FIRST`.
- [grid-master-detail-subtree.json](blueprints/grid-master-detail-subtree.json): grid containing master table plus row-detail form.
- [tab-layout-subtree.json](blueprints/tab-layout-subtree.json): two tabs, one reusable include and one form.
- [include-subtree.json](blueprints/include-subtree.json): minimal reusable UI reference.
- [menu-submenu-subtree.json](blueprints/menu-submenu-subtree.json): overflow submenu with one command using its ObjectFlow defaults.
- [direct-property-delegate-subtree.json](blueprints/direct-property-delegate-subtree.json): direct property binding path.
- [nested-property-delegate-subtree.json](blueprints/nested-property-delegate-subtree.json): `PathDot` binding path.
- [reference-delegate-subtree.json](blueprints/reference-delegate-subtree.json): reference selection; `scopeText` paths are properties of the referenced type, the choices come from `#Meta.setScope` in the page scope function.

For roots and subtrees above roughly 4 KB, pass the file path to the MPS tool or construct incrementally. Do not paste an oversized JSON string into a tool call.
