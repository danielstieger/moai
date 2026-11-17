# Plan: Bereich `rechnung` – Stornieren

| | |
|---|---|
| Anwendung | `org.beispiel.faktura` |
| Bounded Context | einer, ohne eigenes Segment |
| Art | Aggregat-Bereich |
| Änderung | Änderung an bestehendem Bereich |
| Status | freigegeben |
| Bestehende Modelle | `rechnung.domain`, `rechnung.tests`, `rechnung.unit.read`, `rechnung.unit` |

## Anforderung

Die Buchhaltung kann eine Rechnung stornieren, solange noch keine Zahlung auf sie gebucht ist. Eine stornierte Rechnung bleibt erhalten, erscheint aber nicht mehr in der Rechnungssuche.

## 1. Akzeptanzkriterien

| Nr | gegeben | wenn | dann |
|---|---|---|---|
| 1 | eine erfasste oder freigegebene Rechnung ohne Zahlung | sie storniert wird | hat sie den Status Storniert und den Zeitpunkt der Stornierung |
| 2 | eine Rechnung mit gebuchter Zahlung | sie storniert wird | wird abgelehnt: „Die Rechnung hat bereits Zahlungen und kann nicht storniert werden.“ |
| 3 | eine stornierte Rechnung | sie storniert wird | wird abgelehnt: „Die Rechnung ist bereits storniert.“ |

## 2. `domain` – Werte und Aggregat

### Value Objects

unverändert

### Entities

`Rechnung` (Wurzel)

| Property | Typ | Bezeichnung | Pflicht | Wertebereich (Länge, Bereich) | Schlüssel / eindeutig | Bedeutung |
|---|---|---|---|---|---|---|
| `storniertAm` | `DateTime` | Storniert am | nein | – | – | Zeitpunkt der Stornierung; leer, solange nicht storniert |

## 3. `domain` – Status und Regeln

### Status

`RechnungStatus`; Storniert ist der Status, mit dem eine Rechnung fachlich entfällt.

| Wert | Kürzel | Bezeichnung | Bedeutung |
|---|---|---|---|
| `STORNIERT` | S | Storniert | Rechnung ist storniert |

### Übergänge

| Name | von | nach | Bedingung | Meldung bei Ablehnung | Akzeptanzkriterium |
|---|---|---|---|---|---|
| `stornieren` | `ERFASST`, `FREIGEGEBEN` | `STORNIERT` | Status ist nicht `STORNIERT` | „Die Rechnung ist bereits storniert.“ | 1, 3 |
| | | | bezahlter Betrag ist 0 | „Die Rechnung hat bereits Zahlungen und kann nicht storniert werden.“ | 2 |

### Weitere Regeln und Berechnungen

| Regel | Ort (Entity, Value Object, Service) | Akzeptanzkriterium |
|---|---|---|
| Der Übergang setzt `storniertAm` auf den übergebenen Zeitpunkt | `RechnungService` | 1 |

### Service Methods mit getrenntem Laden

| Methode, die lädt | Fakten und ihre Quelle | Methode, die entscheidet |
|---|---|---|
| `stornieren(rechnung, zeitpunkt)` | bezahlter Betrag aus `ZahlungsLeseRepo.summeZuRechnung(rechnung.id)` | `stornierungEntscheiden(rechnung, bezahlterBetrag, zeitpunkt)` |

## 4. `domain` – Persistenz

| Entity | Tabelle | Schlüssel (Sequence) | Besonderheiten |
|---|---|---|---|
| `Rechnung` | `RECHNUNG` | unverändert | neue Spalte `STORNIERT_AM` |

Checkout und Check-in unverändert.

**Schemaänderung durch den Entwickler:** Spalte `STORNIERT_AM` in `RECHNUNG`.

## 5. `read`

entfällt: Der Bereich hat kein `read`; der bezahlte Betrag kommt aus `zahlung.read`.

## 6. Abhängigkeiten zu anderen Bereichen

| braucht | aus Modell | als (Querverweis, gelesener Fakt, Service, Command) | wozu |
|---|---|---|---|
| `ZahlungsLeseRepo.summeZuRechnung` | `org.beispiel.faktura.zahlung.read` (vorhanden) | gelesener Fakt | Bedingung des Übergangs `stornieren` |

## 7. `tests`

| Akzeptanzkriterium | Testmethode | Art (ohne Datenbank / mit Datenbank / Command) | Testdaten |
|---|---|---|---|
| 1 | `Rechnung ohne Zahlung stornieren` | ohne Datenbank | freigegebene Rechnung, bezahlter Betrag 0 |
| 2 | `Rechnung mit Zahlung nicht stornieren` | ohne Datenbank | freigegebene Rechnung, bezahlter Betrag 50,00 |
| 3 | `Stornierte Rechnung nicht erneut stornieren` | ohne Datenbank | stornierte Rechnung |
| 1 | `Stornierte Rechnung wird gespeichert` | mit Datenbank | `TestDaten.erzeugeRechnung`, ohne Zahlung |

**Tests für Commands beauftragt:** nein.

**Voraussetzungen:** vorhanden.

## 8. `unit.read` und `unit`

### Suchen

| Suche | Kriterien | Spalten | Ergebnis (Entity / DTO) | schließt Status aus |
|---|---|---|---|---|
| `Rechnungen suchen` | unverändert | unverändert | Entity | `STORNIERT` (neu) |

### Commands

| Command | Typ | Parameter | aufgerufen aus (Hauptmenü, Menü eines Page Pane oder einer Tabelle, Command) | bedienbar wenn (`generally enabled` / Precondition im `command init`) | Pages | Abschluss ruft (Service Method) |
|---|---|---|---|---|---|---|
| `Rechnung stornieren` | `GRAPH_OWNER_CMD(modal)` | selektierte Rechnung, Checkout über ihren Schlüssel | Menü der Ergebnistabelle von `Rechnungen suchen` | `generally enabled`: Status ist `ERFASST` oder `FREIGEGEBEN` | eine Page „Rechnung stornieren?“ mit `DISABLED` `Delegate Form` | `RechnungService.stornieren` |

ANNAHME: Der Menüeintrag steht im `Submenu` der Ergebnistabelle nach „Rechnung bearbeiten“.

ANNAHME: Die stornierte Rechnung bleibt bis zum nächsten „Aktualisieren“ in der Ergebnisliste sichtbar.

### DTOs, die nur einem Command dienen

entfällt: Der Command zeigt die Rechnung selbst.

## 9. `app` und Rechte

| Command | Menüeintrag | Rollen `CAN_OPEN_RW` | Rollen `CAN_OPEN_RO` |
|---|---|---|---|
| `Rechnung stornieren` | keiner im Hauptmenü | `Buchhaltung` | – |

### Batchjobs

entfällt: keine Hintergrundverarbeitung.

## 10. Modelle und Roots

| Modell | Root | Konzept | neu / geändert | aus Abschnitt |
|---|---|---|---|---|
| `…rechnung.domain` | `Rechnung` | `Entity` | geändert | 2, 3 |
| `…rechnung.domain` | `RechnungPersistenz` | `Persistence Description` | geändert | 4 |
| `…rechnung.domain` | `RechnungService` | `Service` | geändert | 3 |
| `…rechnung.tests` | `RechnungTests` | `OFXTestSuit` | geändert | 7 |
| `…rechnung.unit.read` | `RechnungSucheRepo` | `Repository` | geändert | 8 |
| `…rechnung.unit` | `Rechnung stornieren` | `Command` | neu | 8, 9 |
| `…rechnung.unit` | `RechnungStornierenPane` | `Page Pane` | neu | 8 |
| `…rechnung.unit` | `RechnungenSuchenErgebnisPane` | `Page Pane` | geändert | 8 |

## 11. Abweichungen von Konventionen

| Konvention | Abweichung | Grund |
|---|---|---|

## 12. Offene Fragen

keine

## 13. Annahmen

- Der Menüeintrag steht im `Submenu` der Ergebnistabelle nach „Rechnung bearbeiten“.
- Die stornierte Rechnung bleibt bis zum nächsten „Aktualisieren“ in der Ergebnisliste sichtbar.

## 14. Reihenfolge der Umsetzung

1. `domain`: Status `STORNIERT`, Property `storniertAm`, Mapping der Spalte.
2. `domain`: `RechnungService.stornieren` und `stornierungEntscheiden`.
3. `tests`: die drei Tests ohne Datenbank.
4. Halt: Der Entwickler legt die Spalte `STORNIERT_AM` an.
5. `tests`: `Stornierte Rechnung wird gespeichert`.
6. `unit.read`: Suche schließt `STORNIERT` aus.
7. `unit`: Command `Rechnung stornieren` mit Page Pane; Menüeintrag in der Ergebnistabelle.
