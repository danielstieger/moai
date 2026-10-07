# Gotchas and diagnostics

## Binding is not loading

A reference or list can be structurally bindable while still absent at runtime. Load the necessary graph in ObjectFlow/ManMap before the Page is displayed; DataUX performs no lazy loading. [PagePane data responsibility](../../../docu/dataux.md#page-panes), [ManMap loading rules](../../../docu/manmap.md#explizites-laden)

## Owning classifier, list property, and row type differ

For a table over `Rechnung.positionen`, use `Rechnung` as `boundClassifier`, `positionen` as `boundProperty`, and row-type (`Rechnungsposition`) properties inside delegates. Confusing these three layers can pass structural checks while producing a wrong or empty UI. [Table binding](../../../docu/dataux.md#tabellenbindung-und-selektion)

## Shared selection is type-wide

Tables with the same row type share a selection inside one PagePane. Matching is based on the same runtime instance, not merely equal IDs or business equality. A form bound only to that type goes blank when no instance is selected. [Table selection](../../../docu/dataux.md#tabellenbindung-und-selektion), [empty selection](../../../docu/dataux.md#leere-selektion)

## Root auto-selection is narrow

One root instance, or a root list containing exactly one instance, is automatically selected. A nested list with one element is not automatically selected merely because of its size. Use `SELECT FIRST` when that behavior is desired. [Type binding](../../../docu/dataux.md#typbindung)

## Tables reject Value Object lists semantically

The raw descriptor exposes generic classifier/property references, but DataUX table semantics require a list of Entities or DTOs. Do not infer semantic validity from assignable reference targets alone. [Table binding restriction](../../../docu/dataux.md#tabellenbindung-und-selektion)

## Required children are easy to miss

- `PagePane.uxChild`: exactly one.
- `DelegateForm.colWeights`: one or more.
- `DelegateForm.delegates` and `Table.delegates`: at least one; the checker reports "At least one delegate is necessary in a DelegateForm" / "… in a Table."
- `GridLayout.uxChild`: one or more.
- `TabLayout.tabs`: one or more.
- `Tab.label` and `Tab.uxChild`: exactly one each.
- Typed delegate `boundTo`: exactly one; `DummyDelegate` is the exception.
- `ReferenceDelegate.scopeText`: exactly one, containing one or more paths.
- `Include.uxElement`: exactly one reference.

The documentation explains the composition semantics; the live descriptors are authoritative for cardinality. [UI composition](../../../docu/dataux.md#kapitellandkarte-ui-komposition), [delegates](../../../docu/dataux.md#kapitellandkarte-delegates)

## Include does not isolate context

Include reuses a bindable element. It creates neither new data nor a separate selection scope. An Include is always bound (`boundClassifier` mandatory, `boundProperty` optional); roots are typed only, layouts inside a hierarchy carry no binding; local `menuItems` on the Include are allowed only when the target is a `Table` and then override its menu at that usage site. [Include behavior](../../../docu/dataux.md#layouts-tabs-und-wiederverwendung)

## Menus run in the current UI context

Table actions usually need the selected row; PagePane actions usually need the root/page context. Verify the exact selection type before building command arguments. Command defaults, permissions, and `generally enabled` remain active even when the DataUX action has no explicit arguments. [Menu action context](../../../docu/dataux.md#menüs-und-command-aktionen), [ObjectFlow command availability](../../../docu/objectflow.md#aufbau-eines-commands)

## Compound actions are not ordinary action chains

`MenuCompoundAction` coordinates a Graph Owner call (auto-conclusion and `customLabel` mandatory) with an optional Graph Edit call in a shared session. Every referenced conclusion must exist on its Command. `USER_CANCEL` as auto-conclusion ends the command like a user cancel; it never continues the chain. [Compound action semantics](../../../docu/dataux.md#menüs-und-command-aktionen), [ObjectFlow command types](../../../docu/objectflow.md#die-vier-command-typen)

## Disabled UI is not business validation

Delegate/form options govern presentation and editability. Put business invariants, calculations, and meaningful validation in ObjectFlow domain structures, services, or Commands. [Delegate responsibility](../../../docu/dataux.md#formulare-tabellen-und-delegates), [MoWare development principles](../../../docu/moware-werkbank.md#grundprinzipien-für-die-anwendungsentwicklung)

## Read-only provenance matters

A UI can display read-only Entities or DTO projections but cannot safely treat them as editable merely because their shape matches an Entity. Trace their repository/session origin before changing UI editability. [Read-only versus editing](../../../docu/moware-werkbank.md#grundprinzipien-für-die-anwendungsentwicklung), [ManMap session identity](../../../docu/manmap.md#read-only-checkout-und-session-identität)

## Layouts are runtime-sensitive

A wide desktop grid may be unsuitable for mobile or MDE devices. Model alternative PagePanes and let ObjectFlow PagePane links select by condition, with an unconditional default last. [Target-device guidance](../../../docu/dataux.md#layouts-tabs-und-wiederverwendung), [multiple PagePanes](../../../docu/objectflow.md#mehrere-page-panes)

## Custom element integration is conditional

`CustomElement` requires an implementation-class expression. Menu visibility/support depends on the concrete UI runtime component. Keep domain binding, delegates, and actions in DataUX and limit custom code to presentation. [Custom element semantics](../../../docu/dataux.md#layouts-tabs-und-wiederverwendung), [menu runtime caveat](../../../docu/dataux.md#menüs-und-command-aktionen)

## Modules need a configuration and a version

`configuration` is `0..1` in the descriptor, but the checker reports "AppUi Module needs a configuration." / "BatchJob Module needs a configuration." Likewise one `VERSION` option is required: "Sepcify a version option for this app module." (sic, both modules). The `OFXConfig` lives in `<firma>.<app>.base`. [Executable modules](../../../docu/dataux.md#teil-ii--anwendung-und-batchjob)

## Module options are single-use

`IModuleOption` rule: "Use this option only once per module." Do not duplicate `VERSION`, `OFFICIAL NAME`, or `DEPENDENT_CONSECUTIVE`. Pair-scoped options (`CRON`, `DELAY`, `CONSUMERS`) are additionally checked per pair, see below.

## Module startup and shutdown hooks are rejected

`onStartup`/`onShutdown` still exist structurally; the checker reports "OnStartup() is no longer supported. Please remove the function." and "OnShutdown() is no longer supported. Please remove the function." Never create them from JSON. [Deprecated areas](../../../docu/dataux.md#teil-ii--anwendung-und-batchjob)

## Module actions have no selection

Menu and tile actions of a module run outside any PagePane. Arguments that use selections fail with "Parameters given for this action are not correct. (Selections are not available)". Rely on command defaults or pass constants/expressions without `getSelected()`.

## CONSUMERS is per pair, exactly once

"There is exactly one CONSUMERS option needed per producer/consumer pair." and, for a producer-only pair, "Do not specify any CONSUMERS for this producer/consumer pair - it does not have any." Each `CONSUMERS`, `CRON`, and `DELAY` option references its pair explicitly; with several pairs assign them deliberately. [Batch options](../../../docu/dataux.md#kapitellandkarte-batchoptionen)

## CRON shape depends on the pair mode

- With a `DELAY` option the pair is in continuous mode; crons must be windows (second `*`): "The pair is in continous/delay mode, specify cron windows only."
- Without `DELAY` the pair needs at least one time-specific cron (concrete second): "Need more or one specific cron when not in continous/delay mode" and "The pair is in not in continous/delay mode, use only time specific crons."
- At most one `DELAY` per pair: "There can be at most one DELAY option provided per producer/consumer pair."

[Operating modes](../../../docu/dataux.md#kapitellandkarte-batchoptionen)

## DEPENDENT_CONSECUTIVE needs several pairs and silent followers

"DEPENDENT_CONSECUTIVE can only be used, if more than one consumer/producer pair is present." Only the first pair carries timing options; later pairs trigger "Do not specify any timing options for this pair in dependent mode."

## Exception strategy ends with one default rule

"A exception strategy should have a default behaviour without 'matches' as last strategy." and "There should be only one default strategy defined without exception name 'match'." Put `OFXStrategyForException` members with `exMatch` first and exactly one member without `exMatch` last. [Exception strategies](../../../docu/dataux.md#exception-strategien-und-wiederanlauf)

## RUN_IN_CONSOLE is deprecated by the checker

`OptRunInConsole` yields "No longer supported. Just use the 'org.modellwerkstatt.objectflow.job.console.ConsoleBatchJobAppFactory' in your configuration." The documentation still lists `RUN_IN_CONSOLE`; configure the console factory in the `OFXConfig` instead. `OptIncludeBatchUi` is checked with "The included job is not a batchjob containg relevant commands." when the referenced job has no commands with pages.

## Module names without spaces

`check_IModule` warns: "It's strongly recommended to use identifiers/names without spaces here (Typically '_' is used instead of spaces)."

## Reference and blueprint safety

- Use fully qualified concept names.
- Use `r:` node references or deliberately resolvable names for reference targets; never put a `c:` concept reference into a node-reference role.
- Replace every `TARGET_MODEL.*` placeholder before insertion.
- Never copy persistent references from an application model.
- Expect dry-run warnings for unresolved names; do not treat them as harmless without a resolution plan.
- Validate the finished root even when insertion returned `ok: true`.

## Inner UI elements must stay unnamed

`DelegateForm`, `Table`, `GridLayout`, `TabLayout`, and `CustomElement` inside a PagePane must have `isNamed = false` and `name = "#"`. JSON insertion leaves `isNamed = true` even though the concept constructor sets `false`, so always set both explicitly; the blueprints do. The checker error "optionally named component is not used anywhere … remove name" means: set `isNamed = false`. Do not clear the name; an empty name crashes the generator. Name an element only when it is reused with `Include`. [Include](../../../docu/dataux.md#layouts-tabs-und-wiederverwendung)

## Partially documented concepts

Some live UI concepts/options are absent from the documentation's detailed tables or have no complete runtime contract there. Do not infer behavior from their names; verify them against a focused package example before use.
