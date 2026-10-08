# Gotchas and diagnostics

## Modeling traps

- Business Properties require both `type` and `propertyImplementation`; an inserted node can be structurally accepted yet incomplete. Start from the verified subtree blueprint. [Business Properties](../../../docu/objectflow.md#business-properties)
- `StatusDeclaration` is nested under Entity/Value Object/DTO and is not rootable. Every element requires the `shortDescNew` and `longDescNew` children in the AST. [Status](../../../docu/objectflow.md#status)
- Checker: comparing a Value-Object key with `null` (`rechnung.kunde#Key == null`) is an error; use `isNullKey`. `#Key` versus the loaded object: see [Beziehungen und Objektgraphen](../../../docu/objectflow.md#beziehungen-und-objektgraphen).

## Runtime semantics (documentation pointers)

- Initial values and `null`: see [Null-Werte in Datenstrukturen](../../../docu/objectflow.md#null-werte-in-datenstrukturen).
- Read-only versus Checkout, dirty tracking: see [Dirty-Tracking, Read-only und unveränderliche Werte](../../../docu/objectflow.md#dirty-tracking-read-only-und-unveränderliche-werte).
- `StringFormatString` placeholders (`%bd`, `%st`, `%ld`, …) and `null` rendering: see [Formatieren von Zeichenketten](../../../docu/objectflow.md#formatieren-von-zeichenketten).
- Preconditions in Page Init (only `WARNING_HINT`): see [Page Init und Datenbereitstellung](../../../docu/objectflow.md#page-init-und-datenbereitstellung).
- `session.setReadOnly()` and `session.isDirty()`: see [Session-weites Read-only und Dirty](../../../docu/objectflow.md#session-weites-read-only-und-dirty).
- Double checkout and `session entities` (`CheckedOutEntities`): see [Entities in der Session prüfen](../../../docu/objectflow.md#entities-in-der-session-prüfen).

## MPS diagnostics

- Always use FQ concept names in blueprints. Never use a `c:` concept reference as a node-reference target.
- A dry-run warning about an unresolved `TARGET_*` means the production write would create a dynamic reference. Resolve the placeholder first unless a temporary dynamic reference is deliberate.
- Inspect roots shallowly first; deep-print only the needed subtree.
- Use `mps_mcp_check_root_node_problems` on each changed root after every complex edit. Run `FIX_REFERENCES` before declaring an existing target unresolvable.
- A `descriptorStatus: "hollow"` entry is untrustworthy; what to do: `moai:mps-language-analysis` (`references/concept-details.md`).
- Never copy persistent node references from an application project into this skill or into portable blueprints.

