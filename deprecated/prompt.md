  

TODO:
- Git-Submodule und portables Plugin
- Fehler und Problemprotokoll ersrtellen (oder leer, wen keine Probleme!); Löse Widersprüche nicht stillschweigend auf.


  Verwende den Skill `mps-dsl-memory` für org.modellwerkstatt.manmap
  

  Nutze dabei folgende Quellen:

  1. Die aktuell über MPS MCP erreichbare Sprache
     - `org.modellwerkstatt.manmap` als technische Quelle der Wahrheit für:
     - Die global geladene Solution `org.modellwerkstatt.dataux.tests` (wird immer mit ausgeliefert! darf zitiert werden!)
     - Das offene Beispielprojekt (wird nicht ausgeliefert, steht später nicht zu Verfügung und darf nicht zitiert werden.)

  2. Die Dokumentation `manmap.md`, `objectflow.md`, `dataux.md` und die Übersicht `moware-werkbank.md`
     - Dort wird sehr vieles erläutert (fachliche Semantik, Laufzeitverhalten, Einschränkungen, typische Anwendungsfälle, Best Practices, Fehlerbilder und Diagnose, Zuständigkeiten der DSLs , Zusammenspiel der DSLs. 
     - Die Doku steht immer zur Verfügung, darf Referenziert und Verlinkt werden.
     - Wichtiges und Zentrales für das mps-dsl-memory kann auch direkt übernommen werden. Der Skill soll die Dokumentation aber nicht generell duplizieren, sondern für Agenten operationalisieren: Navigation, kritische Regeln, Workflows, Gotchas, überprüfte Beispielreferenzen und portable JSON-Blueprints.


  ## Portabilitätsanforderungen

  Der erzeugte Skill wird als Bestandteil eines portablen MoAI-Pakets
  ausgeliefert. Deshalb gelten zwingend folgende Regeln:

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

  ## Quellenpriorität

  Behandle Quellen bei Widersprüchen folgendermaßen:

  1. Das aktuelle MPS-Sprachmodell ist maßgeblich für AST-Struktur, Roles,
     Kardinalitäten, Referenztypen und Vererbung.
  2. Paketinterne Tests und Beispiele sind Evidenz für konkrete Verwendung und
     Laufzeitverhalten.
  3. `manmap.md` ist maßgeblich für die beabsichtigte fachliche Semantik.
  4. `moware-werkbank.md` ist maßgeblich für die architektonische Einordnung.

  Löse Widersprüche nicht stillschweigend auf. Dokumentiere unklare oder nicht
  verifizierbare Aussagen in `references/gotchas.md` oder melde sie im
  Abschlussbericht. Erfinde keine Semantik aus der bloßen AST-Struktur.

  ## Inhalt des Skills

  Erzeuge mindestens:

  - `.agents/skills/manmap-dsl/SKILL.md`
  - `.agents/skills/manmap-dsl/references/concepts.md`
  - `.agents/skills/manmap-dsl/references/workflows.md`
  - `.agents/skills/manmap-dsl/references/gotchas.md`
  - `.agents/skills/manmap-dsl/references/sandbox.md`
  - `.agents/skills/manmap-dsl/references/blueprints/*.json`

  Zusätzliche thematische Referenzdateien sind erwünscht, wenn sie die Benutzung
  erleichtern, beispielsweise für:

  - Schlüssel und Insert-/Update-Entscheidung
  - Entity-, Reference-, Embedded- und List-Mappings
  - explizites Laden von Referenzen und Listen
  - gemappte Queries und Query-Operatoren
  - Save und Delete
  - Session-Identität und Read-only-Verhalten
  - Custom SQL und C2-Parameter
  - Row-Mapper und No-Key-Mapper
  - Audit, Optimistic Locking, Batch und alternative Tabellen
  - Fehlerdiagnose
  - paketinterne Tests

  ## Abgrenzung zur Dokumentation

  Kopiere `manmap.md` nicht vollständig in den Skill.

  Der Skill soll die Dokumentation operationalisieren:

  - `SKILL.md` enthält Einstieg, kritische Regeln und Navigation.
  - `concepts.md` enthält technisch verifizierte Concepts, Roles,
    Kardinalitäten und Referenzen.
  - `workflows.md` enthält konkrete MPS-Arbeitsabläufe.
  - `gotchas.md` enthält nur besonders folgenreiche Fehlerquellen.
  - thematische Referenzen enthalten kompakte, aufgabenbezogene Regeln.
  - Blueprints enthalten wiederverwendbare, validierte AST-Strukturen.
  - Für ausführliche fachliche Erklärungen verweist der Skill mit relativen
    Links auf `manmap.md` und `moware-werkbank.md`.

  ## Blueprints

  Erzeuge kompakte Blueprints für die wichtigsten ManMap-Operationen. Dabei gilt:

  - Verwende vollständig qualifizierte Concept-Namen.
  - Verwende keine Referenzen auf fremde Modelle oder Nodes.
  - Verwende verständliche Platzhalter wie
    `<TARGET_ENTITY_NODE_REF>`,
    `<TARGET_PROPERTY_NODE_REF>` oder
    `<ENTITY_MAPPING_NODE_REF>`.
  - Dokumentiere zu jedem Blueprint seine Voraussetzungen und einzusetzenden
    Referenztypen.
  - Bevorzuge Root-Skeletons plus kleinere Role-Subtrees.
  - Prüfe jeden Blueprint auf gültiges JSON.
  - Prüfe seine AST-Struktur nach Möglichkeit über einen nicht schreibenden
    MPS-MCP-Dry-Run.
  - Verändere bei der Erzeugung des Skills keine fachlichen MPS-Modelle.

  ## Paketinterne Beispiele und Tests

  Falls geeignete ManMap-Beispiele oder Tests Bestandteil des MoAI-Pakets sind:

  - dokumentiere sie über stabile MPS-Modell- und Node-Referenzen,
  - ordne sie konkreten Fragestellungen zu,
  - unterscheide klar zwischen Spezifikation, Testbeleg und bloßem Beispiel.

  Falls keine paketinternen Beispiele vorhanden sind:

  - erfinde keine Sandbox-Referenzen,
  - erkläre dies in `references/sandbox.md`,
  - verwende verifizierte, referenzfreie Blueprints als primäre Beispiele.

  ## Beziehungen zu anderen Skills

  Verlinke relativ auf:

  - `../objectflow-dsl/SKILL.md`, wenn Entities, DTOs, Business Properties,
    Sessions oder Commands betroffen sind;
  - `../dataux-dsl/SKILL.md`, wenn ManMap-Ergebnisse für UI- oder
    Batch-Anwendungsfälle relevant sind;
  - die allgemeinen MPS-Skills für BaseLanguage und Node Editing.

  Übernimm keine absoluten Skill-Verzeichnisse.

  ## Abschlussprüfung

  Prüfe vor Abschluss:

  - keine absoluten Pfade,
  - keine Namen lokaler oder externer Beispielprojekte,
  - keine Angaben zur IDE-Sitzung während der Erzeugung,
  - keine nicht ausgelieferten Modell- oder Node-Referenzen,
  - alle relativen Links vorhanden,
  - alle JSON-Dateien syntaktisch gültig,
  - alle dokumentierten Concepts und Roles gegen MPS geprüft,
  - alle Blueprints ohne fremde IDs,
  - klare Trennung zwischen MPS-Struktur, dokumentierter Semantik,
    Testbeleg und Empfehlung.

  Gib anschließend einen kurzen Bericht aus:

  - welche Quellen verwendet wurden,
  - welche paketinternen Tests oder Beispiele verwendet wurden,
  - welche Blueprints erzeugt wurden,
  - welche Aussagen nicht technisch verifiziert werden konnten,
  - welche Widersprüche oder Dokumentationslücken gefunden wurden.

  Ändere außer `.agents/skills/manmap-dsl/` keine Dateien.
  Ändere insbesondere weder die Dokumentation noch MPS-Modelle oder andere Skills.

  Der entscheidende Satz ist dabei nicht nur „keine absoluten Pfade“, sondern:

  > Referenziere nur Modelle, Tests und Nodes, die garantiert Bestandteil des ausgelieferten Pakets sind.

  Damit verhindert der Prompt auch indirekte, aber ebenso problematische Abhängigkeiten auf simpleone, eFWWS oder lokal verfügbare globale Testmodelle.
