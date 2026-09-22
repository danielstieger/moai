# DataUX examples in `simpleone`

## Project and module

- Open MPS project: `/home/rocketdan/migration/2026_1/simpleone`
- Example module: `f6ea4529-b826-49cb-a717-2ac43f8ba5f5(org.modellwerkstatt.simple)`
- Application model: `r:579ac6f7-5136-4b5d-93d4-60d7664141bd(org.modellwerkstatt.simple.app)`
- Rich UI model: `r:9a5d071c-824e-4204-b68c-cfe03dc3bd00(org.modellwerkstatt.simple.order.unitOrderHandling)`
- Invoice UI model: `r:a45417bc-e0f5-409d-9810-db4068333b13(org.modellwerkstatt.simple.invoice.unitInvoice)`

## Representative PagePanes

| Example | Stable root reference | Why inspect it |
| --- | --- | --- |
| `PPOrderEditor` | `r:9a5d071c-824e-4204-b68c-cfe03dc3bd00(org.modellwerkstatt.simple.order.unitOrderHandling)/7314559125540380517` | Master/detail GridLayout with list-bound Table, object-bound DelegateForm, delegate options, menu and submenu |
| `Search Order Pane` | `r:9a5d071c-824e-4204-b68c-cfe03dc3bd00(org.modellwerkstatt.simple.order.unitOrderHandling)/6871219927627843893` | Compact search form containing reference, date, status, string, decimal, and integer delegates |
| `THE List of Orders` | `r:9a5d071c-824e-4204-b68c-cfe03dc3bd00(org.modellwerkstatt.simple.order.unitOrderHandling)/4169514245306418769` | Filter plus result table, selection, dynamic color, compound action and table options |
| `Invoice Editor` | `r:a45417bc-e0f5-409d-9810-db4068333b13(org.modellwerkstatt.simple.invoice.unitInvoice)/8026528294245641186` | Invoice editing UI |
| `Invoices Result List` | `r:a45417bc-e0f5-409d-9810-db4068333b13(org.modellwerkstatt.simple.invoice.unitInvoice)/8026528294243707351` | Search result PagePane |
| `PPInvoiceTbl` | `r:a45417bc-e0f5-409d-9810-db4068333b13(org.modellwerkstatt.simple.invoice.unitInvoice)/7309056827527211515` | Small table-oriented PagePane |

Additional focused models include `cases.LineChart`, `cases.articlePieChartUnit`, `cases.dynamicSearchUnit`, `cases.hookOption`, `cases.iframeUnit`, `cases.inheritUnit`, and `cases.uploadUnit`.

## Application and batchjob examples

- Desktop application `App_Desktop_Order`: `r:579ac6f7-5136-4b5d-93d4-60d7664141bd(org.modellwerkstatt.simple.app)/6871219927627844241`
  - configuration, configured component, auth function, main/extras/help menus, submenus, tiles, version, and official name
- Mobile/MDE application `App_MDE_Order`: `r:579ac6f7-5136-4b5d-93d4-60d7664141bd(org.modellwerkstatt.simple.app)/6871219927627844301`
  - mobile-oriented menu and tiles, tile initialization and module variables
- Batchjob `PrintingJob`: `r:579ac6f7-5136-4b5d-93d4-60d7664141bd(org.modellwerkstatt.simple.app)/5423396569854736805`
  - configuration, auth, exception strategy, producer/consumer pair, CRON, version, official name
- Batchjob `InvoicingJob`: `r:579ac6f7-5136-4b5d-93d4-60d7664141bd(org.modellwerkstatt.simple.app)/4731759461587253888`
- Small batch sample `JobInv26`: `r:e5edbbf4-9823-4900-bef5-349396e4cf20(org.modellwerkstatt.simple.cases.batchjob)/7027955313955471804`

These references were resolved with `mps_mcp_print_node` during skill generation. Re-resolve them before copying subtrees if `simpleone` has changed.

