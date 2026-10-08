# Blueprint Index and Placeholder Contract

Every JSON file in [blueprints](blueprints) uses fully qualified concept names and parses as JSON. The templates intentionally contain no application-project node IDs.

## Placeholder Contract

- Values named `$TARGET_*` are unresolved placeholders, not stable package references.
- Before insertion, resolve each placeholder in the target model's applicable reference scope. Replace it with an unambiguous target name or, preferably for overloaded/duplicate names, the target model's persistent `r:` reference.
- Text placeholders sit in property values and must be replaced with the intended text: `$TARGET_*_NAME$` (mapping, mapper, method, repository, persistence, sequence names), `$TARGET_TABLE$`, `$TARGET_COLUMN$`, `$TARGET_FOREIGN_KEY_COLUMN$`, `$TARGET_SQL_COLUMN_OR_ALIAS$` (column name or SQL alias in a `nokeystore/read-only map` field mapping), `$TARGET_ASSIGNMENT$` (the `column = value` part of the `UPDATE ... SET` statement), and `$TARGET_VIRTUAL_PACKAGE$`. Every other `$TARGET_*$` value is a reference target.
- A dry-run warning about a remaining `$TARGET_*` reference means the production write would create a dynamic reference. Do not accept that warning accidentally.

## Root Skeletons

- [persistence-description-skeleton.json](blueprints/persistence-description-skeleton.json)
- [repository-skeleton.json](blueprints/repository-skeleton.json)

## Mapping Subtrees

- [entity-mapping-subtree.json](blueprints/entity-mapping-subtree.json)
- [field-mapping-subtree.json](blueprints/field-mapping-subtree.json)
- [reference-mapping-subtree.json](blueprints/reference-mapping-subtree.json)
- [embedded-mapping-subtree.json](blueprints/embedded-mapping-subtree.json)
- [list-mapping-backref-subtree.json](blueprints/list-mapping-backref-subtree.json)
- [list-mapping-key-only-subtree.json](blueprints/list-mapping-key-only-subtree.json)
- [autoid-option-subtree.json](blueprints/autoid-option-subtree.json)

## Repository and Operation Subtrees

- [repository-method-skeleton.json](blueprints/repository-method-skeleton.json)
- [query-from-map-where-subtree.json](blueprints/query-from-map-where-subtree.json)
- [save-with-map-subtree.json](blueprints/save-with-map-subtree.json)
- [delete-with-map-subtree.json](blueprints/delete-with-map-subtree.json)
- [no-key-mapper-subtree.json](blueprints/no-key-mapper-subtree.json)
- [custom-sql-statement-subtree.json](blueprints/custom-sql-statement-subtree.json)

For complex BaseLanguage closures, method calls, or predicates, inspect a focused package-shipped node from [sandbox.md](sandbox.md), then rebuild the subtree with target-local references under the guidance of `moai:mps-baselanguage`.

