# ManMap Concept and Role Map

The live MPS descriptor exposes 94 concepts. Exactly two are rootable: `PersistenceDescription` and `Repository`. No hollow runtime descriptors were observed during generation of this memory.

Use `mps_mcp_get_concept_details` again before relying on this inventory after a language upgrade. The language reference is recorded in the parent [SKILL.md](../SKILL.md). Use the FQ names from the Kapitellandkarten in JSON blueprints; resolve references, child roles and cardinalities via MPS MCP in the current project before changing a model.

## Root Concepts

For the semantic distinction between persistence mappings and repositories, see [the two ManMap access paths](../../../docu/manmap.md#die-zwei-zugriffswege-im-überblick) and [repositories and their four method kinds](../../../docu/manmap.md#repositories-und-die-vier-methodenarten).

| Fully qualified concept | Essential shape | Purpose |
| --- | --- | --- |
| `org.modellwerkstatt.manmap.structure.PersistenceDescription` | property `name`; child `persistenceMapping: EntityMapping[0..n]` | Groups class-to-table mappings. |
| `org.modellwerkstatt.manmap.structure.Repository` | extends BaseLanguage `ClassConcept`; inherited `member`, `visibility`, and class roles | Hosts repository methods and mapper fields. |

## Mapping Core

The domain meaning and composition rules are described in [Persistence Description and mapping capabilities](../../../docu/manmap.md#persistence-description-und-mapping-möglichkeiten), especially [references, embedded values, and lists](../../../docu/manmap.md#referenzen-eingebettete-werte-und-listen).

| Concept | References | Children |
| --- | --- | --- |
| `EntityMapping` | `classConcept -> ClassConcept[1]` | `tableName: StringLiteral[1]`, `tableOption: ITableOption[0..n]`, `atomMpig: IAtomMapping[0..n]` |
| `FieldMapping` | `property -> Property[1]` | `fieldName: StringLiteral[1]`, `mappingOption: FieldOption[0..n]` |
| `ReferenceMapping` | `property -> Property[1]` | `keyMapping: IKeyMapping[1]`, `atomMpig: IAtomMapping[0..n]` |
| `EmbeddedMapping` | optional `property -> Property[0..1]` | `atomMpig: IAtomMapping[0..n]` |
| `ListMapping` | `property -> Property[1]` | `mappedfieldRef: IReferenceMapping[1]` |
| `IncludeMapping` | optional `mapping -> IIncludeAbleMapsClassConcept[0..1]` | none |
| `MappedFieldRef` | optional `entityMapping`, optional `refMapping` | none |
| `KeyOnlyReferenceMapping` | optional `entityMapping`, optional `keyOnlyRef` | none |

The live child-role spelling is `atomMpig`; keep it exactly as written. Table names, column names, and sequence names are BaseLanguage `StringLiteral` children, not ManMap string properties.

## Mapping Options

Use the documentation for the runtime meaning of [fields, keys, and options](../../../docu/manmap.md#felder-schlüssel-und-optionen), [automatic IDs and sequences](../../../docu/manmap.md#automatische-ids-und-sequences), [optimistic locking and audit](../../../docu/manmap.md#optimistic-locking-und-audit), and [alternate tables](../../../docu/manmap.md#alternative-tabellen).

- Key and ID: `KeyOption`, `AutoidOption`, `OverWriteAutoIdOption`.
- Concurrency and audit: `OptimisticOption` (table option on `EntityMapping`, role `tableOption`), `CreatedAtFieldOption`, `CreatedByFieldOption`, `ModifiedAtFieldOption`, `ModifiedByFieldOption`.
- Schema metadata: `IndexOption`, `NotnullOption`, `SizeOption`, `UniqueOption`.
- Alternate storage: `AdditionalTableName` (table option on `EntityMapping`, role `tableOption`) declares a table; `AdditionalTableReference` (projected as `WHEN <condition> <name>`; child `condition` [1], reference `alternativeAccess`) uses it for an operation when the condition holds.

`AutoidOption.sequenceName` and `AdditionalTableName.tablename` each require a `StringLiteral`. `OverWriteAutoIdOption` references the affected `FieldMapping` and supplies another sequence-name literal.

## Repository Content

The AST inventory below complements the semantic rules in [repositories and the four method kinds](../../../docu/manmap.md#repositories-und-die-vier-methodenarten) and [read-only, checkout, and session identity](../../../docu/manmap.md#read-only-checkout-und-session-identität).

`RepositoryInstanceMethodDeclaration` extends BaseLanguage `InstanceMethodDeclaration`. Its `repoMethodType` enumeration is exactly `READONLY`, `CHECKOUT`, `CHECKIN`, or `DELETE`. It still requires the BaseLanguage `returnType` and `body` children.

Other reusable repository members include:

- `RowMapperField`: property `name`; required `rowMapper: ClosureLiteral`.
- `NoKeyMapperField`: property `name`; required `classConcept` reference; `atomMpig` field/include mappings. To reuse an `EntityMapping` for custom SQL results, put an `IncludeMapping` into its `atomMpig`; an `EntityMapping` cannot be referenced directly as a SQL row mapper.
- `SqlStringField`: property `name`; required `sqlString: SqlString`.
- `RowMapperFieldRef`, `NoKeyMapperFieldRef`, and `SqlStringFieldRef`: references to those members.

## Mapped Queries

For operation ordering, filter semantics, joins, and loading behavior, see [mapped `get`/`where` queries](../../../docu/manmap.md#gemappte-abfragen-mit-queryfrommap) and [explicit loading](../../../docu/manmap.md#explizites-laden).

`QueryFromMap` is an expression with required reference `entityMapping`, properties `readOnly` and `debugMe`, children `joinOption: IQueryOption[0..n]`, and `queryOperation: IQueryOperation[0..n]`.

| Concept | Essential shape |
| --- | --- |
| `GetQuery` | required `argument: Expression` |
| `WhereQuery` | required `filter: Expression` |
| `SortByQuery` | required `toComparable: Expression`; `sortDirection = ASC\|DESC` |
| `LimitQuery` | required `count: Expression` |
| `SizeQuery` | no additional child |
| `ReloadQuery` | required `argument: Expression` |
| `RefJoinOption` | references `refMapping` and target `entityMapping`; `readOnly = ReadOnly\|Checkout` |
| `ListJoinOption` | reference `listMapping`; `readOnly = ReadOnly\|Checkout` |
| `MappingReference` | references `mappingSource` and `fieldMapping`; `option = NOP\|TO_LOCALDATE\|TO_LOWERCASE\|TO_UPPERCASE` |
| `InOperation` | `operand: MappingReference`, `targetList: Expression` |
| `LikeOperator` | `operand: Expression`, `target: Expression` |
| `OptionalOperator` | `expression: Expression` |

`WhereQuery.filter`, `SortByQuery.toComparable` and `LimitQuery.count` take a plain `Expression`; the editor's brace/parameter projection of `where` is not a `ClosureLiteral` — never wrap the filter in a closure. `MappingReference` is itself an `Expression` (type = type of the referenced property), requires both `mappingSource` and `fieldMapping`, and is valid only inside `where`/`sortBy`.

Only joins present on the query extend the `MappingReference.mappingSource` scope. An alternate table is not a mapping instance and does not extend that scope.

## Save and Delete

The operational semantics are documented under [`save with`](../../../docu/manmap.md#speichern-mit-save-with), [saving object graphs](../../../docu/manmap.md#speichern-von-objektgraphen), and [`delete with`](../../../docu/manmap.md#löschen-mit-delete-with).

- `SaveWithMap`: statement; required `entityMapping` reference and `expression` child; optional `SaveOption` children.
- `DeleteWithMap`: statement; same essential shape.
- Save options: `InsertSaveOption`, `UpdateSaveOption`, `BatchSaveOption`, `ForceAuditSaveOption`, `SkipAuditSaveOption`, and `AdditionalTableReference`.

## Direct SQL (C2)

Use [Custom SQL](../../../docu/manmap.md#custom-sql-mit-sql), [SQL query versus statement](../../../docu/manmap.md#sql-query-und-sql-statement), [SQL parameter binding](../../../docu/manmap.md#parameter-in-sql-text), and [row/no-key mappers](../../../docu/manmap.md#row-mapper-und-no-key-mapper) for semantics and runtime behavior.

`C2SqlBlock` is an expression. `sqlType` is exactly `QUERY` or `STATEMENT`; `statements: StatementList[1]` contains reached `C2SqlText` statements, while optional `mapping: Expression[0..1]` maps query rows.

Key concepts are `C2SqlText`, `C2SqlWordVarReference`, `C2Dot`, `C2PropertyReference`, `C2EntityKeyPropReference`, `C2MethodReference`, `C2SqlStatusReference`, `C2SqlIntegration`, and `SqlNamedParameter`.

`C2SqlIntegration` has an optional `sqlString` expression, ordered `arguments`, and `SqlNamedParameter` children; when to use it: see [Custom SQL](../../../docu/manmap.md#custom-sql-mit-sql).

`QueryFromSql` and `UpdateFormSql` are marked deprecated in the live descriptor. Do not use them for new models.

## Concept Families

The remaining abstract/interface concepts mainly constrain placement: `IAtomMapping`, `IKeyMapping`, `IReferenceMapping`, `IQueryOperation`, `IQueryOption`, `IJoinOption`, `ITableOption`, `IRepositoryContent`, `IMappingInstance`, `IDataBaseOperation`, `INeedsClassMapper`, `IMapsClassConcept`, and `IIncludeAbleMapsClassConcept`. Never instantiate abstract/interface concepts in blueprints; choose a concrete implementation accepted by the role.

For the complete concept list with projections and FQ names, use the Kapitellandkarten in the package documentation, starting with [Repository](../../../docu/manmap.md#kapitellandkarte-repository) and [Persistenz-Mappings](../../../docu/manmap.md#kapitellandkarte-persistenz-mappings).
