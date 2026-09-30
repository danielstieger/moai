# Packaged example catalogue

The stable examples below belong to the shipped solution `org.modellwerkstatt.dataux.tests` (`3c6ef8ca-6366-4c8b-8839-0277eaca1f7e(org.modellwerkstatt.dataux.tests)`). They may be cited and inspected. Do not replace them with examples or persistent node references from an application project. Query it with explicit module/model references (`scope: "modules"` or `"models"`); see *Packaged modules outside the project* in `moai:mps-mcp-workflow` (`references/finding-things.md`).

## Domain structures and basic tests

Model: `r:92160189-dec1-4f0a-9046-c09a5bafe28d(org.modellwerkstatt.objectflow.tests.FixedBugs)`

- Entity `SimpleEntity`: `r:92160189-dec1-4f0a-9046-c09a5bafe28d(org.modellwerkstatt.objectflow.tests.FixedBugs)/2631052178919868679`
- Value Object `SimpleValue`: `r:92160189-dec1-4f0a-9046-c09a5bafe28d(org.modellwerkstatt.objectflow.tests.FixedBugs)/6665012079371707457`
- Test suite `SomeFixes`: `r:92160189-dec1-4f0a-9046-c09a5bafe28d(org.modellwerkstatt.objectflow.tests.FixedBugs)/1013479022845488722`

Use these for compact Entity/Value Object/property/equality/test shapes. Interpret them with [domain-model semantics](../../../docu/objectflow.md#teil-i--fachliche-datenmodellierung) and [ObjectFlow test semantics](../../../docu/objectflow.md#teil-iv--tests-mit-objectflow).

## DTO, nested status, and service

Model: `r:5bf243d1-e033-4283-af3f-e92e48129c81(org.modellwerkstatt.dataux.tests.apidesc)`

- DTO `SimpleDTO` with nested status: `r:5bf243d1-e033-4283-af3f-e92e48129c81(org.modellwerkstatt.dataux.tests.apidesc)/8339618607382769256`
- Service `ApiService`: `r:5bf243d1-e033-4283-af3f-e92e48129c81(org.modellwerkstatt.dataux.tests.apidesc)/5959129396280194436`
- Test suite `ApiTestSuit`: `r:5bf243d1-e033-4283-af3f-e92e48129c81(org.modellwerkstatt.dataux.tests.apidesc)/8339618607383211424`

Use `SimpleDTO` to inspect the required `StatusElement` descriptions and status options. [Status runtime semantics](../../../docu/objectflow.md#status)

## Commands and headless command tests

Model: `r:40578ea0-bba5-4ae6-abfa-3691d42660ff(org.modellwerkstatt.objectflow.tests.OrderDocumentRunCmd)`

- Test suite `RunCmdTests`: `r:40578ea0-bba5-4ae6-abfa-3691d42660ff(org.modellwerkstatt.objectflow.tests.OrderDocumentRunCmd)/5353263021888352480`
- Graph-owner command `GO`: `r:40578ea0-bba5-4ae6-abfa-3691d42660ff(org.modellwerkstatt.objectflow.tests.OrderDocumentRunCmd)/5353263021888364202`
- Graph-edit command `GE`: `r:40578ea0-bba5-4ae6-abfa-3691d42660ff(org.modellwerkstatt.objectflow.tests.OrderDocumentRunCmd)/5353263021888364229`
- Search command `SEARCH_CMD`: `r:40578ea0-bba5-4ae6-abfa-3691d42660ff(org.modellwerkstatt.objectflow.tests.OrderDocumentRunCmd)/7464717488285058627`

Use these to compare command ownership and `run command` structures. Do not copy domain-specific references into portable blueprints; replace them with `TARGET_*` placeholders. [Command lifecycle](../../../docu/objectflow.md#grundablauf-eines-commands) and [headless command tests](../../../docu/objectflow.md#commands-ohne-ui-ausführen)

## Session merge and permissions

Model: `r:9ec2b7d3-20d4-4c7b-a16d-9bf9768c1f66(org.modellwerkstatt.objectflow.tests.ObjectFlowInfra)`

- Test suite `SessionAndMerge`: `r:9ec2b7d3-20d4-4c7b-a16d-9bf9768c1f66(org.modellwerkstatt.objectflow.tests.ObjectFlowInfra)/6865978791313588783`
- Roles/scopes/identities root `TestRolesAndPermissions`: `r:9ec2b7d3-20d4-4c7b-a16d-9bf9768c1f66(org.modellwerkstatt.objectflow.tests.ObjectFlowInfra)/7804852809881977578`

Use these for explicit merge and authorization shapes. [Session merge](../../../docu/objectflow.md#explizites-command-termination-handling-und-session-merge) and [roles/scopes/identities](../../../docu/objectflow.md#rollen-scopes-und-identities)

## Configuration and resources

Model: `r:9a581386-85ce-41a3-b17b-b79192665eb8(org.modellwerkstatt.objectflow.tests.config)`

- Configuration `Defaults`: `r:9a581386-85ce-41a3-b17b-b79192665eb8(org.modellwerkstatt.objectflow.tests.config)/5505654805890699853`
- Static resources `RessourcesForTests`: `r:9a581386-85ce-41a3-b17b-b79192665eb8(org.modellwerkstatt.objectflow.tests.config)/8255348026212344894`

Inspect these instead of inventing component-wiring or platform-resource child shapes. [Configuration](../../../docu/objectflow.md#konfiguration-mit-ofx-config) and [static resources](../../../docu/objectflow.md#statische-ressourcen)

## Verification protocol

1. Resolve the solution/module/model by persistent reference with `mps_mcp_get_project_structure`.
2. Use `mps_mcp_print_node` with `deep=false` first.
3. Deep-print only the subtree needed for the task.
4. Re-query concept details for required roles/cardinalities.
5. Never persist a reference discovered outside this packaged solution.

