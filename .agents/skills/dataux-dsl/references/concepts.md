# DataUX concepts

The live descriptor exposes the following rootable concepts:

| Concept | Purpose | Important structure |
| --- | --- | --- |
| `org.modellwerkstatt.dataux.structure.PagePane` | UI for an ObjectFlow Page | optional `boundClassifier`/`boundProperty`; required `uxChild: IUxElement`; optional page options and menus |
| `org.modellwerkstatt.dataux.structure.DelegateForm` | Form built from property delegates | optional binding; required `colWeights`; delegates and form options |
| `org.modellwerkstatt.dataux.structure.Table` | Rows and columns for a bound list | optional binding; delegates as columns; form options and menus |
| `org.modellwerkstatt.dataux.structure.GridLayout` | Rows/columns containing UI elements | row/column weights and one or more `uxChild` elements |
| `org.modellwerkstatt.dataux.structure.TabLayout` | Tabs containing UI elements | one or more `Tab` children |
| `org.modellwerkstatt.dataux.structure.CustomElement` | Project-specific UI implementation | required implementation class expression; optional delegates/options/menus |
| `org.modellwerkstatt.dataux.structure.AppUiModule` | Executable application with UI | optional configuration; required auth; menus, tiles, startup command and lifecycle |
| `org.modellwerkstatt.dataux.structure.BatchJobModule` | Executable batchjob | optional configuration; required auth and exception strategy; producer/consumer pairs and options |
| `org.modellwerkstatt.dataux.structure.ApiDescription` | API declaration | intentionally not documented in this skill revision |

## Binding and UI composition

`PagePane`, `DelegateForm`, `Table`, `GridLayout`, `TabLayout`, and `CustomElement` are bindable. Their inherited references are:

- `boundClassifier -> jetbrains.mps.baseLanguage.structure.Classifier` (`0..1`)
- `boundProperty -> jetbrains.mps.baseLanguage.structure.Property` (`0..1`)

The binding may be inherited from the enclosing element. Resolve explicit bindings from the target ObjectFlow/BaseLanguage declaration nodes; do not substitute concept refs for declaration node refs.

Important concrete children:

| Parent | Role | Target | Cardinality |
| --- | --- | --- | --- |
| `PagePane` | `uxChild` | `IUxElement` | `1` |
| `PagePane` | `options` | `IPagePaneOption` | `0..n` |
| `PagePane` | `menuItems` | `IMenuItem` | `0..n` |
| `DelegateForm` | `colWeights` | `LayoutWeight` | `1..n` |
| `DelegateForm` | `delegates` | `IDelegate` | `0..n` |
| `Table` | `delegates` | `IDelegate` | `0..n` |
| `Table` | `menuItems` | `IMenuItem` | `0..n` |
| `GridLayout` | `rowWeights` / `colWeights` | `LayoutWeight` | `0..n` |
| `GridLayout` | `uxChild` | `IUxElement` | `1..n` |
| `TabLayout` | `tabs` | `Tab` | `1..n` |
| `Tab` | `label` | BaseLanguage `Expression` | `1` |
| `Tab` | `uxChild` | `IUxElement` | `1` |
| `Include` | reference `uxElement` | `IBindable` | `1` |

## Delegates

`DelegateForm` and `Table` accept `IDelegate` children. Concrete delegate concepts include:

- `StringDelegate`
- `IntegerDelegate`
- `BigDecimalDelegate`
- `DateTimeDelegate`
- `DateTimeDateOnlyDelegate`
- `LocalDateDelegate`
- `StatusDelegate`
- `ReferenceDelegate`
- `ImageDelegate`
- `UploadDelegate`
- `DummyDelegate`

Most property delegates carry their binding below `boundTo` and accept `IDOption` children below `option`. Common examples seen in `simpleone` include `WidthDOption`, `DisabledDOption`, `OptionalDOption`, `PickerDOption`, `ImportantDOption`, `DynColorDOption`, and `StatusLongDescDOption`. Select a delegate compatible with the bound property type; inspect a focused sample before constructing the subtree.

## Menus and actions

- `MenuAction` requires `command -> org.modellwerkstatt.objectflow.structure.Command`; it optionally references a custom label and accepts actual argument expressions.
- `MenuSub` contains an optional string label and nested `IMenuItem` children.
- `MenuCompoundAction` sequences command calls and their page-conclusion behavior.
- `MenuSeparator` visually separates entries.

## Application

`AppUiModule` has optional `configuration -> OFXConfig` and these important children:

- `authFunction: AppAuthenticationFunction[1]`
- `onStartupCmd: StartupCommandCall[0..1]`
- `configuredComponents: ContainerVariable[0..n]`
- `onStartup` / `onShutdown: OFXVoidStatementList[0..1]`
- `mainMenu`, `extrasMenu`, `helpMenu: IMenuItem[0..n]`
- `tiles: AppTile[0..n]`
- `tileInit: TileInitFunction[0..1]`
- `parameter`, `variable`, and `options`

`AppTile` requires a `MenuAction` and optionally supplies label and color expressions. `StartupCommandCall` requires an ObjectFlow `CommandCallBasis` and optionally an enablement expression.

## Batchjob

`BatchJobModule` has optional `configuration -> OFXConfig` and these important children:

- `authFunction: AppAuthenticationFunction[1]`
- `exceptionStrategy: OFXExceptionStrategy[1]`
- `pairs: OFXProducerConsumerPair[0..n]`
- common configured components, lifecycle, parameters, variables, and options

Batch-oriented options:

| Concept | Alias / purpose | Required link or data |
| --- | --- | --- |
| `OptCronPairExp` | `CRON` | required `pair`; cron fields `sec`, `min`, `hour`, `dayOfMonth`, `month`, `dayOfWeek` |
| `OptDelayPair` | `DELAY` | required `pair`; `delayInSec` |
| `OptNumConsumersPair` | `CONSUMERS` | required `pair`; `numConsumers` |
| `OptBatchDependent` | `DEPENDENT_CONSECUTIVE` | marker option |
| `OptRunInConsole` | `RUN_IN_CONSOLE` | marker option; no UI instance |
| `OptIncludeBatchUi` | include batch UI | required `batchJob` reference |
| `OptVersion` | `VERSION` | required expression |
| `OptOfficialAppName` | `OFFICIAL NAME` | required expression |

