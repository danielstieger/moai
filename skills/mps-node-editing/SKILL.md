---
name: mps-node-editing
description: Add, update, or delete MPS nodes using JSON blueprints — covers the unified blueprint format, staged construction for large subtrees, validation, and reference repair. Use whenever creating, editing, or restructuring nodes in any MPS model (application code, console commands, etc.).
---

# MPS Node Editing

The core workflow for mutating MPS nodes through MCP tools. JSON blueprints describe the node hierarchy you want; the tools resolve concepts, references, and used languages on insert.

## Critical Directives

- **Always use the fully qualified concept name** (`qualifiedName`) in `concept` — rule: `moai:mps-mcp-workflow` (`references/node-editing-rules.md`).
- **Resolve before editing** — call `mps_mcp_get_current_editor_root_node` (for the user's focus) or `mps_mcp_search_root_node_by_name` (by name) to lock onto the target. Don't guess refs.
- **Prefer surgical edits** — `mps_mcp_update_node` (`ADD`/`CHILD` or `SET`/`CHILD`) preserves persistent IDs. `mps_mcp_update_root_node_from_json` rewrites the entire root and is wasteful when only one subtree changed.
- **Don't delete-and-reinsert** to make a small change — deletion destroys persistent IDs and breaks incoming references.
- **Validate frequently** — call `mps_mcp_check_root_node_problems` immediately after inserting or modifying a complex node. `"ok": true` from insert does not mean the AST is semantically valid.

## `mps_mcp_update_node` — Unified Node-Mutation Tool

All child, property, and reference operations on existing nodes go through `mps_mcp_update_node`. The operation is selected via `operation` (`ADD`/`SET`) × `kind` (`CHILD`/`PROPERTY`/`REFERENCE`). There is no `DELETE` operation — deletion is `SET` with a `null` value.

| operation × kind        | Required parameters                                           | Notes |
|-------------------------|---------------------------------------------------------------|-------|
| `ADD` × `CHILD`         | `nodeReference` (parent), `childRole`, `childJson`            | Optional `position` (0-based; null/-1 = append) and `dryRun`. A `position` ≥ the current child count clamps to an append; a negative value other than -1 is rejected. The response's `data.index` reports the actual landing index. |
| `SET` × `CHILD`         | `childNodeRef`, `childJson`                                   | Replaces an existing child; preserves its position in the role. `childJson = null` **deletes** the child (returns the parent's envelope). Optional `dryRun`. |
| `SET` × `PROPERTY`      | `properties` = `[[nodeRef, propertyName, value], …]`          | Batch operation; returns per-row results. `value = null` **deletes** the property. |
| `SET` × `REFERENCE`     | `references` = `[[nodeRef, role, targetRefOrName], …]`        | Batch operation; `targetRefOrName` accepts an `r:...` ref or a plain name. A plain name is resolved within the reference role's search scope; if it cannot be resolved the call fails (`NOT_FOUND`), preserves the previous reference value, and stores no dangling reference. |

`ADD` × `PROPERTY` and `ADD` × `REFERENCE` are not valid combinations and return an error envelope.

`mps_mcp_update_node` (PROPERTY / REFERENCE / CHILD) and `mps_mcp_alter_nodes` MOVE_CHILD / MOVE_NODE_TO_PARENT also work on nodes inside the **current MPS Console input command** — pass the node's normal persistent reference; no extra parameter is needed. The node must be inside the current unexecuted console input (not history/stale). MOVE_NODE_TO_PARENT only relocates a node *within* the current console command — moving a node between the console and a project model, or making a console node a root, is refused. Edits to console nodes skip disk-persistence and refresh the console's imports instead. Nodes outside the selected project are rejected as before.

## Prerequisites

- Load the `moai:mps-language-analysis` skill if you do not yet know what concepts the model uses.
- Resolve the target node (unless creating a brand-new root):
    - `mps_mcp_get_current_editor_root_node` for the user's focus.
    - `mps_mcp_search_root_node_by_name` for a known name.
- Resolve required languages and concepts:
    - Check used languages of the current model via `mps_mcp_get_project_structure`.
    - **DevKit rule for MoWare models:** every new model gets the DevKit `org.modellwerkstatt.MoWareWerkbank` right after `mps_mcp_create_model`: `mps_mcp_model_used_language(modelReference, kind="devkit", usedLanguage="org.modellwerkstatt.MoWareWerkbank")`. It provides objectflow, manmap, dataux, baseLanguage, closures, collections and javadoc; do not add these languages individually. Inserting a node whose language is missing adds that language automatically (verified), but a model without the DevKit is incomplete.
    - Get concept details using `mps_mcp_get_concept_details` for specific languages.
    - Use `mps_mcp_search_concepts` for discovery.

## Common Workflow

1. **Identify** the target node (existing) or parent model (new root).
2. **Choose the right tool**: `mps_mcp_create_root_node` / `mps_mcp_insert_root_node_from_json` for new roots; `mps_mcp_update_node` (`ADD`/`SET` × `CHILD`/`PROPERTY`/`REFERENCE`) for surgical edits; `mps_mcp_update_root_node_from_json` only for full-root rewrites.
3. **Author the JSON** following the unified blueprint format.
4. **Insert** with `dryRun: true` first for large blueprints and read `warnings` (`references/json-format.md`).
5. **Validate** with `mps_mcp_check_root_node_problems`.
6. **Repair** broken refs with `mps_mcp_alter_nodes FIX_REFERENCES` if validation surfaces resolvable-but-unresolved targets.

## Related Skills

- **`moai:mps-baselanguage`** — when the nodes you edit are BaseLanguage / Java.
- **`moai:mps-language-analysis`** — exploring an unfamiliar language before editing.
- **`moai:mps-model-manipulation`** — when the edit also requires navigating the tree from model code (`.ancestor<C>`, `.descendants<C>`, siblings, containingRoot).

## JSON Input — File-Path Semantics

The tools that accept a node JSON blueprint (`mps_mcp_update_node` for `ADD`/`SET` × `CHILD`, `mps_mcp_insert_root_node_from_json`, `mps_mcp_update_root_node_from_json`, `mps_mcp_insert_console_command_from_json`) take the blueprint in `childJson` / `json`:

- The parameter is **either** an inline JSON string (max 4 KB) **or** an absolute file path. `mps_mcp_update_node.childJson` accepts any absolute path; the root/console tools (`insert_root_node_from_json`, `update_root_node_from_json`, `insert_console_command_from_json`) accept only a file **inside the system temp directory**. Bundled blueprint files (`references/blueprints/*.json` of the DSL skills) must therefore be copied to the temp directory, or their content passed inline (≤ 4 KB), before use.
- Files may contain either a **raw node blueprint** or the **full MCP response envelope** produced by `mps_mcp_print_node`; in the latter case the `data` field is used.
- **Ordinary input files are never deleted.** Only temporary JSON files created by this toolset may be cleaned up after reading (and only when `dryRun=false`).
- Very large JSON inputs may be truncated by the MCP transport before the tool reads them. If that happens, insert a smaller blueprint first and add children in follow-up calls with `mps_mcp_update_node` (`ADD`/`CHILD` or `SET`/`CHILD`), or pass the JSON as a file path instead of an inline string. See `references/staged-construction.md` for the recommended pattern.

## Reference Index

- Open `references/json-format.md` when you need the unified JSON blueprint shape — concept/properties/children/references layout, optional-section rules, and reference-resolution semantics (`r:...` vs name auto-resolution).
- Open `references/staged-construction.md` when the subtree exceeds the inline limit or its child refs are needed for later edits — the skeleton → validate → incremental-fill → targeted-update → cleanup pattern.
- Open `references/troubleshooting.md` when an insert call fails with `JsonElement.getAsString()` errors or when the JSON shape diverges from the user's textual notation.
