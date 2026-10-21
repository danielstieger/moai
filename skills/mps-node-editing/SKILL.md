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
- **Set references by name.** Give the target's name; the write resolves it in the role's scope, also for nodes created in the same blueprint. Use a persistent ref (`r:…`) only for JDK/library stubs, overloaded methods, a target in another model whose name is ambiguous, and long property chains over entities of other models. After the write, `fixReferences.stillBroken` must be 0; otherwise run `mps_mcp_alter_nodes FIX_REFERENCES`, then apply the problems' `quickFixes` (`autoApplyQuickFixes=true`, e.g. "Resolve method call"). Harvest refs with `mps_mcp_print_node` only if that still fails.
- **Replace referenced members through their body.** `SET CHILD` gives the new node a new ID and breaks every persistent ref to the old one. Replace constructors and test methods only through their `body`; replace methods that call each other together, so their by-name refs resolve again.
- **Cloning an existing node? Use `mps_mcp_alter_nodes` `COPY_NODE`, not a JSON blueprint.** It clones the subtree natively within the same model — a root as a new root, a node in a `0..n`/`1..n` role as the next sibling (a single-child role is an error) — then tweak the copy with `mps_mcp_update_node`. Reserve blueprints for nodes with no close match to copy from; nodes of shipped example modules cannot be copied this way.
- **Filling a typed slot?** Ask `mps_mcp_query_nodes` `GET_EXPECTED_TYPE` on the node you are about to replace and confirm a candidate with `mps_mcp_query_types` `IS_SUBTYPE` — `moai:mps-mcp-workflow` (`references/type-queries.md`).
- **A blueprint is not the whole node** — outside a dry run the concept's node factory runs and may add properties, children and references your JSON never mentions. See [Node factories](#node-factories).
- **Validate frequently** — call `mps_mcp_check_root_node_problems` immediately after inserting or modifying a complex node; after work on several roots, once on the model reference with `perRoot=true`. `"ok": true` from insert does not mean the AST is semantically valid; read `warnings` and `details.uncheckedSubtrees` as well.

## `mps_mcp_update_node` — Unified Node-Mutation Tool

All child, property, and reference operations on existing nodes go through `mps_mcp_update_node`. The operation is selected via `operation` (`ADD`/`SET`) × `kind` (`CHILD`/`PROPERTY`/`REFERENCE`). **There is no `DELETE` operation** — deletion is a `SET`:

- **Delete a child:** `SET` × `CHILD` with `childNodeRef` and **no `childJson`** (omit the parameter or send an unquoted JSON `null`; the string `"null"` is rejected).
- **Clear a property or reference:** an unquoted `null` as the **third element** of the triplet, e.g. `[nodeRef, "name", null]`. A shortened two-element row is rejected (`Invalid property triplet: expected at least 3 elements`), not read as a delete.
- **Delete a root:** `mps_mcp_update_root_node_from_json` with `operation: "DELETE"` and the root's `nodeReference` (no blueprint).

| operation × kind        | Required parameters                                           | Notes |
|-------------------------|---------------------------------------------------------------|-------|
| `ADD` × `CHILD`         | `nodeReference` (parent), `childRole`, `childJson`            | Optional `position` (0-based; null/-1 = append) and `dryRun`. A `position` ≥ the current child count clamps to an append; a negative value other than -1 is rejected. The response's `data.index` reports the actual landing index. |
| `SET` × `CHILD`         | `childNodeRef` (+ `childJson` to replace)                     | Replaces an existing child; preserves its position in the role. Without `childJson` it **deletes** the child. Optional `dryRun`. The success envelope is the **parent's** (`data.reference` is the parent) for both replacement and deletion; the replaced child's reference is stale — find the new child with `mps_mcp_print_node` on the parent. |
| `SET` × `PROPERTY`      | `properties` = `[[nodeRef, propertyName, value], …]`          | Batch operation; returns per-row results. `value = null` **deletes** the property. |
| `SET` × `REFERENCE`     | `references` = `[[nodeRef, role, targetRefOrName], …]`        | Batch operation; `targetRefOrName` accepts an `r:...` ref or a plain name. A plain name is resolved within the reference role's search scope; if it cannot be resolved the call fails (`NOT_FOUND`), preserves the previous reference value, and stores no dangling reference. |

`ADD` × `PROPERTY` and `ADD` × `REFERENCE` are not valid combinations and return an error envelope; so does any other `operation` value, `DELETE` included.

`mps_mcp_update_node` (PROPERTY / REFERENCE / CHILD) and `mps_mcp_alter_nodes` MOVE_CHILD / MOVE_NODE_TO_PARENT / COPY_NODE also work on nodes inside the **current MPS Console input command** — pass the node's normal persistent reference; no extra parameter is needed. The node must be inside the current unexecuted console input (not history/stale). MOVE_NODE_TO_PARENT only relocates a node *within* the current console command — moving a node between the console and a project model, or making a console node a root, is refused. Edits to console nodes skip disk-persistence and refresh the console's imports instead. Nodes outside the selected project are rejected.

`MOVE_NODE_TO_PARENT` has two forms: a non-null `newParentRef` plus `role` reparents the node; omitting `newParentRef` and supplying `modelReference` promotes it to a root. An explicit `"newParentRef": null` is rejected.

## Prerequisites

- Load the `moai:mps-language-analysis` skill if you do not yet know what concepts the model uses.
- Resolve the target node (unless creating a brand-new root):
    - `mps_mcp_get_current_editor_root_node` for the user's focus.
    - `mps_mcp_search_root_node_by_name` for a known name.
- Resolve required languages and concepts:
    - Check used languages of the current model via `mps_mcp_get_project_structure`.
    - **DevKit rule for MoWare models:** every new model gets the DevKit `org.modellwerkstatt.MoWareWerkbank` right after `mps_mcp_create_model`: `mps_mcp_model_used_language(modelReference, kind="devkit", usedLanguage="org.modellwerkstatt.MoWareWerkbank")`. It provides objectflow, manmap, dataux, baseLanguage, closures, collections and javadoc; do not add these languages individually. Inserting a node whose language is missing adds that language automatically (verified), even when the DevKit already provides it — harmless, but a model without the DevKit is incomplete.
    - Get concept details using `mps_mcp_get_concept_details` for specific languages.
    - Use `mps_mcp_search_concepts` for discovery.

## Common Workflow

1. **Identify** the target node (existing) or parent model (new root).
2. **Choose the right tool**: `mps_mcp_create_root_node` / `mps_mcp_insert_root_node_from_json` for new roots; `mps_mcp_update_node` (`ADD`/`SET` × `CHILD`/`PROPERTY`/`REFERENCE`) for surgical edits; `mps_mcp_update_root_node_from_json` only for full-root rewrites.
3. **Author the JSON** following the unified blueprint format.
4. **Insert.** A `dryRun: true` call checks concepts, roles, properties and assignability; it runs no node factories and never looks up a reference target given by name — it warns "is a name, not looked up" for every one, existing names included. Do not rewrite names or dry-run again because of those warnings; fix only "names no node" and "matches no Model.Root" warnings. After the real write, `fixReferences.stillBroken` must be 0. Full rule: `moai:mps-mcp-workflow` ([`references/response-envelope.md`](../mps-mcp-workflow/references/response-envelope.md#dry-run-response)).
5. **Check the result** with `mps_mcp_print_node` when the concepts have node factories (what the factory added is not in your blueprint), then **validate** with `mps_mcp_check_root_node_problems` — the root, or the model reference with `perRoot=true` after several roots. Read `warnings` and `details.uncheckedSubtrees` as well as `data`; apply a problem's `quickFixes` with `mps_mcp_apply_intention` or `autoApplyQuickFixes=true`.
6. **Repair** broken refs with `mps_mcp_alter_nodes FIX_REFERENCES` if `stillBroken` or validation shows resolvable-but-unresolved targets.

## Related Skills

- **`moai:mps-baselanguage`** — when the nodes you edit are BaseLanguage / Java.
- **`moai:mps-language-analysis`** — exploring an unfamiliar language before editing.
- **`moai:mps-model-manipulation`** — when the edit also requires navigating the tree from model code (`.ancestor<C>`, `.descendants<C>`, siblings, containingRoot).

## JSON Input — File-Path Semantics

The tools that accept a node JSON blueprint (`mps_mcp_update_node` for `ADD`/`SET` × `CHILD`, `mps_mcp_insert_root_node_from_json`, `mps_mcp_update_root_node_from_json`, `mps_mcp_insert_console_command_from_json`) take the blueprint in `childJson` / `json`:

- The parameter is **either** the JSON itself (max 4 KB; real JSON or that JSON written as a string) **or** an absolute file path.
- **Every blueprint tool accepts only a file inside the JVM system temp directory** — `$TMPDIR` on Linux (`/tmp` when `TMPDIR` is unset), `%TEMP%` on Windows. A leading `$TMPDIR`, `${TMPDIR}` or `%TEMP%` in the path is expanded by the server. Any other path is rejected (`Input file path '...' is not inside the system temp directory`), so bundled blueprint files (`references/blueprints/*.json` of the DSL skills) are copied first or passed inline: `d="${TMPDIR:-/tmp}/moai-blueprints"; mkdir -p "$d"; cp <blueprint>.json "$d/"`.
- `mps_mcp_insert_root_node_from_json` and `mps_mcp_update_root_node_from_json` also accept a **top-level array** (bulk, atomic); `mps_mcp_update_node` `childJson` takes a single object only.
- Files may contain either a **raw node blueprint** or the **full MCP response envelope** produced by `mps_mcp_print_node`; in the latter case the `data` field is used.
- **Ordinary input files are never deleted.** Only temporary JSON files created by this toolset may be cleaned up after reading (and only when `dryRun=false`).
- Very large JSON inputs may be truncated by the MCP transport before the tool reads them. If that happens, insert a smaller blueprint first and add children in follow-up calls with `mps_mcp_update_node` (`ADD`/`CHILD` or `SET`/`CHILD`), or pass the JSON as a file path instead of an inline string. See `references/staged-construction.md` for the recommended pattern.

## Node factories

Many concepts ship a **node factory** that initializes a freshly created node; the MoWare languages use them widely (an Entity gets its key property, a DataUX form its label option, a SQL block its mapping closure). Outside a dry run, the blueprint tools run the factory for every node they **create** — each new root and every nested child of `mps_mcp_insert_root_node_from_json`, the new child of `mps_mcp_update_node` `ADD`/`SET` × `CHILD`, the staged children (not the existing root) of `mps_mcp_update_root_node_from_json`. Factories see the enclosing nodes. `COPY_NODE` and deletions run none.

- **A factory fills only the roles the blueprint omits.** A property you set wins over the factory's value. A child or reference role you **name** replaces the factory's content — even an empty one, `{"role": "options", "nodes": []}`, which is the way to suppress unwanted factory children.
- **Name a role only to override it.** Listing a role you meant to leave alone discards the factory's contribution; omitting a role keeps it.
- **Mandatory roles are not auto-filled.** A role neither the factory nor the blueprint fills stays empty, and `mps_mcp_check_root_node_problems` reports it.
- **A dry run runs no factories**, so it validates the blueprint, not the final node. Check the written node with `mps_mcp_print_node` and validate it; the per-DSL factory effects are in each DSL skill's `gotchas.md` ("Node factories").
- **Factory side effects survive a failed batch.** A failed call removes only the nodes it created, not what factories wrote elsewhere (used languages, model imports). Re-read the affected state instead of assuming a failed call changed nothing.
- **A factory that throws is reported as a `warnings` entry**, and the node is still created without its factory state; one that catches its own exception reports nothing — check the IDE log (`moai:mps-mcp-workflow`, `references/ide-log.md`) when expected factory content is missing.
- **Factories may add model imports without the module dependency.** After an insert that pulled in a model of another module (e.g. a runtime model), check the module's dependencies (`mps_mcp_get_project_structure`, `includeDependencies=true`) and add the missing one with `mps_mcp_module_dependency`.

Whether a concept has a factory: `mps_mcp_query_structure` `LIST_CONCEPT_ASPECTS` lists the `actions` aspect for it (read `relation`: only `appliesTo` roots act on the concept).

## Reference Index

- Open `references/json-format.md` when you need the unified JSON blueprint shape — concept/properties/children/references layout, optional-section rules, and reference-resolution semantics (`r:...` vs name auto-resolution).
- Open `references/staged-construction.md` when the subtree exceeds the inline limit or its child refs are needed for later edits — the skeleton → validate → incremental-fill → targeted-update → cleanup pattern.
- Open `references/troubleshooting.md` when an insert call fails (missing fields, unknown roles, temp-directory rejection, assignability errors, `featureId` as target, object vs. array) or a dry run lists name warnings.
