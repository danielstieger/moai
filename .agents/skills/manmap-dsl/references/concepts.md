# ManMap Concepts

The live MPS descriptor exposes 94 concepts. The two rootable concepts are `PersistenceDescription` and `Repository`; everything else is embedded below mappings, BaseLanguage methods, expressions, or statements.

## Root Concepts

| Concept | Shape | Purpose |
|---|---|---|
| `org.modellwerkstatt.manmap.structure.PersistenceDescription` | property `name`; children `persistenceMapping: EntityMapping[0..n]` | Groups class-to-table mappings. |
| `org.modellwerkstatt.manmap.structure.Repository` | extends BaseLanguage `ClassConcept`; normal class properties/children plus optional `documentation2` | Hosts repository methods and mapper fields. |

## Mapping Core

| Concept | References | Children |
|---|---|---|
| `EntityMapping` | `classConcept -> ClassConcept` (required) | `tableName: StringLiteral` (required), `tableOption: ITableOption*`, `atomMpig: IAtomMapping*` |
| `FieldMapping` | `property -> Property` (required) | `fieldName: StringLiteral` (required), `mappingOption: FieldOption*` |
| `ReferenceMapping` | `property -> Property` (required) | `keyMapping: IKeyMapping` (required), `atomMpig: IAtomMapping*` |
| `EmbeddedMapping` | optional `property -> Property` | `atomMpig: IAtomMapping*` |
| `ListMapping` | `property -> Property` (required) | `mappedfieldRef: IReferenceMapping` (required) |
| `IncludeMapping` | optional `mapping -> IIncludeAbleMapsClassConcept` | none |

`IAtomMapping` accepts field, reference, embedded, list, and include mapping shapes. `IKeyMapping` is implemented by key-capable field/embedded/reference forms. Required references point to declarations in the consumer model and must be resolved for that model.
The key is declared either on the ObjectFlow entity property or by a ManMap `FieldMapping.mappingOption` `KeyOption`; see [keys](keys.md).

## Mapping Options

- Field options: `KeyOption`, `AutoidOption`, `CreatedAtFieldOption`, `CreatedByFieldOption`, `ModifiedAtFieldOption`, `ModifiedByFieldOption`, plus schema options `IndexOption`, `NotnullOption`, `SizeOption`, and `UniqueOption`.
- Table options: `AdditionalTableName`, `OptimisticOption`, and `OverWriteAutoIdOption`.
- `AdditionalTableName` requires `tablename: StringLiteral` and supplies a named secondary table target.
- `AutoidOption` requires `sequenceName: StringLiteral`.

## Repository Content

`RepositoryInstanceMethodDeclaration` extends BaseLanguage `InstanceMethodDeclaration`. Its ManMap-specific `repoMethodType` property is combined with the usual required `returnType` and `body`, optional parameters, visibility, annotations, and modifiers. Repositories can also contain `RowMapperField`, `NoKeyMapperField`, and other `IRepositoryContent` concepts.

Important database operations:

| Concept | Kind | Required structure |
|---|---|---|
| `QueryFromMap` | expression | reference `entityMapping`; children `joinOption*`, `queryOperation*`; properties `debugMe`, `readOnly` |
| `SaveWithMap` | statement | reference `entityMapping`; required `expression`; `options*` |
| `DeleteWithMap` | statement | reference `entityMapping`; required `expression`; `options*` |
| `ReloadQuery` | query operation | reloads mapped data |

Query operations include `GetQuery` (`argument` required), `WhereQuery` (`filter` required), `SortByQuery` (`toComparable` required plus `sortDirection`), `LimitQuery` (`count` required), and `SizeQuery`. `InOperation`, `LikeOperator`, and `OptionalOperator` participate in query predicates.

`QueryFromMap.joinOption` accepts `RefJoinOption`, `ListJoinOption`, and `AdditionalTableReference` as peers. The first two reference relationship mappings. `AdditionalTableReference` references an `AdditionalTableName` and requires a BaseLanguage condition expression.

## Direct SQL and result mapping

`C2SqlBlock` supports direct SQL. Use an inline row-mapping closure or `RowMapperFieldRef` for small/simple results such as one integer, and `NoKeyMapperField` for results without usable keys, often aggregates mapped to ObjectFlow DTOs. `NoKeyMapperField` can map all fields itself or reuse an existing `EntityMapping` through `IncludeMapping`. See [direct SQL](direct-sql.md).

The `C2*` concepts (`C2SqlBlock`, `C2SqlText`, path/reference concepts, and `C2SqlIntegration`) provide direct SQL integration. Prefer copying a focused, live `C2SqlRepo` subtree over assembling C2 nodes from concept names alone.

## Full Concept Families

- Mapping: `EntityMapping`, `FieldMapping`, `ReferenceMapping`, `KeyOnlyReferenceMapping`, `MappedFieldRef`, `EmbeddedMapping`, `ListMapping`, `IncludeMapping`.
- Query: `QueryFromMap`, `GetQuery`, `WhereQuery`, `SortByQuery`, `LimitQuery`, `SizeQuery`, `ReloadQuery`, `MappingReference`, `RefJoinOption`, `ListJoinOption`, `AdditionalTableReference`, `InOperation`, `LikeOperator`, `OptionalOperator`, `QuerySmartClosureParamDeclaration`.
- Save: `SaveWithMap`, `DeleteWithMap`, `InsertSaveOption`, `UpdateSaveOption`, `BatchSaveOption`, `ForceAuditSaveOption`, `SkipAuditSaveOption`.
- C2 result mapping: inline row-mapping closure or `RowMapperField`/`RowMapperFieldRef` for small/simple results, `NoKeyMapperField`/`NoKeyMapperFieldRef` for results without a usable key, with own field mappings or optional `IncludeMapping` to reuse an `EntityMapping`.
- C2 SQL: `C2SqlBlock`, `C2SqlText`, `C2SqlIntegration`, `C2Dot`, `C2EntityKeyPropReference`, `C2MethodReference`, `C2PropertyReference`, `C2SqlStatusReference`, `C2SqlWordVarReference`.
- Interfaces define valid placement: `IAtomMapping`, `IKeyMapping`, `IReferenceMapping`, `IQueryOperation`, `IQueryOption`, `IJoinOption`, `ITableOption`, `IRepositoryContent`, `IMappingInstance`, `IDataBaseOperation`, and related marker/provider interfaces.
