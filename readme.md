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
├── MPS_AGENT_GUIDE.md          General MPS working rules
├── INSTALL_INSTRUCTIONS.md     Installation instructions for agents
└── TEMPLATE_PROJECT_AGENTS.md  Template for the application project
```

The MoWare skills are:

- `objectflow-dsl` for the domain model, services, commands, tests and
  configuration;
- `manmap-dsl` for persistence mappings, repositories, queries and SQL;
- `dataux-dsl` for user interfaces, applications and batch jobs.

Additional MPS skills support node editing, BaseLanguage, model manipulation,
language analysis, the MPS console and run configurations. `mps-mcp-workflow`
is the entry point for MPS work.

## Documentation (in German)

- [MoWare Werkbank](docu/moware-werkbank.md) – architecture and interaction;
- [ObjectFlow](docu/objectflow.md) – domain model and business logic;
- [ManMap](docu/manmap.md) – relational persistence and repositories;
- [DataUX](docu/dataux.md) – user interfaces, applications and batch jobs.

The documentation describes the intended domain semantics. The loaded MPS
language models are authoritative for the technical AST structure, roles,
cardinalities, references and validation rules.

## Installation as a Git Submodule

MoAI is not listed in any plugin marketplace and is included locally in the
project.

1. Add the submodule manually in the root of the application project:

   ```bash
   git submodule add https://github.com/danielstieger/moai.git moai
   git submodule update --init --recursive
   ```

2. Hand the rest of the installation to a coding agent [INSTALL_INSTRUCTIONS.md](INSTALL_INSTRUCTIONS.md) is written as a
   prompt for this. In the root of the application project, this is enough:

   > Read `INSTALL_INSTRUCTIONS.md` from ./moai and perform the installation
   > for this project.

   The agent registers the plugin in its runtime, sets up `AGENTS.md` from
   `moai/TEMPLATE_PROJECT_AGENTS.md` and checks the prerequisites. The template
   marks `moai/` as a packaged dependency and points agents to the installed
   MoAI skills and the documentation.

## Updating

The application project determines which MoAI version is used through its
submodule commit. An update is performed in the application project and then
versioned as a new submodule state:

```bash
git submodule update --remote --merge moai
git add moai
```

Package files under `moai/` are not modified directly during regular
application development. Project-specific instructions and skills stay outside
the submodule.

## Prerequisites

- JetBrains MPS with the target project open;
- enabled MPS MCP integration for model-aware agent work;
- the MoAI plugin installed and enabled in the agent runtime in use.
