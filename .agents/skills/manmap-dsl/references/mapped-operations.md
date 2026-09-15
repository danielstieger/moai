# Mapped queries, saves, and deletes

## Query results

`QueryFromMap` names an `EntityMapping`. Its `queryOperation` contains `GetQuery` to retrieve one instance by the supplied key argument or `WhereQuery` to retrieve a list selected by its filter expression. The latter can be assigned to an entity's list property when loading that list through a separate query. See [explicit loading](loading.md) for how this differs from a query join.

Use the [compact `get` blueprint](blueprints/query-from-map-get-subtree.json) for the outer ManMap shape. The key argument is a BaseLanguage expression; the example uses a `VariableReference` that must point to a declaration in the repository method's scope. For `where`, inspect a focused method in the permanent `Domain.RepoInvoice` example and build its BaseLanguage predicate with the `mps-baselanguage` skill.

For repeated `get` or `where` queries in one ObjectFlow session, follow [session identity rules](session-behavior.md).

## Save

`SaveWithMap` references the `EntityMapping` and holds the entity expression being saved. Start with the [minimal save blueprint](blueprints/save-with-map-subtree.json); replace both placeholders with references valid in the target model and method.

**Language-author rule:** The entity key marks the property used as the key. By default, ManMap calls `org.modellwerkstatt.manmap.runtime.MMStaticAccessHelper.isNullKeyStaticHelper()` for that key field: when this helper returns `true`, ManMap inserts; otherwise it updates. `InsertSaveOption` forces Insert and `UpdateSaveOption` forces Update without this check. `AutoidOption` obtains an ID from the database before Insert. For compound ValueObject keys, explicitly select Insert or Update instead of relying on the default check; see [key rules](keys.md).

**Language-author rule:** `SaveWithMap` persists the mapped columns of the entity being saved, including the foreign-key value represented by its `ReferenceMapping`. It does not save the referenced entity itself, and a `ListMapping` does not cause list elements to be saved. Give each child its parent key (for example through its back-reference) and save the children explicitly with their own `EntityMapping`; there is no automatic graph-save option.

The options are children of `SaveWithMap.options`. A transient production repository showed each of `InsertSaveOption`, `UpdateSaveOption`, `BatchSaveOption`, `ForceAuditSaveOption`, and `SkipAuditSaveOption` in this role. Their presence is evidence of supported shapes, not guidance to add them by default. Choose options from the required behavior and validate the resulting method.

## Graph examples

The permanent `Domain.RepoInvoice.saveInvoicePosListBatch` method saves `MapInvoice`, assigns each position's `invoice` back-reference, then saves the positions with `MapInvoicePosition` and `BatchSaveOption`. `Domain.RepoInvoice.deleteInovice` explicitly deletes each position before deleting the invoice. Inspect these focused methods when building a graph save/delete workflow; do not infer cascade behavior from a declared `ListMapping` alone.

## Delete

`DeleteWithMap` references the `EntityMapping` and holds the entity expression being deleted. Start with the [minimal delete blueprint](blueprints/delete-with-map-subtree.json). Resolve its `VariableReference` to the actual entity variable or use another well-typed BaseLanguage expression. The entity must already be loaded, and its key must be present. `DeleteWithMap` deletes that entity using the selected mapping.
