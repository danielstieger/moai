## Allgemeine verbindliche Konventionen

- **KONVENTION:** Unsere Ubiquitous Language ist Deutsch. Alles, was Fachlichkeit in der Software ausdrückt, wird konsistent mit deutschen Fachbegriffen benannt – insbesondere Namespaces, Datenmodelle, Services und Methoden.
- **KONVENTION:** Das Datenbankschema erstellt der Entwickler in MPS aus den `EntityMapping`s der Persistence Descriptions. Agenten erzeugen oder ändern keine Datenbankschemata.
- **KONVENTION:** Eine Run Configuration, die ein `AppUI Module` mit `org.modellwerkstatt.fx8forms` direkt in MPS startet, erhält den VM-Parameter `--enable-native-access=ALL-UNNAMED`.
- **KONVENTION:** Eine Anwendung wird von innen nach außen aufgebaut: zuerst der ExpensiveCode (`domain`, `read`) mit seinen Tests, danach der CheapCode (`unit`, `unit.read`, `app`). Ein Command setzt erst auf Services auf, deren Tests laufen.
- **KONVENTION:** Die Tests des ExpensiveCode leiten sich aus den fachlichen Anforderungen der Spezifikation ab, etwa aus Akzeptanzkriterien und Geschäftsregeln.
- **KONVENTION:** Tests für CheapCode werden nur auf ausdrücklichen Auftrag erstellt.

### Fehlende Werte

- **KONVENTION:** Ein `string` ist nie `null`; „kein Wert“ ist der leere String. Fachlicher Code prüft Strings (falls notwendig) auf Leere und nicht auf `null` und setzt einen String nicht auf `null`. Ausgenommen ist ein String, der bewusst optional geführt wird, etwa als Kriterium eines `optional`-Filters, das mit `null` entfällt.
- **KONVENTION:** Keine vorsorglichen `null`-Prüfungen. `isEmpty`, `isNotEmpty`, `:eq:`, `:ne:` und die Collections-Operationen auf Listen und Maps (`size`, `where`, `select`, `any`, `contains`, `forEach` …) sind null-sicher und werden nicht mit `!= null` abgesichert. Auf `null` geprüft wird nur, wo `null` fachlich vorkommen kann: bei Datum/Zeit, Value Objects und Referenzen sowie beim Ergebnis von `first`, `findFirst` und `map[k]`.
- **KONVENTION:** `java.util.Optional` wird nicht verwendet. Ein fehlender Wert ist `null` beziehungsweise der leere String.
