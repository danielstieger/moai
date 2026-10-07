# JSON AST Workflow for BaseLanguage

Use this workflow when authoring non-trivial BaseLanguage code via JSON blueprints (rather than the Java parser). It is the right path when:

* The parser is unavailable.
* The code uses BaseLanguage extensions (`jetbrains.mps.lang.smodel`, `jetbrains.mps.baseLanguage.closures`, `jetbrains.mps.baseLanguage.collections`).
* You need stable persistent references to members.

## Core Principles

* **Stage large roots**: don't insert a full complex root at once; use a staged approach (Skeleton → Members → Bodies).
* **Reference stability**: references (especially `baseMethodDeclaration`) are fragile. Use persistent refs (`r:...`) instead of names for stable wiring.
* **Validation gates**: always use `dryRun` (structure), `mps_mcp_check_root_node_problems` (semantics), and `MAKE` (generation/compilation).
* **Generated Java as signal**: if `MAKE` fails, check the generated Java for hints (`new ()` or `???()`).

## Recommended Workflow

1. **Context**: load `moai:mps-node-editing` and the `moai:mps-baselanguage` references on concept-mapping + critical-rules.
2. **Setup**: resolve/create the target module/model and verify dependencies.
3. **Skeleton**:
    * Insert the root with signatures, fields and empty bodies (`mps_mcp_insert_root_node_from_json`, or `mps_mcp_create_root_node` + `mps_mcp_update_root_node_from_json` once).
4. **Harvest References**:
    * **Own members**: use `mps_mcp_print_node` on the skeleton to get persistent refs for constructors and methods.
    * **External members**: derive refs from the class ref using URL-encoded signatures (`stub-references.md`).
    * **Inherited methods**: use the declaring class ref for `baseMethodDeclaration`.
    * **Ambiguity**: use `GET_ASSIGNABLE_REFERENCES` (mode: `completion`) for overloaded/inherited members if name auto-resolution fails.
5. **Patch & Apply**:
    * Replace placeholder targets in your member blueprints with the harvested/derived persistent refs (especially for `ClassCreator` and `InstanceMethodCallOperation`).
    * Apply member by member with `mps_mcp_update_node` (`ADD`/`SET` × `CHILD`). Never re-run `mps_mcp_update_root_node_from_json` after harvesting — it re-creates all children and invalidates the harvested refs (`moai:mps-node-editing`, `references/staged-construction.md`).
6. **Final Validation**: `dryRun` → `mps_mcp_check_root_node_problems` → `MAKE`.

## Reference Rules

* `ClassCreator.baseMethodDeclaration`: points to a **constructor**, not the class.
* `InstanceMethodCallOperation.baseMethodDeclaration`: points to the **method declaration**.
* **Stale refs**: a full-root rewrite (`mps_mcp_update_root_node_from_json`) re-creates all children; re-harvest afterwards.

## Practical Authoring Tips

* Use fully qualified concept names in JSON.
* Keep helper JSON-generation scripts outside the model.
* If only one subtree changes, prefer `mps_mcp_update_node` over a full root rewrite to reduce reference churn.
* Harvest refs from live AST with `mps_mcp_print_node` for own-class members; member identities do not survive a full-root rewrite.
* For library stubs, derive persistent refs from the class ref using the URL-encoded signature formula; do not print stubs to harvest refs that can be computed.

## Checklist

* [ ] Model and placeholder roots exist.
* [ ] Skeleton applies and validates.
* [ ] Member references are harvested (own) or derived (external).
* [ ] Final JSON is patched with persistent refs.
* [ ] `MAKE` succeeds and generated Java looks correct.
