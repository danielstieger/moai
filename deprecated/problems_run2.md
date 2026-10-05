# Protokoll Run 2: Unklarheiten, Probleme, Unzulänglichkeiten

Laufendes Protokoll des Agenten beim Bau der Fuhrpark-Applikation mit der MoAI-Umgebung. Jeder Eintrag entsteht sofort, wenn die Unklarheit auftritt, und wird nachgetragen, sobald klar ist, wie es ausging.

Format je Eintrag: **Stelle** (Datei, Skill, Tool), **Unklar/Problem**, **Annahme**, **Ausgang**.

---

## P-001: Umfang in CLAUDE.md und specs/README.md widerspricht dem Auftrag

- **Stelle:** `CLAUDE.md` (Arbeitsweise, erster Punkt), `specs/README.md` (Absatz „Aktueller Umfang“)
- **Unklar/Problem:** Beide Dateien sagen, die Schritte 5 bis 8 werden nicht gestartet und das Produkt wird nicht gebaut. Der Auftrag vom 2026-10-05 lautet, die Applikation zu bauen.
- **Annahme:** Der Auftrag des Nutzers gilt, die beiden Stellen sind veraltet und werden angepasst, sobald der Nutzer das Vorgehen bestätigt.
- **Ausgang:** Nutzer hat bestätigt, beide Stellen am 2026-10-05 auf den Umfang bis Schritt 8 umgestellt.

## P-002: Schreibweise „furhpark“ und „fuhrpark“ gemischt

- **Stelle:** Verzeichnisse `claudefurhpark` und `solutions/org.modellwerkstatt.mjfurhpark`, Solution `org.modellwerkstatt.mjfuhrpark`, Marketplace `mjfuhrpark-local`
- **Unklar/Problem:** Ich hatte aus dem Verzeichnisnamen geschlossen, die Solution heiße „mjfurhpark“. Die `.msd` und MPS nennen sie `org.modellwerkstatt.mjfuhrpark`; nur die beiden Verzeichnisse haben den Buchstabendreher.
- **Annahme:** Modell- und Solution-Namen verwenden „mjfuhrpark“. Die Verzeichnisnamen bleiben, wie sie sind.
- **Ausgang:** Meine erste Aussage an den Nutzer war falsch und ist hiermit berichtigt. Ob das Solution-Verzeichnis umbenannt wird, entscheidet der Nutzer (siehe P-004).

## P-003: Solution ohne Modelle, nicht versioniert

- **Stelle:** `solutions/org.modellwerkstatt.mjfurhpark/`, `.mps/`
- **Unklar/Problem:** Die Solution enthält nur die `.msd`, keine Modelle, keine Abhängigkeiten, kein DevKit. `solutions/` und `.mps/` sind nicht in Git.
- **Annahme:** Modelle und Abhängigkeiten legt der Agent über die MPS-MCP-Werkzeuge an.
- **Ausgang:** Am 2026-10-05 über MCP erledigt: Abhängigkeit auf `JDK`, Modelle `base`, `testbase`, `benutzer.domain`, `fahrzeug.domain` mit DevKit. Das Solution-Verzeichnis heißt inzwischen `solutions/org.modellwerkstatt.mjfuhrpark` (während der Sitzung vom Nutzer oder von MPS umbenannt), die Modelldateien sind in Git vorgemerkt.

## P-004: Vorhandene Solution passt nicht zur Konvention

- **Stelle:** `moai/conventions/moware-werkbank-anwendung_v1.md` (Tabelle der Ebenen), Solution `org.modellwerkstatt.mjfuhrpark`
- **Unklar/Problem:** Die Konvention verlangt die Solutions `<firma>.<app>.base`, `<firma>.<app>.<boundedcontext>` und `<firma>.<app>.app`. Vorhanden ist eine einzige Solution `org.modellwerkstatt.mjfuhrpark`, die keiner Zeile der Tabelle entspricht. Die Konvention sagt nicht, was mit einer solchen Start-Solution geschehen soll, und nicht, ob der Agent Solutions anlegen darf oder ob das ein Schritt des Entwicklers ist (Q13 sagt: das MPS-Projekt legt der Nutzer an).
- **Annahme:** Der Agent legt `org.modellwerkstatt.mjfuhrpark.base`, `.fuhrpark` und `.app` neu an. Die vorhandene leere Solution bleibt unberührt und ungenutzt; der Nutzer löscht sie oder gibt sie frei.
- **Ausgang:** Der Nutzer liest es am 2026-10-05 anders: Die eine Solution `org.modellwerkstatt.mjfuhrpark` ist die Anwendung, `base`, Bereiche und `app` sind Modelle darin. Die Konvention sagt dagegen wörtlich „jeder Bounded Context ist eine MPS-Solution“ und führt in der Spalte „Solution“ drei Namen; `moware-werkbank.md` sagt „Eine Anwendung besteht aus mehreren MPS-Solutions“. Konventionstext und Erwartung des Autors gehen hier auseinander. **Entscheidung des Nutzers:** eine Solution, alles Modelle; die Konvention muss angepasst werden (Fall „Anwendung mit einem Bounded Context“). Meine Folgeannahme: Modellnamen ohne eigenes Segment für den Bounded Context, also `org.modellwerkstatt.mjfuhrpark.fahrzeug.domain`, weil die Solution selbst der Bounded Context ist. Die Konvention sollte auch das festlegen.
- **Stand:** erledigt (`conventions/moware-werkbank-anwendung_v1.md`: eine Solution bei einem Bounded Context, sonst eine Solution je Bounded Context; Tabelle beschreibt nur noch Modelle, Segment `<boundedcontext>` entfällt bei einem Bounded Context; `moware-werkbank.md` „Solutions anlegen“ angeglichen)

## P-005: Ort für Rollen, wenn es keinen Bereich „Benutzer“ gibt

- **Stelle:** `moai/conventions/moware-werkbank-anwendung_v1.md`, Zeile Aggregat-Bereich `domain`: „im Bereich für Benutzer auch Roles and Permissions“
- **Unklar/Problem:** Die Konvention setzt einen Bereich für Benutzer voraus. Die Specs kennen keinen Benutzerstamm, brauchen aber die Rollen Fuhrparkleiter und Disponent (FR-024). Unklar ist, ob dafür ein Bereich `benutzer` nur mit Rollen entstehen soll oder ob die Rollen nach `base` gehören. Offen ist auch, woran eine Rolle erkannt wird (Q9: „Anmeldung der Werkbank“), die Doku beschreibt nur die Mechanik (`is(userEnvironment)`).
- **Annahme:** Aggregat-Bereich `benutzer` mit einem `domain`-Modell, das nur `Roles and Permissions` enthält. Die Rolle wird in der Demo aus dem Benutzernamen abgeleitet.
- **Ausgang:** Nutzer bestätigt am 2026-10-05: `benutzer` ist ein Modell (`…mjfuhrpark.benutzer.domain`). Die Konvention sollte sagen, wohin Rollen gehören, wenn es keinen Benutzerstamm gibt.
- **Stand:** erledigt (`conventions/moware-werkbank-anwendung_v1.md`, Zeile `domain`: Roles and Permissions liegen im Aggregat-Bereich `benutzer`, auch wenn er sonst nichts enthält)

## P-006: Laufzeit und Datenbank nicht festgelegt

- **Stelle:** `specs/research/open-questions.md` Q10, Q11 („keine Annahme“)
- **Unklar/Problem:** Ohne Datenbank laufen keine Tests, ohne Laufzeit keine Anwendung. Auf der Maschine sind `mysql`/`mariadb` installiert, der Dienst läuft nicht. In MPS sind laut Doku nur `fx8forms` und `h2forms` verfügbar.
- **Annahme:** MariaDB lokal, Laufzeit `fx8forms`. Dienst starten, Datenbank und Benutzer anlegen sind Schritte des Entwicklers.
- **Ausgang:** Nutzer bestätigt am 2026-10-05: `fx8forms` und MariaDB. Als Verbindungsdaten hat der Nutzer einen Konfigurationsausschnitt ohne Begleittext geschickt (Datenbank `test` auf `localhost`, Benutzer `dan`). Ich habe das als „diese Werte verwenden“ gedeutet und `url`, `username` und `password` in `FuhrparkTestKonfiguration` entsprechend gesetzt.

## P-007: `mps_mcp_list_open_projects` scheitert ohne `projectPath`

- **Stelle:** `moai/MPS_AGENT_GUIDE.md` („Selecting the MPS Project“), Skills `objectflow-dsl`, `manmap-dsl`, `dataux-dsl` („Determine the target MPS project dynamically with `mps_mcp_list_open_projects`“)
- **Unklar/Problem:** Der Aufruf ohne Argument endet mit „Unable to determine the target project“, obwohl genau ein Projekt offen ist. Das Werkzeug, das das Projekt ermitteln soll, braucht selbst schon den Projektpfad. Die offenen Projekte stehen nur in der Fehlermeldung.
- **Annahme:** Projektpfad ist das Arbeitsverzeichnis; ich gebe `projectPath` bei jedem Aufruf mit.
- **Ausgang:** Mit `projectPath` funktionieren die Aufrufe. Der Hinweis fehlt in Guide und Skills.

## P-008: Constitution ist nur ein Entwurf

- **Stelle:** `specs/constitution.md`, Zeile „Status: Entwurf, noch nicht freigegeben“
- **Unklar/Problem:** Pläne und Tasks werden gegen die Constitution geprüft, sie selbst ist nicht freigegeben. Ihr Abschnitt „Offen“ verweist auf Q10 bis Q12, Q12 ist inzwischen beantwortet.
- **Annahme:** Die Constitution gilt in der vorliegenden Fassung.
- **Ausgang:** Weiter offen am Ende des Laufs: Die Constitution steht auf „Entwurf“. Beide Pläne wurden gegen die vorliegende Fassung geprüft; die Freigabe liegt beim Nutzer.

## P-009: `tech-stack.md` beschreibt einen veralteten Stand der Umgebung

- **Stelle:** `specs/research/tech-stack.md`, Abschnitt „Stand der Umgebung“
- **Unklar/Problem:** Dort steht, der MCP-Server `mps-mcp` sei nicht erreichbar, und die drei DSL-Dokus und Skills seien noch nicht gelesen.
- **Annahme:** keine nötig
- **Ausgang:** Am 2026-10-05 ist `mps-mcp` erreichbar, das Projekt offen, das DevKit `org.modellwerkstatt.MoWareWerkbank` sichtbar. Die Dokus sind gelesen. Der Abschnitt wird mit Plan 001 nachgezogen.

## P-010: Mindestinhalt einer lauffähigen `OFXConfig` ist nicht dokumentiert

- **Stelle:** `moai/docu/objectflow.md`, „Konfiguration mit `OFXConfig`“; Beispiel `Defaults` in `org.modellwerkstatt.objectflow.tests.config`
- **Unklar/Problem:** Die Doku erklärt die Konfigurationsknoten, aber nicht, welche Instanzen eine Anwendung oder Testsuite mindestens braucht (DataSource, Transaktionsmanager, `databaseDesc`, Type Handler, String-Formatter, User Environment, AppFactory je Laufzeit). Das Beispiel `Defaults` zeigt sie, ist aber auf Oracle und eine fremde Umgebung zugeschnitten (fremde Hostnamen, Benutzer und Passwörter im Klartext). Die Klasse der Datenbankbeschreibung für MySQL/MariaDB und die AppFactory für `fx8forms` nennt die Doku nicht.
- **Annahme:** Die Konfiguration wird aus `Defaults` und der im Beispielmodul referenzierten `LocalMySqlCONFIG` abgeleitet.
- **Ausgang:** Am 2026-10-05 bestätigt: Mit der aus den Beispielen abgeleiteten Liste (P-018) läuft die Testsuite gegen MariaDB. Die Liste gehört in die Doku.

## P-011: Pflicht-Status ohne Vorbelegung

- **Stelle:** `moai/docu/objectflow.md`, „Null-Werte in Datenstrukturen“ und „Status“; Spec 001 AC-1.4
- **Unklar/Problem:** Eine Status-Property startet mit dem Default- beziehungsweise `ON_CREATION`-Element. AC-1.4 verlangt, dass eine leer gelassene Fahrzeugklasse abgelehnt wird. Die Doku sagt nicht, welches Element ohne `ON_CREATION` der Default ist und ob eine Status-Property ohne `ALLOW_NULL_PERSISTANCE` im Speicher `null` sein darf.
- **Annahme:** Der Command setzt Fahrzeugklasse, Nutzungsart und Antriebsart beim Anlegen auf `null`; der Service prüft auf `null`; persistiert wird nie `null`.
- **Ausgang:** Teilweise geklärt am 2026-10-05: MPS meldet „You have to specify exactly one status element with 'on creation'“. Jede Statusdeklaration braucht also zwingend genau ein `ON_CREATION`-Element; die Doku stellt die Option als optional dar, und der Blueprint `status-subtree.json` zeigt sie ohne Hinweis auf die Pflicht. Ich habe `Pkw`, `FestZugeordnet` und `Benzin` als Startwerte gesetzt. Ob der Command sie zum Anlegen auf `null` setzen kann, ist weiter offen (AC-1.4). Nachtrag: Ein Status lässt sich im Speicher gegen `null` prüfen (`fahrzeug.fahrzeugklasse != null` wird ohne Fehler akzeptiert). Ob die Oberfläche einen leeren Status liefern kann, zeigt sich erst mit dem Command.
- **Stand:** teilweise erledigt (`objectflow.md` „Status“: `ON_CREATION` ist Pflicht, genau ein Element je Statusdeklaration; Startwert-Tabelle nennt nur noch das `ON_CREATION`-Element. Offen: ob und wo eine Status-Property im Speicher `null` sein soll, siehe P-034)

## P-012: Anlegen als modaler Owner oder als Owner mit Edit-Command

- **Stelle:** `moai/docu/objectflow.md`, „Die vier Command-Typen“
- **Unklar/Problem:** Laut Doku hält ein `GRAPH_OWNER_CMD` meist nur Session und Navigation, die editierbare Maske öffnet ein `GRAPH_EDIT_CMD`; ein `GRAPH_OWNER_CMD(modal)` „kann selbst editierbare Delegates enthalten“. Für einen einfachen Anlegen-Dialog bleibt offen, welches Muster gemeint ist und ob ein normaler Owner editierbare Formulare haben darf.
- **Annahme:** „Fahrzeug anlegen“ ist ein `GRAPH_OWNER_CMD(modal)` mit eigenem Formular. Das Bearbeiten läuft über einen Owner mit `GRAPH_EDIT_CMD`s.
- **Ausgang:** Am 2026-10-05 bestätigt: `Fahrzeug anlegen` als `GRAPH_OWNER_CMD(modal)` mit eigenem Formular wird von der Prüfung akzeptiert und läuft im Test über `run command` (Anlegen, Ablehnung bei fehlender Marke, sofort aktiv). In der Oberfläche ist es noch nicht ausprobiert.

## P-013: `OPTIMISTIC_LOCK` empfohlen, Voraussetzungen nicht beschrieben

- **Stelle:** `moai/docu/manmap.md`, „Felder, Schlüssel und Optionen“ und „Optimistic Locking und Audit“; `objectflow.md` nennt eine „TCN“
- **Unklar/Problem:** Die Option ist für neue Mappings empfohlen. Nicht beschrieben ist, ob sie eine eigene Property oder Spalte braucht und wie diese heißt.
- **Annahme:** Beide Mappings erhalten `OPTIMISTIC_LOCK`; was dafür nötig ist, kläre ich an der Sprachdefinition.
- **Ausgang:** Geklärt am 2026-10-05 über die generierte Schemabeschreibung: `OPTIMISTIC_LOCK` braucht keine Property im Modell, erzeugt aber eine zusätzliche Spalte `TCN NUMBER (9) NOT NULL` je Tabelle. Das steht nicht in der ManMap-Doku.

## P-014: Doku-Dateien überschreiten die Lesegrenze des Agenten

- **Stelle:** `moai/docu/objectflow.md` (1302 Zeilen, rund 67.000 Tokens), `dataux.md`
- **Unklar/Problem:** Eine Datei lässt sich nicht in einem Zug lesen (Grenze 25.000 Tokens je Lesevorgang). `objectflow.md` brauchte drei Lesevorgänge, alle drei DSL-Dokus zusammen rund 150.000 Tokens Kontext, bevor die erste Zeile Plan entsteht. Die Skills verweisen auf Abschnitte, für einen Plan über alle Schichten braucht man aber fast alles.
- **Annahme:** keine
- **Ausgang:** Gelesen sind `moware-werkbank.md`, `objectflow.md`, `manmap.md` vollständig und `dataux.md` bis Zeile 403 (Rest: Monitoring, Diagnose, Konzeptindex; wird vor der DataUX-Umsetzung nachgeholt).

## P-015: Glossar und Spec weichen bei Begriffen ab

- **Stelle:** `specs/research/domain.md` Glossar, Spec 001 Abschnitt 5
- **Unklar/Problem:** Das Glossar definiert Kilometerstand als „Stand mit Datum und Quelle“, die Spec kennt keine Quelle. „Antriebsart“ und „Standort“ stehen in der Spec, aber nicht im Glossar; die Constitution verlangt, dass ein neuer Begriff zuerst ins Glossar kommt.
- **Annahme:** Die freigegebene Spec gilt: Kilometerstand ohne Quelle. Antriebsart und Standort werden im Glossar ergänzt (Task T001).
- **Ausgang:** Erledigt am 2026-10-05: Glossar um Antriebsart, Standort und Personalnummer ergänzt, Kilometerstand ohne Quelle.

## P-016: Beispielkonfigurationen im MoWare-Testmodul enthalten Zugangsdaten

- **Stelle:** Modell `org.modellwerkstatt.objectflow.tests.config` im ausgelieferten Modul `org.modellwerkstatt.dataux.tests`: `MySQLOFXLdapConfig`, `LocalMySqlCONFIG`, `Defaults`
- **Unklar/Problem:** Die Skills verweisen auf dieses Modell als Vorlage für Konfigurationen. `MySQLOFXLdapConfig` enthält ein LDAP-Bind-Passwort im Klartext, das echt aussieht; die anderen enthalten Hostnamen, Benutzer und Passwörter einer fremden Umgebung. Ein Agent liest das beim Nachschlagen zwangsläufig mit.
- **Annahme:** Ich übernehme keine dieser Werte, nur die Struktur der Instanzen.
- **Ausgang:** Hinweis an den Nutzer: Passwort prüfen und gegebenenfalls ändern, Beispiele bereinigen.

## P-017: JDBC-Treiber für MySQL/MariaDB ist in keinem MoWare-Modul eingebunden

- **Stelle:** `moai/docu/moware-werkbank.md`, „Solutions anlegen“ („Java-Bibliotheken wie einen JDBC-Treiber … nur ergänzt, wenn Inhalte daraus direkt verwendet werden“); MoWare-Bibliothek unter `${JavaWare35}/moware`
- **Unklar/Problem:** `LocalMySqlCONFIG` nennt `com.mysql.cj.jdbc.Driver`. Der Treiber liegt als Jar unter `objectflow/solutions/sandbox/jars/addons/`, wird aber von keiner `.msd` referenziert. Wie eine Anwendungs-Solution den Treiber auf den Klassenpfad bekommt (Java-Library an der Solution, eigene Stub-Solution, Ort der Jar-Datei), sagt die Doku nicht. Die Konfiguration nennt die Klasse nur als String, also ist es nach dem Wortlaut der Doku gar keine „direkte Verwendung“.
- **Annahme:** Jar nach `lib/` im Projekt kopieren und als Java-Library an der Solution eintragen, sobald der erste Testlauf ansteht.
- **Ausgang:** Der Nutzer hat den Treiber am 2026-10-05 selbst der Solution hinzugefügt; damit lief der erste Test. Der Weg ist weiter nicht dokumentiert.

## P-018: Minimalkonfiguration aus dem Beispiel abgeleitet

- **Stelle:** `LocalMySqlCONFIG` und `Defaults` (siehe P-010)
- **Unklar/Problem:** Aus den Beispielen ergibt sich diese Liste von Instanzen: Locale, `transactionDefinition`, `transactionManager`, `jdbcTemplate`, `dataSource`, `databaseDescription` (`MMMySqlDescription`), User Environment und User Services, `eventBus`, `printFactory`, `consoleAppFactory`, sieben Type Handler, `deprecatedServerDateProvider`, `simplePrinterServices`, `stringFormatter`, `currentPlatform` (generierte Klasse `<StaticRessources>_<Plattform>`). Welche davon Pflicht sind und welche nur Altlast (Name `deprecatedServerDateProvider`), ist nicht erkennbar. Eine eigene Beschreibung für MariaDB gibt es nicht.
- **Annahme:** Alle übernehmen, MariaDB läuft über `MMMySqlDescription` und den MySQL-Treiber.
- **Ausgang:** Am 2026-10-05 bestätigt: Der Test `speichernUndZuruecklesen` läuft mit dieser Konfiguration durch. Ob einzelne Instanzen entbehrlich sind, habe ich nicht geprüft.

## P-019: Liste der Kilometerstände mit Schlüsselreferenz statt Rückreferenz

- **Stelle:** `moai/docu/manmap.md`, „Referenzen, eingebettete Werte und Listen“; Plan 001 Abschnitt 4
- **Unklar/Problem:** Die Doku nennt zwei Formen des `ListMapping` (Rückreferenz mit `OPPOSITE`, reine Schlüsselreferenz), sagt aber nicht, wann welche vorzuziehen ist. Das einzige kompakte Beispiel im Testmodul (`NewInvoice`/`NewInvoicePos`) verwendet die Schlüsselreferenz.
- **Annahme:** `Kilometerstand` trägt `fahrzeugId` (int) statt einer Rückreferenz `fahrzeug`; das weicht vom Plan ab (dort `fahrzeug` mit `OPPOSITE`). Der Plan wird nachgezogen.
- **Ausgang:** Am 2026-10-05 bestätigt: Speichern und Zurücklesen des Fahrzeugs funktioniert; die Liste mit Kilometerständen wird mit US-5 getestet.

## P-020: Abfragen im Beispielmodul sind sehr teuer

- **Stelle:** Skills verweisen zum Nachschlagen auf `org.modellwerkstatt.dataux.tests`; Werkzeug `mps_mcp_query_nodes` `FIND_INSTANCES`
- **Unklar/Problem:** `FIND_INSTANCES` liefert je Treffer einen vollen Umschlag direkt in die Antwort, nicht in eine Datei. Eine Suche nach dem Konzept `Session` im Beispielmodul brachte 17 Treffer und rund 9.000 Tokens, obwohl ich nur ein Beispiel brauchte. Die Skills erwähnen `sampleOnly` nur in einer Referenzdatei.
- **Annahme:** Ab jetzt `sampleOnly: true` oder Tiefendruck in eine Datei mit eigener Auswertung.
- **Ausgang:** Der Weg „Tiefendruck in Datei, Auswertung per Skript, Teilbäume als Blueprint übernehmen“ funktioniert gut; er steht in keinem Skill.

## P-021: Blueprints der Skills decken nur Gerüste ab

- **Stelle:** `moai/skills/objectflow-dsl/references/blueprints/`
- **Unklar/Problem:** Für `OFXConfig`, `RolesAndPermissions`, `Service` und `OFXTestSuit` enthalten die Blueprints nur den leeren Root. Die eigentliche Arbeit (Instanzen, Sections, Rollenfunktion, Service-Methode, Autowired-Feld, `session`) musste ich aus dem Beispielmodul ableiten. `TryUniversalStatement` verlangt `MultipleCatchClause`; die Testkonvention zeigt `try/catch` nur als Text.
- **Annahme:** `TryCatchStatement` mit `CatchClause` für `CS.COMMIT()`.
- **Ausgang:** `CS`, `FuhrparkRollen`, `FuhrparkTestKonfiguration` und `FuhrparkRessourcen` sind angelegt und ohne Fehler geprüft (bei `CS` nur die Warnung „Field appFactory is never assigned“, die bei `@Autowired` zu erwarten ist).

## P-022: Option `INDEX` erzeugt einen eindeutigen Index

- **Stelle:** `moai/docu/manmap.md` und `objectflow.md`: „`INDEX` – Beschreibt einen Indexhinweis für die gemappte Spalte“; generierte Datei `DbSchema_FahrzeugPersistenz.xml`
- **Unklar/Problem:** Für `INDEX` an `Kilometerstand.fahrzeugId` und `Fahrzeug.kennzeichenNormiert` erzeugt der Generator `CREATE UNIQUE INDEX`. Damit könnte ein Fahrzeug nur einen einzigen Kilometerstand haben, und zwei bestellte Fahrzeuge ohne Kennzeichen wären ebenso unmöglich wie die Wiederverwendung eines Kennzeichens. Umgekehrt erzeugt `UNIQUE` an `fahrgestellnummer` nichts Sichtbares, und `KEY` keinen Primärschlüssel.
- **Annahme:** `INDEX` ist für nicht eindeutige Spalten nicht verwendbar.
- **Ausgang:** Beide `INDEX`-Optionen entfernt; der Plan (Abschnitt 5) wird nachgezogen. Die Eindeutigkeit der Fahrgestellnummer sichert der Service, nicht das Schema. Bitte prüfen, ob das Verhalten des Generators gewollt ist.

## P-023: Schemabeschreibung ist Oracle-Syntax

- **Stelle:** generierte `DbSchema_FahrzeugPersistenz.xml`; `moware-werkbank.md`, „Datenbankschema erstellen“
- **Unklar/Problem:** Die generierte Beschreibung verwendet `NUMBER`, `VARCHAR2` und `CREATE SEQUENCE`, auch wenn die Konfiguration `MMMySqlDescription` nennt. Wie der Entwickler in MPS das Schema für MariaDB erzeugt, beschreibt die Doku nicht.
- **Annahme:** Der Entwickler kennt den Weg; ich erzeuge kein Schema.
- **Ausgang:** Der Nutzer hat das Schema am 2026-10-05 erstellt; die Tabellen passen zum Mapping (erster Test grün). Wie er von der Oracle-Beschreibung zu MariaDB kam, weiß ich nicht.

## P-024: Kind löschen über `mps_mcp_update_node`

- **Stelle:** Skill `mps-node-editing` (Tabelle: `DELETE` × `CHILD`), Werkzeugbeschreibung (`SET` × `CHILD` mit `childJson = null`)
- **Unklar/Problem:** `operation: DELETE` wird abgelehnt („Valid operations: ADD, SET“). `childJson: "null"` wird ebenfalls abgelehnt. Es funktioniert nur `SET` × `CHILD` ganz ohne `childJson`.
- **Annahme:** keine
- **Ausgang:** Drei Versuche nötig; Skill und Werkzeug widersprechen sich.

## P-025: Make über MCP funktioniert

- **Stelle:** `mps_mcp_alter_nodes` `MAKE`; `tech-stack.md` („Rebuild ist ein Schritt des Entwicklers“)
- **Unklar/Problem:** Offen war, ob der Agent selbst bauen kann.
- **Annahme:** keine
- **Ausgang:** `MAKE` auf der Solution läuft durch und erzeugt `source_gen` und `classes_gen`. Der Plan führt den Rebuild trotzdem als Schritt des Entwicklers vor dem Ant-Build.

## P-026: Kein Beispiel für `session operation add`

- **Stelle:** `moai/conventions/moware-werkbank-tests_v1.md` (Service `TestDaten`), Beispielmodul `org.modellwerkstatt.dataux.tests`
- **Unklar/Problem:** Die Testkonvention verlangt `session operation add`. Im Beispielmodul gibt es keine einzige Instanz von `SessionOperationAdd`. Der Kommentar im Konventionsbeispiel (`// "Testdaten Zahlungsart"`) ist in Wahrheit ein Pflichtfeld: Ohne Text meldet MPS „Description text should not be empty“.
- **Annahme:** Aufbau nach Konzeptdefinition (`operationCall`, `ex`).
- **Ausgang:** Funktioniert; der Beschreibungstext ist die Rolle `ex`.

## P-027: Erster Test läuft durch, Testlauf über MCP möglich

- **Stelle:** `mps_mcp_create_run_configuration`, `execute_run_configuration`
- **Unklar/Problem:** Offen war, ob der Agent Testsuiten selbst starten kann.
- **Annahme:** keine
- **Ausgang:** `OFXTestSuit` ist als „Java Application“ startbar. `FahrzeugTests.speichernUndZuruecklesen` ist am 2026-10-05 grün: Fahrzeug über Custom Session angelegt und committet, ID vergeben, in frischer Session zurückgelesen. In der Textprojektion erscheint `#+ with # TestDaten…` ohne den Session-Ausdruck `#CS.CREATE()`; im Modell ist er vorhanden.

## P-028: Neues Datumsliteral steht auf „Serverdatum“

- **Stelle:** `moai/docu/objectflow.md`, „Literale für Datum, Zeitpunkt und Dezimalzahl“; Konzept `DateLiteral`
- **Unklar/Problem:** Ein per Blueprint angelegtes `DateLiteral` mit `year`, `month`, `day` hat `fromServer = true` als Vorgabe. Tag, Monat und Jahr werden dann stillschweigend ignoriert, generiert wird das Serverdatum. Die Prüfung meldet nichts; die Projektion zeigt `new_LocalDateFromServer()`, was ich erst nach zwei roten Tests gelesen habe. Die Doku nennt die Property nicht.
- **Annahme:** `fromServer` muss für feste Daten ausdrücklich auf `false` gesetzt werden.
- **Ausgang:** Elf Literale korrigiert, danach liefen alle Tests. Gehört in die Gotchas des ObjectFlow-Skills.
- **Stand:** erledigt (`objectflow.md` „Literale für Datum, Zeitpunkt und Dezimalzahl“: neue Tabellenspalte „Property“ mit `fromServer=false`/`fromServer=true` je Projektion; bei `true` bleiben Datum und Uhrzeit des Knotens ohne Wirkung. Kein Gotcha im Skill, weil es in der Doku steht)

## P-029: Konzept `LocalPropertyReference` gibt es doppelt

- **Stelle:** Zugriff auf eigene Properties in einer Methode der Entity
- **Unklar/Problem:** `org.modellwerkstatt.dataux.structure.LocalPropertyReference` und `jetbrains.mps.baseLanguage.structure.LocalPropertyReference` tragen denselben Namen. In einer Entity-Methode ist das BaseLanguage-Konzept richtig; die Skills sagen dazu nichts, die Doku erwähnt den Zugriff auf eigene Properties in Methoden gar nicht.
- **Annahme:** BaseLanguage-Konzept, wie im Beispiel `NewInvoice.complete`.
- **Ausgang:** Funktioniert.

## P-030: Verletzte Precondition im Test außerhalb eines Commands

- **Stelle:** `moai/docu/objectflow.md`, „Testoptionen“ (`FAIL IN`) und „Commands ohne UI ausführen“
- **Unklar/Problem:** Die Doku nennt für abgelehnte Fälle nur `FAIL IN OFXJobWorkCanceledException` an einem `run command`. Welche Ausnahme ein direkter Service-Aufruf im `Simple Test` wirft, steht nicht da. Laut generiertem Code ist es `OFXAbortedException`, und die Probleme bleiben an der Session hängen (`hasProblemsOtherThanWarnings`), sodass jede weitere Validation in derselben Session ebenfalls scheitern würde.
- **Annahme:** Jeder Service-Aufruf im Test läuft mit `#+ with #CS.CREATE()` in einer frischen Session; erwartete Ablehnungen tragen `FAIL IN OFXAbortedException`. Das Testmodell braucht dafür einen Import auf `org.modellwerkstatt.objectflow.runtime`.
- **Ausgang:** Funktioniert, 4 von 4 Tests grün. Ob der Meldungstext über `contains` prüfbar ist, habe ich noch nicht versucht.

## P-031: Stapelaufrufe liefern sehr große Antworten

- **Stelle:** `mps_mcp_update_node` `SET` × `PROPERTY` mit mehreren Zeilen
- **Unklar/Problem:** Für elf Property-Änderungen kam je Zeile ein voller Knoten-Umschlag zurück, zusammen rund 5.000 Tokens ohne Informationswert.
- **Annahme:** keine
- **Ausgang:** Beobachtung für die MCP-Werkzeuge; eine knappe Erfolgsantwort würde reichen.

## P-032: Java-Parser spart viel Arbeit, aber nur für reines Java

- **Stelle:** `mps_mcp_parse_java_and_insert`, Skill `mps-baselanguage`
- **Unklar/Problem:** Methoden ohne ObjectFlow-Konstrukte (Normierung, Regex-Prüfung) ließen sich als Java-Text in die Entity einfügen, ohne Fehler. Sobald eine Methode eigene Properties, Status oder `#`-Aufrufe braucht, bleibt nur der JSON-Blueprint; der `FahrzeugService` hatte als Blueprint 64 KB.
- **Annahme:** keine
- **Ausgang:** Beides funktioniert. Die DSL-Skills erwähnen den Parser nicht als Abkürzung.

## P-033: Suche als gemappte Abfrage statt Custom SQL (Abweichung vom Plan)

- **Stelle:** `moai/docu/manmap.md`, „Custom SQL mit `SQL`“ und „Parameter in SQL-Text“; Plan 001 Abschnitt 6
- **Unklar/Problem:** Für die Suche brauche ich optionale Filter auf Status-Properties. Die Doku sagt, ein gebundener Wert müsse „einen primitiven Typ besitzen“, und nennt für Status nur Konstanten (`C2SqlStatusReference`). Wie man einen Status aus einer Variablen oder einem DTO bindet, steht nicht da; der Persistenzwert (`getDbValue()`) ist im Modell nicht erreichbar. Dazu kommt der Aufwand: SQL-Text ist im Modell Wort für Wort ein eigener Knoten.
- **Annahme:** Die Doku erlaubt für Lesemodelle ausdrücklich auch `EntityMapping` mit `where`. Ich verwende `where` mit `optional`, `like`, `TO_LOWERCASE`, `in` und `listJoin`. Das Ergebnis sind read-only geladene `Fahrzeug`-Entities in `FahrzeugFilter.results`; das DTO `FahrzeugInfo` entfällt. Die Vorbereitung der Suchmuster liegt im Service `FahrzeugSuche` im `read`-Modell.
- **Ausgang:** Test `suche` grün: Teilbegriff ohne Rücksicht auf Groß- und Kleinschreibung, Kennzeichen ohne Leerzeichen, Ausschluss ausgeschiedener Fahrzeuge ohne Statusfilter, Statusfilter, Filter nach Fahrzeugklasse. Offen: Die Konvention nennt für `read` keine Services; ob `FahrzeugSuche` dort richtig liegt, entscheidet der Nutzer. Sortierung fehlt noch.

## P-034: Status-Property in einem DTO startet nicht leer

- **Stelle:** `FahrzeugFilter`; `objectflow.md`, „Null-Werte in Datenstrukturen“
- **Unklar/Problem:** Ein Filter-DTO braucht „kein Filter“ als Ausgangswert. Status-Properties starten aber mit dem `ON_CREATION`-Element, der Filter stünde also sofort auf PKW, „fest zugeordnet“ und „bestellt“.
- **Annahme:** Der Konstruktor des DTOs setzt die drei Status-Properties auf `null`.
- **Ausgang:** Funktioniert im Test; `optional` lässt die Bedingung bei `null` weg, wie dokumentiert.
- **Stand:** offen (Entscheidung des Nutzers steht aus: Ist das Setzen auf `null` im Konstruktor der vorgesehene Weg für Filter-DTOs, und gilt es auch für Entities ohne `ALLOW_NULL_PERSISTANCE`?)

## P-035: Command und `run command` ließen sich ohne Rückfrage bauen

- **Stelle:** Skill `objectflow-dsl` (Blueprint `command-skeleton.json`), Beispiel `GO` und `RunCmdTests` im Testmodul
- **Unklar/Problem:** Der Blueprint ist nur ein leerer Root. Rollen wie `okConclusionStatements`, `finalOkSelection`, `commandCreationInformation`, `permissionNew` mit `PermissionHasReference`, `OFXRunCmdPage.beforeConclude` und `OFXRunCmdVarRef` stehen in keiner Skill-Referenz, nur in der Konzeptdefinition und im Beispiel.
- **Annahme:** Aufbau wie im Beispiel `GO`.
- **Ausgang:** Erster Versuch fehlerfrei, Test `anlegenUeberCommand` grün. Die Textprojektion des fertigen Commands entsprach genau der Doku; das war die wirksamste Kontrolle. Eine Skill-Referenz mit einem vollständigen kleinen Command samt Test würde den Umweg über das Beispielmodul sparen.

## P-036: Statusauswahl beim Anlegen noch nicht eingeschränkt

- **Stelle:** Command `Fahrzeug anlegen`, FR-008
- **Unklar/Problem:** Beim Anlegen sind nur „bestellt“ und „aktiv“ zulässig. Die Einschränkung der Auswahl über `#Meta.setElements` in der Scope-Funktion fehlt noch, und der Service lehnt „stillgelegt“ oder „ausgeschieden“ beim Anlegen bisher nicht ab.
- **Annahme:** Wird mit den Scope-Funktionen der Edit-Commands nachgezogen, zusammen mit einer Prüfung im Service.
- **Ausgang:** Erledigt am 2026-10-05: Die Scope-Funktion der Page begrenzt die Auswahl mit `fahrzeug.status#Meta.setElements(Bestellt, Aktiv)`, und `pruefeUndUebernehme` lehnt bei einem neuen Fahrzeug (ohne ID) jeden anderen Status ab. Die Scope-Funktion ließ sich nach dem Pseudocode der Doku bauen (`BPMetaReference` als Operation eines `DotExpression`).

## P-037: `optional` wird im Oder zu `(1 != 1)`; eine Oder-Gruppe aus lauter entfallenden Prädikaten liefert keine Treffer

- **Stelle:** `moai/docu/manmap.md`, „Spezifikum - Filterausdrücke und gemappte Felder“: Ist der Parameter nicht gesetzt, werde das Prädikat „nicht in die SQL-Bedingung aufgenommen“; `optional` lasse sich „innerhalb einer `||`- oder `&&`-Verknüpfung unabhängig aktivieren“.
- **Unklar/Problem:** In `FahrzeugLeseRepo.suche` stehen vier `optional(… like …)` in einer geklammerten Oder-Gruppe, die mit den übrigen Filtern über `&&` verknüpft ist. Sind alle vier Parameter `null`, findet die Abfrage nichts. Der Fehler fiel nur auf, weil der Such-Command im Test den Hinweis „Es wurde kein Fahrzeug gefunden“ ausgab; mein erster Suchtest hatte immer einen Suchbegriff gesetzt, und der Test des Commands prüfte nur, dass die Ergebnisliste nicht `null` ist.
- **Ursache (vom Nutzer am 2026-10-05 erklärt, im generierten Code bestätigt):** Ein entfallendes `optional` wird nicht weggelassen, sondern durch das neutrale Element seiner Verknüpfung ersetzt. In `FahrzeugLeseRepo.java` steht für die vier Prädikate im Oder `__whereStatement.append("( 1 != 1)")` und für die drei im Und `append("(1 = 1)")`. Im Und ist das harmlos: `(1 = 1)` schränkt nicht ein. Im Oder ist `(1 != 1)` für sich ebenfalls neutral, aber eine Gruppe, in der **alle** Prädikate entfallen, ergibt `(falsch OR falsch OR falsch OR falsch)`, also falsch, und zieht über das umgebende Und die ganze Bedingung auf falsch. „Kein Kriterium“ bedeutet in einer reinen Oder-Gruppe also „kein Treffer“, nicht „keine Einschränkung“.
- **Annahme:** Ohne Suchbegriff setzt der Service beide Muster auf `%`; die Gruppe ist dann immer aktiv und trifft alles.
- **Ausgang:** Test `sucheOhneKriterien` grün (liefert das eben angelegte Fahrzeug und kein ausgeschiedenes). Dieselbe Lösung in `LenkerSuche`.
- **Was in die Doku gehört:** (1) Die Formulierung „nicht in die SQL-Bedingung aufgenommen“ ist irreführend; richtig ist: im Und wird `(1 = 1)` eingesetzt, im Oder `(1 != 1)`. (2) Ausdrücklich warnen: Eine Oder-Gruppe, die nur aus `optional`-Prädikaten besteht, liefert nichts, wenn alle entfallen. (3) Das Muster dafür nennen: einen Platzhalterwert übergeben, der immer trifft (bei `like` das Muster `%`), oder die Gruppe selbst in ein `optional` fassen, falls das geht. (4) Gehört auch in die Gotchas des Skills `manmap-dsl`.
- **Vorschlag für den Generator (2026-10-05, nach Lesen von `FahrzeugLeseRepo.java`, Zeilen 60–135; den Generator selbst habe ich nicht gesehen):** Heute erzeugt jedes `optional`-Prädikat für sich `if (param != null) { …Prädikat… } else { append(neutrales Element) }`; das neutrale Element richtet sich nach dem direkt umgebenden Operator. Die Klammergruppe selbst (`" ("` … `") "`) wird unbedingt geschrieben. Nötig wäre, das Entfallen nach oben weiterzugeben: Eine Gruppe, deren Operanden alle entfallen können, bekommt eine eigene Laufzeitbedingung (Oder-Verknüpfung der Parameterprüfungen ihrer Blätter, hier `begriff != null || begriffKennzeichen != null`). Ist sie falsch, schreibt der Generator statt der Gruppe das neutrale Element des Operators, der die Gruppe umgibt (im Und und auf oberster Ebene `(1 = 1)`, im Oder `(1 != 1)`). Gruppen mit mindestens einem nicht-optionalen Operanden bleiben unverändert. Zu prüfen ist der Spiegelfall: Eine Und-Gruppe aus lauter entfallenden Prädikaten innerhalb eines Oder ergäbe nach heutigem Muster `… OR ((1 = 1) AND (1 = 1))`, also alle Zeilen; das habe ich nicht ausprobiert. Die Änderung ändert das Verhalten bestehender Abfragen (bisher „nichts“, dann „alles“). Der Kommentar `// remove leading AND / OR` im generierten Code passt nicht mehr zu dem, was dort geschieht.
- **Stand:** erledigt (`manmap.md` „Spezifikum - Filterausdrücke und gemappte Felder“: Wirkung eines entfallenden `optional` in `&&` und `||`, leere `||`-Gruppe liefert keine Treffer, Muster `%`; kein Gotcha im Skill, weil es in der Doku steht. Der Generator bleibt unverändert)

## P-038: Layout darf nicht gebunden sein

- **Stelle:** Blueprint `moai/skills/dataux-dsl/references/blueprints/grid-master-detail-subtree.json`
- **Unklar/Problem:** Der Blueprint gibt dem `GridLayout` ein `boundClassifier`. Innerhalb eines Page Pane meldet die Prüfung dafür „A layout in an ui hierarchy should not be bound to any object“.
- **Annahme:** Bindung am Layout weglassen.
- **Ausgang:** Ohne Bindung fehlerfrei. Der Blueprint führt in die Irre, wenn man ihn als Kind eines Page Pane verwendet.

## P-039: Aufgabe zu früh abgehakt

- **Stelle:** `specs/001-fahrzeug/tasks.md`, T035
- **Unklar/Problem:** Ich hatte T035 abgehakt, obwohl nur `letzterKilometerstand` existierte und die virtuelle Property `aktuellerKilometerstand` fehlte. Aufgefallen ist es erst, als die Ergebnistabelle sie brauchte.
- **Annahme:** keine
- **Ausgang:** Property nachgezogen (`CustomPropertyImplementation` mit `PRESENTATION`), Vorlage war ein Beispiel im Testmodul.

## P-040: `save with … BATCH` mit Auto-ID ist für MySQL/MariaDB nicht implementiert

- **Stelle:** `moai/docu/manmap.md`, „Save-Optionen“ (`BATCH`); Beispiel `NewInvRepo.checkinBatch` im Testmodul
- **Unklar/Problem:** Ich hatte das Speichern der Kilometerstände wie im Beispiel als `save with MapKilometerstand, BATCH (liste)` modelliert. Beim ersten echten Insert eines Kilometerstands wirft die Laufzeit `RuntimeException: Not implemented yet.` aus `MMMySqlDescription.queryForListOfKey`. Die Doku nennt keine Einschränkung auf Oracle. Aufgefallen ist es erst im Test über die Commands, weil vorher kein Test Kilometerstände in die Datenbank schrieb.
- **Annahme:** Kilometerstände einzeln in einer Schleife speichern.
- **Ausgang:** Mit Einzelspeicherung läuft `aendernUeberCommands` durch. Die Doku sollte die Einschränkung nennen, oder die Laufzeit sollte es können.

## P-041: Entfernte Kilometerstände über Vergleich im Owner gelöscht

- **Stelle:** Plan 001 Abschnitt 7 und Abschnitt 13 (offener Punkt: Rückgabe eines Werts aus einem `GRAPH_EDIT_CMD` ohne Page)
- **Unklar/Problem:** Die Doku beschreibt nicht, wie ein Edit-Command ohne Page seinem Owner einen Wert übergibt, ohne den Weg über Push und Termination Handler.
- **Annahme:** Die im Plan genannte Ausweichlösung: `Fahrzeug oeffnen` merkt sich beim Start die geladenen Kilometerstände und löscht in `FINAL OK_CONCLUSION` jene mit vergebener ID, die nicht mehr in der Liste stehen.
- **Ausgang:** Test `aendernUeberCommands` grün: Stand erfassen, zweiten erfassen, letzten entfernen, jeweils aus der Datenbank zurückgelesen. Ein `DELETE`-Repository-Aufruf in einer Schleife innerhalb von `FINAL OK_CONCLUSION` wird wie erwartet als Session-Operation ausgeführt.

## P-042: Statuswechsel-Maske arbeitet auf der echten Property

- **Stelle:** Command `Fahrzeugstatus aendern`
- **Unklar/Problem:** Die Maske bindet direkt an `Fahrzeug.status`. Damit der Service den Übergang prüfen kann, merkt sich der Command den alten Status, setzt ihn vor der Prüfung zurück und übergibt den gewählten als Ziel. Lehnt der Service ab, zeigt die Maske weiter den gewählten Wert, das Objekt hat aber wieder den alten.
- **Annahme:** Für die Demo vertretbar; sauberer wäre ein eigenes Eingabe-DTO wie beim Kilometerstand.
- **Ausgang:** Im Test über `run command` funktioniert der Wechsel. Das Verhalten nach einer Ablehnung ist in der Oberfläche zu prüfen.

## P-043: Anwendungskonfiguration für `fx8forms` abgeleitet

- **Stelle:** `moai/docu/moware-werkbank.md`, „Laufzeitkonfiguration auswählen“ („über AppFactories“); `dataux.md`, „Anwendung mit `AppUI Module`“
- **Unklar/Problem:** Die Doku nennt keine Klasse einer AppFactory. Das Beispiel `OrderApp` im Testmodul verwendet `FakeUiFactory`. Die Klasse für JavaFX (`org.modellwerkstatt.fx8forms.windows.FX8UiFactory`) habe ich im generierten Code der MoWare-Bibliothek gesucht. Nachbarprojekte auf dieser Maschine (andere Anwendungen mit fertigen Konfigurationen) habe ich bewusst nicht als Vorlage gelesen, damit der Test der MoAI-Unterlagen nicht verfälscht wird.
- **Annahme:** `FuhrparkAnwendung` bindet die drei Sections der Testkonfiguration ein und setzt `FX8UiFactory` als Instanz `consoleAppFactory`. `isAuthenticated` übernimmt den Benutzernamen und liefert `true`; eine Passwortprüfung gibt es in der Demo nicht.
- **Ausgang:** Das AppUI-Modul `MjFuhrpark` ist fehlerfrei, die Run-Konfiguration `MjFuhrpark` startet einen JavaFX-Prozess ohne Fehlerausgabe. Ob Anmeldung, Menü und Masken funktionieren, kann ich nicht sehen; das prüft der Nutzer (T027, T042).

## P-044: Suche aktualisiert sich nach dem Bearbeiten nicht von selbst

- **Stelle:** Command `Fahrzeuge suchen`, `objectflow.md` „Termination Handler“
- **Unklar/Problem:** Nach `Fahrzeug oeffnen` oder `Fahrzeug anlegen` müsste die Trefferliste neu geladen werden. Dafür ist ein Termination Handler an der Page nötig; ob darin `page Suche` zulässig ist, sagt die Doku nicht.
- **Annahme:** Vorerst lädt der Benutzer mit „Suchen“ neu.
- **Ausgang:** Erledigt am 2026-10-05: Ein Termination Handler (`AnyCmdTerminated`) an der Page `Suche` ruft die Suche erneut auf; ein `page`-Statement war nicht nötig. Die Prüfung akzeptiert den Komponentenaufruf im Handler. Ob die Tabelle in der Oberfläche tatsächlich neu zeichnet, prüft der Nutzer.

## P-045: UI-Konventionen fehlten, zwei nachgetragen

- **Stelle:** `moai/conventions/` (bisher nur Anwendung, Sprache, Tests); neu `moai/conventions/moware-werkbank-ui_v1.md`
- **Unklar/Problem:** Für Oberflächen gab es keine Konvention. Ich habe deshalb keine Page Titles gesetzt (optional im Konzept, die Prüfung meldet nichts, das Beispiel `GO` hat keine) und die Fahrzeugansicht links/rechts aufgeteilt. Die Suche habe ich mit einer statt zwei Pages gebaut, weil die Doku das Zwei-Page-Muster nur als Beispiel zeigt.
- **Annahme:** keine
- **Ausgang:** Der Nutzer hat am 2026-10-05 zwei Konventionen vorgegeben, ich habe sie auf seine Anweisung in `moai/` erfasst; das Submodul verwaltet er selbst. Angewendet am selben Tag: Alle sechs Pages haben einen Page Title (`dynamicPageTitle` als formatierter String, bei `Fahrzeug oeffnen` mit Marke und Modell). `FahrzeugAnsicht` stellt Formular und Kilometerstand-Tabelle untereinander. Die Formulare bleiben zwei- beziehungsweise dreispaltig; ob die Konvention auch das meint, ist offen. 11 von 11 Tests grün.


## P-046: Menüaktion nicht im Overflow-Menü

- **Stelle:** `moai/docu/dataux.md`, „Menüs und Command-Aktionen“: „Ein Menü beginnt üblicherweise mit einem `Submenu` … Nur wenige, außergewöhnlich wichtige Aktionen sollten direkt auf der obersten Ebene stehen“
- **Unklar/Problem:** Die Doku sagt es, als Empfehlung („üblicherweise“). Ich habe es an zwei Stellen befolgt (Fahrzeugansicht, Menü der Suchseite) und `Fahrzeug oeffnen` in der Ergebnistabelle direkt auf die oberste Ebene gesetzt, ohne das abzuwägen. Im Hauptmenü des AppUI-Moduls stehen die Actions ebenfalls direkt, wie im Beispiel `OrderApp`.
- **Annahme:** Die Hauptaktion der Tabelle gehört auch ins Submenü; Doppelklick und Enter finden sie dort laut Doku trotzdem.
- **Ausgang:** `Fahrzeug oeffnen` steht jetzt im Submenü „Aktionen“ der Tabelle. Vorschlag: als Konvention aufnehmen, weil „üblicherweise“ einen Agenten nicht bindet, und dabei festlegen, ob das Hauptmenü der Anwendung ausgenommen ist.

## P-047: Oberstes Submenü darf keinen Text haben

- **Stelle:** Blueprint `moai/skills/dataux-dsl/references/blueprints/menu-submenu-subtree.json` (setzt `label` „Actions“); `moai/docu/dataux.md`, „Menüs und Command-Aktionen“
- **Unklar/Problem:** Ich hatte den drei obersten Submenüs den Text „Aktionen“ gegeben, wie es der Blueprint vormacht. Laut Nutzer darf das Submenü auf oberster Ebene (das Overflow-Menü) keinen Text tragen. Die Doku sagt dazu nichts; `label` ist im Konzept optional.
- **Annahme:** keine
- **Ausgang:** Am 2026-10-05 an allen drei Stellen entfernt (Fahrzeugansicht, Suchseite, Ergebnistabelle). Der Blueprint führt hier in die Irre; die Regel gehört in die UI-Konvention oder in die Doku. Am selben Tag als dritte Konvention in `moai/conventions/moware-werkbank-ui_v1.md` aufgenommen (Overflow-Menü, oberstes Submenü ohne Text); damit ist auch der Vorschlag aus P-046 umgesetzt.

## P-048: Gesperrter Command im Test wirft `RuntimeException`, und `FAIL IN` meldet es missverständlich

- **Stelle:** `moai/docu/objectflow.md`, „Commands ohne UI ausführen“; Test `abbruchUndAusgeschieden`
- **Unklar/Problem:** Die Doku sagt nicht, was `run command` tut, wenn `generally enabled` des Commands nicht erfüllt ist. Ich hatte `FAIL IN OFXJobWorkCanceledException` erwartet. Der Lauf meldete „Fail In Exception OFXJobWorkCanceledException was NOT catched!“, also dieselbe Meldung wie bei ausbleibender Ausnahme. Daraus und aus dem unveränderten Datensatz habe ich fälschlich geschlossen, der Command werde stillschweigend übersprungen, und das dem Nutzer auch so gemeldet. Erst ohne `FAIL IN` zeigte sich die wahre Ursache: `RuntimeException: Command … can not be started. Enabled condition of command not fulfilled.`
- **Annahme:** `FAIL IN RuntimeException` für diesen Fall.
- **Ausgang:** Test grün (12 von 12). AC-3.3 und AC-3.4 sind damit über die Commands geprüft: Ein Abbruch durch eine verletzte Precondition im Edit-Command speichert nichts, und bei einem ausgeschiedenen Fahrzeug lässt sich der Edit-Command nicht starten. Die Doku sollte das Verhalten nennen; die Meldung von `FAIL IN` sollte die tatsächlich geworfene Ausnahme zeigen.

## P-049: Sortierung der Trefferliste

- **Stelle:** `FahrzeugLeseRepo.suche`
- **Unklar/Problem:** keine; `sortBy` ließ sich nach der Doku ergänzen.
- **Annahme:** Sortiert wird nach normiertem Kennzeichen, dann Marke, dann Modell.
- **Ausgang:** Fehlerfrei, Tests grün. Die Reihenfolge selbst prüft kein Test.

## P-050: Regel über zwei Aggregate ohne Use-Case-Bereich

- **Stelle:** `moai/conventions/moware-werkbank-anwendung_v1.md` („zwischen Modellen, Bereichen und Bounded Contexts gibt es keine Zyklen“; Use-Case-Bereiche für Abläufe über mehrere Aggregate); Plan 002 D-2
- **Unklar/Problem:** „Lenker ausscheiden“ muss die Zuordnungen der Fahrzeuge kennen, `fahrzeug` hängt wegen der Zuordnung aber schon von `lenker` ab. Nach dem Wortlaut der Konvention bleibt nur ein Use-Case-Bereich, also drei Modelle für einen Service und einen Command. Die Konvention sagt nicht, ab welcher Größe sich das lohnt, und nennt keine leichtere Lösung.
- **Annahme:** Mein Vorschlag war der Use-Case-Bereich `lenkerausscheiden`.
- **Ausgang:** Der Nutzer hat am 2026-10-05 entschieden: ohne Use-Case-Bereiche. Umsetzung: Die Regel liegt in `LenkerService.scheideAus(lenker, laufendeZuordnung)`; den Fakt liest der Command in `lenker.unit` aus `fahrzeug.domain`. Auf Modellebene gibt es keinen Zyklus, auf Bereichsebene schon. Die Konvention sollte diesen Fall regeln (Zyklus nur auf Modellebene verbieten, oder ein Muster „Fakt wird vom Aufrufer geliefert“ nennen).
- **Stand:** keine Änderung (Entscheidung des Nutzers vom 2026-10-05: Das Zyklenverbot der Konvention bleibt, wie es ist)

## P-051: Entscheidungen zu Suche und Lesemodell

- **Stelle:** Plan 001 D-9 und D-11, Plan 002 D-4 und D-5
- **Unklar/Problem:** Offen war, ob Suchen eine oder zwei Pages haben und ob Lesemodelle Custom SQL brauchen.
- **Annahme:** eine Page, gemappte Abfrage
- **Ausgang:** Vom Nutzer am 2026-10-05 bestätigt: Suche mit einer Page, Lesemodell als gemappte Abfrage. In Doku oder Konvention steht beides nicht als Regel.
- **Stand:** keine Änderung (Entscheidung des Nutzers vom 2026-10-05: wird nicht als Konvention aufgenommen)

## P-052: Referenz auf ein anderes Aggregat und zweite Liste am Fahrzeug

- **Stelle:** `moai/docu/manmap.md`, „Referenzen, eingebettete Werte und Listen“ und „Explizites Laden“; Beispiele `Referer`/`RepoReferer` im Testmodul
- **Unklar/Problem:** Für `Zuordnung.lenker` brauchte ich `ReferenceMapping` und `refJoin`; die Blueprints des Skills zeigen `refJoin` nicht. Offen ist außerdem, ob eine Repository-Methode einer read-only geladenen Entity eine Liste zuweisen darf (`fahrzeug.zuordnungen = …` in `get`); die Doku nennt die Zuweisung als üblichen Weg, sagt aber auch, dass Setter einer read-only Entity eine Ausnahme werfen.
- **Annahme:** `ReferenceMapping` mit `keyMapping` auf `Lenker.id`; Zuordnungen in einer zweiten Abfrage mit `refJoin` auf `MapLenker` laden und der Property zuweisen; kein `ListMapping` für die Zuordnungen, weil kein `listJoin` gebraucht wird.
- **Ausgang:** Am 2026-10-05 bestätigt: Test `zuordnungSpeichernUndLaden` grün. `ReferenceMapping` speichert den Fremdschlüssel, die zweite Abfrage mit `refJoin` lädt Zuordnungen samt Lenker, und die Zuweisung an die read-only geladene Entity funktioniert.

## P-053: Doku-Lücke: Repository-Methode darf einer read-only Entity eine Liste zuweisen

- **Stelle:** `moai/docu/manmap.md`, „Explizites Laden“ und „Read-only, Checkout und Session-Identität“; `moai/docu/objectflow.md`, „Dirty-Tracking, Read-only und unveränderliche Werte“
- **Unklar/Problem:** Die Doku sagt einerseits, Listen würden „mit separaten Abfragen geladen, deren Ergebnis der Property explizit zugewiesen wird“, andererseits, dass der Setter einer read-only geladenen Entity `OFXIllegalAccessException` wirft. Ob die Zuweisung in einer `READONLY`-Repository-Methode erlaubt ist, steht nirgends (siehe P-052).
- **Annahme:** erlaubt
- **Ausgang:** Vom Nutzer am 2026-10-05 bestätigt: Eine Repository-Methode darf einer read-only geladenen Entity eine Liste zuweisen. **Das ist in die Doku aufzunehmen** (ManMap, „Explizites Laden“, mit Verweis aus dem Read-only-Abschnitt). Im Testlauf bestätigt: `FahrzeugRepo.get` weist `zuordnungen` zu, alle Tests grün.

## P-054: Tabelle `ZUORDNUNG` fehlt, Run-Konfigurationen waren verschwunden

- **Stelle:** Datenbank `test`; MPS-Run-Konfigurationen
- **Unklar/Problem:** Nach der Meldung „Schema erstellt“ gibt es `LENKER`, aber keine Tabelle `ZUORDNUNG`. Außerdem war die Run-Konfiguration `FahrzeugTests` nicht mehr vorhanden (vermutlich nach einem Neustart von MPS; über MCP angelegte Konfigurationen sind offenbar nicht dauerhaft).
- **Annahme:** Die Run-Konfigurationen lege ich bei Bedarf neu an. Das Schema erzeuge ich nicht selbst.
- **Ausgang:** Der Nutzer hat `ZUORDNUNG` am 2026-10-05 angelegt (MariaDB: `ID` als `auto_increment`, Datumsspalten als `timestamp`). Danach `FahrzeugTests` 12 von 12 grün. Die Run-Konfigurationen lege ich nach einem Neustart von MPS neu an.

## P-055: Zwei Services `TestDaten` in verschiedenen Modellen

- **Stelle:** `moai/conventions/moware-werkbank-tests_v1.md`: „Service `TestDaten` des jeweiligen `tests`-Modells“
- **Unklar/Problem:** Mit 002 gibt es `TestDaten` in `fahrzeug.tests` und in `lenker.tests`. Bei Komponenten-Scanning über das gemeinsame Basispaket hätte ich einen Namenskonflikt der gleichnamigen Komponenten für möglich gehalten; die Konvention sagt dazu nichts.
- **Annahme:** Es funktioniert, wie die Konvention es vorsieht.
- **Ausgang:** Teilweise falsch, berichtigt am 2026-10-05: Zwei `TestDaten` vertragen sich, solange jede Testsuite nur ihr eigenes verwendet (`LenkerTests` 3 von 3 grün). Sobald eine Suite beide verwendet, bricht der Build: Der Generator erzeugt für beide dasselbe Feld `__testsTestDaten` (letztes Paketsegment plus Name) und meldet „variable __testsTestDaten is already defined“. Die Modellprüfung erkennt das nicht. Die Testkonvention verlangt den Namen `TestDaten` in jedem `tests`-Modell und erlaubt zugleich, dass `tests` auf andere `tests` zugreifen; beides zusammen funktioniert nicht. Umgangen: `fahrzeug.tests.TestDaten` legt seinen Lenker selbst an. Die Konvention oder der Generator muss angepasst werden.
- **Stand:** keine Änderung an der Konvention (Nutzer, 2026-10-05: Konventionen beziehen sich nur auf Inhalte der MPS-Modelle, nicht auf generierten Code; die Namenskollision ist Sache des Generators und liegt beim Nutzer)


## P-056: Zuordnungsregeln auf Service-Ebene umgesetzt

- **Stelle:** Plan 002 Abschnitt 4
- **Unklar/Problem:** keine neue Unklarheit; alle Bausteine (Methoden an Entities, `validation`, Status aus zwei Deklarationen, `refJoin`) waren aus 001 oder aus dem Testmodul bekannt.
- **Annahme:** „Laufend“ heißt ohne Ende oder mit Ende nach dem heutigen Serverdatum (FR-008, FR-017).
- **Ausgang:** `FahrzeugTests` 15 von 15, `LenkerTests` 3 von 3. Abgedeckt: AC-2.1 bis AC-2.6, AC-3.1 bis AC-3.4, AC-3.6, AC-4.1 bis AC-4.3, Zuordnung für einen Tag, Stilllegung mit Zuordnung, Entfernen. Noch ohne Test: die Sperre „Poolfahrzeug bei laufender Zuordnung“, AC-3.5 mit echten Zuordnungen, AC-4.4, sowie alles über Commands.

## P-057: Lenker- und Zuordnungs-Commands ohne Nacharbeit

- **Stelle:** `lenker.unit`, `fahrzeug.unit`, Tests `anlegenSuchenAendernUeberCommands` und `zuordnenUeberCommands`
- **Unklar/Problem:** Neu waren der `Reference`-Delegate mit `scopeText`, `#Meta.setScope` für die Lenker-Auswahl, eine Tabellenspalte über einen Pfad (`lenker.anzeigename` als `PathDot`), Edit-Commands mit zwei Selektionsparametern (`Fahrzeug`, `Zuordnung`) und ein `SEARCH_CMD` mit Parameter (Lenkerauskunft). Der Blueprint `reference-delegate-subtree.json` und das Beispiel-Page-Pane reichten als Vorlage.
- **Annahme:** `Lenker ausscheiden` liest die Zuordnungen des Lenkers ohne `refJoin` und die Fahrzeugdaten über eine eigene Methode `getStammdaten`, damit der in derselben Session ausgecheckte Lenker nicht ein zweites Mal als read-only Referenz geladen wird (die Doku nennt für diesen Fall eine `IllegalStateException`).
- **Ausgang:** Alle Roots beim ersten Versuch fehlerfrei; `LenkerTests` 4 von 4, `FahrzeugTests` 16 von 16 nach vollständigem Rebuild. Über Commands geprüft: Lenker anlegen, suchen, ändern, ausscheiden, reaktivieren; Zuordnung beenden, neu zuordnen, entfernen (mit Löschen in der Datenbank); Lenkerauskunft; Ablehnung von „Lenker ausscheiden“ bei laufender Zuordnung (AC-3.5). In der Oberfläche ungeprüft: Lenker-Auswahl, Verlaufstabelle, Menüs.

## P-058: Was in 002 ohne Test bleibt

- **Stelle:** Spec 002, Edge Cases und FR-017, FR-019
- **Unklar/Problem:** keine
- **Annahme:** keine
- **Ausgang:** Am 2026-10-05 nachgezogen: Test `zuordnungSperrenUndEnddatum` deckt die Poolfahrzeug-Sperre, das Ändern eines gesetzten Enddatums und AC-4.4 ab (`FahrzeugTests` 17 von 17). Ohne automatischen Test bleibt FR-019 (Rollen), weil alle Tests als `leiter` laufen. Der Disponent kann Zuordnungen über `Fahrzeug oeffnen` ansehen, einen Lenker aber nur in der Trefferliste; Entscheidung des Nutzers offen.


## P-059: Abgleich der Edge Cases gegen die Tests

- **Stelle:** Spec 001 Abschnitt 3, Spec 002 Abschnitt 3; T040 (001), T024 (002)
- **Unklar/Problem:** keine
- **Annahme:** keine
- **Ausgang:** Alle 13 Edge Cases aus 001 und alle 10 aus 002 sind durch einen Test oder durch den Aufbau abgedeckt (kein `delete` für Fahrzeug und Lenker). Lücken, die bleiben:
  - 001 AC-1.4 (fehlende Fahrzeugklasse): nicht herstellbar, weil jede Statusdeklaration einen Startwert braucht (P-011). Spec oder Modell muss angepasst werden; Entscheidung des Nutzers.
  - 001 AC-5.5 (Verlauf nach Datum geordnet): Die Kilometerstände kommen über `listJoin` ohne Sortierung; in den Tests stimmt die Reihenfolge, garantiert ist sie nicht. Für `listJoin` nennt die Doku keine Sortierung der Kindliste.
  - 001 negativer Kilometerstand: Regel modelliert, nicht getestet.
  - 001 AC-2.6 und FR-014, 002 Auswahl und Verlauf: nur in der Oberfläche prüfbar.
  - 001 FR-024 und 002 FR-019 (Rollen): nur in der Oberfläche prüfbar.

## P-060: `CAN_OPEN_RO` sperrt Formulare und Conclusions; ein `SEARCH_CMD` mit Filter darf nicht RO sein (wichtig, gehört in die Doku)

- **Stelle:** `moai/docu/objectflow.md`: Absatz nach der Kapitellandkarte „Commands und Anwendungsabläufe“ (Zeile 461), Tabelle „Aufbau eines Commands“ (Zeile „Permissions“), Abschnitt „Die vier Command-Typen“ (Zeile `SEARCH_CMD`), Abschnitt „Session-weites Read-only und Dirty“, Abschnitt „Rollen, Scopes und Identities“. `moai/docu/dataux.md`: Optionen `DISABLED` für Formular und Delegate. Skill `objectflow-dsl` (Workflow „Create a command“, Gotchas). Commands `Fahrzeuge suchen`, `Lenker suchen`, `Lenkerauskunft`.

- **Was die Doku sagt:** `CAN_OPEN_RO` sei die Berechtigung „für lesenden“, `CAN_OPEN_RW` „für ändernden Zugriff“; als typischer Inhalt wird „Beobachterrolle für Anzeige, Sachbearbeiterrolle für Änderung“ genannt. Zum Read-only-Modus der Session steht nur, dass ObjectFlow „alle Page-Conclusions auf disabled“ setzt. Beim `SEARCH_CMD` heißt es, Filter-DTOs dürften editierbar sein und die Session werde nie committet.

- **Was tatsächlich gilt (vom Nutzer am 2026-10-05 erläutert, in der Oberfläche beobachtet):**
  1. Öffnet ein Benutzer einen Command nur über `CAN_OPEN_RO`, sind **alle `Delegate Form`s der Pages gesperrt**, so als trügen sie die Option `DISABLED`.
  2. Zusätzlich sind **alle Page Conclusions deaktiviert**.
  3. **Actions in Menüs bleiben startbar.** Ob eine Action läuft, hängt allein von `generally enabled` und den Berechtigungen des gestarteten Commands ab, nicht vom RO-Zustand des umgebenden Commands.

- **Folge für `SEARCH_CMD`:** Ein Such-Command mit Filterformular und einer Conclusion zum Suchen ist unter `CAN_OPEN_RO` unbrauchbar: Der Benutzer kann keinen Suchbegriff eingeben und „Suchen“ nicht auslösen. Ein `SEARCH_CMD` mit Eingaben braucht deshalb `CAN_OPEN_RW` (oder gar keine Berechtigung). Das ist ungefährlich, weil ein `SEARCH_CMD` seine Session nie committet; `RW` an einer Suche gibt kein Schreibrecht auf Daten. Der Schutz der Daten liegt an den Berechtigungen der Owner- und Edit-Commands, die aus der Suche gestartet werden. `CAN_OPEN_RO` passt an einem `SEARCH_CMD` nur, wenn er eine reine Anzeige ohne Eingabefelder und ohne Conclusion ist.

- **Warum der Agent es falsch gemacht hat:** Die Wörter „lesend“ und „ändernd“ legen nahe, die Berechtigungsart nach der Art des Datenzugriffs zu wählen. Eine Suche liest nur, also `RO`. Dass `RO` die Bedienbarkeit der Oberfläche steuert und nicht den Datenzugriff beschreibt, steht nirgends. Ich hatte alle drei Such-Commands mit `CAN_OPEN_RO` modelliert und im Plan 001 (Abschnitt 7) auch so beschrieben, ohne eine Unklarheit zu bemerken; deshalb gab es bisher keinen Protokolleintrag.

- **Warum es nicht aufgefallen ist:** Die Modellprüfung meldet nichts. Die Tests über `run command` laufen ohne Oberfläche: Sie setzen Werte direkt am gebundenen Objekt und erzwingen die Conclusion, auch wenn beides in der Oberfläche gesperrt wäre. `suchenUeberCommand`, `zuordnenUeberCommands` (mit der Lenkerauskunft) und `anlegenSuchenAendernUeberCommands` waren deshalb grün. Der Fehler zeigt sich nur in der laufenden Anwendung. Daraus folgt auch: Ein grüner `run command`-Test sagt nichts über die Wirkung von Berechtigungen aus.

- **Annahme:** keine mehr; Verhalten wie oben vom Nutzer beschrieben.

- **Ausgang:** `Lenker suchen` (Rolle Disponent) und `Lenkerauskunft` (Rolle Fuhrparkleiter) am 2026-10-05 von `CAN_OPEN_RO` auf `CAN_OPEN_RW` umgestellt, Make erfolgreich. `Fahrzeuge suchen` hatte der Nutzer in MPS bereits selbst geändert und steht auf „keine Berechtigung nötig“; das habe ich nicht angefasst. Plan 001 Abschnitt 7 und Plan 002 Abschnitt 7 nennen noch „RO“ und sind entsprechend zu lesen.

- **Was in die Doku gehört:**
  1. Bei `CAN_OPEN_RO`/`CAN_OPEN_RW` ausdrücklich: `RO` sperrt alle `Delegate Form`s (wie `DISABLED`) und alle Page Conclusions; Menü-Actions bleiben startbar und richten sich nach dem gestarteten Command.
  2. Bei `SEARCH_CMD` in „Die vier Command-Typen“ und in der Tabelle „Aufbau eines Commands“: Ein Such-Command mit Filter braucht `CAN_OPEN_RW` oder keine Berechtigung; `RW` bedeutet dort kein Schreibrecht, weil die Session nie committet wird.
  3. Im Abschnitt „Session-weites Read-only und Dirty“: Zusammenhang zwischen `CAN_OPEN_RO`, dem Read-only-Modus der Session und der Sperre der Formulare herstellen (bisher steht dort nur die Sperre der Conclusions).
  4. In „Commands ohne UI ausführen“: Hinweis, dass `run command` die Sperren durch `RO` nicht nachbildet.
  5. In „Häufige Fehler und Diagnose“ und in den Gotchas des Skills `objectflow-dsl`: „`SEARCH_CMD` mit `CAN_OPEN_RO` versehen“.
  6. Offen für die Doku: was gilt, wenn ein Benutzer über eine Rollenhierarchie sowohl einen `RO`- als auch einen `RW`-Eintrag erfüllt.

- **Nutzen des Verhaltens:** `CAN_OPEN_RO` ist das Mittel, einer Rolle eine reine Ansicht zu geben. Für die offene Frage aus P-058 (Disponent und Lenker-Einzelansicht) heißt das: `Lenker oeffnen` könnte zusätzlich `CAN_OPEN_RO` für den Disponenten bekommen; er sähe dann die Ansicht mit gesperrtem Formular und ohne „Speichern“, und die Edit-Commands blieben wegen ihrer eigenen Berechtigung dem Fuhrparkleiter vorbehalten.

- **Stand:** erledigt (`objectflow.md`: „Session-weites Read-only und Dirty“ nennt die gesperrten `Delegate Form`s; „Rollen, Scopes und Identities“ erklärt `CAN_OPEN_RO` als Read-only-Session, den Vorrang von `CAN_OPEN_RW` und den `SEARCH_CMD` mit Filterformular; Wortlaut „lesend/ändernd“ in der Kapiteleinleitung und in der Tabelle „Aufbau eines Commands“ berichtigt; „Commands ohne UI ausführen“: `run command` bildet die Sperren nicht nach. Kein Eintrag in „Häufige Fehler“ und in den Skills, um Doppelungen zu vermeiden)

## P-061: Zeilengewicht von Formularen im Grid

- **Stelle:** `moai/docu/dataux.md`, „Layouts, Tabs und Wiederverwendung“; Blueprint `grid-master-detail-subtree.json`
- **Unklar/Problem:** Die Doku nennt das Gewicht `-1` (`MinWeight`) nur in der Aufzählung der Gewichte und als Möglichkeit („ein kompaktes Suchformular oberhalb einer flexiblen Ergebnistabelle“). Eine Regel, dass ein Formular im Grid die minimale Höhe bekommt, steht nicht da; der Blueprint verwendet `1*`. Ich hatte den Formularen `1*` beziehungsweise `2*` gegeben, sie nahmen also unnötig Höhe ein.
- **Annahme:** keine
- **Ausgang:** Vom Nutzer am 2026-10-05 als vierte UI-Konvention vorgegeben und in `moai/conventions/moware-werkbank-ui_v1.md` eingetragen: Ein `Delegate Form` im `Grid Layout` hat immer das Zeilengewicht `-1`. Angewendet auf `FahrzeugSuche`, `LenkerSuche` und `FahrzeugAnsicht`; andere Page Panes haben kein Grid. Wirkung nur in der Oberfläche prüfbar.

## P-062: Disponent sieht die Lenker-Einzelansicht über `CAN_OPEN_RO`

- **Stelle:** Command `Lenker oeffnen`; P-058, P-060
- **Unklar/Problem:** Offen war, wie der Disponent Lenker „ansehen“ kann (FR-019), ohne Schreibrecht zu bekommen. Ungeklärt bleibt, welcher Eintrag gilt, wenn ein Benutzer über die Rollenhierarchie beide erfüllt: Der Fuhrparkleiter ist auch Disponent.
- **Annahme:** `Lenker oeffnen` hat `CAN_OPEN_RW` für den Fuhrparkleiter (erster Eintrag) und zusätzlich `CAN_OPEN_RO` für den Disponenten. Ich nehme an, dass der weitergehende Eintrag gewinnt.
- **Ausgang:** Am 2026-10-05 eingebaut, Prüfung und Make ohne Fehler, Tests grün (sie laufen als `leiter` und prüfen die Sperre nicht). In der Oberfläche zu prüfen: Der Disponent sieht die Ansicht ohne „Speichern“ und kann keine Edit-Commands starten; der Fuhrparkleiter kann weiter speichern. Falls der Fuhrparkleiter jetzt gesperrt ist, gewinnt `RO`, und die Rollen müssen anders geschnitten werden.
- **Stand:** erledigt (Nutzer, 2026-10-05: Der Generator sortiert `CAN_OPEN_RW` zuerst, `RW` gewinnt; steht in `objectflow.md` „Rollen, Scopes und Identities“, siehe P-060)

## P-063: Tabellen ohne Beschriftung

- **Stelle:** `moai/docu/dataux.md`, „Optionen für Formulare und Tabellen“ (`LABEL`); Blueprint `table-subtree.json`
- **Unklar/Problem:** Die Doku führt `LABEL` als Option auf, sagt aber nicht, dass eine Tabelle eine Beschriftung haben soll; der Blueprint setzt keine. Ich hatte keiner der vier Tabellen ein Label gegeben. In der Fahrzeugansicht stehen zwei Tabellen untereinander, ohne dass erkennbar ist, welche die Kilometerstände und welche die Zuordnungen zeigt.
- **Annahme:** Die Doku verbietet `LABEL` am obersten Element eines Page Pane (dort gilt der Page Title); diese Ausnahme habe ich in den Konventionstext übernommen.
- **Ausgang:** Vom Nutzer am 2026-10-05 als fünfte UI-Konvention vorgegeben und in `moai/conventions/moware-werkbank-ui_v1.md` eingetragen. Angewendet: „Gefundene Fahrzeuge“, „Kilometerstände“, „Zuordnungen“, „Gefundene Lenker“. Prüfung und Make ohne Fehler; Wirkung nur in der Oberfläche prüfbar.

## P-064: Beschriftung und Hotkey der Conclusions nicht geregelt

- **Stelle:** `moai/conventions/` (bisher keine Regel); `moai/docu/objectflow.md` nennt bei den Conclusions nur die semantischen Hotkeys `SCAN/UPDATE` und `GO/OK`, keine Vorgabe für Beschriftung oder `F12`.
- **Unklar/Problem:** Wie die Default-Conclusion je Command-Typ heißt und welchen Hotkey sie bekommt, stand nirgends. Ich hatte eigene Labels gewählt („Speichern“, „Suchen“, „Uebernehmen“ in `FuhrparkRessourcen`).
- **Annahme:** keine; Vorgabe des Nutzers vom 2026-10-05.
- **Ausgang:** Zwei Konventionen in `moai/conventions/moware-werkbank-ui_v1.md` ergänzt: Default-Conclusion mit `F12`, Beschriftung „OK“ (`GRAPH_EDIT_CMD`), „Aktualisieren“ (`SEARCH_CMD`), „Speichern & Schließen“ (`GRAPH_OWNER_CMD`); im Wizard „Zurück“ `F3` und „Weiter“ `F4` für den Page-Wechsel. Meine Auslegung: „Wizard“ = Command mit mehreren nacheinander durchlaufenen Pages; `GRAPH_OWNER_CMD(modal)` zählt wie `GRAPH_OWNER_CMD`. Angewendet über die drei Labels in `FuhrparkRessourcen`: `Speichern` → `SpeichernUndSchliessen` („Speichern & Schließen“), `Suchen` → `Aktualisieren`, `Uebernehmen` → `Ok` („OK“), alle mit Hotkey `F12` an der `LabelSpecification`. Jedes Label wurde schon vorher nur von einem Command-Typ verwendet, daher war keine Änderung an den Commands nötig. Einen Wizard gibt es in der Anwendung nicht. Make erfolgreich, `FahrzeugTests` 17/17 und `LenkerTests` 4/4 grün; in der Oberfläche nicht geprüft. Nachtrag (Nutzer, 2026-10-05): `Lenkerauskunft` ist eine Ausnahme, die Conclusion heißt dort „Suchen“ (neues Label `Suchen` mit `F12`). Die Ausnahme steht in der Konvention; ihre allgemeine Fassung („`SEARCH_CMD` ohne Trefferliste, der eine einzelne Auskunft liefert“) ist meine Formulierung.

---

# Zusammenfassung für die MoAI-Auswertung

Stand 2026-10-05, Ende des Laufs. Ergebnis: Features 001 und 002 modelliert, `FahrzeugTests` 17 von 17 und `LenkerTests` 4 von 4 grün gegen MariaDB, Anwendung `MjFuhrpark` startet. Die Oberfläche wurde vom Agenten nicht gesehen.

## Was gut funktioniert hat

- MPS-MCP: Modelle anlegen, Roots aus JSON einfügen, Prüfung je Root, Make und Testlauf (P-025, P-027).
- Die Textprojektion eines Roots war die wirksamste Kontrolle; sie entsprach der Doku (P-035).
- Das Beispielmodul `org.modellwerkstatt.dataux.tests` als Vorlage: Tiefendruck in eine Datei, Auswertung per Skript, Teilbäume als Blueprint übernehmen (P-020).
- Ab dem zweiten Feature liefen neue Commands, Page Panes und Tests beim ersten Versuch (P-057).

## Lücken in der Doku (nach Wirkung geordnet)

| Eintrag | Lücke |
|---|---|
| P-010, P-018, P-043 | Mindestinhalt einer lauffähigen `OFXConfig`, AppFactory für `fx8forms` |
| P-017 | JDBC-Treiber: wie er auf den Klassenpfad kommt |
| P-023 | Schema für MariaDB: Beschreibung ist Oracle-Syntax |
| P-040 | `BATCH` mit Auto-ID ist für MySQL/MariaDB nicht implementiert |
| P-037 | `optional` wird im Oder zu `(1 != 1)`, im Und zu `(1 = 1)`; eine reine Oder-Gruppe liefert keine Treffer, wenn alle Prädikate entfallen |
| P-028 | `DateLiteral` steht nach dem Anlegen auf „Serverdatum“ |
| P-022 | `INDEX` erzeugt einen eindeutigen Index |
| P-053 | Repository-Methode darf einer read-only Entity eine Liste zuweisen |
| P-030, P-048 | Welche Ausnahme im Test fliegt: `OFXAbortedException` beim Service, `RuntimeException` bei gesperrtem Command |
| P-011, P-034 | Jede Statusdeklaration braucht `ON_CREATION`; Status in DTOs startet nicht leer |
| P-013 | `OPTIMISTIC_LOCK` erzeugt die Spalte `TCN` |
| P-033 | Status aus einer Variablen in Custom SQL binden |
| P-026 | `session operation add`: Beschreibungstext ist Pflicht, kein Beispiel im Testmodul |
| P-029 | `LocalPropertyReference` gibt es in DataUX und in BaseLanguage |
| **P-060** | **`CAN_OPEN_RO` sperrt Formulare und Conclusions; ein `SEARCH_CMD` mit Filter darf nicht RO sein; `run command` merkt es nicht** |

## Lücken in den Konventionen

| Eintrag | Lücke |
|---|---|
| P-004 | Anwendung mit einem Bounded Context: eine Solution, alles Modelle |
| P-005 | Ort der Rollen ohne Benutzerbereich |
| P-050 | Regel über zwei Aggregate ohne Use-Case-Bereich; Zyklus auf Bereichsebene |
| P-055 | Zwei Services `TestDaten` in einer Testsuite brechen den Build |
| P-045, P-046, P-047, P-061, P-063 | UI-Konventionen fehlten; fünf wurden im Lauf ergänzt (Page Title, Aufteilung, Overflow-Menü, Formulargewicht im Grid, Tabellen-Label) |
| P-051 | Suche mit einer Page, Lesemodell als gemappte Abfrage: entschieden, aber nirgends geregelt |

## Skills, Blueprints und Werkzeuge

| Eintrag | Befund |
|---|---|
| P-021, P-035 | Blueprints für Config, Rollen, Service, Testsuite und Command sind leere Roots |
| P-038 | Blueprint bindet ein `GridLayout`, was im Page Pane ein Fehler ist |
| P-047 | Blueprint gibt dem obersten Submenü einen Text |
| P-007 | `mps_mcp_list_open_projects` scheitert ohne `projectPath` |
| P-024 | Kind löschen: Skill und Werkzeug widersprechen sich |
| P-020, P-031 | `FIND_INSTANCES` und Stapel-Updates liefern sehr große Antworten |
| P-014 | Die DSL-Dokus kosten rund 150.000 Tokens Kontext vor dem ersten Plan |
| P-016 | Beispielkonfigurationen im Testmodul enthalten Zugangsdaten |
| P-048 | `FAIL IN` meldet eine falsche Ausnahme wie eine fehlende |

## Fehler des Agenten

- P-060: Alle Such-Commands mit `CAN_OPEN_RO` modelliert; in der Oberfläche unbenutzbar, in den Tests unbemerkt.
- P-002: Solution-Namen aus dem Verzeichnisnamen geschlossen.
- P-039: Task zu früh abgehakt.
- P-037: Suchtest prüfte den Fall ohne Suchbegriff nicht; der Fehler fiel nur durch eine Konsolenausgabe auf.
- P-048: Falsche Deutung einer Testmeldung an den Nutzer weitergegeben.
- P-055: Verträglichkeit zweier `TestDaten` zu früh bestätigt.
- P-045: Keine Page Titles gesetzt und die Ansicht links/rechts geteilt, obwohl die Doku Hinweise enthielt.

## Offen am Ende des Laufs

- Probelauf in der Oberfläche mit beiden Rollen (Nutzer).
- AC-1.4 in 001: Spec oder Modell anpassen (P-059).
- Rollenwirkung in der Oberfläche: Disponent mit `CAN_OPEN_RO` auf `Lenker oeffnen`, Fuhrparkleiter mit beiden Einträgen (P-062).
- Freigabe der Constitution (P-008).
- Sortierung der Kindliste bei `listJoin` (P-059).
