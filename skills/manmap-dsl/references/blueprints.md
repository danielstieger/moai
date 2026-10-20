# Blueprint Index and Placeholder Contract

Every JSON file in [blueprints](blueprints) uses fully qualified concept names and parses as JSON. The templates intentionally contain no application-project node IDs.

## Placeholder Contract

- Values named `$TARGET_*` are unresolved placeholders, not stable package references.
- Before insertion, resolve each placeholder in the target model's applicable reference scope. Replace it with an unambiguous target name or, preferably for overloaded/duplicate names, the target model's persistent `r:` reference.
- Text placeholders sit in property values and must be replaced with the intended text: `$TARGET_*_NAME$` (mapping, mapper, method, repository, persistence, sequence names), `$TARGET_TABLE$`, `$TARGET_COLUMN$`, `$TARGET_FOREIGN_KEY_COLUMN$`, `$TARGET_SQL_COLUMN_OR_ALIAS$` (column name or SQL alias in a `nokeystore/read-only map` field mapping), `$TARGET_ASSIGNMENT$` (the `column = value` part of the `UPDATE ... SET` statement; it is a single `Word`, so write it without spaces, e.g. `MENGE=0`, or add further `Word` nodes), and `$TARGET_VIRTUAL_PACKAGE$`. Every other `$TARGET_*$` value is a reference target.
- The dry-run does not look up names, so it does not reliably catch a remaining reference placeholder: up to 20 characters (e.g. `$TARGET_ENTITY$`) it is rejected as "looks like an MPS XML short ID", longer ones get only the general "is a name, not looked up" warning, and text placeholders are not checked at all. Search the filled blueprint for `TARGET_` before every write; any match stops the write. After the real write, `fixReferences.stillBroken` must be 0.

Send a filled blueprint inline (up to 4 KB; every file here is smaller minified) or copy it to `${TMPDIR:-/tmp}` and pass the copy's absolute path; the server rejects files under `skills/`. The format rules are in `moai:mps-node-editing` (`references/json-format.md`).

## Root Skeletons

- [persistence-description-skeleton.json](blueprints/persistence-description-skeleton.json)
- [repository-skeleton.json](blueprints/repository-skeleton.json)

Subtree blueprints are inserted with `mps_mcp_update_node` `ADD CHILD` under the parent role given after each file.

## Mapping Subtrees

- [entity-mapping-subtree.json](blueprints/entity-mapping-subtree.json): `PersistenceDescription.persistenceMapping`. Always give `tableName`; without `tableOption` the factory adds an `OptimisticOption`.
- [field-mapping-subtree.json](blueprints/field-mapping-subtree.json): `atomMpig`.
- [reference-mapping-subtree.json](blueprints/reference-mapping-subtree.json): `atomMpig`; its inner key field mapping sits in `keyMapping`.
- [embedded-mapping-subtree.json](blueprints/embedded-mapping-subtree.json): `atomMpig`.
- [list-mapping-backref-subtree.json](blueprints/list-mapping-backref-subtree.json): `atomMpig`.
- [list-mapping-key-only-subtree.json](blueprints/list-mapping-key-only-subtree.json): `atomMpig`.
- [autoid-option-subtree.json](blueprints/autoid-option-subtree.json): `FieldMapping.mappingOption`. Only for an entity whose key property has no AUTOID option of its own; the ObjectFlow entity factory already sets one on the key property, so this is normally unnecessary. With both, the checker reports "A AUTOID option is specified in this mapping, but overruled with an option in the Entity."

## Repository and Operation Subtrees

- [repository-method-skeleton.json](blueprints/repository-method-skeleton.json): `Repository.member`. The factory already sets `READONLY`, `resolveInfo`, `VoidType` and `PublicVisibility`; only `body` is required.
- [query-from-map-where-subtree.json](blueprints/query-from-map-where-subtree.json): an expression slot. Always give `queryOperation`; otherwise the factory leaves an abstract placeholder.
- [save-with-map-subtree.json](blueprints/save-with-map-subtree.json): `StatementList.statement`.
- [delete-with-map-subtree.json](blueprints/delete-with-map-subtree.json): `StatementList.statement`.
- [no-key-mapper-subtree.json](blueprints/no-key-mapper-subtree.json): `Repository.member`.
- [custom-sql-statement-subtree.json](blueprints/custom-sql-statement-subtree.json): an expression slot. The empty `mapping` role suppresses the factory's `row` closure, which a `STATEMENT` must not have.

For complex BaseLanguage closures, method calls, or predicates, inspect a focused package-shipped node from [sandbox.md](sandbox.md), then rebuild the subtree with target-local references under the guidance of `moai:mps-baselanguage` (closures and collections: `moai:baselanguage-collections-dsl`).

