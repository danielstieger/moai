# Mapped query operations

Build `QueryFromMap` from an `EntityMapping` reference and its `queryOperation` children. `GetQuery` takes a key argument and returns one entity; `WhereQuery` takes a BaseLanguage filter closure and returns a list. See [mapped operations](mapped-operations.md) and [session behavior](session-behavior.md) before composing multiple queries in one session.

The permanent `Domain.RepoInvoice` supplies focused methods for the remaining operations:

| Method | Pattern to copy |
|---|---|
| `findInvoiceByIds` | `WhereQuery` with `InOperation`: `invoice.id in ids` against a list parameter. |
| `findInvoiceByByNameeWithLikeOP` | `WhereQuery` with `LikeOperator`: a string property compared with a pattern parameter such as `%likeop%`. |
| `findInvoiceByIdOrByName` | `OptionalOperator` around individual predicates combined by `||`. The permanent test exercises `id=0` and `name=null` as omitted choices; see the type rules below. |
| `findInvoicesByIdSortReversId` | `WhereQuery` followed by `SortByQuery` with `sortDirection=DESC`. |
| `findAllInvoicePositionsLimit` | `WhereQuery`, `SortByQuery` with `sortDirection=ASC`, then `LimitQuery` with a count expression. |

**Language-author rule:** `OptionalOperator` has its own no-value sentinels: `0` for `int`; `null` for BigDecimal, date, time/date-time, string, object references, and ObjectFlow status values. When the relevant value has that sentinel, the optional predicate is omitted. `boolean` is not supported by `OptionalOperator`. This is independent of `isNullKeyStaticHelper()` for `SaveWithMap`; do not treat `-1` or an empty string as an omitted optional filter merely because they can represent an unset key.

These are ManMap operations whose predicates, comparables, arguments, and counts are BaseLanguage expressions. Print the smallest relevant method through MPS MCP, build/rebind its variable and property references for the target model, and validate the repository root. Use a `ParenthesizedExpression` where boolean precedence matters. The permanent `Tests.Query and Operators (no session)` suite checks `in`, `like`, and optional-filter cases; see the [test index](test-index.md).
