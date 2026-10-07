# modellwerkstatt MoWare-Werkbank – Drei DSLs zur Modellierung von Geschäftsanwendungen

## Zweck und Geltungsbereich

Dieses Dokument ist die architektonische Einstiegsseite zur **modellwerkstatt MoWare-Werkbank**. Es erklärt die Zuständigkeiten und das Zusammenspiel der drei DSLs, die gemeinsamen Grundprinzipien sowie den Weg vom fachlichen Modell zur laufenden Anwendung.

Die Beispiele sind fachliche Skizzen und keine ausführbare DSL-Syntax. Konkrete Konzepte, Eigenschaften, Einschränkungen und Modellierungsmuster werden in den jeweiligen DSL-Dokumentationen beschrieben. Bei Abweichungen zwischen Dokumentation und den geladenen MPS-Sprachen sind die Sprachdefinitionen und ihre Prüfregeln die technische Quelle der Wahrheit.

Die Dokumentation beschreibt beobachtete und technisch bestätigte Praxis. Sie legt keine zusätzliche, von der Sprache nicht erzwungene Architektur fest; das tun die [verbindlichen Konventionen](#verbindliche-konventionen). Wo sich aus bestehenden Anwendungen wiederkehrende Empfehlungen ergeben, werden diese als solche benannt.

## Modellierungssprachen und Laufzeitumgebungen

Die **modellwerkstatt MoWare-Werkbank** basiert auf JetBrains MPS und umfasst drei eng integrierte domänenspezifische Sprachen (DSLs) zur Erstellung von Geschäftsanwendungen. Sie decken Persistenz, Geschäftslogik und Benutzeroberflächen ab.

**ManMap** (`org.modellwerkstatt.manmap`) bildet die Persistenzschicht der Anwendung. Die Sprache definiert die Zuordnung zwischen relationalen Datenbanktabellen und Entitäten und stellt Operationen zum Laden, Speichern und Löschen bereit. Diese bilden die Grundlage für den Datenzugriff über Repositories. Darüber hinaus unterstützt ManMap die Arbeit mit Lesemodellen (Read Models) und Tabellenmodellen (Table Models): Komplexe SQL-Abfragen lassen sich formulieren und ihre Ergebnismengen über spezialisierte Mapper in DTOs (Data Transfer Objects) überführen.

**ObjectFlow** (`org.modellwerkstatt.objectflow`) dient der Modellierung von Service-Komponenten und Geschäftslogik. Die Sprache umfasst fachliche Datenstrukturen wie Entities und Value Objects sowie Commands zur Beschreibung von Aktionen und Anwendungsabläufen. Darüber hinaus unterstützt ObjectFlow die Modellierung von Testabläufen in Testsuiten sowie die Definition von Rollen und Berechtigungen.

**DataUX** (`org.modellwerkstatt.dataux`) dient der Modellierung von Benutzeroberflächen, Anwendungen und Batchjobs. Tabellen und Formulare werden durch ihre Spalten, Felder, Formatierungen und Datenbindungen beschrieben; Layouts strukturieren die Darstellung und ermöglichen die Zusammenstellung komplexerer Oberflächen. Anwendungen dienen für Endanwender als Einstiegspunkt und verfügen über das Hauptmenü. Für die automatisierte Verarbeitung lassen sich Batchjobs modellieren.

Aus den in MPS modellierten Anwendungen wird Java-Code generiert; die drei Laufzeitumgebungen sind unter [Laufzeitumgebungen](#laufzeitumgebungen) beschrieben.

## Ziele der Werkbank

Die **modellwerkstatt MoWare-Werkbank** stellt die fachliche Gestaltung von Geschäftsanwendungen in den Mittelpunkt: Welche Daten werden benötigt, wie hängen sie zusammen, welche Geschäftsregeln gelten und wie arbeiten Benutzer mit ihnen? Die Modellsprachen bieten dafür passende Ausdrucksmittel. Generatoren und Laufzeitumgebungen übernehmen wiederkehrende technische Aufgaben und Infrastruktur-Code. Dadurch konzentriert sich die Anwendungsentwicklung auf fachliche Datenstrukturen, Geschäftslogik und Benutzerinteraktionen.

**Fachliche Modellierung.** Die Entwicklung geeigneter Datenstrukturen und korrekter Geschäftsregeln bleibt die zentrale Entwurfsaufgabe (Einordnung unter [Zentrale Konzepte](#zentrale-konzepte-der-moware-werkbank)).

**Ausdrucksstarke Geschäftslogik.** Berechnungen, Prüfungen und Änderungen werden unmittelbar an den fachlichen Datenstrukturen formuliert. Java-Ausdrücke und Mengenoperationen unterstützen diese Arbeit. Technische Details der verwendeten UI-Frameworks und Laufzeitumgebungen werden weitgehend durch die Werkzeugkette gekapselt.

**Einheitliche Architektur und klare Zuständigkeiten.** Die Sprachkonzepte geben vor, wo Datenzugriff, Geschäftslogik und Benutzeroberflächen beschrieben werden. Diese gemeinsame Struktur erleichtert die Orientierung, die Wiederverwendung und die Zusammenarbeit. Fachliche Begriffe bleiben im Modell sichtbar und unterstützen die Abstimmung zwischen Entwicklern und Fachverantwortlichen.

**ExpensiveCode und CheapCode.** MoWare unterscheidet zwischen aufwendig erarbeitetem Fachwissen (*ExpensiveCode*) und leichter überprüfbaren und anpassbaren Teilen einer Anwendung (*CheapCode*). Zum ExpensiveCode gehören insbesondere fachliche Datenstrukturen, Geschäftsregeln und Verarbeitungslogik. Ihre Entwicklung erfordert Domänenwissen und sorgfältige Abstimmung; Fehler sind häufig erst durch eine fachliche Prüfung erkennbar. CheapCode umfasst dagegen UI-Beschreibungen, Menüs und die Gestaltung der Interaktion mit dem fachlichen Modell. Fehler in diesen Bereichen fallen beim Ausprobieren meist schnell auf und lassen sich gezielt korrigieren. Das fachliche Modell verlangt besondere Sorgfalt, während Oberflächen und Bedienabläufe durch kurze Feedbackzyklen schrittweise verbessert werden können.

**Langfristige Wartbarkeit und technische Flexibilität.** Das fachliche Wissen wird in den Modellen festgehalten. Generatoren und Laufzeitumgebungen bestimmen dessen technische Umsetzung. Diese Trennung ermöglicht es, fachliche Anforderungen und technische Infrastruktur weitgehend unabhängig weiterzuentwickeln. Ziel ist, bestehende Modelle langfristig zu nutzen und Anpassungen an Frameworks oder Ausführungsplattformen möglichst zentral umzusetzen.

## Zentrale Konzepte der MoWare-Werkbank

Der gesamte Stack orientiert sich stark an Domain-Driven Design (DDD), übernimmt aber nicht sämtliche DDD-Konzepte. Diese Übersicht erfasst die zentralen Konzepte der drei MoWare-Sprachen. Sie beschreibt die erkennbare Verantwortung der Konzepte, ohne zusätzliche DDD-Regeln für die DSLs festzulegen.

### Einordnung entlang der fachlichen Architektur

| Schicht | Konzept | DSL | Kapitellandkarte |
| --- | --- | --- | --- |
| Fachliches Modell | `Entity`, `Value Object`, `DTO` | `org.modellwerkstatt.objectflow` | [Fachliche Datenmodellierung](objectflow.md#kapitellandkarte-fachliche-datenmodellierung) |
| Geschäftslogik und Anwendungsfälle | `Service`, `Command` | `org.modellwerkstatt.objectflow` | [Services und Domänenlogik](objectflow.md#kapitellandkarte-services-und-domänenlogik), [Commands und Anwendungsabläufe](objectflow.md#kapitellandkarte-commands-und-anwendungsabläufe) |
| Persistenz | `Persistence Description`, `Repository` | `org.modellwerkstatt.manmap` | [Persistenz-Mappings](manmap.md#kapitellandkarte-persistenz-mappings), [Repository](manmap.md#kapitellandkarte-repository) |
| Benutzeroberfläche | `Page Pane`, `Table`, `Delegate Form`, `Grid Layout`, `Tab Layout`, `Custom UI Element` | `org.modellwerkstatt.dataux` | [UI-Komposition](dataux.md#kapitellandkarte-ui-komposition) |
| Ausführbare Module | `AppUI Module`, `BatchJob Module` | `org.modellwerkstatt.dataux` | [Anwendung](dataux.md#kapitellandkarte-anwendung), [Batchjob](dataux.md#kapitellandkarte-batchjob) |
| Querschnitt | `OFXConfig`, `OFXTestSuit`, Roles and Permissions, Static Ressources | `org.modellwerkstatt.objectflow` | [Querschnittsthemen](objectflow.md#kapitellandkarte-querschnittsthemen), [Tests](objectflow.md#kapitellandkarte-tests) |

### Bezeichnung der Konzepte

Der **Name** eines Konzepts entspricht seiner sichtbaren Projektion in MPS. Der **Konzeptname** bezeichnet das technische AST-Konzept; der **FQ-Name** ist dessen vollständig qualifizierter Name. Die Kapitellandkarten der DSL-Dokumentationen führen alle drei Bezeichnungen zusammen; bei dort fehlenden Konzepten ergänzt der Fließtext beim ersten Auftreten den Konzeptnamen beziehungsweise bei Konzepten aus anderen Sprachen den FQ-Namen in Klammern und verwendet danach nur noch den Namen. Hat ein Konzept keine als Wort benennbare Projektion, wird sein Konzeptname verwendet. Umschreibungen und Kurzformen treten nicht an die Stelle von Projektion oder Konzeptname. Zwei Ausnahmen: `Service` und `OFXConfig` werden mit ihrem Konzeptnamen bezeichnet, obwohl der Editor `component` beziehungsweise `Configuration` zeigt.

## Zusammenspiel der DSLs

Eine typische Geschäftsanwendung verbindet die drei Sprachen entlang eines durchgängigen Daten- und Kontrollflusses:

```text
ObjectFlow
Entity / Value Object / DTO / Service / Command
        │
        ├── ManMap
        │   Mapping / Repository / SQL / DTO-Mapping
        │
        └── DataUX
            Page Pane / Form / Table / Layout / Interaktion
                    │
                    ▼
             AppUI Module / BatchJob Module
                    │
                    ▼
                 OFXConfig
                    │
                    ▼
        fx8forms / turkuforms / h2forms
```

- **ObjectFlow** definiert die fachlichen Daten, Regeln und Anwendungsfälle.
- **ManMap** verbindet Entities und DTOs mit der relationalen Persistenz und stellt den Datenzugriff über Repositories bereit.
- **DataUX** projiziert Commands und deren Daten in Seiten, Formulare, Tabellen und ausführbare Module.

### Wo gehört eine Änderung hin?

| Änderungswunsch                                         | mit DSL                                                                         | Primärer Modellierungsort                                                                         |
| ------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Neue fachliche Eigenschaft                              | `org.modellwerkstatt.objectflow`                                                | `Entity`, `Value Object` oder `DTO`, abhängig von der Bedeutung der Daten                         |
| Neue Geschäftsregel oder Berechnung                     | `org.modellwerkstatt.objectflow`                                                | Fachliches Verhalten in `Entity`, `Value Object` oder `Service`                                   |
| Neues Persistenzmapping                                 | `org.modellwerkstatt.manmap`                                                    | `EntityMapping` innerhalb einer `Persistence Description`                                          |
| Neue Datenbankabfrage oder Speicheroperation            | `org.modellwerkstatt.manmap`                                                    | Methode und gegebenenfalls Mapper innerhalb eines `Repository`                                    |
| Neuer Anwendungsfall oder geänderter Interaktionsablauf | `org.modellwerkstatt.objectflow`                                                | `Command` und dessen Pages                                                                        |
| Neue Darstellung oder Bedienelemente                    | `org.modellwerkstatt.dataux`                                                    | `Page Pane` und darin eingebundene Formulare, Tabellen, Layouts oder andere UI-Komponenten        |
| Neue Anwendung oder geändertes Hauptmenü                | `org.modellwerkstatt.dataux`                                                    | `AppUI Module`                                                                                   |

Fachliche Prüfungen und Berechnungen gehören in das fachliche Modell beziehungsweise in Services. Datenbankabfragen und Speicheroperationen werden in Repositories implementiert. Commands koordinieren den Anwendungsfall, die Session und die zugehörigen Pages. Deren Darstellung wird durch `Page Pane`s und die darin eingebundenen UI-Komponenten beschrieben. Eine Änderung kann daher mehrere Modellierungsorte und DSLs betreffen.

## Laufzeitumgebungen

Die Ausführung richtet sich nach dem modellierten Modultyp: Anwendungen mit Benutzeroberfläche unterstützen drei Laufzeitumgebungen, Batchjobs können automatisiert oder mit Benutzeroberfläche betrieben werden. Testsuiten können in MPS über eine Run-Konfiguration oder standalone mit Java ausgeführt werden.

| Modultyp         | Ausführungsart                                    | Technologie/Laufzeitumgebung                     | Primärer Einsatz                                                       |
| ---------------- | ------------------------------------------------- | ------------------------------------------------ | ---------------------------------------------------------------------- |
| `AppUI Module`    | Desktop-Anwendung                                 | JavaFX / `org.modellwerkstatt.fx8forms`          | Desktop-PCs                                                            |
| `AppUI Module`    | Webanwendung auf Tomcat                           | Vaadin / `org.modellwerkstatt.turkuforms`        | Desktop-PCs                                                            |
| `AppUI Module`    | HTML5-Webanwendung auf Tomcat                     | Pebble Templates / `org.modellwerkstatt.h2forms` | MDE-Geräte, beispielsweise von Zebra oder Datalogic, sowie Smartphones |
| `BatchJob Module` | Automatisierte Ausführung ohne Benutzeroberfläche | Servlet auf Tomcat                               | Hintergrundverarbeitung                                                |
| `BatchJob Module` | Ausführung mit Desktop-Oberfläche                 | JavaFX / `org.modellwerkstatt.fx8forms`          | Interaktive Ausführung auf Desktop-PCs                                 |
| `BatchJob Module` | Ausführung mit Weboberfläche                      | Vaadin / `org.modellwerkstatt.turkuforms`        | Interaktive Ausführung im Browser                                      |
| `OFXTestSuit`    | Testausführung                                    | MPS (Run-Konfiguration) oder standalone mit Java | Ausführen und Prüfen modellierter Testabläufe                          |

`org.modellwerkstatt.turkuforms` ist nicht Teil von MPS und wird erst im finalen Build-Prozess der Anwendung eingebunden; in MPS sind nur `org.modellwerkstatt.fx8forms` und `org.modellwerkstatt.h2forms` verfügbar.

Anwendungsmodelle sind mit wenigen Ausnahmen zwischen `org.modellwerkstatt.fx8forms`, `org.modellwerkstatt.turkuforms` und `org.modellwerkstatt.h2forms` portabel. Bei der Oberflächengestaltung sind die unterschiedlichen Gerätezielgruppen und Bildschirmgrößen zu berücksichtigen: Eine technisch ausführbare Oberfläche ist nicht automatisch für jedes Gerät gleichermaßen geeignet.

Batchjobs können direkt gestartet, zeitgesteuert über Cron ausgeführt oder kontinuierlich mit einer konfigurierten Wartezeit zwischen den Durchläufen betrieben werden. Zusätzlich ist eine Ausführung mit Benutzeroberfläche über `org.modellwerkstatt.fx8forms` oder `org.modellwerkstatt.turkuforms` möglich.

## Gesamtbeispiel: Rechnungsverwaltung

Das Beispiel umfasst die Suche nach Rechnungen, die Bearbeitung einer Rechnung mit ihren Positionen und die Anzeige der Summe aller Rechnungen. Die verwendeten Namen sind beispielhaft.

### Fachliches Modell mit der DSL `org.modellwerkstatt.objectflow`

| Element       | Beispiel                  | Aufgabe                                                                                                                                                       |
| ------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Entity`      | `Rechnung`                | Enthält Rechnungs-ID, Rechnungsnummer, Rechnungsdatum und eine Liste von Rechnungspositionen.                                                                 |
| `Entity`      | `Rechnungsposition`       | Enthält Positionsnummer, Beschreibung, Menge und Einzelpreis.                                                                                                 |
| `Value Object` | `Geldbetrag`              | Fasst Betrag und Währung zusammen.                                                                                                                            |
| `DTO`         | `RechnungInfo`            | Read-only-Projektion für ein Suchergebnis. Enthält die Rechnungs-ID sowie die für die Ergebnisliste benötigten Rechnungsdaten.                                 |
| `DTO`         | `RechnungFilter`          | Enthält Suchkriterien, beispielsweise Rechnungsnummer und Datumsbereich, sowie die Property `results` vom Typ `list<RechnungInfo>`.                           |
| `DTO`         | `RechnungsSummenErgebnis` | Nimmt das Ergebnis der SQL-Aggregation zur Summe aller Rechnungen auf.                                                                                        |
| `Service`     | `RechnungsService`        | Berechnet Positionswerte und Rechnungssumme und prüft fachliche Regeln bei der Bearbeitung.                                                                   |

Für das vereinfachte Beispiel müssen Mengen positiv und Einzelpreise nicht negativ sein. Alle Rechnungen verwenden dieselbe Währung. Die Summe einer Rechnung ergibt sich aus ihren Positionswerten. Steuern und Rundungsregeln werden in diesem Beispiel nicht behandelt.

### Persistenz mit der DSL `org.modellwerkstatt.manmap`

Eine `Persistence Description` enthält die Mappings für `Rechnung` und `Rechnungsposition`. Die Positionstabelle besitzt eine Zuordnung zur jeweiligen Rechnung.

Zwei Repositories kapseln die Datenbankzugriffe. Das `RechnungsRepo` lädt und speichert das Aggregat Rechnung; das `RechnungsLeseRepo` enthält die Abfragen, die nur lesen.

| Repository          | Beispielhafte Methode        | Aufgabe                                                                                                                                                                       |
| ------------------- | ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `RechnungsRepo`     | `checkout(id)`               | Lädt die Rechnung und explizit ihre Positionen zur Bearbeitung. Stellt den vollständigen Rechnungsgraphen zusammen.                                                           |
| `RechnungsRepo`     | `checkin(rechnung)`          | Speichert die bearbeitete Rechnung einschließlich der zugehörigen Änderungen an ihren Positionen.                                                                             |
| `RechnungsLeseRepo` | `sucheRechnungen(filter)`    | Übersetzt die Suchkriterien aus `RechnungFilter` in eine benutzerdefinierte SQL-Abfrage. Ein No-Key-Mapper überführt jede Ergebniszeile in ein read-only `RechnungInfo`-DTO. |
| `RechnungsLeseRepo` | `ladeSummeAllerRechnungen()` | Führt die Aggregation direkt per SQL in der Datenbank aus. Ein No-Key-Mapper überführt das Ergebnis in das read-only DTO `RechnungsSummenErgebnis`.                           |

Die Suche lädt keine `Rechnung`-Entitäten. Die benutzerdefinierte SQL-Abfrage liest nur die für die Ergebnisliste benötigten Daten und bildet jede Zeile auf ein `RechnungInfo`-DTO ab. Diese No-Key-Ergebnisse sind read-only und werden nicht in die Session-Identity-Map integriert. Erst beim Öffnen eines Suchergebnisses wird anhand seiner Rechnungs-ID die zugehörige `Rechnung` einschließlich ihrer Positionen zur Bearbeitung explizit geladen.

Auch für die Summe aller Rechnungen werden keine vollständigen Rechnungsgraphen aufgebaut. Die Datenbank berechnet das Aggregationsergebnis, das anschließend als DTO zur Anzeige bereitsteht. Diese Auswertung umfasst alle Rechnungen und ist unabhängig vom aktuellen Suchfilter.

### Anwendungsfälle mit der DSL `org.modellwerkstatt.objectflow`

| Beispiel-Command                  | Command-Typ       | Aufgabe                                                                                                                       |
| --------------------------------- | ----------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `Rechnungen suchen`               | `SEARCH_CMD`      | Erfasst Suchkriterien und zeigt die als `RechnungInfo`-DTOs geladenen Treffer auf einer zweiten Seite an.                     |
| `Rechnung bearbeiten`             | `GRAPH_OWNER_CMD` | Lädt eine Rechnung anhand ihrer ID, zeigt Kopf und Positionen an und registriert Repository-Methoden zum Speichern als Session-Operationen. |
| `Rechnungskopf bearbeiten`        | `GRAPH_EDIT_CMD`  | Bearbeitet die Kopfdaten innerhalb der bestehenden Session des `GRAPH_OWNER_CMD`.                                              |
| `Rechnungsposition bearbeiten`    | `GRAPH_EDIT_CMD`  | Bearbeitet eine Position innerhalb der bestehenden Session des `GRAPH_OWNER_CMD`.                                             |
| `Summe aller Rechnungen anzeigen` | `SEARCH_CMD`      | Ruft die SQL-Aggregation im `RechnungsLeseRepo` auf und zeigt das Ergebnis an.                                                |

Der ebenfalls verfügbare Typ `GRAPH_OWNER_CMD(modal)` wird in diesem Beispiel nicht benötigt.

#### Rechnungen suchen

Der Command `Rechnungen suchen` startet eine eigene Read-only-Session und besteht aus zwei Pages:

1. **Suchfilter eingeben:** Ein Formular ist an das DTO `RechnungFilter` gebunden. Der Benutzer legt die Suchkriterien fest.
2. **Suchergebnisse anzeigen:** Mit den Kriterien aus dem DTO wird die Methode `sucheRechnungen(filter)` des `RechnungsLeseRepo` aufgerufen. Sie führt benutzerdefiniertes SQL aus und legt die über ein No-Key-Mapper erzeugten `RechnungInfo`-DTOs in der Property `results` des Filter-DTOs ab. Eine Tabelle auf der zweiten Page zeigt diese Liste an.

Bei der Suche werden weder `Rechnung`-Entitäten noch deren Positionen geladen. Die Session des `SEARCH_CMD` kann nicht committed werden. Die Eingabe von Suchkriterien und das Befüllen von `results` im DTO sind davon unabhängig: Diese Daten dienen dem Suchablauf und werden nicht in die Datenbank geschrieben. Auch die `RechnungInfo`-Ergebnisse des No-Key-Mapper sind read-only und nicht Bestandteil der Session-Identity-Map.

Ein Doppelklick auf eine Tabellenzeile startet `Rechnung bearbeiten`. Als Parameter wird die Rechnungs-ID aus dem ausgewählten `RechnungInfo`-DTO übergeben. Bei erfolgreichem Abschluss pusht `Rechnung bearbeiten` die bearbeitete `Rechnung`; der Termination Handler der Suchseite übernimmt die geänderten Werte mit gewöhnlichen Anweisungen aus der Entity in das zugehörige `RechnungInfo`-DTO der Ergebnisliste. Die Suche wird dafür nicht wiederholt.

#### Rechnung und Positionen bearbeiten

Der Command `Rechnung bearbeiten` hat den Typ `GRAPH_OWNER_CMD` und startet eine eigene Session. Er ist dafür verantwortlich, die Daten zur Bearbeitung zu laden (**Checkout**). Dazu ruft er `checkout(id)` des `RechnungsRepo` mit der übergebenen Rechnungs-ID auf. Die Repository-Methode lädt den Rechnungskopf und die zugehörigen Positionen.

Der `GRAPH_OWNER_CMD` zeigt Rechnungskopf und Positionen an, bearbeitet sie aber nicht selbst; sein `Delegate Form` ist `DISABLED`. Zum Bearbeiten öffnet er `Rechnungskopf bearbeiten` und `Rechnungsposition bearbeiten` vom Typ `GRAPH_EDIT_CMD`. Diese Commands arbeiten innerhalb der bestehenden Session des `GRAPH_OWNER_CMD` und eröffnen keine eigene Session. Änderungen werden direkt an den Entities durchgeführt.

Der `RechnungsService` übernimmt fachliche Prüfungen und Berechnungen. Der `GRAPH_OWNER_CMD` registriert die zum Speichern benötigten Repository-Methoden (**Check-in**) als **Session-Operationen**. Im Beispiel dient dazu `checkin(rechnung)`.

Beim vorgesehenen Abschluss des `GRAPH_OWNER_CMD` wird eine Datenbanktransaktion gestartet. Die registrierten Session-Operationen werden ausgeführt und die Transaktion wird committed. Die Session begleitet damit die Bearbeitung; die Transaktion zum Speichern wird erst beim Abschluss ausgeführt.

#### Summe aller Rechnungen anzeigen

Der Command `Summe aller Rechnungen anzeigen` hat den Typ `SEARCH_CMD` und verwendet eine eigene Read-only-Session. Er ruft `ladeSummeAllerRechnungen()` im `RechnungsLeseRepo` auf.

Die Repository-Methode führt eine aggregierende SQL-Abfrage direkt auf der Datenbank aus. Ein No-Key-Mapper überführt deren Ergebnis in das read-only DTO `RechnungsSummenErgebnis`, das nicht in die Session-Identity-Map integriert wird. Der Command stellt dieses DTO für die Anzeige bereit. Ein Laden und anschließendes Durchlaufen aller Rechnungsentitäten in der Anwendung ist dafür nicht erforderlich.

### Benutzeroberfläche mit der DSL `org.modellwerkstatt.dataux`

Eine **Page** beschreibt eine Seite im Ablauf eines Commands. Das zugehörige **`Page Pane`** bildet ihr Gegenstück in der Benutzeroberfläche und nimmt deren UI-Inhalte auf. Formulare, Tabellen, Layouts und andere UI-Komponenten müssen jeweils innerhalb eines `Page Pane`s eingebunden sein, gegebenenfalls über darin enthaltene Layouts. `Page Pane`s können wiederverwendet werden.

| Element                                 | Inhalt                                                                                                                                                                     |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AppUI Module`                           | Einstieg in die Rechnungsverwaltung mit Menüeinträgen für `Rechnungen suchen` und `Summe aller Rechnungen anzeigen`.                                                       |
| `Page Pane` für die Suchfilter-Page      | Enthält ein `Delegate Form`, dessen Eingabefelder an die Suchkriterien des DTOs `RechnungFilter` gebunden sind.                                                             |
| `Page Pane` für die Suchergebnis-Page    | Enthält eine `Table`, die die `RechnungInfo`-DTOs aus `RechnungFilter.results` zeigt. Ein Doppelklick startet `Rechnung bearbeiten` mit der Rechnungs-ID aus dem DTO.    |
| `Page Pane` für die Rechnungsbearbeitung | Enthält ein `Delegate Form` (`DISABLED`) für den Rechnungskopf und eine `Table` für die geladenen Rechnungspositionen; die Aktionen öffnen `Rechnungskopf bearbeiten` und `Rechnungsposition bearbeiten`. Ein `Grid Layout` oder `Tab Layout` strukturiert diese Komponenten. |
| `Page Pane` für die Kopfbearbeitung     | Enthält ein `Delegate Form` zur Bearbeitung des Rechnungskopfs im Command `Rechnungskopf bearbeiten`.                                                                      |
| `Page Pane` für die Positionsbearbeitung | Enthält ein `Delegate Form` zur Bearbeitung einer einzelnen Rechnungsposition im Command `Rechnungsposition bearbeiten`.                                                    |
| `Page Pane` für die Summenanzeige        | Enthält ein `Delegate Form` zur Anzeige des DTOs `RechnungsSummenErgebnis`.                                                                                                 |

Die Seitenfolge wird im jeweiligen Command beschrieben. Die zugeordneten `Page Pane`s und ihre enthaltenen UI-Komponenten legen Darstellung, Datenbindungen und angebotene Interaktionen fest.

### Fachliche Prüfung und Qualitätssicherung

Eine `OFXTestSuit` kann beispielsweise folgende Fälle abdecken:

- Zwei Positionen mit `2 × 50 EUR` und `1 × 30 EUR` ergeben eine Rechnungssumme von `130 EUR`.
- Eine Position mit Menge `0` wird fachlich abgelehnt.
- Die Rechnungssuche liefert die im Test angelegten Rechnungen als `RechnungInfo`-DTOs.

### ExpensiveCode und CheapCode im Beispiel

Rechnungsstruktur, Berechnungen, fachliche Prüfungen und Aggregationslogik bilden den sorgfältig abzusichernden fachlichen Kern (**ExpensiveCode**).

Spaltenanordnung, Formularlayouts, Menügestaltung und die Benutzerinteraktion mit diesem Modell gehören zum **CheapCode**. Sie lassen sich beim Ausprobieren unmittelbar beurteilen und durch kurze Feedbackzyklen verbessern. Darstellungs- und Interaktionsanteile eines Commands sind typischerweise CheapCode; fachlich relevante Ablaufregeln im Command können aber auch ExpensiveCode sein.

## Von der Modellierung zur Ausführung

1. **Solutions anlegen:** Jede Solution hat eine Modulabhängigkeit auf `JDK`; ihre Modelle verwenden das DevKit `org.modellwerkstatt.MoWareWerkbank`. Weitere Abhängigkeiten, etwa auf Laufzeitmodule wie `org.modellwerkstatt.objectflow.runtime` oder auf Java-Bibliotheken wie einen JDBC-Treiber, werden nur ergänzt, wenn Inhalte daraus direkt verwendet werden.

2. **Modellieren und versionieren:** Die Anwendung wird mit den DSLs in MPS modelliert und mit Git versioniert. MPS speichert die Modelle als XML-Dateien. Diese enthalten strukturierte Modelle mit Referenzen und Identitäten; ein rein textueller Merge kann deren Konsistenz verletzen. Für die Versionsverwaltung werden deshalb die Git-Unterstützung von MPS und der MPS-Merge-Driver verwendet. Modellkonflikte werden mit den modellbewussten Werkzeugen von MPS aufgelöst.

3. **Datenbankschema erstellen:** Das Datenbankschema erstellt der Entwickler in MPS aus den `EntityMapping`s der Persistence Descriptions.

4. **Laufzeitkonfiguration auswählen:** In der `OFXConfig` wird über **AppFactories** festgelegt, welche Laufzeitumgebung tatsächlich verwendet wird. Ein Projekt enthält häufig mehrere Konfigurationen.

5. **Vollständig neu bauen:** Vor jedem Ant-Build wird die gesamte Anwendung in MPS (alle dem Projekt zugeordneten MPS-Solutions) vollständig neu gebaut (**Rebuild**). Ein inkrementeller Build reicht nicht aus. Dabei wird insbesondere der Java-Code aus den Modellen neu generiert. Erst nach einem erfolgreichen Rebuild wird mit dem nächsten Schritt fortgefahren.

6. **Mit Ant bauen und bereitstellen:** Anschließend wird Ant auf der Konsole ausgeführt. Die projektspezifische Builddatei und die gewählten Targets bestimmen den Build und die Bereitstellung. Sie müssen zur ausgewählten Laufzeitkonfiguration passen.

7. **Ausführen und prüfen:** Die Anwendung wird in der durch die `OFXConfig` festgelegten Laufzeitumgebung gestartet und ihre Funktionsfähigkeit geprüft.

## Grundprinzipien für die Anwendungsentwicklung

Für die Entwicklung von Anwendungen gelten folgende Grundprinzipien:

1. **Das fachliche Modell ist der Ausgangspunkt.**
   Persistenter fachlicher Zustand wird mit Entities und Value Objects modelliert. Fachliche Regeln, Berechnungen und Zustandsübergänge gehören an die fachlichen Datenstrukturen oder in geeignete Services. DTOs dienen dagegen anwendungsfallbezogenen Daten, Projektionen, Suchen und Darstellungen. Fachliche Regeln sollen nicht in Benutzeroberflächen, Persistenzcode oder technische Laufzeitkomponenten verlagert werden.

2. **Benötigte Objektgraphen werden bewusst und explizit geladen.**
   Eine Beziehung zwischen fachlichen Objekten bedeutet nicht automatisch, dass die referenzierten Daten geladen sind. Automatisches Lazy Loading ist nicht möglich. Repository-Methoden müssen deshalb den für einen Anwendungsfall benötigten Objektgraphen gezielt aufbauen. Welche Daten geladen werden, ist Teil des Entwurfs des Anwendungsfalls.

3. **Persistenz ist ebenfalls explizit.**
   Eine fachliche Beziehung oder ein Mapping bedeutet nicht automatisch, dass ein vollständiger Objektgraph kaskadierend gespeichert wird. Check-in- und Delete-Operationen müssen ausdrücklich festlegen, welche Bestandteile gespeichert oder gelöscht werden. Fachmodell, Mapping und tatsächlich ausgeführte Speicheroperation sind getrennte Aspekte.

4. **Read-only-Zugriff und Bearbeitung werden bewusst unterschieden.**
   Daten für Suchen, Übersichten und Auswertungen sollen ohne Änderungsabsicht geladen werden. Zweckgebundene Lesemodelle werden vorzugsweise als DTOs modelliert. Soll eine Entity verändert werden, muss sie in einem dafür vorgesehenen bearbeitbaren Kontext geladen beziehungsweise ausgecheckt werden. Read-only-Projektionen dürfen nicht allein deshalb wie bearbeitbare Domänenobjekte behandelt werden, weil sie dieselbe Struktur wie eine Entity besitzen.

5. **Session und Transaktion gehören zum Anwendungsablauf, nicht zu einzelnen Repository-Aufrufen.**
   Repository-Methoden führen Datenzugriffsoperationen aus, bestimmen aber nicht selbst die fachliche Transaktionsgrenze. Der Session Owner – typischerweise ein `GRAPH_OWNER_CMD` – koordiniert Session und Transaktion. Speicher- und Löschoperationen werden als Session-Operationen registriert und erst beim erfolgreichen Abschluss ausgeführt und committed; bei einem Abbruch werden sie nicht ausgeführt.

   Das gilt auch für datenbankveränderndes Custom SQL. `UPDATE`-, `DELETE`- oder andere `STATEMENT`-Operationen dürfen nicht unmittelbar ausgeführt werden, wenn ihre Wirkung zum erfolgreichen Abschluss des Anwendungsfalls gehört, sondern müssen in den Session-Operations-Ablauf eingebunden werden. Andernfalls könnten Änderungen bereits wirksam sein, obwohl der Benutzer den Graph Owner anschließend noch mit `ESC` abbricht.

6. **Prüfen und Verändern sind möglichst klar zu trennen.**
   Fachliche Voraussetzungen und Precondition-Prüfungen sollen grundsätzlich erfolgen, bevor ein Objektgraph verändert wird. Dadurch hinterlässt ein abgebrochener Vorgang möglichst keinen teilweise veränderten Zustand. Abweichungen davon müssen eine bewusste fachliche Bedeutung haben und dürfen nicht zufällig aus der Reihenfolge technischer Operationen entstehen.

7. **Die Benutzeroberfläche bleibt möglichst „CheapCode“.**
   DataUX beschreibt Bindung, Darstellung, Layout und Interaktionsmöglichkeiten (CheapCode, siehe [Ziele der Werkbank](#ziele-der-werkbank)). Fachliche Entscheidungen und schwer überprüfbare Geschäftsregeln gehören nicht in die Oberfläche. Dadurch können Oberflächen in kurzen Feedbackzyklen verändert und erprobt werden, ohne das fachliche Modell unnötig zu beeinflussen.

8. **Fachliches Wissen soll unabhängig von der technischen Laufzeit bleiben.**
    Modelle sollen möglichst keine unnötigen Abhängigkeiten von einem konkreten UI-Framework oder einer bestimmten Ausführungsplattform enthalten. Plattformspezifische Modellierung ist nur dort sinnvoll, wo sich die fachliche oder ergonomische Anforderung tatsächlich unterscheidet.

9. **Anwendungsfälle müssen überprüfbar bleiben.**
    Fachliche Regeln und Abläufe sollen so modelliert werden, dass sie durch Beispiele und Tests nachvollzogen werden können. Besonders sorgfältig zu prüfen sind Änderungen an fachlichen Datenstrukturen und Geschäftsregeln, da Fehler dort häufig nicht allein durch technische Tests oder das Ausprobieren der Oberfläche erkennbar werden. Die zugehörige Dokumentation wird möglichst direkt bei den beschriebenen Modellelementen gepflegt.

## Weiterführende Dokumentation

Die Detaildokumentationen beschreiben Konzepte, Möglichkeiten, Einschränkungen, Regeln, Beispiele und Best Practices der jeweiligen DSL.

### Detaildokumentationen zu DSLs

| DSL | Dokumentation | 
| --- | --- |
| `org.modellwerkstatt.manmap` | [manmap.md](manmap.md) |
| `org.modellwerkstatt.objectflow` | [objectflow.md](objectflow.md) |
| `org.modellwerkstatt.dataux` | [dataux.md](dataux.md) |

### Verbindliche Konventionen

Die Dokumentation beschreibt, was die Sprachen können. Wie eine Anwendung das verwenden muss, legen die verbindlichen Konventionen im Verzeichnis `conventions/` fest. 

## Stand der Dokumentation

Diese Dokumentation beschreibt die **modellwerkstatt MoWare-Werkbank, Stand Oktober 2026**, auf Basis von **JetBrains MPS 2026.1**.
