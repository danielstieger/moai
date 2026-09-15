# Query results and session identity

`QueryFromMap` always integrates its result into an ObjectFlow session, which extends `org.modellwerkstatt.manmap.runtime.IM3Session`. This is about object identity and mutability; transaction lifecycle belongs to the ObjectFlow/session setup.

| Result path | Mutability | Behavior within one session |
|---|---|---|
| `QueryFromMap` with `readOnly=true` | Changing an entity in application code raises an exception. | An entity already loaded by a query in that session is not materialized again by a later query. |
| `QueryFromMap` without `readOnly` (*checked out*) | The entity is available for changes. | Attempting to check out an entity already present in the session (r/w or r/o) through `get` or `where` raises `IllegalStateException`. |
| `NoKeyMapperField` result | Always read-only, including when `IncludeMapping` reuses an entity map. | It is not integrated into the session; the no-key result object itself is outside the session identity map, while entities loaded through its joins are integrated into the session. |

The checked-out exception includes: `Entity <class> with key <key> was already checked out r/w or r/o!`. When diagnosing it, find both queries in the same session and determine whether the repeated `get` or `where` is intentional; prefer using the already loaded instance or one consistent loading strategy. For read-only object changes, inspect the originating `QueryFromMap.readOnly` flag or whether the result came from a `NoKeyMapperField`.

The permanent `Domain.RepoInvoice` model contains `QueryFromMap` instances with `readOnly=true`. The permanent `Tests` model covers changing/deleting read-only objects and compares no-key results with and without a ManMap session. Consult the [test index](test-index.md) and print the focused case before changing session-sensitive behavior.
