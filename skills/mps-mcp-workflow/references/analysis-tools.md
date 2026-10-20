# Analyzing MPS Code and Languages

**Read tools inline small results.** `mps_mcp_print_node`, `mps_mcp_get_project_structure`, `mps_mcp_get_concept_details`, `mps_mcp_search_concepts`, `mps_mcp_query_nodes`, `mps_mcp_query_types`, `mps_mcp_check_root_node_problems` and `mps_mcp_list_node_intentions` return `data` inline when it is at most `maxInlineBytes` (default 20000) and a temp-file path only above that — do not assume `data` is a path. When it *is* a path, the file holds the complete `{"ok":…,"data":…}` envelope: read the payload from its `data` field.

- Use `mps_mcp_print_node` for the structural JSON form or for a textual or HTML projection. To verify a whole root, one call with `deep=true` (JSON) or `format: "PLAIN TEXT"` (projection) beats walking its children.
- Use `mps_mcp_check_root_node_problems` to find errors in the code — on a node, a root, a model or a module (below).
- Use `mps_mcp_list_node_intentions` / `mps_mcp_apply_intention` to discover and apply the node's Alt+Enter actions (intentions and quick-fixes) headlessly (below).
- Use `mps_mcp_query_nodes` for node search and navigation (FIND_INSTANCES, FIND_USAGES, GET_PARENT, GET_ROOT, GET_MODEL_FOR_NODE, NODE_INDEX, SIBLINGS, GET_CHILD_ROLE, GET_TYPE, GET_EXPECTED_TYPE). FIND_INSTANCES finds nodes of a concept (see below); FIND_USAGES finds nodes whose references point at a given node; GET_TYPE reads a node's type and GET_EXPECTED_TYPE the type its context requires.
- Use `mps_mcp_query_types` to let the typesystem engine decide type questions instead of reading rules (table below, details in [`type-queries.md`](type-queries.md)).
- Use `mps_mcp_query_structure` to investigate the relationships between concepts and their assignability.
- Use `mps_mcp_alter_nodes` (`FIX_REFERENCES`) to repair broken or mispointed references in a node and all its descendants. Typical situations where this helps:
    - After moving or copying nodes across models or modules, references to nodes in the original location may break.
    - After refactoring a BaseLanguage method signature, `overrides` references in subclasses may point to the wrong overload ("Reference to wrong overridden method") — FIX_REFERENCES corrects this generically without any language-specific logic.
    - After bulk-inserting nodes from JSON where some reference targets could not be found at insertion time.
    - Whenever `mps_mcp_check_root_node_problems` reports unresolved or wrong reference errors and the target nodes actually exist in the project.
    - Run FIX_REFERENCES before concluding that a reference error is genuinely unresolvable.

## `mps_mcp_query_nodes` (`FIND_INSTANCES`) — Finding Nodes of a Concept

Returns all nodes that are instances of the specified concepts (or one random sample) as a JSON array of node info objects (non-root entries include `rootName`), inline up to `maxInlineBytes` (a top-level parameter of `mps_mcp_query_nodes`), otherwise a temp-file path. **One call per concept is never necessary:** `conceptRefs` takes several concepts and scans once, and `detail: "count"` answers `[{concept, conceptReference, count}]`, one row per requested concept in request order (rows overlap for superconcepts unless `exact: true`).

Parameters:
```
{
  "conceptRef": "Persistent reference of the concept (SAbstractConcept) or fully qualified concept name",
  "conceptRefs": "Alternative to conceptRef for several concepts: one reference or a JSON array. Not together with conceptRef.",
  "detail": "Optional: 'nodes' (default) or 'count'.",
  "rootsOnly": "Boolean (optional, default: false). Matches only root nodes; combinable with any scope or detail.",
  "scope": "Optional: 'all', 'editable' (default), 'models', 'modules', 'roots'",
  "models": "Optional: list of persistent model references (required if scope is 'models')",
  "modules": "Optional: list of persistent module references (required if scope is 'modules')",
  "roots": "Optional: list of root node references (required if scope is 'roots'). Restricts the search to nodes within the specified roots.",
  "propertyFilter": "Optional: {\"name\": \"<propertyName>\", \"value\": \"<expectedValue>\"} — only nodes whose property equals the value (e.g. find a literal by its value).",
  "exact": "Boolean (optional, default: false). Whether to exclude instances of subconcepts.",
  "sampleOnly": "Boolean (optional, default: false). If true, returns a single random sample instance to illustrate usage and JSON structure."
}
```

Explicit `models`, `modules` and `roots` selectors are all-or-error: every reference must resolve, or the whole search is rejected with INVALID_REQUEST naming it — a search never narrows silently to the resolvable subset. An unresolvable `conceptRefs` entry is `NOT_FOUND`.

## `mps_mcp_print_node` — Output Format

`format` accepts exactly `JSON` (default), `HTML` and `PLAIN TEXT` — with a **space**; `PLAIN_TEXT` and `text` are rejected. `nodeReference` must be a node reference; a model reference is rejected (use `mps_mcp_get_project_structure`). `data` is inline up to `maxInlineBytes` and a temp-file path above that. The default is **shallow**. Behaviour depends on `deep`:

- `deep=true` recursively inlines all descendants.
- `deep=false` (shallow) lists properties, children roles with references, and reference roles.

A saved file contains the full MCP response envelope; its `data` field contains the node JSON object shown below. **JSON mutation tools accept either that full envelope file or a file containing only the raw `data` object** — see `moai:mps-node-editing` (File-Path Semantics and `references/json-format.md`).

```
{
  "name": "NodeName",
  "concept": "ShortConceptName",                    // FQN = suffix of conceptReference; use the FQN as `concept` in blueprints
  "conceptReference": "PersistentConceptReference",  // informational; optional in blueprints
  "reference": "PersistentNodeReference",
  "properties": [
    { "name": "propertyName", "type": "propertyType", "value": "propertyValue" }
  ],
  "references": [
    { "role": "linkRole", "type": "roleConcept", "typeReference": "PersistentRoleConceptReference",
      "cardinality": "0..1|1", "target": "TargetNodeName",
      "targetReference": "PersistentTargetReference" }
  ],
  "children": [
    { "role": "linkRole", "type": "roleConcept",
      "typeReference": "PersistentRoleConceptReference",
      "cardinality": "0..1|1|0..n|1..n",
      "children": [ /* if deep=false */
        { "name": "ChildNodeName", "reference": "..." }
      ],
      "nodes": [ /* if deep=true */
        { "name": "ChildNodeName", "concept": "...", "conceptReference": "...",
          "reference": "...", "properties": [...], "references": [...], "children": [...] }
      ]
    }
  ]
}
```

- **Default values are invisible.** MPS stores nothing for a property at its default, so it is omitted from `properties` — except an enum property at its enumeration's default, printed with the default literal and `"isDefault": true` (`mps_mcp_get_concept_details` names it `enumerationDefault`). Read an absent property or a report's `"value": ""` as "holds its default", never as missing, and never copy a `""` enum value into a blueprint.
- **Enum values are the declared literal name** (e.g. `ML`), never the persistence encoding `<id>/<name>`.
- **`"declared": false`** marks a stored property, child role or reference the node's concept does not declare (stale runtime, removed role); `"conceptLoaded": false` marks a node whose concept is not loaded. Its content is still there — never report such a node as empty. The blueprint tools do not re-apply these entries (`moai:mps-node-editing`, `references/json-format.md`).
- **`PLAIN TEXT` renders an empty collection as its placeholder cell** (`<< ... >>`); take counts from the JSON form.

## `mps_mcp_check_root_node_problems` — Output Format

Validates the specified node (and its descendants), model, or module. Pass any of them in `nodeReference` — a node reference, a model reference or qualified model name, a module reference or module name. If no problems are found, returns `data: "no problems found"`; when unchecked subtrees exist, `data` reads `no problems found in checked nodes (N subtree(s) unchecked: …)`. Otherwise the report is inline up to `maxInlineBytes` and a temp-file path above that. It reports *problems*, not content: to verify what a root contains, print it.

- **Model reference:** checks the model itself (imports, used languages, devkits) and every root in one exhaustive call — `details.scope: "model"`, `details.rootsChecked`. Problems come as the model object plus a `roots` array, one entry per offending root. `perRoot=true` returns `[{root, name, concept, errors, warnings}]` for every root, clean ones included. Do **not** re-check the roots individually after a clean model-level result.
- **Module reference or name:** the module (dependencies, used languages) and every model it owns; `details.modelsChecked`, `rootsChecked`; `perRoot=true` gives one row per model. Module-level warnings in `details.moduleProblems` do not make the answer unclean.
- **When to use which:** the changed root after a single edit; the model reference with `perRoot=true` after work on several roots.

- `onlyNodesWithProblems=true` (default) returns a flat list of just the nodes that have problems — easier to skim.
- `onlyNodesWithProblems=false` returns the full subtree with `problems` arrays attached to each node, property, reference, and child role; useful when sibling context matters.

Besides the standard structure/constraints/typesystem checkers, the check also decodes the encoded feature ids stored on attribute nodes — `PropertyAttribute.propertyId` (used by `PropertyMacro`) and `LinkAttribute.linkId` (used by `ReferenceMacro`) — and reports a malformed, blank, or non-resolving id as a structure-level error on the offending macro. This catches the common mistake of pasting a node reference, a short id, or a bare property name into `propertyId`, which the write path accepts silently and which otherwise only fails at generation time as an opaque "an error occurred". Run a check after attaching or editing any `PropertyMacro`/`ReferenceMacro`.

- `autoApplyQuickFixes=true` (node/root references only; ignored with a warning on a model) applies, for every problem carrying exactly one auto-applicable quick-fix, that fix before returning the final report (`details.appliedQuickFixes`, `details.failedQuickFixes`). One round — call again if the fresh report still shows auto-applicable fixes.
- Each `problems[]` entry may carry **`quickFixes`** `[{id, description, autoApplicable}]`; apply one with `mps_mcp_apply_intention(nodeReference = <the problem node>, intentionId = <id>)`.
- A typesystem, constraints or scope problem may carry **`rules`** `[{rule, ruleReference, statement}]`: the first entry names the reporting rule — cite it instead of guessing; print `ruleReference` only to read the rule. A problem about a property or reference sits in that `properties[]` / `references[]` entry.
- **Commented-out code is not type- or constraints-checked.** Such subtrees are counted in `details.uncheckedSubtrees` (and `uncheckedSubtrees` per root / `perRoot` row), and a clean verdict over them adds a `warnings` entry. A clean verdict over commented-out code proves nothing — ask `mps_mcp_query_types` `IS_SUBTYPE`.

Each entry has the shape:

```
{
  "name": "NodeName",
  "reference": "PersistentNodeReference",
  "concept": "ConceptName",
  "conceptReference": "PersistentConceptReference",
  "problems": [
    { "severity": "error|warning|info", "message": "...",
      "quickFixes": [ { "id": "…_QuickFix", "description": "…|null", "autoApplicable": false } ],
      "rules": [ { "rule": "…", "ruleReference": "PersistentRootReference", "statement": "PersistentNodeReference" } ] }
  ],
  "properties": [
    { "name": "propertyName", "type": "propertyType", "value": "propertyValue",
      "problems": [ { "severity": "error|warning|info", "message": "..." } ] }
  ],
  "references": [
    { "role": "linkRole", "type": "targetConcept",
      "typeReference": "PersistentConceptReference",
      "cardinality": "0..1|1",
      "target": "TargetNodeName", "targetReference": "PersistentTargetReference",
      "problems": [ { "severity": "error|warning|info", "message": "..." } ] }
  ],
  "children": [
    { "role": "linkRole", "type": "targetConcept",
      "typeReference": "PersistentConceptReference",
      "cardinality": "0..1|1|0..n|1..n",
      "problems": [ { "severity": "error|warning|info", "message": "..." } ],
      "nodes": [
        { "name": "...", "reference": "...", "concept": "...", "conceptReference": "...",
          "problems": [...], "properties": [...], "references": [...], "children": [...] }
      ]
    }
  ]
}
```

## Intentions & quick-fixes

Two tools bring the editor's Alt+Enter actions to a node without opening an editor:

- `mps_mcp_list_node_intentions(nodeReference, includeAncestors=true, includeDisabled=false, includeQuickFixes=true)` lists entries `{type: "intention"|"quickFix", id, kind, description, targetNode, declarationNode, parameterized?, problemMessage?, autoApplicable?}`.
- `mps_mcp_apply_intention(nodeReference, intentionId, description=null, problemMessage=null)` applies one entry in an undoable command: `nodeReference` = the entry's `targetNode` (for a check-report fix, the problem node), `intentionId` = its `id`; `description` / `problemMessage` disambiguate several instances. It returns `{applied, type, description, targetNode, problems:{before, after}}`. The action may write outside the target model; only the target model is saved automatically.

Typical loop: `mps_mcp_check_root_node_problems` → a `quickFixes` id → `mps_mcp_apply_intention` → re-check.

## Type queries

| question | call |
|---|---|
| type of this node | `mps_mcp_query_nodes` `GET_TYPE` `{nodeReference}` |
| type this node must have here | `mps_mcp_query_nodes` `GET_EXPECTED_TYPE` `{nodeReference}` |
| does A fit where B is required | `mps_mcp_query_types` `IS_SUBTYPE` `{sub, super}` |
| what can A be widened to | `SUPERTYPES` `{type}` |
| what do A and B have in common | `COMMON_SUPERTYPE` `{types:[A, B]}` |
| view A as a given type concept | `COERCE` `{type, conceptRef}` |
| what does `a op b` give | `OPERATION_TYPE` `{operatorNode or operatorConceptRef, left, right}` |
| why does this node have its type | `EXPLAIN_TYPE` `{nodeReference}` |

Operand forms, outputs and the meanings of `null`: [`type-queries.md`](type-queries.md).

## Workflow and Best Practices

1.  **Navigate with precision**: prefer using `startingPoint` and `reference` (ID) over names to avoid ambiguity.
2.  **Respect the AST**: remember that you are editing a tree. When writing Java (`BaseLanguage`), use `ParenthesizedExpression` if you are unsure about operation priorities in the tree structure.
3.  **Learn from samples**: study existing code to understand how to perform common tasks. Use `mps_mcp_query_nodes` (`FIND_INSTANCES`) to find existing nodes of a given concept.
4.  **Defensive problem checking**: always use `mps_mcp_check_root_node_problems` immediately after inserting or modifying a complex node. A successful insertion `"ok": true` does not guarantee the resulting AST is semantically or structurally valid.
5.  **Validate frequently**: make/rebuild languages with `mps_mcp_alter_nodes` (`MAKE`) after making changes so they can be imported and used, and so you see whether they generate and compile. Pass `MAKE` with a JSON parameters object that names what to build — `{"modules": ["<module-ref>"]}` for one or more modules (e.g. a language plus its generator), `{"models": ["<model-ref>"]}` to make individual models, or `{"wholeProject": true}` to rebuild everything. Generation and compile errors appear in the `MAKE` result; `mps_mcp_check_root_node_problems` reports model-level problems per root and does not surface generator output, so run it on the changed roots (or the model, `perRoot=true`) before the make. After a MAKE or generation that reports success but lacks its effect, read the IDE log ([`ide-log.md`](ide-log.md)).
