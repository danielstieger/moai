---
name: mps-mcp-workflow
description: Complete JetBrains MPS workflow guide for MoWare application projects — modules, models, node JSON blueprints, validation, type queries, IDE log, MPS MCP tool usage, and the index of companion skills. Use whenever working in an MPS project, when `MPS_AGENT_GUIDE.md` says to load it, or when you need to pick the right companion skill.
---

# Projectional Agent Toolkit – JetBrains MPS for Agents

Hub skill for working with JetBrains MPS (Meta Programming System) models and the MPS MCP tools. Load it after `AGENTS.md` and `MPS_AGENT_GUIDE.md` whenever the task involves MPS artifacts or MPS MCP tooling.

## Critical Directives

- **Never read or edit raw `.mps` / `.mpl` XML; use `mps_mcp_*` tools.** Rule and fallback: [`MPS_AGENT_GUIDE.md`](../../MPS_AGENT_GUIDE.md#never-read-raw-mps-model-files).
- **Pass `projectPath` on every `mps_mcp_*` call**, starting with the first one — rule below in [Which project the tools act on](#which-project-the-tools-act-on).
- **Load each tool's schema before its first call** (`ToolSearch select:` when the host defers schemas). The keys are not guessable: `nodeReference`, `conceptRefs`/`languageRefs`, `searchTexts`, `parameters.code` / `insert.modelRef`.
- **Editing rules** (preserve node IDs, surgical `mps_mcp_update_node` over full-root rewrites, validate after every change): `moai:mps-node-editing`.
- **Copy-then-modify beats reconstruct-from-JSON.** To create a node that closely resembles an existing one in the same model, duplicate it with `mps_mcp_alter_nodes` `COPY_NODE` (a root becomes a new root of the same model, a node in a `0..n`/`1..n` role the next sibling) and adjust the copy with `mps_mcp_update_node`. Shipped example modules are not part of the project and cannot be copied from this way.
- **Ask the typesystem, do not simulate it.** Whether a type fits, what a slot requires, what an operator returns (BaseLanguage, collections, DSL expressions): call `mps_mcp_query_types` or `mps_mcp_query_nodes` `GET_TYPE` / `GET_EXPECTED_TYPE` — [`references/type-queries.md`](references/type-queries.md).
- **Validate frequently.** A successful insertion (`"ok": true`) does not mean the AST is semantically valid — follow with `mps_mcp_check_root_node_problems`: on the changed root, or after work on several roots once on the model reference with `perRoot=true`. Read `warnings` and `details.uncheckedSubtrees`, not just the `data` verdict (commented-out code is not type- or constraints-checked); a problem's `rules[0].rule` names the reporting rule, `quickFixes` can be applied with `mps_mcp_apply_intention` — [`references/analysis-tools.md`](references/analysis-tools.md).
- **Check the IDE log when the envelope and the effect disagree.** When a tool reports success but the effect is missing, call `mps_mcp_read_ide_log` with `sinceMinutes` covering the call window and `minLevel="WARN"` — [`references/ide-log.md`](references/ide-log.md).
- **Language definitions are off-limits.** In a MoWare application project never edit language structure or aspects (`mps_mcp_alter_structure`, `mps_mcp_scaffold_editor`, aspect models of the MoWare languages) — see `MPS_AGENT_GUIDE.md`.

> **Tool name note**: MPS MCP tools are named with a `mps_mcp_` prefix (e.g. `mps_mcp_query_nodes`, `mps_mcp_alter_nodes`, `mps_mcp_get_concept_details`). Your MCP client wraps these with a server-specific prefix (e.g. `mcp__mps-mcp__`), which varies by environment. Match tools by the stable `mps_mcp_*` suffix.

## Which project the tools act on

- **`projectPath` in every call.** The platform routes each call by resolving `projectPath` to an open project; a call without it is rejected before dispatch (`Unable to determine the target project…`), `mps_mcp_list_open_projects` included. Pass the open MPS project's base directory (`mpsProjectBaseDirectory`) — a path *at or inside* the folder MPS opened, **not** an ancestor such as the repository root.
- **Unknown path:** on the first call pass the session's current working directory. If that is rejected, take the path from the rejection message, which lists the open projects (`Currently open projects: {...}`), and reuse that one path for every later call in the session.
- **Empty project list** (`Currently open projects: {"projects":[]}`): MPS shows the welcome screen, and no retry can succeed. Ask the user to open the project in MPS; opening it from the command line: [`references/project-management.md`](references/project-management.md).
- **Subdirectory & multi-project checkouts.** The MPS project often lives in a **subdirectory** of your repository (e.g. `<repo>/<mps-project-dir>`), and one checkout may even hold **several** MPS projects; `projectPath` always names the folder MPS actually opened.

> **Multi-project repository rules.** All open MPS projects share the same module repository. Write targets — models, modules, root nodes, and nodes being mutated — must belong to the project selected by `projectPath`; tools refuse writes to another open project's elements. Read/reference/dependency targets may come from another open MPS project when they are explicitly named or imported: model/module dependencies, model used languages/devkits, node concepts, and reference targets can point across projects, and the foreign elements are treated like read-only library/stub elements. Returned JSON for an element from another open project includes `containingProject: { name, mpsProjectBaseDirectory }` and `editableFromCurrentProject: false`; nested references use prefixes such as `conceptContainingProject`, `targetContainingProject`, or `typeContainingProject`. These markers appear *only* for elements owned by another open project — their absence does not imply an element is editable (a read-only library/stub in the current project carries `readOnly: true` but no `containingProject`), so decide editability from `readOnly` together with these markers.
>
> **When in doubt, ask which project.** When several MPS projects are open under one repository / VCS root, the `mps_mcp_*` tools accept *any* valid project path and act relative to that project. Same-name resolution prefers the selected project's own elements before falling back to the shared repository, but an explicit reference may still resolve to another open project. If the intended project is not obvious from the user's request or the current editor focus (`mps_mcp_get_current_editor_root_node`), do **not** guess — show the `mps_mcp_list_open_projects` entries and ask the user which project the query or change should run against.

## Companion Skills

All skills bundled with this package are loaded as `moai:<skill-name>`. Load whichever ones apply to the current task.

> **Never call `mps_mcp_initialize_project_for_agents` in a MoWare project.** It installs JetBrains' generic `mps-*` skills into the project's `.claude/skills` (they compete with the `moai:` skills) and creates a `CLAUDE.md`. The `moai` package is the only skill catalog; see `INSTALL_INSTRUCTIONS.md`.

| Skill | What it covers |
|-------|---------------|
| `moai:baselanguage-collections-dsl` | Collections and closures: BaseLanguage collection types, creators, operations, access expressions, foreach statements, closure literals, `yield`, and the downcast expression. |
| `moai:mps-baselanguage` | Author and edit `jetbrains.mps.baseLanguage` nodes using the Java parser or JSON AST blueprints. |
| `moai:mps-console` | Console commands and `smodel.query` scope queries. |
| `moai:mps-language-analysis` | Analyze MPS language definitions, concepts, metadata, aspects, and sample nodes. |
| `moai:mps-model-manipulation` | smodel model code — querying, navigating, creating and mutating nodes (collections and closures: `moai:baselanguage-collections-dsl`). |
| `moai:mps-node-editing` | Add, update, or delete MPS nodes using JSON blueprints. |
| `moai:mps-run-configurations` | Create and execute MPS IDE run configurations for runnable roots and tests. |
| `moai:dataux-dsl` | Create, edit, validate, or inspect MoWare DataUX pages, forms, tables, layouts, bindings, includes, and menus. |
| `moai:manmap-dsl` | Create, edit, validate, or inspect MoWare ManMap persistence descriptions, repositories, queries, and persistence operations. |
| `moai:objectflow-dsl` | Create, edit, validate, or inspect MoWare ObjectFlow domains, services, commands, tests, configuration, permissions, and resources. |

## Key Concepts

MPS is a projectional editor and a language workbench. Unlike text-based IDEs, MPS works with an Abstract Syntax Tree (AST) directly. JSON is used to represent MPS nodes and their properties in a structured format for the MPS tools.

- **Modules**: The top-level containers in an MPS project.
    - **Solution**: contains user code (models).
    - **Language**: defines a new language - structure (concepts and interface concepts), editor, etc.
    - **Generator**: defines how to transform one language to another (usually to Java/BaseLanguage). May belong to a language or be independent.
    - **DevKit**: a bundle of languages and other devkits. DevKits can also export solutions and languages. Importing a DevKit into a module or model automatically makes all its exported languages and solutions available. This is the preferred way to manage common sets of languages and dependencies.
- **Models**: contained within modules. They hold a collection of **Root Nodes**.
- **Nodes**: the basic building blocks of the AST. Nodes are organized hierarchically.
    - **Root Nodes**: the top-level nodes in a model.
- **Concepts**: define the "type" of a node (like a class in OOP). They define properties, children, and references. Concepts are defined in the **structure** aspect of a language. Like in OOP, a concept can extend another concept and implement multiple interface concepts, which leads to subconcept-superconcept relationships and affects assignability of nodes into child or reference roles.
- **Aspects**: different parts of a language definition (Structure, Editor, Typesystem, Constraints, etc.). Technically, each aspect is a dedicated model inside a language's module.
- Some MPS modules and models can be read-only.
- MPS modules and models define dependencies between each other. DevKits can re-export dependencies on solutions and other devkits. If a module depends on a DevKit, it implicitly depends on all solutions exported by that DevKit.
- MPS models specify 'used languages'. If model A uses language L, nodes in model A can be instances of concepts from language L. Using a DevKit in a model automatically includes all languages exported by that DevKit (and any devkits it extends).

## Common Workflow — Initialize a Session

1. **Check the bundled skills** (the `moai:` skills in the table above) before starting unfamiliar work and load the relevant MoWare or MPS skill when it exists.
2. **Anchor on the user's focus** — call `mps_mcp_get_current_editor_root_node` so you know which root the user is looking at.
3. **Identify the task family**: editing user code → load `moai:mps-node-editing` and often `moai:mps-baselanguage`; investigating an unfamiliar language → load `moai:mps-language-analysis`; working with a MoWare DSL → load its dedicated skill.
4. **Validate frequently** with `mps_mcp_check_root_node_problems` — the changed root, or the model reference with `perRoot=true` after work on several roots.

## Essential Skills (Detail)

Hub references (`references/`):

| Reference | Open it for |
|---|---|
| [`finding-things.md`](references/finding-things.md) | Finding models, modules, languages, nodes and concepts (shortened names like `j.m.l.core`, smallest projection, caret/selection, packaged modules outside the project). |
| [`node-editing-rules.md`](references/node-editing-rules.md) | The rulebook on adding/updating nodes: concept selection, role types, cardinality, assignability, persistent IDs, surgical edits, temp-directory rule. |
| [`reference-formats.md`](references/reference-formats.md) | Node refs (`r:`/`i:`), concept refs (`c:`), model refs, list parameters, key spellings, rejected keys, node info envelope. |
| [`response-envelope.md`](references/response-envelope.md) | The `{ok, data, warnings, details}` envelope and the "Dry-run response" rule. |
| [`analysis-tools.md`](references/analysis-tools.md) | `mps_mcp_print_node`, `mps_mcp_check_root_node_problems` (model/module scope, `perRoot`, `rules`, `uncheckedSubtrees`, `quickFixes`), intentions, `FIX_REFERENCES`. |
| [`type-queries.md`](references/type-queries.md) | `mps_mcp_query_types` and `GET_TYPE` / `GET_EXPECTED_TYPE`. |
| [`ide-log.md`](references/ide-log.md) | Reading `idea.log` with `mps_mcp_read_ide_log`, verifying a write call. |
| [`module-dependencies.md`](references/module-dependencies.md) | Module and model dependencies, used languages and devkits, creating and renaming modules, "Cannot resolve concept" / `ClassNotFoundException`. |
| [`project-management.md`](references/project-management.md) | Opening a project when MCP only sees the welcome screen (standalone MPS, Linux/Windows), closing it with `mps_mcp_close_project`. |
| [`mcp-tools-index.md`](references/mcp-tools-index.md) | The complete inventory of MPS MCP tools. |

Large subtrees / staged construction and the inline-size/file-path rules: `moai:mps-node-editing` (`references/staged-construction.md`, SKILL.md File-Path Semantics).

## Scripts

`scripts/mps_dump.py` (Python standard library, offline) projects a large MCP result file (`mps_mcp_get_project_structure`, `mps_mcp_print_node`, `mps_mcp_get_concept_details`) down to the lines you need instead of reading the whole 10–40 KB file: `roots`, `models`, `node`, `tree`, `shape`, `count`.

```
python3 scripts/mps_dump.py roots "$TMPDIR/mps-node-123.json" --concept Entity
python3 scripts/mps_dump.py models "$TMPDIR/mps-node-789.json"          # modules, models, root counts
python3 scripts/mps_dump.py tree "$TMPDIR/mps-node-321.json" --depth 3  # indented subtree
```

`roots`, `count`, `node` and `tree` need a dump made with `includeRootNodes` (or `includeNodes`, or a `print_node` result); on a structure-only dump they exit 3 and name `models`. Run `--help` for every subcommand; `scripts/examples/` holds dumps to try it on. Stdout is the table plus a one-line JSON summary; the full table is written to a file under the system temp directory. Without `python3`, ask the server for the reduction instead: `mps_mcp_get_project_structure` with `nodeDetail: "names"` returns name / concept / reference of each root inline.

## Boundaries

- **Do not** edit `.mpl` module descriptors manually if an MCP wiring tool (`mps_mcp_module_dependency`, `mps_mcp_update_module`, …) covers the change.
- **Do not** delete-and-reinsert a node to "change" it when surgical tools exist.
