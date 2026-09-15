# Diagnose SQL and mapping failures

First locate the operation that failed: `QueryFromMap` (generated SQL from an `EntityMapping`), `SaveWithMap`/`DeleteWithMap`, or direct `C2SqlBlock`. Record the SQL/database error and the repository method, then follow the corresponding path below. ManMap supports Oracle and MySQL; check which dialect the application's connection uses before adjusting SQL syntax.

`QueryFromMap.debugMe` is a quick diagnostic hack that writes the generated SQL and its parameters to the console with `System.out.println`. Use it when you need to inspect one failing mapped query; treat it as a temporary debugging aid, not a query-design option.

For `QueryFromMap`, verify the `EntityMapping.tableName`, `FieldMapping.fieldName`, key mapping, and any `AdditionalTableReference` or join option used by that query. Follow persistent references from query to mapping; same-looking names are not proof that the query targets the intended mapping. A reference join uses both the source `ReferenceMapping` and the target `EntityMapping`. A list join uses the list mapping and its child mapping. Compare the resulting SQL table and column names with the live schema; ManMap does not actively manage schema changes.

For `C2SqlBlock`, inspect the SQL text and [C2 parameter nodes](c2-parameters.md) in the same block. Named values must point to in-scope declarations. For a mapped result, compare selected column order/aliases and SQL types with the `RowMapperField` or `NoKeyMapperField` conversion and ObjectFlow target properties. For an aggregate, check whether a no-key DTO mapper is appropriate; a `MappingReference` cannot directly point at an `EntityMapping`.

For `SaveWithMap`, inspect the key value and [insert/update decision](keys.md), especially a compound key without an explicit save option. Verify `AutoidOption.sequenceName` and any audit or archive option used by that operation. For `DeleteWithMap`, verify that the entity was loaded and has a key.

Use the focused permanent example or test listed in the [test index](test-index.md) to compare node shape, and inspect generated output only as read-only evidence when a generator produced unexpected SQL. Change the MPS mapping/repository source through MCP, validate the changed root, regenerate, and rerun the failing scenario. For `OFXNotInitializedException`, use the separate [reference-loading diagnosis](troubleshooting.md); an unloaded reference is a query loading issue, not evidence of a missing SQL row.
