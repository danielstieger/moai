# ManMap Workflows

## Create A Persistence Description

1. Resolve the editable target model and the domain `ClassConcept`/`Property` node refs.
2. Dry-run and insert `persistence-description-skeleton.json`.
3. Add one `EntityMapping` at a time under `persistenceMapping`, starting from `entity-mapping-subtree.json`.
4. Add `FieldMapping`, `ReferenceMapping`, `EmbeddedMapping`, `ListMapping`, or `IncludeMapping` nodes under `atomMpig`.
5. Add `OptimisticOption` under `tableOption` for a new writable entity mapping; see [advanced options](advanced-options.md).
6. Set table/column/sequence names as BaseLanguage `StringLiteral` children, not plain properties.
7. Validate after each entity mapping and again after the full root is assembled.

Relationship subtrees: [reference](blueprints/reference-mapping-subtree.json), [embedded ValueObject](blueprints/embedded-mapping-subtree.json), [list via mapped back-reference](blueprints/list-mapping-backref-subtree.json), and [list via key-only reference](blueprints/list-mapping-key-only-subtree.json). Match their required node references to the target domain declarations and inspect the permanent `Domain.PersDesc` example for context.

For a small single-entity mapping a full-root JSON insert is reasonable. For roots comparable to `PersDesc`, always use skeleton plus subtrees; a single large blueprint is hard to review and likely to exceed tool limits.

## Create Or Extend A Repository

1. Load `mps-baselanguage` and `mps-node-editing` in addition to this skill.
2. Insert `repository-skeleton.json`, or update an existing repository surgically.
3. Add one `RepositoryInstanceMethodDeclaration` under inherited role `member`.
4. Construct the BaseLanguage return type, parameters, body, and visibility before adding ManMap operations.
5. Resolve all query/save mapping references against the persistence root used by this model.
6. Add query operations in editor order: joins/options, filtering/get, sorting, limiting, sizing/reload as appropriate.
7. Validate the repository root and generate the owning solution to catch type-system and generator issues.

Use a live method from `RepoInvoice` as a focused template. Print that method node, not the entire repository, then replace its external references and local declaration refs carefully.

## Direct SQL with C2
 
For SQL values and named parameters, see [C2 parameters](c2-parameters.md).

Use `C2SqlRepo` for direct SQL. `C2SqlBlock` contains SQL statements and an optional mapping expression. Select an inline row-mapping closure or `RowMapperFieldRef` for a small/simple result and `NoKeyMapperFieldRef` when there is no usable key. Define result fields within `NoKeyMapperField.atomMpig`; use `IncludeMapping` there only when an existing `EntityMapping` is suitable. For aggregates, prefer an ObjectFlow DTO as the ephemeral result. Inspect a focused live subtree and follow [the C2 recipe](direct-sql.md).

## Mapped Queries, Save, and Delete

Use [the mapped-operations reference](mapped-operations.md) for `get` versus `where`, the `SaveWithMap` insert/update decision, and the loaded-key precondition for `DeleteWithMap`.
For `in`, `like`, optional filters, sorting, and limits, use [mapped query operators](query-operators.md).

## Editing Existing Models

Prefer `mps_mcp_update_node` for properties, references, or one containment role. Do not replace a complete persistence/repository root merely to change a table name, column mapping, predicate, or save option. Persistent mapping IDs are referenced by repository nodes and must remain stable.
