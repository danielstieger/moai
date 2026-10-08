# Golden Rules and Common Pitfalls

Read this first when an error message looks weird or you're about to write your first DotExpression chain.

## Golden rules

- **Node equality**: `:eq:`/`:ne:` only — `node-equality.md`.
- **Closure parameter needs a `type` child**: every `InferredClosureParameterDeclaration` needs a `type` child (`UndefinedType`), otherwise misleading cascade errors follow — `closures-catalog.md`, Closure parameter notes.

## Background: two worlds in one model

Model code mixing these languages uses:

| Layer | Language | Generated Java | Examples |
|---|---|---|---|
| Core statements / expressions | BaseLanguage | plain Java | `if`, `for`, local variables, assignments, static calls |
| Node / link access | `smodel` | `SLinkOperations.getTarget(node, link)` | `node.link`, `node:Concept`, `.parent:C` |
| Typed collections | `collections` | `ListSequence`, `SetSequence`, `Sequence` | `sequence<node<T>>`, `list<node<T>>`, `hashset<>` |
| Lambda / closure | `closures` | anonymous class or lambda | `(x) -> ...`, generator-style iterators |

The MPS **type system** tracks these separately: `sequence<node<Type>>` is an MPS
`SequenceType` containing an `SNodeType`, which is entirely different from
`java.util.List<SNode>`, even though both generate to `Iterable<SNode>`.

What `mps_mcp_parse_java_and_insert` can and cannot produce (lambdas, smodel/collection types, casts): `java-parser-capabilities.md`.

## Common pitfalls (symptom → cause → fix)

| Symptom | Cause | Fix |
|---|---|---|
| `UnknownDotCall` for `SLinkOperations.getTarget` | Inline `MetaAdapterFactory.getContainmentLink` argument could not be resolved | Use `LINKS.xxx` constant instead of inline MetaAdapterFactory call |
| `UnknownDotCall` for `MetaAdapterFactory.getContainmentLink` | Java parser can't match the `(long,long,long,long,String)` overload in this context | Never call getContainmentLink in method bodies; always use LINKS/CONCEPTS constants |
| `type undefined is not a subtype of SNode` (cascade) | A preceding unresolved call returned `undefined` type | Fix the first `UnknownDotCall` and the cascade disappears |
| `type List<SNode> is not a subtype of sequence<node<Type>>` | Method return type was parsed as Java `List<SNode>` instead of MPS `SequenceType` | Replace the `returnType` child after parsing using `mps_mcp_update_node` |
| Smodel expression (e.g. `:CatchClause` cast) cannot be passed as argument | Java parser has no syntax for smodel casts | Change method signature to accept wider node and compute cast inside the method |
| `access to link 'X' is not expected here` / `out of search scope` despite correct cardinality | Operand typed as `node<>` rather than `node<X>` (e.g. `ForEachVariable` over `sequence<node<>>`, loosely-typed parameter) | Wrap operand in `SNodeTypeCastExpression` to typed `node<X>` — see "Operand must be a typed `node<X>`" in `dot-expression-basics.md` |
| `"different parameter numbers"` on a `ClosureLiteral` + `"out of search scope"` / `"operation is not applicable to null"` inside the closure body | The `InferredClosureParameterDeclaration` was inserted without its required `type` child, so closure-signature inference fails and the parameter's type stays null | Add the missing `type` child (`UndefinedType`) on `InferredClosureParameterDeclaration` — `closures-catalog.md` |
