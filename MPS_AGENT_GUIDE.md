# Agents Guide for MPS Work in a MoWare Application

This is a modellwerkstatt MoWare application built with JetBrains MPS. All source of truth lives in MPS models. The MoWare languages ObjectFlow, ManMap and DataUX are used, not changed: their language definitions and generators are not part of the application project. This file is the entry point for MPS work.

After this file, load `moai:mps-mcp-workflow`: it holds the detailed node, model, validation, and MCP workflows and the table of every other MoAI skill.

MCP integration with MPS is an experimental feature. Use it with caution, expect surprises as well as future changes, and report any issues to the JetBrains MPS team.

## ⚠️ Known Limitation: MCP Tools Fail on Paths Containing Spaces

Every JetBrains MCP server (`mps-mcp`, `idea-mcp`, and equivalents in other JetBrains IDEs) shares a platform bug: an MCP tool call throws `java.net.URISyntaxException: Illegal character in path` if **any currently open project's absolute path contains a space** — not only the project a call targets. This is not fixable from the agent or client side: percent-encoding the path argument does not reliably help, because the same crash also occurs while the server internally scans its own list of open projects for a match, a code path the client cannot influence. Tracked upstream as IJPL-236112 (and duplicates); fixed on the platform's newer line but, as of 2026.1.x, not yet backported to the release line MPS/IDEA ships on.

If MCP tool calls start failing session-wide with this error:
- Do not retry with an encoded/escaped path — it will not help.
- Check whether any open project — including phantom or harness-created ones — lives at a path containing a space.
- Ask the user to move/rename the affected project to a space-free path and reopen it in the IDE.
- Until then, the fallback in "Never Read Raw MPS Model Files" applies.

## Never Read Raw MPS Model Files

**Never open, read, parse, edit, or reason from `.mps`, `.mpl`, or other MPS XML files.** They are opaque serialized XML: reading them yields node IDs without semantics, editing them corrupts the model. All inspection, navigation, and editing of models goes through the MPS MCP tools (`mps_mcp_*`).

**Fallback when MPS MCP tools are unavailable** (not exposed in the session, or failing session-wide): stop all model work, explain the limitation, and ask the user to start MPS with the target project open and the MPS MCP server enabled, or to fix the cause (see the known limitations above). Continue only with work that needs no model access: documentation, generated output, project configuration. Hand-editing `.mps` XML happens only on the user's explicit instruction.

## Project Nature

This repository is primarily an MPS project. Generated Java and XML artifacts are produced by MPS generators and must not be edited directly. By default, all meaningful source lives in MPS models, but some projects also include hand-authored JVM or build code (e.g. custom runtime libraries, Gradle build scripts, or test harnesses). If this project contains such code, the section "Hand-Authored Code Outside MPS" in `AGENTS.md` lists it together with the tools appropriate for it.

Use MPS MCP tools as the primary toolset for all model-related work.

## Tool Selection

Use MPS MCP tools for everything model-related:
- modules, models, and root nodes
- model navigation, node editing, and validation
- generation and build

Do not change the MoWare language definitions (structure, editor, constraints, typesystem, behavior, generator) from an application project.

File-based tools (Read, Grep, Glob, or their shell equivalents such as `cat` and `grep` when your runtime has no such tools) are acceptable for:
- inspecting generated output to understand runtime behavior or diagnose a problem
- reading project configuration files that are not driven by MPS models
- reading plain text documentation

Pass `projectPath` — the open MPS project's base directory, never an ancestor such as the repository root — on **every** `mps_mcp_*` call, starting with the first one; a call without it is rejected. If you do not know the path yet, pass the session's current working directory on the first call; if that is rejected, take the path from the rejection message, which lists the open projects, and reuse it for the session. An empty project list means MPS shows the welcome screen: ask the user to open the project. Details, multi-project checkouts and when to ask the user: ["Which project the tools act on"](skills/mps-mcp-workflow/SKILL.md#which-project-the-tools-act-on) in `moai:mps-mcp-workflow`.

## Generated Code Is Read-Only

Generated artifacts are recreated on every Make/Rebuild. Do not edit them. If a problem appears in generated code, find the root cause and fix it in the MPS model; if the cause lies in a MoWare language or generator, report it to the user instead of changing the language.

Typical generated locations in MPS projects:
- `source_gen/` — Java sources generated by MPS generators
- `source_gen_append/` — additional generated sources appended to the main output
- `classes_gen/` — compiled class files produced from generated sources

Inspect the project structure if you are unsure which directories apply to this project.

Inspection of generated code is allowed when:
- reading a generated file to understand what a generator is producing
- tracing a runtime error back to a generator
- confirming that a model change had the expected effect

## Rules for MPS Work

- Resolve nodes, concepts, models, and modules precisely before editing.
- Validate after structural changes using `mps_mcp_check_root_node_problems`: on the single changed root, or after work on several roots once on the model reference with `perRoot=true` (one row per root). Read `warnings` and `details.uncheckedSubtrees` too (`references/analysis-tools.md` in `moai:mps-mcp-workflow`).
- Errors must be fixed. Warnings and infos can come from the MoWare Werkbank or BaseLanguage itself and are to be ignored; do not change a model to silence them.
- Rebuild or regenerate after significant changes to keep generated artifacts consistent.

Some failures (swallowed node-factory exceptions, generator or make problems, tool-side regressions) reach only the IDE log, not the tool response. When a tool reports success but the effect is missing, call `mps_mcp_read_ide_log` with `sinceMinutes` covering the call window and `minLevel="WARN"`: it reads `idea.log` and its rotated files without a path, also for a standalone MPS. `mps_mcp_list_open_projects` reports the log location as `logDirectory` / `logFile`; reading the log by hand: [`references/ide-log.md`](skills/mps-mcp-workflow/references/ide-log.md) in `moai:mps-mcp-workflow`.
