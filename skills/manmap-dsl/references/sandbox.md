# Shipped Examples and Verification Anchors

Despite this file's conventional name, these are package-shipped test models, not assumptions about editor state or a target application. They belong to the guaranteed module `3c6ef8ca-6366-4c8b-8839-0277eaca1f7e(org.modellwerkstatt.dataux.tests)` and may be cited and inspected read-only. Query it with explicit module/model references (`scope: "modules"` or `"models"`); see *Packaged modules outside the project* in `moai:mps-mcp-workflow` (`references/finding-things.md`).

## Clean Root Anchors

These roots resolved and returned `no problems found` from `mps_mcp_check_root_node_problems` during generation:

| Purpose | Root reference |
| --- | --- |
| Broad persistence mapping | `r:38200fa4-ed1e-4f5b-bf14-ca3dff023767(org.modellwerkstatt.objectflow.tests.manmap.Domain)/8078003855688249945` (`PersDesc`) |
| Compact end-to-end persistence mapping | `r:3fd71311-ae9c-4a95-889b-8542e84d2ec1(org.modellwerkstatt.objectflow.tests.OrderDocument)/5788629615580249756` (`DefaultPd`) |
| Compact repository | `r:3fd71311-ae9c-4a95-889b-8542e84d2ec1(org.modellwerkstatt.objectflow.tests.OrderDocument)/3498864448993201879` (`ORDERDOCUMENTS`) |
| Save/delete and audit repository | `r:38200fa4-ed1e-4f5b-bf14-ca3dff023767(org.modellwerkstatt.objectflow.tests.manmap.Domain)/3498864448993201739` (`RepoAccountAudit`) |
| No-key persistence mapping | `r:b291b2f5-a194-4e43-aecb-36ae047ab7b5(org.modellwerkstatt.objectflow.tests.manmap.XNokeys)/2428815495442616998` (`NKPersistanceDescription`) |

Re-check a root before treating it as clean after package upgrades.

## Focused Node Anchors

Use focused deep prints rather than printing a multi-megabyte repository root:

| Shape | Node reference |
| --- | --- |
| Entity mapping with optimistic option, fields, embedded mapping, and list mapping | `r:3fd71311-ae9c-4a95-889b-8542e84d2ec1(org.modellwerkstatt.objectflow.tests.OrderDocument)/5788629615580249768` |
| Field mapping | `r:3fd71311-ae9c-4a95-889b-8542e84d2ec1(org.modellwerkstatt.objectflow.tests.OrderDocument)/5788629615580249910` |
| Embedded value-object mapping | `r:3fd71311-ae9c-4a95-889b-8542e84d2ec1(org.modellwerkstatt.objectflow.tests.OrderDocument)/5788629615580249790` |
| Key-only list mapping | `r:3fd71311-ae9c-4a95-889b-8542e84d2ec1(org.modellwerkstatt.objectflow.tests.OrderDocument)/5788629615580249800` |
| Read-only mapped `get` query | `r:b291b2f5-a194-4e43-aecb-36ae047ab7b5(org.modellwerkstatt.objectflow.tests.manmap.XNokeys)/2428815495460955444` |
| Save statement | `r:38200fa4-ed1e-4f5b-bf14-ca3dff023767(org.modellwerkstatt.objectflow.tests.manmap.Domain)/8078003855688249815` |
| Delete statement | `r:38200fa4-ed1e-4f5b-bf14-ca3dff023767(org.modellwerkstatt.objectflow.tests.manmap.Domain)/995084002912093027` |
| Direct SQL block | `r:38200fa4-ed1e-4f5b-bf14-ca3dff023767(org.modellwerkstatt.objectflow.tests.manmap.Domain)/1480444990479808861` |
| No-key mapper | `r:b291b2f5-a194-4e43-aecb-36ae047ab7b5(org.modellwerkstatt.objectflow.tests.manmap.XNokeys)/781751828141699450` |
| Reusable row mapper | `r:38200fa4-ed1e-4f5b-bf14-ca3dff023767(org.modellwerkstatt.objectflow.tests.manmap.Domain)/1538415634284477467` |

The focused references were verified to resolve. They are examples only: do not copy their internal target references into application models.

## Navigation Procedure

1. Determine the target MPS project dynamically.
2. Resolve the shipped module/model by the explicit reference above. If name-based discovery omits globally visible modules, call `mps_mcp_get_project_structure` with `includeStubModules=true`.
3. Print only the root or subtree needed for the current shape.
4. Replace every domain/mapping/member reference with a reference resolved in the actual target model.
5. Validate the changed target root; do not edit these examples as part of an application task.
