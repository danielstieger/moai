# Concepts and verified AST roles

These facts were verified against the live descriptors for `jetbrains.mps.baseLanguage.collections`. Re-query with `mps_mcp_get_concept_details` before using a feature not listed here. Of the 172 language concepts, only `CustomContainers` is rootable; the other concepts live inside a host-language root.

## Root concept for custom containers

`CustomContainers` is a specialized named root with `containerDeclaration` children (`0..n`). Each `CustomContainerDeclaration` has a required `containerType`, a required BaseLanguage `ClassifierType` in `runtimeType`, optional `factory`, type variables and visibility, plus a `name` property. Use it only when registering a custom collection abstraction/runtime implementation, not for ordinary list/set/map expressions.

## Core concept IDs

All concept refs start with `c:83888646-71ce-4f1c-9c53-c54016f6ad4f/...`. When you need an ID not listed here, prefer `mps_mcp_search_concepts` with the expected name — there are many short-named `*Operation` concepts and typos silently resolve to the wrong one.

| Concept | Full `conceptReference` | MPS notation |
|---|---|---|
| `SequenceType` | `c:83888646-71ce-4f1c-9c53-c54016f6ad4f/1151689724996` | `sequence<T>` type |
| `ListType` | `c:83888646-71ce-4f1c-9c53-c54016f6ad4f/1151688443754` | `list<T>` type |
| `SetType` | `c:83888646-71ce-4f1c-9c53-c54016f6ad4f/1226511727824` | `set<T>` type |
| `ListCreatorWithInit` | `c:83888646-71ce-4f1c-9c53-c54016f6ad4f/1160600644654` | `new arraylist<T>` / `new linkedlist<T>` |
| `HashSetCreator` | `c:83888646-71ce-4f1c-9c53-c54016f6ad4f/1226516258405` | `new hashset<T>` |
| `WhereOperation` | `c:83888646-71ce-4f1c-9c53-c54016f6ad4f/1202120902084` | `.where { predicate }` |
| `AnyOperation` | `c:83888646-71ce-4f1c-9c53-c54016f6ad4f/1235566554328` | `.any { predicate }` |
| `TranslateOperation` | `c:83888646-71ce-4f1c-9c53-c54016f6ad4f/1201792049884` | `.translate { it => yield ...; ... }` — flatMap-style; body is a closure that may `yield` multiple elements |
| `AddElementOperation` | `c:83888646-71ce-4f1c-9c53-c54016f6ad4f/1160612413312` | `.add(element)` |
| `SkipStatement` | `c:83888646-71ce-4f1c-9c53-c54016f6ad4f/1224446583770` | `continue;` inside a collections `foreach` or `.translate`/`.where`/etc. closure |
| `ForEachStatement` (collections) | `c:83888646-71ce-4f1c-9c53-c54016f6ad4f/1153943597977` | `foreach v in sequence { ... }` — see `foreach-statements.md` |
| `ForEachVariable` | `c:83888646-71ce-4f1c-9c53-c54016f6ad4f/1153944193378` | Loop variable of the collections `ForEachStatement`. **Not** a `LocalVariableDeclaration`. |
| `ForEachVariableReference` | `c:83888646-71ce-4f1c-9c53-c54016f6ad4f/1153944233411` | Reference to a `ForEachVariable` inside the loop body. **Not** a `VariableReference`. |

`DowncastExpression` (`downcast expr`, collection type → Java interface): `moai:mps-model-manipulation` (`references/dot-expression-basics.md`).

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

Use a concrete BaseLanguage `Type` node below each type role.

Type hierarchy:

```
sequence<T>    ← Iterable-like, lazy
  list<T>      ← ordered, indexed, mutable
  set<T>       ← unordered unique (hashset | linked_hashset)
  map<K,V>     ← key→value; also a sequence<MapEntry<K,V>>
    sorted_map<K,V>
```

- `map` is a sequence of entries — you can pass it anywhere `sequence` is expected.
- Sorted variants exist: `sortedset<T>`, `sorted_map<K,V>` (see "Sorted collections").

## Null and emptiness semantics

- Assigning `null` to a `sequence`/`list`/`set`/`map` typed variable yields an **empty** collection; subsequent operations do **not** NPE.
- Terminal accessors on empty sequences return **null** instead of throwing: `seq.first`, `seq.last`, `seq.findFirst{..}`, `seq.reduceLeft{..}` → `null` when empty. Preserve these empty/null semantics when translating to host logic.
- This affects null-check placement in generated Java — explicit `== null` checks after `first`/`last` are idiomatic, not defensive noise.

## Collection creators

Creators are placed in the `creator` role of `jetbrains.mps.baseLanguage.structure.GenericNewExpression`.

| Concept | MPS expression | Important direct children |
| --- | --- | --- |
| `ListCreatorWithInit` | `new arraylist<T>` | `elementType` (`0..1`), `initValue` (`0..n`), `copyFrom` (`0..1`), `initSize` (`0..1`) |
| `LinkedListCreator` | `new linkedlist<T>` | same container-creator roles |
| `HashSetCreator`, `LinkedHashSetCreator` | `new hashset<T>`, `new linked_hashset<T>` | same container-creator roles |
| `HashMapCreator`, `LinkedHashMapCreator` | `new hashmap<K,V>`, `new linked_hashmap<K,V>` | `keyType` (`0..1`), `valueType` (`0..1`), `initializer` (`0..1`), `initSize` (`0..1`) |
| `TreeSetCreator` | — | container-creator roles plus optional `comparator` |
| `TreeMapCreator` | — | map-creator roles |
| `SequenceCreator` | `new sequence<T>({=> yield ...})` | optional `elementType`; optional Closures `ClosureLiteral` in `initializer` |
| `SingletonSequenceCreator` | — | optional `elementType`; required `singletonValue` |

The optional brace initializer (`{a, b, c}` for lists/sets, `{k=v, k=v}` for maps) is a separate child role (`initValue` / `initializer` above).

## Dot-expression operations

Most operations have this outer shape:

```text
DotExpression
├─ operand: <collection expression>
└─ operation: <collections operation>
```

Operations with a predicate/selector hold a `ClosureLiteral` in role `closure`; closure shape, `UndefinedType` and plain-name parameter references: `moai:mps-model-manipulation` (`references/closures-catalog.md`, Closure literal blueprint).

Important operation families (verified direct children):

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

### Sequence operations (syntax, laziness, result)

| Syntax | Operation concept | Lazy? | Returns |
|---|---|---|---|
| `seq.where{it=>P}` | `WhereOperation` | ✓ | `sequence<T>` |
| `seq.select{it=>E}` | `SelectOperation` | ✓ | `sequence<U>` |
| `seq.selectMany{it=>Es}` | `TranslateOperation` (alias `selectMany`) | ✓ | `sequence<U>` |
| `seq.translate{it=>yield..}` | `TranslateOperation` | ✓ | `sequence<U>` (yields) |
| `seq.ofType<C>` | `OfTypeOperation` | ✓ | `sequence<C>` |
| `seq.take(n)` / `.skip(n)` / `.tail(n)` / `.cut(n)` / `.page(a,b)` | `TakeOperation` etc. | ✓ | `sequence<T>` |
| `seq.distinct` | `DistinctOperation` | ✓ | `sequence<T>` |
| `seq.reverse` | `ReverseOperation` | — | `list<T>` (new list) |
| `seq.sortBy{..}, asc` / `.alsoSortBy{..}, asc` / `.sort{a,b=>cmp}` | `SortOperation` (children `closure`, `ascending`) / `AlsoSortOperation` (extends `SortOperation`) / `ComparatorSortOperation` (`closure`, optional `ascending`) | force | `sequence<T>` |
| `seq.concat(other)` / `.union` / `.intersect` / `.except` / `.disjunction` | matching `*Operation` | ✓ | `sequence<T>` |
| `seq.any{..}` / `.all{..}` | `AnyOperation` / `AllOperation` | force | `boolean` |
| `seq.contains(x)` / `.indexOf(x)` | `ContainsOperation` / `IndexOfOperation` | force | `boolean` / `int` |
| `seq.findFirst{..}` / `.findLast{..}` | `FindFirstOperation` / `FindLastOperation` | force | `T` (nullable) |
| `seq.first` / `.last` | `GetFirstOperation` / `GetLastOperation` | force | `T` (nullable) |
| `seq.size` | `GetSizeOperation` | force | `int` |
| `seq.isEmpty` | `IsEmptyOperation` (collections) | force | `boolean` |
| `seq.isNotEmpty` | `IsNotEmptyOperation` (collections) | force | `boolean` |
| `seq.reduceLeft{..}` / `.foldLeft(z){..}` | `ReduceLeftOperation` / `FoldLeftOperation` | force | `T` / `Z` |
| `seq.toList` / `.toArray` | `ToListOperation` / `ToArrayOperation` | force | materialized |
| `seq.join(",")` | `JoinOperation` | force | `string` |
| `seq.forEach{it=>..}` (dot-op form) | `VisitAllOperation` (alias `forEach`) | force | — |

`seq.ofConcept<C>` is the smodel `OfConceptOperation`: `moai:mps-model-manipulation` (`references/smodel-concepts-catalog.md`).

The dot-op `seq.forEach{..}` (concept `VisitAllOperation`) is distinct from the statement-level `foreach v in seq { .. }` (concept `ForEachStatement`, see `foreach-statements.md`). They look similar in prose but have different AST shapes.

### Select vs translate

`SelectOperation` maps one input to one result. `TranslateOperation`/`selectMany` flattens the values its closure emits with `YieldStatement` (zero or many per input); a non-yielding closure normally ends with an `ExpressionStatement` as its result. Do not substitute one solely because the editor text looks similar.

`YieldStatement` (closures; single child `expression`) emits one element per executed `yield`; the result of `.translate` is the concatenation of all yielded elements across all inputs. This is the idiomatic way to express tree traversals that produce a flat sequence of nodes (replacement for imperative collect-into-list loops), e.g.:

```
sequence<node<ReturnStatement>> collected =
    root.children.translate { it =>
      if (it.isInstanceOf<ReturnStatement>) { yield it:ReturnStatement; }
      foreach sub in collectReturnStatements(it) { yield sub; }
    };
```

### Lazy vs eager

Filtering/mapping/`ofType`/`take`/`skip`/`distinct`/`concat` are lazy; everything that returns a scalar, `boolean`, `int`, materialized collection, or performs side effects forces iteration. Do not assume a lazy operation has already executed.

### `isEmpty` / `isNotEmpty` ambiguity

There are two unrelated concepts with the same name:

| FQN | ID | Applies to |
|---|---|---|
| `jetbrains.mps.baseLanguage.collections.structure.IsEmptyOperation` | `1165530316231` | `sequence<T>`, `list<T>`, `set<T>`, `map<K,V>` |
| `jetbrains.mps.baseLanguage.collections.structure.IsNotEmptyOperation` | `1176501494711` | same collections |
| `jetbrains.mps.baseLanguage.structure.IsEmptyOperation` | `1225271369338` | `string` |
| `jetbrains.mps.baseLanguage.structure.IsNotEmptyOperation` | `1225271408483` | `string` |

Pick the correct one based on the receiver's type: `node.someRole.isEmpty` on a multi-cardinality containment uses the **collections** variant (because `.someRole` yields a sequence), while `node.name.isEmpty` on a `string` property uses the **baseLanguage** variant. Using the wrong FQN in a blueprint produces a constraint error even though the surface syntax is identical.

## List mutators

`ListType` adds (all are `*Operation` concepts, statement or expression; indexed `list[i]` access: see "Indexed access"):

| Syntax | Concept |
|---|---|
| `list.set(i,v)` | `SetElementOperation` (alias `set`) |
| `list.insert(i,v)` | `InsertElementOperation` (alias `insert`) |
| `list.add(v)` (implicit `+=`) | `AddElementOperation` |
| `list.addFirst(v)` / `addLast(v)` | `AddFirstElementOperation` / `AddLastElementOperation` |
| `list.addAll(seq)` / `removeAll(seq)` | `AddAllElementsOperation` / `RemoveAllElementsOperation` |
| `list.remove(v)` (by value) | `RemoveElementOperation` |
| `list.removeFirst` / `removeLast` | `RemoveFirstElementOperation` / `RemoveLastElementOperation` |
| `list.clear` | `ClearAllElementsOperation` |

## Set and map operations

Sets reuse the collection-level concepts: `set.add(v)` → `AddElementOperation`, `set.addAll(seq)` → `AddAllElementsOperation`, `set.remove(v)` → `RemoveElementOperation`, `set.removeAll(seq)` → `RemoveAllElementsOperation`, `set.clear` → `ClearAllElementsOperation`. (Deprecated `AddSetElementOperation` / `RemoveSetElementOperation` exist but should not be used in new code — they were superseded in 2018.3.)

`set.iterator` → `GetIteratorOperation`. For a mutable set, this yields a **`modifying_iterator`**, enabling in-place removal during traversal — not a plain Java iterator (see "Iterator and modifying_iterator" below).

Maps (indexed `map[k]` access: see "Indexed access"):

| Syntax | Concept |
|---|---|
| `map.containsKey(k)` / `.containsValue(v)` | `ContainsKeyOperation` / `ContainsValueOperation` |
| `map.keys` / `.values` | `GetKeysOperation` / `GetValuesOperation` |
| `map.removeKey(k)` | `MapRemoveOperation` (alias `removeKey`) |
| `map.clear` | `MapClearOperation` |
| `map.putAll(other)` | `PutAllOperation` |

`map.keys` and `.values` return **sequences** (live views), not new collections.

## Indexed access

- `map[k]` → `MapElement`, a standalone expression (not a dot operation) with required `map` and `key` children.
- `list[i]` → `ListElementAccessExpression`, a standalone expression (not a dot operation) with required `list` and `index` children.
- Reads use these expressions directly. Writes (`map[k] = v`, `list[i] = v`) place one of them in the `lValue` role of a BaseLanguage `AssignmentExpression`.

## Control flow within closures

Inside a closure passed to `selectMany`/`translate`/`forEach`/sequence initializer:

- `skip;` — abort this element, go to next input element (concept: `SkipStatement`).
- `stop;` — terminate the outer sequence construction entirely, discarding the rest of the input (concept: `StopStatement`).
- `yield expr;` — emit into the output sequence (from the closures language; `moai:mps-model-manipulation`, `references/closures-catalog.md`).

`skip`/`stop` only make sense in the enumerated contexts; using them elsewhere yields a typesystem error.

## Collection foreach

`ForEachStatement`/`ForEachVariable`/`ForEachVariableReference` vs BaseLanguage `ForeachStatement`, with blueprints: `foreach-statements.md`.

## Sorted collections

Types `sortedset<T>` / `sorted_map<K,V>` add range operations on top of their unordered cousins. Creators: `TreeSetCreator` and `TreeMapCreator` (both wrapped in `GenericNewExpression`). A `sortedset` iterates in natural/comparator order; likewise `sorted_map.keys` is ordered.

Range operations (all sit in the `operation` role of a `DotExpression`; all share the same arity as their `java.util.SortedSet` / `SortedMap` analogues):

| Syntax | Concept | Returns |
|---|---|---|
| `sortedset.headSet(hi)` | `HeadSetOperation` | `sortedset<T>` (elements `< hi`) |
| `sortedset.tailSet(lo)` | `TailSetOperation` | `sortedset<T>` (elements `≥ lo`) |
| `sortedset.subSet(lo, hi)` | `SubSetOperation` | `sortedset<T>` (range `[lo, hi)`) |
| `sorted_map.headMap(hi)` | `HeadMapOperation` | `sorted_map<K,V>` |
| `sorted_map.tailMap(lo)` | `TailMapOperation` | `sorted_map<K,V>` |
| `sorted_map.subMap(lo, hi)` | `SubMapOperation` | `sorted_map<K,V>` |

The returned collections are **live views** over the original — writes through them propagate. Use `.toList` or a fresh creator if you need an independent snapshot.

## Iterator and modifying_iterator

Two distinct iterator types:

- `iterator<T>` — read-only cursor. Methods: `.hasNext`, `.next`. Produced by `GetIteratorOperation` (alias `iterator`) on any sequence/collection.
- `modifying_iterator<T>` — cursor that also supports `.remove` (delete the element most recently returned by `.next`). Produced by `.iterator` on a **mutable** collection (`list`, `set`, map views). Using `.remove` on a plain `iterator<T>` is a typesystem error.

Typical "remove-while-iterating" pattern:

```
var it = mySet.iterator;
while (it.hasNext) {
  var e = it.next;
  if (shouldDrop(e)) { it.remove; }
}
```

In AST terms: `.hasNext`, `.next`, `.remove` are `DotExpression` operations whose operand is the iterator variable. Search concept names when needed — they follow the same `*Operation` convention as the rest of this catalog.
