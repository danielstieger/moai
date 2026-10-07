# Agent Guide for a MoWare Application Project

This project uses the MoAI package in the `moai/` subdirectory. MoAI provides
the agent skills and documentation for the modellwerkstatt MoWare DSLs and the
JetBrains MPS workflow.

## MoAI Package Boundary

- Treat `moai/` as a versioned dependency. Do not modify files below `moai/`;
  anything project-specific, including runtime registration files, lives in
  the application project outside the submodule.

## Skills

Use the skills supplied by the installed MoAI plugin:

- `moai:objectflow-dsl` for domain structures, services, commands, tests,
  configuration, permissions, and resources;
- `moai:manmap-dsl` for persistence descriptions, repositories, queries, save/delete,
  and direct SQL;
- `moai:dataux-dsl` for pages, forms, tables, layouts, bindings, includes, menus,
  applications, and batch jobs;
- `moai:baselanguage-collections-dsl` for BaseLanguage collection types,
  creators, operations, and foreach statements;
- `moai:mps-mcp-workflow` for MPS tooling and workflow; its skill table names
  the matching MPS support skill (node editing, BaseLanguage, console work,
  model manipulation, language analysis, run configurations).

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
they name every concept the documentation treats with its projection and FQ
name. Read the full part of a DSL document only when modeling that layer,
following the section links in the skills. Reading all four documents up front
costs about 140,000 tokens and is rarely needed.

## Conventions

Before modeling, read all files in `./moai/conventions/`. They are the MoWare
standard modeling conventions (e.g. structure, naming) and apply in full unless
this project states otherwise in the section below.

## Deviations from the MoWare Conventions

None.

A project may change individual conventions or replace them with its own. List
here what deviates and what applies instead. An agent never deviates on its
own; a deviation is a project decision.

## Hand-Authored Code Outside MPS

None.

If the project contains hand-written JVM or build code (custom runtime
libraries, Gradle build scripts, test harnesses), list it here together with
the tools appropriate for it.

## MPS Workflow

Before any MPS-related work, read and follow `moai/MPS_AGENT_GUIDE.md`. Its MPS
tooling, model-editing, validation, generated-code, and troubleshooting rules
apply to this application project.
