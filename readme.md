# modellwerkstatt moware werkbank – Dokumentation

Dieses Repository enthält die Dokumentation der **modellwerkstatt moware werkbank** und ihrer drei domänenspezifischen Sprachen zur Entwicklung von Geschäftsanwendungen mit JetBrains MPS.

Im Mittelpunkt stehen fachliche Datenstrukturen, Geschäftslogik und Benutzerinteraktionen. Die Architektur orientiert sich an ausgewählten Konzepten des Domain-Driven Design. Generatoren und Laufzeitumgebungen übernehmen wiederkehrende technische Aufgaben und erzeugen aus den Modellen ausführbare Java-Anwendungen.

## Einstieg und Sprachreferenzen

Die Dokumentation richtet sich an Anwendungsentwickler und KI-Agenten. Als Einstieg dient die übergeordnete Übersicht. Die Sprachreferenzen vertiefen die Konzepte, Regeln, Einschränkungen und Best Practices der jeweiligen DSL.

| Dokument                                                   | Inhalt                                                                                                                   |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| [modellwerkstatt-overview.md](modellwerkstatt-overview.md) | Grundprinzipien, fachliche Architektur, zentrale Konzepte, Laufzeitumgebungen und Entwicklungsablauf                     |
| [manmap.md](manmap.md)                                     | `org.modellwerkstatt.manmap`: Persistenzabbildungen, Repositories, SQL-Abfragen und Mapping von Ergebnismengen           |
| [objectflow.md](objectflow.md)                             | `org.modellwerkstatt.objectflow`: fachliche Datenstrukturen, Services, Commands, Konfiguration, Tests und Berechtigungen |
| [dataux.md](dataux.md)                                     | `org.modellwerkstatt.dataux`: Benutzeroberflächen, Applikationen, Menüs und BatchJobs                                    |