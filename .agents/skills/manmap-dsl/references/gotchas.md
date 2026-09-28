# ManMap Gotchas

## Loading and Identity

Sources: [ManMap explicit loading](../../../../docu/manmap.md#explizites-laden), [read-only, checkout, and session identity](../../../../docu/manmap.md#read-only-checkout-und-session-identität), and [ObjectFlow dirty tracking/read-only](../../../../docu/objectflow.md#dirty-tracking-read-only-und-unveränderliche-werte).

- `ReferenceMapping` and `ListMapping` describe relationships; they do not load them.
- Accessing an unloaded reference throws `org.modellwerkstatt.objectflow.runtime.OFXNotInitializedException`.
- An unloaded list appears empty, so `size == 0` does not prove the database has no children.
- `QueryFromMap` results participate in the ObjectFlow session identity map. Repeated read-only loads reuse the same instance; checking out an already mutable instance again can throw `IllegalStateException`.
- `NoKeyMapperField` results are always read-only and remain outside the session identity map, even if `IncludeMapping` reuses entity field mappings.

## Save, Delete, and Transactions

Sources: [saving object graphs](../../../../docu/manmap.md#speichern-von-objektgraphen), [`delete with`](../../../../docu/manmap.md#löschen-mit-delete-with), [ObjectFlow explicit session operations](../../../../docu/objectflow.md#explizite-session-operationen), and [session and unit of work](../../../../docu/objectflow.md#session-und-unit-of-work).

- `SaveWithMap` writes only columns in the selected mapping. It can write a mapped foreign key but never saves the referenced entity or list elements automatically.
- `DeleteWithMap` does not cascade. Delete dependents explicitly in the correct order.
- Repository invocation is not a transaction boundary. ObjectFlow commands/session owners coordinate session operations, transaction execution, commit, and cancellation.
- Database-changing direct SQL that belongs to command success must follow the same session-operation lifecycle.

## Queries and References

Sources: [mapped query semantics](../../../../docu/manmap.md#gemappte-abfragen-mit-getwhere-auf-einem-mapping), [references, embedded values, and lists](../../../../docu/manmap.md#referenzen-eingebettete-werte-und-listen), and [limits of included mappings](../../../../docu/manmap.md#grenzen-von-mapping-einbinden).

- `MappingReference` requires both `mappingSource` and `fieldMapping`. It cannot point directly to an `EntityMapping` as a custom-SQL row mapper.
- Only declared joins add mapping instances to query scope.
- `optional` omits predicates for `0` (`int`) and `null` (supported reference/value types); it does not support `boolean`. These rules differ from save key-nullness.
- Use `TO_LOCALDATE` when comparing a mapped date/time value as `LocalDate`; ensure the other operand is type-compatible.
- Never put concept references (`c:`) into roles that expect declaration nodes (`r:`).

## Keys and Options

Sources: [automatic IDs and sequences](../../../../docu/manmap.md#automatische-ids-und-sequences), [insert or update](../../../../docu/manmap.md#insert-oder-update), [save options](../../../../docu/manmap.md#save-optionen), and [database portability and schema](../../../../docu/manmap.md#datenbankportabilität-und-schema).

- Automatic IDs support a simple key, not a composite key.
- Default save treats integer `null`, `0`, `-1`; string `null`, `""`; and documented composite-key component values as unassigned. Use explicit insert/update for composite keys.
- `BATCH` is for collections, not an incidental option for a single object.
- An alternate table changes the physical target only; it is not a new mapping instance.
- Schema options describe metadata and requirements. ManMap is not a general database schema migration engine.

## SQL

Sources: [Custom SQL](../../../../docu/manmap.md#custom-sql-mit-sql), [SQL parameter binding](../../../../docu/manmap.md#parameter-in-sql-text), [row/no-key mappers](../../../../docu/manmap.md#row-mapper-und-no-key-mapper), and [database portability](../../../../docu/manmap.md#datenbankportabilität-und-schema).

- ManMap supports Oracle and MySQL, but custom SQL remains dialect-specific.
- SQL row access by index follows JDBC and starts at `1`.
- Prefer specific C2 variable/property/status nodes and named parameters. Use free SQL integration only for legacy or strongly dynamic fragments.
- Check generated SQL/parameters with `debugMe` only as a diagnostic aid, not as a normal runtime setting.

## Tooling

- JSON uses fully qualified concepts even when shallow MPS prints display short names.
- The role spelling `atomMpig` is intentional.
- `PersistenceDescription` and `Repository` are the only rootable ManMap concepts.
- Large repositories can produce multi-megabyte deep prints. Query or print the smallest relevant method/subtree.
- A globally visible shipped example may not appear in project-scoped name search. Use its explicit model/node reference or `includeStubModules=true`.
- Dry-run and write operations target the dynamically selected application project; do not attempt to mutate a read-only/global example.

For diagnosis beyond these checks, consult [ManMap frequent errors and diagnosis](../../../../docu/manmap.md#häufige-fehler-und-diagnose), [ObjectFlow frequent errors and diagnosis](../../../../docu/objectflow.md#häufige-fehler-und-diagnose), and the [documentation source coverage](source-coverage.md).
