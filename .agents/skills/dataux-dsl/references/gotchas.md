# Gotchas and diagnostics

## Binding is not loading

A reference or list can be structurally bindable while still absent at runtime. Load the necessary graph in ObjectFlow/ManMap before the Page is displayed; DataUX performs no lazy loading. [PagePane data responsibility](../../../../docu/dataux.md#page-panes), [ManMap loading rules](../../../../docu/manmap.md#modellierungsumfang-und-ausdrucksmöglichkeiten)

## Owner type, property, and row type differ

For a table over `Owner.items`, use `Owner` as `boundClassifier`, `items` as `boundProperty`, and row-type properties inside delegates. Confusing these three layers can pass structural checks while producing a wrong or empty UI. [Table binding](../../../../docu/dataux.md#tabellenbindung-und-selektion)

## Shared selection is type-wide

Tables with the same row type share a selection inside one PagePane. Matching is based on the same runtime instance, not merely equal IDs or business equality. A form bound only to that type goes blank when no instance is selected. [Table selection](../../../../docu/dataux.md#tabellenbindung-und-selektion), [empty selection](../../../../docu/dataux.md#leere-selektion)

## Root auto-selection is narrow

One root instance, or a root list containing exactly one instance, is automatically selected. A nested list with one element is not automatically selected merely because of its size. Use `SELECT FIRST` when that behavior is desired. [Type binding](../../../../docu/dataux.md#typbindung)

## Tables reject Value Object lists semantically

The raw descriptor exposes generic classifier/property references, but DataUX table semantics require a list of Entities or DTOs. Do not infer semantic validity from assignable reference targets alone. [Table binding restriction](../../../../docu/dataux.md#tabellenbindung-und-selektion)

## Required children are easy to miss

- `PagePane.uxChild`: exactly one.
- `DelegateForm.colWeights`: one or more.
- `GridLayout.uxChild`: one or more.
- `TabLayout.tabs`: one or more.
- `Tab.label` and `Tab.uxChild`: exactly one each.
- Typed delegate `boundTo`: exactly one; `DummyDelegate` is the exception.
- `ReferenceDelegate.scopeText`: exactly one, containing one or more paths.
- `Include.uxElement`: exactly one reference.

The documentation explains the composition semantics; the live descriptors are authoritative for cardinality. [UI composition](../../../../docu/dataux.md#kapitellandkarte-ui-komposition), [delegates](../../../../docu/dataux.md#kapitellandkarte-delegates)

## Include does not isolate context

Include reuses a bindable element. It creates neither new data nor a separate selection scope. A binding override changes the context deliberately; a local menu can override the reused element's menu at that usage site. [Include behavior](../../../../docu/dataux.md#layouts-tabs-und-wiederverwendung)

## Menus run in the current UI context

Table actions usually need the selected row; PagePane actions usually need the root/page context. Verify the exact selection type before building command arguments. Command defaults, permissions, and `generally enabled` remain active even when the DataUX action has no explicit arguments. [Menu action context](../../../../docu/dataux.md#menüs-und-command-aktionen), [ObjectFlow command availability](../../../../docu/objectflow.md#aufbau-eines-commands)

## Compound actions are not ordinary action chains

`MenuCompoundAction` coordinates Graph Owner/Edit calls and optional automatic conclusions in a shared session. Every referenced conclusion must exist on its Command. Treat `USER_CANCEL` explicitly when it should continue the chain. [Compound action semantics](../../../../docu/dataux.md#menüs-und-command-aktionen), [ObjectFlow command types](../../../../docu/objectflow.md#die-vier-command-typen)

## Disabled UI is not business validation

Delegate/form options govern presentation and editability. Put business invariants, calculations, and meaningful validation in ObjectFlow domain structures, services, or Commands. [Delegate responsibility](../../../../docu/dataux.md#formulare-tabellen-und-delegates), [MoWare development principles](../../../../docu/moware-werkbank.md#grundprinzipien-für-die-anwendungsentwicklung)

## Read-only provenance matters

A UI can display read-only Entities or DTO projections but cannot safely treat them as editable merely because their shape matches an Entity. Trace their repository/session origin before changing UI editability. [Read-only versus editing](../../../../docu/moware-werkbank.md#grundprinzipien-für-die-anwendungsentwicklung), [ManMap session identity](../../../../docu/manmap.md#read-only-checkout-und-session-identität)

## Layouts are runtime-sensitive

A wide desktop grid may be unsuitable for mobile or MDE devices. Model alternative PagePanes and let ObjectFlow PagePane links select by condition, with an unconditional default last. [Target-device guidance](../../../../docu/dataux.md#layouts-tabs-und-wiederverwendung), [multiple PagePanes](../../../../docu/objectflow.md#mehrere-page-panes)

## Custom element integration is conditional

`CustomElement` requires an implementation-class expression. Menu visibility/support depends on the concrete UI runtime component. Keep domain binding, delegates, and actions in DataUX and limit custom code to presentation. [Custom element semantics](../../../../docu/dataux.md#layouts-tabs-und-wiederverwendung), [menu runtime caveat](../../../../docu/dataux.md#menüs-und-command-aktionen)

## Reference and blueprint safety

- Use fully qualified concept names.
- Use `r:` node references or deliberately resolvable names for reference targets; never put a `c:` concept reference into a node-reference role.
- Replace every `TARGET_MODEL.*` placeholder before insertion.
- Never copy persistent references from an application model.
- Expect dry-run warnings for unresolved names; do not treat them as harmless without a resolution plan.
- Validate the finished root even when insertion returned `ok: true`.

## Partially documented concepts

Some live UI concepts/options are absent from the documentation's detailed tables or have no complete runtime contract there. Do not infer behavior from their names. See the explicit entries in [problems.md](problems.md).
