# Agent Guide for a MoWare Application Project

This project uses the MoAI package in the `moai/` subdirectory. MoAI provides
the agent skills and documentation for the modellwerkstatt MoWare DSLs and the
JetBrains MPS workflow.

## MoAI Package Boundary

- Treat `moai/` as a versioned dependency. Do not modify files below `moai/`
  during normal application development.

## Skills

Use the skills supplied by the installed MoAI plugin:

- `moai:objectflow-dsl` for domain structures, services, commands, tests,
  configuration, permissions, and resources;
- `moai:manmap-dsl` for persistence descriptions, repositories, queries, save/delete,
  and direct SQL;
- `moai:dataux-dsl` for pages, forms, tables, layouts, bindings, includes, menus,
  applications, and batch jobs;
- `moai:mps-mcp-workflow` as the entry point for MPS tooling and workflow;
- the matching MPS support skill for node editing, BaseLanguage, console work,
  model manipulation, language analysis, or run configurations.

If the runtime does not expose these skills, report that the MoAI plugin is not
installed or enabled. Do not recreate MoAI skills as project-local skills.

## Documentation

Use these package documents for the intended MoWare semantics:

- `moai/docu/moware-werkbank.md` — architecture and interaction of the DSLs;
- `moai/docu/objectflow.md` — ObjectFlow language documentation;
- `moai/docu/manmap.md` — ManMap language documentation;
- `moai/docu/dataux.md` — DataUX language documentation.

Read them in stages. For research and planning, `moai/docu/moware-werkbank.md`
together with the sections "Modellierungsumfang und Ausdrucksmöglichkeiten" and
the chapter maps ("Kapitellandkarte") of the three DSL documents is sufficient;
they name every concept with its projection and FQ name. Read the full part of a
DSL document only when modeling that layer, following the section links in the
skills. Reading all four documents up front costs about 140,000 tokens and is
rarely needed.

## Conventions

Before modeling, read all files in `./moai/conventions/`. They define binding
modeling conventions (e.g. naming) for this application project.

## MPS Workflow

Before any MPS-related work, read and follow `moai/MPS_AGENT_GUIDE.md`. Its MPS
tooling, model-editing, validation, generated-code, and troubleshooting rules
apply to this application project.
