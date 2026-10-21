# JSON AST Workflow for BaseLanguage

Use this workflow when authoring non-trivial BaseLanguage code via JSON blueprints (rather than the Java parser). It is the right path when:

* The parser is unavailable.
* The code uses BaseLanguage extensions (`jetbrains.mps.lang.smodel`, `jetbrains.mps.baseLanguage.closures`, `jetbrains.mps.baseLanguage.collections`).
* You need stable persistent references to members.

## Core Principles

* **Stage large roots** (skeleton → fill): `moai:mps-node-editing` (`references/staged-construction.md`).
* **References**: by name; exceptions (stubs, overloads, …) and repair order in `moai:mps-node-editing` (Critical Directives).
* **Validation gates**: always use `dryRun` (structure), `mps_mcp_check_root_node_problems` (semantics), and `MAKE` (generation/compilation).
* **Generated Java as signal**: if `MAKE` fails, check the generated Java for hints (`new ()` or `???()`).

## Recommended Workflow

1. **Context**: load `moai:mps-node-editing` and the `moai:mps-baselanguage` references on concept-mapping + critical-rules.
2. **Setup**: resolve/create the target module/model and verify dependencies.
3. **Skeleton**:
    * Insert the root with signatures, fields and empty bodies (`mps_mcp_insert_root_node_from_json`, or `mps_mcp_create_root_node` + `mps_mcp_update_root_node_from_json` once).
4. **Set References**:
    * **Own members**: by name.
    * **External members**: derive refs from the class ref using URL-encoded signatures (`stub-references.md`).
    * **Inherited methods**: use the declaring class ref for `baseMethodDeclaration`.
    * **Overloads**: persistent ref; use `GET_ASSIGNABLE_REFERENCES` (mode: `completion`) to find it.
5. **Apply**:
    * Apply member by member with `mps_mcp_update_node` (`ADD`/`SET` × `CHILD`); replace constructors and test methods only through their `body` (`moai:mps-node-editing`, Critical Directives). Never re-run `mps_mcp_update_root_node_from_json` on a filled root — it re-creates all children with new IDs (`moai:mps-node-editing`, `references/staged-construction.md`).
6. **Final Validation**: `dryRun` → `mps_mcp_check_root_node_problems` → `MAKE`.

## Reference Rules

* `ClassCreator.baseMethodDeclaration`: points to a **constructor**, not the class.
* `InstanceMethodCallOperation.baseMethodDeclaration`: points to the **method declaration**.
* **Stale refs**: a full-root rewrite (`mps_mcp_update_root_node_from_json`) or a `SET CHILD` re-creates the replaced nodes with new IDs; by-name refs resolve again, persistent refs to them break.

## Practical Authoring Tips

* Keep helper JSON-generation scripts outside the model.
* If only one subtree changes, prefer `mps_mcp_update_node` over a full root rewrite to reduce reference churn.
* For library stubs, derive persistent refs from the class ref using the URL-encoded signature formula; do not print stubs to find refs that can be computed.

## Checklist

* [ ] Model and placeholder roots exist.
* [ ] Skeleton applies and validates.
* [ ] Own member references set by name; stub refs derived; overloads persistent.
* [ ] `fixReferences.stillBroken` is 0.
* [ ] `MAKE` succeeds and generated Java looks correct.
