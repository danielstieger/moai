  

TODO:
- Git-Submodule und portables Plugin
- Fehler und Problemprotokoll ersrtellen (oder leer, wen keine Probleme!); Löse Widersprüche nicht stillschweigend auf.


  Verwende den Skill `mps-dsl-memory` für org.modellwerkstatt.manmap
  

  Nutze dabei folgende Quellen:

  1. Die aktuell über MPS MCP erreichbare Sprache
     - `org.modellwerkstatt.manmap` als technische Quelle der Wahrheit für:
     - Die global geladene Solution `org.modellwerkstatt.dataux.tests` (wird immer mit ausgeliefert! darf zitiert werden!)
     - Das offene Beispielprojekt (wird nicht ausgeliefert, steht später nicht zu Verfügung und darf nicht zitiert werden.)

  2. Die Dokumentation `manmap.md`, `objectflow.md`, `dataux.md` und die Übersicht `moware-werkbank.md` im Verzeichnius docu
     - Dort wird sehr vieles erläutert (fachliche Semantik, Laufzeitverhalten, Einschränkungen, typische Anwendungsfälle, Best Practices, Fehlerbilder und Diagnose, Zuständigkeiten der DSLs , Zusammenspiel der DSLs. 
     - Die Doku steht immer zur Verfügung, darf Referenziert und Verlinkt werden.
     - Wichtiges und Zentrales für das mps-dsl-memory kann auch direkt übernommen werden. Der Skill soll die Dokumentation aber nicht generell duplizieren, sondern für Agenten operationalisieren: Navigation, kritische Regeln, Workflows, Gotchas, überprüfte Beispielreferenzen und portable JSON-Blueprints.
     - Die Dokumentation darf nicht verändert werden. 


  ## Portabilitätsanforderungen

  Der erzeugte Skill wird als Bestandteil eines portablen MoAI-Pakets
  ausgeliefert. Daher dauerhafte Distributionsregeln. 

  - Schreibe keine absoluten Dateisystempfade in den Skill.
  - Schreibe keine Benutzernamen, Home-Verzeichnisse, Checkout-Verzeichnisse
    oder maschinenspezifischen Verzeichnisnamen in den Skill.
  - Übernimm keine Angaben darüber, welches Projekt während der Erzeugung
    in MPS geladen oder ausgewählt war.
  - Verwende in den erzeugten Dateien keine Formulierungen, die ein bestimmtes
    „offenes Projekt“ oder eine bestimmte IDE-Sitzung voraussetzen.
  - Nenne keine externen Beispielprojekte wie `simpleone` oder `eFWWS`.
  - Referenziere nur Module, Modelle, Tests und Nodes, die garantiert Bestandteil
    des ausgelieferten MoAI-Pakets oder einer ausdrücklich dokumentierten
    Paketabhängigkeit sind - SONST NACHFRAGEN.
  - Übernimm keine persistenten Node-Referenzen aus fremden Anwendungsprojekten.
  - Verwende für nicht paketinterne Referenzziele klar benannte Platzhalter,
    die im jeweiligen Zielmodell zur Laufzeit aufgelöst werden müssen.
  - Verwende ausschließlich relative Links auf Dateien innerhalb des Pakets.
  - Das jeweilige MPS-Zielprojekt muss bei der späteren Anwendung des Skills
    dynamisch bestimmt werden; im Skill darf kein Projektpfad gespeichert sein.

  Falls ein untersuchtes Beispiel nicht zum auslieferbaren Paket gehört, darf
  daraus eine allgemeine, anonymisierte JSON-Struktur abgeleitet werden. Namen,
  Node-IDs, Modellreferenzen und fachliche Bezeichner des fremden Projekts dürfen
  dabei nicht übernommen werden.
 