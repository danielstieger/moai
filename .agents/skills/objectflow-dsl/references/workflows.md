# ObjectFlow editing workflows

## Create an Entity, DTO, or ValueObject

1. Identify the target model through `mps_mcp_get_project_structure` and confirm it uses ObjectFlow. Resolve the exact `projectPath` with `mps_mcp_list_open_projects`.
2. Query the intended root concept with `mps_mcp_get_concept_details`. Start with [entity-skeleton.json](blueprints/entity-skeleton.json) for an Entity; choose the analogous root concept for a DTO or ValueObject.
3. Change `name` and `nestedName` together; optionally set `virtualPackage`. Dry-run the root JSON, then insert it with `mps_mcp_insert_root_node_from_json`.
4. Add one `BusinessProperty` at a time under `businessProperties`, using [business-property-int-subtree.json](blueprints/business-property-int-subtree.json) as the typed integer example. Select a different BaseLanguage `Type` concept for non-integer data; do not copy a ManMap key option unless the property is a key.
5. Build constructors and methods with `mps-baselanguage`, adding them to the inherited `member` role. Validate the root after meaningful subtrees are present.

## Create or change a Command

Use [command-skeleton.json](blueprints/command-skeleton.json) to establish the root, then insert `parameter`, `variable`, and `pages` subtrees as needed. A `PageCrtl` needs a `pageInit` child and at least one `pagePaneActionProviderLink` child, so inspect an existing page and its current descriptor before copying it. Command expressions and statement lists use BaseLanguage; load `mps-baselanguage` for them. When a page or action points to a DataUX UI root, resolve that target in the active MPS project.

## Edit an existing root

Resolve the root by current editor focus or `mps_mcp_search_root_node_by_name`, print it shallowly, and inspect only the affected subtree deeply. Use `mps_mcp_update_node` for property, reference, or child edits so persistent IDs remain stable. Re-query concept details if role cardinality or available child concepts are unclear. Run `mps_mcp_check_root_node_problems` after the edit; make/generate when the task requires runtime output.

Blueprints here document MPS AST shapes. Keep examples small: roots with large methods or pages should be built as a skeleton followed by focused child-role insertions.
