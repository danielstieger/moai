# Plan: Bereich `<bereich>`

| | |
|---|---|
| Anwendung | `<firma>.<app>` |
| Bounded Context | |
| Art | Aggregat-Bereich / Use-Case-Bereich |
| Status | Entwurf / freigegeben |
| Bestehende Modelle | *welche Modelle des Bereichs es schon gibt; „keine“ bei einem neuen Bereich* |

## Anforderung

*Zwei, drei Sätze in Fachsprache: was der Bereich leisten soll und für wen.*

## 1. Akzeptanzkriterien

| Nr | gegeben | wenn | dann |
|---|---|---|---|

## 2. `domain` – Werte und Aggregat

### Value Objects

| Name | Properties (Typ) | Gleichheit über | Regeln im Wert |
|---|---|---|---|

### Entities

*Je Entity eine Tabelle; die Wurzel des Aggregats zuerst.*

| Property | Typ | Pflicht | Schlüssel | Bedeutung |
|---|---|---|---|---|

## 3. `domain` – Status und Regeln

### Status

| Wert | Kürzel | Bezeichnung | Bedeutung |
|---|---|---|---|

### Übergänge

| Name | von | nach | Bedingung | Meldung bei Ablehnung |
|---|---|---|---|---|

### Weitere Regeln und Berechnungen

| Regel | Ort (Entity, Value Object, Service) | Akzeptanzkriterium |
|---|---|---|

## 4. `domain` – Persistenz

| Entity | Tabelle | Schlüssel | Besonderheiten |
|---|---|---|---|

*Was der Checkout lädt und was der Check-in speichert.*

## 5. `read`

*Nur Abfragen, die einer Entscheidung, einem Service oder einer Berechnung dienen.*

| Lesemodell / Abfrage / Lese-Service | liefert | Quelle | verwendet von |
|---|---|---|---|

## 6. `tests`

| Akzeptanzkriterium | Testmethode | Testdaten |
|---|---|---|

## 7. `unit.read` und `unit`

### Suchen

| Suche | Kriterien | Spalten | Ergebnis (Entity / DTO) |
|---|---|---|---|

### Commands

| Command | Typ | Parameter | Pages | Abschluss |
|---|---|---|---|---|

### DTOs, die nur einem Command dienen

| DTO | Command | Properties |
|---|---|---|

## 8. `app` und Rechte

| Command | Menüeintrag | Rollen |
|---|---|---|

## 9. Abweichungen von Konventionen

*Leer heißt: keine. Jede Zeile braucht die Entscheidung des Nutzers.*

| Konvention | Abweichung | Grund |
|---|---|---|

## 10. Offene Fragen

*Alle `KLÄREN:`-Punkte aus den Abschnitten oben. Vor der Freigabe leer.*

## 11. Reihenfolge der Umsetzung

*Von innen nach außen: `domain` und `read` mit ihren Tests, dann `unit.read` und `unit`, dann `app`.*

1.
