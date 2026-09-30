## Verbindliche Konventionen für Tests

### Testdaten mit einer Custom Session anlegen

Tests committen nicht. Testdaten, die für einen Test in der Datenbank stehen müssen, werden deshalb über eine eigene Custom Session angelegt und dort committet.

- **KONVENTION:** Das Modell `<firma>.<app>.testbase` enthält den Service `CS` mit den Methoden `CREATE()` und `COMMIT()`. `CREATE()` erzeugt eine neue Custom Session; `COMMIT()` startet mit `startTransactionAndFlush()` eine Transaktion auf der Session des aktuellen Kontexts, führt die registrierten Session-Operationen aus und committet.
- **KONVENTION:** Alle Methoden zum Anlegen von Testdaten liegen im Service `TestDaten` des jeweiligen `tests`-Modells. Eine solche Methode baut den Objektgraphen auf, registriert das Speichern mit `session operation add` und schließt mit `#CS.COMMIT()` ab.
- **KONVENTION:** Der Test ruft Methoden zum Anlegen von Testdaten mit `#+ with #CS.CREATE()` auf. Innerhalb der Methode ist `session` damit die Custom Session; die Session des Tests bleibt unberührt.
- **KONVENTION:** Persistierte Ergebnisse werden in einer frischen Custom Session zurückgelesen, etwa `#+ with #CS.CREATE() OwnerRepository.lade(id)`.

```objectflow
component CS

  @Autowired()
  private IOFXApplicationFactory appFactory;

  public IOFXSession CREATE() {
    return appFactory.createNewSession(session.getUserEnvironment(), session.getUserServices());
  }

  public void COMMIT() {
    try {
      session.startTransactionAndFlush();
    } catch (Exception e) {
      throw new RuntimeException(e);
    }
  }
```

```objectflow
component TestDaten

  public Tierart erzeugeTierart(string name) {
    final Tierart tierart = new Tierart();
    tierart.name = name;
    session operation add # TierartRepository.speichern(tierart)
      // "Testdaten Tierart";
    #CS.COMMIT();
    return tierart;
  }
```

Aufruf im Test:

```objectflow
Tierart katze = #+ with #CS.CREATE() TestDaten.erzeugeTierart("Katze");
```

Das funktioniert unabhängig von der Datenbank; nach dem Commit sind automatisch vergebene IDs gesetzt.

### Plausible Testdaten

Committete Testdaten bleiben in der Datenbank und sammeln sich über mehrere Testläufe an. Testdaten sollen trotzdem plausibel und für Menschen lesbar bleiben; technische Zufallswerte werden nicht verwendet.

- **KONVENTION:** Ein Test greift über die zurückgegebenen Objekte auf seine Testdaten zu, nicht über ihre Namen oder andere fachliche Werte. Mehrfach vorhandene Datensätze mit gleichen Werten sind dadurch unschädlich.
- **KONVENTION:** Stammdaten, insbesondere solche mit eindeutigen Werten, werden geholt oder angelegt: `TestDaten.tierart("Katze")` liefert die vorhandene Tierart „Katze“ oder legt sie an. Die Werte bleiben so über alle Läufe stabil.
- **KONVENTION:** Ein Suchtest sucht nach einem Merkmal, das nur dieser Testlauf anlegt, und prüft nicht die Gesamtzahl der Treffer. Das Merkmal ist ein lesbarer Zusatz mit Datum und Uhrzeit des Laufs, etwa der Nachname „Müller 30.09. 14:32“.
