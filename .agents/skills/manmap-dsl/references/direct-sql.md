# Direct SQL with C2

Use `C2SqlBlock` for direct SQL. Its `statements` child is a BaseLanguage `StatementList` containing `C2SqlText` (text lines and words) and, where needed, C2 integration nodes for dynamic values. The optional `mapping` child determines how rows become values. Start with a focused, live example such as the permanent `org.modellwerkstatt.objectflow.tests.manmap.Domain.C2SqlRepo`.
For named values in SQL text, choose `C2SqlWordVarReference`, `C2Dot`, or `C2SqlStatusReference` according to [C2 parameters](c2-parameters.md).

| Result | C2 `mapping` expression | Repository member |
|---|---|---|
| Small/simple scalar, e.g. one integer | inline row-mapping closure or `RowMapperFieldRef` | A reusable `RowMapperField` is needed only for the reference form |
| No usable key, e.g. a `GROUP BY` aggregate | `NoKeyMapperFieldRef` | `NoKeyMapperField` with its own field mappings, commonly targeting an ObjectFlow `DTO` |
| Entity-shaped read-only result when a suitable map already exists | `NoKeyMapperFieldRef` | `NoKeyMapperField` with `IncludeMapping` referencing the existing `EntityMapping` |

A `NoKeyMapperField` references the result `classConcept` and contains `atomMpig` field mappings. It can map every result column itself. `IncludeMapping` is optional reuse of a suitable existing map, often for an entity-shaped result. `MappingReference` has a `fieldMapping` reference to `FieldMapping`; it cannot name an `EntityMapping` as the C2 row mapper. For the reuse case, the path is `C2SqlBlock.mapping` → `NoKeyMapperFieldRef` → `NoKeyMapperField.atomMpig` → `IncludeMapping.mapping` → `EntityMapping`.

**Language-author rule:** Every object produced by a `NoKeyMapperField` is read-only, including one mapped through `IncludeMapping` to an existing `EntityMapping`. The permanent `NoKey Tests` suite checks this behavior. These results are not integrated into the ObjectFlow session; see [session behavior](session-behavior.md).

Aggregates typically lack a domain or surrogate key. Since their result object is transient, an ObjectFlow `DTO` (`org.modellwerkstatt.objectflow.structure.DTO`) is often the appropriate target instead of an `Entity`. This is a preference from the language author, not a structural requirement.

The permanent `Domain.C2SqlRepo.getCountOfAuditEntities` method (`/798898777369868665`) uses an inline closure to map `count(*)` to an integer. Print that method through MPS MCP and use `mps-baselanguage` for the closure AST. Use `RowMapperFieldRef` when the row conversion is defined as a reusable repository member.

Use these compact shapes as starting points, then resolve every placeholder to a node in the target model:

- [Scalar C2 block](blueprints/c2-row-mapper-subtree.json)
- [Aggregate C2 block](blueprints/c2-no-key-aggregate-subtree.json)
- [No-key DTO field mapper](blueprints/c2-no-key-dto-mapper-subtree.json)
- [Entity-shaped mapper using an existing map](blueprints/c2-entity-readonly-mapper-subtree.json)

The permanent `Domain.C2SqlRepo.noKeyAuditEntityMapper` (`/8232801790818224466`) demonstrates a `NoKeyMapperField` with its own field mappings and an `IncludeMapping`; the compact blueprints also preserve patterns observed in the transient production project without business names or IDs. For diagnostics, compare SQL aliases and result columns with mapper field names and class properties, then check that the C2 block points to the intended mapper member.
