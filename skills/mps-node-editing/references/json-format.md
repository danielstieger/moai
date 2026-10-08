# Unified JSON Format

MPS tools use a single JSON blueprint shape for all insertions and updates:

```json
{
  "concept": "fully.qualified.ConceptName",
  "properties": [
    { "name": "propertyName", "value": "propertyValue" }
  ],
  "children": [
    {
      "role": "childRoleName",
      "nodes": [
        { "concept": "fully.qualified.ChildConcept", "properties": [...] }
      ]
    }
  ],
  "references": [
    {
      "role": "referenceRoleName",
      "target": "targetNodeNameOrRef"
    }
  ]
}
```

* **Concept**: `qualifiedName` (`moai:mps-mcp-workflow`, `references/node-editing-rules.md`).
* **Optional sections**: `properties`, `children`, and `references` can be omitted if empty.
* **Reference resolution**: `target` accepts a persistent node reference (`r:...`/`i:...`, resolved directly) or a node **name** for auto-resolution in scope. A plain name is deferred to MPS's scope system after insertion — ideal for local variables, parameters and other non-root declarations within the same blueprint. For roots in another model prefer `"ModelName.RootName"` or a full `r:` ref to avoid ambiguity.
* **Best practices**: avoid deprecated concepts, properties, or roles.

## Response Envelope

All blueprint mutation tools return the standard MCP envelope:

```json
{ "ok": true, "data": { ... } }
```

On **dry-run** (`dryRun: true`) the `data` payload is:

```json
{ "dryRun": true, "message": "Dry run successful for ..." }
```

A `"warnings"` array may appear at the top level alongside `data` when the staging phase found something to surface. Producers are the dry-runs of the blueprint readers — `mps_mcp_update_node` (`ADD`/`SET` × `CHILD`), `mps_mcp_insert_root_node_from_json`, `mps_mcp_update_root_node_from_json`: a warning is added when a reference target did not resolve during staging and the production write *would* create a dynamic (unresolved) reference. The dry-run itself succeeds.

```json
{
  "ok": true,
  "data": { "dryRun": true, "message": "..." },
  "warnings": ["Dry run at $.references[0]: target 'SomeName' did not resolve; production run would create a dynamic reference, but dry-run skips this step."]
}
```

Always inspect `warnings` after a dry-run — empty = staging clean; non-empty = the production write creates dynamic references for the listed targets. Either fix those targets before writing, or accept that the write will create dynamic (potentially broken) references (forward-reference strategy: `staged-construction.md`). Full envelope shape: `moai:mps-mcp-workflow` (`references/reference-formats.md`).
