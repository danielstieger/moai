# What `mps_mcp_parse_java_and_insert` Can and Cannot Do

Open before calling the Java parser. The parser understands plain Java plus the Java 8+ syntax MPS recognizes (notably lambdas, which map to `baseLanguage.closures` closures — see below); it cannot produce smodel/collection types or most other MPS-specific concept nodes — construct those directly.

## What the Java parser CAN handle

Use `mps_mcp_parse_java_and_insert` freely for:

- `featureKind: "METHOD"` — whole method including signature (see "Method return types" below for the caveat)
- `featureKind: "EXPRESSION"` — replacing a single expression node (`insert.mode: "replace"` + `targetRef`); `contextNodeRef` must lie inside the same body so that parameters and locals resolve. Arguments in smodel syntax (casts, `.link`) cannot be parsed — pass the uncasted node and derive the narrower value inside the called method.
- `featureKind: "STATEMENTS"` — replacing or inserting a statement block
- `featureKind: "FIELD"` — single field declarations (for adding to LINKS/CONCEPTS classes)

Things that resolve correctly:

- Static Java method calls: `SomeHelper.check(...)`, `SNodeOperations.xxx(...)`, `<Concept>__BehaviorDescriptor.<method>_id<…>.invoke(...)`
- Identifiers that are **already known in the context** — local variables and parameters — resolve to their MPS model equivalents
- `LINKS.xxx` and `CONCEPTS.xxx` field references (inner-class constants) resolve fine
  as long as they already exist on the target class
- `MetaAdapterFactory.getConcept(...)`, `MetaAdapterFactory.getReferenceLink(...)` resolve,
  but see the note on `getContainmentLink` below

## Java 8 lambdas → closures

Lambda expressions parse and insert: each becomes a `jetbrains.mps.baseLanguage.closures.ClosureLiteral` (an expression-bodied lambda such as `() -> 42` becomes a closure whose trailing expression is its result), and the closures language is auto-imported when `postProcess.importUsedLanguages` is on. They are **not** plain Java in the MPS sense — they cross into the `closures` extension. A lambda only type-checks against a matching **functional-type** target (e.g. `() -> 42` fits a `{() => int}` slot, but not an `int` slot); untyped parameters get the closures `var` type and rely on the target to infer. A type mismatch at the destination is surfaced in the tool response's `problems` array — **not** as a parse error — so inspect `problems` after inserting a lambda. Java constructs the MPS parser does not recognize (e.g. records) still fail with a parse error; JSON blueprints have no lambda syntax — build a `closures` `ClosureLiteral` (`closures-catalog.md`).

## What the Java parser CANNOT handle (and how to work around it)

### Method return types with MPS collection types

The Java parser does **NOT** correctly produce MPS collection types when `java.util.List<SNode>`
(or similar) appears as a **method return type**. In that position it produces a Java
`ClassifierType` (e.g. `ClassifierType(java.util.List<SNode>)`) instead of `ListType`.

This causes a type mismatch error at the call site when the result is assigned to
an MPS `sequence<node<Type>>` or `list<node<Type>>` variable.

**Fix**: After parsing the method, replace the `returnType` child using
`mps_mcp_update_node`:

| Needed MPS return type | Blueprint |
|---|---|
| `sequence<node<Type>>` | `SequenceType(elementType: SNodeType(concept: Type))` |
| `list<node<Type>>` | `ListType(elementType: SNodeType(concept: Type))` |

Full blueprints: `variable-declarations.md`.

**Note**: the parser never produces MPS collection/smodel types in any position — `List<SNode> x = …` and `new ArrayList<SNode>()` parse to Java `ClassifierType`s, which is fine as long as the code stays plain Java. Method return types are where this bites, because MPS callers expect `sequence<node<X>>`/`list<node<X>>`.

### Where the Java parser produces wrong types

The Java parser produces correct MPS types in most positions, but fails for
**method return types** when the intended type is an MPS collection or node type.

| Location | Intended MPS type | Java-parser result | Action |
|---|---|---|---|
| Method **return type** | `sequence<node<Type>>` | `ClassifierType(List<SNode>)` — **wrong** | Replace `returnType` child after parsing |
| Method **return type** | `list<node<Type>>` | `ClassifierType(List<SNode>)` — **wrong** | Same |
| Method parameter type | `node<CatchClause>` | `ClassifierType(SNode)` — Java type | Fine for most purposes; replace if MPS type checking fails |

When a local variable or `new` expression must have an MPS type (`list<node<X>>`, `new arraylist<node<X>>`), construct it directly using the blueprints in `variable-declarations.md` — the parser has no syntax for them.

**After parsing a method**, check its `returnType` and parameter `type` children.
If they should be MPS collection or smodel types, replace them using `mps_mcp_update_node`.

### smodel language expressions

These concepts live in `jetbrains.mps.lang.smodel` and are not parseable from Java:

| MPS notation | Concept | Workaround |
|---|---|---|
| `node.link` or `node:Concept.link` | `SLinkAccess` inside `DotExpression` | Already in tree; keep it, or use `SLinkOperations.getTarget` in parsed Java |
| `node:SomeConcept` (type-cast) | `SNodeTypeCastExpression` | Cannot be parsed; if you need the casted node as an argument, restructure: pass the uncasted node and derive the cast inside the Java method |
| `.someBehaviorMethod()` (behavior method call) | `Node_ConceptMethodCall` | Cannot be parsed; build the `DotExpression` by hand (see `dot-expression-basics.md`) or call the generated behavior descriptor directly: `<Concept>__BehaviorDescriptor.<method>_id<…>.invoke(node)` |
| `node.parent:C` | `DotExpression(Node_GetParentOperation, SNodeTypeCastExpression)` | Cannot be parsed; use `SNodeOperations.getParent(node)` + `SNodeOperations.cast(...)` in parsed Java |

### `MetaAdapterFactory.getContainmentLink` inside method bodies

`MetaAdapterFactory.getContainmentLink(long, long, long, long, String)` does **not**
reliably resolve when used inline inside a parsed method body.  This causes a cascade of
`UnknownDotCall` errors because the return type of the unresolved call is `undefined`,
breaking all downstream type inference.

**Root cause**: generated MPS code never calls `MetaAdapterFactory.getContainmentLink` inline; it uses `LINKS.xxx` static inner-class constants.

**Fix**: use the `LINKS.xxx` pattern:

1. If the constant you need already exists in the class's `LINKS` inner class, use it directly.
2. If it does not exist, add it first with `mps_mcp_parse_java_and_insert`:
   ```json
   {
     "featureKind": "FIELD",
     "contextNodeRef": "<LINKS-inner-class-node-ref>",
     "code": "/*package*/ static final SContainmentLink throwable$kKKg = MetaAdapterFactory.getContainmentLink(0xf3061a5392264cc5L, 0xa443f952ceaf5816L, 0x10f3ee082d8L, 0x10f3ee0cd6fL, \"throwable\");",
     "insert": { "mode": "child", "parentRef": "<LINKS-class-ref>", "role": "member" }
   }
   ```
   Then reference `LINKS.throwable$kKKg` in the method body.

> The `LINKS` inner class node ref is found by printing the parent class (shallow depth)
> and reading the node ref of the nested class child.

### Behavior method invocations through descriptors

Behavior descriptor calls use the pattern:
```java
SomeDescriptor.methodName_idXXXX.invoke(targetNode, arg1, arg2)
```
These work fine when parsed as Java because the descriptor constants are plain static fields.
The only pitfall: the `invoke` method is typed as `Object invoke(...)` so pass arguments
with explicit casts when needed (e.g. `((boolean) false)` for boolean params).
