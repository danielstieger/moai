# ObjectFlow workflows

## Create a domain structure

1. Decide Entity vs Value Object vs DTO from identity, immutability, and use-case scope. [Decision semantics](../../../docu/objectflow.md#entity-value-object-und-dto)
2. Insert the matching root skeleton from [blueprints.md](blueprints.md).
3. Add Business Properties with `mps_mcp_update_node` (`ADD CHILD`, role `businessProperties`). Use the verified property subtree as a starting point.
4. Choose only supported property types and add ObjectFlow/ManMap options deliberately. [Property types and options](../../../docu/objectflow.md#business-properties)
5. For Value Objects, add `equalProperties` only for components that define value equality. Treat instances immutably. [Value Object equality](../../../docu/objectflow.md#value-object-gleichheit)
6. Add status declarations under the structure's `status` role, not as roots. Ensure every element has technical value plus short/long descriptions. [Status](../../../docu/objectflow.md#status)
7. Validate the root and generate/build if the target project workflow requires it.

For Entity references, distinguish the key from the loaded object. `#Key` does not load; direct property access requires the reference join to have loaded the target. [Relationships and object graphs](../../../docu/objectflow.md#beziehungen-und-objektgraphen)

## Add or change domain logic

1. Keep calculations and invariant-preserving behavior on the domain structure when they need no infrastructure.
2. Use a stateless Service for cross-object coordination or repository/service access. [Service placement](../../../docu/objectflow.md#service-komponenten)
3. Invoke configured components through `OperationCall` (`#`). [Operation calls](../../../docu/objectflow.md#komponenten-mit--aufrufen)
4. Load required facts first, collect expected failures in `validation`, then mutate. [Validation pattern](../../../docu/objectflow.md#preconditions-validation-guards-und-exceptions)
5. Use server date/time literals and `BigDecimal` literals for business time and exact decimals; do not use `double`/`float` for exact values. [Date/time/decimal literals](../../../docu/objectflow.md#literale-für-datum-zeitpunkt-und-dezimalzahl)
6. Use `status switch` without a default when exhaustive handling should be checked. [Status switch](../../../docu/objectflow.md#statuswerte-mit-status-switch-behandeln)

Load the MPS BaseLanguage skill whenever writing method bodies or expressions.

## Create a command

1. Pick the command type from its ownership and commit semantics, not its visual appearance. [Command types](../../../docu/objectflow.md#die-vier-command-typen)
2. Insert [command-skeleton.json](blueprints/command-skeleton.json) and set a space-containing user-facing name.
3. Add parameters/default selections and `generally enabled` conditions. Defaults do not replace business validation. [Parameters and selection](../../../docu/objectflow.md#parameter-defaults-und-selektion)
4. In `command init`, load/checkout the graph and reject startup with Preconditions before mutation. `IN_BACKGROUND` applies only to init. [Command init](../../../docu/objectflow.md#command-init-und-hintergrundinitialisierung)
5. Add Pages incrementally. Each normal Page requires a Page Init and at least one Page Pane link; keep an unconditional link last. [Pages](../../../docu/objectflow.md#pages-und-page-conclusions)
6. Put Page-specific `#Meta` changes in scopes; keep server-side validation as well. [Property metadata](../../../docu/objectflow.md#ui-metadaten-einer-property-mit-meta-steuern)
7. Use `save` conclusions normally; use `no_save` only to discard editor state intentionally. [Page Conclusions](../../../docu/objectflow.md#page-conclusions)
8. Register check-in/delete operations in the session owner. Do not register normal session operations in a Graph Edit. [Session and Unit of Work](../../../docu/objectflow.md#session-und-unit-of-work)
9. Add the aggregate root to `revert` when a child edit must be undone on cancel. Revert is in-memory, not a database rollback. [Revert](../../../docu/objectflow.md#revert-beim-abbruch)
10. Validate the command, then test it with `run command`.

Prefer `NEWSTYLE_CMD_TERM_HANDLING`: consume pushed values in a termination handler, merge explicitly, and continue with the merge result. [Explicit termination and merge](../../../docu/objectflow.md#explizites-command-termination-handling-und-session-merge)

Use Successors for one atomic Unit of Work; use `session queue next command` for a post-commit UI flow. [Successors](../../../docu/objectflow.md#successor-commands) and [post-commit queue](../../../docu/objectflow.md#command-nach-dem-commit-einplanen)

## Create an ObjectFlow test

1. Insert [test-suite-skeleton.json](blueprints/test-suite-skeleton.json).
2. Replace `TARGET_OFX_CONFIG` with a resolvable configuration in the destination model.
3. Add configured components and test content incrementally.
4. Use `Simple Test` for session-aware domain/service/repository tests. [OFX Test Suit](../../../docu/objectflow.md#ofx-test-suit)
5. Use `run command` to model expected Pages, forced Conclusions, child Commands, Successors, cancellation, and pushed results. [Commands without UI](../../../docu/objectflow.md#commands-ohne-ui-ausführen)
6. Use `FAIL IN` for expected failures and `DEFAULT_DATETIME` for deterministic business time. [Test options](../../../docu/objectflow.md#testoptionen)
7. Remember that tests do not commit; assert through prepared/read state and observed operations. [Typical test levels](../../../docu/objectflow.md#typische-testebenen)

## Integrate persistence with ManMap

1. Load [the ManMap DSL skill](../../manmap-dsl/SKILL.md).
2. Map Entity properties in a `Persistence Description`; DTOs are normally read models rather than persisted aggregates.
3. Explicitly load every reference/list needed by the use case; no lazy loading occurs. [Mapped queries and explicit loading](../../../docu/manmap.md#explizites-laden)
4. Use ReadOnly for searches/evaluation and Checkout for modification; reuse the session instance instead of checking out the same identity twice. [Read-only, Checkout, and identity](../../../docu/manmap.md#read-only-checkout-und-session-identität)
5. Register `save with`, `delete with`, and transactional SQL statements as session operations owned by the Command. [Saving](../../../docu/manmap.md#speichern-mit-save-with) and [MoWare transaction boundary](../../../docu/moware-werkbank.md#grundprinzipien-für-die-anwendungsentwicklung)

## Integrate UI with DataUX

1. Keep Page state/control flow in ObjectFlow and visible composition in a DataUX Page Pane. [DSL responsibilities](../../../docu/moware-werkbank.md#wo-gehört-eine-änderung-hin)
2. Prepare and load the data before binding it; a binding never loads data. [Data binding](../../../docu/dataux.md#datenbindung-und-selektion)
3. Match delegate type to Business Property type and handle empty selections. [Forms, tables, and delegates](../../../docu/dataux.md#formulare-tabellen-und-delegates)
4. Place command actions in Page Pane menus; declaring a branching Command on a Page does not make it visible by itself. [Menus and command actions](../../../docu/dataux.md#menüs-und-command-aktionen)
5. Keep business rules out of UI expressions. [MoWare CheapCode principle](../../../docu/moware-werkbank.md#grundprinzipien-für-die-anwendungsentwicklung)

## Large-root editing

1. Insert only the root skeleton.
2. Validate it immediately.
3. Add Business Properties, Pages, methods, conclusions, test content, or config elements with surgical `ADD CHILD` calls.
4. Use `SET CHILD` for one subtree; avoid a full-root rewrite unless the complete root is intentionally replaced.
5. Run `FIX_REFERENCES` only after the expected targets exist, then validate again.

