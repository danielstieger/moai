# Bulk Node Creation and Staged Construction

## Bulk Insert (Top-Level Array)

- To insert multiple root nodes in one call, pass a **top-level JSON array** to `mps_mcp_insert_root_node_from_json`. All nodes are inserted atomically — if any node fails, the entire batch is rolled back.
- Use `r:` refs for existing targets; for targets created in the same batch or later, see the forward-reference strategy in `moai:mps-node-editing` (`references/staged-construction.md`).

## Print-Shallow-Then-Add-Children Workflow

Prefer **staged construction** over one giant blueprint when a subtree is large or its child node refs are needed for later edits. Single JSON blueprints over ~4 KB get truncated, and very deep trees are hard to debug.

The pattern is:

1. Insert (or create) the **outer node** with a minimal blueprint — concept, properties, and just enough children/references to make the node valid.
2. Call `mps_mcp_print_node` with `deep=false` (shallow) on the outer node to learn the **persistent refs** of its direct children and roles.
3. Fill or extend each child role with `mps_mcp_update_node`: `ADD`/`CHILD` (append a new child in a role) or `SET`/`CHILD` (swap an existing placeholder child for a real subtree).
4. Repeat the print-shallow step on any newly inserted child to drill further down — every staged call returns its own node ref.

Use this pattern whenever you would otherwise paste a node ref you have not yet seen, when the subtree might exceed the JSON size limit, or when intermediate validation (`mps_mcp_check_root_node_problems`) between layers helps localise errors.
