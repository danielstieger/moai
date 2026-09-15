# Example models and persistent refs

These models were inspected through the running MPS instance with `projectPath=/home/rocketdan/migration/2026_1/eFWWS`. They are application examples, not a dedicated sandbox. Re-resolve refs before use because examples may change. Keep skill files in `moai_ware`, and route MCP calls to the MPS project that owns the model.

| Example | Node ref | What to inspect |
| --- | --- | --- |
| `WarenGruppe` Entity | `r:84369f59-1457-4da0-87e2-44b592195158(at.mpreis.erp.stammdaten.extern.warenGruppe)/3537458515767883376` | Small Entity with five `businessProperties` and three BaseLanguage members |
| `WarenGruppe.id` BusinessProperty | `r:84369f59-1457-4da0-87e2-44b592195158(at.mpreis.erp.stammdaten.extern.warenGruppe)/3537458515767883382` | Required `type`/`propertyImplementation`, public visibility, ManMap key option |
| `NeuerWarenBeleg` Service | `r:17ebe0d0-ed17-40bb-b8a1-6db1918885ec(at.mlab.erp.wws.domain.lager)/1805084501161900826` | Service methods in `member` |
| `WarenPosGruppe` DTO | `r:17ebe0d0-ed17-40bb-b8a1-6db1918885ec(at.mlab.erp.wws.domain.lager)/4698263724088712737` | DTO shape |
| `BewInfo` ValueObject | `r:17ebe0d0-ed17-40bb-b8a1-6db1918885ec(at.mlab.erp.wws.domain.lager)/128458200777810907` | ValueObject shape |
| `Ergebnisse nach Inventurgruppe anzeigen` Command | `r:d9e8432b-9cea-4212-a0b1-142039bf3fd7(at.mlab.erp.wws.unit.bestandsInfo)/2593803359164753595` | Command with page, init, parameter, variable, icon, documentation |
| `AppConfSmartFX8_Lokal` OFXConfig | `r:73f2a41e-97cd-44b4-ad23-a33e3f98e164(at.mpreis.erp.tech.configs)/7084066082766545304` | Configuration target used by a DataUX app module |

Model refs: `r:84369f59-1457-4da0-87e2-44b592195158(at.mpreis.erp.stammdaten.extern.warenGruppe)`, `r:17ebe0d0-ed17-40bb-b8a1-6db1918885ec(at.mlab.erp.wws.domain.lager)`, and `r:d9e8432b-9cea-4212-a0b1-142039bf3fd7(at.mlab.erp.wws.unit.bestandsInfo)`.

Use `mps_mcp_print_node(deep=false)` for a root overview. Print an individual child with `deep=true` when building a reusable subtree; `WarenGruppe.id` was the source for `blueprints/business-property-int-subtree.json`. Query instances with `mps_mcp_query_nodes(FIND_INSTANCES, sampleOnly=true)` when a recorded ref no longer resolves.
