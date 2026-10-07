## Verbindliche Konventionen für Tests

### Testdaten mit einer Custom Session anlegen

Die Session eines `Simple Test` wird am Testende nicht committet. Testdaten, die für einen Test in der Datenbank stehen müssen, werden deshalb über eine eigene Custom Session angelegt und dort committet.

- **KONVENTION:** Der Service `CS` aus der Solution `org.modellwerkstatt.wbkit` liefert mit `CREATE()` eine neue Custom Session und committet mit `COMMIT()` die Session des aktuellen Kontexts samt der registrierten Session-Operationen. Die Anwendung legt `CS` nicht selbst an.
- **KONVENTION:** Alle Methoden zum Anlegen von Testdaten liegen im Service `TestDaten` des jeweiligen `tests`-Modells. Eine solche Methode baut den Objektgraphen auf, registriert das Speichern mit `session operation add` und schließt mit `#CS.COMMIT()` ab.
- **KONVENTION:** Der Test ruft Methoden zum Anlegen von Testdaten mit `#+ with #CS.CREATE()` auf. Innerhalb der Methode ist `session` damit die Custom Session; die Session des Tests bleibt unberührt.
- **KONVENTION:** Persistierte Ergebnisse werden in einer frischen Custom Session zurückgelesen, etwa `#+ with #CS.CREATE() RechnungsRepo.get(id)`.

```objectflow
component TestDaten

  public Rechnung erzeugeRechnung(Kunde kunde) {
    final Rechnung rechnung = new Rechnung();
    rechnung.kunde = kunde;
    session operation add # RechnungsRepo.checkin(rechnung)
      // "Testdaten Rechnung";
    #CS.COMMIT();
    return rechnung;
  }
```

Aufruf im Test:

```objectflow
Kunde mueller = #+ with #CS.CREATE() TestDaten.kunde("Müller");
Rechnung rechnung = #+ with #CS.CREATE() TestDaten.erzeugeRechnung(mueller);
```

Nach dem Commit sind automatisch vergebene IDs gesetzt.

### Plausible Testdaten

Committete Testdaten bleiben in der Datenbank und sammeln sich über mehrere Testläufe an. Testdaten sollen trotzdem plausibel und für Menschen lesbar bleiben; technische Zufallswerte werden nicht verwendet.

- **KONVENTION:** Ein Test greift über die zurückgegebenen Objekte auf seine Testdaten zu, nicht über ihre Namen oder andere fachliche Werte. Mehrfach vorhandene Datensätze mit gleichen Werten sind dadurch unschädlich.
- **KONVENTION:** Stammdaten, insbesondere solche mit eindeutigen Werten, werden geholt oder angelegt: `TestDaten.zahlungsart("Überweisung")` liefert die vorhandene Zahlungsart „Überweisung“ oder legt sie an. Die Werte bleiben so über alle Läufe stabil.
- **KONVENTION:** Ein Suchtest sucht nach einem Merkmal, das nur dieser Testlauf anlegt, und prüft nicht die Gesamtzahl der Treffer. Das Merkmal ist ein lesbarer Zusatz mit Datum und Uhrzeit des Laufs, etwa der Kundenname „Müller 30.09. 14:32“.
