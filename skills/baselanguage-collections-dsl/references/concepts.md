# Concepts and verified AST roles

These facts were verified against the live descriptors for `jetbrains.mps.baseLanguage.collections`. Re-query with `mps_mcp_get_concept_details` before using a feature not listed here. Of the 172 language concepts, only `CustomContainers` is rootable; the other concepts live inside a host-language root.

## Root concept for custom containers

`CustomContainers` is a specialized named root with `containerDeclaration` children (`0..n`). Each `CustomContainerDeclaration` has a required `containerType`, a required BaseLanguage `ClassifierType` in `runtimeType`, optional `factory`, type variables and visibility, plus a `name` property. Use it only when registering a custom collection abstraction/runtime implementation, not for ordinary list/set/map expressions.

## Collection types

| Concept | Required direct children | Meaning |
| --- | --- | --- |
| `SequenceType` | optional `elementType` (`0..1`) | Lazy/read-oriented sequence type |
| `ListType` | `elementType` (`1`) | Ordered mutable collection |
| `SetType` | `elementType` (`1`) | Unique-element mutable collection |
| `MapType` | `keyType` (`1`), `valueType` (`1`) | Key/value collection |
| `SortedSetType` | `elementType` (`1`) | Ordered set |
| `SortedMapType` | `keyType` (`1`), `valueType` (`1`) | Ordered map |
| `QueueType`, `DequeType`, `StackType` | `elementType` (`1`) | Queue/deque/stack abstractions |
| `ContainerIteratorType`, `EnumeratorType` | `elementType` (`1`) | Cursor abstractions |

Use a concrete BaseLanguage `Type` node below each type role. `UndefinedType` is appropriate only where later inference is intentional and accepted by the host concept.

## Collection creators

Creators are placed in the `creator` role of `jetbrains.mps.baseLanguage.structure.GenericNewExpression`.

| Concept | Important direct children |
| --- | --- |
| `ListCreatorWithInit` | `elementType` (`0..1`), `initValue` (`0..n`), `copyFrom` (`0..1`), `initSize` (`0..1`) |
| `LinkedListCreator` | same container-creator roles |
| `HashSetCreator`, `LinkedHashSetCreator` | same container-creator roles |
| `HashMapCreator`, `LinkedHashMapCreator` | `keyType` (`0..1`), `valueType` (`0..1`), `initializer` (`0..1`), `initSize` (`0..1`) |
| `TreeSetCreator` | container-creator roles plus optional `comparator` |
| `TreeMapCreator` | map-creator roles |
| `SequenceCreator` | optional `elementType`; optional Closures `ClosureLiteral` in `initializer` |
| `SingletonSequenceCreator` | optional `elementType`; required `singletonValue` |

## Dot-expression operations

Most operations have this outer shape:

```text
DotExpression
├─ operand: <collection expression>
└─ operation: <collections operation>
```

Important operation families:

| Family | Concepts | Direct operation children |
| --- | --- | --- |
| Filter/test | `WhereOperation`, `AnyOperation`, `AllOperation`, `FindFirstOperation`, `FindLastOperation`, `RemoveWhereOperation` | required `closure` |
| Map/flat-map | `SelectOperation`, `TranslateOperation` | required `closure`; `TranslateOperation` bodies normally use `YieldStatement` |
| Slice | `TakeOperation`, `SkipOperation`, `TailOperation`, `CutOperation`, `PageOperation` | count/range expressions as declared by the concept |
| Combine | `ConcatOperation`, `UnionOperation`, `ExcludeOperation`, `DisjunctOperation` | required `rightExpression` |
| Sort | `SortOperation` | required `ascending`, required `closure` |
| Fold | `FoldLeftOperation`, `FoldRightOperation` | required `seed`, required `closure` |
| Reduce | `ReduceLeftOperation`, `ReduceRightOperation` | required `closure` |
| Terminal access | `GetFirstOperation`, `GetLastOperation`, `GetSizeOperation`, `IsEmptyOperation`, `IsNotEmptyOperation` | no direct argument |
| Materialize | `ToListOperation`, `ToArrayOperation`, `ToIteratorOperation`, `ToStreamOperation` | normally no direct child; `ToStreamOperation` has property `parallel` |
| Mutation | `AddElementOperation`, `RemoveElementOperation`, `AddAllElementsOperation`, `RemoveAllElementsOperation` | required `argument` |
| Map operations | `ContainsKeyOperation`, `ContainsValueOperation`, `MapRemoveOperation`, `PutAllOperation`, `GetKeysOperation`, `GetValuesOperation`, `MapClearOperation` | key/value/map child where applicable |

For an exhaustive operation catalogue, including aliases, lazy/eager behavior, sorted ranges, and iterators, use [the bundled Collections catalogue](../../mps-model-manipulation/references/collections-catalog.md).

## Closures used by collection operations

`WhereOperation`, `SelectOperation`, `TranslateOperation`, `AnyOperation`, sorting, folds, and similar concepts store the closure in role `closure`. The normal closure shape is:

- `ClosureLiteral`
- `parameter` → `InferredClosureParameterDeclaration`
- parameter properties `name` and `resolveInfo`
- parameter `type` → `UndefinedType` (required structural placeholder)
- `body` → BaseLanguage `StatementList`
- one or more `statement` nodes; an expression result is wrapped in `ExpressionStatement`

Within one blueprint, a `VariableReference.variableDeclaration` may target the declared parameter by its plain name, such as `it`.

## Collection foreach

`ForEachStatement` has:

- required `variable` → `ForEachVariable`
- required `inputSequence` → BaseLanguage `Expression`
- required `body` → BaseLanguage `StatementList`
- optional `loopLabel`
- optional `label` property

`ForEachVariable` stores `name` and `resolveInfo` but no type child. References inside the body use `ForEachVariableReference.variable`, not BaseLanguage `VariableReference.variableDeclaration`.

## Indexed access

- `MapElement` is a standalone expression with required `map` and `key` children.
- `ListElementAccessExpression` is a standalone expression with required `list` and `index` children.
- Reads use these expressions directly. Writes place one of them in the `lValue` role of a BaseLanguage assignment expression.
