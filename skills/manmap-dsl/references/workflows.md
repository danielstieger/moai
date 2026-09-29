# ManMap Workflows

## Create a Persistence Description

Source semantics: [Persistence Description and mapping capabilities](../../../docu/manmap.md#persistence-description-und-mapping-möglichkeiten), [entity-mapping structure](../../../docu/manmap.md#aufbau-eines-entity-mappings), and [fields, keys, and options](../../../docu/manmap.md#felder-schlüssel-und-optionen).

1. Determine the target project dynamically and resolve the editable target model.
2. Resolve ObjectFlow entity and property declaration nodes in that model.
3. Dry-run and insert [persistence-description-skeleton.json](blueprints/persistence-description-skeleton.json).
4. Add one [entity-mapping-subtree.json](blueprints/entity-mapping-subtree.json) under `persistenceMapping` at a time.
5. Add field, reference, embedded, list, or include mappings under the exact role `atomMpig`.
6. Keep `OptimisticOption` on new writable mappings unless the application has a documented reason not to use it.
7. Validate after every entity mapping and after the full root.

Use [field-mapping-subtree.json](blueprints/field-mapping-subtree.json), [reference-mapping-subtree.json](blueprints/reference-mapping-subtree.json), [embedded-mapping-subtree.json](blueprints/embedded-mapping-subtree.json), and one of the two list templates. Table/column/sequence values are `StringLiteral` children.

## Create or Extend a Repository

Source semantics: [repositories and the four method kinds](../../../docu/manmap.md#repositories-und-die-vier-methodenarten) and [ObjectFlow explicit session operations](../../../docu/objectflow.md#explizite-session-operationen).

1. Load `mps-baselanguage` and `mps-node-editing`.
2. Insert [repository-skeleton.json](blueprints/repository-skeleton.json), or identify the existing root and preserve its ID.
3. Add one `RepositoryInstanceMethodDeclaration` under inherited role `member`; [repository-method-skeleton.json](blueprints/repository-method-skeleton.json) is a minimal void-body starting point.
4. Build the BaseLanguage return type, parameters, body, and visibility before adding ManMap operations.
5. Resolve mapping references against the persistence root used by the target model.
6. Add query/save/delete/SQL subtrees surgically.
7. Validate the root, then generate/build the owning solution.

Repository method type states intent but does not create a transaction boundary and does not replace `QueryFromMap.readOnly` or join load modes.

## Build a Mapped Query

Source semantics: [mapped `get`/`where` queries](../../../docu/manmap.md#gemappte-abfragen-mit-getwhere-auf-einem-mapping), [explicit loading](../../../docu/manmap.md#explizites-laden), and [read-only, checkout, and session identity](../../../docu/manmap.md#read-only-checkout-und-session-identität).

1. Choose the source `EntityMapping`.
2. Choose `readOnly=true` for inspection/search or `false` for checkout/editing according to the enclosing repository method.
3. Add required `RefJoinOption` or `ListJoinOption` children before expressions that refer to joined mappings.
4. Add exactly the intended operations in projection order: `GetQuery` or `WhereQuery`, then optional sort/limit/size operations.
5. Build `MappingReference` nodes with both `mappingSource` and `fieldMapping` references.
6. Validate types on both sides of every comparison.

[query-from-map-where-subtree.json](blueprints/query-from-map-where-subtree.json) provides a structurally complete neutral filter that must be replaced with the real predicate.

## Save or Delete a Graph

Source semantics: [`save with`](../../../docu/manmap.md#speichern-mit-save-with), [saving object graphs](../../../docu/manmap.md#speichern-von-objektgraphen), [`delete with`](../../../docu/manmap.md#löschen-mit-delete-with), and [ObjectFlow session and unit of work](../../../docu/objectflow.md#session-und-unit-of-work).

Use [save-with-map-subtree.json](blueprints/save-with-map-subtree.json) or [delete-with-map-subtree.json](blueprints/delete-with-map-subtree.json) inside a repository method body.

- Save the parent with its own mapping.
- Propagate parent keys/back-references to children explicitly.
- Save every child with its own mapping.
- Delete children in a relationally valid order before deleting the parent.
- Register database-changing methods as ObjectFlow session operations when their effect belongs to successful command completion.

Without a forced option, save decides insert versus update from key nullness. For composite keys, prefer an explicit insert/update option.

## Direct SQL and Read Models

Source semantics: [Custom SQL](../../../docu/manmap.md#custom-sql-mit-sql), [parameter binding](../../../docu/manmap.md#parameter-in-sql-text), [row/no-key mappers](../../../docu/manmap.md#row-mapper-und-no-key-mapper), and [the read-model workflow](../../../docu/manmap.md#lesemodell-mit-custom-sql-verwenden).

1. Choose `C2SqlBlock.sqlType=QUERY` for rows or `STATEMENT` for an update count.
2. Compose SQL from reached `C2SqlText` statements. Use bound variables/property/status references, not text concatenation of values.
3. For a small scalar query, use an inline closure or `RowMapperFieldRef`.
4. For DTO/projection/aggregate rows without a usable key, define a `NoKeyMapperField` and reference it from the SQL block.
5. Match SQL aliases exactly to mapper field names and target properties.
6. Treat no-key results as read-only and outside the session identity map.

Use [custom-sql-statement-subtree.json](blueprints/custom-sql-statement-subtree.json) for the statement shape and [no-key-mapper-subtree.json](blueprints/no-key-mapper-subtree.json) for a portable DTO mapper. For a query mapping expression, inspect the focused shipped examples and resolve the mapper member in the target repository.

## Edit Existing Models

Use `mps_mcp_update_node` for a property, reference, or single containment role. Do not replace a complete persistence or repository root merely to change a table name, column name, predicate, load option, or save option. Repository nodes commonly point to mapping IDs, so ID preservation matters.

When an application change crosses language boundaries, use [where a change belongs](../../../docu/moware-werkbank.md#wo-gehört-eine-änderung-hin) before editing ManMap, ObjectFlow, or DataUX nodes.
