# Blueprint index

All blueprints use fully qualified concept names and contain no persistent application reference. Replace every sample name and `TARGET_*` placeholder before insertion.

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
- [status-subtree.json](blueprints/status-subtree.json): add with role `status` to Entity, Value Object, or DTO.

Root skeletons intentionally omit constructors, methods, Pages, config elements, and other large/semantic content. Insert them first, validate, then add those parts surgically. For Pages and Config elements, inspect a packaged reference from [sandbox.md](sandbox.md) because required references and task-specific child concepts cannot be made universally portable.

The test-suite skeleton contains `TARGET_OFX_CONFIG`; resolve it in the destination model before a production write. [Test configuration semantics](../../../docu/objectflow.md#ofx-test-suit)

