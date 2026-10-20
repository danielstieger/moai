# Gotchas and diagnostics

## Owning classifier, list property, and row type differ

`boundClassifier` is the owner of the list (`Rechnung`), not the row type; `boundProperty` is the list property (`positionen`); delegates address row-type (`Rechnungsposition`) properties. The mix-up passes structural checks. [Tabellenbindung und Selektion](../../../docu/dataux.md#tabellenbindung-und-selektion)

## Tables reject Value Object lists semantically

The descriptor accepts any classifier/property for `boundClassifier`/`boundProperty`; table semantics restrict rows to Entity/DTO lists. Do not infer validity from assignable targets. [Tabellenbindung und Selektion](../../../docu/dataux.md#tabellenbindung-und-selektion)

## Checker-mandatory roles beyond the descriptor

- `DelegateForm.delegates` and `Table.delegates` are `0..n` in the descriptor; the checker reports "At least one delegate is necessary in a DelegateForm" / "… in a Table."

Descriptor cardinalities: see [concepts.md](concepts.md#ui-roots-and-composition) and [delegates](concepts.md#delegates).

## Includes are always bound

An Include is always bound: `boundClassifier` mandatory (checker: "An include needs to be bound on an object."), `boundProperty` optional; local `menuItems` only when the target is a `Table`. Semantics: [Layouts, Tabs und Wiederverwendung](../../../docu/dataux.md#layouts-tabs-und-wiederverwendung)

## Modules need a configuration and a version

`configuration` is `0..1` in the descriptor, but the checker reports "AppUi Module needs a configuration." / "BatchJob Module needs a configuration." Likewise one `VERSION` option is required: "Sepcify a version option for this app module." (sic, both modules). Location of the `OFXConfig`: conventions `anwendungsaufbau`. [Executable modules](../../../docu/dataux.md#teil-ii--anwendung-und-batchjob)

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

`OptRunInConsole` yields "No longer supported. Just use the 'org.modellwerkstatt.objectflow.job.console.ConsoleBatchJobAppFactory' in your configuration." Configure the console factory in the `OFXConfig` instead. `OptIncludeBatchUi` is checked with "The included job is not a batchjob containg relevant commands." when the referenced job has no commands with pages.

## Module names without spaces

`check_IModule` warns: "It's strongly recommended to use identifiers/names without spaces here (Typically '_' is used instead of spaces)."

## Reference and blueprint safety

- Use the `qualifiedName` as `concept` in blueprints (`moai:mps-mcp-workflow`, `references/node-editing-rules.md`).
- Use `r:` node references or deliberately resolvable names for reference targets; never put a `c:` concept reference into a node-reference role. The insert accepts it silently and leaves the reference unresolved; only the checker reports it.
- Replace every `TARGET_MODEL.*` placeholder before insertion, then search the blueprint text for `TARGET_`; every hit stops the write. A dotted `TARGET_MODEL.*` value still draws the dry-run warning "matches no Model.Root", but a placeholder left in a plain-name position does not stand out.
- Never copy persistent references from an application model.
- The dry-run does not look up names: every plain name draws "is a name, not looked up", whether the target exists or not. Resolution is proven only after the real write by `fixReferences {fixed, repointed, stillBroken}` with `stillBroken = 0`; `mps_mcp_alter_nodes FIX_REFERENCES` is the fallback when it stays above 0.
- Validate the finished root even when insertion returned `ok: true`.

## Inner UI elements must stay unnamed

`DelegateForm`, `Table`, `GridLayout`, `TabLayout`, and `CustomElement` inside a PagePane must have `isNamed = false` and `name = "#"`. Inner elements inserted from JSON without these properties get exactly that (verified for `DelegateForm`, `Table`, and `GridLayout`); only roots are named, because the DataUX root factory sets `isNamed = true` when there is no enclosing node. Explicit values in a blueprint are kept; the blueprints set both, which does no harm. The checker error "optionally named component is not used anywhere … remove name" means: set `isNamed = false`. Do not clear the name; an empty name crashes the generator. Name an element only when it is reused with `Include`. [Include](../../../docu/dataux.md#layouts-tabs-und-wiederverwendung)

## Node factories

Node factories run on every real insert with the actual enclosing node; the dry-run does not run them. A factory fills only the roles the blueprint omits. A named role replaces the factory content, even an empty one (`{"role":"options","nodes":[]}`), which suppresses factory children deliberately. `mps_mcp_query_structure` `LIST_CONCEPT_ASPECTS` shows whether a concept has a factory; `mps_mcp_print_node` after the write shows what it added.

- `DelegateForm` without a named `options` role inside a layout or tab, and a root `DelegateForm` or `Table` (the target of an `Include`, no PagePane parent), get a `LabelFOption`. In a `GridLayout` it carries the bound classifier's name, an unasked label; in a `Tab` and on a root the text is empty and the checker reports "Specify some text for this the label." Name `options` on such forms and tables, empty or with a `LabelFOption` with text. The tab and master-detail blueprints do; a form directly under a PagePane gets no label.
- Roots are named (`isNamed = true`); inner elements are not, see [above](#inner-ui-elements-must-stay-unnamed).
- `OFXRunCmdPage` in `runCommand.pages` (or a successor handler) is prefilled: `page` (the command's next page, else its last), `name` (instance name of the first page's bound type), `boundObjectType = boundObject`, and `conclusion` (the last conclusion of that page). Omit these roles for the defaults or name them to override; for a page bound to a list set `boundObjectType = boundList` explicitly and check the result (not verified). `beforeConclude` is never filled.
- `OFXProducerContext.name` defaults to `inbox`, `OFXConsumerContext.name` to `inboxElement`, and `OFXProducerConsumerPair.name` to `A Pair`; set the pair name explicitly, the `pair` references of the options use it.
- `OFXRunCmdSuccessorHandler` references the next unique successor command and adds an `OFXRunCmdPage` when that command has pages.

## Partially documented concepts

Some live UI concepts/options are absent from the documentation's detailed tables or have no complete runtime contract there. Do not infer behavior from their names; verify them against a focused package example before use.
