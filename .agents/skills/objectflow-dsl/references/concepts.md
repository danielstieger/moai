# ObjectFlow concepts

Metadata comes from `mps_mcp_get_concept_details` for `l:ec097fca-5b84-41f2-847d-6a5690cae277:org.modellwerkstatt.objectflow`. Use `org.modellwerkstatt.objectflow.structure.<Concept>` in blueprint `concept` fields. The language has 211 reported concepts; this is a task-oriented subset. Re-query MPS before using an unlisted role.

| Rootable concept | Main use | Useful roles |
| --- | --- | --- |
| `Entity` | Persistent domain object | `businessProperties` 0..n; inherited BaseLanguage `member` 0..n and `visibility` 0..1 |
| `ValueObject` | Value-like domain object | `businessProperties` 0..n, `equalProperties` 0..n, inherited `member` |
| `DTO` | Data transfer object | `businessProperties` 0..n, inherited `member` |
| `Service` | Application operations | inherited BaseLanguage `member` 0..n |
| `Command` | Application command and flow | `parameter` 0..n, `variable` 0..n, `pages` 0..n, `commandInit` 0..1, `okConclusionStatements` 0..1, `cancelConclusionStatements` 0..1 |
| `OFXConfig` | MoWare configuration | `elements` 0..n, `dependencyResolution` 0..1, `docu` 0..1 |
| `OFXTestSuit` | Stand-alone runnable tests | Inspect current descriptor before editing |
| `RolesAndPermissions` | Access declarations | Inspect current descriptor before editing |
| `StaticRessources` | Static resource declarations | Inspect current descriptor before editing |

`Entity`, `ValueObject`, `DTO`, and `Service` extend `jetbrains.mps.baseLanguage.structure.ClassConcept`. Their inherited class properties include `name`, `nestedName`, `isStatic`, and `virtualPackage`; methods use BaseLanguage roles. `Entity`, `ValueObject`, and `DTO` implement ObjectFlow's `IOFXObject` interface.

## Frequently edited child concepts

| Concept | Parent role | Important features |
| --- | --- | --- |
| `BusinessProperty` | `Entity`/`ValueObject`/`DTO.businessProperties` | `name`, `propertyName`; required `type` (BaseLanguage `Type`) and `propertyImplementation` (BaseLanguage `PropertyImplementation`); optional `shortDesc`, `longDesc`, `propertyOption`, `visibility` |
| `ContainerParameter` | `Command.parameter` | `name`, required BaseLanguage `type`, optional `initializer` |
| `PageCrtl` | `Command.pages` | `name`, required `pageInit` and `pagePaneActionProviderLink` (1..n); optional `boundObject` reference |

`BusinessProperty.propertyOption` accepts ManMap options. The `WarenGruppe.id` example has a ManMap `KeyOption`; consult the [ManMap skill](../../manmap-dsl/SKILL.md) before changing persistence options.

## Reference conventions

`PageCrtl.boundObject` targets a BaseLanguage `ClassConcept`, which may be an ObjectFlow Entity or DTO. Other roots may reference ManMap or DataUX nodes. Use `r:...` persistent **node** refs for explicit targets; `c:...` concept refs describe types and are not valid node targets. Resolve targets in the intended model's scope.
