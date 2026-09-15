# ObjectFlow gotchas

- The skill resides in `moai_ware`, while its examples currently come from the separately opened `eFWWS` MPS project. Always pass the **open MPS project directory** as `projectPath` for MCP calls. Never pass the skill repository path to a model mutation tool unless that directory is itself an open MPS project.
- `mps_mcp_get_concept_details` expects `l:ec097fca-5b84-41f2-847d-6a5690cae277:org.modellwerkstatt.objectflow`; the module reference with parentheses is a different format.
- A `BusinessProperty` needs both `type` and `propertyImplementation` (cardinality `1`). The inspected default implementation also has required `defaultGetAccessor` and `defaultSetAccessor` children. A name-only property skeleton is incomplete.
- `PageCrtl` requires `pageInit` and at least one `pagePaneActionProviderLink`. A name-only page skeleton is incomplete even if the parent `Command.pages` role is optional.
- `Entity`, `DTO`, `ValueObject`, and `Service` extend BaseLanguage `ClassConcept`. Their methods and constructors are BaseLanguage members; use the BaseLanguage skill and exact concepts for these subtrees.
- ManMap `KeyOption` can appear under `BusinessProperty.propertyOption`. This does not make every business property a persistence key. Consult the ManMap skill before editing persistence-related options.
- Avoid deprecated features. One inspected Command uses `overWriteWindowTitle`, which current concept details mark deprecated; use current `newWindowTitleType` after checking its enum values in the target model.
- Use `r:...` node refs for reference targets. A `c:...` concept ref may silently become an unresolved reference in an insertion; validation catches this after writing.
- MCP JSON dry-run checks parseability and concept-role assignability, not complete semantic validity. Run `mps_mcp_check_root_node_problems` after a real edit.
