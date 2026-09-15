# Explicit loading of references and lists

ManMap means *manual map*: an `EntityMapping` describes how an ObjectFlow entity is stored, including possible references through `ReferenceMapping`. That declaration does not by itself load the referenced object. The query chooses its loading strategy explicitly.

For a mapped query, `QueryFromMap` references the source `EntityMapping`. A `RefJoinOption` under `QueryFromMap.joinOption` identifies the `ReferenceMapping` to traverse and the target `EntityMapping` to load. These are two separate persistent node references: `refMapping` and `entityMapping`. See [the compact JSON shape](blueprints/query-from-map-ref-join-subtree.json).

**Language-author rule:** If a reference was not loaded by the query, accessing that reference property on the returned ObjectFlow entity throws `org.modellwerkstatt.objectflow.runtime.OFXNotInitializedException`. Do not assume that a declared reference is initialized. Check the query's join options before diagnosing the entity property or the mapping itself.

Lists behave differently. A `ListMapping` alone does not populate the list. Without an explicit load, the list is empty (`size == 0`); accessing it does not raise `OFXNotInitializedException`. A `ListJoinOption` can load it as part of the mapped query; see the [list-join blueprint](blueprints/query-from-map-list-join-subtree.json). A repository can also assign the result of a separate `EntityMapping` query to the entity's list property: `where` returns a list, whereas `get` returns one instance. Check which route the repository uses before interpreting an empty list as proof that no database rows exist. See the [mapped back-reference](blueprints/list-mapping-backref-subtree.json) and [key-only](blueprints/list-mapping-key-only-subtree.json) shapes for two structural forms of `ListMapping`.

The permanent `org.modellwerkstatt.objectflow.tests.manmap.Domain.RepoInvoice` example contains reference joins and explicit loading. A transient production example had a `QueryFromMap` with two `RefJoinOption` children; the blueprint above preserves the reusable structure without its business names or node IDs.
