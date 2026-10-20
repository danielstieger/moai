# Finding Models, Modules, Languages, and Nodes

## Finding Nodes

- To find nodes that are instances of a concept — e.g. an example node to study or copy as a JSON template — use `mps_mcp_query_nodes` (`FIND_INSTANCES`) with `conceptRef`. `rootsOnly: true` matches only root nodes; `sampleOnly: true` returns one random example; `scope: "roots"` searches within given roots; `propertyFilter: {"name", "value"}` matches a property value (e.g. find a literal by its value).
- To ask about **several** concepts, or about *how many* instead of *which*, stay in one call: `conceptRefs` takes an array and `detail: "count"` returns `[{concept, conceptReference, count}]` — never one FIND_INSTANCES call per concept (row semantics: [`analysis-tools.md`](analysis-tools.md)).
- To find the nodes that reference a given node, use `FIND_USAGES` (`nodeReference`). Usages are incoming references — FIND_USAGES does **not** return instances of a concept.
- To find root nodes by name, use `mps_mcp_search_root_node_by_name`. Aspect roots like `<Concept>_Editor` have no name property and are not findable this way — use `mps_mcp_query_structure` (`LIST_CONCEPT_ASPECTS`) on the concept instead.
- Explicit `models`, `modules` and `roots` scopes are all-or-error: pass one nonblank reference or a nonempty array, and every reference must resolve — otherwise the call returns INVALID_REQUEST and never searches only the resolvable subset. `mps_mcp_search_root_node_by_name` takes `models`/`modules` as a bare reference or a JSON array (real or as a string).

## Finding Concepts

- To find a concept by name, alias, or short description, use `mps_mcp_search_concepts` (`searchTexts`; optionally scope to a model's languages via `modelReference`). It searches the languages this project owns or uses by default (`scope: "project"`) and widens to the whole registry automatically when they hold no strict match (a `warnings` entry says so); `scope` cannot be combined with `modelReference`. The default `detail: "summary"` record carries no `sourceNode` — pass `detail: "full"` for it; feature lists and `featureId`s come from `mps_mcp_get_concept_details`. At most 50 strict matches come back (`details.totalStrictMatches` when more matched): narrow the query rather than paging.
- There is no "list all concepts" operation: `mps_mcp_query_structure` has no such op. Use `mps_mcp_search_concepts`, or `GET_SUB_CONCEPTS` / `GET_ASSIGNABLE_CONCEPTS` to enumerate the sub/assignable concepts of a given concept.

## Finding Models, Modules, and Languages

- A fully qualified name or a unique persistent reference is needed to unambiguously represent an entity.
- With multiple MPS projects open, same-name lookup prefers the project selected by `projectPath`, then falls back to the shared repository. Use persistent references when you intentionally need a model, module, language, concept, or node from another open project.
- Elements from another open project are read-only from the selected project. Returned JSON marks them with `containingProject: { name, mpsProjectBaseDirectory }` and `editableFromCurrentProject: false`; nested fields use prefixes such as `conceptContainingProject`, `targetContainingProject`, or `typeContainingProject`.
- **Model names include their stereotype.** The `name` a tool reports for a model is its full name with any stereotype attached (e.g. `foo.bar@tests`, `foo.bar@generator`), matching the `@stereotype` form `mps_mcp_create_model` expects. The stereotype is part of the model's identity — when you address a model by name, pass it verbatim (`foo.bar@tests`, not `foo.bar`). Two models can share a long name and differ only by stereotype.
- If given an incomplete or shortened name (e.g. `j.m.l.core`), use `mps_mcp_get_project_structure` with eager filtering to find the full name.
- Single-letter packages usually expand: `j` → `jetbrains`, `m` → `mps`, `l` → `lang`.
- Newly created languages might not be discoverable by specialized language tools until they are compiled. Use `mps_mcp_get_project_structure` to find them as modules and investigate their `structure` model.
- Use `mps_mcp_get_project_structure` to read the organization of an MPS project and to understand the dependencies of a module or dependencies and used languages of a model.
- Use `includeStubModules=true` when you need read-only libraries/stubs or modules from other open MPS projects in project-structure output.
- `mps_mcp_get_project_structure(startingPoint=<module>)` returns `facets` (e.g. `["java","tests"]`) and `loadExtensions` for each module — use these to check whether a solution is a test container (`"tests"` in `facets`) or whether a module loads plugin extensions.
- **Ask for the smallest projection that answers the question.** To list a model's roots and their ids, use `includeRootNodes=true, nodeDetail="names"`; to look inside one root, bound `includeNodes` with `nodeDepth` or use `mps_mcp_print_node(deep=true)` on that root. For orientation (which modules and models exist, how many roots each has) pass `includeModels=true` only; `includeDependencies` adds every dependency and used-language list — pass it only when the question is about dependencies.
- When not explicitly pointing to a node, assume the user is referring to the root node currently open in the editor and possibly also a selected node within that root node. Use `mps_mcp_get_current_editor_root_node`.
- WHEN asked for the 'current model' or 'current module/solution/language/generator', it is the model/module of the root node currently open in the editor — use `mps_mcp_get_current_editor_root_node`.

## Reading the User's Current Focus (caret & selection)

`mps_mcp_get_current_editor_root_node(source="editor")` returns the root node plus the editor's caret and selection (fields: [`reference-formats.md`](reference-formats.md#node-info-envelope)):

- **"These nodes":** if `selection.present` and `selection.kind == "nodes"`, use `selection.nodes` (`{reference, concept, name}`); `nodeCount` is the true total, and `nodesTruncated: true` means the array is capped.
- **"This node":** without a node selection, use the `caret`: `caret.nodeReference` is the node the cursor sits in, `caret.contextualNodeReference` the node whose projection built the cell (they differ inside a reference cell), `caret.feature` the property/reference/child the cursor edits.
- **`selectedNodeReference`** is present for an ordinary caret too; only `bigCellSelected == true` means a whole-node selection.
- A `feature` with `navigational == true` is a reference the cell only navigates to; an edited reference cell has `referenceCell == true`.

## Packaged modules outside the project

Packaged solutions and language modules that are not part of the open project (for example the shipped example solution `org.modellwerkstatt.dataux.tests`, or generator models of a packaged language) need explicit references:

| Tool | Behavior for packaged modules | What works |
| --- | --- | --- |
| `mps_mcp_get_project_structure` with `startingPoint` | `NOT_FOUND` | Add `includeStubModules: true` |
| `mps_mcp_search_root_node_by_name`, `mps_mcp_query_nodes` `FIND_INSTANCES` with `scope: "all"` | Does not include them; `all` means the project's visible dependency closure | `scope: "modules"` or `"models"` with explicit references |
| `mps_mcp_query_nodes` `FIND_USAGES` | Finds nothing inside packaged language modules | `FIND_INSTANCES` of the referencing concept in explicit models, then filter |
| `mps_mcp_print_node` | Works with explicit node references | – |
