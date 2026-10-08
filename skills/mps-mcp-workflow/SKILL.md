---
name: mps-mcp-workflow
description: Complete JetBrains MPS workflow guide for MoWare application projects — modules, models, node JSON blueprints, validation, MPS MCP tool usage, and the index of companion skills. Use whenever working in an MPS project, when `MPS_AGENT_GUIDE.md` says to load it, or when you need to pick the right companion skill.
---

# Projectional Agent Toolkit – JetBrains MPS for Agents

Hub skill for working with JetBrains MPS (Meta Programming System) models and the MPS MCP tools. Load it after `AGENTS.md` and `MPS_AGENT_GUIDE.md` whenever the task involves MPS artifacts or MPS MCP tooling.

## Critical Directives

- **Never read or edit raw `.mps` / `.mpl` XML; use `mps_mcp_*` tools.** Rule and fallback: [`MPS_AGENT_GUIDE.md`](../../MPS_AGENT_GUIDE.md#never-read-raw-mps-model-files).
- **Editing rules** (preserve node IDs, surgical `mps_mcp_update_node` over full-root rewrites, validate every changed root): `moai:mps-node-editing`.
- **Language definitions are off-limits.** In a MoWare application project never edit language structure or aspects (`mps_mcp_alter_structure`, `mps_mcp_scaffold_editor`, aspect models of the MoWare languages) — see `MPS_AGENT_GUIDE.md`.

> **Tool name note**: MPS MCP tools are named with a `mps_mcp_` prefix (e.g. `mps_mcp_query_nodes`, `mps_mcp_alter_nodes`, `mps_mcp_get_concept_details`). Your MCP client wraps these with a server-specific prefix (e.g. `mcp__mps-mcp__`), which varies by environment. Match tools by the stable `mps_mcp_*` suffix.

> **Which project the tools act on (subdirectory & multi-project checkouts).** The `mps_mcp_*` tools operate on the MPS project currently open in the running MPS instance. That project often lives in a **subdirectory** of your repository (e.g. `<repo>/<mps-project-dir>`), and one checkout may even hold **several** MPS projects. The host resolves the project from your client's workspace roots, then falls back to the single open project. If a tool call is rejected with "no project opened" or "multiple projects opened", call `mps_mcp_list_open_projects`, then supply the intended project's `mpsProjectBaseDirectory` — the folder MPS actually opened, i.e. a path *at or inside* it, **not** the repository root — via the host's project-path argument.
>
> **Multi-project repository rules.** All open MPS projects share the same module repository. Write targets — models, modules, root nodes, and nodes being mutated — must belong to the project selected by `projectPath`; tools refuse writes to another open project's elements. Read/reference/dependency targets may come from another open MPS project when they are explicitly named or imported: model/module dependencies, model used languages/devkits, node concepts, and reference targets can point across projects, and the foreign elements are treated like read-only library/stub elements. Returned JSON for an element from another open project includes `containingProject: { name, mpsProjectBaseDirectory }` and `editableFromCurrentProject: false`; nested references use prefixes such as `conceptContainingProject`, `targetContainingProject`, or `typeContainingProject`. These markers appear *only* for elements owned by another open project — their absence does not imply an element is editable (a read-only library/stub in the current project carries `readOnly: true` but no `containingProject`), so decide editability from `readOnly` together with these markers.
>
> **When in doubt, ask which project.** When several MPS projects are open under one repository / VCS root, the `mps_mcp_*` tools accept *any* valid project path and act relative to that project. Same-name resolution prefers the selected project's own elements before falling back to the shared repository, but an explicit reference may still resolve to another open project. If the intended project is not obvious from the user's request or the current editor focus (`mps_mcp_get_current_editor_root_node`), do **not** guess — show the `mps_mcp_list_open_projects` entries and ask the user which project the query or change should run against.

## Companion Skills

All skills bundled with this package are loaded as `moai:<skill-name>`. Load whichever ones apply to the current task.

> **Never call `mps_mcp_initialize_project_for_agents` in a MoWare project.** It installs JetBrains' generic `mps-*` skills into the project's `.claude/skills` (they compete with the `moai:` skills) and creates a `CLAUDE.md`. The `moai` package is the only skill catalog; see `INSTALL_INSTRUCTIONS.md`.

| Skill | What it covers |
|-------|---------------|
| `moai:baselanguage-collections-dsl` | Create and edit BaseLanguage collection types, creators, operations, access expressions, and collection foreach statements. |
| `moai:mps-baselanguage` | Author and edit `jetbrains.mps.baseLanguage` nodes using the Java parser or JSON AST blueprints. |
| `moai:mps-console` | Console commands and `smodel.query` scope queries. |
| `moai:mps-language-analysis` | Analyze MPS language definitions, concepts, metadata, aspects, and sample nodes. |
| `moai:mps-model-manipulation` | smodel + closures model code. |
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
4. **Validate frequently** with `mps_mcp_check_root_node_problems` on each changed root.

## Essential Skills (Detail)

Open `references/finding-things.md` for the protocol on finding models, modules, and languages (including shortened-name resolution like `j.m.l.core` → `jetbrains.mps.lang.core`).

Open `references/node-editing-rules.md` for the full rulebook on adding/updating nodes (concept selection, role types, cardinality, assignability, persistent IDs, surgical edits).

Open `references/reference-formats.md` for the reference-format protocol: node refs (`r:`/`i:`), concept refs (`c:`), and the critical "never use a concept ref where a node ref is expected" rule.

Large subtrees / staged construction and the inline-size/file-path rules: `moai:mps-node-editing` (`references/staged-construction.md`, SKILL.md File-Path Semantics).

Open `references/analysis-tools.md` for the inventory of analysis operations (`mps_mcp_print_node`, `mps_mcp_check_root_node_problems`, `mps_mcp_alter_nodes FIX_REFERENCES`, etc.).

Open `references/mcp-tools-index.md` for the complete inventory of MPS MCP tools grouped by Project/Structure, Modules and Models, Root Nodes and Nodes, Console, and Language Definition.

## Boundaries

- **Do not** edit `.mpl` module descriptors manually if an MCP wiring tool (`mps_mcp_module_dependency`, `mps_mcp_update_module`, …) covers the change.
- **Do not** delete-and-reinsert a node to "change" it when surgical tools exist.
