# What Changes When the MPS MCP Can More

For MoAI maintainers. Agents working in an application project do not need this file.

Several tools and skill rules only bridge gaps of the JetBrains MPS MCP (see [TOOLING.md](TOOLING.md)).
Check this list against each new MPS / MCP version.

| When the MCP can … | Remove or change | Skills / files to adapt |
| --- | --- | --- |
| **Parse in the scope of the target position** (identifiers, types and calls resolved as the editor would, including language extensions: business properties, collections, literals, status, preconditions; stubs from the module dependencies) | Remove Text → ObjectFlow and the marker convention; remove the stub refs in the builder | `objectflow-dsl`, `mps-baselanguage`: method bodies become one parser call |
| **Report factory effects on insert** (properties, references, children and model imports set or changed by node factories) | Remove the target/actual comparison | `mps-node-editing`, DSL skills: check after insert; "Node factories" in the DSL `gotchas.md` shrink |
| **Run factories in `dryRun`** | Target/actual comparison before insert no longer needed | – |
| **Return a map name → reference** of the new nodes on insert | Remove any remaining reading of refs after insert | `mps-node-editing` (reference rule, `staged-construction.md` "Read child refs") |
| **Copy across models** (`COPY_NODE` with a target model, references re-resolved in the target) | Remove root copy | `objectflow-dsl` (workflow OFXConfig): one call |
| **Give compact, filtered output** (`print_node` with depth, role filter, projection; `responseDetail: summary` for parser, insert and check reports) | Reduce `mps_dump.py` to what is still needed | skills that mention `mps_dump.py` |
| **Export structure in one call** (several languages including inherited ones, with hierarchy) | Simplify the structure export | `RELEASE.md` |
| **Set VM options and environment variables** in run configurations | – | `mps-run-configurations`: no manual step for `--enable-native-access=ALL-UNNAMED` (conventions `allgemein`) |
| **Detect and report modal dialogs** instead of timing out | – | `INSTALL_INSTRUCTIONS.md`, `mps-mcp-workflow`: VCS dialog hints |
| **Resolve names the same way on ADD and DELETE** of model imports | – | `mps-mcp-workflow/references/module-dependencies.md` |

## Stays in any case

The generic builder (composing and checking offline), the example export (multi-level shapes from real instances) and
the scaffolds (conventions as a generator). Their value lies above the server.
