# Keys and the Save decision

An ObjectFlow entity's key identifies the property ManMap uses for persistence. Without a forcing save option, `SaveWithMap` calls `org.modellwerkstatt.manmap.runtime.MMStaticAccessHelper.isNullKeyStaticHelper()` for the key: `true` selects Insert, `false` selects Update. The runtime method dispatches an `Integer` to the integer type handler, a `String` to the string type handler, and an `IM3CompoundKey` to its `isNullKey()` method; a `null` argument is treated as no key. This dispatch was checked in the MPS runtime model at `r:22abd22f-3c78-4514-b7c6-da1d82c38fe2(org.modellwerkstatt.manmap.runtime)/8367961125968005027`.

The key can be marked on an ObjectFlow `Entity` business property with `KeyOption` in `propertyOption`. If the entity does not declare it, mark the corresponding ManMap `FieldMapping` with `KeyOption` in `mappingOption`; see the [key field blueprint](blueprints/key-field-mapping-subtree.json). `AutoidOption` is another field `mappingOption` and requires a `sequenceName` `StringLiteral`; see the [auto-ID blueprint](blueprints/autoid-option-subtree.json).

| Key form | Values treated as “not yet keyed” |
|---|---|
| Single integer key | `null`, `0`, or `-1` |
| Single string key | `null` or `""` |
| Compound key represented by a ValueObject | Every integer component is checked against `< 0`; every string component against `null` or `""`. |

The values above apply to `SaveWithMap` key detection. `OptionalOperator` uses [different no-value rules](query-operators.md); do not reuse these key sentinels for optional query filters.

**Language-author rule:** For a compound key, choose `InsertSaveOption` or `UpdateSaveOption` explicitly when saving; do not rely on the automatic decision. These options force their respective operation without asking `isNullKeyStaticHelper()`. `AutoidOption` obtains an ID from the database before Insert.

`DeleteWithMap` removes a loaded entity and requires its key to be present. See [mapped operations](mapped-operations.md) for the node shapes. The permanent `Tests` model covers integer, string, ValueObject, and compound-key cases in `References, initialization(no session)` and `Graph load/save (no session)`.
