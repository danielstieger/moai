# Gotchas and diagnostics

## Domain structures

- Business Properties require both `type` and `propertyImplementation`; an inserted node can be structurally accepted yet incomplete. Start from the verified subtree blueprint. [Business Properties](../../../../docu/objectflow.md#business-properties)
- `StatusDeclaration` is nested under Entity/Value Object/DTO and is not rootable. Every element requires short and long description children in the AST. [Status](../../../../docu/objectflow.md#status)
- Do not mutate Value Objects in place; create a replacement value. [Entity, Value Object, DTO](../../../../docu/objectflow.md#entity-value-object-und-dto)
- Initialized string/int/decimal/list values are not an invitation to overwrite regular state with `null`; use `null` only for genuinely absent optional references/date-time values. [Null values](../../../../docu/objectflow.md#null-werte-in-datenstrukturen)
- A virtual property owns no persisted value and cannot use infrastructure from its getter. [Virtual properties](../../../../docu/objectflow.md#virtuelle-business-properties)
- `#Key` reads identity but does not load the object. Direct access to an unloaded Entity reference throws `OFXNotInitializedException`. [Relationships](../../../../docu/objectflow.md#beziehungen-und-objektgraphen)
- `isNullKey` tests key emptiness, not whether the object is loaded. [Relationships](../../../../docu/objectflow.md#beziehungen-und-objektgraphen)
- Read-only Entity setters throw `OFXIllegalAccessException`; use Checkout for mutation. [Dirty tracking and read-only](../../../../docu/objectflow.md#dirty-tracking-read-only-und-unveränderliche-werte)

## Services, validation, and expressions

- Direct Java calls to Service/Repository instances bypass component/session/transaction semantics; use `#`. [Component calls](../../../../docu/objectflow.md#komponenten-mit--aufrufen)
- Services are stateless application components, not per-user state holders. [Service components](../../../../docu/objectflow.md#service-komponenten)
- A Precondition is a correctable business problem; Guard/Exception terminate technically. A Guard in Graph Edit escalates to the owner. [Preconditions and guards](../../../../docu/objectflow.md#preconditions-validation-guards-und-exceptions)
- Without a `validation` block, the first failing Precondition stops evaluation. Validate completely before mutation. [Validation pattern](../../../../docu/objectflow.md#preconditions-validation-guards-und-exceptions)
- Wrong formatted-string placeholders fail at runtime; unexpected `null` is rendered visibly. [String formatting](../../../../docu/objectflow.md#formatieren-von-zeichenketten)
- Use server time and `BigDecimal` literals; avoid `double` and `float` for exact business values. [Literals](../../../../docu/objectflow.md#literale-für-datum-zeitpunkt-und-dezimalzahl)

## Commands and sessions

- `SEARCH_CMD` never commits, even after `FINAL_OK`. [Command types](../../../../docu/objectflow.md#die-vier-command-typen)
- `GRAPH_OWNER_CMD_MODAL` owns its own session/commit; it is not a Graph Edit. [Command types](../../../../docu/objectflow.md#die-vier-command-typen)
- `IN_BACKGROUND` applies only to `command init`. [Command init](../../../../docu/objectflow.md#command-init-und-hintergrundinitialisierung)
- Do not throw an aborting Precondition from Page Init; use a warning there or move the check to Command Init/Conclusion. [Page Init](../../../../docu/objectflow.md#page-init-und-datenbereitstellung)
- Multiple Page Pane links are ordered; keep the unconditional default last. [Multiple Page Panes](../../../../docu/objectflow.md#mehrere-page-panes)
- `no_save` discards editor values and is exceptional; disabled UI does not justify it. [Page Conclusions](../../../../docu/objectflow.md#page-conclusions)
- Session operations registered by a Graph Edit survive child cancellation; register them in the session owner. [Command types](../../../../docu/objectflow.md#die-vier-command-typen)
- Revert restores copied in-memory graph state, not a database transaction. Include the graph root when the whole aggregate must be restored. [Revert](../../../../docu/objectflow.md#revert-beim-abbruch)
- `session.setReadOnly()` disables saving conclusions but does not retroactively mark integrated Entities read-only. [Session read-only](../../../../docu/objectflow.md#session-weites-read-only-und-dirty)
- Avoid a second Checkout for an identity already in the session; inspect `session entities` first. [Session entities](../../../../docu/objectflow.md#entities-in-der-session-prüfen)
- With new-style termination handling, do not keep using the pushed source; continue with the object returned by `session merge`. [Session merge](../../../../docu/objectflow.md#explizites-command-termination-handling-und-session-merge)
- `session queue next command` is ignored without UI. [Post-commit command queue](../../../../docu/objectflow.md#command-nach-dem-commit-einplanen)
- Successors share one Unit of Work; queued next Commands cross a commit boundary. [Successors](../../../../docu/objectflow.md#successor-commands)

## Persistence and UI boundaries

- Relationships and list mappings neither load nor cascade-save automatically. [ManMap relationships](../../../../docu/manmap.md#referenzen-eingebettete-werte-und-listen)
- Database-changing custom SQL belongs in the successful session-operation flow when it is part of the use case. [MoWare transaction principle](../../../../docu/moware-werkbank.md#grundprinzipien-für-die-anwendungsentwicklung)
- UI binding does not load a reference/list; DataUX requires prepared data. [DataUX diagnosis](../../../../docu/dataux.md#häufige-fehler-und-diagnose)
- `#Meta` changes UI behavior but never replaces server-side business validation. [Property metadata](../../../../docu/objectflow.md#ui-metadaten-einer-property-mit-meta-steuern)

## MPS diagnostics

- Always use FQ concept names in blueprints. Never use a `c:` concept reference as a node-reference target.
- A dry-run warning about an unresolved `TARGET_*` means the production write would create a dynamic reference. Resolve the placeholder first unless a temporary dynamic reference is deliberate.
- Inspect roots shallowly first; deep-print only the needed subtree.
- Use `mps_mcp_check_root_node_problems` after every complex edit. Run `FIX_REFERENCES` before declaring an existing target unresolvable.
- If a concept descriptor is `hollow`, do not trust empty features; rebuild the language module and query again.
- Never copy persistent node references from an application project into this skill or into portable blueprints.

For domain-specific runtime symptoms, also use the comprehensive [ObjectFlow diagnosis list](../../../../docu/objectflow.md#häufige-fehler-und-diagnose), [ManMap diagnosis list](../../../../docu/manmap.md#häufige-fehler-und-diagnose), and [DataUX diagnosis list](../../../../docu/dataux.md#häufige-fehler-und-diagnose).

