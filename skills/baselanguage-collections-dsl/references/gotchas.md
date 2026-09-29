# Gotchas and diagnostics

- Except for the specialized `CustomContainers` registry, Collections concepts are not root nodes. Insert ordinary types, expressions, and statements into BaseLanguage or another host DSL, then validate the containing root.
- A collection operation alone is not the surface expression. It normally belongs in `DotExpression.operation`, paired with the receiver in `DotExpression.operand`.
- Chained calls require nested `DotExpression` nodes. Reusing one operand with several operation children violates cardinality.
- `InferredClosureParameterDeclaration` still requires a `type` child. Use `UndefinedType`; omitting it causes misleading closure-arity, null-type, and operation-applicability errors.
- A closure result is normally an `ExpressionStatement` in the closure `StatementList`. `TranslateOperation` is different: it emits values with Closures `YieldStatement` and may emit zero or many values.
- `SelectOperation` maps one input to one result. `TranslateOperation`/`selectMany` flattens yielded results. Do not substitute one solely because the editor text looks similar.
- Collections `ForEachStatement` uses `ForEachVariable` and `ForEachVariableReference`. BaseLanguage `ForeachStatement` uses `LocalVariableDeclaration` and `VariableReference`; mixing the two families produces type or reference errors.
- `MapElement` and `ListElementAccessExpression` are standalone expressions, not dot operations.
- The Collections and BaseLanguage languages both define `IsEmptyOperation` and `IsNotEmptyOperation`. Use the Collections FQN for collection receivers and the BaseLanguage FQN for strings.
- Deprecated set-specific operations such as `AddSetElementOperation` and `RemoveSetElementOperation` should not be used in new code; use the general collection operations.
- Terminal accessors such as `first`, `last`, `findFirst`, and reductions may be nullable on empty input. Preserve the language's empty/null semantics when translating to host logic.
- Filtering, mapping, slicing, and concatenation are generally lazy; scalar results, materialization, and side effects force traversal. Avoid assuming that a lazy operation has already executed.
- A placeholder such as `$TARGET_SEQUENCE_VARIABLE$` is not a distributable reference target. Resolve it in the destination model before a real write.
- Always use fully qualified concept names. Never use a `c:` concept reference where an API expects a persistent node reference.
- If a descriptor is `hollow`, rebuild the language module before trusting empty features. After edits in compiled language aspects, reload/rebuild before validation.
- Never copy persistent references, domain names, or identifiers from an application project into this skill or its blueprints.

For deeper Collections/Closures/smodel interactions, use [the bundled model-manipulation diagnostics](../../mps-model-manipulation/references/golden-rules-and-pitfalls.md).
