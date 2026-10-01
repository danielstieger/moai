# Concepts and verified AST roles

The technical facts below were verified against the live `org.modellwerkstatt.dataux` runtime descriptors. Re-query with `mps_mcp_get_concept_details` before relying on a feature that is not listed. Semantic rules link directly to the package documentation.

## UI roots and composition

| Concept | Rootable | Required structure | Optional binding/menu structure |
| --- | --- | --- | --- |
| `org.modellwerkstatt.dataux.structure.PagePane` | yes | `uxChild: IUxElement [1]` | `options: IPagePaneOption [0..n]`, `menuItems: IMenuItem [0..n]`, `boundClassifier [0..1]`, `boundProperty [0..1]` |
| `org.modellwerkstatt.dataux.structure.DelegateForm` | yes | `colWeights: LayoutWeight [1..n]` | `delegates: IDelegate [0..n]`, `options: IFOption [0..n]`, binding refs |
| `org.modellwerkstatt.dataux.structure.Table` | yes | no mandatory child at descriptor level | `delegates`, `options`, `menuItems` (`0..n` each), binding refs |
| `org.modellwerkstatt.dataux.structure.GridLayout` | yes | `uxChild: IUxElement [1..n]` | `rowWeights`, `colWeights`, `options` (`0..n`), binding refs |
| `org.modellwerkstatt.dataux.structure.TabLayout` | yes | `tabs: Tab [1..n]` | binding refs |
| `org.modellwerkstatt.dataux.structure.Tab` | no | `label: Expression [1]`, `uxChild: IUxElement [1]` | none |
| `org.modellwerkstatt.dataux.structure.Include` | no | `uxElement: IBindable [1]` reference | binding refs, `menuItems`, `options` |
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
| `LocalPropertyReference` | required `property` reference | Direct property in the current binding context |
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
| `MenuCompoundAction` | inherits `MenuAction`; optional `graphOwnerAutoCon`, `graphEditCall`, and `graphEditAutoCon` |
| `PageConclusionReference` | required `pageConclusion -> ObjectFlow PageConclusion [1]` |
| `PageConclusionOptionUserCancel` | marker for the `USER_CANCEL` continuation case |
| `MenuSeparator` | separator marker |

Prefer a submenu/overflow group and keep only exceptional actions at the top level. A table menu normally acts on row selections; a PagePane menu normally acts on the page/root context, but typed `getSelected(...)` may address any type participating in the shared selection. [Menus and command actions](../../../docu/dataux.md#menüs-und-command-aktionen)

Command availability, parameters, permissions, and conclusions remain ObjectFlow concerns. [ObjectFlow command parameters and selection](../../../docu/objectflow.md#parameter-defaults-und-selektion) and [Page Conclusions](../../../docu/objectflow.md#page-conclusions)
