## Modellierungsumfang und Ausdrucksmöglichkeiten

`org.modellwerkstatt.manmap` beschreibt den Zugriff auf relationale Datenbanken. Die Sprache unterstützt sowohl das Laden und Speichern fachlicher Entitäten als auch gezielte SQL-Abfragen, deren Ergebnisse als DTOs bereitgestellt werden.

**Persistenzabbildungen definieren.** Innerhalb einer `PersistenceDescription` werden Mappings zwischen Entitäten und relationalen Datenbanktabellen beschrieben. Sie legen fest, wie die Eigenschaften einer Entität den Spalten der jeweiligen Tabelle zugeordnet werden.

**Datenzugriffe in Repositories bündeln.** Ein `Repository` enthält Methoden zum Suchen, Laden, Speichern und Löschen von Daten. Suchkriterien können beispielsweise über ein FilterDTO übergeben und in den Abfragen berücksichtigt werden.

**Fachliche Objektstrukturen explizit aufbauen.** Zusammengehörige Entitäten werden gezielt geladen und miteinander verbunden. Beispielsweise kann eine Repository-Methode eine Rechnung und ihre Positionen laden und daraus den vollständigen Rechnungsgraphen zusammenstellen. Es findet kein automatisches Lazy Loading statt; Umfang und Ablauf des Ladens werden ausdrücklich beschrieben.

**Lesemodelle und SQL-Abfragen formulieren.** Neben Entitäts-Mappings unterstützt manmap benutzerdefinierte SQL-Abfragen für Suchübersichten, Tabellenmodelle und Auswertungen. Damit lassen sich genau die Daten abfragen, die für einen Anwendungsfall benötigt werden, ohne vollständige fachliche Objektgraphen aufzubauen.

**Ergebnismengen auf DTOs abbilden.** Spezialisierte Mapper überführen Result-Sets in Datencontainer. So kann eine Rechnungssuche `RechnungInfo`-DTOs für die Ergebnisliste liefern. Auch Aggregationen lassen sich direkt in der Datenbank ausführen und ihre Ergebnisse über einen `nokeystore/read-only map`-Mapper als DTO bereitstellen.

**Speicheroperationen beschreiben.** Repository-Methoden legen fest, wie fachliche Daten gespeichert und Änderungen an zusammengehörigen Entitäten persistiert werden. In einem Bearbeitungsablauf registriert der zuständige `GRAPH_OWNER` diese Methoden als session operations. Die Koordination der Session und ihres Abschlusses gehört zu `org.modellwerkstatt.objectflow`; die Datenbankoperationen werden in `org.modellwerkstatt.manmap` beschrieben.
