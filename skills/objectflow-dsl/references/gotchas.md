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

- Always use FQ concept names in blueprints. Never use a `c:` concept reference as a node-reference target: the insert accepts it silently and leaves it unresolved; only the checker reports it.
- The dry-run does not look up names: `TARGET_OFX_CONFIG` gets the same "is a name, not looked up" warning as a real name, and an unfilled blueprint writes with `ok:true` and `stillBroken` > 0. Search the blueprint text for `TARGET_` before every write.
- Names inside one blueprint resolve on the real write (e.g. `VariableReference` → `val`); each write reports `fixReferences {fixed, repointed, stillBroken}`. `FIX_REFERENCES` is only the fallback for references still broken after the expected targets exist.
- Look up concepts with one `mps_mcp_get_concept_details` call, `languageRefs` (the `l:` form or the plain language name) plus `detail="shape"`, instead of one call per concept. Enum literals: `mps_mcp_query_structure` `GET_ENUMERATION_LITERALS`; `enumerationRef` takes the qualified name. Never write an empty enum value `""`; omit the property.
- Inspect roots shallowly first; deep-print only the needed subtree.
- Use `mps_mcp_check_root_node_problems` after every complex edit: on the root, or on the model reference with `perRoot=true` after several roots.
- A `descriptorStatus: "hollow"` entry is untrustworthy; what to do: `moai:mps-language-analysis` (`references/concept-details.md`).
- Never copy persistent node references from an application project into this skill or into portable blueprints.

## Node factories

Factories run on every real insert (not in the dry-run) and fill only the roles the blueprint omits. A named role replaces the factory content, even as an empty role `{"role":"…","nodes":[]}`. `mps_mcp_query_structure` `LIST_CONCEPT_ASPECTS` shows whether a concept has a factory (`actions`, `relation: appliesTo`).

- Entity: adds `int id` with `KeyOption` + `AutoidOption("S_")`, `shortDesc`/`longDesc`, and a public default constructor (a constructor in the blueprint is kept, not doubled). A blueprint that brings its own `businessProperties` gets no `id`: "Exactly one key has to be defined for an Entity." Insert the skeleton without properties and add them with `ADD CHILD`, or include a KEY property yourself. Rename `id` and the sequence `S_` as the conventions require.
- Value Object: adds `int myVal`. The skeleton alone leaves checker errors (missing `equalProperties`, missing `withMyVal(..)`); without `myVal` the `equalProperties` error stays. After the insert: replace the property, add `equalProperties`, a constructor taking all properties, and one `with<Prop>(val)` per property that returns `new <ValueObject>(..)` with `val` in its position and the other properties unchanged (packaged `SimpleValue`) ([blueprints](blueprints.md#incremental-subtrees)).
- DTO: adds `string name`; rename or delete it.
- Command: sets `newWindowTitleType=ADDON` and `defaultHotkey="_"`.
- Check factory effects with `print_node` after the insert.
