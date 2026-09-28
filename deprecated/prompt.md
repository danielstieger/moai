




# TODO

- Skill für baselang collection

- Plugin erzeugen
  - .agents/skills nach skills?  !! PFADE STIMMEN JA GARNICHT !! Codex verschieben lassen + Referenzen (z.B. auf docu anpassen, Report "Summary angepasste Referenzen")
  - AGENT.md mit neuem namespace, welche skills gibt es, welchen skill für was verwenden? Was ist im docu ordner 
  - json plugin manifest
  - ? 

- Readme anpassen.. 
- Erster Testlauf für PetClinic. Was ist in der Doku zu Verbessern, was in den beteiligten dsl skills. Welche Verbesserungen hätten positive Konsquenzen? Was bietet sich an? Lass uns das erst diskutieren.    








--- 


  Verwende den Skill `mps-dsl-memory` für org.modellwerkstatt.dataux
  

  Nutze dabei folgende Quellen:

  1. Die aktuell über MPS MCP erreichbare Sprache
     - `org.modellwerkstatt.dataux` als technische Quelle der Wahrheit für:
     - Die global geladene Solution `org.modellwerkstatt.dataux.tests ` (wird immer mit ausgeliefert, primär aber kein dataux content! darf zitiert werden!)
     - Das offene Beispielprojekt (wird nicht ausgeliefert, steht später nicht zu Verfügung und darf nicht zitiert werden.)
     - English als Sprache verwenden. Nur die Doku in /docu bleibt deutsch. 

  2. Die Dokumentation `manmap.md`, `objectflow.md`, `dataux.md` und die Übersicht `moware-werkbank.md` im Verzeichnius docu
     - Dort wird sehr vieles erläutert (fachliche Semantik, Laufzeitverhalten, Einschränkungen, typische Anwendungsfälle, Best Practices, Fehlerbilder und Diagnose, Zuständigkeiten der DSLs , Zusammenspiel der DSLs. 
     - Die Doku steht immer zur Verfügung, darf Referenziert und Verlinkt werden.
     - Wichtiges und Zentrales für das mps-dsl-memory dieser DSL kann auch direkt übernommen werden. Der Skill soll die Dokumentation aber nicht generell duplizieren, sondern für Agenten operationalisieren: Navigation, kritische Regeln, Workflows, Gotchas, überprüfte Beispielreferenzen und portable JSON-Blueprints.
     - Die Dokumentation darf nicht verändert werden. 
    
  3. NEU ist, dass der erzeugte Skill sowohl für Codex als auxh für Claude optimal sein soll. 


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
 

 # Verlinkung und Nachvollziehbarkeit der Dokumentation

  Die Dokumentation soll nicht nur gesammelt in der zentralen `SKILL.md`
  aufgeführt werden.

  - Verlinke jede zentrale fachliche Regel, Laufzeitaussage, Einschränkung,
    Best Practice und Diagnoseanweisung möglichst direkt mit dem passenden
    Abschnitt in `/docu`.
  - Verwende relative Markdown-Links, nach Möglichkeit einschließlich des
    Abschnittsankers.
  - Setze kontextbezogene Links insbesondere in:
    - `references/concepts.md`
    - `references/workflows.md`
    - `references/gotchas.md`
  - Die zentrale `SKILL.md` soll weiterhin kompakt bleiben und eine
    Dokumentationsübersicht enthalten.
  - Die Dokumentation darf nicht großflächig wiedergegeben werden. Formuliere
    stattdessen eine kurze operationale Regel und verlinke unmittelbar die
    ausführliche Begründung oder Semantik.
  - Ein bloßer Sammellink pro Dokument genügt nicht.
  - Erstelle abschließend eine Quellenabdeckung: Für jede wichtige
    Themenfamilie muss erkennbar sein, welche Dokumentationsdatei und welcher
    Abschnitt verwendet wurden.

  Prüfe zum Abschluss:

  1. Alle Links sind relativ und zeigen auf vorhandene Dateien.
  2. Die zentralen operationalen Aussagen besitzen passende Quellenlinks.
  3. Keine Dokumentation wurde verändert.
  4. Das Problemprotokoll nennt fehlende, widersprüchliche oder nicht eindeutig
     zuordenbare Dokumentationsaussagen ausdrücklich.

 WICHTIG: Fehler und Problemprotokoll ersrtellen (oder leer, wen keine Probleme!); Löse Widersprüche nicht stillschweigend auf! Frage nach! 