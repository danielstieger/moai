# Agents Guide for MPS Work in a MoWare Application

This is a modellwerkstatt MoWare application built with JetBrains MPS. All source of truth lives in MPS models. The MoWare languages ObjectFlow, ManMap and DataUX are used, not changed: their language definitions and generators are not part of the application project. MCP integration with MPS is experimental — expect surprises and report issues to the JetBrains MPS team.

After this file, load `moai:mps-mcp-workflow`: it holds the detailed node, model, validation, and MCP workflows and the table of every other MoAI skill.

## Never Read Raw MPS Model Files

Do not open, parse, edit, or reason from `.mps`, `.mpl`, or other MPS XML files: the serialized format is opaque, gives node IDs without semantics, and hand-edits corrupt models. All inspection, navigation, and editing of models goes through the MPS MCP tools (`mps_mcp_*`).

If the MPS MCP server is not connected, or its calls fail session-wide: stop all model work, explain the limitation, and ask the user to start MPS with the target project open and the MPS MCP server enabled, or to fix the cause. Continue only with work that needs no model access: documentation, generated output, project configuration. Hand-editing `.mps` XML happens only on the user's explicit instruction. A connected server whose tools were filtered or deferred is not this case; see the next section.

## Keep the Full MPS MCP Toolset

The `mps_mcp_*` tools are how this project's code is read and edited. Which of them a session needs cannot be guessed from the opening request.

- Do not reduce, defer, hide, or filter the MPS MCP tools; keep every `mps_mcp_*` tool available for the whole session.
- A filtered or deferred tool is not unavailable: load it, or restore the server, before any other work; if the host offers no way, ask the user to enable the full server. Do not continue on a reduced subset, and do not fall back to file tools or raw `.mps` XML in its place.

## Tool Selection

Use MPS MCP tools for everything model-related: modules, models, nodes, navigation, editing, validation, generation, and build. File-based tools (Read, Grep, Glob, or `cat` and `grep` when your runtime has no such tools) are fine for reading generated output, configuration that is not driven by MPS models, and plain-text documentation. If the project contains hand-authored JVM or build code, the project's `CLAUDE.md` / `AGENTS.md` lists it together with the tools appropriate for it.

Do not change the MoWare language definitions (structure, editor, constraints, typesystem, behavior, generator) from an application project.

Pass `projectPath` — the open MPS project's base directory, never an ancestor such as the repository root — on **every** `mps_mcp_*` call, starting with the first one; a call without it is rejected. If you do not know the path yet, pass the session's current working directory on the first call; if that is rejected, take the path from the rejection message, which lists the open projects, and reuse it for the session. An empty project list means MPS shows the welcome screen: ask the user to open the project. Details, multi-project checkouts and when to ask the user: ["Which project the tools act on"](skills/mps-mcp-workflow/SKILL.md#which-project-the-tools-act-on) in `moai:mps-mcp-workflow`.

If MCP calls fail session-wide with `java.net.URISyntaxException: Illegal character in path`, an open project's absolute path contains a space — a platform bug in every JetBrains MCP server. Do not retry with an encoded or escaped path. Ask the user to move that project to a space-free path and reopen it; details: [`references/mcp-server-troubleshooting.md`](skills/mps-mcp-workflow/references/mcp-server-troubleshooting.md) in `moai:mps-mcp-workflow`.

## Generated Code Is Read-Only

`source_gen/`, `source_gen_append/`, and `classes_gen/` are recreated on every Make/Rebuild — never edit them. Reading them is fine to see what a generator produces, to trace a runtime error back to its generator, or to confirm that a model change took effect. Fix problems in the MPS model; if the cause lies in a MoWare language or generator, report it to the user instead of changing the language.

## Rules for MPS Work

- Validate after structural changes using `mps_mcp_check_root_node_problems`: on the single changed root, or after work on several roots once on the model reference with `perRoot=true` (one row per root). Read `warnings` and `details.uncheckedSubtrees` too (`references/analysis-tools.md` in `moai:mps-mcp-workflow`).
- Errors must be fixed. Warnings and infos can come from the MoWare Werkbank or BaseLanguage itself and are to be ignored; do not change a model to silence them.
- Some failures (swallowed node-factory exceptions, generator or make problems, tool-side regressions) reach only the IDE log, not the tool response. When a tool reports success but the effect is missing, call `mps_mcp_read_ide_log` with `sinceMinutes` covering the call window and `minLevel="WARN"`: it reads `idea.log` and its rotated files without a path, also for a standalone MPS. `mps_mcp_list_open_projects` reports the log location as `logDirectory` / `logFile`; reading the log by hand: [`references/ide-log.md`](skills/mps-mcp-workflow/references/ide-log.md) in `moai:mps-mcp-workflow`.
