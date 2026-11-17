# Plan: Bereich `<bereich>` – <Thema>

| | |
|---|---|
| Anwendung | `<firma>.<app>` |
| Bounded Context | |
| Art | Aggregat-Bereich / Use-Case-Bereich |
| Änderung | neuer Bereich / Änderung an bestehendem Bereich |
| Status | Entwurf / freigegeben |
| Bestehende Modelle | *welche Modelle des Bereichs es schon gibt; „keine“ bei einem neuen Bereich* |

## Anforderung

*Zwei, drei Sätze in Fachsprache: was die Änderung leisten soll und für wen.*

## 1. Akzeptanzkriterien

| Nr | gegeben | wenn | dann |
|---|---|---|---|

## 2. `domain` – Werte und Aggregat

### Value Objects

| Name | Properties (Typ) | Gleichheit über | Regeln im Wert |
|---|---|---|---|

### Entities

*Je Entity eine Tabelle; die Wurzel des Aggregats zuerst. Bei einer Entity als Typ steht, ob sie Teil des Aggregats ist (Liste, Kind) oder ein Querverweis auf ein anderes Aggregat.*

| Property | Typ | Bezeichnung | Pflicht | Wertebereich (Länge, Bereich) | Schlüssel / eindeutig | Bedeutung |
|---|---|---|---|---|---|---|

## 3. `domain` – Status und Regeln

### Status

*Der erste Wert ist der Anfangszustand. Der Status, mit dem ein Objekt fachlich entfällt, ist als solcher benannt (Konventionen `domaenenmodell`, Löschen).*

| Wert | Kürzel | Bezeichnung | Bedeutung |
|---|---|---|---|

### Übergänge

*Jeder Übergang ist eine Service Method im `<Aggregat>Service`.*

| Name | von | nach | Bedingung | Meldung bei Ablehnung | Akzeptanzkriterium |
|---|---|---|---|---|---|

### Weitere Regeln und Berechnungen

| Regel | Ort (Entity, Value Object, Service) | Akzeptanzkriterium |
|---|---|---|

### Service Methods mit getrenntem Laden

*Nur Service Methods mit nicht trivialer Fachlogik: eine Methode lädt die Fakten, eine Methode ohne Komponentenaufrufe entscheidet (Konventionen `domaenenmodell`).*

| Methode, die lädt | Fakten und ihre Quelle | Methode, die entscheidet |
|---|---|---|

## 4. `domain` – Persistenz

| Entity | Tabelle | Schlüssel (Sequence) | Besonderheiten |
|---|---|---|---|

*Was der Checkout lädt und was der Check-in speichert.*

**Schemaänderung durch den Entwickler:** *welche Tabellen und Spalten angelegt oder geändert werden; „keine“.*

## 5. `read`

*Nur Abfragen, die einer Entscheidung, einem Service oder einer Berechnung dienen.*

| Lesemodell / Abfrage / Lese-Service | liefert | Quelle | verwendet von |
|---|---|---|---|

## 6. Abhängigkeiten zu anderen Bereichen

*Was der Bereich von anderen Bereichen, `sharedvalues` oder einem Gate braucht. Jede Zeile ist ein Import, den die Konventionen `anwendungsaufbau` erlauben müssen.*

| braucht | aus Modell | als (Querverweis, gelesener Fakt, Service, Command) | wozu |
|---|---|---|---|

## 7. `tests`

| Akzeptanzkriterium | Testmethode | Art (ohne Datenbank / mit Datenbank / Command) | Testdaten |
|---|---|---|---|

**Tests für Commands beauftragt:** *ja / nein; ohne Auftrag keine (Konventionen `allgemein`).*

**Voraussetzungen:** *Test-`OFXConfig` in `base`, `CS` als Komponente auffindbar, Service `TestDaten` – vorhanden oder Teil dieses Plans.*

## 8. `unit.read` und `unit`

### Suchen

| Suche | Kriterien | Spalten | Ergebnis (Entity / DTO) | schließt Status aus |
|---|---|---|---|---|

### Commands

| Command | Typ | Parameter | aufgerufen aus (Hauptmenü, Menü eines Page Pane oder einer Tabelle, Command) | bedienbar wenn (`generally enabled` / Precondition im `command init`) | Pages | Abschluss ruft (Service Method) |
|---|---|---|---|---|---|---|

### DTOs, die nur einem Command dienen

| DTO | Command | Properties |
|---|---|---|

## 9. `app` und Rechte

| Command | Menüeintrag | Rollen `CAN_OPEN_RW` | Rollen `CAN_OPEN_RO` |
|---|---|---|---|

### Batchjobs

| `consumer/producer pair` | Producer liefert | Consumer verarbeitet mit | Zeitplan (`CRON` / `DELAY`), Anzahl Consumer | bei technischem Fehler |
|---|---|---|---|---|

## 10. Modelle und Roots

*Jede Root, die entsteht oder sich ändert, mit ihrem Modell. Unveränderte Roots stehen nicht hier. Ein Modell, das neu angelegt wird, trägt den Zusatz „(neu)“.*

| Modell | Root | Konzept | neu / geändert | aus Abschnitt |
|---|---|---|---|---|

## 11. Abweichungen von Konventionen

*Leer heißt: keine. Jede Zeile braucht die Entscheidung des Nutzers; Abweichungen, die das Projekt festlegt, tragen als Grund „Projekt“.*

| Konvention | Abweichung | Grund |
|---|---|---|

## 12. Offene Fragen

*Alle `KLÄREN:`-Punkte aus den Abschnitten oben. Vor der Freigabe leer.*

## 13. Annahmen

*Alle `ANNAHME:`-Punkte aus den Abschnitten 8 und 9. Sie verhindern die Freigabe nicht.*

## 14. Reihenfolge der Umsetzung

*Von innen nach außen: Voraussetzungen in `base`; `domain` und `read`; Halt, bis der Entwickler das Datenbankschema erstellt hat; die Tests von `domain` und `read`; dann `unit.read` und `unit`; dann `app`.*

1.
