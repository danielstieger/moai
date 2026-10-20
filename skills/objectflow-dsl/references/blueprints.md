# Blueprint index

All blueprints use fully qualified concept names and contain no persistent application reference. Replace every sample name and `TARGET_*` placeholder before insertion, then search the text for `TARGET_`: the dry-run does not report a forgotten placeholder. Send the JSON inline or as a copy under `${TMPDIR:-/tmp}`; every blueprint is below 4 KB minified.

## Root skeletons

- [entity-skeleton.json](blueprints/entity-skeleton.json)
- [value-object-skeleton.json](blueprints/value-object-skeleton.json)
- [dto-skeleton.json](blueprints/dto-skeleton.json)
- [service-skeleton.json](blueprints/service-skeleton.json)
- [command-skeleton.json](blueprints/command-skeleton.json)
- [test-suite-skeleton.json](blueprints/test-suite-skeleton.json)
- [ofx-config-skeleton.json](blueprints/ofx-config-skeleton.json)
- [roles-and-permissions-skeleton.json](blueprints/roles-and-permissions-skeleton.json)

## Incremental subtrees

- [business-property-int-subtree.json](blueprints/business-property-int-subtree.json): add with role `businessProperties` to Entity, Value Object, or DTO.
- [value-object-equal-property-subtree.json](blueprints/value-object-equal-property-subtree.json): add with role `equalProperties` to a Value Object; `TARGET_BUSINESS_PROPERTY` is the node reference of one of its Business Properties.
- [value-object-with-method-subtree.json](blueprints/value-object-with-method-subtree.json): add with role `member` to a Value Object; `TARGET_VALUE_OBJECT` is the Value Object, `TARGET_VALUE_OBJECT_CONSTRUCTOR` its constructor taking the properties. Adapt name and parameter type; with several properties add one `actualArgument` per constructor parameter (`LocalPropertyReference` for the unchanged ones), as in the packaged `SimpleValue`.
- [status-subtree.json](blueprints/status-subtree.json): add with role `status` to Entity, Value Object, or DTO.

The Entity, Value Object, and DTO skeletons contain an empty public default constructor, as the packaged examples do; the Entity factory would add it anyway (it is not doubled). The Service skeleton and the other root skeletons contain no constructor. The factories add an `id` key (Entity), `myVal` (Value Object), or `name` (DTO); a Value Object skeleton is not checker-clean until `equalProperties` and the `with` methods exist. Details and follow-up edits: [Node factories](gotchas.md#node-factories). All root skeletons intentionally omit further constructors, methods, Pages, config elements, and other large/semantic content. Insert them first, validate, then add those parts surgically. For Pages and Config elements, inspect a packaged reference from [sandbox.md](sandbox.md) because required references and task-specific child concepts cannot be made universally portable.

The test-suite skeleton contains `TARGET_OFX_CONFIG`; replace it with the test `OFXConfig` root (location: conventions `anwendungsaufbau`; imported by the `tests` model) before a production write. [Test configuration semantics](../../../docu/objectflow.md#ofxtestsuit)

