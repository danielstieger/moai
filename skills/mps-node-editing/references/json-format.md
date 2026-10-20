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
* **Optional sections**: `properties`, `children`, and `references` can be omitted if empty. A named child role with `"nodes": []` is not the same as an omitted one: it clears what a node factory put there.
* **Reference resolution**: `target` accepts a persistent node reference (`r:...`/`i:...`, resolved directly) or a node **name** for auto-resolution in scope. A plain name is deferred to MPS's scope system after insertion — ideal for local variables, parameters and other non-root declarations within the same blueprint. For roots in another model prefer `"ModelName.RootName"` or a full `r:` ref to avoid ambiguity.
* **References inside one blueprint**: there is no local id, temp id or `"id"` key. To point at a node created in the same blueprint (or the same batch), give its `name` as `target`. The write resolves it in the reference's scope after the nodes exist; check `fixReferences.stillBroken` in the response. An unnamed target, or a name that is ambiguous in scope, needs a second write: insert the target on its own (the response carries its `reference`) or look the ref up with `mps_mcp_print_node`, then set it with `mps_mcp_update_node` `SET` × `REFERENCE`. A response holds only the ref of the write's top node, not of nested nodes.
* **Never a `c:` concept reference as `target`**: it is accepted silently and stays unresolved; only `mps_mcp_check_root_node_problems` reports it. Likewise a `featureId` is not a node reference — use the feature's `sourceNode`.
* **Best practices**: avoid deprecated concepts, properties, or roles.
* **Default property values are invisible**: MPS stores nothing for a property that holds its default value — most visibly the default literal of an enumeration. Dumps omit such a property or print it with `"isDefault": true`; report-style output prints `"value": ""`. Read absent / `""` as "holds its default", and never copy a `""` enum value into a blueprint — omit the property.
* **`declared:false` and `conceptLoaded:false` entries from a printout are not re-applied**: a `declared:false` property is skipped with a warning (on update its stored value stays); a `declared:false` child role or reference is rejected, and so is a node record with `conceptLoaded:false`. Drop the entry (a full-root update then deletes what it held); a root record with `conceptLoaded:false` can only be deleted (`mps_mcp_update_root_node_from_json` operation `DELETE`). In a MoWare project such entries mean a language is not deployed correctly — report it to the user.

## What the node gets besides the blueprint

Every blueprint node gets its behavior constructor and, outside a dry run, its node factories as in the editor (`SKILL.md`, [Node factories](../SKILL.md#node-factories)), then the blueprint's values. Unlike the editor, mandatory child roles the blueprint omits are not auto-filled.

* **An omitted property or role keeps its constructor and factory value.** Leave it out to get what the editor would set; name it (an empty child role included) to replace it.
* **Blueprint values win over the node's own constructor and factories**, but a nested child's factory runs after its parent's values are applied and may still change the parent.
* **Factories see the enclosing nodes**, up through the live node that `mps_mcp_update_node` `ADD`/`SET` × `CHILD` or `mps_mcp_update_root_node_from_json` writes into. A root being inserted is not in the model yet, so factories below it see a root without a model — the same as the editor's New Root.
* **Constraints setters and getters.** `name` and non-enum property values are stored as given, bypassing constraints property setters; enum values go through them. `mps_mcp_print_node` reads properties through constraints getters, so it can show a value that is not stored.

## Response Envelope

All blueprint mutation tools return the standard MCP envelope:

```json
{ "ok": true, "data": { ... } }
```

A real write also reports `fixReferences {fixed, repointed, stillBroken}`; `stillBroken` must be 0. From 10 top-level nodes the default `responseDetail` is `summary` (`{inserted, roots: [{name, reference, concept}], fixReferences}`); `full` can always be forced.

On **dry-run** (`dryRun: true`) the response is:

```json
{
  "ok": true,
  "data": { "dryRun": true, "message": "..." },
  "warnings": [
    "Dry run at $.references[0]: target 'SomeName' is a name, not looked up.",
    "A dry run does not look up reference targets given by name, so every name is listed above, existing and same-batch nodes included. The write resolves names in each role's scope; check fixReferences.stillBroken in its response (or mps_mcp_check_root_node_problems)."
  ]
}
```

A name warning is not a defect: a dry run lists every name target, existing ones included, and it runs no node factories. Do not rewrite names because of it. Fix only a "names no node" or "matches no Model.Root" warning, and check `fixReferences.stillBroken` after the real write. The rule: `moai:mps-mcp-workflow` ([`references/response-envelope.md`](../../mps-mcp-workflow/references/response-envelope.md#dry-run-response)).
