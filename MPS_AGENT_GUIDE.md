# Agents Guide for MPS Work in a MoWare Application

This is a modellwerkstatt MoWare application built with JetBrains MPS. All source of truth lives in MPS models. The MoWare languages ObjectFlow, ManMap and DataUX are used, not changed: their language definitions and generators are not part of the application project. Use this file as the entry point for MPS work.

For detailed MPS node, model, validation, and MCP workflows, load the `moai:mps-mcp-workflow` skill. If the MoAI skills are not available through the agent runtime, report that the MoAI plugin is not installed or enabled.

MCP integration with MPS is an experimental feature. Use it with caution, expect surprises as well as future changes, and report any issues to the JetBrains MPS team.

## ⚠️ Known Limitation: MCP Tools Fail on Paths Containing Spaces

Every JetBrains MCP server (`mps-mcp`, `idea-mcp`, and equivalents in other JetBrains IDEs) shares a platform bug: an MCP tool call throws `java.net.URISyntaxException: Illegal character in path` if **any currently open project's absolute path contains a space** — not only the project a call targets. This is not fixable from the agent or client side: percent-encoding the path argument does not reliably help, because the same crash also occurs while the server internally scans its own list of open projects for a match, a code path the client cannot influence. Tracked upstream as IJPL-236112 (and duplicates); fixed on the platform's newer line but, as of 2026.1.x, not yet backported to the release line MPS/IDEA ships on.

If MCP tool calls start failing session-wide with this error:
- Do not retry with an encoded/escaped path — it will not help.
- Check whether any open project — including phantom or harness-created ones — lives at a path containing a space.
- Ask the user to move/rename the affected project to a space-free path and reopen it in the IDE.
- Until then, fall back to manual source reading and ask the user to build/test via the IDE UI.

## ⚠️ Known Limitation: Model-Level Problem Check Misses Root Problems

`mps_mcp_check_root_node_problems` accepts a model reference, but then it does not check the roots the model contains: it returns `no problems found` even when roots have errors or warnings. Reported to JetBrains.

To validate a model:
- List its roots with `mps_mcp_get_project_structure` (`startingPoint` = the model, `includeRootNodes: true`).
- Call `mps_mcp_check_root_node_problems` for each root node reference.
- Never treat a model-level `no problems found` as a successful validation.

## ⚠️ WARNING: Never Read Raw MPS Model Files

**If you are opening or reading `.mps`, `.mpl`, or other MPS XML files directly, you are way off track and must stop immediately.**

MPS model files are binary-like serialized XML that cannot be safely understood or edited as plain text. Reading them gives you opaque node IDs and no semantic insight — you will misinterpret the content and likely corrupt the model if you try to edit it.

**What to do instead:**
- Use MPS MCP tools (`mps_mcp_*`) to inspect, navigate, and edit MPS models.
- If MPS MCP tools are not available in your session, ask the user to start MPS and enable the MPS MCP server before continuing with any MPS work.
- Do not attempt to parse, edit, or reason from raw `.mps` XML.

## Project Nature

This repository is primarily an MPS project. Generated Java, Kotlin, and XML artifacts are produced by MPS generators and must not be edited directly. By default, all meaningful source lives in MPS models, but some projects also include hand-authored JVM or build code (e.g. custom runtime libraries, Gradle build scripts, or test harnesses). If this project contains such code, it is documented in the application project's `AGENTS.md`, together with the tools appropriate for it.

Use MPS MCP tools as the primary toolset for all model-related work.

## Tool Selection

Use MPS MCP tools for everything model-related:
- modules, models, and root nodes
- model navigation, node editing, and validation
- generation and build

Do not change the MoWare language definitions (structure, editor, constraints, typesystem, behavior, generator) from an application project.

File-based tools (Read, Grep, Glob) are acceptable for:
- inspecting generated output to understand runtime behavior or diagnose a problem
- reading project configuration files that are not driven by MPS models
- reading plain text documentation

Do not use file-based tools to modify `.mps` model files directly. MPS serializes models as XML, but the format is opaque and fragile — always use MPS MCP tools instead.

If MPS MCP tools are unavailable and the task requires model-aware editing:
- do not hand-edit `.mps` model files as plain XML unless the user explicitly asks for that
- explain the limitation and ask whether to proceed with a workaround or wait for MPS-aware tooling

## Generated Code Is Read-Only

Generated artifacts are recreated on every Make/Rebuild. Do not edit them. If a problem appears in generated code, find and fix the root cause in the MPS model, language, or generator.

Typical generated locations in MPS projects:
- `source_gen/` — Java/Kotlin sources generated by MPS generators
- `source_gen_append/` — additional generated sources appended to the main output
- `classes_gen/` — compiled class files produced from generated sources

Inspect the project structure if you are unsure which directories apply to this project.

Inspection of generated code is allowed when:
- reading a generated file to understand what a generator is producing
- tracing a runtime error back to a generator
- confirming that a model change had the expected effect

## Rules for MPS Work

- Load the `moai:mps-mcp-workflow` skill at the start of an MPS session. If MPS MCP tools are unavailable, apply the fallback described in the Tool Selection section above.
- Use MPS MCP tools whenever available; do not hand-edit `.mps` files as plain XML.
- Resolve nodes, concepts, models, and modules precisely before editing.
- Validate after structural changes using `mps_mcp_check_root_node_problems` on each changed root.
- Errors must be fixed. Warnings and infos can come from the MoWare Werkbank or BaseLanguage itself and are to be ignored; do not change a model to silence them.
- Rebuild or regenerate after significant changes to keep generated artifacts consistent.

Use the `moai:mps-mcp-workflow` skill for complete guidance on MPS workflows, skills, available tools, and best practices.

## Skills

MoAI provides its skills through the `moai:` plugin namespace. Start with `moai:mps-mcp-workflow` for the overview and a directory of every other skill.

## Selecting the MPS Project

The `mps_mcp_*` tools themselves act on whichever MPS project is open in MPS; if a tool reports "no project" or "multiple projects opened", call `mps_mcp_list_open_projects` and give the next tool the intended project's `mpsProjectBaseDirectory`, not this repository root. All `mps_mcp_*` tools are routed by the framework's `projectPath` selector, so pass the open project's base directory (never an ancestor) as `projectPath`. When several MPS projects are open and the target is not obvious from the request or current editor focus, ask the user which project to use rather than guessing.