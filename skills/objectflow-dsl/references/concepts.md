# Concepts and verified AST roles

These facts were verified against the live `org.modellwerkstatt.objectflow` runtime descriptors. Re-query with `mps_mcp_get_concept_details` before relying on a feature not listed here.

## Root concepts

| Concept | Primary use | Important direct structure |
| --- | --- | --- |
| `org.modellwerkstatt.objectflow.structure.Entity` | Identity-bearing domain object | `businessProperties`, nested `status`, BaseLanguage `member` |
| `org.modellwerkstatt.objectflow.structure.ValueObject` | Immutable domain value | `businessProperties`, `equalProperties`, nested `status` |
| `org.modellwerkstatt.objectflow.structure.DTO` | Search criteria, projections, transport data | `businessProperties`, nested `status` |
| `org.modellwerkstatt.objectflow.structure.Service` | Stateless domain/application operations | BaseLanguage `member`; service methods use the ObjectFlow method concept |
| `org.modellwerkstatt.objectflow.structure.Command` | User-facing use case and session boundary | `newCommandType`, `parameter`, `variable`, `commandInit`, `pages`, final conclusions, permissions, options |
| `org.modellwerkstatt.objectflow.structure.OFXTestSuit` | ObjectFlow integration test suite | optional `configuration` reference; `configuredComponents`, startup/shutdown, options, test `content` |
| `org.modellwerkstatt.objectflow.structure.OFXConfig` | Runtime component configuration | `elements`, optional `dependencyResolution` |
| `org.modellwerkstatt.objectflow.structure.RolesAndPermissions` | Roles, scopes, identities | `staticRoles`, `scopes`, `identities` |
| `org.modellwerkstatt.objectflow.structure.StaticRessources` | Shared labels, colors, platforms | required `platforms` (`1..n`), optional `labels`, `color`, and `extends` |

Choose Entity, Value Object, and DTO by semantics, not convenience: identity/lifecycle, immutable value, or use-case projection respectively. [Detailed semantics](../../../docu/objectflow.md#entity-value-object-und-dto)

## Domain structure children

### Business Property

`org.modellwerkstatt.objectflow.structure.BusinessProperty` is non-rootable. Its operationally important shape is:

- Properties: `propertyName` and inherited `name`.
- Required child `type` (`1`) targeting `jetbrains.mps.baseLanguage.structure.Type`.
- Required child `propertyImplementation` (`1`) targeting `jetbrains.mps.baseLanguage.structure.PropertyImplementation`.
- Optional `propertyOption` (`0..n`) targets ManMap's abstract `FieldOption`, so ObjectFlow and ManMap options may appear together.
- Optional `shortDesc`, `longDesc`, `numberFormat`, `documentation`, and `visibility`.

Use only the supported property types listed in the documentation; arbitrary Java types are not offered by the editor. [Business Property types and options](../../../docu/objectflow.md#business-properties)

Use `CustomPropertyImplementation` only for computed/virtual values; it has no independent persistence value and its getter cannot call repositories or services. [Virtual Business Properties](../../../docu/objectflow.md#virtuelle-business-properties)

### Status

`org.modellwerkstatt.objectflow.structure.StatusDeclaration` is non-rootable and belongs in the `status` role of Entity, Value Object, or DTO. It contains `element` (`0..n`) children of `StatusElement` and declaration `options`.

Each `StatusElement` has `name` and technical `value`, required `shortDescNew` and `longDescNew` string-literal children, plus optional element options. Model creation/default/null behavior explicitly rather than treating Java `null` as a regular status. [Status semantics and options](../../../docu/objectflow.md#status)

## Services and calls

Services are long-lived, normally singleton-like components and must remain stateless. Put cross-aggregate or infrastructure-coordinating operations here; keep rules that naturally belong to one domain structure on that structure. [Service components](../../../docu/objectflow.md#service-komponenten)

Invoke configured Services and ManMap Repositories with `org.modellwerkstatt.objectflow.structure.OperationCall` (`#`), not as ordinary Java instances; this preserves component, session, and transaction semantics. [Component calls](../../../docu/objectflow.md#komponenten-mit--aufrufen)

## Commands and pages

`Command.newCommandType` accepts exactly `GRAPH_EDIT_CMD`, `GRAPH_OWNER_CMD`, `SEARCH_CMD`, or `GRAPH_OWNER_CMD_MODAL`. Their session/commit semantics differ materially. [Four command types](../../../docu/objectflow.md#die-vier-command-typen)

Important verified roles:

- `pages`: `PageCrtl` (`0..n`)
- `commandInit`: `CommandVoidStatementList` (`0..1`)
- `okConclusionStatements` / `cancelConclusionStatements`: `CommandVoidStatementList` (`0..1`)
- `parameter`: `ContainerParameter` (`0..n`)
- `variable`: `ContainerVariable` (`0..n`)
- `preconditiondsNew`: `Precondition` (`0..n`)
- `permissionNew`: `IPermissionCmd` (`0..n`)
- `options`: `ICommandOption` (`0..n`)
- `successorCommand`: `SuccessorCommandCall` (`0..n`)

`PageCrtl` is non-rootable. It requires `pageInit` (`1`) and at least one `pagePaneActionProviderLink` (`1..n`); `boundObject` is optional structurally but required for a normal bound UI page. It may contain conclusions, scopes, and command-termination handlers. ObjectFlow owns page state and flow; DataUX owns visible layout and menus. [Pages and Page Conclusions](../../../docu/objectflow.md#pages-und-page-conclusions)

`PageConclusion` optionally contains `function` and `enabledWhen`, requires a `label` reference, and uses `conclusionType` values `SAVE_CONCLUSION` or `NOSAVE_CONCLUSION`. `save` is the normal mode; use `no_save` only when editor changes must deliberately be discarded. [Page Conclusions](../../../docu/objectflow.md#page-conclusions)

## Tests, configuration, permissions, resources

- Prefer `OFXTestSuit` over JUnit whenever ObjectFlow, ManMap, session, component, or command semantics are under test. [OFXTestSuit](../../../docu/objectflow.md#ofxtestsuit)
- `run command` can simulate pages, conclusions, child commands, and successors without DataUX. [Commands without UI](../../../docu/objectflow.md#commands-ohne-ui-ausführen)
- A value passed forward from `FINAL OK_CONCLUSION` is declared by `CommandCreationInfo` (projected as `user toast message`; `msg` [1], optional `keyReference`, name in `refName`). In the test, reference it with `OFXRunCmdCreateInfoRef` (reference role `reference` → that `CommandCreationInfo`), not with a `VariableReference`. [Commands without UI](../../../docu/objectflow.md#commands-ohne-ui-ausführen)
- `OFXConfig` models component wiring, reusable sections, overrides, scanning, and primary implementations. [OFXConfig](../../../docu/objectflow.md#konfiguration-mit-ofxconfig)
- `RolesAndPermissions` separates roles, object-returning scopes, and cached identities. Invalidate role caches deliberately when context changes. [Roles, scopes, and identities](../../../docu/objectflow.md#rollen-scopes-und-identities)
- `StaticRessources` requires at least one platform and centralizes platform-specific labels/colors without duplicating commands. [Static resources](../../../docu/objectflow.md#statische-ressourcen)

## DSL responsibility boundaries

| Concern | Model in | Operational rule |
| --- | --- | --- |
| Domain data, rules, services, use-case flow | ObjectFlow | Keep business meaning and command/session coordination here. |
| Mapping, repository query, save/delete, SQL | ManMap | Load graphs explicitly and register transactional writes as session operations. [Persistence boundaries](../../../docu/manmap.md#repositories-und-die-vier-methodenarten) |
| Page panes, forms, tables, layout, menus | DataUX | Bind already-prepared data; binding does not load it. [Data binding and selection](../../../docu/dataux.md#datenbindung-und-selektion) |
| Choosing the responsible DSL | MoWare overview | Use the [change-location matrix](../../../docu/moware-werkbank.md#wo-gehört-eine-änderung-hin). |

