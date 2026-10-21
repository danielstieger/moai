# Staged Construction for Large Hierarchies

Blueprints above the inline limit (`SKILL.md`, File-Path Semantics) or whose child refs you need later: build in stages. Every blueprint passed as a file must lie in the system temp directory (`${TMPDIR:-/tmp}` on Linux, `%TEMP%` on Windows).

1. **Skeleton first**: insert the parent/root node with properties, references, and a minimal child skeleton (e.g. empty method bodies).
2. **Read child refs**: after inserting the skeleton, `mps_mcp_print_node` (`deep=false`) on the new node gives the persistent refs of its direct children, which the following `ADD`/`SET` × `CHILD` calls address. References between nodes are still set by name (`SKILL.md`, Critical Directives). Repeat on any newly inserted child to drill further down — every staged call returns its own node ref.
3. **Validate early**: run `mps_mcp_check_root_node_problems` on the skeleton to catch structural errors — and `mps_mcp_print_node` to see what node factories added to it (`SKILL.md`, Node factories).
4. **Incremental fill**: use `mps_mcp_update_node` with `ADD`/`CHILD` to add remaining subtrees. `childJson` takes a single object only — add N children with N calls, or nest them under the parent's blueprint.
5. **Targeted updates**: use `mps_mcp_update_node` with `SET`/`CHILD` to rewrite specific subtrees.
6. **Full root updates**: `mps_mcp_update_root_node_from_json` is a full-root rewrite — only the root's persistent ID survives; all properties, references and children are re-set from the blueprint, so omitted elements are removed and every child gets a **new** ID (refs read from the previous skeleton become invalid). An omitted `name` keeps the current name; a different `name` renames the root. Use it only when the whole root changes; otherwise add/replace members with `mps_mcp_update_node` (`ADD`/`SET` × `CHILD`).
7. **Final cleanup**: check `fixReferences.stillBroken` of each write, run `mps_mcp_check_root_node_problems` — after several roots once on the model reference with `perRoot=true` — and use `mps_mcp_alter_nodes` with `FIX_REFERENCES` if needed.

A bulk insert of 10 or more top-level nodes answers with `responseDetail: "summary"` by default (`{inserted, roots: [{name, reference, concept}], fixReferences}`); pass `responseDetail: "full"` only when you need every node envelope.

## Forward references: the dynamic-reference escape hatch

You do **not** always have to insert a reference's target before the node that points at it. When a blueprint `target` is a plain **name** rather than an `r:`/`i:` persistent ref, the blueprint reader stores it as a **dynamic reference** that MPS resolves later by that name. This lets you author one logical unit — e.g. a `Root_MappingRule` together with the template it points at — without strictly ordering the inserts, as long as the name is unambiguous in the resolution scope. (This escape hatch is specific to the blueprint readers — `mps_mcp_insert_root_node_from_json`, `mps_mcp_update_node ADD`/`SET CHILD`, `mps_mcp_update_root_node_from_json`. `mps_mcp_update_node SET REFERENCE` differs: it resolves a plain name in the role's scope immediately and fails with `NOT_FOUND` if it cannot, rather than leaving a dynamic ref.)

- A dry-run (`dryRun: true`) lists every name target as "is a name, not looked up", existing and same-batch names included. These are the refs the write leaves dynamic until its fix-references pass. An empty list does not prove the references will resolve; `fixReferences.stillBroken` after the write does (`json-format.md`, Response Envelope).
- Once the target exists, run `mps_mcp_alter_nodes FIX_REFERENCES` to materialize the dynamic refs into persistent (`r:...`) references.
- Strict ordering (insert the target first) is only required when the name **can't** resolve on its own — duplicate names in scope, or a target identified only by node id.
- Inside one bulk insert (top-level array in `mps_mcp_insert_root_node_from_json`), a plain name in `target` also resolves to a node created in the same call. If auto-resolution is not possible, leave the reference out and set it afterwards with `mps_mcp_update_node` (`SET` × `REFERENCE`) once the target's ref is known.
