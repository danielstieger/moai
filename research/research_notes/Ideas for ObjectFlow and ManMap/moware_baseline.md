# MoWare baseline: what ObjectFlow and ManMap can and cannot express today

Scope: inventory drawn exclusively from the local documentation in `/home/rocketdan/migration/2026_1/moai/` (German). All section titles are quoted verbatim so the report writer can cite them. File abbreviations used below: `OF` = `docu/objectflow.md`, `MM` = `docu/manmap.md`, `WB` = `docu/moware-werkbank.md`, `DUX` = `docu/dataux.md`, `CONV-*` = files in `conventions/`, `PR1`/`PR2` = `deprecated/problems_run1.md` / `problems_run2.md`. Documentation state: "Stand Oktober 2026, auf Basis von JetBrains MPS 2026.1" (OF § "Dokumentstand", MM § "Dokumentstand", WB § "Stand der Dokumentation"). WB § "Zweck und Geltungsbereich" states that where documentation and loaded MPS languages differ, the language definitions and their checking rules are the technical source of truth, and that the documentation describes observed practice while the binding architecture rules live in `conventions/`.

---

## 1. ObjectFlow capability inventory

### Takeaway
ObjectFlow is a closed-world DSL on top of MPS BaseLanguage: three root data structures with a fixed property-type list (no boolean, no double), a rich Status concept replacing enums, stateless Services called through `#`, a Precondition/Validation/Guard triad, and a Command concept with four types that owns session and transaction. Tests, configuration, roles, static resources, logging and serdes are part of the same language.

### Cited Findings

**Data structures and property types**
- Three root-capable data structures: `Entity` (identity and lifecycle), `Value Object` (value without identity, used immutably), `DTO` (application data container without entity identity; may itself hold Entities and lists of Entities). All three have Business Properties and may contain BaseLanguage constructors and methods. — OF § "Entity, Value Object und DTO"
- Modeling an Entity does not imply persistence; tables, keys and load/save are described in ManMap. — OF § "Entity, Value Object und DTO"
- A Business Property has name, type, implementation, optional short/long description, number/date format (`java.text.DecimalFormat`, `org.joda.time.format.DateTimeFormatter`), documentation, visibility and property options. — OF § "Business Properties"
- The property type list is explicitly complete ("Die folgende Liste ist vollständig"): `string`, `int`, `LocalDate` (Joda), `DateTime` (Joda), `BigDecimal`, declared Status, declared Entity, declared Value Object, declared DTO, `list<T>` (T an Entity or DTO), `byte[]`. `boolean` is "Nicht unterstützt ... ManMap kann ihn nicht mappen und DataUX nicht darstellen. Ein fachliches Ja/Nein wird als Status modelliert." — OF § "Business Properties"
- `double` and `float` are not supported anywhere ("auf sie ist stets zu verzichten"); `13.44bd` creates a `BigDecimal`. — OF § "Literale für Datum, Zeitpunkt und Dezimalzahl"
- Property options on a Business Property accept ManMap `FieldOption` subconcepts: ObjectFlow options `PRESENTATION` (not persisted, dirty-irrelevant), `CONTAINMENT` (list as parent-child, optional back-reference), `OPPOSITE` (back-reference), `DEPRECATED`, `RANGE` (int and BigDecimal), `LENGTH` (min/max string length; controls mandatory input and max length in UI); ManMap options `KEY`, `AUTOID`, `CREATEDAT`, `CREATEDBY`, `MODIFIEDAT`, `MODIFIEDBY`, `INDEX`, `NOTNULL`, `SIZE`, `UNIQUE`. — OF § "Business Properties", table "Projektion | Konzeptname | Bedeutung"
- Virtual properties via `custom` implementation: `get` accessor computes on every read, optional `set(value)` distributes; keep metadata and are usable in expressions and DataUX bindings; "Getter können keine Repositories oder Services aufrufen". — OF § "Virtuelle Business Properties"
- `equal properties` on a Value Object selects which properties define value equality. — OF § "Value-Object-Gleichheit"
- Initial values: `string` → `""`, `int` → `0`, `BigDecimal` → `0.0`, Status → `ON_CREATION` element, list → empty, `LocalDate`/`DateTime` → `null`, Value Object → `null`, Entity/DTO reference → `null`. A loaded `string` is never `null` (ManMap maps SQL `NULL` to `""`). — OF § "Null-Werte in Datenstrukturen"
- Equality is type-dependent: `int` `==`; `string` `:eq:`/`:ne:` (generator also rewrites `==` to `equals`); `BigDecimal` `==` null-safe via `compareTo`; Status via `of` / `status switch`; Entity `==` = instance identity (unique only for session-integrated entities); DTO has no object comparison; `LocalDate`, `DateTime`, Value Object and other objects need `:eq:`/`:ne:`. `rechnung.kunde#Key == null` on a Value-Object key is a checker error; use `isNullKey`. — OF § "Null-Werte in Datenstrukturen"
- `#Key` reads the referenced entity's key without loading it; direct access to an unloaded reference throws `OFXNotInitializedException`; `isNullKey` understands ObjectFlow/ManMap null-key semantics including composite keys. — OF § "Beziehungen und Objektgraphen"

**Status**
- A Status replaces a Java enum but carries a persistence value, short/long description and metadata; usable as property type, comparable, referenceable in SQL, rendered by DataUX with label and color. — OF § "Status"
- Options at declaration level: `ALLOW_NULL_PERSISTANCE` (status property can always be `null` in memory; without the option saving `null` throws), `OPTIONAL_AS`. Element level: `ON_CREATION` ("Jede Statusdeklaration braucht genau ein Element mit dieser Option"), `COLOR`, `WHEN_NULL_WL`, `WHEN_UNDEFINED_WL`. `ALLOW_NULL_PERSISTANCE` and `WHEN_NULL_WL` are mutually exclusive. — OF § "Status"
- `status switch` with `case` branches offering only elements of that status; without `default` the language checks completeness; `default: // and null` handles `null` too. — OF § "Statuswerte mit `status switch` behandeln"
- `#Meta` on a property sets runtime UI metadata: `setEnabled`, `setOptional`, `requestFocus`, `setElements(...)` for status, `setScope(...)` for entity selection. Business rules must still exist as Preconditions/validation. — OF § "UI-Metadaten einer Property mit `#Meta` steuern"

**Methods on data structures**
- Entities, Value Objects and DTOs can contain BaseLanguage constructors and methods for object-bound logic (calculations, state queries, normalization, consistent aggregate changes such as add/remove position). Static methods exist only on Value Objects. — OF § "Methoden an Datenstrukturen"
- No component call `#Component.method()` from a data structure; consequently a data-structure method cannot load missing data; values must be passed in; anything needing repositories/config/other aggregates goes to a Service. — OF § "Methoden an Datenstrukturen"
- Dirty tracking: entity becomes dirty on actual value change after load or when new; lists are compared by content (reordering is not a change); read-only loaded entity throws `OFXIllegalAccessException` on setter; checked-out entity is read/write; identity map rejects second checkout. Value Objects have no dirty/read-only state and are replaced wholesale. — OF § "Dirty-Tracking, Read-only und unveränderliche Werte"

**Services**
- `Service` (editor: `component <Name>`) is a runtime-managed singleton; must not hold user/session state; caches/lookups allowed as exceptions. — OF § "Service-Komponenten"
- ObjectFlow has no separate service subtypes: "allgemeiner Domänenservice" and "Anwendungsfallservice" are both the same concept `Service`; the distinction is by responsibility and naming only. Four placement levels: data-structure method, general domain service, use-case service, Command. — OF § "Service-Komponenten"
- Service Method: parameters, return type, body, optional Preconditions; options `API_METHOD` (marks for API integration, does not change `#` classification) and `TO_SESSION_OPS` (deferred only when called in `FINAL OK_CONCLUSION`; a method with `TO_SESSION_OPS` may not have Preconditions, runtime throws). — OF § "Service-Methoden"
- A service can change persisted data directly by executing a ManMap `STATEMENT` repository operation (e.g. targeted `UPDATE`/`DELETE`); as session operation it joins the owner transaction. — OF § "Service-Komponenten"

**Preconditions, validation, guards**
- `precondition`: user-correctable condition; stops program flow outside a `validation`; message shown in UI; `validation` collects several violated preconditions into one problem report; `guard` ends the command in `FINAL CANCEL_CONCLUSION` with neutral user message and developer diagnostics; Exception does the same. — OF § "Preconditions, Validation, Guards und Exceptions"
- Full form: `precondition <condition> : + <options> 'Text'%(<args>) / <instance>` + `'propertyName' : <value>` log properties + `resolve with <GRAPH_EDIT_CMD>(<args>)`. Options `WARNING_HINT`, `PRIO_INFO`, `PRIO_FATAL` (`PRIO_ERROR` is default and may not be written). Empty condition shows `->` and always fires. Message must be a `StringFormatString` (single quotes), not a Java string. — OF § "Preconditions, Validation, Guards und Exceptions"
- `resolve with` allows only a `GRAPH_EDIT_CMD` with given arguments as corrective action. — OF § "Preconditions, Validation, Guards und Exceptions"
- A guard in a `GRAPH_EDIT_CMD` escalates and ends the session owner too; only a guard can forward an exception (`guard <cond> : forward <ex> 'Text'%()`). — OF § "Preconditions, Validation, Guards und Exceptions"
- Recommended pattern: load facts → one `validation` block → only then mutate graph; "Prüfungen und Änderungen sollen nicht abwechselnd ausgeführt werden." — OF § "Preconditions, Validation, Guards und Exceptions"
- `StringFormatString` placeholders include `%bd`, `%st`, `%sts`, `%stdb`, `%dt`, `%ld`, `%sld`, `%tdt`; `null` renders as `#NULL?`. — OF § "Formatieren von Zeichenketten"
- Literals: `31.12.2026`, `new_LocalDateFromServer()`, `31.12.2026 14:30:0`, `new_DateTimeFromServer()`, `13.44bd`. — OF § "Literale für Datum, Zeitpunkt und Dezimalzahl"

**Operation calls and session operations**
- Service and repository methods are called exclusively with `#`; direct Java calls are "nicht vorgesehen". Behavior table: normal service method runs immediately; `TO_SESSION_OPS` outside `FINAL OK_CONCLUSION` is a normal call; in `FINAL OK_CONCLUSION` it is registered; `READONLY`/`CHECKOUT` ManMap methods run immediately; `CHECKIN`/`DELETE` outside `FINAL OK_CONCLUSION` in a Command is a checker error unless `#+ with` custom session is given, in a Service it runs immediately; in `FINAL OK_CONCLUSION` they are registered (`+ to session ops`); calls at `<marker operation>`/`<journal operation>` positions in `FINAL CANCEL_CONCLUSION` are cancel operations with own transaction, only in `GRAPH_OWNER_CMD`. — OF § "Komponenten mit `#` aufrufen"
- `#+ with <Session>` passes a custom session for that call; enables loading outside the current session, avoiding double checkout, and short independent transactions whose commit is not rolled back by the outer session; "soll deshalb sparsam eingesetzt werden". — OF § "Komponenten mit `#` aufrufen"
- `session operation add # Repo.checkin(x) // 'Text';` registers a call on the operation stack; requires description text; local variables used in the call must be `final`; return values and generated IDs are not available after registration. Not allowed in addition to auto-registered calls. — OF § "Explizite Session-Operationen"

**Commands**
- Four types (table "Die vier Command-Typen"): `SEARCH_CMD` (own session, `FINAL OK_CONCLUSION` ends session without commit, session operations are not executed); `GRAPH_OWNER_CMD` (own session, commit on `FINAL OK_CONCLUSION`; as successor takes over predecessor's session); `GRAPH_EDIT_CMD` (uses owner's session, no own commit); `GRAPH_OWNER_CMD(modal)` (`GRAPH_OWNER_CMD_MODAL`, same as owner, modal UI). — OF § "Die vier Command-Typen"
- A `GRAPH_EDIT_CMD` can technically register session operations but they are not removed on child cancel, so in practice it should not. — OF § "Die vier Command-Typen"
- Lifecycle: parameters/defaults → local variables → `command init` (may stop with Precondition) → `command title` → first page or `page <Name>`/`done` → Conclusions → `FINAL OK_CONCLUSION`/`FINAL CANCEL_CONCLUSION`/`FINAL_USER_CANCEL`. — OF § "Grundablauf eines Commands"
- Command parts (table "Aufbau eines Commands"): parameters and defaults (`getSelected()`, constants), `generally enabled` (AND-ed booleans), Permissions (`CAN_OPEN_RO`/`CAN_OPEN_RW`), Preconditions, local variables, Command Settings (label, icon, hotkey, color, revert, locks, options), `command init`, Pages, `FINAL OK_CONCLUSION`, `FINAL CANCEL_CONCLUSION` (with `listOfProblems`), `FINAL_USER_CANCEL`. — OF § "Aufbau eines Commands"
- Parameter defaults `getSelected(Typ)` / `getSelectedObjects()`; `+ derived` includes subtypes; missing default makes command unavailable. — OF § "Parameter, Defaults und Selektion"
- `IN_BACKGROUND` runs only `command init` in background; Precondition in `command init` prevents start; `WARNING_HINT` only warns. `command title` computed after init; `newWindowTitleType` `ADDON`/`OVERWRITE`/`OVERWRITE_FORCED`. — OF § "Command Init und Hintergrundinitialisierung"
- Page (`page ctrl`): binding to Entity/DTO type, Page Init (`pageLoadFunc` returns object), Page Title/Subtitle, Scopes (`pageSetScopesFunc`), one or more `PagePaneActionProviderLink` (conditional `<cond> : PagePane`, unconditional `-> : PagePane`, last must be unconditional), `cmdTermHandler`, read-only `branching commands:` display, 0..n Page Conclusions. — OF § "Pages und Page Conclusions" and § "Mehrere Page Panes"
- Only `WARNING_HINT` preconditions belong in Page Init; aborting ones go to `command init` or a Conclusion. — OF § "Page Init und Datenbereitstellung"
- Scope function runs after Page Init and after child termination (after any termination with `any cmd term` handler); it loads no data. — OF § "Scopes"
- Page Conclusion: label, `enabled if`, `ConclusionSaveType` `save` (default, copies editor values) / `no_save`, body; must contain `page`, `done` or a Precondition; `page <same page>` acts as refresh; failed Precondition keeps the page visible. — OF § "Page Conclusions"
- Semantic hotkeys `SCAN/UPDATE` and `GO/OK` (enum `Hotkey`), each once per page; `SCAN/UPDATE` paired with DataUX `ISSUE UPDATE/SCANABLE` yields reactive behavior on change. — OF § "Conclusions mit SCAN/UPDATE oder GO/OK"
- `pushSelection(obj)` allowed only in Page Init, Page Conclusion, `cmdTermHandler`, and `before conclude` of a test `run command`. — OF § "Selektion mit `pushSelection` setzen"
- `FINAL OK_CONCLUSION`: function runs, then transaction, session operations in registration order, commit, then `selection(s)/push(es)`. Preconditions are not supported there (lead to `FINAL CANCEL_CONCLUSION` plus `IllegalStateException`). `user toast message` shows a message and passes named values forward to a calling test; only in committing commands. — OF § "`FINAL OK_CONCLUSION`, `FINAL CANCEL_CONCLUSION` und `FINAL_USER_CANCEL`"
- `FINAL CANCEL_CONCLUSION`: triggered by guards and exceptions, and in jobs also by violated Preconditions; normal session operations are not executed; separate cancel operations (marker/journal) run in a private transaction. `FINAL_USER_CANCEL`: ESC/back/close; UI runtimes always show a cancel button, "eine Abbrechen-Conclusion wird deshalb nie modelliert"; `NO_ESC` disables it. — same section
- `listOfProblems` (`list<IOFXProblem>`) in `FINAL CANCEL_CONCLUSION` with methods `getSimpleUserText()`, `isFromGuard()`, `hasForwardedEx()`, `isWarningOnly()`, `isJobIgnore()`, `isJobItemAlreadDone()`, priority getters. — OF § "Problembericht in der `FINAL CANCEL_CONCLUSION`"
- Revert: `revert on FINAL_ / USER_CANCEL` lists Command parameters only; local variables are not revertible; runtime copies at start; whole subgraph reverted from a root; session operations are not undone; in-memory only, not a DB rollback; a `GRAPH_EDIT_CMD` must list the shared graph root to discard its changes. — OF § "Revert beim Abbruch"
- Command options: `IN_BACKGROUND`, `NO_ESC`, `NEWSTYLE_CMD_TERM_HANDLING`, `URL` (turkuforms/h2forms; path with ordered params, `(opt)` only at end; types `string`, `int`/`Integer`, Status; no URL en/decoding; `url param adjust` expressions). — OF § "Command-Optionen"
- Session: `session` gives direct access to internals ("für Fälle gedacht, die durch die höherwertigen Sprachkonzepte nicht abgedeckt werden"); `session.ensureInSession(...)` for entities not loaded via `QueryFromMap` (new ones, or ones from `nokeystore/read-only map`). — OF § "Session und Unit of Work"
- `session.setReadOnly()` disables all conclusions and locks all `Delegate Form`s; does not mark already-integrated entities read-only. `session.isDirty()` checks explicit flag then all integrated entities (new keyless = dirty; list changes included); used for the automatic cancel confirmation of owner commands. — OF § "Session-weites Read-only und Dirty"
- Locks: `acquire locks` in owner commands; each lock is a string evaluated before `command init` (parameters only); if held by another user the command runs with a read-only session and shows the holder; released on every termination. Optimistic locking via TCN is the default. — OF § "Pessimistische Sperren mit `acquire locks`"
- `session entities` with modes `(checked out)`, `(keys of checked out)`, `(all)`, `(keys of all)`; main use: avoid double checkout; reads only session state. — OF § "Entities in der Session prüfen"
- `session queue next command`: schedules a session-owner command (`SEARCH_CMD`, `GRAPH_OWNER_CMD`) with explicit arguments to start after successful commit; not started on cancel or failed commit; ignored without UI (tests, jobs); "ersetzt jedoch keine allgemeine Job- oder Workflow-Engine". — OF § "Command nach dem Commit einplanen"
- Termination handling: old mode auto-merged pushed entities in a `SEARCH_CMD`; `NEWSTYLE_CMD_TERM_HANDLING` disables that and is "das präferierte Pattern"; without it only `child cmd term` without classifier is allowed; a command with successors may not have `cmdTermHandler`. `CmdTermType` `child cmd term` / `any cmd term`; optional classifier. — OF § "Explizites Command-Termination-Handling und Session Merge"
- `session merge` combinations: `entity→entity`, `entity→list`, `list→list` (extra target elements are not removed), `ref→ref` (target must be `<Entity>.<Referenz>`, no opposite). Not supported: `entity→ref`, `list→entity`, `list→ref`, `ref→entity`, `ref→list`. DTOs need `getIM3Key()`. Modes `(in session as readonly)`, `(in session as checkedout)`, `(do not consider session/rw-state)`. Always use the return value; a graph is merged in several steps (root, lists, references). — same section
- Successors: `followed by` entries in `FINAL OK_CONCLUSION`, conditional first, last unconditional default; successor runs in same UI container without new session, shares graph and session operations; predecessor's `FINAL OK_CONCLUSION` deferred until successor succeeds; predecessor and target must be `GRAPH_OWNER_CMD`(`modal`); "Eine weitere Successor-Kette am Ziel-Command wird nicht unterstützt." — OF § "Successor-Commands"
- Multi-execution: a DataUX `Action` on a multi-row selection runs the same command once per row when a parameter uses `getSelected(Typ)` matching the row type; `getSelectedObjects()` disables it; commands with successors are excluded; `GRAPH_OWNER_CMD` with visible page cannot be multi-executed; owner runs are separate transactions (no atomic batch); a technical exception stops the whole run. A collective command with `getSelectedObjects()` is needed only when the selection must be evaluated as a whole. — OF § "Mehrfachausführung von `GRAPH_OWNER_CMD` / `GRAPH_EDIT_CMD`"

**Tests**
- `OFXTestSuit` references an `OFXConfig`, has configured components, `on startup`/`on shutdown`, `Simple Test`s with own session that is not committed at test end; "Die eigene Test-DSL ist der Ersatz für JUnit". — OF § "`OFXTestSuit`"
- Options: `PATH`, `DEBUG_TEST`, `DEFAULT_DATETIME`, `DEPENDENT_TEST`, `INCLUDE_SUIT` (with `exec tests`), `DONT_EXEC`, `FAIL IN` (exception class mandatory, message text optional). Exceptions: `OFXAbortedException` for a violated Precondition in a direct service/repo call (problems stay on the session); `OFXJobWorkCanceledException` inside `run command`; `RuntimeException` when a command cannot start. — OF § "Testoptionen"
- `run command`: start with arguments, `expect page` sequence with forced conclusion, `before conclude` block with bound object, optional pages, `<user_cancel>` only for `SEARCH_CMD`, nested `run command` for child commands, `when successor command`; owner commits as in production; passed-forward values via `OFXRunCmdCreateInfoRef`; `run command` does not reproduce `CAN_OPEN_RO` locks; `GRAPH_EDIT_CMD` cannot run at top level. — OF § "Commands ohne UI ausführen"
- Test levels: data structure/Value Object, Service, Repository and Session, Command. Persistence expectations are checked by reading back after commit, if needed in a custom session. — OF § "Typische Testebenen"
- Repository replacement: a ManMap `Repository` can extend another via `superclass`; test config marks the test repository with `primary instance`; `#` calls are unchanged. — OF § "Repositories im Test ersetzen"
- Custom sessions in tests: service `CS` from `org.modellwerkstatt.wbkit` with `CREATE()` and `COMMIT()`; `#+ with #CS.CREATE()` call form. — CONV `mw-tests_v1.md` § "Testdaten mit einer Custom Session anlegen"

**Configuration**
- `OFXConfig` (editor `Configuration <Name>`) is a modeled Spring IoC configuration: `section`, `include section`, `OFXConfigPropOverwrite`, `new instance` (class, properties, constructor args, free values), `property`, `constructor Argument`, `primary instance` (tests only), `Component Scanning` (Spring runtime scan under package), `Generation Time Resolution` (all components of the MPS project at generation time, namespaces excludable). Classes and namespaces are given as FQ-name strings only. External `moware_app.properties` via `MOWARE_APP_PROPPATH` with `${...}` placeholders. — OF § "Konfiguration mit `OFXConfig`"

**Roles, scopes, identities, user environment**
- `isAuthenticated(session, userEnvironment, username, password) -> boolean` is the init point for interactive apps; providing parameters does not set user name or ID automatically; `userEnvironment.setUserName`, `setUserId`, `setCompactMode`, `setBrandingId`, `setDynamicStatusInfo`; device getters; `session.getUserServices()`. Headless batch jobs do not run `isAuthenticated`; the `OFXConfig` must provide `IOFXUserEnvironment` and `IOFXUserServices` instances (`UserEnvironmentInformation`, `OFXSimpleUserServices`). — OF § "User Environment und User Service"
- `Roles and Permissions` root bundles `static role` (function `is(userEnvironment) -> boolean`, may call `#`; hierarchy via `is also / can also`), `Scope` (returns accessible objects of a type; parameters, variables, `#` allowed), `identity` (single central object or key). Commands declare `CAN_OPEN_RO role ...` / `CAN_OPEN_RW role ...`; none = unrestricted; `CAN_OPEN_RO` = read-only session (pure view); RW wins if both; `GRAPH_EDIT_CMD` may not declare `CAN_OPEN_RO` (checker error); `SEARCH_CMD` with filter form needs `CAN_OPEN_RW` or nothing. Roles also serve as feature flags. Role results are cached; `clearCachedValues(false|true)`. — OF § "Rollen, Scopes und Identities"

**Static resources**
- `Static Ressources` root: `Label` with `LabelSpecification` variants (default + per platform: text, icon, hotkey, display options), `Color`, `extends` another resource set, `PlatformDeclaration`/`PlatformExtended`. — OF § "Statische Ressourcen"

**Logging**
- `log` statement with level and structured properties, preferred over `System.out`; preconditions, guards, logs have different audiences. — OF § "Logging und Observability"

**Serdes**
- `CONV.jsonSerDes`, `CONV.xmlSerDes`, `CONV.stringSer`, `CONV.fopXmlSer()`; supports `Integer`, `BigDecimal`, `String`, `LocalDate`, `DateTime`, Status, nested Value Objects, key references, lists; "Virtuelle Business Properties werden derzeit nicht unterstützt"; cycles only via `OPPOSITE`, no visited-set, no object IDs; `IConvFormatOptions` modes (`ALL_PROPERTIES_NECESSARY`, `SET_MISSING_PROPERTIES_NULL`, `NULL_PROPERTIES_NO_SER`, `NULL_ARRAY_TO_EMPTY`, `SIMPLE_ARRAYS_TO_DTO`, `PRETTY`, `DEBUG_TO_STDERR`); `CONV.CONV_DEFAULT_EN`; `SerdesException`. — OF § "Serialisierung und Serdes"

### Inferences
- The language has no first-class concept for a "state machine"/transition table, a "query/filter object", an "aggregate repository", a "domain event", or an "authentication service"; all of these are realized by convention from Service, DTO, Repository and `isAuthenticated` (see sections 4 and 5).
- `session` direct access and `#+ with` custom sessions are the documented escape hatches when the higher-level concepts do not suffice.

### Gaps
- The documentation does not describe `ContainerVariable` semantics beyond "nicht revertierbar", nor whether Commands may be parameterized by lists other than via `getSelectedObjects()`.
- No documentation of concrete `IOFXUserServices` capabilities per runtime beyond the generic list.

---

## 2. ManMap capability inventory

### Takeaway
ManMap maps Entities (and embedded Value Objects) to tables with explicit field/reference/embedded/list mappings, offers a small typed query language (`get`/`where`/`reload` with `sortBy`, `limit`, `size`, `refJoin`, `listJoin`, `in`, `like`, `optional`) and `save with`/`delete with` for exactly one mapping at a time; everything else is hand-written dynamic SQL mapped by row mappers or no-key mappers. No lazy loading, no cascades, no schema migration.

### Cited Findings

**Repositories and method types**
- `Repository` bundles repo methods, `row mapper`, `nokeystore/read-only map`, `sql string`, optional fields; stateless, one instance per application. — MM § "Repositories und die vier Methodenarten"
- `repoMethodType` has exactly four values: `READONLY`, `CHECKOUT`, `CHECKIN`, `DELETE`. "Der Methodentyp ... erzeugt keine automatische Graph- oder Transaktionssemantik." A repository call opens no transaction by itself. — same section
- Session identity: `QueryFromMap` results go into the session identity map; a cached hit is returned only if query and instance are both read-only; otherwise `IllegalStateException` (re-checkout of checked-out entity, read-only `get` on checked-out entity, checkout of read-only loaded entity). Read-only forbids change and delete; loading references/lists by a repository method is exempt. `nokeystore/read-only map` results are read-only and outside the identity map (new instances per query); regular entities joined by such a map are read-only but session-integrated. — MM § "Read-only, Checkout und Session-Identität"
- `sql string` is a named reusable SQL text visible in the whole repository. — MM § "Wiederverwendbarer SQL-Text"

**Mappings and options**
- `Persistence Description` groups `EntityMapping`s; each connects an ObjectFlow class to a table with atomic mappings: `FieldMapping`, `ReferenceMapping` (foreign key of an entity reference; key mapping may be composite), `EmbeddedMapping` (Value Object columns in same row; usable as composite key), `ListMapping` with `MappedFieldRef` (back-reference) or `KeyOnlyReferenceMapping` (child table carries parent key, no back-reference), `IncludeMapping` (reuse of field mappings; "lädt oder speichert keinen Objektgraphen"). — MM § "Kapitellandkarte: Persistenz-Mappings", § "Referenzen, eingebettete Werte und Listen", § "Grenzen von `IncludeMapping`"
- Options: `KEY`, `AUTOID` (sequence name always required; Oracle sequence, MySQL/MariaDB `AUTO_INCREMENT`; simple keys only), `OVERWRITE_AUTOID` (in `IncludeMapping`), `OPTIMISTIC_LOCK` (table option; extra column `TCN`; recommended for new mappings), `ADDITIONAL_TABLE_NAME`, audit `CREATEDAT`/`CREATEDBY`/`MODIFIEDAT`/`MODIFIEDBY`, schema hints `INDEX`/`NOTNULL`/`SIZE`/`UNIQUE` ("keine Schema-Migration"). Field options can also be declared on the ObjectFlow property. — MM § "Felder, Schlüssel und Optionen", § "Automatische IDs und Sequences"
- Key reference is the normal case for lists; back-reference only if child→parent navigation inside the aggregate is needed; both describe only the relation, load/save stay explicit. — MM § "Referenzen, eingebettete Werte und Listen"

**Queries**
- `QueryFromMap` = `get` | `where` | `reload` on an `EntityMapping`, integrated `ReadOnly` or `Checkout`; `debugMe` prints SQL. `get` takes a key, returns instance or `null` (null-key semantics), stands alone (no joins). `where` takes exactly one boolean expression, returns list; any number of `sortBy`; last element optionally `limit` or `size` (`size` query is read-only); `refJoin`/`listJoin` only with `where`. `reload` refreshes mapped fields of a given entity, stands alone. — MM § "Gemappte Abfragen mit `QueryFromMap`"
- `MappingReference` addresses a field of a mapping instance available in `where`/`sortBy` (base mapping, `refJoin` target, `listJoin` target); cannot be dotted further; only inside `where`/`sortBy`; option `NOP`/`TO_LOCALDATE`/`TO_LOWERCASE`/`TO_UPPERCASE`. `ADDITIONAL_TABLE_NAME` is not a mapping instance. — MM § "Spezifikum - Filterausdrücke und gemappte Felder"
- Filter comparisons: `==`, `!=`, `<`, `<=`, `>`, `>=`; `:eq:`/`:ne:` are not allowed; `&&`, `||`, `!`; both sides type-compatible. Predicates `in` (list of matching element type incl. Status), `like` (wildcards in the pattern value, not added automatically), `optional` (drops predicate when parameter unset: `0` for `int`, `null` for `BigDecimal`, date/time, string, references, Status; `boolean` not supported; `-1` and `""` are not treated as unset). In `&&` a dropped `optional` is neutral; in `||` a group of only dropped predicates yields no rows ("liefert deshalb keine Treffer und nicht alle Zeilen"), workaround pattern `%`. — MM § "Spezifikum - Filterausdrücke und gemappte Felder"
- Explicit loading: unloaded reference throws `OFXNotInitializedException`; unloaded list is empty (`size == 0`); references/lists loaded by separate queries assigned to the property (allowed on read-only entities) or by `refJoin`/`listJoin`; joins mainly recommended when filtering/sorting on joined fields; "Eine leere Liste beweist daher nicht, dass in der Datenbank keine Kindzeilen vorhanden sind." — MM § "Explizites Laden"
- `listJoin` list order can be fixed by `sortBy` on a child-mapping field. — MM § "Kapitellandkarte: Gemappte Abfragen", row `listJoin`

**Save and delete**
- `save with <EntityMapping> (entity)` saves only the columns of that mapping, including foreign keys of mapped references; not saved: the referenced object, `ListMapping` elements, other graph parts. Parent-then-children ordering is hand-written. — MM § "Speichern von Objektgraphen"
- Insert/update decision without forcing option: single int key `null`/`0`/`-1` = unassigned; string key `null`/`""`; composite Value Object key: int components `< 0`, string components `null`/`""`. Options `INSERT`, `UPDATE`, `BATCH` (JDBC batch; "Auf MySQL und MariaDB ist `BATCH` nicht verfügbar; dort werden die Objekte einzeln gespeichert"), `FORCE AUDIT`, `SKIP AUDIT`, `WHEN <cond> <table>`. — MM § "Insert oder Update", § "Save-Optionen"
- `delete with <EntityMapping> (entity)` deletes a loaded entity by key; "Auch beim Löschen gibt es keine automatische Kaskade"; children deleted explicitly before parent; usually registered as session operation. — MM § "Löschen mit `delete with`"
- Audit: insert sets created/modified fields; update sets modified fields if object changed; timestamps come from the DB. — MM § "Optimistic Locking und Audit"
- Alternate tables: `ADDITIONAL_TABLE_NAME` + `WHEN <Bedingung> <Name>` on query, `save with`, `delete with`; joins may need the matching alternate table per mapping. — MM § "Alternative Tabellen"

**Custom SQL and mappers**
- `SQL` block (`C2SqlBlock`) mixes BaseLanguage statements with `C2SqlText` fragments; reached fragments are concatenated in execution order (e.g. `if` adds a condition only when a criterion is set); all visible variables available. — MM § "Custom SQL mit `SQL`"
- `sqlType` `QUERY` (result mapping) or `STATEMENT` (returns affected rows as `int`, no result mapping). — MM § "`SQL query` und `SQL statement`"
- Parameters: `:var`; dot access with nesting depth 1 (`:rechnung_id`, `:rechnung_kunde_KEY`, `:rechnung_methode`); allowed types `int`, `string`, `BigDecimal`, `DateTime`, `LocalDate`, `byte[]`, Status (bound via persistence value); `C2SqlStatusReference` for status constants; `+` integration with ordered `arguments` or `SqlNamedParameter`, intended for legacy/very dynamic SQL. — MM § "Parameter in SQL-Text", § "Statuskonstanten in SQL-Text", § "Integration mit `+`"
- Result mapping: inline closure (scalar), `row mapper` (closure over `IM3QueryFromSqlRowRef` with `getAsInteger/String/Decimal/DateTime/LocalDate` by name or 0-based index), `nokeystore/read-only map` (names result type and field mappings; may `IncludeMapping` an `EntityMapping`; an `EntityMapping` cannot be used directly as result mapping). Results read-only and outside identity map; DTO is the standard choice. — MM § "Row-Mapper und No-Key-Mapper"
- A read model may also be built with Entities + `EntityMapping` + `where` when expressiveness suffices; session integration must then be considered. — MM § "Die zwei Zugriffswege im Überblick" (note box)

**Database support**
- Oracle, MySQL, MariaDB; custom SQL stays dialect-bound; ManMap is not a schema migration tool. — MM § "Datenbankportabilität und Schema"

### Inferences
- Every aggregate-level operation (load graph, save graph, delete graph, search with filter) decomposes into several hand-written repository methods and per-mapping statements; the language offers no graph-level verb.
- `where` cannot express aggregation, projection to DTOs, grouping, or joins beyond declared `refJoin`/`listJoin`; those require the `SQL` block.

### Gaps
- MM does not document transaction isolation, connection handling, or paging beyond `limit`.
- No documentation on composite-key `get` syntax beyond "zusammengesetzter Schlüssel".

---

## 3. Batch jobs

### Takeaway
A `BatchJob Module` (DataUX) runs ObjectFlow `consumer/producer pair`s over a volatile in-memory inbox; the producer finds work, N consumers process it (usually by running `GRAPH_OWNER_CMD`s); failure handling is a rule list of `exception strategy` reactions; scheduling is `CRON`/`DELAY`/`DEPENDENT_CONSECUTIVE`.

### Cited Findings
- Core is `consumer/producer pair` (`OFXProducerConsumerPair`, ObjectFlow) and `exception strategy` (`OFXExceptionStrategy`); several pairs per module, each separately scheduled and parallelized. — DUX § "Batchjob mit `BatchJob Module`"
- Inbox semantics: producer puts entities or keys into a typed inbox; configured number of consumers each take one element, "häufig über einen oder mehrere `GRAPH_OWNER_CMD`-Commands"; a precondition should re-check that work is still needed; business cancel and technical failure are separated. — same section
- "Die Inbox ist eine flüchtige In-Memory-Queue und keine persistente Jobwarteschlange." Cleared before every producer run; lost on restart; consumer processing must be idempotent or detect done work. Element is removed before processing; re-added only with `READD_TO_INBOX`; no automatic retry otherwise; crashed consumer is replaced only with `CONSUMER_RESTART`. — same section
- Producer runs only when no consumer of the pair is working; completion order of parallel consumers undefined. Producer-only pairs allowed; their inbox must stay empty; `null` elements dropped. — same section
- `isAuthenticated` must be modeled on the `BatchJob Module` but runs only for a started UI; headless user context comes from `OFXConfig`. — same section
- Exception strategy mandatory; rules checked in order; last must be default; reactions `READD_TO_INBOX`, `DELAY_EXECUTION`, `CLEAR_INBOX`, `CONSUMER_RESTART`, `SILENT_NO_LOG`. Business cancel counted separately as *canceled*. No per-element processing timeout; external calls need their own timeouts. — DUX § "Exception-Strategien und Wiederanlauf"
- Options `CRON` (second, minute, hour, day, month, weekday; JVM default timezone), `DELAY` (continuous mode; combined with `CRON` for time windows), `CONSUMERS`, `DEPENDENT_CONSECUTIVE` (only first pair may have `CRON`/`DELAY`; chain restarts from first after failure), `RUN_IN_CONSOLE` (no longer supported, checker error; console mode configured via `ConsoleBatchJobAppFactory` in `OFXConfig`), `OptIncludeBatchUi`, `VERSION`, `OFFICIAL NAME`. — DUX § "Kapitellandkarte: Batchoptionen"
- Manual producer start is asynchronous, may bypass CRON window, clears and rebuilds inbox, is skipped if consumers still work, no retry on failure, does not continue a `DEPENDENT_CONSECUTIVE` chain. Console runtime runs all pairs as one dependent chain exactly once with one consumer each. — DUX § "Manuelle Ausführung und Konsolenbetrieb"
- Monitoring values (inbox size, fill-up time, producer status, counts, durations) via HTML dashboard (read) and JMX (operations). — DUX § "Monitoring und Betriebsdiagnose"
- In jobs a violated Precondition leads to `FINAL CANCEL_CONCLUSION` ("so wird in der Praxis eine Unit of Work im Job gezielt abgebrochen"); `session queue next command` is ignored without UI. — OF § "`FINAL OK_CONCLUSION`, `FINAL CANCEL_CONCLUSION` und `FINAL_USER_CANCEL`", § "Command nach dem Commit einplanen"
- Runtime table: batch jobs run as Tomcat servlet, or with FX8/turkuforms UI; "direkt gestartet, zeitgesteuert über Cron ausgeführt oder kontinuierlich mit einer konfigurierten Wartezeit". — WB § "Laufzeitumgebungen"

### Inferences
- There is no persistent job queue, no retry-with-backoff policy per element, no dead-letter concept and no per-element timeout in the language; durability depends entirely on the producer query and consumer idempotency.

### Gaps
- DUX does not document how a producer's return type is declared or how a consumer receives its element (signature level) in the Teil II text read.

---

## 4. Explicit non-features and design principles stated by the documentation

### Takeaway
The documentation and conventions state a consistent set of deliberate omissions (no lazy loading, no cascades, no migration, no boolean, no Optional, no cancel conclusion, no workflow engine) and a layering/convention model that pushes recurring structure onto the developer.

### Cited Findings
| Non-feature / principle | Statement | Where |
| --- | --- | --- |
| No lazy loading | "Automatisches Lazy Loading ist nicht möglich." / "automatisches Lazy Loading findet nicht statt." | WB § "Grundprinzipien für die Anwendungsentwicklung" item 2; MM § "Modellierungsumfang und Ausdrucksmöglichkeiten" |
| No cascading save | "Eine fachliche Beziehung oder ein Mapping bedeutet nicht automatisch, dass ein vollständiger Objektgraph kaskadierend gespeichert wird." | WB § "Grundprinzipien" item 3; MM § "Speichern von Objektgraphen" |
| No cascading delete | "Auch beim Löschen gibt es keine automatische Kaskade." | MM § "Löschen mit `delete with`" |
| No schema migration | "ManMap ist kein allgemeines Werkzeug zur Migration bestehender Datenbankschemata."; schema hints "keine Schema-Migration"; developer creates schema in MPS; agents never create schemas | MM § "Datenbankportabilität und Schema"; MM § "Kapitellandkarte: Persistenz-Mappings"; WB § "Von der Modellierung zur Ausführung" step 3; CONV `mw-allgemein_v1.md` |
| No boolean property | "`boolean` ... Nicht unterstützt ... Ein fachliches Ja/Nein wird als Status modelliert." | OF § "Business Properties" |
| No double/float | "Die Java-Typen `double` und `float` werden nicht unterstützt" | OF § "Literale für Datum, Zeitpunkt und Dezimalzahl" |
| Strings never null | "Ein `string` ist nie `null`; „kein Wert" ist der leere String." (exception: deliberately optional filter criteria) | CONV `mw-domaenenmodell_v1.md` § "Werte"; OF § "Null-Werte in Datenstrukturen" |
| No `Optional` | "`java.util.Optional` wird nicht verwendet." | CONV `mw-domaenenmodell_v1.md` § "Werte" |
| No cancel conclusion | "eine Abbrechen-Conclusion wird deshalb nie modelliert" | OF § "`FINAL OK_CONCLUSION`, `FINAL CANCEL_CONCLUSION` und `FINAL_USER_CANCEL`" |
| No preconditions in FINAL OK | "Preconditions werden in `FINAL OK_CONCLUSION` nicht unterstützt" | same section |
| No workflow engine | "Der Mechanismus ersetzt jedoch keine allgemeine Job- oder Workflow-Engine." | OF § "Command nach dem Commit einplanen" |
| No successor chains | "Eine weitere Successor-Kette am Ziel-Command wird nicht unterstützt." | OF § "Successor-Commands" |
| No domain events | Not mentioned anywhere in OF/MM/WB; WB § "Zentrale Konzepte" says the stack "übernimmt aber nicht sämtliche DDD-Konzepte". | WB § "Zentrale Konzepte der MoWare-Werkbank" (absence) |
| No service subtypes | "ObjectFlow besitzt keine getrennten Service-Untertypen" | OF § "Service-Komponenten" |
| No component calls from data structures | "Von einer Datenstruktur aus ist kein Komponentenaufruf ... möglich." | OF § "Methoden an Datenstrukturen" |
| Encapsulation not enforced | "Die Sprache erzwingt diese Kapselung nicht: Properties einer Entity sind auch von Commands und anderen Services aus setzbar." | CONV `mw-domaenenmodell_v1.md` § "Service und Aggregat" |
| State transitions as service methods by convention | "Jeder wesentliche fachliche Zustandsübergang ... ist eine eigene Service Method im `<Aggregat>Service` ... benannt nach dem fachlichen Vorgang" | CONV `mw-domaenenmodell_v1.md` § "Aggregate und Invarianten" |
| Load/logic separation by convention | load method + pure method pair, e.g. `freigeben(rechnung)` and `freigabeEntscheiden(rechnung, fakten)` | CONV `mw-domaenenmodell_v1.md` § "Service und Aggregat" |
| Cross-aggregate reference read-only | "Ein Aggregat referenziert ein anderes nur als Querverweis ... read-only geladen ... nie mit dem referenzierenden Aggregat gespeichert." | CONV `mw-domaenenmodell_v1.md` § "Aggregate und Invarianten" |
| Value Objects immutable | change via `with`-method or constructor; static factory/constants/predicates desired; constants as methods not fields | CONV `mw-domaenenmodell_v1.md` § "Werte" |
| Model layering | levels 1–4: `base`, `rollen`, `sharedvalues`, `gate.*`, `<bereich>.domain`, `<bereich>.read`, `<bereich>.unit`, `app`, `tests`; strict import table; no higher-level imports; no cycles between bounded contexts | CONV `mw-anwendungsaufbau_v1.md` § "Solutions und Modelle", § "Abhängigkeiten" |
| Queries outside aggregate load go to `read` | "Alle Abfragen außer dem Laden des Aggregats liegen im `read`" | CONV `mw-anwendungsaufbau_v1.md` § "`domain`, `read` und `unit`" |
| DTO placement | command-only DTO is CheapCode in `unit`; a service never accepts it; DTOs consumed by services or filled by repos live in `read` incl. all search/filter DTOs | CONV `mw-anwendungsaufbau_v1.md` § "`domain`, `read` und `unit`" |
| Input validation vs business rules | DTO input checks are CheapCode and never replace service checks; `LENGTH`/`RANGE` + delegates for mandatory/limits; Precondition on DTO only for cross-field | CONV `mw-domaenenmodell_v1.md` § "Eingabeprüfungen und fachliche Prüfungen" |
| Session owned by command | "Session und Transaktion gehören zum Anwendungsablauf, nicht zu einzelnen Repository-Aufrufen." | WB § "Grundprinzipien" item 5 |
| Check before change | "Prüfen und Verändern sind möglichst klar zu trennen." | WB § "Grundprinzipien" item 6 |
| Read-only vs edit distinction | item 4 | WB § "Grundprinzipien" item 4 |
| UI is CheapCode | item 7; ExpensiveCode/CheapCode | WB § "Grundprinzipien" item 7; WB § "Ziele der Werkbank" |
| Owner/Edit convention | owner holds editable form only when creating; loaded aggregate → `DISABLED` form, edits via `GRAPH_EDIT_CMD` | CONV `mw-commands_v1.md` § "Owner und Edit" |
| Search result refresh by merge, not re-query | "die Suche wird dafür nicht erneut über das Repository ausgeführt" | CONV `mw-commands_v1.md` § "Suche und Rückgabe" |
| UI conventions | page title mandatory; no left/right split; submenu overflow; `-1` form weight; table `LABEL`; wizard F3/F4; last conclusion F12 with type-specific label | CONV `mw-oberflaeche_v1.md` |
| Tests | every transition service method has a success test; pure methods tested without DB; plausible, readable test data with run timestamp; results accessed via returned objects | CONV `mw-tests_v1.md` § "Was getestet wird", § "Plausible Testdaten" |
| Ubiquitous language German | namespaces, models, services, methods in German | CONV `mw-allgemein_v1.md` |
| Deprecated concepts | `onStartup`/`onShutdown` on modules "nicht mehr zu verwenden (Deprecated)"; `RUN_IN_CONSOLE` checker error; `QueryFromSql`/`UpdateFormSql` deprecated (PR2 P-033); `VslCancelExParam`/`VslCancelMsgParam` deprecated (PR1 P-017) | DUX § "Teil II – Anwendung und Batchjob"; DUX § "Kapitellandkarte: Batchoptionen"; PR2 P-033; PR1 P-017 |

### Inferences
- Several "principles" are compensations for missing language features (explicit loading because no lazy loading; parent-then-children save because no cascade; status instead of boolean).

### Gaps
- None of the documents states a rationale for the absence of domain events or for not offering a boolean type beyond "ManMap kann ihn nicht mappen und DataUX nicht darstellen".

---

## 5. Recurring hand-written patterns

### Takeaway
The documentation and conventions describe at least a dozen structures that every application re-implements by hand per aggregate, per search, or per test model.

### Cited Findings
| Pattern | What the developer writes each time | Where described |
| --- | --- | --- |
| Search filter DTO with results list | DTO with criteria properties plus `results` of type `list<Info-DTO>` (e.g. `RechnungFilter` with `results: list<RechnungInfo>`); constructor sets status properties to `null` for "no filter" | WB § "Gesamtbeispiel: Rechnungsverwaltung" (table "Fachliches Modell mit ObjectFlow"), § "Rechnungen suchen"; PR2 P-034 |
| Search command with two pages or one page plus refresh conclusion | `SEARCH_CMD` with filter page and result page; Page Init loads list from filter DTO; `page <same page>` as refresh | WB § "Rechnungen suchen"; OF § "Page Init und Datenbereitstellung", § "Page Conclusions" |
| Checkout/checkin repository per aggregate | `<Aggregat>Repo` with `checkout(id)` (root + explicit lists/references) and `checkin(entity)`; "das Aggregat-Repository mit Laden, Checkout, Speichern und Löschen" | WB § "Persistenz mit ManMap"; CONV `mw-anwendungsaufbau_v1.md` table row `<bereich>.domain`, § "Empfehlung: Namen der Elemente" |
| Parent-then-children save ordering | "zuerst der Parent gespeichert, dann der Parent-Schlüssel beziehungsweise die Rückreferenz an die Kinder gesetzt und schließlich jedes Kind über sein eigenes `EntityMapping` gespeichert" | MM § "Speichern von Objektgraphen"; MM § "Domänenmodell laden, bearbeiten und speichern" step 6 |
| Children-before-parent delete | explicit delete of children in correct order before parent | MM § "Löschen mit `delete with`" |
| Removed children detection | owner remembers loaded children and deletes those no longer in list in `FINAL OK_CONCLUSION` | PR2 P-041 (project workaround, documented as not a moai topic) |
| Read repository with custom SQL + no-key mapper | `<Thema>LeseRepo` with `SQL query`, `nokeystore/read-only map` to DTO; separate read `Persistence Description` `<Bereich>Lesen` if needed | WB § "Persistenz mit ManMap"; MM § "Lesemodell mit Custom SQL verwenden"; CONV `mw-anwendungsaufbau_v1.md` table row `<bereich>.read`, § "Empfehlung: Namen der Elemente" |
| Dynamic SQL via `if` per criterion | `if` adds `C2SqlText` fragment only when criterion set | MM § "Custom SQL mit `SQL`" |
| `%` placeholder for all-optional `||` groups | caller passes `%` so a `like` group always matches | MM § "Spezifikum - Filterausdrücke und gemappte Felder"; PR2 P-037 |
| Explicit load of references and lists | separate query assigned to property or `refJoin`/`listJoin`; `#Key` + `# Repo.get(...)` when reference not loaded | MM § "Explizites Laden"; OF § "Beziehungen und Objektgraphen" |
| State transition service method | `<Aggregat>Service.freigeben(rechnung)` with Preconditions then status and dependent values; plus pure `...Entscheiden(x, fakten)` variant | CONV `mw-domaenenmodell_v1.md` § "Aggregate und Invarianten", § "Service und Aggregat" |
| Facts DTO for cross-aggregate rules | loading method bundles facts in a DTO in `read` and passes to pure method | CONV `mw-domaenenmodell_v1.md` § "Service und Aggregat"; CONV `mw-anwendungsaufbau_v1.md` § "Abhängigkeiten" ("liest ihn der Aufrufer und übergibt ihn dem Service") |
| Validation-then-mutate block | load facts → `validation` → mutate | OF § "Preconditions, Validation, Guards und Exceptions" |
| Edit DTO between UI and aggregate | `Delegate Form` bound to DTO; command passes values individually to service; input checks via `LENGTH`/`RANGE` | WB § "Rechnung und Positionen bearbeiten"; CONV `mw-anwendungsaufbau_v1.md` § "`domain`, `read` und `unit`" |
| Owner + edit command pair | `GRAPH_OWNER_CMD` with `DISABLED` form holding session; `GRAPH_EDIT_CMD`s with editable forms; revert of shared root in the edit | WB § "Rechnung und Positionen bearbeiten"; CONV `mw-commands_v1.md`; OF § "Revert beim Abbruch" |
| Termination handler merging pushed object | `child cmd term with <Entity>` + `session merge entity pushed into list<> filter.results (in session as readonly)`; for DTO result lists copy values from aggregate into existing/new DTO by hand | OF § "`cmdTermHandler`"; CONV `mw-commands_v1.md` § "Suche und Rückgabe"; WB § "Rechnungen suchen" |
| Scope function setting `#Meta` | load allowed values in `command init`, bind via `setScope`/`setElements`/`setEnabled` in `pageSetScopesFunc` | OF § "Scopes" |
| Double-checkout avoidance | `session entities (keys of checked out)` before repository call, or `#+ with` custom session | OF § "Entities in der Session prüfen", § "Komponenten mit `#` aufrufen" |
| `isAuthenticated` body | explicitly `userEnvironment.setUserName(username)` and `setUserId(...)` resolved via service/repo; also mandatory on `BatchJob Module` though unused headless | OF § "User Environment und User Service"; DUX § "Anwendung mit `AppUI Module`", § "Batchjob mit `BatchJob Module`" |
| Job user context in config | `new instance` `userEnv` (`UserEnvironmentInformation`) with `userName`/`userId` and `userService` (`OFXSimpleUserServices`) | OF § "User Environment und User Service" |
| TestDaten service with CS custom session | `component TestDaten` per `tests` model; methods build graph, `session operation add # Repo.checkin(x) // "..."`, `#CS.COMMIT()`; test calls `#+ with #CS.CREATE() TestDaten.x(...)`; read back in fresh `#+ with #CS.CREATE()` | CONV `mw-tests_v1.md` § "Testdaten mit einer Custom Session anlegen" |
| Get-or-create master data | `TestDaten.zahlungsart("Überweisung")` returns existing or creates | CONV `mw-tests_v1.md` § "Plausible Testdaten" |
| Test repository via `superclass` + `primary instance` | subclass repository overriding methods, selected per test `OFXConfig` | OF § "Repositories im Test ersetzen" |
| Idempotent consumer precondition | re-check in consumer command that unit still needs processing | DUX § "Batchjob mit `BatchJob Module`" |
| Feature flags as `static role` | roles in separate `Roles and Permissions` root | OF § "Rollen, Scopes und Identities" |
| Pure read-only user management | optional user entity + repository in `rollen` | CONV `mw-anwendungsaufbau_v1.md` table row `<firma>.<app>.rollen` |

### Inferences
- The conventions' naming recommendations (`<Aggregat>Repo`, `<Aggregat>Service`, `<Bereich>Persistenz`, `<Bereich>Lesen`, `<Thema>LeseRepo`, `<Bereich>Tests`) are themselves evidence that these artefacts recur identically per Bereich.

### Gaps
- No document quantifies how many of these artefacts a typical Bereich contains.

---

## 6. Language limits users hit in the two problem logs

### Takeaway
Across both runs, the limits users actually hit (as opposed to documentation defects) cluster around: test DSL constraints (`<user_cancel>`, `GRAPH_EDIT_CMD` top-level, `:eq:` in assert, `revert` scope), status/null semantics, `optional` in `||`, MySQL/MariaDB gaps (`BATCH`, sequences), and `CAN_OPEN_RO` semantics.

### Cited Findings (PR1 = problems_run1.md, PR2 = problems_run2.md; one line each)
- PR1 P-014: `revert on FINAL_ / USER_CANCEL` accepts only Command parameters (`IRevertableReference`), not local variables.
- PR1 P-016: ManMap on MySQL/MariaDB ignores `AUTOID` sequence names and requires `AUTO_INCREMENT` columns.
- PR1 P-017: no Page Conclusion concept for a user cancel; cancel only via ESC/close (`FINAL_USER_CANCEL`).
- PR1 P-021: `session operation add` requires the description text `ex` or the generator produces uncompilable code.
- PR1 P-023: `==` between `LocalDate` values generates a Java reference comparison (generator rewrites only `string` and `BigDecimal`); silent business error.
- PR1 P-024: `run command` `<user_cancel>` is only possible for `SEARCH_CMD`; for owner/edit commands checker blocks it and runtime fails.
- PR1 P-025: `assert a :eq: b` in tests generates no check at all (silent test failure; generator fix pending).
- PR1 P-026: `GRAPH_EDIT_CMD` cannot be executed at the top level of a test; only as child in an owner's page.
- PR1 P-032: `OPTIONAL` on `StringDelegate` yields `null`, contradicting the `""` string convention.
- PR1 P-033: `LENGTH` controls mandatory input in the UI; validations were modeled twice.
- PR2 P-011: every status declaration needs exactly one `ON_CREATION` element; a "no value" start for a mandatory status is not expressible as default.
- PR2 P-012: unclear whether a plain `GRAPH_OWNER_CMD` may hold editable forms for a create dialog (resolved by convention).
- PR2 P-013: `OPTIMISTIC_LOCK` needs an undocumented extra column `TCN`.
- PR2 P-026: `session operation add` has no example in the sample module; description text is mandatory.
- PR2 P-030: a violated Precondition in a direct service call throws `OFXAbortedException` and leaves problems on the session so later calls in the same session also fail.
- PR2 P-033: binding a Status from a variable in custom SQL was unclear; SQL text is one node per word ("SQL-Text ist im Modell Wort für Wort ein eigener Knoten"); search was rebuilt as mapped `where`.
- PR2 P-034: a Status property in a filter DTO starts at `ON_CREATION`, not empty; constructor must set `null`.
- PR2 P-037: `optional` in an `||` group becomes `(1 != 1)`; a group of only dropped predicates returns no rows.
- PR2 P-040: `save with ... BATCH` with auto-ID is not implemented on MySQL/MariaDB (`Not implemented yet`).
- PR2 P-041: no documented way for a page-less `GRAPH_EDIT_CMD` to return a value to its owner except push + termination handler; removed children detected by list comparison.
- PR2 P-042: a status-change mask bound directly to the real property forces the command to remember/restore the old status around the service check.
- PR2 P-044: a search does not refresh after an edit; needs an `any cmd term` handler that re-runs the query.
- PR2 P-048: a command whose `generally enabled` fails throws `RuntimeException` in `run command`; `FAIL IN` reported it misleadingly (generator fix pending).
- PR2 P-050: a rule spanning two aggregates collides with the no-cycle convention; resolved by caller passing the fact to the service.
- PR2 P-055: two `TestDaten` services used in one suite break the build because the generator derives the same field name `__testsTestDaten`.
- PR2 P-059: initially unclear whether a `listJoin` child list is sortable (it is, via `sortBy` on child field).
- PR2 P-060: `CAN_OPEN_RO` locks all forms and conclusions; a `SEARCH_CMD` with filter is unusable under RO; `run command` does not reproduce the lock.
- PR2 summary "Lücken in der Doku": also lists P-010/P-018/P-043 (minimal runnable `OFXConfig` undocumented), P-017 (JDBC driver on classpath), P-022 (`INDEX` generates a unique index), P-023 (schema description is Oracle syntax), P-028 (`DateLiteral` defaults to server date), P-029 (`LocalPropertyReference` exists twice).

### Inferences
- Items P-014, P-017, P-024, P-026, P-041, P-042, P-044 (PR1/PR2) all stem from the command/session model having only `done`/`page` transitions and push-based child-to-parent communication.
- Items P-011, P-034 stem from Status being the only enumerated type and requiring a creation default.

### Gaps
- Neither log contains a measured count of hand-written artefacts or model nodes per feature; `improvments.md` and `going_forward.md` concern documentation classification (AST-MUSS/MPS-CONSTRAINT/GENERATOR/RUNTIME/ARCHITEKTUR/EMPFEHLUNG), cross-DSL contracts and DataUX compatibility matrices, not language features (`deprecated/improvments.md` §§ 1–3; `deprecated/going_forward.md`).
