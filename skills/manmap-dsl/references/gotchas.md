# ManMap Gotchas

## Runtime semantics (documentation)

- Loading, identity map, read-only vs checkout (`IllegalStateException` on mode mismatch), no-key results outside the identity map: see [Explizites Laden](../../../docu/manmap.md#explizites-laden), [Read-only, Checkout und Session-Identität](../../../docu/manmap.md#read-only-checkout-und-session-identität), [Dirty-Tracking, Read-only](../../../docu/objectflow.md#dirty-tracking-read-only-und-unveränderliche-werte).
- Save writes only the selected mapping's columns, no cascade on save/delete, a repository call is no transaction boundary, direct SQL in the session-operation flow: see [Speichern von Objektgraphen](../../../docu/manmap.md#speichern-von-objektgraphen), [Löschen mit `delete with`](../../../docu/manmap.md#löschen-mit-delete-with), [Explizite Session-Operationen](../../../docu/objectflow.md#explizite-session-operationen), [Grundprinzipien](../../../docu/moware-werkbank.md#grundprinzipien-für-die-anwendungsentwicklung).
- Filter operators (`==`/`!=`, `<`…`>=`, `in`, `like`, `optional`), `TO_LOCALDATE`, joins and the fields available in `where`/`sortBy`: see [Filterausdrücke](../../../docu/manmap.md#spezifikum---filterausdrücke-und-gemappte-felder).
- Auto-ID (simple keys only), insert/update decision, `BATCH`, alternate tables, schema options, supported databases, C2 parameter forms, `debugMe`: see [Automatische IDs und Sequences](../../../docu/manmap.md#automatische-ids-und-sequences), [Insert oder Update](../../../docu/manmap.md#insert-oder-update), [`BATCH`](../../../docu/manmap.md#batch), [Alternative Tabellen](../../../docu/manmap.md#alternative-tabellen), [Datenbankportabilität und Schema](../../../docu/manmap.md#datenbankportabilität-und-schema), [Custom SQL](../../../docu/manmap.md#custom-sql-mit-sql), [Parameter in SQL-Text](../../../docu/manmap.md#parameter-in-sql-text).

## Modeling and tooling

- JSON uses fully qualified concepts even when shallow MPS prints display short names.
- The role spelling `atomMpig` is intentional.
- Never put concept references (`c:`) into roles that expect declaration nodes (`r:`). The insert accepts them silently and leaves them unresolved; only `mps_mcp_check_root_node_problems` reports them.
- Large repositories can produce multi-megabyte deep prints. Query or print the smallest relevant method/subtree.
- A globally visible shipped example may not appear in project-scoped name search. Use its explicit model/node reference or `includeStubModules=true`.
- Dry-run and write operations target the application project named by `projectPath`; do not attempt to mutate a read-only/global example.
- The dry-run does not look up names and runs no node factories. A forgotten `$TARGET_…$` reference placeholder is rejected only up to 20 characters ("looks like an MPS XML short ID"); longer ones get the general name warning, and text placeholders pass unchecked. Search for `TARGET_` before writing and check `fixReferences.stillBroken` after.
- Never write an empty enum value `""` (`sqlType`, `repoMethodType`); omit the property. Literals: `mps_mcp_query_structure` `GET_ENUMERATION_LITERALS`.

## Node factories

ManMap and ObjectFlow node factories run for every node a real write creates, with the actual enclosing node; the dry-run does not run them. A factory fills only the roles the blueprint omits. A role the blueprint names replaces the factory's content, also as an empty role `{"role":"…","nodes":[]}`, which suppresses factory content deliberately. `mps_mcp_query_structure` `LIST_CONCEPT_ASPECTS` shows whether a concept has a factory; `mps_mcp_print_node` shows what it added.

| Concept | Factory adds | Consequence |
| --- | --- | --- |
| `C2SqlBlock` | a `mapping` closure with parameter `row`, also for `sqlType=STATEMENT` | Three checker errors on a statement ("Mappings are only supported for queries…"). [custom-sql-statement-subtree.json](blueprints/custom-sql-statement-subtree.json) names an empty `mapping` role. |
| ObjectFlow `Entity` | an `int id` key property with `AutoidOption` | An additional `AutoidOption` in the `FieldMapping` is reported as "overruled with an option in the Entity". Use [autoid-option-subtree.json](blueprints/autoid-option-subtree.json) only for keys without their own AUTOID. |
| `EntityMapping` | an `OptimisticOption` when `tableOption` is omitted; `tableName` stays empty | Always give `tableName`. |
| `RepositoryInstanceMethodDeclaration` | `READONLY`, `resolveInfo`, `VoidType`, `PublicVisibility` | Harmless; only `body` is needed. |
| `QueryFromMap` | `readOnly=true`; an abstract placeholder when `queryOperation` is omitted | Always give `queryOperation`. |

Inserts may also add explicit used languages to the model (ObjectFlow, BaseLanguage, collections, closures, ManMap) although the DevKit already provides them; this is harmless.
