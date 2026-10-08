# ManMap Gotchas

## Runtime semantics (documentation)

- Loading, identity map, read-only vs checkout (`IllegalStateException` on mode mismatch), no-key results outside the identity map: see [Explizites Laden](../../../docu/manmap.md#explizites-laden), [Read-only, Checkout und Session-Identität](../../../docu/manmap.md#read-only-checkout-und-session-identität), [Dirty-Tracking, Read-only](../../../docu/objectflow.md#dirty-tracking-read-only-und-unveränderliche-werte).
- Save writes only the selected mapping's columns, no cascade on save/delete, a repository call is no transaction boundary, direct SQL in the session-operation flow: see [Speichern von Objektgraphen](../../../docu/manmap.md#speichern-von-objektgraphen), [Löschen mit `delete with`](../../../docu/manmap.md#löschen-mit-delete-with), [Explizite Session-Operationen](../../../docu/objectflow.md#explizite-session-operationen), [Grundprinzipien](../../../docu/moware-werkbank.md#grundprinzipien-für-die-anwendungsentwicklung).
- Filter operators (`==`/`!=`, `<`…`>=`, `in`, `like`, `optional`), `TO_LOCALDATE`, joins and the fields available in `where`/`sortBy`: see [Filterausdrücke](../../../docu/manmap.md#spezifikum---filterausdrücke-und-gemappte-felder).
- Auto-ID (simple keys only), insert/update decision, `BATCH`, alternate tables, schema options, supported databases, C2 parameter forms, `debugMe`: see [Automatische IDs und Sequences](../../../docu/manmap.md#automatische-ids-und-sequences), [Insert oder Update](../../../docu/manmap.md#insert-oder-update), [Save-Optionen](../../../docu/manmap.md#save-optionen), [Alternative Tabellen](../../../docu/manmap.md#alternative-tabellen), [Datenbankportabilität und Schema](../../../docu/manmap.md#datenbankportabilität-und-schema), [Custom SQL](../../../docu/manmap.md#custom-sql-mit-sql), [Parameter in SQL-Text](../../../docu/manmap.md#parameter-in-sql-text).

## Modeling and tooling

- JSON uses fully qualified concepts even when shallow MPS prints display short names.
- The role spelling `atomMpig` is intentional.
- Never put concept references (`c:`) into roles that expect declaration nodes (`r:`).
- Large repositories can produce multi-megabyte deep prints. Query or print the smallest relevant method/subtree.
- A globally visible shipped example may not appear in project-scoped name search. Use its explicit model/node reference or `includeStubModules=true`.
- Dry-run and write operations target the dynamically selected application project; do not attempt to mutate a read-only/global example.
