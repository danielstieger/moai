# `mps_mcp_get_concept_details` — Resolution Semantics & Result Schema

Gets detailed information about a list of MPS concepts, including their properties, references, and children. `data` is inline when the serialized result is at most `maxInlineBytes` (default 20000), otherwise the path of a local JSON file holding the same `{ok, data}` envelope. Concepts can be specified individually (`conceptRefs`) or by language (`languageRefs`) — every concept and interface concept of each listed language is included.

## Input form

Each selector accepts either one value or a JSON array; a real array and the array written as a
string are equivalent. For example, use
`conceptRefs = "jetbrains.mps.baseLanguage.structure.ClassConcept"` for one concept, or
`conceptRefs = "[\"…ClassConcept\", \"…InterfaceConcept\"]"` for several. `languageRefs`
uses the same form and also accepts the bare language name (`l:<uuid>:<name>` works too). Omit an unused selector; when both are absent or blank, the tool preserves its
existing `No concepts nor languages have been provided` error.

## Unresolved refs are never silently dropped

The tool distinguishes three response shapes:

| Resolution outcome | Envelope | Payload |
|---|---|---|
| All refs resolved | `ok:true` | `data`: the concept array inline, or `"/path/to/file.json"` above `maxInlineBytes` |
| Some refs failed, at least one resolved | `ok:true` | `data` as above, plus `warnings` naming each unresolved ref and `details.unresolved` with "did you mean" suggestions |
| Every `conceptRef` and `languageRef` failed | `ok:false`, code `NOT_FOUND` | `details.unresolved` with up to 5 "did you mean" candidates per unresolved ref (qualified names and persistent references) |

## An enumeration is not a concept

This tool returns **concepts and interface concepts only**. An `EnumerationDeclaration` (or another non-concept structure root such as a constrained data type) is never returned, however the ref is spelled. Such a ref is answered with what it is — its `details.unresolved` entry carries `declaredAs` (e.g. `"EnumerationDeclaration"`) and `route` instead of suggestions. Read the literals with:

```
mps_mcp_query_structure
  operation = GET_ENUMERATION_LITERALS
  parameters = {"enumerationRef": "<language>.structure.<EnumName>"}
```

`enumerationRef` accepts the declaration's node reference or exactly this qualified name.

## Suggestion heuristic

- **Exact name or alias first.** Concepts whose simple name equals the input's, ignoring case, come first, then concepts whose alias equals it (`Int` finds the concept whose editor shows `Int`). They may be in another language than the one you named (`…lang.smodel.structure.ThisNodeExpression` finds `jetbrains.mps.lang.behavior.structure.ThisNodeExpression`). Name matches come before alias matches, an exact-case match before a different-case one, and then matches in the language you named (or the nearest namespace) before the rest.
- **Then subtoken matches** (the same camelCase- and underscore-aware splitter used by `mps_mcp_search_concepts`). Beside exact matches, a name with all but one of three or more subtokens counts too. If the input is FQN-shaped (e.g. `"jetbrains.mps.lang.smodel.structure.X"`) and the implied language resolves, they are scoped to that language, and one slot is kept for its best match even when exact matches from other languages fill the rest.
- Only when nothing matched so far does the search run project-wide.
- Candidates owned by **another open MPS project** are never suggested; read-only libraries and stubs remain candidates.

Treat the suggestion list as a **candidate set**, not a ranked answer; an exact-name match is almost always the concept you meant. For free-form lookup, use `mps_mcp_search_concepts` (see `search-concepts.md` for the matching algorithm).

## Detail level

- `detail = "shape"` returns only the structural projection of each concept — `{qualifiedName, conceptReference, sourceNode, isAbstract, isRootable, properties: [{name, type, enumerationValues?, enumerationDefault?, featureId, sourceNode}], references: [{name, targetConcept, cardinality, featureId, sourceNode}], children: [{name, targetConcept, cardinality, featureId, sourceNode}]}` — with no docs and no `sampleNode`. It is everything needed to author a blueprint, including the ids blueprints store (`featureId` and `sourceNode` as in the full record); prefer it over reducing the full record yourself. `cardinality` is the same as in the full record, and a reference is always `0..1` or `1`.
- **Do not refine concept by concept.** When a result reveals further concepts you need — typically the `targetConcept` of a role — pass `languageRefs = "<language>"` once (with `detail = "shape"`) instead of one `conceptRefs` call per target.
- `detail = "full"` (default) returns the schema below.

## Result schema

Each entry in the `detail = "full"` result has the shape:

```
{
  name,
  qualifiedName,            // use this as the `concept` field in JSON blueprints
  conceptAlias,
  shortDescription,
  conceptReference,         // c:... — informational; not required in blueprints
  languageReference,
  superConcept,
  superConceptContainingProject,      // only when the direct superconcept is from another open project
  superConceptEditableFromCurrentProject: false,
  superInterfaces: ["ref1", "ref2", ...],
  superInterfaceDetails: [
    { name, reference, containingProject?, editableFromCurrentProject? }
  ],
  sourceNode,
  isAbstract,
  isInterfaceConcept,
  isRootable,
  virtualFolder,
  present: true,
  properties: [...],
  references: [...],
  children: [...],
  sampleNode: {             // a representative node of this concept
    concept,
    properties: [...],
    references: [...],
    children: [...]
  }
}
```

With multiple MPS projects open, `containingProject` / `editableFromCurrentProject:false` marks concepts from another open project. The direct concept entry gets these fields when the concept itself is foreign; nested references use prefixes such as `superConceptContainingProject` and per-entry `superInterfaceDetails[*].containingProject`.

### Feature entries (`properties`, `references`, `children`)

Each item in these three arrays carries the identifiers needed to reference the feature from blueprints — no deep `print_node` calls required to mine them:

```
{
  name,
  type,                     // properties: "string"|"integer"|"boolean"|<enum/datatype name>
  targetConcept,            // references/children only
  cardinality,              // references/children only
  featureId,                // <langUUID>/<conceptId>/<featureId> — the encoded id triple
  sourceNode,               // declaration node's persistent ref, e.g. r:...(...structure)/<id>
  enumerationValues: [...], // properties with an enum type only
  enumerationDefault,       // enum properties with a default member: its name. A property at the default
                            // stores nothing; `mps_mcp_print_node` reports it with `isDefault: true`,
                            // and an absent value means the default, not "missing"
  doc, deprecated           // when present on the declaration
}
```

- **`featureId`** is the encoded id an attribute stores. It is **not** a node reference: as a blueprint reference `target` it becomes a dynamic reference that never resolves, silently — the insert and its dry run succeed; only `fixReferences.stillBroken` and `mps_mcp_check_root_node_problems` show it.
- **`sourceNode`** is the feature declaration's persistent ref, `r:...(...structure)/<id>`. Paste it as the `target` of smodel feature access — `SPropertyAccess.property`, `SLinkAccess.link`, `SLinkListAccess.link` (`moai:mps-model-manipulation`). An inherited feature's `sourceNode` lies in the declaring concept's model (`name` → `jetbrains.mps.lang.core.structure`). It is omitted when the feature has no resolvable declaration (rare).
