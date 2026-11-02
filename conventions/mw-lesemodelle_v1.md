## Verbindliche Konventionen für Lesemodelle

### Aufbau einer Such- oder Listenabfrage mit Custom SQL

- **KONVENTION:** Optionale Kriterien werden über den Kontrollfluss im `SQL`-Block abgebildet, nicht im SQL-Text: Ein Kriterium ist ein `if`, dessen Zweig sein `C2SqlText`-Fragment enthält; ein nicht gesetztes Kriterium erzeugt kein Fragment. Damit jedes Fragment mit `AND` anschließen kann, trägt das `WHERE` die erste Bedingung, die immer gilt, in der Regel den Status, sonst `WHERE 1 = 1`. SQL, das leere Kriterien im Text neutralisiert, wird nicht verwendet, etwa `(:klasse = '' OR F.KLASSE = :klasse)` oder ein `COALESCE`, das nur eine leere Eingabe abfängt.
- **KONVENTION:** Eine lokale Variable für einen aufbereiteten Wert, etwa ein `LIKE`-Muster, steht im Zweig des Kriteriums direkt vor ihrem Fragment, nicht am Anfang der Methode.
