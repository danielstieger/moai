## Verbindliche Konventionen für das Domänenmodell

### Aggregate und Invarianten

- **KONVENTION:** Invarianten gehören zum Aggregat und werden am vollständig geladenen Aggregat geprüft. Reicht eine Regel über das Aggregat hinaus, wird zuerst geprüft, ob das Aggregat richtig geschnitten ist. Bleibt die Regel aggregatübergreifend, liegt sie in einem Service, der die nötigen Fakten liest.
- **KONVENTION:** Jeder wesentliche fachliche Zustandsübergang eines Aggregats, ein Statuswechsel oder ein anderer Übergang mit eigener fachlicher Bedeutung wie „Rechnung stornieren“, ist eine eigene Service Method im `<Aggregat>Service` des `domain`, benannt nach dem fachlichen Vorgang, etwa `RechnungService.freigeben(rechnung)`. Sie prüft die Voraussetzungen mit Preconditions und setzt danach den Status und die davon abhängigen Werte. Commands und andere Services führen diesen Übergang nicht selbst aus, sondern rufen die Methode auf.

### Werte

- **KONVENTION:** Ein `string` ist nie `null`; „kein Wert“ ist der leere String. Fachlicher Code prüft Strings (falls notwendig) auf Leere und nicht auf `null` und setzt einen String nicht auf `null`. Ausgenommen ist ein String, der bewusst optional geführt wird, etwa als Kriterium eines `optional`-Filters, das mit `null` entfällt.
