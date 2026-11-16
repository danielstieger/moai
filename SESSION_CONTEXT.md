# MoAI session context

This is a modellwerkstatt MoWare application project built with JetBrains MPS. It uses the MoAI
package in `moai_plugin/moai/`, which provides the agent skills, documentation and conventions for
the MoWare DSLs and the MPS workflow. This text is added to every session by a hook the MoAI
installation set up.

## Package boundary

- `moai_plugin/moai/` is a versioned dependency (Git submodule) and read-only. Anything
  project-specific, including runtime registration files, lives outside it.
- `moai_plugin/tools/` is the project's own copy of the MoAI tools and may be extended.

## Skills

The MoAI plugin supplies the skills for all work in this project:

- `moai:objectflow-dsl` – domain structures, services, commands, tests, configuration,
  permissions, resources;
- `moai:manmap-dsl` – persistence descriptions, repositories, queries, save/delete, direct SQL;
- `moai:dataux-dsl` – pages, forms, tables, layouts, bindings, includes, menus, applications,
  batch jobs;
- `moai:baselanguage-collections-dsl` – BaseLanguage collections and closures;
- `moai:plan` – plan an area before modeling it: fixed template, questions instead of guesses,
  approval before any change in MPS;
- `moai:mps-mcp-workflow` – MPS tooling and workflow; its skill table names the matching MPS
  support skill.

If these skills are not visible, the MoAI plugin is not installed or enabled; that is reported to
the user. MoAI skills are not recreated as project-local skills.

The MPS MCP tool `mps_mcp_initialize_project_for_agents` is never called in this project: it
installs JetBrains' generic `mps-*` skills and its own `AGENTS.md` / `CLAUDE.md`, which compete
with MoAI.

## MPS workflow

All MPS-related work follows `moai_plugin/moai/MPS_AGENT_GUIDE.md`, which is read before the first
MPS action of a session.

## Conventions

The MoWare modeling conventions are the files in `moai_plugin/moai/conventions/`. All of them are
read before planning or modeling and apply in full. A project that deviates from a convention
states so in its own `CLAUDE.md` / `AGENTS.md`; without such a statement there is no deviation,
and an agent never deviates on its own.

## Documentation

The intended MoWare semantics are documented in `moai_plugin/moai/docu/`: `moware-werkbank.md`
(architecture and interaction of the DSLs), `objectflow.md`, `manmap.md`, `dataux.md`. They are
read in stages. For research and planning, `moware-werkbank.md` together with the sections
"Modellierungsumfang und Ausdrucksmöglichkeiten" and the chapter maps ("Kapitellandkarte") of the
three DSL documents is sufficient. The full part of a DSL document is read only when modeling
that layer, following the section links in the skills. Reading all four documents up front costs
about 140,000 tokens and is rarely needed.

## Tools

`moai_plugin/tools/` holds command-line tools (Python standard library, called with `python3 -I`):

- `blueprint.py` – look up concepts (`find`, `concept`), build or check blueprints (`build`,
  `check`);
- `verify.py` – compare an inserted node with its blueprint;
- `dump.py` – condense check reports, show blueprints, search dumps;
- `copyroot.py` – copy roots from another model, e.g. configuration templates;
- `text2of.py` – convert method and command bodies written as Java with markers into ObjectFlow
  and ManMap nodes;
- `scaffold.py` – generate convention-compliant skeletons from a JSON specification.

They are used instead of self-written scripts for the same purpose; their input and output files
live in the system temp directory. A limit of a tool is not a limit of the language: the model is
not changed to suit a tool, the tool in `moai_plugin/tools/` is extended instead.
