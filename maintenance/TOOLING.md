# MoAI Tooling – Specification and Plan

For MoAI maintainers. Agents working in an application project do not need this file.

What the tools in `tools/` must do, why they exist, and in which order they are built. What would make
parts of them obsolete on the MCP side is in [MCP_DEPENDENCIES.md](MCP_DEPENDENCIES.md).

## Why

Two runs each built an application with MoAI and the MPS MCP: run 3 (Fuhrpark, 2026-10-20) and run 4
(Rechnungsverwaltung, 2026-10-21), each about 72–74 minutes, 430–516 tool calls, 280–337 of them MCP calls.
Both hit the same problems and both wrote the same kinds of helper scripts.

| | Problem | Solved by |
| --- | --- | --- |
| Z1 | Method bodies with domain logic: the Java parser knows no MoWare constructs | Text → ObjectFlow |
| Z2 | Existing knowledge (docu tables, `get_concept_details`, `dryRun`, `mps_dump.py`) was not found | skills (done); generic builder |
| Z3 | Patterns spanning several levels (precondition with message, service method with validation, command with pages) | builder + pattern layer |
| Z4 | Setting references stably | skills (done: references by name); builder applies the rule |
| Z5 | Behaviour changes with the version (node factories set unexpected defaults where the blueprint leaves a value out, add imports; verified 2026-10-21: a value set in the blueprint is kept) | target/actual comparison; export comparison |
| Z6 | Environment and setup (config templates, copying across models) | root copy; config scaffold |
| Z7 | Context consumption (dumps and check reports of 20–40 KB) | `mps_dump.py` extension |
| Z8 | Convention patterns repeated in every app | scaffolds |

Skills alone do not solve Z1 and Z3: a service method stays 6–15 KB of JSON, and fixed templates cannot be combined.

## Decisions

- Tools are part of the package (`tools/`), versioned with MoAI. They are never copied into a project and write nothing into it.
- **One generic builder** built from the structure export, no hand-written building blocks per concept.
- **Method bodies:** Java-like text with markers, converted to ObjectFlow nodes. The marker set of run 4 is the starting point.
- **References by name**, persistent only for the exceptions in `moai:mps-node-editing` (Critical Directives).
- **The pattern layer stays permanently**, together with builder and scaffolds, even if the MCP improves.
- **The structure export is a maintainer step** before each release ([RELEASE.md](RELEASE.md), to be written in stage 1).
- The scripts of runs 3 and 4 (`mjfuhrpark/example_tooling/`, `rechnung/example_tooling/`) are studied, not reused.
- **Maintenance project:** `mjfuhrpark2`, an MPS project with an editable solution using the DevKit `org.modellwerkstatt.MoWareWerkbank`; used for the export, tool tests and `mps-dsl-memory`.
- No intermediate measurement run. The tooling is accepted together once it is complete.

## Runtime rules for all tools

- Python standard library, offline, called with `python3 -I`; each tool sets `sys.dont_write_bytecode = True`, so no `__pycache__` appears in `moai/` (a submodule in projects).
- Input and output as files in the system temp directory, which the MCP tools read; no state in the working directory.
- No references of an application project.
- Each tool states the language version it is checked against; the builder reads it from the export.
- A tool aborts with the location instead of silently producing something wrong.

## Stage 1 – Basis

**Structure export** (maintainer, with MPS and MCP)
- Query `mps_mcp_get_concept_details` with `detail: "full"` for all involved languages: ObjectFlow, ManMap, DataUX, BaseLanguage, collections, closures and the languages they inherit from (e.g. `jetbrains.mps.lang.core`).
- Store per concept: name, abstractness, super-concept and super-interfaces; properties with type and enum values; references and children with target concept and cardinality.
- Compute the concept hierarchy across languages, so that "does concept X fit role Y" is decidable offline.
- Record the language version (MPS, MoWare, module versions).
- Output the difference to the previous export: new, changed and removed concepts and roles.
- **Done (2026-10-21):** `maintenance/export/structure_export.py` (normalize, missing, diff), steps in [RELEASE.md](RELEASE.md). Output in `tools/data/structure/`, one file per language plus `version.json`, about 840 KB. The closure from the six start languages adds `lang.core`, `lang.text`, `lang.traceable` and `execution.util` (10 languages, 1011 concepts). Role lists include inherited roles.

**Generic builder**
- Builds any node of any exported language from concept name, roles and values, without concept-specific code.
- Checks while building: role exists, cardinality fits, mandatory roles present, no abstract concept, enum value valid, concept fits the role's target concept by hierarchy.
- Handles FQ names, list nesting and omits empty roles.
- Sets references by name where unambiguous, otherwise persistent.
- Provides persistent refs for frequently used Java stubs of the runtime modules, generated with the export.
- **Done (2026-10-21), without stub refs:** `tools/blueprint.py` with `find`, `concept`, `build`, `check`. Missing mandatory roles are warnings, since node factories may fill them. All shipped skill blueprints pass `check --placeholders`. Smoke test in `mjfuhrpark2` passed: entity with status, business property (`ADD CHILD`) and persistence description with by-name references; dry-run ok, `stillBroken` 0, model check clean, factory effects as documented. Still open: stub refs (with Text → ObjectFlow in stage 2).

**Target/actual comparison**
- After every insert or `SET CHILD`, compares the inserted node with the blueprint: do all set properties and references keep their value? Reports deviations with location and both values.
- Checks new model imports against the module dependencies.
- Needs no knowledge of individual factories.
- **Done (2026-10-21), node part:** `tools/verify.py node BLUEPRINT ACTUAL` (ACTUAL = `print_node` deep of the inserted node, right after the write). Deviations: changed or unstored values (defaults excepted), unresolved or other references, other child count or concept in a named role. "Added": everything only MPS set. Tested in `mjfuhrpark2`: found `DateLiteral.fromServer=true` set by the factory, an unresolved by-name reference, factory-added `id` and `OPTIMISTIC_LOCK`.
- **Open:** model imports vs module dependencies. The project-structure dump does not name the module of an imported model, so this needs one more MCP query per import; until then the manual check in `mps-node-editing` (Node factories) applies.

**`mps_dump.py` extension**
- In addition to `roots`, `models`, `node`, `tree`, `shape`: read blueprints; condense check reports, grouped by root and kind of error; list intentionally unresolved places (marker code before conversion) separately; search dumps by concept, name or reference.
- **Done (2026-10-21) as `tools/dump.py`**, which imports `mps_dump.py` as a library. `mps_dump.py` is a JetBrains file and stays unchanged in `skills/mps-mcp-workflow/scripts/`, so a JetBrains update is a plain copy. Commands: `problems` (any check-report form, one line per problem plus a count per message; 47 KB full-tree report → 5 lines), `bp` (blueprint as tree), `grep` (by concept, name, reference, `--unresolved`). Marker places come with Text → ObjectFlow in stage 2.

**Root copy**
- Turns a root from a dump into an insertable blueprint with references by name, so they resolve in the target model.
- Select parts (e.g. config sections), rename, replace text (e.g. `firma.app` → package name), omit default properties.
- Reports which references will probably not resolve in the target.
- **Done (2026-10-21):** `tools/copyroot.py DUMP... [--replace OLD=NEW] [--drop NAME] [--keep-defaults]`. References into copied nodes become names, references to other models stay persistent (reported as "import needed"), references into the source model outside the copy are reported as "will not resolve". Tested in `mjfuhrpark2`: wbkit `baseconfig` + `Test` with `firma.app` replaced and `LocalDB_Oracle` dropped (52 KB, inserted as file): `stillBroken` 0, model check clean, target/actual comparison of `Test` 0 deviations.

**Skill and template changes in stage 1**

| Where | Change |
| --- | --- |
| `TEMPLATE_PROJECT_AGENTS.md`, new section "Tools" | MoAI ships tools in `moai/tools/`; use them first, do not rebuild them; input and output only in the temp directory |
| DSL skills, `mps-node-editing` | builder as the standard way to write blueprints (quick start) |
| `mps-node-editing`, DSL skills | target/actual comparison replaces the manual `print_node` check after an insert |
| skills that produce large dumps or check reports | name the `mps_dump.py` or `tools/dump.py` call where the output is produced |
| `objectflow-dsl` (workflow OFXConfig) | root copy for the wbkit templates |
| `INSTALL_INSTRUCTIONS.md` (step 3) | check that `python3` is available |
| `readme.md` | `tools/` in the contents |
| `maintenance/RELEASE.md` (new) | release steps: export, export comparison, update skills and patterns |

**Stage 1 done (2026-10-21).** All rows above are in place. Deferred: stub refs in the builder (stage 2, with Text → ObjectFlow) and the check of model imports against module dependencies (manual check in `mps-node-editing` until a real case needs the tool).

## Stage 2 – Patterns and method bodies

**Pattern layer**
- Short forms for patterns spanning several levels, built with the generic builder. Examples: precondition with message; service method with rules; command with pages and conclusions; custom SQL as text with marked variables and status constants; test method with expected exception.
- Selection by rule, not by finding: every construct whose mandatory roles themselves require concept-specific nodes gets a pattern. The export determines this.
- Generates the blueprints shown in the skills and replaces today's fixed blueprints with placeholders.

**Text → ObjectFlow**
- Accepts method bodies as Java-like text with markers. Expressible must be every concept that fits statement and expression roles according to the export.
- Converts the parser output via the generic builder into one blueprint per member and sets the kind of method (normal, service, repository with type).
- Preserves identity: constructors and test methods are replaced only through their body.
- Aborts with the location on unknown markers, unresolved identifiers and ambiguous bindings.

Starting point for the markers (run 4):

| Java text | ObjectFlow result |
| --- | --- |
| `betrag`, `x.betrag` | business property reference |
| `List<T>`, `new ArrayList<T>()`, `.where(..)`, `.size()` | `list<T>`, `new arraylist<T>`, collections operations |
| `BD("1.50")`, `SERVERDATE()`, `SERVERDATETIME()`, `DATE(y,m,d)` | `1.50bd`, server date/time, fixed date |
| `STATUS("Decl","ELEM")`, `OF(expr,"A","B")` | `Decl.ELEM`, `expr of A, B` |
| `PRE(cond,"fmt",args)`, `PREW(..)` | `precondition` (`WARNING_HINT`) |
| `if (VALIDATION()) { … }` | `validation { … }` |
| `GUARD(cond,"fmt",args)` | `guard` |
| `CALL("Comp","m",args)`, `CALL_WITH(sess,"Comp","m",args)` | `# Comp.m(..)`, `#+ with sess Comp.m(..)` |
| `SESSION_OP("Comp","m","Text",args)` | `session operation add # Comp.m(..) // 'Text'` |
| `FAIL_IN("Ex"[, "text"]);` | `FAIL IN Ex` on the following statement |

**Skill changes in stage 2**

| Where | Change |
| --- | --- |
| `references/blueprints/` and `blueprints.md` of all DSL skills | generated patterns replace the fixed blueprints |
| `objectflow-dsl`, `mps-baselanguage` | workflow for method bodies: skeleton → text with markers → Text → ObjectFlow → `SET CHILD` per member → target/actual comparison; the path "bodies as JSON" is removed |
| `objectflow-dsl` | marker convention: per marker the target construct, an example and limits |

## Stage 3 – Scaffolds

- Generate convention-compliant skeletons from a small specification in one bulk insert: aggregate; search; owner and edit commands; status transition; configs for test and FX8.
- The conventions live in the generator. Deviations of a project (`AGENTS.md`) can be expressed in the specification.

**Skill changes in stage 3:** the workflows "Create a command", search, owner/edit and config in `objectflow-dsl` and `dataux-dsl` point to the scaffolds.

Changes to the `mps-*` skills are recorded in [MPS_SKILLS_CHANGES.md](MPS_SKILLS_CHANGES.md).

## Quality assurance

- Export comparison before each release: structural differences are checked before skills and patterns are released.
- Smoke test in `mjfuhrpark2`: insert patterns, target/actual comparison, build.
- Golden tests for pattern layer and Text → ObjectFlow, with fixtures from runs 3 and 4 and from `org.modellwerkstatt.dataux.tests`.

## Acceptance

Together, once the tooling is complete. A new run rebuilds the domain of runs 3 and 4 (Fahrzeug and Lenker, Rechnung with positions). It learns no concept shapes from dumps, rebuilds no shipped tool and writes no hand JSON for method bodies; all tests are green. MCP calls and duration are compared with runs 3 and 4.

## Open questions

- **`sampleNode`** of `get_concept_details` is a one-level placeholder and no pattern.
- **Markers:** check before fixing them whether they cover all constructs allowed in bodies and are unambiguous for agents.
- **Limit of resolution by name:** when property chains get too long is observed, not measured.
- **Scaffolds and conventions:** if deviations cannot be expressed, agents bypass the generator.
