# moai - Ai-Unterstützung für die **modellwerkstatt moware werkbank** 

Dieses Repository enthält die Dokumentation der **modellwerkstatt moware werkbank** und ihrer drei domänenspezifischen Sprachen (DSLs) zur Entwicklung von Geschäftsanwendungen mit JetBrains MPS. 

Im Mittelpunkt steht die Modellierung von fachlichen Datenstrukturen, Geschäftslogik und Benutzerinteraktionen. Die Architektur orientiert sich an ausgewählten Konzepten des Domain-Driven Design. Generatoren und Laufzeitumgebungen übernehmen wiederkehrende technische Aufgaben und erzeugen aus den Modellen ausführbare Java-Anwendungen.

## Einstieg und Sprachreferenzen

Die Dokumentation richtet sich an Anwendungsentwickler und KI-Agenten. Daher sind neben Konzeptlandkarten für die DSLs jeweils auch Fully-Qualified-Names der Sprachkonzepte angegeben. 
Als Einstieg dient das übergeordnete Dokument. Die Sprachreferenzen vertiefen die Konzepte, Regeln, Einschränkungen und Best Practices der jeweiligen DSL.

| Dokument                                                   | Inhalt                                                                                                                   |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| [moware-werkbank.md](moware-werkbank.md) | Grundprinzipien, fachliche Architektur, zentrale Konzepte, Laufzeitumgebungen und Entwicklungsablauf                     |
| [manmap.md](manmap.md)                                     | `org.modellwerkstatt.manmap`: Persistenzabbildungen, Repositories, SQL-Abfragen und Mapping von Ergebnismengen           |
| [objectflow.md](objectflow.md)                             | `org.modellwerkstatt.objectflow`: fachliche Datenstrukturen, Services, Commands, Konfiguration, Tests und Berechtigungen |
| [dataux.md](dataux.md)                                     | `org.modellwerkstatt.dataux`: Benutzeroberflächen, Applikationen, Menüs und BatchJobs                                    |
