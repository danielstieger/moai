# ManMap Workflows

## Create a Persistence Description

Source semantics: [Persistence Description and mapping capabilities](../../../docu/manmap.md#persistence-description-und-mapping-möglichkeiten) and [fields, keys, and options](../../../docu/manmap.md#felder-schlüssel-und-optionen).

1. Pass `projectPath` in every call (`moai:mps-mcp-workflow`, "Which project the tools act on") and resolve the editable target model; placement and name: conventions `anwendungsaufbau`.
2. Resolve ObjectFlow entity and property declaration nodes in that model.
3. Dry-run and insert [persistence-description-skeleton.json](blueprints/persistence-description-skeleton.json).
4. Add one [entity-mapping-subtree.json](blueprints/entity-mapping-subtree.json) under `persistenceMapping` at a time; always give `tableName`.
5. Add field, reference, embedded, list, or include mappings under the exact role `atomMpig`.
6. Keep `OptimisticOption` on new writable mappings unless the application has a documented reason not to use it.
7. After each write check `fixReferences.stillBroken` (must be 0); validate after every entity mapping and after the full root.

Use [field-mapping-subtree.json](blueprints/field-mapping-subtree.json), [reference-mapping-subtree.json](blueprints/reference-mapping-subtree.json), [embedded-mapping-subtree.json](blueprints/embedded-mapping-subtree.json), and one of the two list templates. Table/column/sequence values are `StringLiteral` children.

## Create or Extend a Repository

Source semantics: [repositories and the four method kinds](../../../docu/manmap.md#repositories-und-die-vier-methodenarten) and [ObjectFlow explicit session operations](../../../docu/objectflow.md#explizite-session-operationen).

1. Load `moai:mps-baselanguage` and `moai:mps-node-editing`.
2. Insert [repository-skeleton.json](blueprints/repository-skeleton.json), or identify the existing root and preserve its ID. Which repository holds which method, placement and name: conventions `anwendungsaufbau`.
3. Add one `RepositoryInstanceMethodDeclaration` under inherited role `member`; [repository-method-skeleton.json](blueprints/repository-method-skeleton.json) is a minimal void-body starting point.
4. Write the methods as Java with markers (`GET`, `WHERE`, `SAVE`, `DELETE`, `SQL`) and convert them with `moai/tools/text2of.py`, setting the method kind with `--repo-type` (`moai:objectflow-dsl`, `references/workflows.md`, "Write method bodies and command functions").
5. Resolve mapping references against the persistence root used by the target model.
6. Add query/save/delete/SQL subtrees surgically.
7. Validate the root (several changed roots: the model reference with `perRoot=true`), then generate/build the owning solution.

Method kind vs `QueryFromMap.readOnly` and the transaction boundary: see [Repositories und die vier Methodenarten](../../../docu/manmap.md#repositories-und-die-vier-methodenarten).

## Build a Mapped Query

Source semantics: [mapped `get`/`where` queries](../../../docu/manmap.md#gemappte-abfragen-mit-queryfrommap), [explicit loading](../../../docu/manmap.md#explizites-laden), and [read-only, checkout, and session identity](../../../docu/manmap.md#read-only-checkout-und-session-identität).

1. Choose the source `EntityMapping`.
2. Choose `readOnly=true` for inspection/search or `false` for checkout/editing according to the enclosing repository method.
3. Add required `RefJoinOption` or `ListJoinOption` children before expressions that refer to joined mappings.
4. Add exactly the intended operations in projection order: `GetQuery` or `WhereQuery`, then optional sort/limit/size operations.
5. Build `MappingReference` nodes with both `mappingSource` and `fieldMapping` references. In a blueprint, set `mappingSource` to the name of the query's `EntityMapping` as a plain name (e.g. `"MapRechnung"`); it resolves to the enclosing `QueryFromMap`, even when the query is inserted in the same blueprint. For joined mappings use the joined mapping's name. The dry-run does not look up these names; after the real write `fixReferences.stillBroken` must be 0.
6. Validate types on both sides of every comparison: `mps_mcp_query_nodes` `GET_TYPE` for each operand, `mps_mcp_query_types` (`IS_SUBTYPE`, `COMMON_SUPERTYPE`, `EXPLAIN_TYPE`) to decide whether they fit; see `moai:mps-mcp-workflow` (`references/type-queries.md`).

[query-from-map-where-subtree.json](blueprints/query-from-map-where-subtree.json) provides a complete `where` query that compares a mapped field with a parameter in one blueprint.

## Save or Delete a Graph

Source semantics: [`save with`](../../../docu/manmap.md#speichern-mit-save-with), [saving object graphs](../../../docu/manmap.md#speichern-von-objektgraphen), [`delete with`](../../../docu/manmap.md#löschen-mit-delete-with), and [ObjectFlow session and unit of work](../../../docu/objectflow.md#session-und-unit-of-work).

Use [save-with-map-subtree.json](blueprints/save-with-map-subtree.json) or [delete-with-map-subtree.json](blueprints/delete-with-map-subtree.json) inside a repository method body.

- Order of saving/deleting a graph: see [Speichern von Objektgraphen](../../../docu/manmap.md#speichern-von-objektgraphen) and [Löschen mit `delete with`](../../../docu/manmap.md#löschen-mit-delete-with).
- Register database-changing methods as ObjectFlow session operations when their effect belongs to successful command completion.

Insert versus update without a forced option, composite keys: see [Insert oder Update](../../../docu/manmap.md#insert-oder-update).

## Direct SQL and Read Models

Source semantics: [Custom SQL](../../../docu/manmap.md#custom-sql-mit-sql), [parameter binding](../../../docu/manmap.md#parameter-in-sql-text), [row/no-key mappers](../../../docu/manmap.md#row-mapper-und-nokeystoreread-only-map), and [the read-model workflow](../../../docu/manmap.md#lesemodell-mit-custom-sql-verwenden).

1. Choose `C2SqlBlock.sqlType=QUERY` for rows or `STATEMENT` for an update count. A `STATEMENT` needs an explicit empty `mapping` role; otherwise the node factory adds a `row` mapping closure and the checker rejects it.
2. Compose SQL from reached `C2SqlText` statements. Use bound variables/property/status references, not text concatenation of values.
3. For a small scalar query, use an inline closure or `RowMapperFieldRef`.
4. For DTO/projection/aggregate rows without a usable key, define a `NoKeyMapperField` and reference it from the SQL block.
5. Match SQL aliases exactly to mapper field names and target properties.

Use [custom-sql-statement-subtree.json](blueprints/custom-sql-statement-subtree.json) for the statement shape and [no-key-mapper-subtree.json](blueprints/no-key-mapper-subtree.json) for a portable DTO mapper. For a query mapping expression, inspect the focused shipped examples and resolve the mapper member in the target repository.

## Edit Existing Models

Use `mps_mcp_update_node` for a property, reference, or single containment role. Do not replace a complete persistence or repository root merely to change a table name, column name, predicate, load option, or save option. Repository nodes commonly point to mapping IDs, so ID preservation matters.

- Delete a child: `SET CHILD` without `childJson`; the returned reference is the parent's.
- Clear a property or reference: unquoted `null` as the third element of the triplet. Never write an empty enum value `""`; omit the property instead.
- Delete a root: `mps_mcp_update_root_node_from_json` with `operation:"DELETE"`.
- Clone a field mapping, mapping, or repository method within the same model with `mps_mcp_alter_nodes` `COPY_NODE`, then retarget its references. Shipped examples cannot be copied in this way.
- Checker problems with a quick fix: `quickFixes` in the validation report (`autoApplyQuickFixes`), or `mps_mcp_list_node_intentions` and `mps_mcp_apply_intention`.

When an application change crosses language boundaries, use [where a change belongs](../../../docu/moware-werkbank.md#wo-gehört-eine-änderung-hin) before editing ManMap, ObjectFlow, or DataUX nodes.
