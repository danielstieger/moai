# Creation and editing workflows

## Resolve context before editing

1. Call `mps_mcp_list_open_projects`; select the intended target from the user's task or current editor focus.
2. Resolve the destination model with `mps_mcp_get_project_structure`, including dependencies and used languages.
3. Confirm that DataUX, ObjectFlow, and any needed BaseLanguage expressions are available.
4. Resolve every target-model classifier, property, command, conclusion, label, and reusable UI root. Do not carry references across projects.
5. Inspect an existing destination root before editing it; preserve persistent node IDs with surgical operations.

This separation follows the [MoWare ownership map](../../../docu/moware-werkbank.md#wo-gehört-eine-änderung-hin): ObjectFlow owns use-case state/control flow, ManMap owns loading/persistence, and DataUX owns presentation.

## Create a PagePane with a form

1. Identify the ObjectFlow Page's bound Entity/DTO and ensure Page Init returns the corresponding object. [Page Init and data preparation](../../../docu/objectflow.md#page-init-und-datenbereitstellung)
2. Copy [page-pane-form-skeleton.json](blueprints/page-pane-form-skeleton.json).
3. Replace `TARGET_MODEL.RootClassifier` and `TARGET_MODEL.textProperty` from the destination model.
4. Adjust the delegate concept to the property's actual type and add only valid options. [Delegate type rules](../../../docu/dataux.md#formulare-tabellen-und-delegates)
5. Dry-run, insert, then link the ObjectFlow Page to the new PagePane in the ObjectFlow model.
6. Validate both the PagePane root and the owning Command root.

Use a direct `DelegateForm` as `uxChild` only when it is the sole visible element. `PagePane.uxChild` has cardinality `1`. [UI composition](../../../docu/dataux.md#kapitellandkarte-ui-komposition)

## Create a table over a list property

1. Ensure the owner object and list are already populated; UI binding never loads them. [Binding does not load](../../../docu/dataux.md#page-panes)
2. Confirm that the list element is an Entity or DTO, not a Value Object. [Table binding restrictions](../../../docu/dataux.md#tabellenbindung-und-selektion)
3. Use [table-subtree.json](blueprints/table-subtree.json).
4. Set `TARGET_MODEL.TableOwnerClassifier` to the classifier owning the list and `TARGET_MODEL.items` to the list property.
5. Set each delegate path to a property of the row type, such as `TARGET_MODEL.rowText`.
6. Add `SelectFirstFOption` only when the first row should initialize the shared row-type selection.
7. Add the subtree under an `uxChild` role, then validate the containing root.

Do not set `boundClassifier` to the row type when `boundProperty` belongs to a different owner. This is a frequent source of misleading bindings.

## Build master-detail UI

1. Decide the page root type, master list property, and row/detail type.
2. Ensure the command loads the complete master/detail graph before showing the Page. [Explicit loading](../../../docu/manmap.md#domänenmodell-laden-bearbeiten-und-speichern)
3. Use [grid-master-detail-subtree.json](blueprints/grid-master-detail-subtree.json).
4. Bind the form to the page root and the table to the owner/list property; one column `1*`, the form row `-1`, the table row `1*`, no left/right split.
5. Keep the table's `LabelFOption` (set the text) unless the table is the Page Pane's top element; keep `SelectFirstFOption` only when an initial selection is desired.
6. Add delegates for both types; give every table delegate a `WidthDOption` (percentages add up to 100).
7. Put the table's actions, including the `ENTER` main action, into one text-less `MenuSub` (see [menu-submenu-subtree.json](blueprints/menu-submenu-subtree.json)). The selected row updates the PagePane-wide selection for its type. [UI conventions](../../../conventions/moware-werkbank-ui_v1.md)
8. Validate behavior for empty lists and cleared selection. [Empty selection](../../../docu/dataux.md#leere-selektion) and [master-detail behavior](../../../docu/dataux.md#master-detail)

## Add tabs

1. Use [tab-layout-subtree.json](blueprints/tab-layout-subtree.json).
2. Keep at least one `Tab`; each Tab requires exactly one label expression and one `uxChild`.
3. Use string literals for static labels or load `moai:mps-baselanguage` for dynamic expressions.
4. Put composite content inside a GridLayout; do not add multiple `uxChild` nodes to one Tab.
5. Validate target-device suitability. Distinct device classes may require distinct PagePanes or conditional PagePane links. [Layouts and target devices](../../../docu/dataux.md#layouts-tabs-und-wiederverwendung) and [multiple PagePanes](../../../docu/objectflow.md#mehrere-page-panes)

## Reuse UI with Include

1. Ensure the reusable target is a declared UI root; roots are typed only (`boundClassifier`, no `boundProperty`).
2. Use [include-subtree.json](blueprints/include-subtree.json).
3. Resolve `TARGET_MODEL.ReusableUiRoot` in the destination model.
4. `boundClassifier` is mandatory on an Include (the checker reports "An include needs to be bound on an object."); add `boundProperty` when the reused element works on a property of the selected object. The content type must match the reused root's type.
5. Remember that Include creates neither data nor an independent selection space. It may override menus at the usage site only when a `Table` is included. [Include semantics](../../../docu/dataux.md#layouts-tabs-und-wiederverwendung)

## Add menus and command actions

1. Determine whether the action belongs to the full PagePane context or a table row context.
2. Resolve the ObjectFlow Command and confirm its required/default parameters, permissions, and enabled conditions. [Command parameters and selection](../../../docu/objectflow.md#parameter-defaults-und-selektion)
3. Start with [menu-submenu-subtree.json](blueprints/menu-submenu-subtree.json) when command defaults are sufficient.
4. Add explicit argument expressions only after resolving the correct selection type; use `getSelected()`/`getSelectedObjects()` deliberately.
5. Use `MenuCompoundAction` only after confirming Graph Owner/Edit and conclusion semantics. [Compound action behavior](../../../docu/dataux.md#menüs-und-command-aktionen)
6. Validate the DataUX root and the referenced Command root.

Put the entries in the text-less `Submenu`, including the `ENTER` main action; actions before submenus, one overflow, top level only (checker). [UI conventions](../../../conventions/moware-werkbank-ui_v1.md), [menu rules](../../../docu/dataux.md#menüs-und-command-aktionen)

## Create an AppUI Module

1. Place the root in the application's `app` model (`<firma>.<app>.app`), the only model that holds `AppUI Module` and `BatchJob Module`. [Model layering](../../../conventions/moware-werkbank-modularisierung_v1.md#solutions-und-modelle)
2. Resolve the `OFXConfig` root in `<firma>.<app>.base` and set it as `TARGET_MODEL.OFXConfig`. `configuration` is always required although only start-ups from MPS, FX8, or standalone use it. [Configuration note](../../../docu/dataux.md#teil-ii--anwendung-und-batchjob)
3. Copy [appui-module-skeleton.json](blueprints/appui-module-skeleton.json); give the module a name without spaces.
4. Replace `TARGET_MODEL.Command` in `mainMenu` and in the tile with the commands the user starts; add one `MenuAction` per entry command to `mainMenu` (business entries), `extrasMenu` (rare functions), or `helpMenu`. Use `MenuSub` for grouping. Module actions have no selection, so give them no `getSelected()` arguments. [Navigation](../../../docu/dataux.md#anwendung-mit-appui-module)
5. Keep `VERSION` (`OptVersion`) and `OFFICIAL NAME` (`OptOfficialAppName`) once each.
6. Dry-run and insert the root. Then replace the body of `isAuthenticated` so that it stores the runtime user name in `userEnvironment` (`userEnvironment.setUserName(...)`) and sets the user id via a service or repository; the body must end with a boolean expression statement. Load `moai:mps-baselanguage` for this subtree. [isAuthenticated](../../../docu/dataux.md#anwendung-mit-appui-module)
7. Optional: add `tileInit` (`TileInitFunction`), tile label/color expressions, or `startup command to run` (`StartupCommandCall` with `commandCall: CommandCallBasis`) with `ADD CHILD`. [Tiles](../../../docu/dataux.md#tiles-und-dynamische-darstellung)
8. Run `mps_mcp_check_root_node_problems` on the module root; also validate the referenced Command roots.

Do not add `onStartup`/`onShutdown`; the checker rejects them.

## Create a BatchJob Module

1. Model the command side first with `moai:objectflow-dsl`: a producer command that finds the work items (usually with a page whose bound list carries the result) and a consumer command that processes one item, typically a `GRAPH_OWNER_CMD`. [Batch concept](../../../docu/dataux.md#batchjob-mit-batchjob-module)
2. Place the root in `<firma>.<app>.app`; reference the `OFXConfig` from `<firma>.<app>.base` as `TARGET_MODEL.OFXConfig`.
3. Copy [batchjob-module-skeleton.json](blueprints/batchjob-module-skeleton.json). Replace `TARGET_MODEL.InboxClassifier` (inbox element type), `TARGET_MODEL.ProducerCommand`, and `TARGET_MODEL.ConsumerCommand`; rename `ExamplePair` consistently in the pair and in the `pair` references of the `CRON` and `CONSUMERS` options.
4. Dry-run and insert the root.
5. Add the inbox-filling page to the producer's `runCommand.pages` (`OFXRunCmdPage` with `page -> <producer page>`, `name` for the page variable, and `beforeConclude` with `inbox.addAll(<pageVar>.<list>)` built from `OFXRunCmdVarRef` nodes); load `moai:mps-baselanguage` for the statement. Add an `ifClause` precondition to the consumer call context when the item may already be processed. [Inbox rules](../../../docu/dataux.md#batchjob-mit-batchjob-module)
6. Choose the timing per pair: a `CRON` with a concrete second for point-in-time runs, or `DELAY` plus optional `CRON` windows (second `*`) for continuous mode. Exactly one `CONSUMERS` per pair with a consumer; none for a producer-only pair. Use `DEPENDENT_CONSECUTIVE` only with several pairs, with timing options on the first pair only. [Batch options](../../../docu/dataux.md#kapitellandkarte-batchoptionen)
7. Keep the exception strategy's default rule (no `exMatch`) last; put matching rules before it. [Exception strategies](../../../docu/dataux.md#exception-strategien-und-wiederanlauf)
8. For console or one-shot runs do not add `RUN_IN_CONSOLE`; configure `org.modellwerkstatt.objectflow.job.console.ConsoleBatchJobAppFactory` in the `OFXConfig` instead (checker message, see gotchas). Use `OptIncludeBatchUi` on an `AppUiModule` to show the batch job's pages in that application.
9. Run `mps_mcp_check_root_node_problems` on the module root and on the producer/consumer Command roots.

## Choose full-root JSON versus staged construction

- Use a full root only for a small new PagePane whose complete structure is understood.
- Use a skeleton plus `mps_mcp_update_node ADD CHILD` for grids, tab sets, large delegate lists, or menus with expressions.
- Use `SET CHILD`, property updates, or reference updates for existing roots; do not rewrite the entire root for one change.
- Dry-run every non-trivial blueprint. A successful insert does not prove semantic validity.
- After real changes, run `mps_mcp_check_root_node_problems` on each changed root; then generate/build when runtime or generated-code behavior matters.

## Diagnose a UI that shows no or wrong data

1. Check whether Page Init/Command actually supplies and loads the data. [Data preparation](../../../docu/objectflow.md#page-init-und-datenbereitstellung)
2. Check owner classifier versus list property versus row type.
3. Check the shared selection by runtime type and account for an empty selection.
4. Check each delegate path, especially every operand/operation step of a `PathDot`.
5. Check read-only/session provenance if editing unexpectedly fails. [ManMap read-only and session identity](../../../docu/manmap.md#read-only-checkout-und-session-identität)
6. Run MPS validation on both UI and command roots.
