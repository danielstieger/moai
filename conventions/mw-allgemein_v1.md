## Allgemeine verbindliche Konventionen

- **KONVENTION:** Unsere Ubiquitous Language ist Deutsch. Alles, was Fachlichkeit in der Software ausdrückt, wird konsistent mit deutschen Fachbegriffen benannt – insbesondere Namespaces, Datenmodelle, Services und Methoden.
- **KONVENTION:** Das Datenbankschema erstellt der Entwickler in MPS aus den `EntityMapping`s der Persistence Descriptions. Agenten erzeugen oder ändern keine Datenbankschemata.
- **KONVENTION:** Eine Run Configuration, die ein `AppUI Module` mit `org.modellwerkstatt.fx8forms` direkt in MPS startet, erhält den VM-Parameter `--enable-native-access=ALL-UNNAMED`.
