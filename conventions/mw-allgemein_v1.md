## Allgemeine verbindliche Konventionen

- **KONVENTION:** Unsere Ubiquitous Language ist Deutsch. Alles, was Fachlichkeit in der Software ausdrückt, wird konsistent mit deutschen Fachbegriffen benannt – insbesondere Namespaces, Datenmodelle, Services und Methoden.
- **KONVENTION:** Das Datenbankschema erstellt der Entwickler in MPS aus den `EntityMapping`s der Persistence Descriptions. Agenten erzeugen oder ändern keine Datenbankschemata.
- **KONVENTION:** Eine Run Configuration, die ein `AppUI Module` mit `org.modellwerkstatt.fx8forms` direkt in MPS startet, erhält den VM-Parameter `--enable-native-access=ALL-UNNAMED`.
- **KONVENTION:** Eine Anwendung wird von innen nach außen aufgebaut: zuerst der ExpensiveCode (`domain`, `read`) mit seinen Tests, danach der CheapCode (`unit`, `unit.read`, `app`). Ein Command setzt erst auf Services auf, deren Tests laufen.
- **KONVENTION:** Die Tests des ExpensiveCode leiten sich aus den fachlichen Anforderungen der Spezifikation ab, etwa aus Akzeptanzkriterien und Geschäftsregeln.
- **KONVENTION:** Tests für CheapCode werden nur auf ausdrücklichen Auftrag erstellt.
