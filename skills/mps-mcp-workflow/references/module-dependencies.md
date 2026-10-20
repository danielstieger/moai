# Module and Model Dependencies

The wiring layer of an application project: module dependencies (in the module descriptor), model imports, used languages and devkits (per model), and creating or renaming modules. Always use the MCP wiring tools; never hand-edit `.mpl` / `.msd` / `.mps` files.

## Rules

- **DevKit first.** Every new MoWare model gets the DevKit `org.modellwerkstatt.MoWareWerkbank` (`moai:mps-node-editing`, Prerequisites); it provides objectflow, manmap, dataux, baseLanguage, closures, collections and javadoc. Do not add these languages one by one.
- **Used languages auto-import.** `mps_mcp_insert_root_node_from_json` and `mps_mcp_update_node` add the language of every concept they insert. A manual `mps_mcp_model_used_language` is needed only for a language no inserted node brings in.
- **Model imports only on demand.** Add a model dependency when a reference is reported out of scope, not up front.
- **Rule of thumb:** a concept used in a model → used language (or devkit) of that model; a node of another model referenced → model import; classes or models of another module used → module dependency.

## Model level

- `mps_mcp_model_dependency` — imports of a model (`targetModels`: one reference or an array). DELETE returns `{removed: true|false}`.
- `mps_mcp_model_used_language` (`kind` = `language` or `devkit`) — accepts a persistent `l:<uuid>:<name>` reference or the bare qualified name.
  - ADD of a language a used devkit already exports is a no-op: `{added: false, providedByDevKit: true, devKit: "<name>"}`. A new language returns `{added: true, providedByDevKit: false}`; for a devkit, `{added, alreadyPresent}`.
  - DELETE returns `{removed: true|false}`. A persistent reference that is not imported answers `removed: false`; a bare name that matches no imported language or devkit is an error, so a typo surfaces.
- Inspect the coverage first: `mps_mcp_get_project_structure(startingPoint=<model>, includeDependencies=true)` lists each model's `usedLanguages`; a devkit entry (`kind: "devkit"`) carries `providedLanguages`, the languages it brings in transitively. A language listed there is already usable.

## Module level

`mps_mcp_module_dependency` adds or deletes a dependency of a module. Scopes: `Default` (the normal case), `Design`, `Compile`, `Runtime`, `Provided`, `Generation Target`; `Extends` does not apply to solutions and is rejected for them.

- ADD is an upsert: a module holds one dependency per source → target pair, so ADD again with another scope overwrites it. `{added: true}` for an insert or an overwrite, `{added: false, reason: "providedByDevKit"}` when a used devkit already provides it.
- Inspect: `mps_mcp_get_project_structure(startingPoint=<module>)` (with `includeDependencies=true` for the dependency lists); it also reports the module's `facets` (e.g. `"tests"`).

## Creating a module — `mps_mcp_create_module`

- `type` = `solution` for application modules. `directory` must be an absolute path that is not an existing file; on Linux a solution folder must lie at least three levels below `/` (`/tmp/x` is rejected, `/work/proj/x` is fine).
- `facets`: an additional facet type or an array, e.g. `"tests"` for the solution that holds a `@tests` model. The `java` facet is created automatically and is skipped when listed. An unknown facet type fails before anything is created.
- `virtualFolder`: optional Project View folder.
- On failure nothing is left behind (the error ends with `No module or file was left behind.`); otherwise it names what to remove with `mps_mcp_update_module` DELETE `deleteFiles=true`.
- Placement and naming of application modules: conventions `anwendungsaufbau`; wiring a new application module: `moai:objectflow-dsl`.

## Renaming a module — `mps_mcp_update_module`

`moduleName` (name or reference) plus `newName` and/or `virtualFolder`. The rename uses the IDE's Rename Module refactoring: it renames the descriptor file, the directory when it matches the module name, models prefixed with the module name, and updates references inside the project. References from outside the open project are not rewritten and are reported in `renameWarnings`; `renameCriticalProblems` must be read before assuming a clean rename. The absence of both means the rename ran cleanly.

## Pitfalls

| Symptom | Cause | Fix |
|---|---|---|
| "Cannot resolve concept X" in a model | The concept's language is not used by the model | Add the DevKit `org.modellwerkstatt.MoWareWerkbank`, or `mps_mcp_model_used_language` ADD for the concept's language |
| Reference reported out of scope | The target's model is not imported | `mps_mcp_model_dependency` ADD of the target model; for another module also `mps_mcp_module_dependency` |
| "Cannot resolve class Y" in code | Missing module dependency | `mps_mcp_module_dependency` ADD with scope `Default` |
| Generated code fails at runtime with `ClassNotFoundException` | A runtime module of a language or a dependency is missing at run time | Check the module dependencies of the running solution; a missing MoWare runtime is an installation problem — report it to the user, do not change the language |
| DevKit changes not picked up | The model uses an older devkit snapshot | Re-add the devkit, then MAKE the module |
