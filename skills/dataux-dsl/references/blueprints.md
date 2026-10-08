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
| `TARGET_MODEL.rowText` | Displayed property of the table row type |
| `TARGET_MODEL.nestedObject` | Direct property used as the left side of a nested path |
| `TARGET_MODEL.nestedText` | Property reached after the path dot |
| `TARGET_MODEL.referenceProperty` | Entity-typed property selected by a reference delegate |
| `TARGET_MODEL.targetTypeProperty` | Property of the referenced type shown as the choice text |
| `TARGET_MODEL.ReusableUiRoot` | Bindable DataUX root referenced by Include |
| `TARGET_MODEL.Command` | ObjectFlow Command referenced by a menu action |
| `TARGET_MODEL.OFXConfig` | `OFXConfig` root in the application's `<firma>.<app>.base` model, referenced by a module's `configuration` |
| `TARGET_MODEL.InboxClassifier` | Entity/DTO (or key type) of the producer inbox (`OFXProducerContext.keytype`) |
| `TARGET_MODEL.ProducerCommand` | ObjectFlow Command that searches or computes the work items of a pair |
| `TARGET_MODEL.ConsumerCommand` | ObjectFlow Command that processes one inbox element (usually `GRAPH_OWNER_CMD`) |

Prefer persistent `r:` references when the destination target has been resolved uniquely. Plain names are acceptable only when they are unambiguous in the role's scope.

Names without the `TARGET_MODEL.` prefix inside a blueprint (`ExamplePair`, `inbox`, `inboxElement`) are intra-root references to sibling nodes of the same blueprint; keep them consistent when renaming, and check the dry-run warnings for them. Both module blueprints were verified by a real insert into a throwaway model: the only checker problems were placeholder-related (unresolved `configuration`, placeholder command call), while the intra-root name references (`pair`, `varRef`) resolved.

## Files

- [page-pane-form-skeleton.json](blueprints/page-pane-form-skeleton.json): small complete PagePane root with a single form.
- [table-subtree.json](blueprints/table-subtree.json): table over an owner list property with one column, `LABEL` and `SELECT FIRST`. Remove the `LabelFOption` when the table is the Page Pane's top element (its label is the Page Title). [UI conventions](../../../conventions/moware-werkbank-ui_v1.md)
- [grid-master-detail-subtree.json](blueprints/grid-master-detail-subtree.json): compact form (row `-1`) above the list table (row `1*`), one column `1*`, table with `LABEL` and `SELECT FIRST`.
- [tab-layout-subtree.json](blueprints/tab-layout-subtree.json): two tabs, one reusable include and one form.
- [include-subtree.json](blueprints/include-subtree.json): minimal reusable UI reference.
- [menu-submenu-subtree.json](blueprints/menu-submenu-subtree.json): overflow submenu with one command using its ObjectFlow defaults.
- [direct-property-delegate-subtree.json](blueprints/direct-property-delegate-subtree.json): direct property binding path.
- [nested-property-delegate-subtree.json](blueprints/nested-property-delegate-subtree.json): `PathDot` binding path.
- [reference-delegate-subtree.json](blueprints/reference-delegate-subtree.json): reference selection; `scopeText` paths are properties of the referenced type, the choices come from `#Meta.setScope` in the page scope function.
- [appui-module-skeleton.json](blueprints/appui-module-skeleton.json): complete `AppUiModule` root with configuration, minimal `isAuthenticated`, one main-menu action, one tile, `VERSION` and `OFFICIAL NAME`.
- [batchjob-module-skeleton.json](blueprints/batchjob-module-skeleton.json): complete `BatchJobModule` root with configuration, minimal `isAuthenticated`, one producer/consumer pair, `CRON` and `CONSUMERS` for that pair, a default exception strategy (`DELAY_EXECUTION` 60 s), `VERSION` and `OFFICIAL NAME`. The producer's inbox-filling page is not included; add it with `ADD CHILD` on `runCommand.pages`.

For roots and subtrees above the inline limit, pass a file in the system temp directory or construct incrementally (file-path rules: `moai:mps-node-editing`, File-Path Semantics).
