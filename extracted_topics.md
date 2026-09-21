# Aus „MoWare Werkbank 2022“ extrahierte Themen

## Quellenstatus und Verwendung

Dieses Dokument fasst die Themen aus der Datei `MoWare Werkbank 2022.pdf` nach den drei MoWare-DSLs zusammen. Die PDF umfasst 67 Seiten. Ihr Deckblatt bezeichnet sie als **„MoWare Werkbank 2023 – unfertige Themensammlung V1“**; mehrere Folien tragen zusätzlich ältere Stände wie „Winter 2021“ oder „Frühling 2022“.

Die Inhalte sind daher als historische Arbeitsnotizen und Dokumentationskandidaten zu verstehen, nicht als aktuelle technische Quelle der Wahrheit. Begriffe, Optionen und Laufzeitverhalten müssen vor der Übernahme in die reguläre Dokumentation mit den geladenen MPS-Sprachen, ihren Prüfregeln und aktuellen Verbrauchermodellen abgeglichen werden. Seitenangaben beziehen sich auf die PDF-Seiten.

Die Folien behandeln einige übergreifende Abläufe. In dieser Zusammenfassung werden fachliches Modell, Commands, Sessions und Producer/Consumer-Logik unter ObjectFlow eingeordnet, Persistenzthemen unter ManMap sowie Page Panes, Oberflächen, Anwendungen und die ausführbare Batch-Konfiguration unter DataUX.

## ObjectFlow (`org.modellwerkstatt.objectflow`)

### Architektur und Verantwortlichkeiten

Die Werkbank wird als Zusammenspiel von Commands, Services, Repositories, Page Panes, Anwendungen beziehungsweise Jobs und Tests dargestellt (Seiten 2–5). Die fachliche Verarbeitung liegt in einer Unit beziehungsweise einem Use Case:

- Commands koordinieren eine Benutzerinteraktion oder einen automatisierten Ablauf.
- Services enthalten fachliche beziehungsweise anwendungsbezogene Logik.
- Repositories kapseln den Datenzugriff.
- Die Session verbindet den Ablauf mit geladenen und veränderten Objekten.
- Presentation Models bereiten Daten für die Interaktion auf.
- Page Panes beschreiben die Darstellung und werden in der PDF als eigener UI-Baustein geführt.
- Tests und Standardpersistenz gehören zur jeweiligen fachlichen Unit.

Die Skizze betont die Trennung von interaktionsspezifischer Logik und fachlicher Domänenlogik. Anwendungen, Batchjobs und Tests verwenden dieselben fachlichen Bausteine, aber unterschiedliche Laufzeitumgebungen und Infrastrukturkomponenten.

### Strings, Übersetzungen und Serialisierung

Für Strings wird eine plattformabhängige Formatierung diskutiert (Seite 8). Genannt werden insbesondere:

- Formatierung von Dezimalzahlen,
- unterschiedliche Darstellungen von Statuswerten,
- Datums- und Zeitwerte,
- Übersetzbarkeit,
- plattformabhängige Darstellung,
- die Frage, ob Formatierungsdienste an eine Session oder eine globale Instanz gebunden sein sollen.

Für Serialisierung, beispielsweise nach JSON, skizziert die PDF eine erweiterbare Serdes-Struktur (Seite 9). Projektspezifische Serialisierer können Properties filtern, verändern, formatieren oder besonders behandeln. Eine gemeinsame Basisschicht soll die Standardkonvertierung bereitstellen.

### Session und Unit of Work

Die komplexere Session-Struktur besteht aus einem Session Owner und mehreren darin ausgeführten Bearbeitungsschritten (Seiten 10 und 14–18):

- Ein `GRAPH_OWNER`, `SEARCH_COMMAND` oder modaler Graph Owner stellt die Session bereit.
- Mehrere `GRAPH_EDIT`-Commands können innerhalb dieser Session arbeiten.
- Session Operations werden gesammelt und bei `FINAL_OK` innerhalb einer Datenbank-Session beziehungsweise Transaktion ausgeführt.
- Neu erzeugte Objekte müssen mit `session.ensureInSession(...)` in die Session aufgenommen werden, damit die Anwendung Änderungen und offene Arbeit erkennt.
- Abfragen nach ausgecheckten Entity-Typen beziehungsweise deren Schlüsseln werden als Diagnose- und Navigationsmöglichkeit genannt.
- Bereits geladene Read-only-Entities sollen aus dem Session-Cache geliefert werden, ohne erneut auf die Datenbank zuzugreifen.

Die Folien unterscheiden Entity-Schlüssel und Referenzschlüssel:

| Schlüsselart | Historischer Nullwert | Prüfung einer nicht gesetzten Referenz |
| --- | --- | --- |
| Integer | `0` | `reference#KEY.isNullKey` |
| String | leerer String; bei Oracle gegebenenfalls `null` | `reference#KEY.isNullKey` |
| zusammengesetztes Value Object | Null-Value-Object aus Nullwerten | `reference#KEY.isNullKey` |

Bei einer Entity selbst soll für die Entscheidung „neu in der Session“ die Metainformation der Entity verwendet werden. Die direkte Anwendung von `isNullKey` auf einen zusammengesetzten Entity-Schlüssel wird auf der Folie als fehlerhaft markiert (Seiten 15–16).

### ViewObjects

ViewObjects werden als nicht persistierbare Datencontainer beschrieben (Seiten 17 und 42):

- Änderungen an einem ViewObject markieren die Session nicht als dirty.
- Sie können primitive Werte, Value Objects, Referenzen und Listen enthalten.
- Sie eignen sich für Suchergebnisse, Datenbankberechnungen und andere temporäre Projektionen.
- Als Identität wird in den Folien der Hashwert genannt; zwei inhaltlich gleiche ViewObjects gelten damit nicht automatisch als dieselbe Instanz.

Die PDF widerspricht sich bei der Session-Integration: Seite 17 sagt ausdrücklich, ViewObjects seien in keiner Weise session-integriert. Seiten 41 und 44 bezeichnen No-Key-/ViewObject-Ergebnisse dagegen als session-integriert, wobei der Hashwert die Instanzen unterscheidet. Dieses Verhalten muss vor einer Übernahme in die aktuelle Dokumentation geklärt werden.

### Preconditions, Guards, Validierung und Exceptions

Die Folien unterscheiden drei Fehlerklassen (Seiten 11–13):

- **Precondition:** Ein für den Benutzer verständliches und grundsätzlich korrigierbares Problem. Die Meldung soll Problem, betroffenen Wert und mögliche Lösung beschreiben. Ein Warning-Hinweis kann Feedback geben, ohne den Ablauf zu unterbrechen.
- **Guard:** Ein unerwarteter oder technisch nicht durch den Benutzer korrigierbarer Zustand. Er kann eine Session beenden und soll administrativ sichtbar werden.
- **Exception:** Technischer Ausnahmefall; seine Weiterleitung und Darstellung ähnelt in vielen Abläufen der Guard-Behandlung.

Validierungsblöcke sammeln mehrere Prüfungen in einem Report. Als Modellierungsmuster wird vorgeschlagen, zuerst benötigte Fakten und Konfigurationen zu laden, anschließend alle Voraussetzungen zu prüfen und erst danach das Aggregat zu verändern.

Die konkrete Behandlung hängt vom Kontext ab: Anwendung oder Job, Graph Owner oder Graph Edit, Successor-Ablauf sowie die aktuelle Phase (`command init`, `page init`, Page Conclusion oder `FINAL_OK`). Die Folien sind hierzu eine Entwurfs- und Verhaltenstabelle; die Details müssen gegen die aktuelle Runtime geprüft werden.

### Command-Patterns

Die Seiten 19–26 sammeln wiederverwendbare Command-Muster. Ziel sind unterstützte, getestete Abläufe ohne duplizierte Geschäftslogik.

| Muster | Extrahierte Absicht |
| --- | --- |
| Search → Main Document → Graph Edit | Ein `SEARCH_COMMAND` findet Objekte; ein `GRAPH_OWNER` lädt und speichert das Hauptdokument; `GRAPH_EDIT` übernimmt einzelne Editieroperationen. Das Hauptdokument selbst wird in der UI nicht direkt editiert. |
| Compound Action | Dieselbe Tätigkeit, etwa Drucken oder Freigeben, kann aus verschiedenen Menüs gestartet werden. Mehrere Commands werden über ihre Conclusions verkettet. Für mehrseitige Commands und UI-Anzeige nennt die Folie Einschränkungen beziehungsweise offene Fragen. |
| Successor / Task Handling | Eine Tätigkeit kann unabhängig von einer Aufgabenverwaltung modelliert und bei Bedarf in einen vorgeschalteten Aufgaben-Command eingebettet werden. Für eine gemeinsame Unit of Work wird eine gemeinsame Session erwogen. |
| Create/Edit Successor | Ein Command erzeugt aus einem Artefakt ein Folgedokument und öffnet anschließend dessen Bearbeitung. Erzeugung und Bearbeitung sollen möglichst gemeinsam bestätigt oder zurückgenommen werden. Ein noch nicht persistiertes Dokument darf nicht unnötig erneut ausgecheckt werden. |
| Multiple Execution on Lists | Für mehrere markierte Entities wird jeweils ein Command ausgeführt. Bei Graph Ownern in Suchansichten werden Fehler gesammelt; bei Graph Edits innerhalb eines Graph Owners soll ein nicht erfolgreicher Abschluss weitere Ausführungen stoppen. |
| Filter Search Pattern | Ein eigenes ViewObject enthält Filter-Properties und eine Ergebnisliste. Filterseite und Ergebnisliste binden an dasselbe ViewObject beziehungsweise dessen Listen-Property. |
| Graph Composition | Ein bearbeiteter Teilgraph kann Änderungen an einem übergeordneten Aggregat auslösen. Child-Termination wird genutzt, um das übergeordnete Aggregat erneut zu validieren, zu ergänzen oder abzuschließen. |
| Modal Graph Owner | Ein modaler Graph Owner sperrt andere Tabs und isoliert eine Editieroperation. Die Folie stellt zusätzlichen Checkout und die genaue Unit-of-Work-Grenze als offene Entwurfsfrage dar. |

### Producer/Consumer und Job-Verarbeitung

Ein Job verbindet einen Producer mit einem Consumer beziehungsweise einem verarbeitenden Command (Seiten 27–31):

- Der Producer ermittelt Arbeitseinheiten und füllt eine Inbox.
- Consumer verarbeiten die Arbeitseinheiten, häufig mit einem Graph Owner und optionalen Successor-Commands.
- Die traditionelle Variante nutzt `FINAL_OK` für Check-in und `FINAL_CANCEL` für Fehlerbehandlung.
- Die als „new-style“ bezeichnete Variante behandelt erwartbare fachliche Probleme explizit im normalen Ablauf: Problem protokollieren, Fehlerstatus setzen und gezielte Session Operations für Marker oder Journal registrieren.
- Exception-Strategien bestimmen Wiederholung, Verzögerung, Leeren der Inbox und Fortsetzung.
- Blockierende externe Aufrufe, etwa Datenbank- oder FTP-Zugriffe, werden als Betriebsrisiko genannt.

Preconditions, Guards und Exceptions werden bei Jobs bis `FINAL_CANCEL` beziehungsweise zur Exception-Strategie weitergereicht. Für komplexe Fehlerfälle empfiehlt die Sammlung explizite Protokollierung und gezielte Session Operations statt duplizierter Fallunterscheidungen.

### Logging und Betriebsdiagnose

Die Seiten 32–38 beschreiben zwei Betriebsarten:

- ohne PortJ mit umgebungsabhängigen Logger-Einstellungen,
- mit PortJ, aktiviert über die AppFactory-Konfiguration, wobei MoWare-Meldungen oberhalb einer Priorität weitergeleitet werden.

Genannt werden Framework-Trace, Application-Trace, Problem- und Message-Kanäle sowie `OFXLogger` als Fallback, wenn keine Session oder kein Event Bus verfügbar ist. Jobs verwenden in den Folien einen Fake Event Bus, um Logging ohne normale UI-Infrastruktur zu ermöglichen. Trace-Stufen sollen im Produktivbetrieb zurückhaltend eingesetzt werden. Die Folie zu `DataAccessException` ist lediglich als TODO angelegt und enthält keine ausgearbeitete Lösung.

### Command-Termination, explizites Merge und Selektion

Die Seiten 57–67 behandeln die Reaktion eines Parent-Commands auf beendete Child-Commands und betonen erneut Aggregatgrenzen.

Im Legacy-Modus werden gepushte Entities beziehungsweise DTOs teilweise automatisch in Suchergebnisse übernommen oder ersetzt und anschließend selektiert. Der neue Command-Termination-Modus soll dieses implizite Verhalten entfernen:

- Termination-Handler reagieren auf einen bestimmten Entity-/DTO-Typ oder unspezifisch auf jeden beendeten Command.
- Gepushte Objekte müssen explizit in Graph und Session übernommen werden.
- Die Auswahl muss anschließend mit `pushSelection()` auf die integrierte beziehungsweise neu erzeugte Instanz gesetzt werden.
- Mehrere typbezogene Handler können auf mehrere gepushte Objekte reagieren.

Für das explizite Session-Merge werden folgende Regeln skizziert:

- Primitive Werte und Schlüssel werden in das Ziel übernommen.
- Das Ziel kann aus der Session anhand des Schlüssels gefunden, neu erzeugt oder explizit übergeben werden.
- Der Read-only-Status des Ziels muss zum gewünschten Merge passen.
- Listen werden elementweise über Schlüssel abgeglichen; neue Elemente werden ergänzt und vorhandene ersetzt.
- Beim Listen-Merge werden entfernte Elemente laut Folie nicht automatisch aus der Zielliste gelöscht.
- Referenzen werden separat gemergt und anschließend am Ziel gesetzt; dafür wird der Read-only-Status des Ziels vorübergehend aufgehoben und danach wiederhergestellt.

Die Folien nennen dafür die Optionen beziehungsweise Modi `NEW_CMD_STYLE_HANLDING` und `NEWSTYLE_CMD_TERM_HANDLING` in unterschiedlicher Schreibweise. Der aktuelle technische Name muss in der Sprache geprüft werden.

## ManMap (`org.modellwerkstatt.manmap`)

### Persistierbare Graphen und No-Key-Lesemodelle

Die Folien unterscheiden zwei Datenzugriffsarten (Seiten 39–44):

- **Entities:** besitzen einen Key, werden über eine ManMap Persistence Description gemappt und können abgefragt und gespeichert werden.
- **ViewObjects:** werden über No-Key-Mappings aus Abfrageergebnissen erzeugt und nicht zurückgespeichert. Result-Sets benötigen dabei keinen eindeutigen fachlichen Schlüssel.

ViewObjects dienen dazu, Datenbankergebnisse und optimierte Berechnungen in Objekte zu verpacken. Dadurch stehen persistierbare Entity-Graphen und nicht persistierbare Abfragegraphen nebeneinander.

Wie im ObjectFlow-Abschnitt beschrieben, sind die Folien zur Session-Integration der ViewObjects widersprüchlich. Für die aktuelle Semantik von No-Key-Mappings dürfen die Aussagen dieser PDF deshalb nicht ungeprüft übernommen werden.

### Joins und Session-Identität

Joins sollen zusammengehörige Daten in einem Datenbankzugriff laden (Seiten 43–44):

- Bei Entities sorgt die Session für Identität: Dieselbe Entity mit demselben Key soll nicht mehrfach geladen werden, und Read-only- sowie veränderbare Varianten desselben Keys dürfen nicht unkontrolliert nebeneinander existieren.
- Die Session dient dabei als Cache; wiederholte Auflösung desselben Keys soll dieselbe Entity-Instanz liefern.
- Für ViewObjects beschreibt die PDF ebenfalls Join-Unterstützung, verwendet zur Unterscheidung der Ergebnisse aber deren Hashwert. Diese Aussage gehört zum bereits markierten Prüfbedarf.

### SQL-Import und erzeugte Modelle

Als Arbeitsablauf für bestehendes SQL wird vorgeschlagen (Seite 45):

1. SQL zunächst in einer SQL-Workbench entwickeln.
2. Die Anweisung in ein Map-SELECT-Konstrukt in MPS übernehmen.
3. Mit einer Intention ein ViewObject und das zugehörige Mapping erzeugen.
4. Mit einer weiteren Intention einen Test erzeugen, der Mapping und Ergebnis langfristig absichert.
5. Alternativ Metadaten aus `desc <view>` über einen MoWare-Importer verwenden.

Als Erweiterungen werden genannt (Seite 46):

- Überschreiben einer Sequence in Mappings, ausdrücklich Oracle-spezifisch,
- Konvertierungswerkzeuge zwischen ViewObject und Entity,
- ein erweiterbarer `DESC`-zu-Entity-Importer,
- ein erweiterbarer `DESC`-zu-No-Key-Mapping-Importer.

Ob und unter welchen Namen diese Intentionen und Importer heute existieren, muss in der aktuellen Sprache geprüft werden.

### Aggregate, Referenzen und Schlüssel

Die Aggregate-Folie verwendet eine Rechnung mit einer Liste von Positionen (Seite 47). ManMap soll sowohl echte Entity-Referenzen als auch reine Schlüsselreferenzen abbilden können. Das fachliche Aggregat stellt Methoden wie `addPosition`, `attachPosition` oder `getOrCreatePosition` bereit, während das Mapping die relationale Beziehung beschreibt.

Für große oder alternative Schlüssel werden folgende Themen genannt (Seite 48):

- Auswirkungen eines Wechsels von `int` zu `long`,
- String-Schlüssel mit Auto-ID-Verhalten,
- Sequence-basierte Schlüssel ohne die Beschränkung auf Integer,
- UUID-basierte Schlüssel,
- die Testsuite als Referenz für unterstützte Varianten.

Die Archiv-Folie (Seite 49) enthält nur eine Überschrift und keine extrahierbare fachliche Beschreibung.

### Batch-Speichern

Für Oracle wird auf Bulk Insert und Bulk Update eingegangen (Seite 50). Als abschließender Lösungsansatz nennt die PDF die Unterstützung manipulierter Spalten durch einen neueren Oracle-Treiber und die Operation:

```text
save BATCH (list<Entities> list)
```

Damit sollen Insert- und Update-Operationen für größere Mengen gebündelt werden. Die Folie verweist außerdem auf externe JDBC- und Oracle-Beispiele, beschreibt aber keine vollständige DSL-Syntax oder Transaktionssemantik.

## DataUX (`org.modellwerkstatt.dataux`)

### Page Panes, Anwendungen und Plattformen

Page Panes werden als Präsentationsbausteine zu Commands eingeordnet (Seiten 2–5). Anwendungen und Batchjobs können je nach Konfiguration mit unterschiedlicher UI- beziehungsweise Laufzeitinfrastruktur ausgeführt werden:

- Vaadin,
- FX8,
- H2Forms,
- Batchjob mit UI,
- Ausführung auf der Konsole beziehungsweise in der IDE,
- Servlet-Ausführung auf Tomcat,
- Tests mit einer einfachen AppFactory.

Authentifizierung für ein Modul soll nur ausgeführt werden, wenn tatsächlich eine UI vorhanden ist. Die Folien unterscheiden außerdem Umgebungen mit oder ohne User Environment, User Service, Lock Service und Print Service.

### Übersetzungen und plattformabhängige Darstellung

Die DataUX-Folien nennen folgende übersetzbare UI-Inhalte (Seite 52):

- Labels und Beschreibungen,
- Actions und Buttons,
- Tabellen und Delegates,
- MoWare-Systemmeldungen,
- Statuswerte und MultiStrings.

Das Modell soll die zentrale Quelle für Übersetzungen sein. Vorgesehen sind der Export neuer und bereits übersetzter Texte, der Reimport der Übersetzungen und eine Übersetzungsdatei für das Deployment. Die Folie kennzeichnet die technische Umsetzung noch als erwartbar fehleranfällig beziehungsweise unfertig.

### Live-Suche und Update-Conclusions

Für eine „Live Search View“ wird ein bindingsbasierter Ablauf skizziert (Seite 53):

- Parameter müssen nicht zwischen UI-Komponenten weitergereicht werden, weil Bean Binding verwendet wird.
- Eine gemeinsame Update-Conclusion reicht aus, wenn Änderungen über das Binding erkannt werden.
- Delegates lösen die Conclusion aus, sobald sich ein geeigneter Wert ändert, beispielsweise ein Status.
- Bei Textfeldern erfolgt die explizite Übernahme etwa durch Enter, Tab oder einen Suchbutton.
- Eine dynamische Änderung des Button-Texts wird als mögliche, aber noch offene Option erwähnt.

### Update/Scan und Scanner-Eingaben

Eine Update/Scan-Conclusion bezieht sich auf ein bestimmtes Feld (Seiten 54–55):

1. Eine Eingabe wird in dieses Feld geschrieben.
2. Anschließend wird die zugeordnete Conclusion ausgelöst.
3. Konzeptionell entspricht dies einem Hotkey für eine spezielle Conclusion.

Für EAN plus Code-Typ werden mehrere entsprechend markierte Delegates ausgewertet:

- Der erste Delegate nimmt die Hauptinformation auf.
- Ein zweiter Delegate kann den Code-Typ aufnehmen.
- Weitere markierte Delegates werden ignoriert.
- `FOLD` kann das Feld für den Code-Typ zunächst ausblenden.
- `FORCE NUMERIC EDITOR` erzwingt einen numerischen Editor, obwohl die gebundene Property als String modelliert ist.

### Weitere UX-Themen mit Klärungsbedarf

Die letzte DataUX-Folie (Seite 56) nennt nur offene Stichworte:

- Mouse Controller gegenüber Key Controller pro Delegate,
- explizites `RequestFocus` gegenüber Standardfokus,
- direkte Kopplung gegenüber Slots-and-Signals,
- Verhalten bei mehreren Delegates,
- F12 gegenüber Enter als UX-Konvention.

Diese Punkte sind nicht ausgearbeitet und eignen sich daher zunächst als Recherche- oder Dokumentations-Backlog.

### Batchjob-Konfiguration

Die Job-Folien beschreiben drei Ausführungsmodi, die der ausführbaren Batch-Konfiguration zuzuordnen sind (Seiten 28–31):

- **Time Specific Mode:** Cron-Ausdrücke starten einen Producer zu bestimmten Zeiten. Mehrere Cron-Ausdrücke pro Pair sind möglich; der nächste früheste Termin gewinnt. Die Consumer arbeiten anschließend, bis die Inbox leer ist.
- **Cron Window Mode:** Ein Pair läuft grundsätzlich wiederholt mit einer Pause zwischen den Durchläufen. Der Cron-Ausdruck definiert ein Zeitfenster. Außerhalb des Fensters wird verbleibende Arbeit beim nächsten Fenster fortgesetzt.
- **Dependent Mode (`DEPENDENT_CONSECUTIVE`):** Mehrere Producer/Consumer-Paare laufen abhängig nacheinander. Nur das erste Pair benötigt eine Zeitplanung. Ein nachgelagertes Pair läuft nur, wenn seine Vorgänger erfolgreich waren.

Die Exception-Strategie beeinflusst Wiederholung, Wartezeit und Inbox-Behandlung. Ein manueller Producer-Start führt im Dependent Mode laut Folie nur das ausdrücklich ausgewählte Pair aus. Beim Zusammenspiel von abhängigen Pairs und Cron-Fenstern soll nach einem Fehler wieder mit dem Producer des ersten Pairs begonnen werden.

Diese Betriebsdetails sind besonders stark versionsabhängig und müssen vor der Übernahme in die aktuelle DataUX-Dokumentation gegen `BatchJobModule`, seine Optionen und die aktuelle Runtime geprüft werden.
