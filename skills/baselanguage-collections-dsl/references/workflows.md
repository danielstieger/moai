# BaseLanguage Collections workflows

## Define custom containers

1. Use `CustomContainers` only when the language/runtime integration needs a named custom container declaration.
2. Dry-run [custom-containers-root-skeleton.json](blueprints/custom-containers-root-skeleton.json) with `mps_mcp_insert_root_node_from_json` in the destination model.
3. Insert the root, then add each `CustomContainerDeclaration` incrementally.
4. Supply its required abstract `containerType` and concrete runtime `ClassifierType`, and resolve any factory/runtime classifier references in the destination model.
5. Validate the root and build/generate the consuming model.

## Add a collection type

1. Identify the host role that accepts a BaseLanguage `Type`.
2. Choose `SequenceType`, `ListType`, `SetType`, or `MapType` from the intended semantics.
3. Add the required `elementType`, or `keyType` and `valueType`, using concrete BaseLanguage type nodes.
4. Insert or replace only the host's type child.
5. Validate the containing root; type errors often indicate that the host declaration and initializer disagree.

Start with [list-string-type-subtree.json](blueprints/list-string-type-subtree.json) for a reference-free type shape.

## Create a list, set, or map

1. Create a BaseLanguage `GenericNewExpression`.
2. Put the collection creator in role `creator`.
3. Fill the creator's element/key/value type children.
4. Use `initValue` for explicit list/set elements, `copyFrom` for an existing sequence, or `initializer` for map entries as supported by the selected creator.
5. Place the complete `GenericNewExpression` in the destination expression role and validate its containing root.

See [arraylist-string-creator-subtree.json](blueprints/arraylist-string-creator-subtree.json) and [hashmap-string-creator-subtree.json](blueprints/hashmap-string-creator-subtree.json).

## Add a collection operation

1. Keep or construct the collection expression that will be the operand.
2. Wrap it in BaseLanguage `DotExpression`.
3. Put the Collections operation in role `operation`.
4. Add the operation's required arguments or closure.
5. For a chain, make the previous `DotExpression` the next `operand`; do not place several operation nodes side-by-side.
6. Replace the original expression with the completed chain and validate the containing root.

Use [where-operation-subtree.json](blueprints/where-operation-subtree.json) for closure-based operations. `AnyOperation` has the same closure shape. For `SelectOperation`, the closure body returns one mapped value. For `TranslateOperation`, use one or more Closures `YieldStatement` nodes as shown in [translate-operation-subtree.json](blueprints/translate-operation-subtree.json).

## Add a Collections foreach

1. Use `jetbrains.mps.baseLanguage.collections.structure.ForEachStatement` for Collections `sequence`, `list`, `set`, or `map` values.
2. Add `ForEachVariable` under `variable`; set both `name` and `resolveInfo`.
3. Put the collection expression under `inputSequence`.
4. Put a BaseLanguage `StatementList` under `body`.
5. Refer to the loop variable with `ForEachVariableReference.variable`, not BaseLanguage `VariableReference`.
6. Validate the containing root after body statements are added.

Start with [foreach-statement-skeleton.json](blueprints/foreach-statement-skeleton.json). Resolve `$TARGET_SEQUENCE_VARIABLE$` in the destination model before insertion.

## Read or write an indexed element

For maps, create `MapElement` with `map` and `key`. For lists, create `ListElementAccessExpression` with `list` and `index`. Use the expression directly for a read; for a write, place it in the `lValue` role of a BaseLanguage assignment expression.

See [map-element-subtree.json](blueprints/map-element-subtree.json) and [list-element-access-subtree.json](blueprints/list-element-access-subtree.json).

## Large or mixed-language host code

1. Load the BaseLanguage skill for the surrounding method, statement, or expression nodes.
2. Load the model-manipulation skill when Collections is combined with closures, smodel, quotations, or model mutation.
3. Print the smallest existing host subtree that establishes the insertion role.
4. Add the Collections subtree surgically; avoid rewriting a whole class, service, rule, or generator root.
5. Validate the containing root and rebuild/reload when the changed host is a compiled language aspect.
