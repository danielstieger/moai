## Verbindliche Konventionen für das Domänenmodell

### Aggregate und Invarianten

- **KONVENTION:** Invarianten gehören zum Aggregat und werden am vollständig geladenen Aggregat geprüft. Reicht eine Regel über das Aggregat hinaus, wird zuerst geprüft, ob das Aggregat richtig geschnitten ist. Bleibt die Regel aggregatübergreifend, liegt sie in einem Service, der die nötigen Fakten liest.
- **KONVENTION:** Ein Aggregat referenziert ein anderes nur als Querverweis. Wird das referenzierte Aggregat gebraucht, wird es read-only geladen; so ist es gegen versehentliche Änderungen geschützt. Verändert wird es ausschließlich über seinen eigenen `<Aggregat>Service`, und es wird nie mit dem referenzierenden Aggregat gespeichert.
- **KONVENTION:** Jeder wesentliche fachliche Zustandsübergang eines Aggregats, ein Statuswechsel oder ein anderer Übergang mit eigener fachlicher Bedeutung wie „Rechnung stornieren“, ist eine eigene Service Method im `<Aggregat>Service` des `domain`, benannt nach dem fachlichen Vorgang, etwa `RechnungService.freigeben(rechnung)`. Sie prüft die Voraussetzungen mit Preconditions und setzt danach den Status und die davon abhängigen Werte. Commands und andere Services führen diesen Übergang nicht selbst aus, sondern rufen die Methode auf.

### Service und Aggregat

Entities modellieren die Datenstruktur, Services das Verhalten; beides sind Sichten auf dasselbe Aggregat.

- **KONVENTION:** Der `<Aggregat>Service` kapselt alle fachlich bedeutsamen Veränderungen eines Aggregats. Am Aggregat selbst stehen nur einfache Prädikate und Helfer zum Umgang mit Listen; wichtige Fachlogik liegt im Service. Value Objects kapseln dagegen die Operationen ihres Werts, etwa die Prüfung, ob ein Datum innerhalb eines Stichtags mit Toleranz liegt. Die Sprache erzwingt diese Kapselung nicht: Properties einer Entity sind auch von Commands und anderen Services aus setzbar. Wer einen Command oder Service ändert, prüft deshalb, dass fachlich bedeutsame Veränderungen über den `<Aggregat>Service` laufen und nicht direkt an der Entity.
- **KONVENTION:** Service Methods sind fachliche Operationen wie `freigeben(rechnung)` oder `stornieren(rechnung)`, keine Wrapper um einzelne Properties. Eine kurze Schnittstelle verbirgt Prüfungen, Statuswechsel und abhängige Werte.
- **KONVENTION:** Enthält eine Service Method nicht triviale Fachlogik, werden Datenzugriff und Fachlogik getrennt: Eine Service Method lädt die benötigten Fakten, bei mehreren gebündelt in einem DTO im `read`, und übergibt sie einer Service Method ohne Komponentenaufrufe, die nur mit ihren Parametern und dem Aggregat arbeitet. Die Namen zeigen den Unterschied, etwa `freigeben(rechnung)` und `freigabeEntscheiden(rechnung, fakten)`. Commands rufen die ladende Methode auf. Die Fachlogik lässt sich so ohne Testdaten in der Datenbank testen. Eine Service Method mit einfacher Fachlogik, etwa einer Precondition und einem Statuswechsel, bleibt eine Methode.

### Eingabeprüfungen und fachliche Prüfungen

- **KONVENTION:** Eingabeprüfungen an einem DTO, das zwischen Oberfläche und Aggregat liegt, sind CheapCode und ersetzen nie die fachliche Prüfung. Jede Geschäftsregel steht im Service oder am Aggregat, und der Service prüft sie auch dann, wenn das DTO sie bereits geprüft hat.
- **KONVENTION:** Pflichteingaben und Wertegrenzen der Eingabe regeln die DataUX-Delegates zusammen mit `LENGTH` und `RANGE` an den Properties des DTOs. Eine Precondition am DTO wird nur für Eingabeprüfungen modelliert, die sich damit nicht ausdrücken lassen, etwa Abhängigkeiten zwischen Feldern.

### Löschen

- **KONVENTION:** Fachliche Objekte werden nicht physisch gelöscht. Muss ein Objekt fachlich entfallen, auch ein Teil eines Aggregats wie eine Position, erhält es einen Status, etwa „storniert“ oder „gelöscht“. Abfragen und Lesemodelle schließen diesen Status aus. `delete with` ist technischen Daten vorbehalten.

### Werte

- **KONVENTION:** Value Objects sind erwünscht. Ein zusammengesetzter fachlicher Wert (Compound Value), etwa Geldbetrag, Zeitraum, Anschrift oder ein Stichtag mit Toleranz, wird als Value Object modelliert und nicht als einzelne Properties der Entity. Einzelne Properties bleiben nur, wenn ihre Bestandteile auch einzeln einen fachlichen Sinn ergeben.
- **KONVENTION:** Ein Value Object wird nach dem Erzeugen nicht über Setter verändert. Eine Änderung erzeugt mit einer `with`-Methode oder einem Konstruktor ein neues Value Object, das der Property zugewiesen wird. Nur so wird die besitzende Entity dirty und die Änderung gespeichert.
- **KONVENTION:** Statische Methoden an einem Value Object sind erwünscht, wenn sie zum Wert gehören und ohne Infrastruktur auskommen: Fabrikmethoden wie `Geldbetrag.von(betrag, waehrung)`, benannte Konstanten wie `Geldbetrag.NULL()`, Prädikate und Prüfungen wie `Zeitraum.istGueltig(von, bis)` sowie Operationen über mehrere Werte wie `Geldbetrag.summe(betraege)`, `min` und `max`. Sie liefern neue Werte oder Antworten und werfen keine fachlichen Fehler; die fachliche Prüfung bleibt im Service. Konstanten werden als Methode modelliert, nicht als statisches Feld.

### Fehlende Werte

- **KONVENTION:** Ein `string` ist nie `null`; „kein Wert“ ist der leere String. Fachlicher Code prüft Strings (falls notwendig) auf Leere und nicht auf `null` und setzt einen String nicht auf `null`. Ausgenommen ist ein String, der bewusst optional geführt wird, etwa als Kriterium eines `optional`-Filters, das mit `null` entfällt.
- **KONVENTION:** `java.util.Optional` wird nicht verwendet. Ein fehlender Wert ist `null` beziehungsweise der leere String.
