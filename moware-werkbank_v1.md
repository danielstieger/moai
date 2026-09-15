# modellwerkstatt moware werkbank: 3 DSLs zur Modellierung von Geschäftsanwendungen


## Modellierungssprachen und Laufzeitumgebungen

Die **modellwerkstatt werkbank** basiert auf JetBrains MPS und umfasst drei eng integrierte domänenspezifische Sprachen (DSLs) zur Erstellung von Geschäftsanwendungen. Sie decken Persistenz, Geschäftslogik und Benutzeroberflächen ab. Die Architektur orientiert sich stark an **Domain-Driven Design (DDD)** und übernimmt ausgewählte Konzepte: Entities und Value Objects beschreiben fachliche Daten, Repositories ermöglichen deren Laden und Speichern, und Services bündeln Geschäftslogik.

**manmap** (`org.modellwerkstatt.manmap`) bildet die Persistenzschicht der Anwendung. Die Sprache definiert die Zuordnung zwischen relationalen Datenbanktabellen und Entitäten und stellt Operationen zum Laden, Speichern und Löschen bereit. Diese bilden die Grundlage für den Datenzugriff über Repositories. Komplexe Objektstrukturen werden explizit geladen und zusammengestellt; auf automatisches Lazy Loading wird bewusst verzichtet. Darüber hinaus unterstützt manmap die Arbeit mit Lesemodellen (Read Models) und Tabellenmodellen (Table Models): Komplexe SQL-Abfragen lassen sich formulieren und ihre Ergebnismengen über spezialisierte Mapper in DTOs (Data Transfer Objects) überführen.

**objectflow** (`org.modellwerkstatt.objectflow`) dient der Modellierung von Service-Komponenten und Geschäftslogik. Die Sprache umfasst fachliche Datenstrukturen wie Entities und Value Objects sowie Commands zur Beschreibung von Aktionen und Anwendungsabläufen. Darüber hinaus unterstützt objectflow die Modellierung von Testabläufen in Testsuiten sowie die Definition von Rollen und Berechtigungen.

**dataux** (`org.modellwerkstatt.dataux`) dient der Modellierung von Benutzeroberflächen, Applikationen und BatchJobs. Tabellen und Formulare werden durch ihre Spalten, Felder, Formatierungen und Datenbindungen beschrieben; Layouts strukturieren die Darstellung und ermöglichen die Zusammenstellung komplexerer Oberflächen. Applikationen dienen für Endanwender als Einstiegspunkt und verfügen über das Hauptmenü. Für die automatisierte Verarbeitung lassen sich BatchJobs modellieren, die direkt als Applikation gestartet, zeitgesteuert über Cron ausgeführt oder kontinuierlich mit einer konfigurierten Wartezeit zwischen den Durchläufen betrieben werden können.

Aus den in MPS modellierten Anwendungen wird Java-Code generiert. Für die Ausführung stehen drei Laufzeitumgebungen zur Verfügung: `org.modellwerkstatt.fx8forms` für JavaFX-Desktop-Anwendungen, `org.modellwerkstatt.turkuforms` für Vaadin-Webanwendungen auf Tomcat und `org.modellwerkstatt.h2forms` für HTML5-Webanwendungen mit Pebble Templates auf Tomcat. Während fx8forms und turkuforms primär auf Desktop-PCs ausgerichtet sind, richtet sich h2forms an mobile Datenerfassungsgeräte und Smartphones. Die Applikationsmodelle sind mit wenigen Ausnahmen zwischen diesen Laufzeitumgebungen portabel; bei der Oberflächengestaltung sind insbesondere die unterschiedlichen Bildschirmgrößen zu berücksichtigen.


## Grundprinzipien und Ziele

Die **modellwerkstatt moware werkbank** stellt die fachliche Gestaltung von Geschäftsanwendungen in den Mittelpunkt: Welche Daten werden benötigt, wie hängen sie zusammen, welche Geschäftsregeln gelten und wie arbeiten Benutzer mit ihnen? Die Modellsprachen bieten dafür passende Ausdrucksmittel. Generatoren und Laufzeitumgebungen übernehmen wiederkehrende technische Aufgaben und Infrastruktur-Code. Dadurch konzentriert sich die Anwendungsentwicklung auf fachliche Datenstrukturen, Geschäftslogik und Benutzerinteraktionen.

**Fachliche Modellierung.** Die Architektur orientiert sich an ausgewählten Konzepten des Domain-Driven Design. Entities und Value Objects beschreiben fachliche Daten, Repositories deren Laden und Speichern, Services die Geschäftslogik. Die Entwicklung geeigneter Datenstrukturen und korrekter Geschäftsregeln bleibt die zentrale Entwurfsaufgabe.

**Ausdrucksstarke Geschäftslogik.** Berechnungen, Prüfungen und Änderungen werden unmittelbar an den fachlichen Datenstrukturen formuliert. Java-Ausdrücke und Mengenoperationen unterstützen diese Arbeit. Technische Details der verwendeten UI-Frameworks und Laufzeitumgebungen werden weitgehend durch die Werkzeugkette gekapselt.

**Einheitliche Architektur und klare Zuständigkeiten.** Die Sprachkonzepte geben vor, wo Datenzugriff, Geschäftslogik und Benutzeroberflächen beschrieben werden. Diese gemeinsame Struktur erleichtert die Orientierung, die Wiederverwendung und die Zusammenarbeit. Fachliche Begriffe bleiben im Modell sichtbar und unterstützen die Abstimmung zwischen Entwicklern und Fachverantwortlichen.

**Schrittweise Entwicklung und überprüfbare Anforderungen.** Anwendungen werden anhand konkreter Anwendungsfälle modelliert und schrittweise verfeinert. Beispiele, Testdaten und Testabläufe helfen, fachliche Annahmen früh zu prüfen und Änderungen abzusichern. Die zugehörige Dokumentation wird möglichst direkt bei den beschriebenen Modellelementen gepflegt.

**ExpensiveCode und CheapCode.** MoWare unterscheidet zwischen aufwendig erarbeitetem Fachwissen (*ExpensiveCode*) und leichter überprüfbaren und anpassbaren Teilen einer Anwendung (*CheapCode*). Zum ExpensiveCode gehören insbesondere fachliche Datenstrukturen, Geschäftsregeln und Verarbeitungslogik. Ihre Entwicklung erfordert Domänenwissen und sorgfältige Abstimmung; Fehler sind häufig erst durch eine fachliche Prüfung erkennbar. CheapCode umfasst dagegen UI-Beschreibungen, Menüs und die Gestaltung der Interaktion mit dem fachlichen Modell. Fehler in diesen Bereichen fallen beim Ausprobieren meist schnell auf und lassen sich gezielt korrigieren. Das fachliche Modell verlangt besondere Sorgfalt, während Oberflächen und Bedienabläufe durch kurze Feedbackzyklen schrittweise verbessert werden können.

**Langfristige Wartbarkeit und technische Flexibilität.** Das fachliche Wissen wird in den Modellen festgehalten. Generatoren und Laufzeitumgebungen bestimmen dessen technische Umsetzung. Diese Trennung ermöglicht es, fachliche Anforderungen und technische Infrastruktur weitgehend unabhängig weiterzuentwickeln. Ziel ist, bestehende Modelle langfristig zu nutzen und Anpassungen an Frameworks oder Ausführungsplattformen möglichst zentral umzusetzen.


## Zentrale Konzepte der moware werkbank DSLs
 
Der gesamte Stack orientiert sich stark an Domain-Driven Design (DDD), übernimmt aber nicht sämtliche DDD-Konzepte. Diese Übersicht erfasst die zentralen Konzepte der drei MoWare-Sprachen. Sie beschreiben die erkennbare Verantwortung der Konzepte, ohne zusätzliche DDD-Regeln für die DSLs festzulegen.


### Einordnung entlang der fachlichen Architektur

| Schicht                            | Konzept                                                              | Implementiert in DSL                              |
| ---------------------------------- | ------------------------------------------------------------------------------- | -------------------------------- |
| Fachliches Modell                  | `Entity`, `ValueObject`, `DTO`                                                  | `org.modellwerkstatt.objectflow` |
| Geschäftslogik und Anwendungsfälle | `Service`, `Command`                                                            | `org.modellwerkstatt.objectflow` |
| Persistenz                         | `PersistenceDescription`, `Repository`                                          | `org.modellwerkstatt.manmap`     |
| Benutzeroberfläche                 | `PagePane`, `Table`, `DelegateForm`, `GridLayout`, `TabLayout`, `CustomElement` | `org.modellwerkstatt.dataux`     |
| Ausführbare Module                 | `AppUiModule`, `BatchJobModule`                                                 | `org.modellwerkstatt.dataux`     |
| Querschnitt                        | `OFXConfig`, `OFXTestSuit`, `RolesAndPermissions`, `StaticRessources`           | `org.modellwerkstatt.objectflow` |


### org.modellwerkstatt.manmap im Detail

`org.modellwerkstatt.manmap` bildet die Persistenzschicht und verbindet fachliche Objekte mit der relationalen Datenbank (Oracle oder MySQL). Neben der Persistierung von Entitäten unterstützt die Sprache benutzerdefinierte SQL-Abfragen und das Überführen ihrer Ergebnismengen in Datencontainer.

| Kurzbezeichnung          | FQ-Name                                                       | Beschreibung/Aufgabe                                                                                                                                                                                                                                                                                   |
| ------------------------ | ------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `PersistenceDescription` | `org.modellwerkstatt.manmap.structure.PersistenceDescription` | Bündelt die Persistenzabbildungen eines Modells. Die enthaltenen Entity-Mappings ordnen fachliche Objekte und ihre Eigenschaften Tabellen, Spalten und Beziehungen zu.                                                                                                                                 |
| `Repository`             | `org.modellwerkstatt.manmap.structure.Repository`             | Kapselt den Datenbankzugriff. Enthält Methoden zum Abfragen, Laden, Zusammensetzen, Speichern und Löschen fachlicher Objekte. Unterstützt außerdem benutzerdefinierte SQL-Abfragen (Custom SQL) und spezialisierte Mapper, die Ergebnismengen (Result-Sets) in Objekte, insbesondere DTOs, überführen. |

### org.modellwerkstatt.objectflow im Detail

`org.modellwerkstatt.objectflow` beschreibt das fachliche Modell, Service-Komponenten, Anwendungsoperationen und Geschäftsabläufe. Ergänzend stellt die Sprache Konzepte für Konfiguration, Tests, Berechtigungen und gemeinsame Ressourcen bereit.

| Kurzbezeichnung       | FQ-Name                                                        | Beschreibung/Aufgabe                                                                                                                                                                                                                                                                |
| --------------------- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Entity`              | `org.modellwerkstatt.objectflow.structure.Entity`              | Beschreibt ein fachliches Objekt mit eigener Identität und Lebenszyklus. Trägt fachliche Eigenschaften und Verhalten und ist typischerweise persistent.                                                                                                                             |
| `ValueObject`         | `org.modellwerkstatt.objectflow.structure.ValueObject`         | Beschreibt einen fachlichen Wert ohne eigene Identität. Seine Gleichheit kann über ausgewählte Eigenschaften definiert werden.                                                                                                                                                      |
| `DTO`                 | `org.modellwerkstatt.objectflow.structure.DTO`                 | Definiert einen Datencontainer für die Benutzeroberfläche oder die Ergebnisse von Datenbankabfragen. Nimmt die für eine Darstellung oder Interaktion benötigten Daten auf und kann durch Mapper aus Result-Sets befüllt werden, ohne selbst ein persistentes Domänenobjekt zu sein. |
| `Service`             | `org.modellwerkstatt.objectflow.structure.Service`             | Bündelt fachliche oder anwendungsbezogene Operationen, die nicht sinnvoll einer einzelnen Entity oder einem Value Object zugeordnet werden. Erlaubt Zugriff auf Repositories und andere Infrastrukturkomponenten.                                                                             |
| `Command`             | `org.modellwerkstatt.objectflow.structure.Command`             | Modelliert einen Anwendungsfall beziehungsweise eine Benutzeraktion. Koordiniert Parameter, Zustandsvariablen, Seiten sowie Initialisierung und Abschluss bei Bestätigung oder Abbruch. Steuert Session-Logik.                                                                                             |
| `OFXConfig`           | `org.modellwerkstatt.objectflow.structure.OFXConfig`           | Definiert die zentrale Konfiguration der Anwendungskomponenten und ihrer Abhängigkeiten. Ist konzeptionell mit einer XML-basierten Spring-Bean-Konfiguration vergleichbar: Komponenten werden konfiguriert und ihre Abhängigkeiten miteinander verdrahtet.                          |
| `OFXTestSuit`         | `org.modellwerkstatt.objectflow.structure.OFXTestSuit`         | Definiert eine eigenständig ausführbare Testsuite mit konfigurierten Komponenten, Start-/Ende-Logik und Testinhalten.                                                                                                                                                               |
| `RolesAndPermissions` | `org.modellwerkstatt.objectflow.structure.RolesAndPermissions` | Beschreibt das Berechtigungsmodell mit Rollen, Geltungsbereichen und Identitäten. Dient als zentrale Grundlage für Zugriffskontrollen.                                                                                                                                              |
| `StaticRessources`    | `org.modellwerkstatt.objectflow.structure.StaticRessources`    | Bündelt wiederverwendbare, plattformbezogene Ressourcen wie Bezeichnungen und Farben. Ressourcensätze können aufeinander aufbauen.                                                                                                                                                  |

### org.modellwerkstatt.dataux im Detail

`org.modellwerkstatt.dataux` beschreibt Benutzeroberflächen, ausführbare Anwendungen und Batch-Verarbeitung.

| Kurzbezeichnung  | FQ-Name                                               | Beschreibung/Aufgabe                                                                                                                                                                                              |
| ---------------- | ----------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AppUiModule`    | `org.modellwerkstatt.dataux.structure.AppUiModule`    | Definiert eine ausführbare Anwendung mit Benutzeroberfläche. Bündelt Konfiguration, Authentifizierung, Haupt- und Zusatzmenüs sowie Kacheln.                                                   |
| `BatchJobModule` | `org.modellwerkstatt.dataux.structure.BatchJobModule` | Definiert einen automatisiert ausführbaren BatchJob. Bündelt Konfiguration, Fehlerstrategie und Producer-Consumer-Verarbeitung; Betriebsart und Zeitsteuerung werden über Optionen festgelegt. |
| `PagePane`       | `org.modellwerkstatt.dataux.structure.PagePane`       | Kapselt den Inhalt einer Anwendungsseite als wiederverwendbares UI-Element und kann seitenspezifische Optionen und Menüeinträge bereitstellen.                                                                    |
| `Table`          | `org.modellwerkstatt.dataux.structure.Table`          | Beschreibt eine tabellarische Darstellung gebundener Daten. Delegates, Optionen und Menüeinträge bestimmen Spalten, Darstellung und Interaktionen.                                                                |
| `DelegateForm`   | `org.modellwerkstatt.dataux.structure.DelegateForm`   | Beschreibt ein an ein fachliches Objekt oder eine Eigenschaft gebundenes Formular, dessen Felder aus Delegates zusammengesetzt werden.                                                                            |
| `GridLayout`     | `org.modellwerkstatt.dataux.structure.GridLayout`     | Ordnet UI-Elemente in Zeilen und Spalten an. Gewichtungen steuern die Größenverteilung im Raster.                                                                                                                 |
| `TabLayout`      | `org.modellwerkstatt.dataux.structure.TabLayout`      | Strukturiert eine Oberfläche in mehrere Registerkarten und bündelt deren jeweilige Inhalte.                                                                                                                       |
| `CustomElement`  | `org.modellwerkstatt.dataux.structure.CustomElement`  | Deklariert ein projektspezifisches UI-Element mit eigener Implementierungsklasse, optionaler Datenbindung, Delegates und Menüaktionen.                                                                            |


## Laufzeitumgebungen

Die Ausführung richtet sich nach dem modellierten Modultyp: Anwendungen mit Benutzeroberfläche unterstützen drei Laufzeitumgebungen, BatchJobs können automatisiert oder mit Benutzeroberfläche betrieben werden. Testsuiten werden in der MPS-Konsole ausgeführt.

| Konzept         | Ausführungsart                                    | Technologie / Laufzeitumgebung                   | Primärer Einsatz                                                       |
| ---------------- | ------------------------------------------------- | ------------------------------------------------ | ---------------------------------------------------------------------- |
| `AppUiModule`    | Desktop-Anwendung                                 | JavaFX / `org.modellwerkstatt.fx8forms`          | Desktop-PCs                                                            |
| `AppUiModule`    | Webanwendung auf Tomcat                           | Vaadin / `org.modellwerkstatt.turkuforms`        | Desktop-PCs                                                            |
| `AppUiModule`    | HTML5-Webanwendung auf Tomcat                     | Pebble Templates / `org.modellwerkstatt.h2forms` | MDE-Geräte, beispielsweise von Zebra oder Datalogic, sowie Smartphones |
| `BatchJobModule` | Automatisierte Ausführung ohne Benutzeroberfläche | Servlet auf Tomcat                               | Hintergrundverarbeitung                                                |
| `BatchJobModule` | Ausführung mit Desktop-Oberfläche                 | JavaFX / `org.modellwerkstatt.fx8forms`          | Interaktive Ausführung auf Desktop-PCs                                 |
| `BatchJobModule` | Ausführung mit Weboberfläche                      | Vaadin / `org.modellwerkstatt.turkuforms`        | Interaktive Ausführung im Browser                                      |
| `OFXTestSuit`    | Testausführung                                    | MPS-Konsole                                      | Ausführen und Prüfen modellierter Testabläufe                          |

Applikationsmodelle sind mit wenigen Ausnahmen zwischen `org.modellwerkstatt.fx8forms`, `org.modellwerkstatt.turkuforms` und `org.modellwerkstatt.h2forms` portabel. Bei der Oberflächengestaltung sind die unterschiedlichen Gerätezielgruppen und Bildschirmgrößen zu berücksichtigen: Eine technisch ausführbare Oberfläche ist nicht automatisch für jedes Gerät gleichermaßen geeignet.

BatchJobs können direkt gestartet, zeitgesteuert über Cron ausgeführt oder kontinuierlich mit einer konfigurierten Wartezeit zwischen den Durchläufen betrieben werden. Zusätzlich ist eine Ausführung mit Benutzeroberfläche über `org.modellwerkstatt.fx8forms` oder `org.modellwerkstatt.turkuforms` möglich.


## Von der Modellierung zur Ausführung

1. **Modellieren und versionieren:** Die Applikation wird mit den DSLs in MPS modelliert und mit Git versioniert. MPS speichert die Modelle als XML-Dateien. Diese enthalten strukturierte Modelle mit Referenzen und Identitäten; ein rein textueller Merge kann deren Konsistenz verletzen. Für die Versionsverwaltung werden deshalb die Git-Unterstützung von MPS und der MPS-Merge-Driver verwendet. Modellkonflikte werden mit den modellbewussten Werkzeugen von MPS aufgelöst. Agenten bearbeiten Modelle über die MPS-Werkzeuge und führen keine manuellen Text-Merges der XML-Modelldateien durch.

2. **Laufzeitkonfiguration auswählen:** In der `OFXConfig` wird über die **AppFactories** festgelegt, welche Laufzeitumgebung tatsächlich verwendet wird. Ein Projekt enthält daher meist mehrere Konfigurationen. Vor dem Build ist zu prüfen, welche `OFXConfig` das auszuführende Modul verwendet und ob deren AppFactories zur gewünschten Laufzeitumgebung passen.

3. **Vollständig neu bauen:** Vor jedem Ant-Build wird die gesamte Applikation in MPS vollständig neu gebaut (**Rebuild**). Ein inkrementeller Build reicht nicht aus. Dabei wird insbesondere der Java-Code aus den Modellen neu generiert. Erst nach einem erfolgreichen Rebuild wird mit dem nächsten Schritt fortgefahren.

4. **Mit Ant bauen und bereitstellen:** Anschließend wird Ant auf der Konsole ausgeführt. Die projektspezifische Builddatei und die gewählten Targets bestimmen den Build und die Bereitstellung. Sie müssen zur ausgewählten Laufzeitkonfiguration passen.

5. **Ausführen und prüfen:** Die Anwendung wird in der durch die `OFXConfig` festgelegten Laufzeitumgebung gestartet und ihre Funktionsfähigkeit geprüft.

## Weiterführende Dokumentation

Die Detaildokumentationen beschreiben Konzepte, Möglichkeiten, Einschränkungen, Regeln, Beispiele und Best Practices der jeweiligen DSL.

| DSL                              | Dokumentation                  |
| -------------------------------- | ------------------------------ |
| `org.modellwerkstatt.manmap`     | [manmap.md](manmap.md)         |
| `org.modellwerkstatt.objectflow` | [objectflow.md](objectflow.md) |
| `org.modellwerkstatt.dataux`     | [dataux.md](dataux.md)         |


## Stand der Dokumentation
Diese Dokumentation beschreibt die **modellwerkstatt moware werkbank, Stand Herbst 2026**, auf Basis von **JetBrains MPS 2026.1**.