# Dataux ManMap Examples

## Primary Model

`r:38200fa4-ed1e-4f5b-bf14-ca3dff023767(org.modellwerkstatt.objectflow.tests.manmap.Domain)` is the broadest example. It contains 16 mapped entities, 87 field mappings, references, embedded/list/include mappings, repository methods, joins, custom SQL, save/delete operations, and C2 SQL.

Representative roots:

- `PersDesc`: `r:38200fa4-ed1e-4f5b-bf14-ca3dff023767(org.modellwerkstatt.objectflow.tests.manmap.Domain)/8078003855688249945`
- `NewInvoicePosDesc`: `r:38200fa4-ed1e-4f5b-bf14-ca3dff023767(org.modellwerkstatt.objectflow.tests.manmap.Domain)/5435761382090956033`
- `RepoInvoice`: `r:38200fa4-ed1e-4f5b-bf14-ca3dff023767(org.modellwerkstatt.objectflow.tests.manmap.Domain)/3498864448993201631`
- `C2SqlRepo`: `r:38200fa4-ed1e-4f5b-bf14-ca3dff023767(org.modellwerkstatt.objectflow.tests.manmap.Domain)/798898777369858633`

Use `mps_mcp_print_node(deep=true)` only for the smallest relevant root or method subtree. `RepoInvoice` is deliberately comprehensive and very large.

## Specialized Models

No-key and DTO result mapping:

- Model: `r:b291b2f5-a194-4e43-aecb-36ae047ab7b5(org.modellwerkstatt.objectflow.tests.manmap.XNokeys)`
- Persistence root: `r:b291b2f5-a194-4e43-aecb-36ae047ab7b5(org.modellwerkstatt.objectflow.tests.manmap.XNokeys)/2428815495442616998`
- Repository root: `r:b291b2f5-a194-4e43-aecb-36ae047ab7b5(org.modellwerkstatt.objectflow.tests.manmap.XNokeys)/3498864448993201819`

Compact blob/list mapping:

- Model: `r:77e4d07f-295e-4cf2-8e95-a300af89b0b0(org.modellwerkstatt.objectflow.tests.manmap.ZMixedNewer)`
- Persistence root: `r:77e4d07f-295e-4cf2-8e95-a300af89b0b0(org.modellwerkstatt.objectflow.tests.manmap.ZMixedNewer)/1273212173384952708`
- Repository root: `r:77e4d07f-295e-4cf2-8e95-a300af89b0b0(org.modellwerkstatt.objectflow.tests.manmap.ZMixedNewer)/3498864448993201851`

Small end-to-end order example:

- Model: `r:3fd71311-ae9c-4a95-889b-8542e84d2ec1(org.modellwerkstatt.objectflow.tests.OrderDocument)`
- Persistence root: `r:3fd71311-ae9c-4a95-889b-8542e84d2ec1(org.modellwerkstatt.objectflow.tests.OrderDocument)/5788629615580249756`
- Repository root: `r:3fd71311-ae9c-4a95-889b-8542e84d2ec1(org.modellwerkstatt.objectflow.tests.OrderDocument)/3498864448993201879`

## Reference Targets

Mapping references normally target ObjectFlow/BaseLanguage class and property declaration nodes in the same consumer model. Query/save nodes then reference `EntityMapping`, `ReferenceMapping`, `ListMapping`, or `AdditionalTableName` nodes from a persistence root. Harvest those persistent refs from the target model with shallow project structure or focused node prints; sandbox refs are examples, not universal targets.
