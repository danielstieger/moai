# Concepts and verified AST roles

The technical facts below were verified against the live `org.modellwerkstatt.dataux` runtime descriptors. Re-query with `mps_mcp_get_concept_details` before relying on a feature that is not listed. Semantic rules link directly to the package documentation.

## UI roots and composition

| Concept | Rootable | Required structure | Optional binding/menu structure |
| --- | --- | --- | --- |
| `org.modellwerkstatt.dataux.structure.PagePane` | yes | `uxChild: IUxElement [1]` | `options: IPagePaneOption [0..n]`, `menuItems: IMenuItem [0..n]`, `boundClassifier [0..1]`, `boundProperty [0..1]` |
| `org.modellwerkstatt.dataux.structure.DelegateForm` | yes | `colWeights: LayoutWeight [1..n]` | `delegates: IDelegate [0..n]`, `options: IFOption [0..n]`, binding refs |
| `org.modellwerkstatt.dataux.structure.Table` | yes | no mandatory child at descriptor level | `delegates`, `options`, `menuItems` (`0..n` each), binding refs |
| `org.modellwerkstatt.dataux.structure.GridLayout` | yes | `uxChild: IUxElement [1..n]` | `rowWeights`, `colWeights`, `options` (`0..n`), binding refs (root only; never inside a hierarchy) |
| `org.modellwerkstatt.dataux.structure.TabLayout` | yes | `tabs: Tab [1..n]` | binding refs (root only; never inside a hierarchy) |
| `org.modellwerkstatt.dataux.structure.Tab` | no | `label: Expression [1]`, `uxChild: IUxElement [1]` | none |
| `org.modellwerkstatt.dataux.structure.Include` | no | `uxElement: IBindable [1]` reference, `boundClassifier [1]` (checker-mandatory) | `boundProperty`, `menuItems` (Table targets only), `options` |
| `org.modellwerkstatt.dataux.structure.CustomElement` | yes | `implClassFqName: Expression [1]` | `fullSize`, binding refs, delegates, menus, custom options |

`PagePane` is the visible counterpart of an ObjectFlow Page. ObjectFlow owns data and control flow; DataUX owns layout and menus. A `PagePane` always has one top-level UI element, so combine siblings inside a grid or tabs. [Page Pane semantics and composition](../../../docu/dataux.md#page-panes)

`DelegateForm`, `Table`, `GridLayout`, `TabLayout`, and `CustomElement` may also be declared as reusable roots. `Include` references an already declared bindable UI element and does not create data or a new selection space. [Layouts, tabs, and reuse](../../../docu/dataux.md#layouts-tabs-und-wiederverwendung)

## Binding model

Every bindable concept exposes optional references:

- `boundClassifier -> jetbrains.mps.baseLanguage.structure.Classifier [0..1]`
- `boundProperty -> jetbrains.mps.baseLanguage.structure.Property [0..1]`

Interpret them operationally:

- Classifier-only binding uses the current selection of that Entity/DTO type.
- A root object supplied as exactly one instance is selected automatically; nested single-element lists are not.
- Property binding is evaluated on the current selection of the property's owner type.
- For a table bound to an owner list property, `boundClassifier` names the owner classifier and `boundProperty` names its list property; delegate paths then address row properties.
- The selection is shared per Entity/DTO type across the complete `PagePane` and uses runtime instance identity.
- Data must already be loaded. A UI binding does not trigger repository loading.

See [binding and selection](../../../docu/dataux.md#datenbindung-und-selektion), [table binding](../../../docu/dataux.md#tabellenbindung-und-selektion), and [ObjectFlow Page data preparation](../../../docu/objectflow.md#page-init-und-datenbereitstellung).

## Binding paths

| Concept | Shape | Use |
| --- | --- | --- |
| `DuxLocalPropertyReference` | required `property` reference | Direct property in the current binding context |
| `PathDot` | required `operand: IPath [1]`, `operation: IPathOperation [1]` | Nested property navigation |
| `OperationPropertyReference` | required `property` reference | Ordinary property after a dot |
| `LocalSpecialPropertyReference` | required `property` reference | Direct special/virtual property |
| `OperationSpecialPropertyReference` | required `property` reference | Nested special/virtual property |

Use [direct-property-delegate-subtree.json](blueprints/direct-property-delegate-subtree.json) and [nested-property-delegate-subtree.json](blueprints/nested-property-delegate-subtree.json) as portable path templates. Resolve each property in the target model; do not copy a property reference from another application.

## Delegates

All typed delegates below are non-rootable and implement `IDelegate`. Except for `DummyDelegate`, each has required `boundTo: IPath [1]` and optional `option: IDOption [0..n]`.

| Property kind | Delegate concept | Operational note |
| --- | --- | --- |
| text | `StringDelegate` | Use `ForceNumericEditor` only for deliberately numeric text input. |
| integer | `IntegerDelegate` | Bind only to a compatible integer property. |
| decimal | `BigDecimalDelegate` | Bind to the supported decimal property type. |
| date/time | `DateTimeDelegate` | Full date and time. |
| date part | `DateTimeDateOnlyDelegate` | Date-only editor for a DateTime value. |
| local date | `LocalDateDelegate` | LocalDate value. |
| status | `StatusDelegate` | `StatusLongDescDOption` selects the long description. |
| reference | `ReferenceDelegate` | Additionally requires `scopeText: RefDelegateScopeProps [1]`; that node requires one or more `paths`. |
| image | `ImageDelegate` | Form-only according to the documentation. |
| upload | `UploadDelegate` | Form-only according to the documentation. |
| spacer | `DummyDelegate` | Layout placeholder; it has no `boundTo` role. |

Delegate kind must match the ObjectFlow property type. Delegates control presentation and interaction, not business validation. [Forms, tables, and delegates](../../../docu/dataux.md#formulare-tabellen-und-delegates)

### Delegate options

Common zero-child options are `DisabledDOption`, `PickerDOption`, `IssueUpdateDOption`, `ForceNumericEditor`, `AlternativeDOption`, `WideDOption`, `EditableDOption`, `ImportantDOption`, `StatusLongDescDOption`, `FoldDOption`, `RightAlignDOption`, and `TimeOnlyDOption`.

Options with additional structure:

- `WidthDOption.percent: integer`
- `NumOfLinesDOption.lines: integer`
- `OptionalDOption.text: Expression [0..1]`
- `OverwriteLabelDOption.expression: Expression [1]`
- `OverwriteFormatDOption.expression: Expression [1]`
- `DynColorDOption.func: DynColorConceptFunction [1]`

Apply an option only where its delegate/property context permits it; several constraints are semantic rather than expressible by the raw role type. [Documented delegate options](../../../docu/dataux.md#delegate-optionen)

## Form, table, grid, and page options

- `DisabledFOption`: disable a form.
- `LabelFOption.expression: Expression [1]`: label a form/table.
- `SelectFirstFOption`: initialize table selection with the first row.
- `SelectionSummaryLineFOption.expression: Expression [1]`: summary of selected rows.
- `TableSummaryLineFOption.expression: Expression [1]`: summary of all table rows.
- `TableCustomCsvExportFOption.result: Expression [1]`: custom CSV export result.
- `FlexibleOption`: flexible grid sizing.
- `SkipFocusOption.element -> IUxElement [1]`: move initial focus forward to a later element.
- `ColorPpOption.color: Expression [1]` and `StatusColorPpFOption.path: IPath [1]` are structurally available PagePane options; their complete runtime semantics are not documented, so verify them against a focused package example before use.

See [form and table options](../../../docu/dataux.md#optionen-für-formulare-und-tabellen) and [layout options](../../../docu/dataux.md#layouts-tabs-und-wiederverwendung).

## Layout weights

`MinWeight`, `OneWeight`, `TwoWeight`, `ThreeWeight`, `FourWeight`, and `FiveWeight` are concrete `LayoutWeight` concepts rendered as `-1`, `1*`, `2*`, `3*`, `4*`, and `5*`. `GridLayout` accepts all six; `DelegateForm.colWeights` excludes `MinWeight` semantically. [Layout weight semantics](../../../docu/dataux.md#layouts-tabs-und-wiederverwendung)

## Menus and command actions

| Concept | Verified shape |
| --- | --- |
| `MenuSub` | optional `label: StringLiteral [0..1]`, nested `menuItems: IMenuItem [0..n]` |
| `MenuAction` | required `command -> ObjectFlow Command [1]`, optional `customLabel`, `actualArgument: Expression [0..n]` |
| `MenuCompoundAction` | inherits `MenuAction`; `customLabel` and `graphOwnerAutoCon` checker-mandatory; optional `graphEditCall` (owner must then have exactly one page) and `graphEditAutoCon` (only if the edit command has pages); outer command must be `GRAPH_OWNER_CMD` or `GRAPH_OWNER_CMD(modal)`; successor commands unsupported |
| `PageConclusionReference` | required `pageConclusion -> ObjectFlow PageConclusion [1]` |
| `PageConclusionOptionUserCancel` | auto-conclusion option that ends the command like a user cancel (`cancel`); no continuation |
| `MenuSeparator` | separator marker |

Prefer a submenu/overflow group and keep only exceptional actions at the top level. A table menu normally acts on row selections; a PagePane menu normally acts on the page/root context, but typed `getSelected(...)` may address any type participating in the shared selection. [Menus and command actions](../../../docu/dataux.md#menüs-und-command-aktionen)

Command availability, parameters, permissions, and conclusions remain ObjectFlow concerns. [ObjectFlow command parameters and selection](../../../docu/objectflow.md#parameter-defaults-und-selektion) and [Page Conclusions](../../../docu/objectflow.md#page-conclusions)

## Executable modules

`AppUiModule` and `BatchJobModule` are rootable concepts of `org.modellwerkstatt.dataux` that extend `org.modellwerkstatt.objectflow.structure.Container`. They are the executable entry points; use cases stay in ObjectFlow Commands, Services, and Repositories. [Executable modules](../../../docu/dataux.md#teil-ii--anwendung-und-batchjob)

| Concept | Rootable | Required structure | Optional structure |
| --- | --- | --- | --- |
| `org.modellwerkstatt.dataux.structure.AppUiModule` | yes | `authFunction: AppAuthenticationFunction [1]`; `configuration -> OFXConfig` and one `OptVersion` are enforced by the checker (descriptor: `0..1` / `0..n`) | `mainMenu`, `extrasMenu`, `helpMenu: IMenuItem [0..n]`, `tiles: AppTile [0..n]`, `tileInit: TileInitFunction [0..1]`, `onStartupCmd: StartupCommandCall [0..1]`, `options: IModuleOption [0..n]`, `configuredComponents`/`variable: ContainerVariable [0..n]`, `parameter: ContainerParameter [0..n]` |
| `org.modellwerkstatt.dataux.structure.BatchJobModule` | yes | `authFunction: AppAuthenticationFunction [1]`, `exceptionStrategy: OFXExceptionStrategy [1]`; `configuration -> OFXConfig` and one `OptVersion` are enforced by the checker | `pairs: OFXProducerConsumerPair [0..n]`, `options: IModuleOption [0..n]`, `configuredComponents`/`variable`, `parameter` |

Both concepts still carry `onStartup` and `onShutdown` (`OFXVoidStatementList [0..1]`). Do not create them; the checker rejects them (see [gotchas](gotchas.md#module-startup-and-shutdown-hooks-are-rejected)).

`name` is a plain string property. Prefer identifiers without spaces; the checker warns otherwise.

### Module children

| Concept | Verified shape | Note |
| --- | --- | --- |
| `AppAuthenticationFunction` | `body: StatementList [1]` (BaseLanguage concept function; `userEnvironment` parameter available) | Mandatory on both modules. The body must end with a boolean expression statement. Initialize the user context here (`userEnvironment.setUserName(...)` and the user id); the shipped examples return only `true`. [isAuthenticated](../../../docu/dataux.md#anwendung-mit-appui-module) |
| `AppTile` | `action: MenuAction [1]`; optional `tileLabel`, `tileColor: Expression [0..1]` | Tile on the start surface. [Tiles](../../../docu/dataux.md#tiles-und-dynamische-darstellung) |
| `TileInitFunction` | `body: StatementList [1]` | Prepares shared tile state. |
| `StartupCommandCall` | `commandCall: CommandCallBasis [1]`, optional `enabledCondition: Expression [0..1]` | Command run after login. |
| `MenuAction` in `mainMenu`/`extrasMenu`/`helpMenu`/`AppTile.action` | as in [Menus and command actions](#menus-and-command-actions) | No selection exists at module level; `getSelected()`-style arguments are rejected by the checker. |

### Module options (`IModuleOption`)

| Editor name | Concept | Properties / references | Applies to |
| --- | --- | --- | --- |
| `VERSION` | `OptVersion` | `exp: Expression [1]` (use a `StringLiteral`) | both; required once |
| `OFFICIAL NAME` | `OptOfficialAppName` | `exp: Expression [1]` | both |
| `CRON` | `OptCronPairExp` | string properties `sec`, `min`, `hour`, `dayOfMonth`, `month`, `dayOfWeek`; `pair -> OFXProducerConsumerPair [1]` | BatchJob |
| `DELAY` | `OptDelayPair` | `delayInSec: integer`; `pair [1]` | BatchJob; at most one per pair |
| `CONSUMERS` | `OptNumConsumersPair` | `numConsumers: integer`; `pair [1]` | BatchJob; exactly one per pair with a consumer, none for a producer-only pair |
| `DEPENDENT_CONSECUTIVE` | `OptBatchDependent` | none | BatchJob with more than one pair |
| `RUN_IN_CONSOLE` | `OptRunInConsole` | none | Deprecated by the checker; use `ConsoleBatchJobAppFactory` in the `OFXConfig` instead |
| – | `OptIncludeBatchUi` | `batchJob -> BatchJobModule [1]` | AppUI; embeds a batch job in the UI context |

Semantics of the batch options: [Batch options](../../../docu/dataux.md#kapitellandkarte-batchoptionen).

### Producer/consumer pairs and exception strategy (ObjectFlow concepts)

| Concept | Verified shape |
| --- | --- |
| `org.modellwerkstatt.objectflow.structure.OFXProducerConsumerPair` | `name: string`; `producerImpl: OFXProducerContext [1]`, `consumerImpl: OFXConsumerContext [0..1]` |
| `OFXProducerContext` | `name` (inbox variable name); `keytype: Type [1]` (a `ClassifierType` with `classifier -> Classifier`), `runCommand: OFXRunCmd [1]` |
| `OFXConsumerContext` | `name` (inbox element variable name); `cmdCallContext: OFXConsumerCmdCallContext [1..n]` |
| `OFXConsumerCmdCallContext` | `runCommand: OFXRunCmd [1]`, optional `ifClause: Expression [0..1]` (precondition) |
| `OFXRunCmd` | `commandCall: CommandCallBasis [1]`, `pages: OFXRunCmdPage [0..n]`, `successorHandler: OFXRunCmdSuccessorHandler [0..n]` |
| `CommandCallBasis` | `command -> Command [1]`, `actualArgument: Expression [0..n]` |
| `OFXRunCmdPage` | `name`; `page -> PageCrtl [1]`, `conclusion -> PageConclusion [0..1]`; `beforeConclude: OFXRunCmdStatementList [0..1]` (`body: StatementList [1]`); properties `optionalPage: boolean`, `boundObjectType` enum `boundObject` / `boundList` |
| `OFXRunCmdVarRef` | `varRef -> IOFXRContextVarDeclaration [1]` (the producer context, consumer context, or a run-command page) |
| `OFXExceptionStrategy` | `name`; `member: IOFXExceptionStrategyMember [1..n]` |
| `OFXStrategyForException` | optional `exMatch`, `messagePartMatch: StringLiteral [0..1]`; `properties: IOFXStratBehaviour [0..n]`; a member without `exMatch` is the default rule and must be last |
| `OFXExceptionStrategyInclude` | `strategy -> OFXExceptionStrategy [1]` |

Strategy behaviours (`IOFXStratBehaviour`, editor alias in parentheses): `OFXReAddInboxStratBehaviour` (`READD_TO_INBOX`), `OFXDelayStratBehaviour` (`DELAY_EXECUTION`, property `supendSeconds: integer`, sic), `OFXClearInboxStratBehaviour` (`CLEAR_INBOX`), `OFXConsRestartStratBehaviour` (`CONSUMER_RESTART`), `OFXSilentNoLogStratBehaviour` (`SILENT_NO_LOG`). `JOB_*`/`VM_*` reactions listed in the documentation have no concept in the live language. [Exception strategies](../../../docu/dataux.md#exception-strategien-und-wiederanlauf)

The producer fills its inbox inside `OFXRunCmdPage.beforeConclude`, typically `inbox.addAll(<page var>.<list property>)`; the consumer passes the inbox element to its command as `actualArgument`. Load `moai:objectflow-dsl` for the command side and `moai:mps-baselanguage` for these expressions.
