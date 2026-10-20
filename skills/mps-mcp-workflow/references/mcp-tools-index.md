# Available MPS MCP Tools

## Project and Structure

Every call takes the top-level `projectPath` ([`../SKILL.md`](../SKILL.md#which-project-the-tools-act-on)). Read tools return `data` inline up to `maxInlineBytes` (default 20000), a temp-file path above it.

- `mps_mcp_list_open_projects`: lists open IDE projects, marks those with an MPS project, and returns the `mpsProjectBaseDirectory` to pass as `projectPath`. Top-level `mpsVersion`/`mpsBuild`/`mpsEap` are the running IDE's identity; `logDirectory`/`logFile` locate the IDE log.
- `mps_mcp_read_ide_log`: read-only tail of the IDE log as records (`ts`, `level`, `message`, `stackTrace`), filtered by `sinceMinutes`/`since`, `minLevel`, `grep`; follows rotation ([`ide-log.md`](ide-log.md)).
- `mps_mcp_close_project`: closes the project selected by `projectPath` (`force`, `shutdownWithLastProject`; `MODAL_BLOCKED` after 20 s). No tool opens a project ([`project-management.md`](project-management.md)).
- `mps_mcp_get_project_structure`: the universal tool to explore the project. Use `startingPoint` and filtering to avoid large responses; pass `includeStubModules=true` to include read-only libraries/stubs and modules from other open MPS projects. `nodeDetail="names"` reduces node records to name/concept/reference, `nodeDepth` bounds how far `includeNodes` inlines.
- `mps_mcp_reload_all`: reloads module classes from disk; compiles nothing.
- `mps_mcp_initialize_project_for_agents`: **never call it in a MoWare project** — it installs JetBrains' generic `mps-*` skills and a `CLAUDE.md` into the project, competing with the `moai:` skills.

## Modules and Models

- `mps_mcp_create_module`, `mps_mcp_update_module` (operations: RENAME, CHANGE_VIRTUAL_FOLDER, DELETE)
- `mps_mcp_create_model`, `mps_mcp_update_model` (operations: RENAME, DELETE). In a MoWare project follow a create with the DevKit `org.modellwerkstatt.MoWareWerkbank` (see `moai:mps-node-editing`). Model names are plain names or `name@stereotype` (e.g. `@tests` for MPS test-case models, which also need the `tests` facet on the hosting solution; see `finding-things.md` for addressing stereotyped models by name).
- `mps_mcp_module_dependency`, `mps_mcp_model_dependency`, `mps_mcp_model_used_language` ([`module-dependencies.md`](module-dependencies.md)). Explicit target references may point to another open MPS project; the selected project records the dependency/import, but the foreign target stays read-only.
- `mps_mcp_list_facet_types`, `mps_mcp_get_module_facets`, `mps_mcp_update_module_facet`: inspect and modify module facets (e.g. attach the `tests` facet to a Solution that hosts a `@tests` model). Facet read responses include a `module` context object, with `containingProject` / `editableFromCurrentProject:false` when the inspected module is from another open MPS project. `mps_mcp_create_module` accepts one initial facet type or a JSON-array string in `facets` for `solution`/`language` modules.

## Root Nodes and Nodes

- `mps_mcp_open_node`: opens a node in the editor; non-root references open the containing root and select the target.
- `mps_mcp_get_current_editor_root_node`: identifies the node the user is currently looking at.
- `mps_mcp_create_root_node`, `mps_mcp_update_root_node_from_json` (full-root rewrite; `operation: "DELETE"` with the root's `nodeReference` deletes a root)
- `mps_mcp_query_nodes`: read-only node queries — FIND_INSTANCES (find nodes of a concept; `sampleOnly` for one example), FIND_USAGES (nodes referencing a given node), GET_PARENT, GET_ROOT, GET_MODEL_FOR_NODE, NODE_INDEX, SIBLINGS, GET_CHILD_ROLE, GET_TYPE / GET_EXPECTED_TYPE (a node's own / required type; `null` if none). FIND_INSTANCES takes `conceptRefs` for several concepts, `detail:"count"`, `rootsOnly`. Default scopes are selected-project based; explicit model/module/root scopes may target another open project read-only; explicit scopes must resolve completely or the query is rejected.
- `mps_mcp_query_types`: the typesystem engine answers type queries — IS_SUBTYPE, SUPERTYPES, COMMON_SUPERTYPE, COERCE, OPERATION_TYPE, EXPLAIN_TYPE ([`type-queries.md`](type-queries.md)).
- `mps_mcp_alter_nodes`: structural node mutations and code generation — MOVE_CHILD, MOVE_NODE_TO_PARENT, COPY_NODE (deep copy: a root becomes a new root of the same model, a node in a `0..n`/`1..n` role the next sibling; a single-child role is an error), MAKE, FIX_REFERENCES.
- `mps_mcp_print_node`: shows the underlying JSON structure or the projection of a node. `format` = `JSON` (default), `HTML`, `PLAIN TEXT` (with a space); `nodeReference` must be a node reference.
- `mps_mcp_insert_root_node_from_json`: creates one or more roots from a blueprint (top-level array = atomic batch, rolled back as a whole on any failure). `responseDetail` = `summary` (default from 10 top-level nodes: `{inserted, roots: [{name, reference, concept}], fixReferences}`) or `full`. Forward references and staged construction: `moai:mps-node-editing` (`references/staged-construction.md`).
- `mps_mcp_update_node`: unified node-mutation tool for child, property, and reference roles (`ADD`/`SET` × `CHILD`/`PROPERTY`/`REFERENCE`). **There is no `DELETE` operation** — delete a child with `SET` × `CHILD` without `childJson`, clear a property or reference with an explicit `null` as the triplet's third element. The node being mutated must belong to the selected project; reference targets may point to another open project if the target is in scope/imported. Operation table: `moai:mps-node-editing`.
- `mps_mcp_check_root_node_problems`: validation tool. Accepts a node/root, a model (reference or qualified name) or a module in `nodeReference`; the model form checks every root in one exhaustive call, `perRoot=true` gives one row per root. Problems may carry `quickFixes` (`autoApplyQuickFixes=true` for node/root references) and `rules`; `details.uncheckedSubtrees` counts skipped (commented-out) subtrees ([`analysis-tools.md`](analysis-tools.md)).
- `mps_mcp_list_node_intentions`, `mps_mcp_apply_intention`: the headless Alt+Enter menu — list and apply intentions and quick-fixes of a node.
- `mps_mcp_search_root_node_by_name`: finds root nodes by name (`names` = single name or JSON array; `scope` `editable`/`all`/`models`/`modules`); returns node-info envelopes.
- `mps_mcp_parse_java_and_insert`: parses Java with the MPS `JavaParser` and inserts the result as root(s), as a child in a role, as a replacement of a node, or into the current Console input (`insert.mode: "console"`); no `dryRun`; success envelopes carry a `problems` array. See `moai:mps-baselanguage`.

## Console

- `mps_mcp_insert_console_command_from_json`: inserts a console `Command` node or one or more BaseLanguage statements into the current MPS Console input without executing it.
- `mps_mcp_get_current_editor_root_node` with `source="console"`: returns the current unexecuted command in the MPS Console input editor.
- `mps_mcp_get_console_history`: lists executed console commands, optionally interleaved with response/output entries.
- `mps_mcp_recall_console_command`: copies a command from console history back into the input editor without executing it.
- `mps_mcp_run_console_command`: runs the command currently in the Console input editor; it can have side effects and returns only that execution was triggered, so read results from console history or the Console UI.

## Language Definition

- `mps_mcp_get_concept_details`: provides properties, children, and references for one concept/language or a JSON array in `conceptRefs` / `languageRefs`; `detail="shape"` returns only the structural projection. A `descriptorStatus: "hollow"` entry is untrustworthy — see `moai:mps-language-analysis` (`references/concept-details.md`).
- `mps_mcp_search_concepts`: search for concepts by name, alias or description (`searchTexts`: one string or an array). Default `scope="project"` with automatic widening, `detail="summary"` (no `sourceNode`), at most 50 strict matches (`moai:mps-language-analysis`, [`search-concepts.md`](../../mps-language-analysis/references/search-concepts.md)).
- `mps_mcp_query_structure`: read-only structure queries — `GET_SUB_CONCEPTS`, `GET_ASSIGNABLE_CONCEPTS`, `GET_ALL_SUPERCONCEPTS`, `IS_SUBCONCEPT_OF`, `GET_ENUMERATION_LITERALS`, `LIST_CONCEPT_ASPECTS`, `GET_ASSIGNABLE_REFERENCES`, `IS_SMART_REFERENCE`.
- `mps_mcp_alter_structure`, `mps_mcp_scaffold_editor`: write tools for language structure and concept editors — not used in MoWare application projects (language definitions are off-limits, see `MPS_AGENT_GUIDE.md`).

## Run Configurations

- `mps_mcp_create_run_configuration`: creates/registers a run configuration for a root (`IMainClass`/class with `main` → Java Application, requires `compileInMPS=true`; `ITestCase` → JUnit Tests); same name replaces the existing config. See `moai:mps-run-configurations`.
