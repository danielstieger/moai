# Gotchas and diagnostics

- Except for the specialized `CustomContainers` registry, Collections concepts are not root nodes. Insert ordinary types, expressions, and statements into BaseLanguage or another host DSL, then validate the containing root.
- A collection operation alone is not the surface expression. It normally belongs in `DotExpression.operation`, paired with the receiver in `DotExpression.operand`.
- Chained calls require nested `DotExpression` nodes. Reusing one operand with several operation children violates cardinality.
- Closure parameters need a `type` child (`UndefinedType`) — `moai:mps-model-manipulation` (`references/closures-catalog.md`).
- `SelectOperation` (one-to-one) and `TranslateOperation` (yield, flattening) are not interchangeable — [concepts.md](concepts.md#select-vs-translate).
- Collections `ForEachStatement` and BaseLanguage `ForeachStatement` are different families; never mix them — [foreach-statements.md](foreach-statements.md).
- `MapElement` and `ListElementAccessExpression` are standalone expressions, not dot operations — [concepts.md](concepts.md#indexed-access).
- `IsEmptyOperation`/`IsNotEmptyOperation` exist in both Collections and BaseLanguage; pick by receiver type — [concepts.md](concepts.md#isempty--isnotempty-ambiguity).
- Do not use the deprecated set-specific operations in new code — [concepts.md](concepts.md#set-and-map-operations).
- Terminal accessors and reductions return `null` on empty input — [concepts.md](concepts.md#null-and-emptiness-semantics).
- Filtering/mapping/slicing are lazy; scalar results and materialization force traversal — [concepts.md](concepts.md#lazy-vs-eager).
- A placeholder such as `$TARGET_SEQUENCE_VARIABLE$` is not a distributable reference target. Resolve it in the destination model before a real write.
- Use the `qualifiedName` as `concept` (`moai:mps-mcp-workflow`, `references/node-editing-rules.md`); never use a `c:` concept reference where an API expects a persistent node reference.
- A `descriptorStatus: "hollow"` entry is untrustworthy; what to do: `moai:mps-language-analysis` (`references/concept-details.md`).
- After edits in compiled language aspects, reload/rebuild before validation.
- Never copy persistent references, domain names, or identifiers from an application project into this skill or its blueprints.

For deeper Collections/Closures/smodel interactions, use `moai:mps-model-manipulation` (`references/golden-rules-and-pitfalls.md`).
