# MoAI – Agent Plugin for modellwerkstatt MoWare

MoAI bundles agent skills and documentation for the three MoWare languages
ObjectFlow, ManMap and DataUX, as well as reusable workflows for JetBrains MPS.
The package is intended to live as a versioned Git submodule in a MoWare
application project and to be installed as an agent plugin at the same time.

## Contents

```text
moai/
├── skills/                     MoWare and MPS skills
├── docu/                       Architecture and language documentation
├── conventions/                Binding modeling conventions (in German)
├── MPS_AGENT_GUIDE.md          General MPS working rules
├── INSTALL_INSTRUCTIONS.md     Installation instructions for agents
├── SESSION_CONTEXT.md          Text a session hook adds to every agent session
├── tools/                      Tools for agents (Python), with the language structure export
└── maintenance/                For MoAI maintainers only, not for agents in a project
```

The MoWare skills are:

- `moai:objectflow-dsl` for the domain model, services, commands, tests and
  configuration;
- `moai:manmap-dsl` for persistence mappings, repositories, queries and SQL;
- `moai:dataux-dsl` for user interfaces, applications and batch jobs;
- `moai:baselanguage-collections-dsl` for BaseLanguage collections and
  closures inside MoWare code;
- `moai:plan` for planning a change to an area before it is modeled (see
  [Planning with `moai:plan`](#planning-with-moaiplan)).

`moai:mps-mcp-workflow` is the hub skill for MPS work; its skill table lists
the remaining MPS skills (BaseLanguage, node editing, model manipulation,
language analysis, MPS console, run configurations).

## Documentation (in German)

- [MoWare Werkbank](docu/moware-werkbank.md) – architecture and interaction;
- [ObjectFlow](docu/objectflow.md) – domain model and business logic;
- [ManMap](docu/manmap.md) – relational persistence and repositories;
- [DataUX](docu/dataux.md) – user interfaces, applications and batch jobs.

The documentation describes the intended domain semantics; its relation to
the loaded MPS languages is stated in "Zweck und Geltungsbereich" of
`docu/moware-werkbank.md`.

## Planning with `moai:plan`

`moai:plan` turns a requirement into a plan file that the developer approves
before anything is changed in MPS. It is called with the requirement:

> /moai:plan Die Buchhaltung kann eine Rechnung stornieren, solange keine
> Zahlung gebucht ist.

The argument `full` makes the agent read all four documents completely
instead of only the parts the area touches.

What it produces depends on the request:

| Request | Result |
|---|---|
| New application or new bounded context | `plan/zuschnitt.md`: glossary, bounded contexts, areas and their dependencies, roles, runtime configuration. One file per application, updated when an area is added. |
| New area | `plan/<bereich>-neu.md`, after the area is entered in `zuschnitt.md`. |
| Change to an existing area | `plan/<bereich>-<thema>.md`, containing only what is new or changes. |
| Small change (no new entity, no new transition, no new or changed rule) | No plan file; the change, the affected roots and the open questions are presented directly. |

The plans live in `plan/` of the application project, outside `moai_plugin/`.
A plan follows a fixed template from the inside out: acceptance criteria,
`domain` (values, aggregate, status, transitions, rules, persistence), `read`,
`tests`, `unit.read` and `unit`, `app` and permissions, then the list of roots
that are created or changed and the order of implementation. A filled example
is [beispiel-rechnung-stornieren.md](skills/plan/templates/beispiel-rechnung-stornieren.md).

How the agent works with the plan:

- **Questions instead of guesses.** Anything domain-related that the
  requirement, the conventions, the project instructions and the existing
  model do not answer is marked `KLÄREN:` and asked in one round, with a
  proposal where there is one. A plan with an open `KLÄREN:` cannot be
  approved.
- **Assumptions for presentation.** Columns, layout, labels and the position
  of a menu entry are set as `ANNAHME:` and listed; they do not block the
  approval.
- **Approval.** The plan has the status "Entwurf" until the developer
  explicitly approves it ("freigegeben"). Before that, models are only read.
- **Traceability.** Every transition and rule refers to an acceptance
  criterion, and every acceptance criterion has a test.
- **Binding during modeling.** The approved plan is modeled in its stated
  order with the DSL skills. If a domain gap appears, the agent stops, the
  plan goes back to "Entwurf" and is approved again.
- **Schema by the developer.** The plan names the tables and columns to be
  created; the agent halts before the tests that need the database until the
  schema is confirmed.
- **Deviations from conventions** are decided by the developer and stand in
  their own section of the plan.

## Installation as a Git Submodule

MoAI is not listed in any plugin marketplace and is included locally in the
project.

1. Add the submodule manually in the root of the application project:

```bash
   git submodule add https://github.com/danielstieger/moai.git moai_plugin/moai
   git -C moai_plugin/moai sparse-checkout set --no-cone '/*' '!/maintenance/'
   git submodule update --init --recursive
```

2. Hand the rest of the installation to a coding agent;
   [INSTALL_INSTRUCTIONS.md](INSTALL_INSTRUCTIONS.md) is written as a prompt
   for this. In the root of the application project, this is enough:

   > Read `INSTALL_INSTRUCTIONS.md` from ./moai_plugin/moai and perform the installation
   > for this project.

   The agent registers the plugin in its runtime, sets up a session hook that
   adds `moai_plugin/moai/SESSION_CONTEXT.md` to every session, copies the tools
   to `moai_plugin/tools/` and checks the prerequisites. The session context marks
   `moai_plugin/moai/` as a packaged dependency and points agents to the MoAI
   skills, conventions and documentation. The project's own `AGENTS.md` /
   `CLAUDE.md` are not touched.

## Updating

The application project determines which MoAI version is used through its
submodule commit. An update is performed in the application project and then
versioned as a new submodule state:

```bash
git submodule update --remote --merge moai_plugin/moai
git add moai_plugin/moai
```

The tools in `moai_plugin/tools/` do not change with it. Afterwards
ask a coding agent to synchronize them ("Update" in
[INSTALL_INSTRUCTIONS.md](INSTALL_INSTRUCTIONS.md)).

The rules for working with the package (read-only `moai_plugin/moai/`, project-specific
instructions and skills outside the submodule) are stated in
`SESSION_CONTEXT.md`.
