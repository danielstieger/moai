# Gotchas and diagnostics

- Except for the specialized `CustomContainers` registry, Collections concepts are not root nodes. Insert ordinary types, expressions, and statements into BaseLanguage or another host DSL, then validate the containing root.
- A collection operation alone is not the surface expression. It normally belongs in `DotExpression.operation`, paired with the receiver in `DotExpression.operand`.
- Chained calls require nested `DotExpression` nodes. Reusing one operand with several operation children violates cardinality.
- Closure parameters need a `type` child (`UndefinedType`) — [closures-catalog.md](closures-catalog.md#closure-parameter-notes). Without it: "different parameter numbers" on the `ClosureLiteral` plus "out of search scope" / "operation is not applicable to null" in its body.
- Operations taking a predicate/selector take exactly one `ClosureLiteral` in role `closure`, not `parameter`.
- A `sequence<T>` is rejected where a `list<T>` is required: `list<T>` and `set<T>` are subtypes of `sequence<T>`, not the reverse, and lazy operations (`where`, `select`, `translate`, …) return `sequence<T>`. Materialize with `.toList` (`ToListOperation`) or widen the target to `sequence<T>`.
- Side effects in a closure fire twice, or not at all: filtering/mapping operations and yielding closures are lazy, fire only on consumption, and re-iterate on each consumption. Materialize once (`.toList`) when the result is consumed more than once.
- A closure body uses either `return` or `yield`, never both; a `yield` closure returns `sequence<T>` — [closures-catalog.md](closures-catalog.md#yield-vs-return-mutual-exclusion).
- `skip;` / `stop;` only inside a closure passed to `selectMany`/`translate`/`forEach` or a sequence initializer; elsewhere they are a typesystem error — [concepts.md](concepts.md#control-flow-within-closures).
- `NoClassDefFoundError` for `_FunctionTypes$...` at load time (not compile time): the module that first introduces closures lacks `jetbrains.mps.baseLanguage.closures.runtime`; collections code also needs `collections.runtime` — [closures-catalog.md](closures-catalog.md#runtime-dependency).
- `SelectOperation` (one-to-one) and `TranslateOperation` (yield, flattening) are not interchangeable — [concepts.md](concepts.md#select-vs-translate).
- Collections `ForEachStatement` and BaseLanguage `ForeachStatement` are different families; never mix them. A typesystem error about the iteration protocol in a `foreach` means the BaseLanguage concept was used over a `sequence<T>` — [foreach-statements.md](foreach-statements.md).
- `MapElement` and `ListElementAccessExpression` are standalone expressions, not dot operations — [concepts.md](concepts.md#indexed-access).
- `IsEmptyOperation`/`IsNotEmptyOperation` exist in both Collections and BaseLanguage; pick by receiver type — [concepts.md](concepts.md#isempty--isnotempty-ambiguity). When the receiver type is unclear (here, for the foreach family, or for `list` vs `sequence`), ask `mps_mcp_query_types` / `mps_mcp_query_nodes` `GET_TYPE` — `moai:mps-mcp-workflow` (`references/type-queries.md`).
- Do not use the deprecated set-specific operations in new code — [concepts.md](concepts.md#set-and-map-operations).
- Terminal accessors and reductions return `null` on empty input — [concepts.md](concepts.md#null-and-emptiness-semantics).
- Filtering/mapping/slicing are lazy; scalar results and materialization force traversal — [concepts.md](concepts.md#lazy-vs-eager).
- A placeholder such as `$TARGET_SEQUENCE_VARIABLE$` is not a distributable reference target. Resolve it in the destination model before a real write. The dry-run does not look names up ("is a name, not looked up" is expected), so a forgotten placeholder passes it: search the blueprint text for `TARGET_` before writing, and require `fixReferences.stillBroken` = 0 after the real write.
- Use the `qualifiedName` as `concept` (`moai:mps-mcp-workflow`, `references/node-editing-rules.md`); never use a `c:` concept reference where an API expects a persistent node reference. In a reference role the insert accepts a `c:` ref silently and leaves it unresolved; only `mps_mcp_check_root_node_problems` reports it.
- A `descriptorStatus: "hollow"` entry is untrustworthy; what to do: `moai:mps-language-analysis` (`references/concept-details.md`).
- After edits in compiled language aspects, reload/rebuild before validation.
- Never copy persistent references, domain names, or identifiers from an application project into this skill or its blueprints.

## Node factories

Node factories run on every real insert (not in the dry-run). A factory fills only the roles a blueprint omits; a named role, even an empty `{"role":"…","nodes":[]}`, replaces the factory content. Every blueprint here passes a real insert with `stillBroken` = 0 and no checker errors; `print_node` the result when inserting other concepts.

For smodel errors inside closure bodies (`UnknownDotCall`, untyped `node<>` operands), use `moai:mps-model-manipulation` (`references/golden-rules-and-pitfalls.md`).
