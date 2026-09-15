## Sessions, Commands und Transaktionen

> Arbeitsstand: Die folgenden Abläufe stammen aus der Beschreibung des Sprachverantwortlichen. Die vier Bezeichnungen wurden durch die Spracheingabe nicht eindeutig wiedergegeben. Die Zeilen beschreiben vorläufig vier Verhaltensweisen und legen keine technischen Typnamen fest.

| Beschriebener Typ | Session und Interaktion | Schreiben und Commit |
| --- | --- | --- |
| SEARCH Command | Startet eine Session im Hintergrund. Lädt Daten anhand von Filtern, kann sie aufbereiten und über mehrere Pages beziehungsweise Views anzeigen. | Die Session darf nicht committed werden; Änderungen dürfen über diese Session nicht in die Datenbank geschrieben werden. |
| GRAPH_OWNER Command | Startet eine eigene Session. Lädt Daten und bereitet sie auf; Benutzer können sie auch über die Oberfläche bearbeiten. | Zum Abschluss werden registrierte Session Operations innerhalb einer Datenbanktransaktion ausgeführt und committed. Der genaue Auslöser ist noch zu klären. |
| GRAPH_EDIT Command | Startet keine neue Session, sondern übernimmt eine bestehende Session eines Performers. Dient der Modellierung von Benutzerinteraktion. | Eigene Abschluss- und Commit-Befugnisse sind noch zu klären. |
| MODAL_GRAPH_OWNER | Modale Benutzerinteraktion, vergleichbar mit einem Dialogfenster. | Session-Zuordnung und Transaktionsverhalten sind noch zu bestätigen. |

Beim ändernden Command registriert der Anwendungsentwickler auszuführende Operationen auf einem **Session Operation Stack**. Zum beschriebenen Abschluss wird eine Datenbanktransaktion gestartet, die registrierten Operationen werden ausgeführt und die Transaktion wird committed. Die Reihenfolge der Abarbeitung, das Verhalten bei Fehlern und Abbruch sowie der genaue Abschlussmechanismus sind noch offen; aus dem Wort „Stack“ wird keine Ausführungsreihenfolge abgeleitet.

Die beschriebene Session begleitet Laden und Benutzerinteraktion. Die Datenbanktransaktion zur Ausführung der Session Operations beginnt dagegen erst beim genannten Abschluss. Session-Lebensdauer und diese Transaktionsdauer sind daher getrennt zu dokumentieren. Über weitere Transaktionen beim Laden trifft diese Beschreibung keine Aussage.



# Applikationsbeispiel Rechnungsverwaltung.

Ein kleines Gesamtbeispiel wäre: **Rechnungen suchen, eine Rechnung öffnen, Positionen bearbeiten und die Änderungen gemeinsam speichern.** Die folgenden Namen sind beispielhaft; es handelt sich um eine fachliche Skizze, noch nicht um ausführbare DSL-Syntax.

**1. Fachliches Modell – `org.modellwerkstatt.objectflow`**

| Element       | Beispiel             | Aufgabe                                                                             |
| ------------- | -------------------- | ----------------------------------------------------------------------------------- |
| `Entity`      | `Rechnung`           | Enthält Rechnungsnummer, Rechnungsdatum und eine Liste von Rechnungspositionen      |
| `Entity`      | `Rechnungsposition`  | Enthält Positionsnummer, Beschreibung, Menge und Einzelpreis                        |
| `ValueObject` | `Geldbetrag`         | Fasst Betrag und Währung zusammen                                                   |
| `DTO`         | `RechnungsSuchzeile` | Enthält Rechnungs-ID, Rechnungsnummer, Datum und Gesamtbetrag für die Suchübersicht |
| `Service`     | `RechnungsService`   | Berechnet Positionswerte und Rechnungssumme und prüft fachliche Regeln              |

Als einfache Beispielregeln gelten: Die Menge muss positiv sein, Einzelpreise dürfen nicht negativ sein und alle Positionen verwenden dieselbe Währung. Die Rechnungssumme ergibt sich aus der Summe der Positionswerte. Steuern und Rundungsregeln lassen wir in diesem ersten Beispiel weg.

**2. Persistenz – `org.modellwerkstatt.manmap`**

Eine `PersistenceDescription` enthält die Mappings für `Rechnung` und `Rechnungsposition`. Die Positionstabelle besitzt eine Zuordnung zur jeweiligen Rechnung.

Das `RechnungsRepository` übernimmt drei Aufgaben:

| Operation          | Verhalten                                                                                                                               |
| ------------------ | --------------------------------------------------------------------------------------------------------------------------------------- |
| Rechnungen suchen  | Führt eine SQL-Abfrage mit Suchfiltern aus. Ein Mapper überführt die Ergebnismenge in `RechnungsSuchzeile`-DTOs.                        |
| Rechnung laden     | Lädt den Rechnungskopf und anschließend explizit die zugehörigen Positionen. Stellt daraus den vollständigen Rechnungsgraphen zusammen. |
| Rechnung speichern | Speichert den Rechnungskopf sowie neue, geänderte und entfernte Positionen entsprechend den modellierten Persistenzoperationen.         |

Damit bleibt ausdrücklich sichtbar, wann der vollständige Rechnungsgraph geladen wird. Die Suche benötigt zunächst nur die Daten für die Übersicht.

**3. Anwendungsfälle – `org.modellwerkstatt.objectflow`**

| Beispiel-Command              | Typ          | Aufgabe                                                                                                                          |
| ----------------------------- | ------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| `RechnungenSuchen`            | `Search`     | Lädt anhand von Filtern die Suchergebnisse und zeigt sie an. Seine eigene Session darf nicht committed werden.                   |
| `RechnungBearbeiten`          | `GraphOwner` | Übernimmt die ausgewählte Rechnungs-ID als Parameter, startet eine eigene Session und lädt den Rechnungsgraphen zur Bearbeitung. |
| `RechnungspositionBearbeiten` | `GraphEdit`  | Verwendet die bestehende Session des aufrufenden Performers und ermöglicht die Bearbeitung einer Position.                       |

Für dieses Beispiel braucht es keinen `ModalGraphOwner`.

Während der Bearbeitung verändert der Benutzer die geladenen Daten. Die fachliche Prüfung und Summenberechnung liegen im `RechnungsService`. Die erforderlichen Speicheroperationen werden auf dem **Session Operation Stack** registriert. Beim dafür vorgesehenen Abschluss des `GraphOwner` wird eine Datenbanktransaktion gestartet, die registrierten Operationen werden ausgeführt und anschließend committed.

**4. Benutzeroberfläche – `org.modellwerkstatt.dataux`**

| Element                       | Inhalt                                                                       |
| ----------------------------- | ---------------------------------------------------------------------------- |
| `AppUiModule`                 | Einstieg in die Rechnungsverwaltung mit einem Menüeintrag zur Rechnungssuche |
| `Table`                       | Suchübersicht mit Rechnungsnummer, Datum und Gesamtbetrag                    |
| `DelegateForm`                | Bearbeitung des Rechnungskopfs                                               |
| `Table`                       | Positionen der geöffneten Rechnung                                           |
| `DelegateForm`                | Bearbeitung einer einzelnen Position                                         |
| `GridLayout` oder `TabLayout` | Zusammenstellung von Rechnungskopf und Positionsübersicht                    |
| `PagePane`                    | Wiederverwendbarer Seiteninhalt für die Rechnungsbearbeitung                 |

Die Oberflächen beschreiben Datenbindungen, Darstellung und angebotene Interaktionen. Die Berechnung der Rechnungssumme und die fachlichen Prüfungen bleiben in der Geschäftslogik.

**5. Konfiguration und Ausführung**

Die `OFXConfig` konfiguriert unter anderem Repository und Service und legt über die AppFactories die Laufzeit fest. Für einen Desktop-Arbeitsplatz könnte die Anwendung mit `org.modellwerkstatt.fx8forms` oder `org.modellwerkstatt.turkuforms` ausgeführt werden.

Nach der Modellierung erfolgt ein vollständiger Rebuild der Applikation in MPS. Anschließend wird Ant auf der Konsole mit den passenden projektspezifischen Targets ausgeführt.

Eine `OFXTestSuit` sollte beispielsweise prüfen, dass zwei Positionen mit `2 × 50 EUR` und `1 × 30 EUR` eine Rechnungssumme von `130 EUR` ergeben und eine Position mit Menge `0` fachlich abgelehnt wird.

Damit wird auch **ExpensiveCode und CheapCode** greifbar: Rechnungsstruktur, Berechnungen, Prüfungen und korrektes Speichern bilden den sorgfältig abzusichernden fachlichen Kern. Spaltenanordnung, Formularlayout und Menügestaltung lassen sich über kurze Feedbackzyklen anpassen.

Für eine präzise Ablaufbeschreibung fehlt uns noch ein Detail: **Registriert der `GraphOwner` bei euch typischerweise eine gemeinsame Speicheroperation für den Rechnungsgraphen, oder werden einzelne Operationen während der Bearbeitung gesammelt?**
