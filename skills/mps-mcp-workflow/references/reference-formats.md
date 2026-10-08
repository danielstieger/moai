# Reference Formats and Resolution

- Persistent references in MPS follow specific formats:
    - **Node References** (`reference`, `targetReference`, `target`): `r:<modelUUID>(<modelName>)/<nodeId>`, e.g. `r:00000000-0000-4000-0000-011c89590301(jetbrains.mps.lang.smodel.structure)/1138055754698`. Stub (JDK/library) nodes use a stub model id such as `…/java:javax.swing(JDK/)/~JButton` (`moai:mps-baselanguage`, `references/stub-references.md`).
    - **Concept References** (`conceptReference`): `c:<langUUID>/<conceptId>:<FQN>` for concepts, `i:<langUUID>/<conceptId>:<FQN>` for interface concepts — `i:` is **not** a stub marker.
- **CRITICAL**: never use a concept reference (`c:...`) where a node reference (`r:...`) is expected. If you need a reference to point to the **declaration node** of a concept (its definition), you must use its node reference.
- To obtain the node reference (`r:...`) for a concept:
    - Use `mps_mcp_get_concept_details` and check the **`sourceNode`** field in the response.
    - Alternatively, use `mps_mcp_search_concepts` and check the `sourceNode` field for each match.
- The blueprint readers (`mps_mcp_insert_root_node_from_json`, `mps_mcp_update_root_node_from_json`, `mps_mcp_update_node` `ADD`/`SET` × `CHILD`) do **not** reject a `c:...` string in a reference role — it silently yields an unresolved reference; an unresolvable plain name becomes a dynamic reference. Both surface only via `dryRun` warnings or `mps_mcp_check_root_node_problems`. Only `mps_mcp_update_node` `SET` × `REFERENCE` fails with `NOT_FOUND`. Forward-reference strategy: `moai:mps-node-editing`, `references/staged-construction.md`.

## MCP Response Envelope

Every MPS MCP tool returns a JSON envelope at the top level:

```
{
  "ok": true | false,
  "data": <payload>,         // present on ok:true; type depends on the tool
  "warnings": ["..."],       // optional; present only when non-empty
  "details": { ... },        // optional; present only when non-empty
  "error": "...",            // present on ok:false
  "code": "ERROR_CODE"       // present on ok:false when a structured error code is available
}
```

**`warnings`** appear in the envelope on a **successful response** (`ok:true`) when the tool completed but found something worth surfacing without treating it as an error. Current producers:

- **`mps_mcp_get_concept_details` partial success**: one warning per unresolved ref, alongside `details.unresolved` with suggestions.
- **Dry-run of node blueprints**: unresolved targets are reported as `warnings` — semantics: `moai:mps-node-editing` (`references/json-format.md`, Response Envelope).

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

- `mps_mcp_get_current_editor_root_node` additionally carries `selectedNodeReference` when an editor selection is active.
- `mps_mcp_update_node` carries `parentReference` of the freshly inserted child.
