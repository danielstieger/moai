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
  included exclusively from the local directory `moai/` in this application
  project.
- MoAI lives as a versioned Git submodule under `moai/`. The application
  project determines the version in use through the submodule commit.

## Rules

- Do not modify any files below `moai/`. Anything your runtime additionally
  needs for registration belongs in the application project, outside the
  submodule.
- Do not copy the MoAI skills as project-local skills and do not recreate
  them. They are provided exclusively through the plugin.
- Do not overwrite existing instruction files (`AGENTS.md`, `CLAUDE.md` or
  similar); merge the content instead.
- If a step requires a decision that cannot be derived from these
  instructions or the project, ask instead of guessing.

## Steps

### 1. Register the plugin in your runtime

- Determine how your agent runtime installs or loads a **local plugin that is
  not listed in a marketplace** from a directory. Use your runtime's official
  documentation or help for this.
- Prefer a **project-scoped** registration that can be versioned with the
  application project over a user-wide installation.
- The registration points to the directory `moai/` (relative path from the
  project root), not to a copy.
- Enable the plugin if the runtime distinguishes between installed and
  enabled.
- If your runtime does not support local plugins, stop here and report this
  together with the available alternatives, without implementing any of them.

### 2. Set up project instructions

- Copy `moai/TEMPLATE_PROJECT_AGENTS.md` to the project root as `AGENTS.md`.
  If an `AGENTS.md` already exists, add the template content as a separate
  section.
- If your runtime reads an instruction file other than `AGENTS.md`, make sure
  that file references `AGENTS.md` or includes its content, instead of
  duplicating the instructions.

### 3. Check prerequisites

- Check whether tools from an MPS MCP integration are available in your
  runtime.
- If not, do not configure anything speculatively; instead point out that
  JetBrains MPS must be running with the target project open and the MPS MCP
  integration enabled.

### 4. Verify

- Reload the runtime or plugins if required for the changes to take effect,
  or state the required command or restart.
- Confirm that the MoAI skills (`moai:objectflow-dsl`, `moai:manmap-dsl`,
  `moai:dataux-dsl`, `moai:mps-mcp-workflow`) are
  visible in your runtime.

## Final Report

Report briefly:

- the included MoAI version according to last commit in moai submodule
- how and in which scope the plugin was registered, including created or
  modified files;
- whether the skills are visible;
- status of the MPS MCP integration;
- open issues and steps required from the user (e.g. restart, commit).
