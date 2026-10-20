---
name: mps-dsl-memory
description: Package-maintainer-only tool for explicitly requested creation or refresh of bundled MPS DSL skills. Do not invoke implicitly, during consumer-project work, or merely because a skill appears missing or outdated.
---

### Maintainer Boundary
Use this skill only when the MoAI package maintainer explicitly requests maintenance of the bundled DSL skills. Do not infer permission from newly discovered DSL facts, missing or stale skill content, or a request to work on an MPS model. Package users and agents working in consumer projects must not modify the bundled skill catalog.

### When to Use
* The package maintainer explicitly asks to create or refresh a bundled DSL skill.
* The requested maintenance target and scope are named clearly.

### Prerequisites
* MPS MCP tools are available.
* The project has one or more language modules and at least one sandbox, example solution, or editable model that exercises the DSLs.
* Use MPS MCP tools for discovery and model edits. Do not hand-edit serialized `.mps` XML.
* A fixed maintenance project is open with an editable solution that uses the DevKit `org.modellwerkstatt.MoWareWerkbank`. Step 8 dry-runs and inserts into models of that solution: a dry-run into a bundled MoWare model is rejected, because its module is not part of the project.
* Pass `projectPath` in every call (rule: `moai:mps-mcp-workflow` SKILL.md, "Which project the tools act on").

### Workflow
1. **Discover languages**: Call `mps_mcp_get_project_structure` with `includeModels: false`. Identify all editable DSL language modules and derive each concept-tools language ref as `l:<uuid>:<languageName>`.
2. **Choose skill scope**: Prefer one generated skill per language. Use one combined skill only when the project languages are tightly coupled and users normally edit them together.
3. **Find examples**: For each language or language group, call `mps_mcp_get_project_structure` with the relevant sandbox/example solution as `startingPoint` and `includeRootNodes: true`. Record editable model refs and representative root refs.
4. **Read concepts**: Call `mps_mcp_get_concept_details` with the relevant `l:<uuid>:<languageName>` refs. Capture rootable concepts, concrete children, properties, child roles, references, and useful `shortDescription` text.
5. **Sample sparingly**: Use `mps_mcp_print_node` only on representative roots or subtrees needed for reference targets, required roles, or reusable blueprints, and derive blueprints from that output rather than writing them by hand. Avoid dumping every root.
6. **Generate DSL skills**: Create or update `skills/<dsl-name>-dsl/` for each selected scope. Preserve user-added notes unless they are stale or wrong. In every generated file, write the temp directory as `$TMPDIR` (`%TEMP%` on Windows), never as the resolved directory (`/private/var/folders/…/T`, `C:\Users\…\Temp`), which differs per machine.
7. **Cross-link related skills**: When generated skills cover languages that extend, depend on, or are commonly used inside each other, add short links and usage notes between them.
8. **Verify**: Confirm linked reference files exist, no `.DS_Store` or editor artifacts were added, and one or two recorded node refs still resolve if the sandbox may have changed. A blueprint counts as valid only once the server accepts it; parsing as JSON is not enough, because the server rejects blueprints that parse.
    * **Dry-run every blueprint** under `references/blueprints/`, with its placeholders replaced: `mps_mcp_insert_root_node_from_json` with `dryRun: true` into a model of the maintenance project for a root blueprint, `mps_mcp_update_node` ADD CHILD with `dryRun: true` under a sample parent for a fragment. The server reads a `json` / `childJson` file only from the system temp directory, so a path under `skills/` is rejected with "is not inside the system temp directory"; that rejection is not a blueprint failure. Send each file's exact content inline (up to 4,096 characters), or copy the files first and pass each copy's absolute path: `d="${TMPDIR:-/tmp}/<dsl-name>-blueprints"; mkdir -p "$d"; cp skills/<dsl-name>-dsl/references/blueprints/*.json "$d/"`. When a dry run fails, fix the shipped file, not only the inline text or the temp copy, and dry-run again from the fixed file.
    * If every blueprint is rejected with `Unknown property …`, the language descriptor is hollow. The MoWare languages ship prebuilt, so do not MAKE them: stop and report a broken installation or build to the user. Warnings for references given by name (`is a name, not looked up`) are expected; see "Dry-run response" in `moai:mps-mcp-workflow` `references/response-envelope.md`.
    * **Insert for real.** The dry run checks concepts, roles, and assignability only; it does not resolve names and does not run node factories. Create a throwaway model in the maintenance solution (`mps_mcp_create_model`, DevKit `org.modellwerkstatt.MoWareWerkbank`), import the models whose roots the blueprints reference, insert each root blueprint there, and add each fragment under a sample parent in it. For every insert, `fixReferences.stillBroken` must be 0; compare `mps_mcp_print_node` (`deep: true`) with the blueprint for children and values the factory added or replaced (for example `isNamed`, labels, default members). Once all inserts are in, run `mps_mcp_check_root_node_problems` on the model reference with `perRoot: true`. Record each deviation under "Node factories" in the generated `gotchas.md`, and fix the blueprint where a named role (empty `{"role":"…","nodes":[]}` included) suppresses unwanted factory content. Finally delete the throwaway model (`mps_mcp_update_model` with `operation: "DELETE"`).

### Generated Skill Layout
```text
skills/<dsl-name>-dsl/
|-- SKILL.md
`-- references/
    |-- concepts.md
    |-- sandbox.md
    |-- workflows.md
    |-- gotchas.md
    `-- blueprints/
        |-- <operation>-skeleton.json
        `-- <operation>-subtree.json
```

The `<dsl-name>` slug is derived from the language namespace: use stable lowercase, split camel case and separators into words, and prefer the namespace's final meaningful segment unless the project consistently names the DSL differently. The `-dsl` suffix is mandatory — callers (such as `mps-mcp-workflow`) discover generated skills with the glob `skills/*-dsl/`.

### Generated `SKILL.md` Requirements
* Frontmatter:
    * `name: <dsl-name>-dsl`
    * `description:` Use when creating, editing, validating, or inspecting this DSL's models.
* Short domain summary: two to four sentences. For combined skills, name each covered language and when to use the combined workflow.
* Critical rules:
    * Use MPS MCP tools; do not hand-edit `.mps` XML.
    * Use `mps_mcp_get_concept_details` with `l:<uuid>:<languageName>`, not `<uuid>(<languageName>)`.
    * Prefer skeleton-plus-subtree insertion for large or uncertain roots.
    * Validate with `mps_mcp_check_root_node_problems`: the single changed root, or, after work on several roots, the model reference with `perRoot: true`.
    * Pass `projectPath` in every call; link the rule in `moai:mps-mcp-workflow` SKILL.md, "Which project the tools act on".
* Quick start:
    * Use the recorded sandbox model for examples or new sample roots.
    * Start from `references/blueprints/` for known shapes: replace the placeholders, then search the blueprint text for `TARGET_`; any hit means stop.
    * Send the blueprint's content inline (up to 4 KB), or copy the file to `${TMPDIR:-/tmp}` (`%TEMP%` on Windows) and pass the copy's absolute path. The server does not read a file under `skills/`.
    * Dry-run root JSON with `mps_mcp_insert_root_node_from_json`; it checks concepts, roles, and assignability, not names, and does not run node factories.
    * Insert roots with `mps_mcp_insert_root_node_from_json`; `fixReferences.stillBroken` must be 0.
    * Add child-role subtrees incrementally for large roots.
    * Run `mps_mcp_print_node` for blueprints with node-factory effects, then `mps_mcp_check_root_node_problems` and any task-required build/generation checks.
* Node factories: name the concepts whose factories add or replace content on insert, and point to the "Node factories" section of `references/gotchas.md`.
* Project references:
    * Concept-tools language ref for each covered language.
    * Sandbox/example model refs.
    * Primary editable modules.
    * Dependencies or extension relationships between covered project languages, if relevant.
* Related DSL skills:
    * Link sibling generated skills when another project language supplies child concepts, expressions, commands, reference targets, or extensions used by this language.
    * Explain when to load each related skill.
* Reference directory links.

### Reference Files
* `references/concepts.md`: concept hierarchy, rootable concepts, properties, child roles, references, and semantic notes.
* `references/sandbox.md`: sandbox model refs, representative roots, configuration nodes, reference targets, and stable node refs.
* `references/workflows.md`: creation/editing recipes, including when to use full-root JSON versus skeleton-plus-subtrees.
* `references/gotchas.md`: reference formats, ordering constraints, required roles, expression precedence issues, extension-language dependencies, and known validation failures. A "## Node factories" section records, per concept, what its factory adds or replaces on insert, as found in step 8, and which named role suppresses it.
* `references/blueprints/`: valid compact JSON skeletons and subtree templates, in the array form `print_node` emits (`properties:[{name,value}]`, not a map).
