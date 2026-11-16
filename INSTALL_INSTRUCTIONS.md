# MoAI – Installation Instructions for Agents

## Context

- MoAI bundles skills and documentation for the MoWare DSLs ObjectFlow, ManMap
  and DataUX, as well as workflows for JetBrains MPS.

  | Information          | .                                                                                                           |
  |----------------|-----------------------------------------------------------------------------------------------------------------|
  | Name           | `moai`                                                                                                          |
  | Display name   | MoAI                                                                                                            |
  | Version        | according to commit                                                                                                         |
  | Description    | Documentation-backed agent skills for the modellwerkstatt.org moware werkbank DSLs and JetBrains MPS workflows. |
  | Author         | modellwerkstatt.org (responsible: Daniel Stieger)                                                               |
  | Repository     | `https://github.com/danielstieger/moai`                                                                         |
  | Skills         | `./skills/`                                                                                                     |
  | Category       | Developer Tools                                                                                                 |
  | Capabilities   | Interactive, Write                                                                                              |
  | Keywords       | moware, jetbrains-mps, objectflow, manmap, dataux                                                               |
- **MoAI is not listed in any plugin marketplace.** Do not search for it and do
  not install a plugin of the same name from any other source. MoAI is
  included exclusively from the local directory `moai_plugin/moai/` in this application
  project.
- MoAI lives as a versioned Git submodule under `moai_plugin/moai/`. The
  application project determines the version in use through the submodule
  commit.
- `moai_plugin/tools/` is a copy of the MoAI tools that belongs to the
  application project. Agents may extend it; it is checked in with the project.

## Rules

- The package boundary in `moai_plugin/moai/SESSION_CONTEXT.md` ("Package boundary", "Skills")
  applies during installation as well: nothing is written below `moai_plugin/moai/`, and only
  `tools/` is copied out of it (step 3).
- Do not create or change the project's instruction files (`AGENTS.md`, `CLAUDE.md` or
  similar). They belong to the project; MoAI reaches the agent through a hook (step 2).
- Do not call the MPS MCP tool `mps_mcp_initialize_project_for_agents`, during installation or
  later. It installs JetBrains' generic `mps-*` skills and its own `AGENTS.md` / `CLAUDE.md`
  into the project, which compete with MoAI.
- If a step requires a decision that cannot be derived from these
  instructions or the project, ask instead of guessing.

## Steps

### 1. Register the plugin in your runtime

- Determine how your agent runtime installs or loads a **local plugin that is
  not listed in a marketplace** from a directory. Use your runtime's official
  documentation or help for this.
- Prefer a **project-scoped** registration that can be versioned with the
  application project over a user-wide installation.
- The registration points to the directory `moai_plugin/moai/` (relative path from the
  project root), not to a copy.
- Enable the plugin if the runtime distinguishes between installed and
  enabled.
- If your runtime does not support local plugins, stop here and report this
  together with the available alternatives, without implementing any of them.

### 2. Set up the session hook

- Configure a hook in your runtime that adds the content of
  `moai_plugin/moai/SESSION_CONTEXT.md`, unchanged, to the agent's context at every session
  start: a new session, a resumed or continued session, after the conversation is cleared, and
  after the context is compacted.
- If your runtime starts subagents with a context of their own, configure the same for the
  start of a subagent.
- The hook reads the file each time it runs. Do not copy the text into the hook configuration;
  a submodule update must take effect without reinstalling.
- Register the hook **project-scoped**, in a file that is versioned with the application
  project and lies outside `moai_plugin/moai/`.
- If your runtime has no hook that adds context at session start, stop here and report this.

### 3. Copy the tools

Run in the project root:

```bash
cp -r moai_plugin/moai/tools moai_plugin/tools
```

### 4. Check prerequisites

- Check whether tools from an MPS MCP integration are available in your
  runtime.
- If not, do not configure anything speculatively; instead point out that
  JetBrains MPS must be running with the target project open and the MPS MCP
  integration enabled.
- Check that `python3` (3.8 or later) is available; the MoAI tools in
  `moai_plugin/tools/` need it. If it is missing, report it.

### 5. Verify

- Reload the runtime or plugins if required for the changes to take effect,
  or state the required command or restart.
- Confirm that `moai:mps-mcp-workflow` is visible in your runtime, then that
  every skill named in its skill table is visible as well.
- Run the hook command once by hand and confirm that it prints `SESSION_CONTEXT.md`. The hook
  takes effect with the next session; state that a new session is required.

## Final Report

Report briefly:

- the included MoAI version according to last commit in moai submodule
- how and in which scope the plugin was registered, including created or
  modified files;
- which hooks were configured, in which file, and for which events;
- whether the skills are visible;
- status of the MPS MCP integration;
- open issues and steps required from the user (e.g. restart, commit).

## Update

Only when the user asks for it. In the project root:

```bash
git submodule update --remote --merge moai_plugin/moai
```

The tools in `moai_plugin/tools/` do not change with this. Synchronize them by hand
with `moai_plugin/moai/tools/`. Do not simply copy over them: they may contain the
project's own extensions, which would be lost.
