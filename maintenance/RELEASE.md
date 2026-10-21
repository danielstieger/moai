# Release Steps

For MoAI maintainers. Agents working in an application project do not need this file.

Run these steps before publishing a new MoAI version. They need MPS with the maintenance project
`mjfuhrpark2` open and the MPS MCP enabled; an agent session makes the MCP calls.

## 1. Structure export

The export in `tools/data/structure/` is what the builder reads offline (see [TOOLING.md](TOOLING.md)).

1. Keep the current export for the comparison: `cp -r tools/data/structure "$TMPDIR/structure-old"`.
2. For each language, call `mps_mcp_get_concept_details` with `languageRefs`, `detail: "full"` and a small
   `maxInlineBytes`, so the result lands in a temp file. Start with ObjectFlow, ManMap, DataUX, BaseLanguage,
   collections and closures.
3. Normalize all raw files at once, with the running MPS build (`mps_mcp_list_open_projects`, `mpsBuild`):

   ```bash
   python3 -I maintenance/export/structure_export.py normalize tools/data/structure <raw files> --mps-build <build>
   ```

4. If it lists missing languages, export them too and normalize again with all raw files, until it reports
   `closed`. Remove files of languages that no longer belong to the closure.
5. Compare with the previous export:

   ```bash
   python3 -I maintenance/export/structure_export.py diff "$TMPDIR/structure-old" tools/data/structure
   ```

## 2. Follow-up of the comparison

- Check every change against the skills (`concepts.md`, gotchas, blueprints), the patterns and the docu chapter maps.
- Record behaviour changes that agents must know.
- Re-run the smoke test in `mjfuhrpark2` when patterns or the builder are affected.

## 3. JetBrains skills and MCP

- New MPS / MCP version: compare the JetBrains skills against [MPS_SKILLS_CHANGES.md](MPS_SKILLS_CHANGES.md)
  and check [MCP_DEPENDENCIES.md](MCP_DEPENDENCIES.md).
