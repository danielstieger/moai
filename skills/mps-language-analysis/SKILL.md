---
name: mps-language-analysis
description: Analyze an MPS language by name — discover concepts, properties, references, children, aspects (editor/constraints/behavior), and metadata. Use when investigating an unfamiliar language, exploring concept structure, or finding sample nodes to use as templates for JSON blueprints.
---

# MPS Language Analysis

Workflow for inspecting an MPS language from a name (e.g. `jetbrains.mps.lang.core`). Returns concepts, metadata, structural info, and pointers to declarations and sample nodes.

## Critical Directives

- Use the **fully qualified** language name (e.g. `jetbrains.mps.lang.core`) — single-letter shorthand (`j.m.l.core`) requires resolution first via `mps_mcp_get_project_structure`.
- Use the returned `qualifiedName` as `concept` in JSON blueprints (`moai:mps-mcp-workflow`, `references/node-editing-rules.md`).

## Analyzing a Language by Name

1. **Verify Language**: call `mps_mcp_get_project_structure` with the language name as a filter (`startingPoint: My_Language`). This confirms existence and provides the UUID.
2. **Retrieve Concepts**: use `mps_mcp_get_concept_details` with the language name in `languageRefs`. Both `conceptRefs` and `languageRefs` accept either one value or a JSON array (real or written as a string); omit the unused selector. Pass `detail: "shape"` when you only need properties, references and children — one `languageRefs` call replaces a call per concept.
3. **Extract Data**: the response includes:
    * **Name**: concept FQN.
    * **Description**: found in `shortDescription`.
    * **Metadata**: `isRootable`, `isAbstract`, and the `conceptReference` ID.
    * **Structure**: properties, children, and references are detailed here.
4. **Drill Down**:
    * **Declaration**: use the `sourceNode` reference with `mps_mcp_open_node` to open the definition.
    * **Examples**: use `mps_mcp_query_nodes` with `FIND_INSTANCES` (`sampleOnly: true`) to get a sample node. Then use `mps_mcp_print_node` to see its canonical JSON structure for use as a template.
    * **Inheritance**: use `mps_mcp_query_structure` (`GET_ALL_SUPERCONCEPTS`, `GET_SUB_CONCEPTS`, `IS_SUBCONCEPT_OF`) for hierarchy analysis.

## Inspecting Concept Aspects

Use `mps_mcp_query_structure` with `LIST_CONCEPT_ASPECTS` to find associated definitions (editor, constraints, behavior, typesystem rules, node factories in `actions`):

* **`relation`**: `appliesTo` marks a root that is *for* the concept (its editor, a rule or node factory applicable to it); `mentions` a root that only references it. `pattern: true` marks a rule that matches the concept through a pattern, so only instances of that shape. Read `relation` before concluding a concept has an editor or factory: `targetsConcept` alone includes mentioning roots.
* **Inherited Aspects**: set `includeInherited: true` to add the aspects of ancestors (superconcepts/interfaces); `targetsConcept` says which concept each root was found through.
* **Node factories**: an `actions` root with `relation: appliesTo` means inserted nodes get more than the blueprint says (`moai:mps-node-editing`, "Node factories").
* **Editor Analysis**:
    * **ConceptEditorDeclaration**: with `relation: appliesTo`, the full editor for the `targetsConcept`.
    * **EditorComponentDeclaration**: defines reusable presentation pieces.
    * Check the `editor` model in the response to identify available editors.

## Answering Type Questions

Let the typesystem engine answer instead of reading rule roots: a node's type → `mps_mcp_query_nodes` `GET_TYPE`; the type its context requires → `GET_EXPECTED_TYPE`; does A fit B → `mps_mcp_query_types` `IS_SUBTYPE`; what A and B share → `COMMON_SUPERTYPE`; the type of `a op b` → `OPERATION_TYPE`; why a node has its type → `EXPLAIN_TYPE`. Operand forms and outputs: `moai:mps-mcp-workflow` (`references/type-queries.md`).

## Related Skills

- **`moai:mps-mcp-workflow`** — `references/finding-things.md` for resolving model, module, and language names before analysis.
- **`moai:mps-node-editing`** — creating or editing nodes once the concepts are understood.

## Reference Index

- Open `references/search-concepts.md` for the `mps_mcp_search_concepts` matching algorithm — haystack composition, subtoken splitting, fallback ranking, the three scopes (`modelReference` / `scope`) and the automatic widening, the `detail` projections, the 50-match cap, and the sub-2-char failure mode.
- Open `references/concept-details.md` for the `mps_mcp_get_concept_details` result schema, `detail: "shape"`, inline vs. file results, enumerations, and the unresolved-ref policy (all-failed vs partial-success envelopes and the suggestion heuristic).
