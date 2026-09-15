# modellwerkstatt moware werkbank: 3 DSLs zur Modellierung von Geschäftsanwendungen


## Modellierungssprachen und Laufzeitumgebungen

Die **modellwerkstatt werkbank** basiert auf JetBrains MPS und umfasst drei eng integrierte domänenspezifische Sprachen (DSLs) zur Erstellung von Geschäftsanwendungen. Sie decken Persistenz, Geschäftslogik und Benutzeroberflächen ab. Die Architektur orientiert sich stark an **Domain-Driven Design (DDD)** und übernimmt ausgewählte Konzepte: Entities und Value Objects beschreiben fachliche Daten, Repositories ermöglichen deren Laden und Speichern, und Services bündeln Geschäftslogik.

**manmap** (`org.modellwerkstatt.manmap`) bildet die Persistenzschicht der Anwendung. Die Sprache definiert die Zuordnung zwischen relationalen Datenbanktabellen und Entitäten und stellt Operationen zum Laden, Speichern und Löschen bereit. Diese bilden die Grundlage für den Datenzugriff über Repositories. Komplexe Objektstrukturen werden explizit geladen und zusammengestellt; auf automatisches Lazy Loading wird bewusst verzichtet. Darüber hinaus unterstützt manmap die Arbeit mit Lesemodellen (Read Models) und Tabellenmodellen (Table Models): Komplexe SQL-Abfragen lassen sich formulieren und ihre Ergebnismengen über spezialisierte Mapper in DTOs (Data Transfer Objects) überführen.

**objectflow** (`org.modellwerkstatt.objectflow`) dient der Modellierung von Service-Komponenten und Geschäftslogik. Die Sprache umfasst fachliche Datenstrukturen wie Entities und Value Objects sowie Commands zur Beschreibung von Aktionen und Anwendungsabläufen. Darüber hinaus unterstützt objectflow die Modellierung von Testabläufen in Testsuiten sowie die Definition von Rollen und Berechtigungen.

**dataux** (`org.modellwerkstatt.dataux`) dient der Modellierung von Benutzeroberflächen, Applikationen und BatchJobs. Tabellen und Formulare werden durch ihre Spalten, Felder, Formatierungen und Datenbindungen beschrieben; Layouts strukturieren die Darstellung und ermöglichen die Zusammenstellung komplexerer Oberflächen. Applikationen dienen für Endanwender als Einstiegspunkt und verfügen über das Hauptmenü. Für die automatisierte Verarbeitung lassen sich BatchJobs modellieren, die direkt als Applikation gestartet, zeitgesteuert über Cron ausgeführt oder kontinuierlich mit einer konfigurierten Wartezeit zwischen den Durchläufen betrieben werden können.

Aus den in MPS modellierten Anwendungen wird Java-Code generiert. Für die Ausführung stehen drei Laufzeitumgebungen zur Verfügung: `org.modellwerkstatt.fx8forms` für JavaFX-Desktop-Anwendungen, `org.modellwerkstatt.turkuforms` für Vaadin-Webanwendungen auf Tomcat und `org.modellwerkstatt.h2forms` für HTML5-Webanwendungen mit Pebble Templates auf Tomcat. Während fx8forms und turkuforms primär auf Desktop-PCs ausgerichtet sind, richtet sich h2forms an mobile Datenerfassungsgeräte und Smartphones. Die Applikationsmodelle sind mit wenigen Ausnahmen zwischen diesen Laufzeitumgebungen portabel; bei der Oberflächengestaltung sind insbesondere die unterschiedlichen Bildschirmgrößen zu berücksichtigen.


## Grundprinzipien und Ziele

Die **modellwerkstratt moware werkbank** stellt die fachliche Gestaltung von Geschäftsanwendungen in den Mittelpunkt: Welche Daten werden benötigt, wie hängen sie zusammen, welche Geschäftsregeln gelten und wie arbeiten Benutzer mit ihnen? Die Modellsprachen bieten dafür passende Ausdrucksmittel. Generatoren und Laufzeitumgebungen übernehmen wiederkehrende technische Aufgaben und Infrastruktur-Code. Dadurch konzentriert sich die Anwendungsentwicklung auf fachliche Datenstrukturen, Geschäftslogik und Benutzerinteraktionen.

**Fachliche Modellierung.** Die Architektur orientiert sich an ausgewählten Konzepten des Domain-Driven Design. Entities und Value Objects beschreiben fachliche Daten, Repositories deren Laden und Speichern, Services die Geschäftslogik. Die Entwicklung geeigneter Datenstrukturen und korrekter Geschäftsregeln bleibt die zentrale Entwurfsaufgabe.

**Ausdrucksstarke Geschäftslogik.** Berechnungen, Prüfungen und Änderungen werden unmittelbar an den fachlichen Datenstrukturen formuliert. Java-Ausdrücke und Mengenoperationen unterstützen diese Arbeit. Technische Details der verwendeten UI-Frameworks und Laufzeitumgebungen werden weitgehend durch die Werkzeugkette gekapselt.

**Einheitliche Architektur und klare Zuständigkeiten.** Die Sprachkonzepte geben vor, wo Datenzugriff, Geschäftslogik und Benutzeroberflächen beschrieben werden. Diese gemeinsame Struktur erleichtert die Orientierung, die Wiederverwendung und die Zusammenarbeit. Fachliche Begriffe bleiben im Modell sichtbar und unterstützen die Abstimmung zwischen Entwicklern und Fachverantwortlichen.

**Schrittweise Entwicklung und überprüfbare Anforderungen.** Anwendungen werden anhand konkreter Anwendungsfälle modelliert und schrittweise verfeinert. Beispiele, Testdaten und Testabläufe helfen, fachliche Annahmen früh zu prüfen und Änderungen abzusichern. Die zugehörige Dokumentation wird möglichst direkt bei den beschriebenen Modellelementen gepflegt.

**ExpensiveCode und CheapCode.** MoWare unterscheidet zwischen aufwendig erarbeitetem Fachwissen (*ExpensiveCode*) und leichter überprüfbaren und anpassbaren Teilen einer Anwendung (*CheapCode*). Zum ExpensiveCode gehören insbesondere fachliche Datenstrukturen, Geschäftsregeln und Verarbeitungslogik. Ihre Entwicklung erfordert Domänenwissen und sorgfältige Abstimmung; Fehler sind häufig erst durch eine fachliche Prüfung erkennbar. CheapCode umfasst dagegen UI-Beschreibungen, Menüs und die Gestaltung der Interaktion mit dem fachlichen Modell. Fehler in diesen Bereichen fallen beim Ausprobieren meist schnell auf und lassen sich gezielt korrigieren. Das fachliche Modell verlangt besondere Sorgfalt, während Oberflächen und Bedienabläufe durch kurze Feedbackzyklen schrittweise verbessert werden können.

**Langfristige Wartbarkeit und technische Flexibilität.** Das fachliche Wissen wird in den Modellen festgehalten. Generatoren und Laufzeitumgebungen bestimmen dessen technische Umsetzung. Diese Trennung ermöglicht es, fachliche Anforderungen und technische Infrastruktur weitgehend unabhängig weiterzuentwickeln. Ziel ist, bestehende Modelle langfristig zu nutzen und Anpassungen an Frameworks oder Ausführungsplattformen möglichst zentral umzusetzen.


## Fachliche Architektur und Domain-Driven Design

Der gesamte Stack orientiert sich stark an Domain-Driven Design (DDD), übernimmt aber nicht sämtliche DDD-Konzepte. Aus dieser Orientierung dürfen keine zusätzlichen, hier nicht beschriebenen Regeln für die DSLs abgeleitet werden.

| Baustein | Rolle im Stack |
| --- | --- |
| Entities und Value Objects | Modellierung fachlicher Daten |
| DTOs (Data Transfer Objects) | Datencontainer ausschließlich für die Benutzeroberfläche |
| Persistenzbausteine | Laden von Daten aus der Datenbank und Speichern von Daten; genaue Konzeptbezeichnung noch zu bestätigen |
| Commands und Command-Handler | Beschreibung beziehungsweise Umsetzung von Aktionen und Benutzerinteraktionen; vier Typen mit unterschiedlichen Session-Regeln |
| UI-Beschreibungen | Modellierung der Benutzeroberflächen |

Die genauen Eigenschaften und Abgrenzungen von Entities, Value Objects und DTOs werden in der DSL-Referenz beschrieben. Der Begriff für die Persistenzbausteine war in der Spracheingabe nicht eindeutig und wird daher noch nicht als technischer Bezeichner verwendet.

## Sessions, Commands und Transaktionen

> Arbeitsstand: Die folgenden Abläufe stammen aus der Beschreibung des Sprachverantwortlichen. Die vier Bezeichnungen wurden durch die Spracheingabe nicht eindeutig wiedergegeben. Die Zeilen beschreiben vorläufig vier Verhaltensweisen und legen keine technischen Typnamen fest.

| Beschriebener Typ | Session und Interaktion | Schreiben und Commit |
| --- | --- | --- |
| SEARCH Command | Startet eine Session im Hintergrund. Lädt Daten anhand von Filtern, kann sie aufbereiten und über mehrere Pages beziehungsweise Views anzeigen. | Die Session darf nicht committed werden; Änderungen dürfen über diese Session nicht in die Datenbank geschrieben werden. |
| GRAPH_OWNER Command | Startet eine eigene Session. Lädt Daten und bereitet sie auf; Benutzer können sie auch über die Oberfläche bearbeiten. | Zum Abschluss werden registrierte Session Operations innerhalb einer Datenbanktransaktion ausgeführt und committed. Der genaue Auslöser ist noch zu klären. |
| GRAPH_EDIT Command | Startet keine neue Session, sondern übernimmt eine bestehende Session eines Performers. Dient der Modellierung von Benutzerinteraktion. | Eigene Abschluss- und Commit-Befugnisse sind noch zu klären. |
| MODAL_GRAPH_OWNER | Modale Benutzerinteraktion, vergleichbar mit einem Dialogfenster. | Session-Zuordnung und Transaktionsverhalten sind noch zu bestätigen. |

Beim ändernden Command registriert der Anwendungsentwickler auszuführende Operationen auf einem **Session Operation Stack**. Zum beschriebenen Abschluss wird eine Datenbanktransaktion gestartet, die registrierten Operationen werden ausgeführt und die Transaktion wird committed. Die Reihenfolge der Abarbeitung, das Verhalten bei Fehlern und Abbruch sowie der genaue Abschlussmechanismus sind noch offen; aus dem Wort „Stack“ wird keine Ausführungsreihenfolge abgeleitet.

Die beschriebene Session begleitet Laden und Benutzerinteraktion. Die Datenbanktransaktion zur Ausführung der Session Operations beginnt dagegen erst beim genannten Abschluss. Session-Lebensdauer und diese Transaktionsdauer sind daher getrennt zu dokumentieren. Über weitere Transaktionen beim Laden trifft diese Beschreibung keine Aussage.

## Von der Modellierung zur Ausführung

1. Die Applikation wird mit den DSLs in MPS modelliert.
2. Aus dem Applikationsmodell wird Java-Code generiert.
3. Die Anwendung wird für die gewählte Laufzeitumgebung gebaut und bereitgestellt. Die konkreten Build- und Bereitstellungsschritte sind noch zu dokumentieren.
4. Die Anwendung wird in der gewählten Laufzeitumgebung ausgeführt.

## Laufzeitumgebungen

| Ziel | Technologie | Laufzeitumgebung | Primäre Gerätezielgruppe |
| --- | --- | --- | --- |
| Desktop-Anwendung | JavaFX | `org.modellwerkstatt.fx8forms` | Desktop-PCs |
| Webanwendung auf Tomcat | Vaadin | `org.modellwerkstatt.turkuforms` | Desktop-PCs |
| HTML5-Webanwendung auf Tomcat | Pebble Templates | `org.modellwerkstatt.h2forms` | Mobile Datenerfassungsgeräte (MDE), beispielsweise von Zebra oder Datalogic, sowie Smartphones |

Die Applikationsmodelle sind laut Sprachverantwortlichem mit wenigen Ausnahmen zwischen den drei Laufzeitumgebungen portabel. Die konkreten Ausnahmen sind noch zu erfassen.

Die Gerätezielgruppen unterscheiden sich insbesondere durch ihre Bildschirmgrößen: `h2forms` richtet sich an MDE-Geräte und Smartphones; `turkuforms` und `fx8forms` primär an Desktop-PCs. Die technische Portabilität eines Modells ist deshalb von der Eignung seiner Oberfläche für die jeweilige Bildschirmgröße zu unterscheiden. Konkrete Empfehlungen zur Gestaltung und gegebenenfalls nötige Modellanpassungen sind noch zu dokumentieren.