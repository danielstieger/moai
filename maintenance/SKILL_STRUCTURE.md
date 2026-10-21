# Where Knowledge Belongs

For MoAI maintainers. Agents working in an application project do not need this file.

Each kind of knowledge has one place. Agents find it there, and a maintainer knows where to add or change it.

| Part | Holds | Does not hold |
| --- | --- | --- |
| `docu/` | Semantics and runtime behaviour of the MoWare languages; chapter maps (Kapitellandkarten): projection → concept → FQ name | Binding architecture rules; links to or the location of the conventions (docu may say that conventions exist) |
| `conventions/` | How an application must use the languages (binding) | Language capabilities |
| `skills/*/SKILL.md` | Entry point: when to use the skill, critical rules, workflows | Lookup tables, detailed semantics |
| `skills/*/references/` | Lookup: concepts and AST roles, packaged examples, recipes, gotchas | Semantics already in `docu/` (link to it instead) |
| `skills/*/references/blueprints/` | Patterns to insert | Application names or references |
| `tools/` | Tools agents run | Project state |
| `maintenance/` | Maintainer material | Anything agents need at work |

## Rules

- **No knowledge twice.** Link to the one place instead of repeating it.
- **Exception: the entry of a skill.** A short section an agent must see when it starts (e.g. "Unknown construct" in the DSL skills) is repeated in every skill that needs it. Agents follow links poorly; the entry is where they look.
- **Conventions are referenced by name** in skills (e.g. conventions `commands`). Where they are and which ones a project changes is stated only in the project's `AGENTS.md` (from `TEMPLATE_PROJECT_AGENTS.md`).
- **Changes to the JetBrains `mps-*` skills** are recorded with their reason in [MPS_SKILLS_CHANGES.md](MPS_SKILLS_CHANGES.md).
