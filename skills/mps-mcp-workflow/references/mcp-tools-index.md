# Available MPS MCP Tools

## Project and Structure

- `mps_mcp_list_open_projects`: lists open IDE projects, marks which have MPS project counterparts, and returns the `mpsProjectBaseDirectory` to use as the host `projectPath` selector when several MPS projects are open.
- `mps_mcp_get_project_structure`: the universal tool to explore the project. Use `startingPoint` and filtering to avoid large responses; pass `includeStubModules=true` to include read-only libraries/stubs and modules from other open MPS projects.
- `mps_mcp_reload_all`: reloads all modules in the MPS project to refresh runtime classes and concept registries.
- `mps_mcp_initialize_project_for_agents`: **never call it in a MoWare project** — it installs JetBrains' generic `mps-*` skills and a `CLAUDE.md` into the project, competing with the `moai:` skills.

## Modules and Models

- `mps_mcp_create_module`, `mps_mcp_update_module` (operations: RENAME, CHANGE_VIRTUAL_FOLDER, DELETE)
- `mps_mcp_create_model`, `mps_mcp_update_model` (operations: RENAME, DELETE). In a MoWare project follow a create with the DevKit `org.modellwerkstatt.MoWareWerkbank` (see `moai:mps-node-editing`). Model names are plain names or `name@stereotype` (e.g. `@tests` for MPS test-case models, which also need the `tests` facet on the hosting solution; see `finding-things.md` for addressing stereotyped models by name).
- `mps_mcp_module_dependency`, `mps_mcp_model_dependency`, `mps_mcp_model_used_language`. Explicit target references may point to another open MPS project; the selected project records the dependency/import, but the foreign target stays read-only.
- `mps_mcp_list_facet_types`, `mps_mcp_get_module_facets`, `mps_mcp_update_module_facet`: inspect and modify module facets (e.g. attach the `tests` facet to a Solution that hosts a `@tests` model). Facet read responses include a `module` context object, with `containingProject` / `editableFromCurrentProject:false` when the inspected module is from another open MPS project. `mps_mcp_create_module` accepts one initial facet type or a JSON-array string in `facets` for `solution`/`language` modules.

## Root Nodes and Nodes

- `mps_mcp_open_node`: opens a node in the editor; non-root references open the containing root and select the target.
- `mps_mcp_get_current_editor_root_node`: identifies the node the user is currently looking at.
- `mps_mcp_create_root_node`, `mps_mcp_update_root_node_from_json`
- `mps_mcp_query_nodes`: read-only node queries — FIND_INSTANCES (find nodes of a concept; `sampleOnly` for one example), FIND_USAGES (nodes referencing a given node), GET_PARENT, GET_ROOT, GET_MODEL_FOR_NODE, NODE_INDEX, SIBLINGS, GET_CHILD_ROLE. Default scopes are selected-project based; explicit model/module/root scopes may target another open project read-only.
- `mps_mcp_alter_nodes`: structural node mutations and code generation — MOVE_CHILD, MOVE_NODE_TO_PARENT, MAKE, FIX_REFERENCES.
- `mps_mcp_print_node`: shows the underlying JSON structure or it shows the "visual" projection of a node.
- `mps_mcp_insert_root_node_from_json`: creates one or more roots from a blueprint (top-level array = atomic batch). Forward references: `moai:mps-node-editing`, `references/staged-construction.md`.
- `mps_mcp_update_node`: unified node-mutation tool for child, property, and reference roles (`ADD`/`SET` × `CHILD`/`PROPERTY`/`REFERENCE`; deletion = `SET` with `null`). The node being mutated must belong to the selected project; reference targets may point to another open project if the target is in scope/imported. Operation table: `moai:mps-node-editing`.
- `mps_mcp_check_root_node_problems`: validation tool. Use this frequently to ensure your changes are correct.
- `mps_mcp_search_root_node_by_name`: finds root nodes by name (`names` = single name or JSON array; `scope` `editable`/`all`/`models`/`modules`); returns node-info envelopes.
- `mps_mcp_parse_java_and_insert`: parses Java with the MPS `JavaParser` and inserts the result as root(s), as a child in a role, as a replacement of a node, or into the current Console input (`insert.mode: "console"`); no `dryRun`; success envelopes carry a `problems` array. See `moai:mps-baselanguage`.

## Console

- `mps_mcp_insert_console_command_from_json`: inserts a console `Command` node or one or more BaseLanguage statements into the current MPS Console input without executing it.
- `mps_mcp_get_current_editor_root_node` with `source="console"`: returns the current unexecuted command in the MPS Console input editor.
- `mps_mcp_get_console_history`: lists executed console commands, optionally interleaved with response/output entries.
- `mps_mcp_recall_console_command`: copies a command from console history back into the input editor without executing it.
- `mps_mcp_run_console_command`: runs the command currently in the Console input editor; it can have side effects and returns only that execution was triggered, so read results from console history or the Console UI.

## Language Definition

- `mps_mcp_get_concept_details`: provides properties, children, and references for one concept/language or a JSON-array string in `conceptRefs` / `languageRefs`. A `descriptorStatus: "hollow"` entry is untrustworthy — see `moai:mps-language-analysis` (`references/concept-details.md`).
- `mps_mcp_search_concepts`: global search for concepts by name, alias or description using a single search string or a JSON array of search strings.
- `mps_mcp_query_structure`: read-only structure queries — `GET_SUB_CONCEPTS`, `GET_ASSIGNABLE_CONCEPTS`, `GET_ALL_SUPERCONCEPTS`, `IS_SUBCONCEPT_OF`, `GET_ENUMERATION_LITERALS`, `LIST_CONCEPT_ASPECTS`, `GET_ASSIGNABLE_REFERENCES`, `IS_SMART_REFERENCE`.
- `mps_mcp_alter_structure`, `mps_mcp_scaffold_editor`: write tools for language structure and concept editors — not used in MoWare application projects (language definitions are off-limits, see `MPS_AGENT_GUIDE.md`).

## Run Configurations

- `mps_mcp_create_run_configuration`: creates/registers a run configuration for a root (`IMainClass`/class with `main` → Java Application, requires `compileInMPS=true`; `ITestCase` → JUnit Tests); same name replaces the existing config. See `moai:mps-run-configurations`.
