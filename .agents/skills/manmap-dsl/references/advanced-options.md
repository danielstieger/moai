# Mapping and operation options

Use `OptimisticOption` as the normal protection for a new, writable entity mapping. It is a child of `EntityMapping.tableOption` and has no own fields. The permanent `Domain.NewInvoicePosDesc` example contains it; the `Graph load/save` tests include a double-write conflict case. The language author recommends it for entities.

Use `CreatedAtFieldOption`, `CreatedByFieldOption`, `ModifiedAtFieldOption`, or `ModifiedByFieldOption` on a `FieldMapping.mappingOption` when the entity needs the corresponding audit information. Inspect the permanent `Audit` suite for insert/update behavior. `ForceAuditSaveOption` and `SkipAuditSaveOption` occur under `SaveWithMap.options` when a particular save needs to override the normal audit handling.

Use `BatchSaveOption` under `SaveWithMap.options` when inserting or updating many objects quickly through JDBC batch mode. Start from the permanent `Graph load/save` batch tests and verify the surrounding method; do not add it to a one-object save merely because it exists.

For an archive or another physical table for the same mapping, declare `AdditionalTableName` under `EntityMapping.tableOption`. Its `name` identifies the alternative and its `tablename` child is a required BaseLanguage `StringLiteral` naming the SQL table. Select it with `AdditionalTableReference`, whose `alternativeAccess` reference targets that declaration and whose required `condition` is a BaseLanguage expression. `Domain.RepoInvoiceArchiv` shows this option in three places: `QueryFromMap.joinOption`, `SaveWithMap.options`, and `DeleteWithMap.options`. A joined query may need the corresponding alternative-table selection for its joined mappings too; inspect the `RepoInvoiceArchiv` full-join example before assembling one.

These options change behavior; copy their exact MPS shape from a focused permanent example and validate the owning root. The [optimistic option blueprint](blueprints/optimistic-option-subtree.json) is the minimal table option shape.
