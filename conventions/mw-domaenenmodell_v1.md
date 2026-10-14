## Verbindliche Konventionen für das Domänenmodell

### Aggregate und Invarianten

- **KONVENTION:** Invarianten gehören zum Aggregat und werden am vollständig geladenen Aggregat geprüft. Reicht eine Regel über das Aggregat hinaus, wird zuerst geprüft, ob das Aggregat richtig geschnitten ist. Bleibt die Regel aggregatübergreifend, liegt sie in einem Service, der die nötigen Fakten liest.
- **KONVENTION:** Jeder wesentliche fachliche Zustandsübergang eines Aggregats, ein Statuswechsel oder ein anderer Übergang mit eigener fachlicher Bedeutung wie „Rechnung stornieren“, ist eine eigene Service Method im `<Aggregat>Service` des `domain`, benannt nach dem fachlichen Vorgang, etwa `RechnungService.freigeben(rechnung)`. Sie prüft die Voraussetzungen mit Preconditions und setzt danach den Status und die davon abhängigen Werte. Commands und andere Services führen diesen Übergang nicht selbst aus, sondern rufen die Methode auf.

### Service und Aggregat

Entities modellieren die Datenstruktur, Services das Verhalten; beides sind Sichten auf dasselbe Aggregat.

- **KONVENTION:** Der `<Aggregat>Service` kapselt alle fachlich bedeutsamen Veränderungen eines Aggregats. Am Aggregat selbst stehen nur einfache Prädikate und Helfer zum Umgang mit Listen; wichtige Fachlogik liegt im Service. Die Sprache erzwingt diese Kapselung nicht: Properties einer Entity sind auch von Commands und anderen Services aus setzbar. Wer einen Command oder Service ändert, prüft deshalb, dass fachlich bedeutsame Veränderungen über den `<Aggregat>Service` laufen und nicht direkt an der Entity.
- **KONVENTION:** Service Methods sind fachliche Operationen wie `freigeben(rechnung)` oder `stornieren(rechnung)`, keine Wrapper um einzelne Properties. Eine kurze Schnittstelle verbirgt Prüfungen, Statuswechsel und abhängige Werte.
- **KONVENTION:** Enthält eine Service Method nicht triviale Fachlogik, werden Datenzugriff und Fachlogik getrennt: Eine Service Method lädt die benötigten Fakten, bei mehreren gebündelt in einem DTO im `read`, und übergibt sie einer Service Method ohne Komponentenaufrufe, die nur mit ihren Parametern und dem Aggregat arbeitet. Die Namen zeigen den Unterschied, etwa `freigeben(rechnung)` und `freigabeEntscheiden(rechnung, fakten)`. Commands rufen die ladende Methode auf. Die Fachlogik lässt sich so ohne Testdaten in der Datenbank testen. Eine Service Method mit einfacher Fachlogik, etwa einer Precondition und einem Statuswechsel, bleibt eine Methode.

### Eingabeprüfungen und fachliche Prüfungen

- **KONVENTION:** Eingabeprüfungen an einem DTO, das zwischen Oberfläche und Aggregat liegt, sind CheapCode und ersetzen nie die fachliche Prüfung. Jede Geschäftsregel steht im Service oder am Aggregat, und der Service prüft sie auch dann, wenn das DTO sie bereits geprüft hat.
- **KONVENTION:** Pflichteingaben und Wertegrenzen der Eingabe regeln die DataUX-Delegates zusammen mit `LENGTH` und `RANGE` an den Properties des DTOs. Eine Precondition am DTO wird nur für Eingabeprüfungen modelliert, die sich damit nicht ausdrücken lassen, etwa Abhängigkeiten zwischen Feldern.

### Werte

- **KONVENTION:** Ein `string` ist nie `null`; „kein Wert“ ist der leere String. Fachlicher Code prüft Strings (falls notwendig) auf Leere und nicht auf `null` und setzt einen String nicht auf `null`. Ausgenommen ist ein String, der bewusst optional geführt wird, etwa als Kriterium eines `optional`-Filters, das mit `null` entfällt.
