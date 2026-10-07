## Verbindliche Konventionen

- **KONVENTION:** Unsere Ubiquitous Language ist Deutsch. Alles, was Fachlichkeit in der Software ausdrückt, wird konsistent mit deutschen Fachbegriffen benannt – insbesondere Namespaces, Datenmodelle, Services und Methoden.
- **KONVENTION:** Command-Namen sind Fachbegriffe mit Leerzeichen, nicht in CamelCase: `Rechnung bearbeiten`, nicht `RechnungBearbeiten`.
- **KONVENTION:** Ein `string` ist nie `null`; „kein Wert“ ist der leere String. Fachlicher Code prüft Strings (falls notwendig) auf Leere und nicht auf `null` und setzt einen String nicht auf `null`. Ausgenommen ist ein String, der bewusst optional geführt wird, etwa als Kriterium eines `optional`-Filters, das mit `null` entfällt.
- **KONVENTION:** Beendet ein Child-Command eines `SEARCH_CMD` erfolgreich, übernimmt der Termination Handler der Suchseite das gepushte Objekt mit `session merge` in die Ergebnisliste; die Suche wird dafür nicht erneut über das Repository ausgeführt.
- **KONVENTION:** Das Datenbankschema erstellt der Entwickler in MPS aus den `EntityMapping`s der Persistence Descriptions. Agenten erzeugen oder ändern keine Datenbankschemata.
