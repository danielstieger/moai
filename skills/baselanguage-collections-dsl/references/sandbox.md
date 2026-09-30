# Packaged example catalogue

The stable examples below belong to the shipped solution `org.modellwerkstatt.dataux.tests` (`3c6ef8ca-6366-4c8b-8839-0277eaca1f7e(org.modellwerkstatt.dataux.tests)`). They may be cited and inspected. Do not replace them with persistent references from an application project. Query it with explicit module/model references (`scope: "modules"` or `"models"`); see *Packaged modules outside the project* in `moai:mps-mcp-workflow` (`references/finding-things.md`).

## Types and mutation

Model: `r:38200fa4-ed1e-4f5b-bf14-ca3dff023767(org.modellwerkstatt.objectflow.tests.manmap.Domain)`

- Root `C2SqlRepo`: `r:38200fa4-ed1e-4f5b-bf14-ca3dff023767(org.modellwerkstatt.objectflow.tests.manmap.Domain)/798898777369858633`
- `SequenceType` sample: `r:38200fa4-ed1e-4f5b-bf14-ca3dff023767(org.modellwerkstatt.objectflow.tests.manmap.Domain)/8315478230712676274`
- `ListType` sample: `r:38200fa4-ed1e-4f5b-bf14-ca3dff023767(org.modellwerkstatt.objectflow.tests.manmap.Domain)/4702435571864900777`
- `MapType` sample: `r:38200fa4-ed1e-4f5b-bf14-ca3dff023767(org.modellwerkstatt.objectflow.tests.manmap.Domain)/1480444990477060264`
- Root `CreatorsFactory`: `r:38200fa4-ed1e-4f5b-bf14-ca3dff023767(org.modellwerkstatt.objectflow.tests.manmap.Domain)/5192736124081733356`
- `AddElementOperation` sample: `r:38200fa4-ed1e-4f5b-bf14-ca3dff023767(org.modellwerkstatt.objectflow.tests.manmap.Domain)/5038704574094064296`

Use these for collection type roles and a verified list/set-style mutation operation.

## Creators and map access

Model: `r:5bf243d1-e033-4283-af3f-e92e48129c81(org.modellwerkstatt.dataux.tests.apidesc)`

- Root `TestDescription`: `r:5bf243d1-e033-4283-af3f-e92e48129c81(org.modellwerkstatt.dataux.tests.apidesc)/8339618607382762701`
- `ListCreatorWithInit` sample: `r:5bf243d1-e033-4283-af3f-e92e48129c81(org.modellwerkstatt.dataux.tests.apidesc)/4294510478599126171`
- Root `ApiTestSuit`: `r:5bf243d1-e033-4283-af3f-e92e48129c81(org.modellwerkstatt.dataux.tests.apidesc)/8339618607383211424`
- `HashMapCreator` sample: `r:5bf243d1-e033-4283-af3f-e92e48129c81(org.modellwerkstatt.dataux.tests.apidesc)/8339618607391913060`
- `MapElement` sample: `r:5bf243d1-e033-4283-af3f-e92e48129c81(org.modellwerkstatt.dataux.tests.apidesc)/8339618607391943299`

The creator nodes are nested below BaseLanguage `GenericNewExpression`; print their parent when reconstructing the complete expression.

## Filters, predicates, and terminals

Model: `r:1e9d9498-1123-47e6-b3ad-2a4dd175afe5(org.modellwerkstatt.objectflow.tests.manmap.Tests)`

- Root `Graph load/save (no session)`: `r:1e9d9498-1123-47e6-b3ad-2a4dd175afe5(org.modellwerkstatt.objectflow.tests.manmap.Tests)/5126215201999370162`
- `WhereOperation` sample: `r:1e9d9498-1123-47e6-b3ad-2a4dd175afe5(org.modellwerkstatt.objectflow.tests.manmap.Tests)/6118054721500784507`
- `AnyOperation` sample: `r:1e9d9498-1123-47e6-b3ad-2a4dd175afe5(org.modellwerkstatt.objectflow.tests.manmap.Tests)/3340964334524672765`
- `GetFirstOperation` sample: `r:1e9d9498-1123-47e6-b3ad-2a4dd175afe5(org.modellwerkstatt.objectflow.tests.manmap.Tests)/1452267886878651376`
- Root `References, initialization(no session)`: `r:1e9d9498-1123-47e6-b3ad-2a4dd175afe5(org.modellwerkstatt.objectflow.tests.manmap.Tests)/2631052178917309181`
- `ToListOperation` sample: `r:1e9d9498-1123-47e6-b3ad-2a4dd175afe5(org.modellwerkstatt.objectflow.tests.manmap.Tests)/8202666999505542590`

Print the parent `DotExpression` rather than only the operation node when the operand and full closure are needed.

## Mapping and size

- Model `org.modellwerkstatt.objectflow.tests.OrderDocument`: `r:3fd71311-ae9c-4a95-889b-8542e84d2ec1(org.modellwerkstatt.objectflow.tests.OrderDocument)`
- Root `OrderDocument`: `r:3fd71311-ae9c-4a95-889b-8542e84d2ec1(org.modellwerkstatt.objectflow.tests.OrderDocument)/5788629615579823422`
- `SelectOperation` sample: `r:3fd71311-ae9c-4a95-889b-8542e84d2ec1(org.modellwerkstatt.objectflow.tests.OrderDocument)/5788629615585609436`
- Model `org.modellwerkstatt.objectflow.tests.OrderDocumentRunCmd`: `r:40578ea0-bba5-4ae6-abfa-3691d42660ff(org.modellwerkstatt.objectflow.tests.OrderDocumentRunCmd)`
- Root `RunCmdTests`: `r:40578ea0-bba5-4ae6-abfa-3691d42660ff(org.modellwerkstatt.objectflow.tests.OrderDocumentRunCmd)/5353263021888352480`
- `GetSizeOperation` sample: `r:40578ea0-bba5-4ae6-abfa-3691d42660ff(org.modellwerkstatt.objectflow.tests.OrderDocumentRunCmd)/7123824244833280604`

## Verification protocol

1. Resolve the packaged solution or model reference with `mps_mcp_get_project_structure`.
2. Print the containing root or operation parent shallowly first.
3. Deep-print only the subtree required for the task.
4. Re-query concept details for required roles and cardinalities.
5. Never persist a reference discovered outside the packaged solution.

