# Compose an entity mapping

Start with an `EntityMapping` for each ObjectFlow `Entity` stored through ManMap. It references the entity class, names its SQL table, and contains atomic mappings in the role spelled `atomMpig`. The [entity blueprint](blueprints/entity-mapping-subtree.json) shows the minimum with one `FieldMapping`. Resolve the target class and property node references in the consumer model.

| Shape | When to use it | Permanent example / blueprint |
|---|---|---|
| `EmbeddedMapping` | An ObjectFlow `ValueObject` is held in an entity and its properties need column mappings. | `Domain.PersDesc` embeds `MoneyAmount`; [blueprint](blueprints/embedded-mapping-subtree.json). |
| `IncludeMapping` | Reuse an existing suitable mapping instead of repeating its field definitions. It is also useful inside a C2 `NoKeyMapperField`. | `Domain.PersDesc` and `Domain.C2SqlRepo.noKeyAuditEntityMapper`; [C2 reuse blueprint](blueprints/c2-entity-readonly-mapper-subtree.json). |
| `ReferenceMapping` | Describe a possible object reference and map its key column(s). It does not load the target unless the query requests it. | `Domain.PersDesc` maps `InvoicePosition.invoice`; [blueprint](blueprints/reference-mapping-subtree.json). |
| `ListMapping` with `MappedFieldRef` | Refer to a list element's existing `ReferenceMapping` back to the parent, together with the element's `EntityMapping`. | `Domain.PersDesc` maps `Invoice.positions`; [blueprint](blueprints/list-mapping-backref-subtree.json). |
| `ListMapping` with `KeyOnlyReferenceMapping` | Use this when the child table carries the parent key but the child object has no `ReferenceMapping` back to the parent. | A transient production model supplied the [anonymized blueprint](blueprints/list-mapping-key-only-subtree.json). |

`ListMapping` declares a relation, while [query loading](loading.md) decides whether a list is populated. Use MPS MCP to inspect the focused permanent example before choosing target refs. `IncludeMapping` is a reuse tool, not a substitute for defining the correct entity or value-object mapping.

The choice between the two `ListMapping.mappedfieldRef` forms depends on the child object model: use `MappedFieldRef` when the child has a real `ReferenceMapping` back to its parent; use `KeyOnlyReferenceMapping` when only the parent key exists in the child table. This distinction comes from the language author.

Neither list mapping form causes `SaveWithMap` on the parent to save its list elements. The child table needs the parent key, and each child must be saved explicitly with its own entity mapping; see [mapped operations](mapped-operations.md).
