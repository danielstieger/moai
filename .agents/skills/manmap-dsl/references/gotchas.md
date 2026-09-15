# ManMap Gotchas

ManMap supports Oracle and MySQL. It does not actively manage schema changes. ObjectFlow sessions manage transactions; consult the ObjectFlow skill for session lifecycle instead of treating a repository method as the transaction boundary.

- A declared `ReferenceMapping` does not initialize the referenced object. Without an explicit query join, accessing that reference property raises `OFXNotInitializedException`; follow [the diagnosis path](troubleshooting.md).
- A `ListMapping` without an explicit load yields an empty list (`size == 0`), not `OFXNotInitializedException`. The list can be loaded with a join or populated from a separate mapped `where` query.
- `SaveWithMap` writes a mapped reference's foreign-key value, but does not save the referenced entity or list elements. Assign the parent key to each child and save children separately; see [mapped operations](mapped-operations.md).
- `NoKeyMapperField` results are always read-only, including when `IncludeMapping` reuses an `EntityMapping`; see [direct SQL](direct-sql.md).
- `QueryFromMap.readOnly` and no-key read-only differ in session identity. A repeated checkout in one session can throw `IllegalStateException`; see [session behavior](session-behavior.md).
- In C2, `MappingReference` references a `FieldMapping`; it cannot target an `EntityMapping`. Use `NoKeyMapperField` with its own field mappings, or an `IncludeMapping` when reusing an existing entity map is appropriate; see [direct SQL](direct-sql.md).
- `PersistenceDescription` and `Repository` are the only rootable ManMap concepts.
- Global-library examples can be resolved by explicit model name/reference even if root-name search in the current project returns nothing. Use `includeStubModules=true` for `mps_mcp_get_project_structure`.
- MPS write tools can refuse cross-project changes to these global examples even with `dryRun=true`. Inspect their JSON as read-only reference, then dry-run a blueprint in the actual target project.
- JSON blueprints must use qualified concepts such as `org.modellwerkstatt.manmap.structure.EntityMapping`; shallow prints often show only `EntityMapping`.
- Concept APIs require `l:5aaa957f-3447-4783-b1f7-b301fa3e0394:org.modellwerkstatt.manmap`. The module reference has a different syntax and purpose.
- `EntityMapping.classConcept`, `FieldMapping.property`, and most query/save mapping links are persistent node references. Never substitute concept refs (`c:`) for node refs (`r:`).
- Table names, field names, and sequence names are required `StringLiteral` child nodes. They are not string-valued ManMap properties.
- The structure role is spelled `atomMpig` in the live descriptor. Keep this exact spelling in JSON.
- `Repository` inherits many BaseLanguage roles. Use the modern `member` role seen in dataux examples; deprecated `field`, `method`, and similar inherited roles remain visible in descriptors but should not guide new nodes.
- Repository method bodies contain local-variable and parameter references. Copying a method subtree without rebinding those references produces broken refs even if mapping refs are correct.
- Query predicates are BaseLanguage expressions. Respect BaseLanguage containment and precedence; use `ParenthesizedExpression` where the intended query condition would otherwise be ambiguous.
- `QueryFromMap.debugMe` prints generated SQL and parameter values to the console via `System.out.println` for diagnosis; it is a debugging hack, not a normal query option. See [SQL troubleshooting](sql-troubleshooting.md).
- `OptionalOperator` omits filters for `int` value `0` or `null` in BigDecimal, date/time, string, reference, and ObjectFlow status values. It does not support `boolean` and does not share the `isNullKeyStaticHelper()` key rules; see [query operators](query-operators.md).
- `RefJoinOption` and `ListJoinOption` point to existing relationship mappings. `AdditionalTableReference` is a separate `QueryFromMap.joinOption` and needs a valid `AdditionalTableName` target plus condition.
- `RepoInvoice` is intentionally huge. Use focused method/subtree prints to avoid oversized JSON and accidental root-wide rewrites.
- After inserting or changing nodes, run `mps_mcp_check_root_node_problems`. A successful JSON insertion only proves the AST was accepted, not that references, types, scopes, or generation are valid.
