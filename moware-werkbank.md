# modellwerkstatt MoWare-Werkbank: drei DSLs zur Modellierung von Geschäftsanwendungen

## Zweck und Geltungsbereich

Dieses Dokument ist die architektonische Einstiegsseite zur **modellwerkstatt MoWare-Werkbank**. Es erklärt die Zuständigkeiten und das Zusammenspiel der drei DSLs, die gemeinsamen Grundprinzipien sowie den Weg vom fachlichen Modell zur laufenden Anwendung.

Die Beispiele sind fachliche Skizzen und keine ausführbare DSL-Syntax. Konkrete Konzepte, Eigenschaften, Einschränkungen und Modellierungsmuster werden in den jeweiligen DSL-Dokumentationen beschrieben. Bei Abweichungen zwischen Dokumentation und den geladenen MPS-Sprachen sind die Sprachdefinitionen und ihre Prüfregeln die technische Quelle der Wahrheit. Ein Agent soll unbekannte Syntax oder Regeln nicht ableiten oder erfinden, sondern die Modelle mit MPS-werkzeugen untersuchen.


## Modellierungssprachen und Laufzeitumgebungen

Die **modellwerkstatt MoWare-Werkbank** basiert auf JetBrains MPS und umfasst drei eng integrierte domänenspezifische Sprachen (DSLs) zur Erstellung von Geschäftsanwendungen. Sie decken Persistenz, Geschäftslogik und Benutzeroberflächen ab. Die Architektur orientiert sich stark an **Domain-Driven Design (DDD)** und übernimmt ausgewählte Konzepte: Entities und Value Objects beschreiben fachliche Daten, Repositories ermöglichen deren Laden und Speichern, und Services bündeln Geschäftslogik.

**manmap** (`org.modellwerkstatt.manmap`) bildet die Persistenzschicht der Anwendung. Die Sprache definiert die Zuordnung zwischen relationalen Datenbanktabellen und Entitäten und stellt Operationen zum Laden, Speichern und Löschen bereit. Diese bilden die Grundlage für den Datenzugriff über Repositories. Komplexe Objektstrukturen werden explizit geladen und zusammengestellt; auf automatisches Lazy Loading wird bewusst verzichtet. Darüber hinaus unterstützt manmap die Arbeit mit Lesemodellen (Read Models) und Tabellenmodellen (Table Models): Komplexe SQL-Abfragen lassen sich formulieren und ihre Ergebnismengen über spezialisierte Mapper in DTOs (Data Transfer Objects) überführen.

**objectflow** (`org.modellwerkstatt.objectflow`) dient der Modellierung von Service-Komponenten und Geschäftslogik. Die Sprache umfasst fachliche Datenstrukturen wie Entities und Value Objects sowie Commands zur Beschreibung von Aktionen und Anwendungsabläufen. Darüber hinaus unterstützt objectflow die Modellierung von Testabläufen in Testsuiten sowie die Definition von Rollen und Berechtigungen.

**dataux** (`org.modellwerkstatt.dataux`) dient der Modellierung von Benutzeroberflächen, Applikationen und BatchJobs. Tabellen und Formulare werden durch ihre Spalten, Felder, Formatierungen und Datenbindungen beschrieben; Layouts strukturieren die Darstellung und ermöglichen die Zusammenstellung komplexerer Oberflächen. Applikationen dienen für Endanwender als Einstiegspunkt und verfügen über das Hauptmenü. Für die automatisierte Verarbeitung lassen sich BatchJobs modellieren, die direkt als Applikation gestartet, zeitgesteuert über Cron ausgeführt oder kontinuierlich mit einer konfigurierten Wartezeit zwischen den Durchläufen betrieben werden können.

Aus den in MPS modellierten Anwendungen wird Java-Code generiert. Für die Ausführung stehen drei Laufzeitumgebungen zur Verfügung: `org.modellwerkstatt.fx8forms` für JavaFX-Desktop-Anwendungen, `org.modellwerkstatt.turkuforms` für Vaadin-Webanwendungen auf Tomcat und `org.modellwerkstatt.h2forms` für HTML5-Webanwendungen mit Pebble Templates auf Tomcat. Während fx8forms und turkuforms primär auf Desktop-PCs ausgerichtet sind, richtet sich h2forms an mobile Datenerfassungsgeräte und Smartphones. Die Applikationsmodelle sind mit wenigen Ausnahmen zwischen diesen Laufzeitumgebungen portabel; bei der Oberflächengestaltung sind insbesondere die unterschiedlichen Bildschirmgrößen zu berücksichtigen.


## Grundprinzipien und Ziele

Die **modellwerkstatt MoWare-Werkbank** stellt die fachliche Gestaltung von Geschäftsanwendungen in den Mittelpunkt: Welche Daten werden benötigt, wie hängen sie zusammen, welche Geschäftsregeln gelten und wie arbeiten Benutzer mit ihnen? Die Modellsprachen bieten dafür passende Ausdrucksmittel. Generatoren und Laufzeitumgebungen übernehmen wiederkehrende technische Aufgaben und Infrastruktur-Code. Dadurch konzentriert sich die Anwendungsentwicklung auf fachliche Datenstrukturen, Geschäftslogik und Benutzerinteraktionen.

**Fachliche Modellierung.** Die Architektur orientiert sich an ausgewählten Konzepten des Domain-Driven Design. Entities und Value Objects beschreiben fachliche Daten, Repositories deren Laden und Speichern, Services die Geschäftslogik. Die Entwicklung geeigneter Datenstrukturen und korrekter Geschäftsregeln bleibt die zentrale Entwurfsaufgabe.

**Ausdrucksstarke Geschäftslogik.** Berechnungen, Prüfungen und Änderungen werden unmittelbar an den fachlichen Datenstrukturen formuliert. Java-Ausdrücke und Mengenoperationen unterstützen diese Arbeit. Technische Details der verwendeten UI-Frameworks und Laufzeitumgebungen werden weitgehend durch die Werkzeugkette gekapselt.

**Einheitliche Architektur und klare Zuständigkeiten.** Die Sprachkonzepte geben vor, wo Datenzugriff, Geschäftslogik und Benutzeroberflächen beschrieben werden. Diese gemeinsame Struktur erleichtert die Orientierung, die Wiederverwendung und die Zusammenarbeit. Fachliche Begriffe bleiben im Modell sichtbar und unterstützen die Abstimmung zwischen Entwicklern und Fachverantwortlichen.

**Schrittweise Entwicklung und überprüfbare Anforderungen.** Anwendungen werden anhand konkreter Anwendungsfälle modelliert und schrittweise verfeinert. Beispiele, Testdaten und Testabläufe helfen, fachliche Annahmen früh zu prüfen und Änderungen abzusichern. Die zugehörige Dokumentation wird möglichst direkt bei den beschriebenen Modellelementen gepflegt.

**ExpensiveCode und CheapCode.** MoWare unterscheidet zwischen aufwendig erarbeitetem Fachwissen (*ExpensiveCode*) und leichter überprüfbaren und anpassbaren Teilen einer Anwendung (*CheapCode*). Zum ExpensiveCode gehören insbesondere fachliche Datenstrukturen, Geschäftsregeln und Verarbeitungslogik. Ihre Entwicklung erfordert Domänenwissen und sorgfältige Abstimmung; Fehler sind häufig erst durch eine fachliche Prüfung erkennbar. CheapCode umfasst dagegen UI-Beschreibungen, Menüs und die Gestaltung der Interaktion mit dem fachlichen Modell. Fehler in diesen Bereichen fallen beim Ausprobieren meist schnell auf und lassen sich gezielt korrigieren. Das fachliche Modell verlangt besondere Sorgfalt, während Oberflächen und Bedienabläufe durch kurze Feedbackzyklen schrittweise verbessert werden können.

**Langfristige Wartbarkeit und technische Flexibilität.** Das fachliche Wissen wird in den Modellen festgehalten. Generatoren und Laufzeitumgebungen bestimmen dessen technische Umsetzung. Diese Trennung ermöglicht es, fachliche Anforderungen und technische Infrastruktur weitgehend unabhängig weiterzuentwickeln. Ziel ist, bestehende Modelle langfristig zu nutzen und Anpassungen an Frameworks oder Ausführungsplattformen möglichst zentral umzusetzen.


## Zentrale Konzepte der MoWare-Werkbank

Der gesamte Stack orientiert sich stark an Domain-Driven Design (DDD), übernimmt aber nicht sämtliche DDD-Konzepte. Diese Übersicht erfasst die zentralen Konzepte der drei MoWare-Sprachen. Sie beschreibt die erkennbare Verantwortung der Konzepte, ohne zusätzliche DDD-Regeln für die DSLs festzulegen.

### Einordnung entlang der fachlichen Architektur

| Schicht                            | Konzept                                                                         | DSL                              |
| ---------------------------------- | ------------------------------------------------------------------------------- | -------------------------------- |
| Fachliches Modell                  | `Entity`, `ValueObject`, `DTO`                                                  | `org.modellwerkstatt.objectflow` |
| Geschäftslogik und Anwendungsfälle | `Service`, `Command`                                                            | `org.modellwerkstatt.objectflow` |
| Persistenz                         | `PersistenceDescription`, `Repository`                                          | `org.modellwerkstatt.manmap`     |
| Benutzeroberfläche                 | `PagePane`, `Table`, `DelegateForm`, `GridLayout`, `TabLayout`, `CustomElement` | `org.modellwerkstatt.dataux`     |
| Ausführbare Module                 | `AppUiModule`, `BatchJobModule`                                                 | `org.modellwerkstatt.dataux`     |
| Querschnitt                        | `OFXConfig`, `OFXTestSuit`, `RolesAndPermissions`, `StaticRessources`           | `org.modellwerkstatt.objectflow` |

### `org.modellwerkstatt.manmap` im Detail

`org.modellwerkstatt.manmap` bildet die Persistenzschicht und verbindet fachliche Objekte mit der relationalen Datenbank (Oracle oder MySQL). Neben der Persistierung von Entitäten unterstützt die Sprache benutzerdefinierte SQL-Abfragen und das Überführen ihrer Ergebnismengen in Datencontainer.

| Kurzbezeichnung          | FQ-Name                                                       | Beschreibung/Aufgabe                                                                                                                                                                                                                                                                                   |
| ------------------------ | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `PersistenceDescription` | `org.modellwerkstatt.manmap.structure.PersistenceDescription` | Bündelt die Persistenzabbildungen eines Modells. Die enthaltenen Entity-Mappings ordnen fachliche Objekte und ihre Eigenschaften Tabellen, Spalten und Beziehungen zu.                                                                                                                                  |
| `Repository`             | `org.modellwerkstatt.manmap.structure.Repository`             | Kapselt den Datenbankzugriff. Enthält Methoden zum Abfragen, Laden, Zusammensetzen, Speichern und Löschen fachlicher Objekte. Unterstützt außerdem benutzerdefinierte SQL-Abfragen und spezialisierte Mapper, die Ergebnismengen in Objekte, insbesondere DTOs, überführen.                                 |

### `org.modellwerkstatt.objectflow` im Detail

`org.modellwerkstatt.objectflow` beschreibt das fachliche Modell, Service-Komponenten, Anwendungsoperationen und Geschäftsabläufe. Ergänzend stellt die Sprache Konzepte für Konfiguration, Tests, Berechtigungen und gemeinsame Ressourcen bereit.

| Kurzbezeichnung       | FQ-Name                                                        | Beschreibung/Aufgabe                                                                                                                                                                                                                                                           |
| --------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Entity`              | `org.modellwerkstatt.objectflow.structure.Entity`              | Beschreibt ein fachliches Objekt mit eigener Identität und Lebenszyklus. Trägt fachliche Eigenschaften und Verhalten und ist typischerweise persistent.                                                                                                                        |
| `ValueObject`         | `org.modellwerkstatt.objectflow.structure.ValueObject`         | Beschreibt einen fachlichen Wert ohne eigene Identität. Seine Gleichheit kann über ausgewählte Eigenschaften definiert werden.                                                                                                                                                 |
| `DTO`                 | `org.modellwerkstatt.objectflow.structure.DTO`                 | Definiert einen Datencontainer für die Benutzeroberfläche oder die Ergebnisse von Datenbankabfragen. Kann durch Mapper aus Result-Sets befüllt werden, ohne selbst ein persistentes Domänenobjekt zu sein.                                                                     |
| `Service`             | `org.modellwerkstatt.objectflow.structure.Service`             | Bündelt fachliche oder anwendungsbezogene Operationen, die nicht sinnvoll einer einzelnen Entity oder einem Value Object zugeordnet werden. Erlaubt Zugriff auf Repositories und andere Infrastrukturkomponenten.                                                             |
| `Command`             | `org.modellwerkstatt.objectflow.structure.Command`             | Modelliert einen Anwendungsfall beziehungsweise eine Benutzeraktion. Koordiniert Parameter, Zustandsvariablen, Seiten sowie Initialisierung und Abschluss bei Bestätigung oder Abbruch. Steuert Session-Logik.                                                                 |
| `OFXConfig`           | `org.modellwerkstatt.objectflow.structure.OFXConfig`           | Definiert die zentrale Konfiguration der Anwendungskomponenten und ihrer Abhängigkeiten. Ist konzeptionell mit einer XML-basierten Spring-Bean-Konfiguration vergleichbar: Komponenten werden konfiguriert und ihre Abhängigkeiten miteinander verdrahtet.                     |
| `OFXTestSuit`         | `org.modellwerkstatt.objectflow.structure.OFXTestSuit`         | Definiert eine eigenständig ausführbare Testsuite mit konfigurierten Komponenten, Start-/Ende-Logik und Testinhalten.                                                                                                                                                          |
| `RolesAndPermissions` | `org.modellwerkstatt.objectflow.structure.RolesAndPermissions` | Beschreibt das Berechtigungsmodell mit Rollen, Geltungsbereichen und Identitäten. Dient als zentrale Grundlage für Zugriffskontrollen.                                                                                                                                         |
| `StaticRessources`    | `org.modellwerkstatt.objectflow.structure.StaticRessources`    | Bündelt wiederverwendbare, plattformbezogene Ressourcen wie Bezeichnungen und Farben. Ressourcensätze können aufeinander aufbauen.                                                                                                                                             |

### `org.modellwerkstatt.dataux` im Detail

`org.modellwerkstatt.dataux` beschreibt Benutzeroberflächen, ausführbare Anwendungen und Batch-Verarbeitung.

| Kurzbezeichnung  | FQ-Name                                               | Beschreibung/Aufgabe                                                                                                                                                                                              |
| ---------------- | ----------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AppUiModule`    | `org.modellwerkstatt.dataux.structure.AppUiModule`    | Definiert eine ausführbare Anwendung mit Benutzeroberfläche. Bündelt Konfiguration, Authentifizierung, Haupt- und Zusatzmenüs sowie Kacheln.                                                                       |
| `BatchJobModule` | `org.modellwerkstatt.dataux.structure.BatchJobModule` | Definiert einen automatisiert ausführbaren BatchJob. Bündelt Konfiguration, Fehlerstrategie und Producer-Consumer-Verarbeitung; Betriebsart und Zeitsteuerung werden über Optionen festgelegt.                      |
| `PagePane`       | `org.modellwerkstatt.dataux.structure.PagePane`       | Kapselt den Inhalt einer Anwendungsseite als wiederverwendbares UI-Element und kann seitenspezifische Optionen und Menüeinträge bereitstellen.                                                                     |
| `Table`          | `org.modellwerkstatt.dataux.structure.Table`          | Beschreibt eine tabellarische Darstellung gebundener Daten. Delegates, Optionen und Menüeinträge bestimmen Spalten, Darstellung und Interaktionen.                                                                |
| `DelegateForm`   | `org.modellwerkstatt.dataux.structure.DelegateForm`   | Beschreibt ein an ein fachliches Objekt oder eine Eigenschaft gebundenes Formular, dessen Felder aus Delegates zusammengesetzt werden.                                                                            |
| `GridLayout`     | `org.modellwerkstatt.dataux.structure.GridLayout`     | Ordnet UI-Elemente in Zeilen und Spalten an. Gewichtungen steuern die Größenverteilung im Raster.                                                                                                                  |
| `TabLayout`      | `org.modellwerkstatt.dataux.structure.TabLayout`      | Strukturiert eine Oberfläche in mehrere Registerkarten und bündelt deren jeweilige Inhalte.                                                                                                                       |
| `CustomElement`  | `org.modellwerkstatt.dataux.structure.CustomElement`  | Deklariert ein projektspezifisches UI-Element mit eigener Implementierungsklasse, optionaler Datenbindung, Delegates und Menüaktionen.                                                                             |


## Zusammenspiel der DSLs

Eine typische Geschäftsanwendung verbindet die drei Sprachen entlang eines durchgängigen Daten- und Kontrollflusses:

```text
objectflow
Entity / ValueObject / DTO / Service / Command
        │
        ├── manmap
        │   Mapping / Repository / SQL / DTO-Mapping
        │
        └── dataux
            PagePane / Form / Table / Layout / Interaktion
                    │
                    ▼
             AppUiModule / BatchJobModule
                    │
                    ▼
                 OFXConfig
                    │
                    ▼
        fx8forms / turkuforms / h2forms
```

- **objectflow** definiert die fachlichen Daten, Regeln und Anwendungsfälle.
- **manmap** verbindet Entities und DTOs mit der relationalen Persistenz und stellt den Datenzugriff über Repositories bereit.
- **dataux** projiziert Commands und deren Daten in Seiten, Formulare, Tabellen und ausführbare Module.


### Wo gehört eine Änderung hin?

| Änderungswunsch                                         | mit DSL                                                                         | Primärer Modellierungsort                                                                         |
| ------------------------------------------------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Neue fachliche Eigenschaft                              | `org.modellwerkstatt.objectflow`                                                | `Entity`, `ValueObject` oder `DTO`, abhängig von der Bedeutung der Daten                          |
| Neue Geschäftsregel oder Berechnung                     | `org.modellwerkstatt.objectflow`                                                | Fachliches Verhalten in `Entity`, `ValueObject` oder `Service`                                    |
| Neues Persistenzmapping                                 | `org.modellwerkstatt.manmap`                                                    | Entity-Mapping innerhalb einer `PersistenceDescription`                                           |
| Neue Datenbankabfrage oder Speicheroperation            | `org.modellwerkstatt.manmap`                                                    | Methode und gegebenenfalls Mapper innerhalb eines `Repository`                                    |
| Neuer Anwendungsfall oder geänderter Interaktionsablauf | `org.modellwerkstatt.objectflow`                                                | `Command` und dessen Pages                                                                        |
| Neue Darstellung oder Bedienelemente                    | `org.modellwerkstatt.dataux`                                                    | `PagePane` und darin eingebundene Formulare, Tabellen, Layouts oder andere UI-Komponenten         |
| Neue Anwendung oder geändertes Hauptmenü                | `org.modellwerkstatt.dataux`                                                    | `AppUiModule`                                                                                     |

Fachliche Prüfungen und Berechnungen gehören in das fachliche Modell beziehungsweise in Services. Datenbankabfragen und Speicheroperationen werden in Repositories implementiert. Commands koordinieren den Anwendungsfall, die Session und die zugehörigen Pages. Deren Darstellung wird durch `PagePane`s und die darin eingebundenen UI-Komponenten beschrieben. Eine Änderung kann daher mehrere Modellierungsorte und DSLs betreffen.

## Laufzeitumgebungen

Die Ausführung richtet sich nach dem modellierten Modultyp: Anwendungen mit Benutzeroberfläche unterstützen drei Laufzeitumgebungen, BatchJobs können automatisiert oder mit Benutzeroberfläche betrieben werden. Testsuiten werden in der MPS-Konsole ausgeführt.

| Modultyp         | Ausführungsart                                    | Technologie/Laufzeitumgebung                    | Primärer Einsatz                                                       |
| ---------------- | ------------------------------------------------- | ----------------------------------------------- | ---------------------------------------------------------------------- |
| `AppUiModule`    | Desktop-Anwendung                                 | JavaFX / `org.modellwerkstatt.fx8forms`          | Desktop-PCs                                                            |
| `AppUiModule`    | Webanwendung auf Tomcat                           | Vaadin / `org.modellwerkstatt.turkuforms`        | Desktop-PCs                                                            |
| `AppUiModule`    | HTML5-Webanwendung auf Tomcat                     | Pebble Templates / `org.modellwerkstatt.h2forms` | MDE-Geräte, beispielsweise von Zebra oder Datalogic, sowie Smartphones |
| `BatchJobModule` | Automatisierte Ausführung ohne Benutzeroberfläche | Servlet auf Tomcat                               | Hintergrundverarbeitung                                                |
| `BatchJobModule` | Ausführung mit Desktop-Oberfläche                 | JavaFX / `org.modellwerkstatt.fx8forms`          | Interaktive Ausführung auf Desktop-PCs                                 |
| `BatchJobModule` | Ausführung mit Weboberfläche                      | Vaadin / `org.modellwerkstatt.turkuforms`        | Interaktive Ausführung im Browser                                      |
| `OFXTestSuit`    | Testausführung                                    | MPS-Konsole                                      | Ausführen und Prüfen modellierter Testabläufe                          |

Applikationsmodelle sind mit wenigen Ausnahmen zwischen `org.modellwerkstatt.fx8forms`, `org.modellwerkstatt.turkuforms` und `org.modellwerkstatt.h2forms` portabel. Bei der Oberflächengestaltung sind die unterschiedlichen Gerätezielgruppen und Bildschirmgrößen zu berücksichtigen: Eine technisch ausführbare Oberfläche ist nicht automatisch für jedes Gerät gleichermaßen geeignet.

BatchJobs können direkt gestartet, zeitgesteuert über Cron ausgeführt oder kontinuierlich mit einer konfigurierten Wartezeit zwischen den Durchläufen betrieben werden. Zusätzlich ist eine Ausführung mit Benutzeroberfläche über `org.modellwerkstatt.fx8forms` oder `org.modellwerkstatt.turkuforms` möglich.


## Gesamtbeispiel: Rechnungsverwaltung

Das Beispiel umfasst die Suche nach Rechnungen, die Bearbeitung einer Rechnung mit ihren Positionen und die Anzeige der Summe aller Rechnungen. Die verwendeten Namen sind beispielhaft; die Beschreibung ist eine fachliche Skizze, keine ausführbare DSL-Syntax.

### Fachliches Modell mit der DSL `org.modellwerkstatt.objectflow`

| Element       | Beispiel                  | Aufgabe                                                                                                                                                       |
| ------------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Entity`      | `Rechnung`                | Enthält Rechnungs-ID, Rechnungsnummer, Rechnungsdatum und eine Liste von Rechnungspositionen.                                                                 |
| `Entity`      | `Rechnungsposition`       | Enthält Positionsnummer, Beschreibung, Menge und Einzelpreis.                                                                                                 |
| `ValueObject` | `Geldbetrag`              | Fasst Betrag und Währung zusammen.                                                                                                                            |
| `DTO`         | `RechnungInfo`            | Read-only-Projektion für ein Suchergebnis. Enthält die Rechnungs-ID sowie die für die Ergebnisliste benötigten Rechnungsdaten.                                 |
| `DTO`         | `RechnungFilter`          | Enthält Suchkriterien, beispielsweise Rechnungsnummer und Datumsbereich, sowie die Property `results` vom Typ `list<RechnungInfo>`.                           |
| `DTO`         | `RechnungsSummenErgebnis` | Nimmt das Ergebnis der SQL-Aggregation zur Summe aller Rechnungen auf.                                                                                        |
| `Service`     | `RechnungsService`        | Berechnet Positionswerte und Rechnungssumme und prüft fachliche Regeln bei der Bearbeitung.                                                                   |

Für das vereinfachte Beispiel müssen Mengen positiv und Einzelpreise nicht negativ sein. Alle Rechnungen verwenden dieselbe Währung. Die Summe einer Rechnung ergibt sich aus ihren Positionswerten. Steuern und Rundungsregeln werden in diesem Beispiel nicht behandelt.

### Persistenz mit der DSL `org.modellwerkstatt.manmap`

Eine `PersistenceDescription` enthält die Mappings für `Rechnung` und `Rechnungsposition`. Die Positionstabelle besitzt eine Zuordnung zur jeweiligen Rechnung.

Das `RechnungsRepository` kapselt die Datenbankzugriffe:

| Beispielhafte Repository-Methode | Aufgabe                                                                                                                                                                                         |
| -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `sucheRechnungen(filter)`        | Übersetzt die Suchkriterien aus `RechnungFilter` in eine benutzerdefinierte SQL-Abfrage. Ein No-Key-Mapper überführt jede Ergebniszeile in ein read-only `RechnungInfo`-DTO. |
| `checkoutRechnung(id)`           | Lädt die Rechnung und explizit ihre Positionen zur Bearbeitung. Stellt den vollständigen Rechnungsgraphen zusammen.                                                                           |
| `checkinRechnung(rechnung)`      | Speichert die bearbeitete Rechnung einschließlich der zugehörigen Änderungen an ihren Positionen.                                                                                               |
| `ladeSummeAllerRechnungen()`     | Führt die Aggregation direkt per SQL in der Datenbank aus. Ein No-Key-Mapper überführt das Ergebnis in das read-only DTO `RechnungsSummenErgebnis`.                                         |

Die Suche lädt keine `Rechnung`-Entitäten. Die benutzerdefinierte SQL-Abfrage liest nur die für die Ergebnisliste benötigten Daten und bildet jede Zeile auf ein `RechnungInfo`-DTO ab. Diese No-Key-Ergebnisse sind read-only und werden nicht in die Session-Identity-Map integriert. Erst beim Öffnen eines Suchergebnisses wird anhand seiner Rechnungs-ID die zugehörige `Rechnung` einschließlich ihrer Positionen zur Bearbeitung explizit geladen.

Auch für die Summe aller Rechnungen werden keine vollständigen Rechnungsgraphen aufgebaut. Die Datenbank berechnet das Aggregationsergebnis, das anschließend als DTO zur Anzeige bereitsteht. Diese Auswertung umfasst alle Rechnungen und ist unabhängig vom aktuellen Suchfilter.

### Anwendungsfälle mit der DSL `org.modellwerkstatt.objectflow`

| Beispiel-Command                  | Command-Typ   | Aufgabe                                                                                                                      |
| --------------------------------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `Rechnungen suchen`               | `SEARCH`      | Erfasst Suchkriterien und zeigt die als `RechnungInfo`-DTOs geladenen Treffer auf einer zweiten Seite an.                    |
| `Rechnung bearbeiten`             | `GRAPH_OWNER` | Lädt eine Rechnung anhand ihrer ID zur Bearbeitung und registriert Repository-Methoden zum Speichern als Session Operations. |
| `Rechnungsposition bearbeiten`    | `GRAPH_EDIT`  | Bearbeitet eine Position innerhalb der bestehenden Session des `GRAPH_OWNER`.                                                |
| `Summe aller Rechnungen anzeigen` | `SEARCH`      | Ruft die SQL-Aggregation im Repository auf und zeigt das Ergebnis an.                                                        |

Der ebenfalls verfügbare Typ `MODAL_GRAPH_OWNER` wird in diesem Beispiel nicht benötigt.

#### Rechnungen suchen

Der Command `Rechnungen suchen` startet eine eigene Read-only-Session und besteht aus zwei Pages:

1. **Suchfilter eingeben:** Ein Formular ist an das DTO `RechnungFilter` gebunden. Der Benutzer legt die Suchkriterien fest.
2. **Suchergebnisse anzeigen:** Mit den Kriterien aus dem DTO wird die Repository-Methode `sucheRechnungen(filter)` aufgerufen. Sie führt benutzerdefiniertes SQL aus und legt die über ein No-Key-Mapper erzeugten `RechnungInfo`-DTOs in der Property `results` des Filter-DTOs ab. Eine Tabelle auf der zweiten Page zeigt diese Liste an.

Bei der Suche werden weder `Rechnung`-Entitäten noch deren Positionen geladen. Die Session des `SEARCH`-Commands kann nicht committed werden. Die Eingabe von Suchkriterien und das Befüllen von `results` im DTO sind davon unabhängig: Diese Daten dienen dem Suchablauf und werden nicht in die Datenbank geschrieben. Auch die `RechnungInfo`-Ergebnisse des No-Key-Mapper sind read-only und nicht Bestandteil der Session-Identity-Map.

Ein Doppelklick auf eine Tabellenzeile startet `Rechnung bearbeiten`. Als Parameter wird die Rechnungs-ID aus dem ausgewählten `RechnungInfo`-DTO übergeben.

#### Rechnung und Positionen bearbeiten

Der Command `Rechnung bearbeiten` hat den Typ `GRAPH_OWNER` und startet eine eigene Session. Er ist dafür verantwortlich, die Daten zur Bearbeitung zu laden (**Checkout**). Dazu ruft er `checkoutRechnung(id)` mit der übergebenen Rechnungs-ID auf. Die Repository-Methode lädt den Rechnungskopf und die zugehörigen Positionen.

Der Benutzer kann den Rechnungskopf und die Positionen bearbeiten. Für die Bearbeitung einer einzelnen Position wird `Rechnungsposition bearbeiten` vom Typ `GRAPH_EDIT` verwendet. Dieser Command arbeitet innerhalb der bestehenden Session des `GRAPH_OWNER` und eröffnet keine eigene Session. Änderungen werden direkt an der Entität Rechnungsposition durchgeführt.

Der `RechnungsService` übernimmt fachliche Prüfungen und Berechnungen. Der `GRAPH_OWNER` registriert die zum Speichern benötigten Repository-Methoden (**Check-in**) als **Session Operations**. Im Beispiel dient dazu `checkinRechnung(rechnung)`.

Beim vorgesehenen Abschluss des `GRAPH_OWNER` wird eine Datenbanktransaktion gestartet. Die registrierten Session Operations werden ausgeführt und die Transaktion wird committed. Die Session begleitet damit die Bearbeitung; die Transaktion zum Speichern wird erst beim Abschluss ausgeführt.

#### Summe aller Rechnungen anzeigen

Der Command `Summe aller Rechnungen anzeigen` hat den Typ `SEARCH` und verwendet eine eigene Read-only-Session. Er ruft `ladeSummeAllerRechnungen()` im Repository auf.

Die Repository-Methode führt eine aggregierende SQL-Abfrage direkt auf der Datenbank aus. Ein No-Key-Mapper überführt deren Ergebnis in das read-only DTO `RechnungsSummenErgebnis`, das nicht in die Session-Identity-Map integriert wird. Der Command stellt dieses DTO für die Anzeige bereit. Ein Laden und anschließendes Durchlaufen aller Rechnungsentitäten in der Anwendung ist dafür nicht erforderlich.

### Benutzeroberfläche mit der DSL `org.modellwerkstatt.dataux`

Eine **Page** beschreibt eine Seite im Ablauf eines Commands. Die zugehörige **`PagePane`** bildet ihr Gegenstück in der Benutzeroberfläche und nimmt deren UI-Inhalte auf. Formulare, Tabellen, Layouts und andere UI-Komponenten müssen jeweils innerhalb einer `PagePane` eingebunden sein, gegebenenfalls über darin enthaltene Layouts. `PagePane`s können wiederverwendet werden.

| Element                                 | Inhalt                                                                                                                                                                     |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AppUiModule`                           | Einstieg in die Rechnungsverwaltung mit Menüeinträgen für `Rechnungen suchen` und `Summe aller Rechnungen anzeigen`.                                                       |
| `PagePane` für die Suchfilter-Page      | Enthält ein `DelegateForm`, dessen Eingabefelder an die Suchkriterien des DTOs `RechnungFilter` gebunden sind.                                                             |
| `PagePane` für die Suchergebnis-Page    | Enthält eine `Table`, die die `RechnungInfo`-DTOs aus `RechnungFilter.results` zeigt. Ein Doppelklick startet `Rechnung bearbeiten` mit der Rechnungs-ID aus dem DTO.    |
| `PagePane` für die Rechnungsbearbeitung | Enthält ein `DelegateForm` für den Rechnungskopf und eine `Table` für die geladenen Rechnungspositionen. Ein `GridLayout` oder `TabLayout` strukturiert diese Komponenten. |
| `PagePane` für die Positionsbearbeitung | Enthält ein `DelegateForm` zur Bearbeitung einer einzelnen Rechnungsposition im Command `Rechnungsposition bearbeiten`.                                                    |
| `PagePane` für die Summenanzeige        | Enthält ein `DelegateForm` zur Anzeige des DTOs `RechnungsSummenErgebnis`.                                                                                                 |

Die Seitenfolge wird im jeweiligen Command beschrieben. Die zugeordneten `PagePane`s und ihre enthaltenen UI-Komponenten legen Darstellung, Datenbindungen und angebotene Interaktionen fest. Fachliche Prüfungen und Berechnungen bleiben in der Geschäftslogik; Datenbankabfragen und Speicheroperationen liegen im Repository.

### Fachliche Prüfung und Qualitätssicherung

Eine `OFXTestSuit` kann beispielsweise folgende Fälle abdecken:

- Zwei Positionen mit `2 × 50 EUR` und `1 × 30 EUR` ergeben eine Rechnungssumme von `130 EUR`.
- Eine Position mit Menge `0` wird fachlich abgelehnt.
- Die benutzerdefinierte Suchabfrage bildet einen bekannten Datenbestand korrekt auf `RechnungInfo`-DTOs ab und liefert keine `Rechnung`-Entitäten.
- Die SQL-Aggregation liefert für einen bekannten Datenbestand die erwartete Summe aller Rechnungen, unabhängig vom aktuell verwendeten Suchfilter.

### ExpensiveCode und CheapCode im Beispiel

Rechnungsstruktur, Berechnungen, fachliche Prüfungen und Aggregationslogik bilden den sorgfältig abzusichernden fachlichen Kern (**ExpensiveCode**).

Spaltenanordnung, Formularlayouts, Menügestaltung und die Benutzerinteraktion mit diesem Modell gehören zum **CheapCode**. Sie lassen sich beim Ausprobieren unmittelbar beurteilen und durch kurze Feedbackzyklen verbessern. Darstellungs- und Interaktionsanteile eines Commands sind typischerweise CheapCode; fachlich relevante Ablaufregeln im Command können aber auch ExpensiveCode sein.


## Von der Modellierung zur Ausführung

1. **Modellieren und versionieren:** Die Applikation wird mit den DSLs in MPS modelliert und mit Git versioniert. MPS speichert die Modelle als XML-Dateien. Diese enthalten strukturierte Modelle mit Referenzen und Identitäten; ein rein textueller Merge kann deren Konsistenz verletzen. Für die Versionsverwaltung werden deshalb die Git-Unterstützung von MPS und der MPS-Merge-Driver verwendet. Modellkonflikte werden mit den modellbewussten Werkzeugen von MPS aufgelöst. Agenten bearbeiten Modelle über die MPS-Werkzeuge und führen keine manuellen Text-Merges der XML-Modelldateien durch.

2. **Laufzeitkonfiguration auswählen:** In der `OFXConfig` wird über **AppFactories** festgelegt, welche Laufzeitumgebung tatsächlich verwendet wird. Ein Projekt enthält häufig mehrere Konfigurationen.

3. **Vollständig neu bauen:** Vor jedem Ant-Build wird die gesamte Applikation in MPS (alle dem Projekt zugeordneten MPS-Solutions) vollständig neu gebaut (**Rebuild**). Ein inkrementeller Build reicht nicht aus. Dabei wird insbesondere der Java-Code aus den Modellen neu generiert. Erst nach einem erfolgreichen Rebuild wird mit dem nächsten Schritt fortgefahren.

4. **Mit Ant bauen und bereitstellen:** Anschließend wird Ant auf der Konsole ausgeführt. Die projektspezifische Builddatei und die gewählten Targets bestimmen den Build und die Bereitstellung. Sie müssen zur ausgewählten Laufzeitkonfiguration passen.

5. **Ausführen und prüfen:** Die Anwendung wird in der durch die `OFXConfig` festgelegten Laufzeitumgebung gestartet und ihre Funktionsfähigkeit geprüft.


## Weiterführende Dokumentation

Die Detaildokumentationen beschreiben Konzepte, Möglichkeiten, Einschränkungen, Regeln, Beispiele und Best Practices der jeweiligen DSL.

### Detaildokumentationen zu DSLs

| DSL                              | Geplante Dokumentation         | Status             |
| -------------------------------- | ------------------------------ | ------------------ |
| `org.modellwerkstatt.manmap`      | [manmap.md](manmap.md)          | initialer Entwurf   |
| `org.modellwerkstatt.objectflow`  | [objectflow.md](objectflow.md)  | leerer Platzhalter |
| `org.modellwerkstatt.dataux`      | [dataux.md](dataux.md)          | leerer Platzhalter |

### Zusätzliche Informationen

| Thema       | Dokumentation                     |
| ----------- | --------------------------------- |
| Konventionen bei der Modellierung | [konventionen.md](konventionen.md) |


## Stand der Dokumentation

Diese Dokumentation beschreibt die **modellwerkstatt MoWare-Werkbank, Stand Herbst 2026**, auf Basis von **JetBrains MPS 2026.1**.
