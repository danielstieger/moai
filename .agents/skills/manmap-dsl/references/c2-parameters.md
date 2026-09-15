# Values in `C2SqlText`

Prefer named parameters in new C2 SQL. In the permanent `Domain.C2SqlRepo`, `updateTextInAuditEntityPlainSQLWithLocalVars` shows local variables (`:text`, `:id`) and an object variable's property (`:ae2_id`) within one `C2SqlBlock`. `namedParamTest` repeats the same named parameter in one query. Use the MPS nodes that point to actual declarations in scope; the display text is not a substitute for those references.

| SQL value to reference | C2 node | Permanent example |
|---|---|---|
| A variable available in the method or SQL block, including a local binding | `C2SqlWordVarReference` with `varDecl` pointing to its `VariableDeclaration` | `C2SqlRepo.updateTextInAuditEntityPlainSQLWithLocalVars`: `:text`, `:id` |
| A property of an object held in a variable | `C2Dot` with `operand` (often a `C2SqlWordVarReference`) and `operation` (for example a `C2PropertyReference` targeting the property) | `C2SqlRepo.deduplicationOfNP`: `:entity_id` |
| An ObjectFlow status element constant | `C2SqlStatusReference` with an ObjectFlow `StatusConstReference` in `primConstant` | `C2SqlRepo.checkoutAuditEntityByIdAndStatusON`: `OnOff.on` |

`C2SqlWordVarReference` and `C2Dot` are based on *what is in the current context*: a direct variable versus a property reached from an object variable. `C2SqlStatusReference` is for a declared status value, not for a variable with a status type. The [word-variable](blueprints/c2-word-var-reference-subtree.json), [object-property](blueprints/c2-dot-property-subtree.json), and [status](blueprints/c2-status-reference-subtree.json) blueprints show these node shapes. Resolve all variable/property/status targets in the target model and method.

Use `C2SqlIntegration` only for legacy or unusually dynamic SQL. For normal SQL with in-scope values, use the C2 text reference nodes above and follow [direct SQL result mapping](direct-sql.md). The permanent `C2SqlRepo` also has `simpleSqlStringText_NP` and positional-argument methods to compare historical forms; the language author prefers named parameters for new work.
