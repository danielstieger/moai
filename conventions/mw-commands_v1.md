## Verbindliche Konventionen für Commands

### Benennung

- **KONVENTION:** Command-Namen sind Fachbegriffe mit Leerzeichen, nicht in CamelCase: `Rechnung bearbeiten`, nicht `RechnungBearbeiten`.

### Owner und Edit

- **KONVENTION:** Ein `GRAPH_OWNER_CMD` hält ein editierbares `Delegate Form` nur, wenn er ein neues Objekt anlegt. Lädt er ein bestehendes Aggregat, ist sein `Delegate Form` `DISABLED`; der Owner hält Session und Navigation, die editierbaren `Delegate Form`s öffnen `GRAPH_EDIT_CMD`s.

### Suche und Rückgabe

- **KONVENTION:** Besteht die Ergebnisliste eines `SEARCH_CMD` aus Entities und beendet ein Child-Command erfolgreich, übernimmt der Termination Handler der Suchseite das gepushte Objekt mit `session merge` in die Ergebnisliste; die Suche wird dafür nicht erneut über das Repository ausgeführt.
- **KONVENTION:** Besteht die Ergebnisliste eines `SEARCH_CMD` aus DTOs, pusht der `GRAPH_OWNER_CMD` bei seinem Abschluss das Aggregat, kein DTO. Der Termination Handler der Suchseite übernimmt die Werte aus dem Aggregat in das vorhandene DTO der Ergebnisliste oder legt ein neues DTO an und übernimmt sie dort.
