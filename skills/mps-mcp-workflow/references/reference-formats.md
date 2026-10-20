# Reference Formats and Resolution

- Persistent references in MPS follow specific formats:
    - **Node References** (`reference`, `targetReference`, `target`): `r:<modelUUID>(<modelName>)/<nodeId>`, e.g. `r:00000000-0000-4000-0000-011c89590301(jetbrains.mps.lang.smodel.structure)/1138055754698`. Stub (JDK/library) nodes use a stub model id such as `…/java:javax.swing(JDK/)/~JButton` (`moai:mps-baselanguage`, `references/stub-references.md`).
    - **Concept References** (`conceptReference`): `c:<langUUID>/<conceptId>:<FQN>` for concepts, `i:<langUUID>/<conceptId>:<FQN>` for interface concepts — `i:` is **not** a stub marker.
    - **Model References**: `r:<modelUUID>(<modelName>)` — a node reference without the `/<nodeId>` part. Tools that accept a model reference also accept the model's **qualified name** (stereotype included, e.g. `foo.bar@tests`).
    - **Language References**: `l:<langUUID>:<name>`; `languageRefs` and `mps_mcp_model_used_language` also accept the bare language name.
- **CRITICAL**: never use a concept reference (`c:...`) where a node reference (`r:...`) is expected. If you need a reference to point to the **declaration node** of a concept (its definition), you must use its node reference.
- To obtain the node reference (`r:...`) for a concept:
    - Use `mps_mcp_get_concept_details` and check the **`sourceNode`** field in the response.
    - Alternatively, use `mps_mcp_search_concepts` with `detail: "full"` and check the `sourceNode` field for each match — the default `"summary"` record does not carry it.
- The blueprint readers (`mps_mcp_insert_root_node_from_json`, `mps_mcp_update_root_node_from_json`, `mps_mcp_update_node` `ADD`/`SET` × `CHILD`) do **not** reject a `c:...` string in a reference role — it silently yields an unresolved reference that only `mps_mcp_check_root_node_problems` reliably reports. A plain name becomes a dynamic reference that the write resolves in the role's scope; an unresolvable one shows up in `fixReferences.stillBroken` of the write's response ([`response-envelope.md`](response-envelope.md#dry-run-response)). Only `mps_mcp_update_node` `SET` × `REFERENCE` fails with `NOT_FOUND`. Forward-reference strategy: `moai:mps-node-editing`, `references/staged-construction.md`.

## Which tools accept a MODEL reference

A model reference is **not** interchangeable with a node reference; each tool takes one or the other:

| Tool | node/root reference | model reference |
|---|---|---|
| `mps_mcp_check_root_node_problems` | yes | **yes** — also a qualified model name, or a module reference/name; pass it in `nodeReference` (there is no `modelReference` parameter). Checks every root of the model in one exhaustive call (`perRoot=true` for one row per root; `autoApplyQuickFixes` is ignored in this mode) |
| `mps_mcp_print_node` | yes | **no** — rejected with INVALID_REQUEST naming the model and a retry line for `mps_mcp_get_project_structure` (`startingPoint`, `includeNodes=true`) |
| `mps_mcp_update_node`, `mps_mcp_open_node`, `mps_mcp_list_node_intentions`, `mps_mcp_apply_intention` | yes | no |
| `mps_mcp_insert_root_node_from_json`, `mps_mcp_create_root_node` | — | yes, as the *target model* parameter |
| `mps_mcp_query_nodes` (`models` scope), `mps_mcp_alter_nodes` (`MAKE` `{"models": […]}`), `mps_mcp_model_dependency`, `mps_mcp_model_used_language`, `mps_mcp_update_model` | — | yes, in the documented model/`models` parameter |

A model reference where a node reference is expected is rejected with INVALID_REQUEST naming the model and the tool to retry with — do not treat it as "the node is gone".

## Request conventions

- **List parameters.** `conceptRefs` / `languageRefs` (`mps_mcp_get_concept_details`), `searchTexts` (`mps_mcp_search_concepts`), `names` / `models` / `modules` (`mps_mcp_search_root_node_by_name`), `targetModels` (`mps_mcp_model_dependency`), `facets` (`mps_mcp_create_module`) and the `json` blueprint of `mps_mcp_insert_root_node_from_json` / `mps_mcp_update_root_node_from_json` take one value or a list. A real JSON array (`["A","B"]`) and the array written as a string (`"[\"A\",\"B\"]"`) are equivalent; a lone `r:…` / `c:…` is always one value. Arrays inside a `parameters` blob are plain JSON.
- **Two spellings inside a `parameters` blob.** Blob keys accept a short and a long form — `conceptRef`/`conceptReference`, `enumerationRef`/`enumerationReference`, `nodeReference`/`nodeRef`, `childNodeRef`/`childNodeReference`, `newParentRef`/`newParentReference`, `modelReference`/`modelRef`, `typeNodeReference`/`typeNodeRef`, `typeConceptRef`/`typeConceptReference`. Sending **both** spellings of one key is rejected with INVALID_REQUEST naming which to keep.
- **Unknown blob keys are rejected, not dropped.** A key the operation does not accept is answered with INVALID_REQUEST naming it, the closest accepted spelling and the accepted set. Every missing required key is reported at once (`details.missingParameters`). `projectPath` is tolerated inside the blob, but must still be passed top-level.
- **Top-level parameters have no aliases.** Only the spelling in the tool's schema is accepted; the schema's `required` array is empty, a required parameter says "Required." in its description. A wrong top-level key is ignored and the default applies; a required one left blank is rejected with the literal retry line.
- **Booleans and integers in a blob are type-checked.** `true`/`false` (also quoted, any case), a number or a quoted number; `null` counts as absent. `1` for a boolean, `1.5`, whitespace, objects or arrays are rejected with a message naming the key.
- **`dryRun`** is accepted only where it is honoured (`mps_mcp_update_node`, the blueprint tools); elsewhere it is rejected rather than ignored.

The response envelope and the "Dry-run response" rule: [`response-envelope.md`](response-envelope.md).

## Node Info Envelope

Tools that return a node (e.g. `mps_mcp_get_current_editor_root_node`, `mps_mcp_create_root_node`, `mps_mcp_search_root_node_by_name`, the success path of node-mutation tools) return a common JSON envelope. Standard fields:

- `name` — node name (when the concept implements `INamedConcept`).
- `concept` — short concept name (e.g. `Entity`); the fully qualified name is the suffix of `conceptReference` after the `:` (also returned as `qualifiedName` by `mps_mcp_get_concept_details` / `mps_mcp_search_concepts`) — use the FQN as `concept` in JSON blueprints.
- `conceptReference` — persistent concept reference (`c:...`); informational.
- `reference` — persistent node reference (`r:...`).
- `parentReference` — persistent reference to the parent node (`""` for roots).
- `rootReference` — persistent reference to the containing root node.
- `modelReference` — persistent reference to the containing model.
- `moduleReference` — persistent reference to the containing module.
- `virtualFolder` — Project View virtual folder, when set.
- `isRoot` — true for root nodes.
- `present` — `true` for a successful envelope.

Tool-specific additions:

- `mps_mcp_get_current_editor_root_node` (`source='editor'`) additionally carries the caret and selection: `caret` (the cursor's cell: its node `nodeReference`, the contextual node, and `feature` — the property/reference/child it edits, with `navigational` for a navigation-only reference), `selection` (`present`, `kind` `"nodes"`/`"text"`, `nodes`, `nodeCount`, `nodesTruncated`, …), `selectedNodeReference` (present for an ordinary caret too) and `bigCellSelected` (a genuine whole-node selection). Interpretation: [`finding-things.md`](finding-things.md#reading-the-users-current-focus-caret--selection).
- `mps_mcp_update_node` `ADD` × `CHILD` carries `parentReference` of the freshly inserted child. `SET` × `CHILD` returns the parent's envelope (`data.reference` is the parent) for both replacement and deletion.
