# MoAI – Probleme und Unzulänglichkeiten

Protokoll der Probleme, Lücken und Widersprüche in MoAI (Skills, Dokumentation,
MPS-MCP-Tooling), die beim Bau der PetClinic auftreten. Ziel: Rückmeldung an die
MoAI-Maintainer. Anwendungsfehler, die sich im Projekt beheben lassen, gehören
nicht hierher.

Format je Eintrag:

- **Bereich:** Doku | Skill | MCP-Tool | Sprache/Generator | Laufzeit
- **Beobachtung:** was passiert ist bzw. was fehlt
- **Erwartung:** was stattdessen zu erwarten wäre
- **Workaround:** wie wir weitergemacht haben (falls vorhanden)
- **Schwere:** blockierend | hinderlich | kosmetisch

---

## P-001 Toter Link auf Konventionen-Dokument

- **Bereich:** Doku (`moai/docu/moware-werkbank.md`, Abschnitt „Zusätzliche Informationen“)
- **Beobachtung:** Verweis auf `stuff/konventionen.md`, das im Paket nicht existiert.
- **Erwartung:** Das Dokument ist mitgeliefert, oder der Verweis wird entfernt.
- **Workaround:** Stattdessen die Abschnitte „Schreibkonventionen“ in den einzelnen DSL-Dokus verwenden.
- **Schwere:** hinderlich (Namens- und Modellierungskonventionen bleiben unklar)

## P-002 Uneinheitliche Namen der Command-Typen

- **Bereich:** Doku
- **Beobachtung:** `moware-werkbank.md` spricht von `SEARCH`, `GRAPH_OWNER`,
  `GRAPH_EDIT` und `MODAL_GRAPH_OWNER`, `objectflow.md` dagegen von `SEARCH_CMD`,
  `GRAPH_OWNER_CMD`, `GRAPH_EDIT_CMD` und `GRAPH_OWNER_CMD_MODAL`.
- **Erwartung:** Überall dieselben Bezeichner wie in der Sprachdefinition.
- **Workaround:** Die Sprachdefinition in MPS ist maßgeblich.
- **Schwere:** kosmetisch

## P-003 Unterstützte Datenbanken: MariaDB nicht erwähnt

- **Bereich:** Doku (`moware-werkbank.md`, `manmap.md`)
- **Beobachtung:** Die Doku nennt nur Oracle und MySQL. Die PetClinic-Spezifikation
  verlangt MariaDB. Ob MariaDB als MySQL-Dialekt unterstützt wird (z. B. bei
  Sequences/AUTOID), steht nirgends.
- **Erwartung:** Eine explizite Aussage zu MariaDB, insbesondere zu Sequences.
- **Workaround:** offen (vorläufig wird MariaDB als MySQL behandelt)
- **Schwere:** hinderlich

## P-004 Widersprüchliche Angaben zur Testausführung

- **Bereich:** Doku
- **Beobachtung:** `moware-werkbank.md` (Laufzeitumgebungen) nennt für `OFXTestSuit`
  die MPS-Konsole. Die Spezifikation und der Skill `mps-run-configurations` sehen
  Run-Konfigurationen vor.
- **Erwartung:** Klare Aussage, welcher Weg empfohlen bzw. unterstützt wird.
- **Workaround:** offen
- **Schwere:** kosmetisch

## P-005 MPS_AGENT_GUIDE ist auf Sprachprojekte zugeschnitten

- **Bereich:** Doku (`moai/MPS_AGENT_GUIDE.md`)
- **Beobachtung:** Das Dokument beginnt mit „This is a JetBrains MPS language project“
  und verweist relativ auf `skills/...`. Im Anwendungsprojekt ist beides irreführend,
  denn es handelt sich um ein Anwendungsprojekt und der Pfad wäre `moai/skills/...`.
- **Erwartung:** Formulierung für Konsumentenprojekte bzw. paketrelative Pfade.
- **Schwere:** kosmetisch

## P-006 Laufzeit turkuforms nicht verfügbar

- **Bereich:** Laufzeit / Doku
- **Beobachtung:** Die Doku beschreibt drei Laufzeiten (fx8forms, turkuforms, h2forms).
  Im MPS-Repository sind aber nur `org.modellwerkstatt.fx8forms` und
  `org.modellwerkstatt.h2forms` sichtbar.
- **Erwartung:** Die Doku gibt an, welche Laufzeiten in einer Standardinstallation vorhanden sind.
- **Workaround:** Nur fx8forms bzw. h2forms verwenden.
- **Schwere:** kosmetisch (für v1 ist keine Laufzeit vorgegeben)

## P-007 Beispiel-Solution nicht als `startingPoint` auflösbar

- **Bereich:** MCP-Tool / Skill
- **Beobachtung:** Die Skills verweisen auf `org.modellwerkstatt.dataux.tests` als
  Beispielquelle. `mps_mcp_get_project_structure` mit
  `startingPoint = 3c6ef8ca-…(org.modellwerkstatt.dataux.tests)` bzw. mit dem Namen liefert
  `NOT_FOUND`, weil das Modul nicht zum Projekt gehört. Erst ein vollständiger Dump mit
  `includeStubModules=true` (mehrere MB) zeigt die Verdrahtung.
- **Erwartung:** Der Skill nennt den funktionierenden Weg, oder `startingPoint` akzeptiert
  sichtbare Nicht-Projektmodule.
- **Workaround:** Vollständiger Dump plus Filterung per Skript; `print_node` und
  `query_nodes` mit expliziten Referenzen funktionieren.
- **Schwere:** hinderlich

## P-008 Verdrahtung eines Anwendungsmoduls nicht dokumentiert

- **Bereich:** Doku / Skill
- **Beobachtung:** Weder Doku noch Skills beschreiben, welche Modul-Abhängigkeiten
  (JDK, `objectflow.runtime`, `manmap.runtime`, `dataux.runtime`) und welche Used
  Languages bzw. welches DevKit (`org.modellwerkstatt.MoWareWerkbank`) ein neues
  Anwendungsmodul braucht. Das musste aus der Beispiel-Solution abgeleitet werden.
- **Erwartung:** Ein Abschnitt oder Skill-Rezept „Neues MoWare-Anwendungsmodul anlegen“.
- **Workaround:** Setup von `org.modellwerkstatt.dataux.tests` kopiert.
- **Schwere:** hinderlich

## P-009 `QueryFromMap.readOnly` ist beim Anlegen per JSON implizit `true`

- **Bereich:** Skill (manmap-dsl) / Sprache
- **Beobachtung:** Ohne explizite `readOnly`-Property wird ein neu eingefügter
  `QueryFromMap` als `ReadOnly` erzeugt. Die Beispiel-Checkout-Queries haben im Print
  keine `readOnly`-Property. Wer sie nachbaut, bekommt stillschweigend eine
  ReadOnly-Query in einer CHECKOUT-Methode, und `check_root_node_problems` meldet nichts.
- **Erwartung:** Der Skill weist darauf hin (Blueprint mit `readOnly=false` für Checkout),
  und/oder die Sprache prüft `CHECKOUT`-Methoden ohne Checkout-Query.
- **Workaround:** `readOnly` immer explizit setzen.
- **Schwere:** hinderlich (fachlich gefährlich, fällt erst zur Laufzeit auf)

## P-010 `MappingReference.mappingSource` verweist auf die umgebende Query

- **Bereich:** Skill (manmap-dsl) / MCP-Tool
- **Beobachtung:** Feldreferenzen in `where`/`sortBy` referenzieren als `mappingSource`
  den `QueryFromMap`- bzw. Join-Knoten selbst. Diese Knoten existieren beim Einfügen
  eines JSON-Blueprints noch nicht, deshalb ist eine Query mit Filter nicht in einem
  Schritt einfügbar. Das Blueprint `query-from-map-where-subtree.json` umgeht das mit
  einem „neutralen Filter“; der nötige zweistufige Ablauf wird nicht erklärt.
- **Erwartung:** Der Skill beschreibt den Ablauf: Platzhalter-Filter einfügen,
  Query-Referenz ermitteln, Filter per `SET CHILD` ersetzen. Alternativ könnte das
  Tool blueprint-lokale IDs unterstützen.
- **Workaround:** Platzhalter-StringLiterals einfügen, danach automatisiert ersetzen.
- **Schwere:** hinderlich

## P-011 Entity-/DTO-Blueprints ohne Konstruktor erzeugen nicht kompilierbaren Code

- **Bereich:** Skill (objectflow-dsl) / Sprache / Generator
- **Beobachtung:** Mit `entity-skeleton.json` bzw. `dto-skeleton.json` angelegte Roots
  prüfen fehlerfrei (`check_root_node_problems`: no problems). Der Generator erzeugt aber
  `new ()` (textgen error „null classifier ref in ClassCreator“) in `copy()`, in den
  Mappern und in den Repositories. Ursache: Der Generator verweist auf einen expliziten
  Default-Konstruktor, den die Datenstruktur nicht hat.
- **Erwartung:** Die Blueprints enthalten `public X() {}`, oder die Sprache meldet das
  Fehlen per Checking Rule. Besser noch: Der Generator kommt ohne expliziten
  Konstruktor aus.
- **Workaround:** Leeren `ConstructorDeclaration` in jede Entity und jedes DTO eingefügt.
- **Schwere:** blockierend (Build schlägt fehl, Ursache aus der Meldung schwer ersichtlich)

## P-012 Per JSON angelegte Knoten erhalten nicht die Konzept-Initialwerte

- **Bereich:** MCP-Tool / Skill (alle DSLs)
- **Beobachtung:** Knoten, die mit `insert_root_node_from_json` oder `update_node ADD CHILD`
  angelegt werden, durchlaufen offenbar nicht den Behavior-Konstruktor (`___init___`) des
  Konzepts. Bisher beobachtete Folgen:
  - `QueryFromMap.readOnly` ist `true` (siehe P-009);
  - `Command.newWindowTitleType` wird als `(overwrite predecessor)` projiziert statt mit
    dem dokumentierten Standard `ADDON`;
  - DataUX `IOptionallyNamed` (GridLayout, Table, DelegateForm, TabLayout): `isNamed`
    wird nicht auf `false` gesetzt. Die Elemente gelten deshalb als benannte,
    wiederverwendbare UX-Elemente. Der Generator erzeugt eigene Klassen `_.java`
    (aus dem Namen `#`), und javac scheitert an `_` als Bezeichner. Mit leerem Namen
    stürzt der Generator dagegen ab (`StringIndexOutOfBounds`).
  `check_root_node_problems` meldet in keinem dieser Fälle etwas.
- **Erwartung:** Die MCP-Tools wenden die Konzept-Initializer an (wie der Editor), oder
  Skill und Blueprints setzen die Werte explizit, etwa `isNamed=false`/`name="#"` in allen
  DataUX-Blueprints.
- **Workaround:** Die Properties explizit setzen.
- **Schwere:** blockierend (Build-Fehler bzw. stilles Fehlverhalten)

## P-013 `print_node` zeigt `#` als Namen und verleitet zum Kopieren

- **Bereich:** MCP-Tool / Skill (dataux-dsl)
- **Beobachtung:** Die JSON-Prints der Beispiel-Panes enthalten `{'name': '#'}`, aber kein
  `isNamed`, weil der Default nicht ausgegeben wird. Wer die Struktur nachbaut (wie der
  Skill empfiehlt), übernimmt `#` ohne `isNamed=false`, mit den Folgen aus P-012. Die
  Rolle von `isNamed` steht weder in Doku noch Skill.
- **Erwartung:** Skill und Doku erklären `IOptionallyNamed` (`isNamed`, `name="#"`,
  generierte Named-UX-Klassen).
- **Schwere:** hinderlich

## P-014 `revert` akzeptiert nur Command-Parameter, nicht Variablen

- **Bereich:** Doku (objectflow.md „Revert beim Abbruch“) vs. Sprache
- **Beobachtung:** Laut Doku können „Parameter beziehungsweise Variablen“ unter
  `revert on FINAL_ / USER_CANCEL` stehen. `ContainerVariableReference` wird aber mit
  „Expected concept(s): IRevertableReference“ abgelehnt. Nur `ContainerParamReference`
  implementiert das Interface.
- **Erwartung:** Doku und Sprache stimmen überein.
- **Workaround:** Beim Graph Owner („Owner öffnen“) kein Revert; die Session wird beim
  Abbruch ohnehin verworfen. Die Graph-Edits reverten den Parameter `owner`.
- **Schwere:** hinderlich

## P-015 AppUI-Modul ohne `configuration` lässt den Generator mit NPE abstürzen

- **Bereich:** Sprache/Generator (dataux) / Doku
- **Beobachtung:** Laut Doku dient `configuration` „ausschließlich dem Start mit FX8, aus
  MPS oder im Standalone-Betrieb“, ist strukturell `0..1`, und die Prüfung meldet nichts.
  Ohne Referenz scheitert die Generierung trotzdem mit
  `NullPointerException ... String.replace ... SMethod.invoke(...) is null`
  (input node: AppUiModule).
- **Erwartung:** Eine Checking Rule, die Pflichtfelder meldet, oder ein robuster Generator.
- **Workaround:** `PetClinic Config` angelegt und referenziert.
- **Schwere:** blockierend (Ursache nicht aus der Meldung ersichtlich)

## P-016 ManMap mit MySQL/MariaDB ignoriert AUTOID-Sequences

- **Bereich:** Doku (manmap.md „Automatische IDs und Sequences“)
- **Beobachtung:** Die Doku beschreibt `autoid` ausschließlich als „bezieht vor einem Insert
  den nächsten Wert der angegebenen Sequence“. `MMMySqlDescription` liefert aber
  `needsSequenceSelectPre() = false` und liest die ID nach dem Insert per
  `SELECT LAST_INSERT_ID()`. Der Sequence-Name bleibt dabei unbenutzt; die ID-Spalten
  müssen `AUTO_INCREMENT` sein. Ergänzung zu P-003.
- **Erwartung:** Die Doku beschreibt das dialektabhängige Verhalten (Oracle: Sequence vorher,
  MySQL: Auto-Increment nachher). Für MariaDB wäre ein Dialekt mit echten Sequences
  wünschenswert.
- **Workaround:** Das PetClinic-Schema braucht `AUTO_INCREMENT`-IDs. Die Sequence-Namen
  bleiben laut Spezifikation im Modell, wirken aber nicht.
- **Schwere:** hinderlich (Schema-Anforderung aus der Spezifikation nicht umsetzbar)

## P-017 Keine Page-Conclusion für einen Benutzerabbruch

- **Bereich:** Doku / Sprache
- **Beobachtung:** Die Spezifikation verlangt „Save & Close, Cancel“ als Aktionen. ObjectFlow
  kennt nur `done` und `page` als Übergänge einer Page Conclusion. Ein Abbruch ist nur
  per ESC bzw. Fensterschließen (`FINAL_USER_CANCEL`) möglich. Die Doku sagt nicht,
  wie ein sichtbarer „Abbrechen“-Button zu modellieren ist.
- **Erwartung:** Ein Konzept für eine Cancel-Conclusion oder ein Hinweis in der Doku.
- **Workaround:** Abbrechen per ESC; kein eigener Button.
- **Schwere:** kosmetisch

## P-018 Kein Beispiel und keine Doku für `ReferenceDelegate.scopeText`

- **Bereich:** Skill / Doku (dataux)
- **Beobachtung:** `ReferenceDelegate` verlangt `scopeText` mit ein oder mehr `paths`. Es gibt
  keine Instanz in `org.modellwerkstatt.dataux.tests`, kein Blueprint und keine
  Erklärung, relativ zu welchem Typ die Pfade aufgelöst werden. Ebenso fehlt ein Beispiel
  für `#Meta.setScope` in einer Page-Scope-Funktion mit Referenz-Picker.
- **Erwartung:** Blueprint und Beispiel für Picker plus Scope.
- **Workaround:** Pfade relativ zum Zieltyp angenommen (`PetType.name`, `Vet.lastName`,
  `Vet.firstName`); prüft fehlerfrei, zur Laufzeit ungetestet.
- **Schwere:** hinderlich

## P-019 `FIND_INSTANCES` mit `scope: all` findet die Beispiel-Solution nicht

- **Bereich:** MCP-Tool
- **Beobachtung:** `query_nodes FIND_INSTANCES` für `OFXConfig` mit `scope: "all"` liefert
  `[]`. Mit `scope: "modules"` und expliziter `dataux.tests`-Referenz kommen neun Treffer.
  Auch „all“ umfasst also nur die Abhängigkeitshülle des Projekts; aus dem Namen ist das
  nicht ersichtlich.
- **Erwartung:** Klare Beschreibung des Scopes oder ein Scope für alle sichtbaren Module.
- **Schwere:** kosmetisch

## P-020 MCP-Tools rufen NodeFactories mit `enclosingNode = null` auf, `OFXRunCmdPage` ist nicht anlegbar

- **Bereich:** MCP-Tool (`insert_root_node_from_json`, `update_node ADD CHILD`)
- **Beobachtung:** Jeder Versuch, eine `OFXRunCmdPage` (die „expect page“ eines
  `run command`) anzulegen, scheitert mit
  `OFXRunCmdPage does not support handling of null`, auch als leerer Knoten und auch per
  `ADD CHILD` direkt unter einem vorhandenen `OFXRunCmd`. Ursache ist die NodeFactory
  des Konzepts: Sie erwartet den Parent als `enclosingNode`, das Tool übergibt aber `null`.
  Ohne diese Pages lassen sich keine Command-Tests (`run command`) per MCP bauen.
- **Erwartung:** Das Tool übergibt beim `ADD CHILD` den Parent als `enclosingNode`, und beim
  Root-Insert den jeweiligen Parent im Blueprint.
- **Workaround:** `run command`s ohne Pages einfügen. Leere Pages per MPS-Konsole anhängen:
  `#instances(OFXRunCmd).where({it => it.pages.isEmpty}).forEach({rc => rc.pages.add(new node<OFXRunCmdPage>())})`.
  Danach per `update_node` Name, Page, Conclusion und `beforeConclude` setzen.
  Verschachtelte `run command`s brauchen dafür eine zweite Runde.
- **Schwere:** blockierend (ohne Konsolen-Umweg keine Command-Tests)

## P-021 `SessionOperationAdd.ex` ist optional, wird aber vom Generator verlangt; Semantik undokumentiert

- **Bereich:** Sprache/Generator / Doku (objectflow)
- **Beobachtung:** `session operation add` hat die Kind-Rolle `ex` (`0..1`). Die Doku erklärt
  sie nicht; naheliegend wäre die Ziel-Session. Tatsächlich ist `ex` der Rückgabewert von
  `IOFXSessionOperation.getInformation()`. Fehlt `ex`, erzeugt der Generator `return;` in
  einer `String`-Methode, und javac scheitert. Wird eine Session übergeben, kommt es zu
  einem Typfehler.
- **Erwartung:** Pflichtfeld oder Default im Generator; Doku zur Bedeutung.
- **Workaround:** Beschreibenden String übergeben (z. B. `"OwnerRepository.saveOwner"`).
- **Schwere:** hinderlich

## P-022 Test-Infrastruktur (Testdaten committen, Session-Operationen prüfen) nicht dokumentiert

- **Bereich:** Doku (objectflow „Tests“) / Skill
- **Beobachtung:** Die Doku sagt „Tests committen nicht“ und empfiehlt, persistente
  Erwartungen über „Testdatenaufbau“ zu prüfen, zeigt aber nicht, wie Testdaten in die DB
  kommen. In den Beispielen geschieht das über eigene Sessions
  (`IOFXApplicationFactory.createNewSession`, `#+ with sess …`,
  `startTransactionAndFlush`), anonyme `IOFXSessionOperation`-Klassen und den Umweg über
  `IM3DatabaseDescription.needsIdSelectPost()`. Ebenso fehlt, wie registrierte
  Session-Operationen im Test geprüft werden (`session.getOperations()`).
- **Erwartung:** Ein Rezept „Testdaten anlegen“ und „Session-Operationen prüfen“ im
  Skill bzw. in der Doku.
- **Workaround:** Service `PetClinicTestData` mit `newSession()`/`commit()`; Aufrufe per
  `#+ with sess`; Prüfung über `session.getOperations().get(i).getInformation()`.
- **Schwere:** hinderlich

## P-023 `==` zwischen `LocalDate`-Werten wird als Java-Referenzvergleich generiert, entgegen der Doku

- **Bereich:** Generator / Doku (objectflow „Null-Werte in Datenstrukturen“)
- **Beobachtung:** Laut `objectflow.md` ersetzt ObjectFlow „allgemeine Gleichheits- und
  Ungleichheitsausdrücke durch einen null-sicheren Vergleich … andernfalls wird `equals`
  verwendet“. In der Entity-Methode `Owner.hasDuplicatePet` (Closure in `any`) wurde
  `other.birthDate == candidate.birthDate` (BaseLanguage `EqualsExpression`, per JSON
  eingefügt) aber 1:1 als Java `other.getBirthDate() == candidate.getBirthDate()` generiert.
  Das ist ein Identitätsvergleich zweier Joda-`LocalDate`-Objekte und damit fast immer `false`.
  Weder `check_root_node_problems` noch Make meldeten etwas. Aufgefallen ist es erst zur
  Laufzeit: Der Test „Pet-Dublette wird abgelehnt“ scheiterte (FAIL IN nicht ausgelöst).
  Der Gegentest „anderes Geburtsdatum ist erlaubt“ lief grün, allerdings nur zufällig.
  Dasselbe gilt für `assert a == b` in Tests: Der Generator zerlegt es in
  `leftSide != rightSide`, also ebenfalls in einen Identitätsvergleich bei `LocalDate`.
- **Ungeklärt:** Ob die Ersetzung nur in bestimmten Kontexten greift (z. B. nicht in
  Entity-Methoden/Closures) oder nur bei einem über den Editor eingegebenen `==` (vgl.
  P-012). Die Doku nennt weder den Mechanismus noch das zuständige Konzept.
- **Erwartung:** Entweder greift die Ersetzung überall, oder die Doku beschränkt die Aussage
  und empfiehlt für Datums-/Objektwerte `:eq:` (`NPEEqualsExpression`) bzw. `equals`;
  idealerweise warnt ein Checker bei `==` auf Nicht-Primitiven.
- **Workaround:** `:eq:` (`NPEEqualsExpression`) explizit verwenden; das generiert
  `Objects.equals(…)`. Die Skill-Regel „`:eq:` für Knotengleichheit“ (mps-baselanguage) gilt also
  sinngemäß auch für Objektwerte in ObjectFlow-Code.
- **Schwere:** kritisch (stiller fachlicher Fehler)

## P-024 `run command`: Benutzerabbruch laut Doku möglich, bei Nicht-Such-Commands aber vom Checker blockiert und zur Laufzeit defekt

- **Bereich:** Doku (objectflow „Commands ohne UI ausführen“) / Checker / Runtime
- **Beobachtung:** Die Doku sagt, ein `run command` könne „neben einer regulären Conclusion
  auch den Benutzerabbruch erzwingen“. Der Checker meldet an einer `OFXRunCmdPage` ohne
  `conclusion` (= `<user_cancel>`) jedoch „This is not a search cmd. You should provide a
  conclusion here.“ (Fehler), Make läuft trotzdem durch. Zur Laufzeit gilt:
  - Oberste Ebene (GRAPH_OWNER): `CmdFlow.runWithFlow` wirft nach allen Pages
    `IllegalStateException: GraphOWNER / GraphEDIT Command … still not terminated in final ok`.
    Ein Benutzerabbruch ist dort also nur bei `SEARCH_CMD` zulässig.
  - Child (GRAPH_EDIT in einer Page des Parents): Für den abgebrochenen Child liefert
    `CmdFlow` als Selections `null`, weil nur FINAL_OK bzw. FINAL_CANCEL Selections haben.
    `OFXCommand.handleCmdTermAndClearGeFqName` iteriert ohne Null-Prüfung darüber: NPE
    „cmdSelections is null“ im Term-Handler des Parents. Dieser wird dann per FINAL_CANCEL
    beendet.
- **Folge:** Die Spezifikationsanforderung „Revert bei Abbruch“ lässt sich nicht wie
  dokumentiert über `<user_cancel>` testen.
- **Erwartung:** Doku auf Such-Commands einschränken oder Runtime und Checker für
  Benutzerabbruch bei GRAPH_OWNER/GRAPH_EDIT ertüchtigen (mindestens Null-Prüfung für
  `cmdSelections`).
- **Workaround:** Abbruch über FINAL_CANCEL provozieren: eine Validierung in der Conclusion
  scheitern lassen (z. B. Pflichtfeld leeren und `Ok` erzwingen). Den `run command` in
  `try … catch (OFXJobWorkCanceledException)` fassen und danach Revert bzw. DB-Zustand
  prüfen. Die Revert-Liste gilt laut Doku für FINAL_CANCEL und FINAL_USER_CANCEL gleichermaßen.
- **Schwere:** hinderlich

## P-025 `assert a :eq: b` in Tests generiert keine Prüfung

- **Bereich:** Generator (objectflow Tests)
- **Beobachtung:** Der Test-Generator zerlegt `assert` mit `EqualsExpression` in
  `leftSide`/`rightSide` plus `if (leftSide != rightSide) throw …`. Mit
  `NPEEqualsExpression` (`:eq:`, Workaround aus P-023) erzeugt er zwar beide Variablen,
  aber **keine Prüfung**. Der Assert ist damit stillschweigend wirkungslos, und kein Checker
  warnt.
- **Erwartung:** `:eq:`/`:ne:` im Assert unterstützen oder als Fehler melden.
- **Workaround:** Boolesche Methode verwenden, z. B. `visit.visitDate.isEqual(heute)`.
  Das generiert `if (!(operand.isEqual(param0))) throw …`. Die Joda-Stub-Referenz liegt in
  `org.joda.time.base`, nicht in `org.joda.time`.
- **Schwere:** kritisch (stiller Testausfall)

## P-026 `GRAPH_EDIT_CMD` lässt sich im Test nicht auf oberster Ebene ausführen; nicht dokumentiert

- **Bereich:** Doku (objectflow Tests) / Checker
- **Beobachtung:** `run command` eines `GRAPH_EDIT_CMD` direkt im Testrumpf ist gültig
  modelliert und baut. Zur Laufzeit folgt: `RuntimeException: Command … ist not a session
  owner, but parent session is null! (GE used?)`.
- **Erwartung:** Checker-Fehler bzw. Doku-Hinweis, dass ein Graph-Edit nur als Child eines
  `run command` für einen GRAPH_OWNER laufen kann.
- **Workaround:** Den Graph-Edit in einer Page von „Owner öffnen“ ausführen; dort
  `session.getOperations().size() == 0` prüfen (`session` ist die Session des Owners).
- **Schwere:** hinderlich

## P-027 `check_root_node_problems` mit Modellreferenz meldet „no problems found“, obwohl Roots Fehler haben

- **Bereich:** MCP-Tool
- **Beobachtung:** Mit einer Modellreferenz (`r:…(org.modellwerkstatt.petclinic.tests)`)
  liefert das Tool „no problems found“. Dieselbe Prüfung pro Root findet im selben Modell
  echte Fehler: `<user_cancel>`-Pages (P-024), `List.size()/get()` auf einer MPS-Collection
  und „Variable must be final“. Im `ui`-Modell kommen neun Fehler hinzu (P-028 bis P-030).
  Alle frühen „no problems“-Aussagen dieses Projekts stützten sich auf den Modell-Check und
  waren daher falsch. Make lief trotz dieser Fehler erfolgreich durch.
- **Erwartung:** Der Modell-Check prüft alle Roots, oder das Tool lehnt eine Modellreferenz
  ab bzw. weist auf die Einschränkung hin. Die Skills empfehlen den Check ausdrücklich als
  Validierungsschritt.
- **Workaround:** Jeden Root einzeln prüfen: Roots per `query_nodes FIND_INSTANCES`
  (`INamedConcept`, `isRoot`) ermitteln, dann `check_root_node_problems` pro Root aufrufen.
- **Schwere:** kritisch (falsche Sicherheit)

## P-028 DataUX: `LABEL` am Top-Level-Formular einer Page Pane unzulässig, Doku sagt „Formular und Tabelle“

- **Bereich:** Doku (dataux „Optionen für Formulare und Tabellen“) / Skill-Blueprints
- **Beobachtung:** Laut Doku ist `LABEL` (`LabelFOption`) für Formular und Tabelle erlaubt.
  Am direkten `uxChild` einer Page Pane meldet der Checker jedoch „Label option can not be
  used here, since label will be set via page title.“ Betroffen waren sechs Page Panes.
  Innerhalb von Grid/Tab ist die Option zulässig.
- **Erwartung:** Die Doku nennt die Einschränkung.
- **Workaround:** `LABEL` am Top-Level-Element weglassen; die Beschriftung kommt aus dem
  Seitentitel.
- **Schwere:** lästig

## P-029 DataUX: `PICKER` an `ReferenceDelegate` unzulässig, Doku legt ihn nahe

- **Bereich:** Doku (dataux „Delegate-Optionen“)
- **Beobachtung:** Die Doku beschreibt `PICKER` als Formular-Option („Verwendet nach
  Möglichkeit eine Auswahlkomponente“), ohne Einschränkung auf Delegate-Typen. Für eine
  Referenzauswahl (Tierart, Tierarzt) liegt sie nahe. Am `ReferenceDelegate` meldet der
  Checker: „Node '(instance of PickerDOption)' cannot be child of node '(instance of
  ReferenceDelegate)'“. Es fehlt eine Zuordnung, welche Delegate-Option zu welchem
  Delegate-Typ passt.
- **Erwartung:** Tabelle „Option × Delegate-Typ“ in Doku bzw. Skill.
- **Workaround:** Option entfernen; der `ReferenceDelegate` bringt ohnehin eine Auswahl mit.
- **Schwere:** lästig

## P-030 DataUX: Scope von `boundClassifier` weicht von der Doku zum Selektionskontext ab

- **Bereich:** Doku (dataux „Datenbindung und Selektion“, „Master-Detail“) / Checker
- **Beobachtung:** Die Doku sagt, jede Page Pane habe einen gemeinsamen Selektionskontext,
  und ein an einen Typ gebundenes Formular zeige dessen aktuelle Selektion, unabhängig
  davon, woher sie stammt. Der Scope (`OFXGetSelectedScoper.scopeForBindableObjects`) lässt
  aber nur Inhaltstypen **vorheriger Geschwister** sowie **bindbarer Vorfahren** zu. Tabs
  und Grid-Layouts sind keine bindbaren Vorfahren. Ein `Delegate Form` für `Pet` im Tab
  „Visits“ sieht deshalb die Pet-Tabelle im vorherigen Tab „Owner“ nicht: Fehler „out of
  search scope“. Make läuft trotzdem durch.
- **Erwartung:** Die Doku beschreibt die Reihenfolge- und Hierarchieregel, oder der Scope
  berücksichtigt vorherige Geschwister auch über Tab-/Grid-Grenzen.
- **Workaround:** Im selben Tab vor dem Detail-Element ein Element mit dem gewünschten
  Inhaltstyp platzieren. Hier ersetzt eine Pet-Tabelle (gemeinsame Selektion) das
  Pet-Formular im Tab „Visits“.
- **Schwere:** hinderlich

## P-031 Skill-Nutzung: DataUX wurde nicht überproportional genutzt, aber Fallen fehlen in Skills und Trigger

- **Bereich:** Skills (objectflow-dsl, manmap-dsl, dataux-dsl) / Doku; Auswertung des
  Session-Transkripts `121da1af…jsonl`. Die drei übrigen Transkripte sind Neben-Sessions
  ohne Skill-Nutzung.
- **Beobachtung (gemessen):**
  - Jeder DSL-Skill wurde genau **einmal** per `Skill` geladen. Nach der Kompaktierung
    wurde jeder einmal automatisch neu eingespielt (SKILL.md: objectflow 5,6 k,
    dataux 6,7 k, manmap 4,3 k Zeichen).
  - **Lesezugriffe (Skill-Referenzen plus Doku)**, von rund 1,55 Mio. Zeichen Tool-Ergebnissen
    insgesamt:

    | Sprache    | Zugriffe | Zeichen | ≈ Tokens | Anteil an allen Tool-Ergebnissen |
    |------------|---------:|--------:|---------:|---------------------------------:|
    | ObjectFlow |       16 |   177 k |     44 k |                           11,5 % |
    | DataUX     |       12 |    89 k |     22 k |                            5,7 % |
    | ManMap     |        5 |    82 k |     21 k |                            5,3 % |

    Meistgelesen je Sprache:
    - ObjectFlow: `docu/objectflow.md` dreimal vollständig bzw. in großen Teilen
      (133 k Zeichen); `references/*.md` plus alle Blueprints in einem Block (37 k).
    - DataUX: `docu/dataux.md` (71 k); `concepts`, `sandbox`, `workflows` und `gotchas`
      in einem Block (27 k); die Blueprints `page-pane-form-skeleton` und
      `tab-layout-subtree` (3 k).
    - ManMap: `docu/manmap.md` einmal (51 k); `references/*.md` (26 k); fünf
      Repository-Blueprints (5 k).
  - **MCP-Arbeit** am Modell, nach Sprache klassifiziert:

    | Sprache    | Aufrufe | Zeichen |
    |------------|--------:|--------:|
    | ObjectFlow |     175 |   401 k |
    | DataUX     |      41 |   121 k |
    | ManMap     |      30 |    82 k |

    Das `ui`-Modell hat das größte Volumen (250 k), überwiegend wegen der 14
    ObjectFlow-Commands, nicht wegen der Page Panes.
  - **Eigene Generator-Skripte** (Wissen außerhalb der Skills):
    - gen_tests 25 k, gen_cmds 11 k und gen_logic 8 k (ObjectFlow);
    - gen_repos 7 k und gen_pers 2 k (ManMap);
    - gen_ui 6 k (DataUX);
    - `bl.py` 23 k (BaseLanguage-AST).
  - **Umfang der Skills** ist nahezu gleich:

    | Skill          | SKILL.md | references/*.md | Blueprints     |
    |----------------|---------:|----------------:|---------------:|
    | objectflow-dsl |    5,7 k |          28,5 k | 6,4 k (10 Dateien) |
    | manmap-dsl     |    4,5 k |          25,9 k | 10,9 k (15 Dateien) |
    | dataux-dsl     |    6,8 k |          28,1 k | 10,0 k (8 Dateien) |

    Bei jedem Laden kommt nur die SKILL.md in den Kontext; die Doku `objectflow.md` ist
    mit 137 k fast dreimal so groß wie `dataux.md` (53 k).
- **Befund zur Ausgangsfrage:** DataUX wurde **nicht** häufiger oder umfangreicher genutzt
  als ObjectFlow. ObjectFlow liegt in allen Messgrößen vorn, DataUX knapp vor ManMap. Der
  Eindruck entsteht vermutlich aus drei Gründen:
  1. Die späten, sichtbaren Nacharbeiten betrafen DataUX (P-028 bis P-030, fünf gezielte
     `dataux.md`-Zugriffe zwischen 12:35 und 12:36).
  2. Die Commands liegen im `ui`-Modell und werden als „UI-Arbeit“ wahrgenommen.
  3. Die DataUX-SKILL.md ist die größte der drei und wird nach jeder Kompaktierung
     mitgeschleppt.
- **Ursachen für Nachschlagen und Umwege (Belege aus dem Transkript):**
  1. **Fallen, die in keinem Skill stehen**; die Zählung erfasst Erwähnungen in
     Tool-Ein- und -Ausgaben.
     - DataUX:
       - `isNamed`/`name="#"`: 71 Erwähnungen, entdeckt über einen Generatorfehler (P-012/013).
       - LABEL am Top-Level-Formular: 36; PICKER an `ReferenceDelegate`: 20
         (beide erst durch die Prüfung einzelner Roots, P-028/029).
       - Scope von `boundClassifier`: 9, ermittelt aus dem `-src.jar` (P-030).
       - AppUi ohne `configuration`: NPE im Generator (P-015).
     - `gotchas.md` von dataux-dsl nennt nur `scopeText`-Kardinalität und Tabellenbindung.
     - ObjectFlow:
       - Seiten von `run command`-Tests (`OFXRunCmdPage`): 310 Erwähnungen (P-020).
       - `user_cancel`: 86 (P-024); `revert`: 69 (P-014); `readOnly`: 64 (P-009);
         `SessionOperationAdd.ex`: 26 (P-021).
       - `==` bei `LocalDate` (P-023).
  2. **Wissen fehlte und wurde geraten, danach zur Laufzeit korrigiert:** P-021 bis P-026
     widersprechen der Doku oder fehlen darin. Die Klärung lief über Laufzeitquellen
     (`moware/objectflow/.../CmdFlow.java`, `OFXCommand.java`), nicht über Skills.
  3. **Überschneidung ObjectFlow/DataUX:** Commands, Pages und Conclusions (ObjectFlow)
     leben im selben Modell wie die Page Panes (DataUX). Die Trigger beider Skills nennen
     „pages“, sodass die Zuständigkeit für Page-Controller unscharf ist.
  4. **Anzahl modellierter Knoten** ist kein Haupttreiber: 9 Page Panes gegenüber
     14 Commands und 44 Tests.
  5. **Gegenprobe ManMap:** Wenig Nachschlagen, weil die Arbeit über `mps-baselanguage`
     (Stub-Referenzen) und eigene Generatoren lief. Die ManMap-Fallen (P-009, P-010, P-016)
     fielen erst beim Build bzw. in der Runtime-Beschreibung auf, nicht in der Doku.
- **Erwartung / Verbesserungsvorschläge für MoAI:**
  - Die wichtigsten Fallen je DSL als kurze Liste direkt in die SKILL.md (Top 5–8),
    nicht nur in `references/gotchas.md`:
    - DataUX: `isNamed=false` plus `name="#"` für innere Elemente; kein LABEL am
      Top-Level-Element; PICKER nicht an `ReferenceDelegate`; Scope-Regel für
      `boundClassifier` (vorherige Geschwister bzw. bindbare Vorfahren, Tabs und Grids
      zählen nicht); AppUi braucht `configuration`.
    - ObjectFlow: `readOnly` an Checkout-Queries explizit setzen; `newWindowTitleType`
      setzen; `SessionOperationAdd.ex` ist Pflicht; `==`/`:eq:` bei Objektwerten;
      `run command` nur mit FINAL_OK bei Nicht-Such-Commands; ein GRAPH_EDIT nur als Child.
  - Die Tabelle „Option × Delegate-Typ“ und die Tabelle „Konzept-Initializer, die per
    JSON nicht greifen“ (P-012) in die Skills aufnehmen.
  - Fehlende Rezepte in objectflow-dsl: Testdaten anlegen und committen,
    Session-Operationen prüfen, Abbruch/Revert testen (P-022, P-024), Laden eines
    Aggregats mit OPPOSITE-Rückreferenz (`#Key`).
  - Fehlende Rezepte in manmap-dsl: MySQL/MariaDB (AUTO_INCREMENT statt Sequence,
    TCN-Spalte), zweistufiges Setzen von `mappingSource`.
  - Trigger schärfen: objectflow-dsl ausdrücklich für „Commands, PageCrtl, Page
    Conclusions, run command“, dataux-dsl ausdrücklich nur für „PagePane-Layout,
    Delegates, Menüs, AppUi“.
  - Validierungsschritt in allen Skills auf „`check_root_node_problems` pro Root“
    ändern (P-027).
- **Workaround:** Vor dem Modellieren `references/gotchas.md` und `problems.md` lesen;
  nach jeder Änderung jeden Root einzeln prüfen.
- **Schwere:** hinderlich

## P-032 DataUX: `OPTIONAL` am `StringDelegate` liefert `null`, widerspricht der `""`-Initialisierung; nicht dokumentiert

- **Bereich:** Doku (dataux „Delegate-Optionen“, objectflow „Null-Werte in Datenstrukturen“) /
  Skill dataux-dsl
- **Beobachtung:** Laut Entwickler setzt ein `StringDelegate` mit `OPTIONAL` den Wert auf
  `null`, sobald `delegateWert.trim()` leer ist. Das passt nicht zur ObjectFlow-Konvention,
  dass `string` als `""` initialisiert wird und nicht durch `null` ersetzt werden soll, und
  wird praktisch nie gewünscht. Die Doku beschreibt `OPTIONAL` nur allgemein („Wert darf
  fehlen beziehungsweise `null` sein“). Sie nennt weder den String-Sonderfall noch, für
  welche Delegate-Typen `OPTIONAL` gedacht ist (Referenz, Status, Datum). Die einzige
  Aussage zum Pflichtverhalten der Oberfläche steht in `objectflow.md` Z. 120, nicht in
  `dataux.md`; der Skill dataux-dsl erwähnt das Thema gar nicht.
- **Folge im Projekt:** Die Filterfelder des Suchformulars erhielten `OPTIONAL`. Damit
  kommen leere Filter als `null` statt `""` an, und `searchOwners` prüft defensiv auf
  beides. `normalize()` enthält zusätzlich eine überflüssige Null-Prüfung.
- **Erwartung / Ort in der Doku:**
  - `dataux.md`, Abschnitt „Formulare, Tabellen und Delegates“: ein eigener Unterabschnitt
    „Pflichtwerte, leere Eingaben und `null`“. Welcher Delegate-Typ liefert wann `null`
    oder `""`? `OPTIONAL` nur für Referenz, Status und Datum/Zeit; ausdrücklich nicht für
    `StringDelegate`, mit Begründung.
  - Tabelle „Delegate-Optionen“, Zeile `OPTIONAL`: die Spalte „Element“ auf die
    zulässigen Delegate-Typen einschränken und auf den Unterabschnitt verweisen.
  - `objectflow.md` Z. 120: den DataUX-Satz durch einen Verweis auf diesen Unterabschnitt
    ersetzen, damit das Pflichtverhalten der Oberfläche nur an einer Stelle beschrieben ist.
  - dataux-dsl `references/gotchas.md` und die SKILL.md-Regeln: „Kein `OPTIONAL` an
    `StringDelegate`“.
- **Workaround:** `OPTIONAL` an `StringDelegate` weglassen; Pflicht oder Nicht-Pflicht
  über `LENGTH` steuern (siehe P-033).
- **Schwere:** hinderlich (still falsche Werte)

## P-033 `LENGTH` steuert die Pflichteingabe in der Oberfläche; Rolle undokumentiert, Validierungen doppelt modelliert

- **Bereich:** Doku (objectflow „Business Property Optionen“, dataux Delegates, objectflow
  „Preconditions, Validation …“) / Skills objectflow-dsl und dataux-dsl
- **Beobachtung:** Laut Entwickler regelt die Property-Option `LENGTH[min-max]`, ob ein
  String-Wert in der Oberfläche zwingend ist (`min ≥ 1`) oder leer bleiben darf
  (`min = 0`) und wie lang er höchstens sein darf. Die Doku enthält dazu nur eine
  Tabellenzeile in `objectflow.md` Z. 72 („Beschreibt minimale und maximale Länge eines
  Strings“). Dass die Oberfläche `LENGTH` durchsetzt, steht weder dort noch in `dataux.md`.
  Ebenso fehlt das Trim-Verhalten. Laut Entwickler trimmt der `StringDelegate` nur für die
  Leer-Prüfung und übernimmt den Wert ungetrimmt. Eine fachliche Trim-Regel (hier
  Spezifikation 3.3) muss daher weiterhin im Modell umgesetzt werden, z. B. durch
  `normalize()` vor der Validierung, ohne Null-Prüfung.
  Folge: Ich habe in `PetClinicService.validate…` Pflicht- und Maximallängen je Feld
  zusätzlich als `validation` modelliert, samt Regeltests dafür. Nach Aussage des
  Entwicklers ist das überflüssig, außer die Regel ist fachlich hochrelevant. Das
  Suchformular bekam `OPTIONAL` statt `LENGTH[0-…]` (P-032).
- **Erwartung / Ort in der Doku:**
  - `objectflow.md`, Tabelle der Business-Property-Optionen, Zeile `LENGTH`: Wirkung
    ergänzen (Pflichteingabe und Maximallänge im UI, `min = 0` heißt optional) mit
    Verweis auf DataUX.
  - `dataux.md`, im neuen Unterabschnitt „Pflichtwerte, leere Eingaben und `null`“
    (P-032): `LENGTH` als Mechanismus für String-Delegates beschreiben, inklusive
    Trim-Verhalten (Trim nur für die Leer-Prüfung; der gespeicherte Wert bleibt
    ungetrimmt).
  - `objectflow.md`, Abschnitt „Preconditions, Validation, Guards und Exceptions“: eine
    Leitlinie, dass `LENGTH`-Grenzen nicht erneut als Validierung modelliert werden, außer
    bei fachlich zwingenden Regeln oder Eingaben ohne UI (Batch, Schnittstellen).
  - objectflow-dsl `workflows.md` (Rezept Domänenstruktur) und dataux-dsl `gotchas.md`
    jeweils mit einem Satz.
- **Workaround:** Pflicht und Länge von Strings über `LENGTH` modellieren. Im Service
  bleiben nur fachliche Regeln (Datum nicht in der Zukunft bzw. nicht vor der Geburt,
  Pet-Dublette, PetType-Eindeutigkeit). Pflichtangaben für Referenzen und Datum setzt die
  Oberfläche ohne `OPTIONAL` selbst durch.
- **Stand im Projekt:** Nur dokumentiert, noch nicht umgesetzt (Entscheidung des
  Entwicklers). Offen sind:
  - `OPTIONAL` aus dem Suchformular entfernen und `LENGTH[0-n]` an `OwnerSearchCriteria`
    bzw. `VetSearchCriteria` setzen;
  - Pflicht- und Längenvalidierungen samt Regeltests entfernen;
  - `normalize()` ohne Null-Prüfung und `hasDuplicatePet` ohne erneutes `trim()`.
- **Schwere:** hinderlich (doppelte Logik, überflüssige Tests)
