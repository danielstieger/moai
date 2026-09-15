# Permanent ManMap test index

The model `org.modellwerkstatt.objectflow.tests.manmap.Tests` has reference `r:1e9d9498-1123-47e6-b3ad-2a4dd175afe5(org.modellwerkstatt.objectflow.tests.manmap.Tests)`. It is available in the global MPS namespace even when another project is open. Combine that model prefix with any `/id` below to print a focused suite or case via MPS MCP.

| Need | Suite `/id` | Useful case `/id` |
|---|---|---|
| Graph query, save, delete | `Graph load/save (no session)` `/5126215201999370162` | `Store and Load Invoices by Graph get/where` `/8078003855688272219`; `Delete and Insert changes object count by one` `/2631052178922711913` |
| Reference initialization | `References, initialization(no session)` `/2631052178917309181` | `Save and load an integer-key reference via join` `/995084002923535251`; `Check Reference initialization in Entities for IntegerKey` `/8367961125966062722` |
| List loading | same reference suite | `Save and load a list of string-key references with join` `/995084002920156278` |
| Key variants | same reference suite | `Check StringKey dirty handling for entities - initially set` `/3522631632405027063`; `Check CompoundKey dirty handling for entities - initially set` `/3522631632408584875` |
| Read-only query protection | `Graph load/save (no session)` `/5126215201999370162` | `Deleting a readonly object results in an exception` `/2342272659640273806`; `Changing a readonly object results in an exception` `/995084002915135931` |
| No-key DTOs and read-only | `NoKey Tests` `/781751828145881358` | `All objects retrieved with noKeyMap are read-only` `/2428815495462864731`; `Load DTO with mapper - load DTOs` `/4954101300527030496` |
| No-key missing reference | same no-key suite | `Use complex NoKeyMap to load article reference - Not Initialized Exception.` `/2428815495459175570` |
| C2 scalar and no-key mapper | `Custom2 SQL` `/798898777369832798` | `Simply query for int with plain sql.` `/798898777369832806`; `Quickly check the no key mapper.` `/8232801790828105024` |
| C2 parameter integration | same C2 suite | `SQL Integration for sql blocks - Named Params` `/227372689777541715`; `SQL Integration for sql blocks - Pos Args` `/227372689780029899` |
| Query operators | `Query and Operators (no session)` `/2631052178917309179` | `Use <in> operator in query.` `/4980043248558901446`; `Use the optional operator in query (on integer).` `/2631052178918254931`; `Query invoices by string with like operator.` `/995084002917996056` |
| Batch save and optimistic locking | `Graph load/save (no session)` `/5126215201999370162` | `Batch Handling: Auto insert/update, depending on key.` `/7433800982201909714`; `Double write with optimistic locking should result in an exception` `/2342272659641380746` |
| Audit fields | `Audit` `/1081373988674145841` | `Insert an AuditEntity with complete auditing (created / modified)` `/7048832525950813215`; `Update the AuditEntity should NOT change modified Stamps when not dirty.` `/7048832525951936382` |
| Alternative tables | `AlternativeTables` `/3903367921600235832` | `Save and Reload on Archive` `/3903367921600247689`; `Query on arch invoice table with ReadOnly and full join.` `/3518857947620003376` |

Test names are navigation hints. Inspect the relevant nodes and assertions before generalizing behavior. To execute a case, use `mps-run-configurations` and the project's configured database environment.
