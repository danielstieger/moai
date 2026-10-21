# Skill-Anpassungen, generisches Tooling und MCP-Feature-Requests – Ergebnis aus zwei Runs

Zwei unabhängige Runs haben mit MoAI und dem MPS-MCP je eine Anwendung gebaut. Beide sind auf dieselben zentralen
Probleme gestoßen und haben dafür dieselben Arten von Hilfsskripten geschrieben:

- **Run 3**: Fuhrpark (`2026_2/mjfuhrpark`), Skripte in `mjfuhrpark/example_tooling/`
- **Run 4**: Rechnungsverwaltung (`2026_2/rechnung`), Skripte und Begründung in `rechnung/example_tooling/` (`TOOLING.md`)

Das Dokument leitet daraus drei Arten von Änderungen ab:

- **Teil A – Low Hanging Fruits:** einfache Anpassungen an bestehenden Skills, Konventionen und der Installation. Ohne neues Werkzeug, sofort wirksam.
- **Teil B – Tooling generisch:** Werkzeuge, die MoAI mitliefert, und die Skill-Teile, die auf ihnen aufbauen.
- **Teil C – Feature Requests an den JetBrains MPS-MCP:** Erweiterungen des Servers, jeweils mit dem Tooling, das dadurch überflüssig würde.

Beschrieben sind Fehlerklassen und Aufgaben, keine Einzelfälle und keine Implementierung. Einzelfunde stehen als Belege im Anhang.

---

## Kurzfassung

- Es gibt **acht zentrale Probleme** (Abschnitt 2).
- **Das meiste Wissen war schon da und wurde nicht gefunden.**
  - Doku-Tabellen nennen jedes Konzept mit Projektion.
  - `get_concept_details` liefert die Struktur, `dryRun` prüft Rollen und Zuweisbarkeit.
  - `mps_dump.py` liest große Dumps.

  Beide Runs haben trotzdem Formen aus Dumps erraten und `mps_dump.py` nachgebaut.
  **Teil A** setzt hier an: an der Skill-Struktur, den Abläufen und dem Setup.
- **Teil B** löst, was Skills nicht lösen: Muster über mehrere Ebenen und Methodenrümpfe mit MoWare-Konstrukten. Kern ist ein
  **generischer Builder**, der die Struktur aller beteiligten Sprachen nutzt. Diese wird bei jedem MoAI-Release exportiert.
- **Teil C** nennt die Server-Erweiterungen, mit denen der größte Teil von Teil B wieder entfallen könnte. Dauerhaft bleiben nur
  Builder, Muster-Schicht und Scaffolds.

---

## 1. Grundlage

| | Run 3 – Fuhrpark | Run 4 – Rechnungsverwaltung |
| --- | --- | --- |
| Datum, Dauer | 20.10.2026, ca. 74 min | 21.10.2026, ca. 72 min |
| Umfang | 2 Features (Fahrzeug, Lenker), 2 Aggregate, Rollen und Berechtigungen, Suche, App, Tests | 1 Aggregat (Rechnung mit Positionen), Value Objects mit Logik, Statusübergänge, Such-Wizard, App, Tests |
| MoAI-Stand / MPS | `7ba6f7a` / 2026.2 | `ac05213` (enthält die ersten Änderungen aus Run 3) / 2026.2 |
| Werkzeugaufrufe gesamt / davon MPS-MCP | 516 / 337 | 430 / 280 |
| `print_node` / `update_node` / `insert_root` | 87 / 68 / 33 | 64 / 55 / 20 |
| Java-Parser | 6 (nur triviale Rümpfe; der Versuch an einem Value Object ergab 40 Fehler) | 23 (Hauptweg für Methodenrümpfe) |
| Python-Aufrufe | 73 | 76 |
| Ablage der Skripte | Scratchpad, verloren; aus dem Transkript rekonstruiert | Projektordner, dokumentiert |

**Werkzeuge beider Runs und was MoAI schon mitbrachte:**

| Werkzeugart | Run 3 | Run 4 | Schon in MoAI |
| --- | --- | --- | --- |
| Blueprint-Builder für Strukturen und Ausdrücke | `gen.py`, `ex.py` | `bp.py` | – (feste Blueprints mit Platzhaltern) |
| Builder für Commands und Oberfläche | `ui.py` | Helfer in `build_unit.py` | – |
| Methodenrümpfe aus Text | – (bewusst umgangen) | `of_fix.py` + Marker-Konvention | – |
| Dump → Blueprint | `tobp.py` | `to_blueprint.py` | – |
| Baumansicht für Dumps | `shape.py` | `compact.py` | **`skills/mps-mcp-workflow/scripts/mps_dump.py`** (`tree`, `node`, `shape`, `roots`), seit `7ba6f7a` |
| Prüfberichte verdichten | – | `problems.py` | – |
| Referenzen aus Dumps ernten | `harvest.py`, `harvest2.py` | – | als Ablauf in `mps-baselanguage` vorgeschrieben |
| Struktur eines Konzepts | aus Dumps erraten | aus Dumps erraten | **`get_concept_details`** mit `detail: "shape"`/`"full"` |
| Prüfung von Rollen und Zuweisbarkeit | – | – | **`dryRun`** beim Insert |

**Abgrenzung:**
- Projekte ändern `moai/` nicht. Skills und Tooling sind Teil des MoAI-Pakets. Das Tooling wird nicht ins Projekt kopiert und schreibt nichts ins Projekt.
- Anwendungsspezifisches gehört weder in Skills noch ins Tooling: Namen von Rollen, Labels und Commands einer App.

---

## 2. Die zentralen Probleme

| | Problem | Wie es sich zeigte | A – Low Hanging Fruits | B – Tooling | C – MCP |
| --- | --- | --- | --- | --- | --- |
| **Z1** | **Methodenrümpfe mit Fachlogik** | Der Parser kennt keine MoWare-Konstrukte (Business Properties, collections, Literale, Status, Preconditions, Komponentenaufrufe, Testerwartungen) und bindet gleichnamige Parameter anderer Methoden falsch. Der Skill schickt diesen Fall ins Hand-JSON. | – | **Text → ObjectFlow**, Ablauf für Rümpfe | Parser löst im Scope der Zielposition auf |
| **Z2** | **Vorhandenes Wissen wird nicht gefunden** | Doku-Tabellen, `get_concept_details`, `dryRun` und `mps_dump.py` waren da. Beide Agenten erschlossen Formen trotzdem aus Dumps und bauten `mps_dump.py` nach. | **Einstieg und Verweise in den Skills** | generischer Builder nutzt die Struktur direkt | – |
| **Z3** | **Muster über mehrere Ebenen** | Struktur und `sampleNode` zeigen eine Ebene; der `sampleNode` ist ein Platzhalter. Precondition mit Meldung, Service-Methode mit Validation (6–15 KB JSON) oder Command mit Pages braucht mehrere Ebenen. | Musterbeispiel zentral verlinken | **Builder + Muster-Schicht**, erzeugte Blueprints | – |
| **Z4** | **Referenzen stabil setzen** | Der Skill verlangt, Referenzen per `print_node` zu ernten (Run 3: Registry, Platzhalter, erneutes Ernten). Run 4 löste über Namen auf; bei langen Property-Ketten gab es Auflösungsschleifen und Timeouts. `SET CHILD` vergibt neue IDs. | **Referenzregel, Identität, Reparatur** | Builder setzt die Regel um | Insert liefert Karte Name → Referenz |
| **Z5** | **Verhalten ändert sich mit der Version** | In MPS 2026.2 laufen beim Einfügen aus JSON die Factories; früher war das ein Bug. Sie setzen Defaults, die gesetzte Werte überschreiben, und Importe ohne Modulabhängigkeit. Der Checker schweigt. | **Verhaltensänderungen je Release, Kontrolle nach dem Insert** | Soll-Ist-Vergleich, Export-Vergleich | Insert meldet Factory-Änderungen |
| **Z6** | **Umgebung und Setup** | Config-Vorlagen schwer zu finden bzw. nicht über Modellgrenzen kopierbar; Component Scanning; JDBC-Treiber; DB-Zugang; VCS-Dialog blockiert MCP-Aufrufe; keine VM-Optionen. | **Konventionen, Workflows, Installation** | Root kopieren, Config-Scaffold | Kopieren über Modellgrenzen, VM-Optionen, modale Dialoge |
| **Z7** | **Kontextverbrauch** | Dumps und Prüfberichte mit 20–40 KB; der Parser liefert bei Marker-Code sehr große Antworten. | **Verweis auf `mps_dump.py` an der Entstehungsstelle** | `mps_dump.py` ausbauen | kompakte Ausgaben |
| **Z8** | **Wiederholte Konventionsmuster** | Commands, Page Panes, Such-DTOs, Owner/Edit-Paare und Configs folgen in jeder App denselben Regeln; beide Runs schrieben app-spezifische Skripte. | – | **Scaffolds** | – |

---

# Teil A – Low Hanging Fruits

Einfache Anpassungen an bestehenden Skills, Konventionen und der Installation. Sie brauchen kein neues Werkzeug und wirken
ab dem nächsten Run. Stand jeweils gegen MoAI `ac05213`.

## A.1 Skill-Struktur und Auffindbarkeit (Z2, Z7)

| Anpassung | Wo | Stand |
| --- | --- | --- |
| **Einheitlicher Einstieg „unbekanntes Konstrukt“**, in allen DSL-Skills gleich: Projektion in der Doku-Tabelle → Konzeptname → `get_concept_details` (`shape`) → echte Instanz im Paketbeispiel (`FIND_INSTANCES`) → mit `mps_dump.py` lesen → Insert mit `dryRun` | `SKILL.md` von objectflow, manmap, dataux, collections | offen (Schritte stehen einzeln in `mps-language-analysis`, `mps-mcp-workflow` und den Doku-Tabellen) |
| **Mitgelieferte Werkzeuge zuerst**, mit dem Satz „nicht nachbauen“ | jeder DSL-Skill | offen (`mps_dump.py` steht nur im Abschnitt „Scripts“ von `mps-mcp-workflow`) |
| **`mps_dump.py` an der Entstehungsstelle nennen:** überall, wo ein Skill einen großen Dump erzeugen lässt (`print_node deep`, `get_concept_details` einer Sprache, Prüfberichte) | Skills mit solchen Abläufen | offen |
| **Aufgaben der Teile festlegen:** `SKILL.md` = Einstieg und Abläufe; `references/` = Nachschlagen; Doku-Tabellen = Projektion → Konzept; Blueprints = Muster. Kein Wissen doppelt an zwei Orten. | alle Skills | offen |

## A.2 Abläufe korrigieren (Z4)

| Anpassung | Wo | Stand |
| --- | --- | --- |
| **Referenzregel statt Ernten:** standardmäßig über Namen. Persistent für Stubs, Überladungen, Ziele in fremden Modellen und lange Property-Ketten über fremde Entities. Ernten nur, wenn eine Auflösung über Namen nachweislich scheitert. | `mps-baselanguage`, `mps-node-editing` | offen (heute ist Ernten der Standard) |
| **Identität erhalten:** Konstruktoren und Testmethoden nur über den Rumpf ersetzen; Methoden eines Roots gemeinsam ersetzen, damit Referenzen zwischen ihnen über Namen stimmen | `mps-baselanguage`, `mps-node-editing` | teilweise |
| **Reparatur im Ablauf nennen:** `FIX_REFERENCES` und Quick-Fixes (`autoApplyQuickFixes`) nach der Auflösung über Namen | `mps-baselanguage` | dokumentiert in `mps-mcp-workflow`, im Ablauf offen |

## A.3 Muster (Z3)

| Anpassung | Wo | Stand |
| --- | --- | --- |
| **Ein vollständiges Musterbeispiel je Aufgabe** an zentraler Stelle: Aggregat (etwa `org.modellwerkstatt.objectflow.tests.OrderDocument`), Service mit Regeln, Commands und Oberfläche, Tests | `sandbox.md` der DSL-Skills | nur Einzelteile verlinkt |

## A.4 Versionsabhängiges Verhalten (Z5)

| Anpassung | Wo | Stand |
| --- | --- | --- |
| **Abschnitt „Verhaltensänderungen“ je MoAI-Release:** was sich gegenüber der Vorversion in MPS, MoWare oder MCP geändert hat, etwa dass Factories beim Einfügen jetzt laufen und Defaults setzen | `MPS_AGENT_GUIDE.md` oder `mps-mcp-workflow` | offen (der Einzelfall `DateLiteral` steht in den Gotchas) |
| **Kontrolle nach dem Insert:** eingefügten Knoten ausgeben und prüfen, ob gesetzte Werte erhalten blieben; neue Modellimporte gegen Modulabhängigkeiten prüfen. Bis zum Werkzeug in B.2 als Schritt von Hand. | `mps-node-editing` | offen |

## A.5 Umgebung und Setup (Z6)

| Anpassung | Wo | Stand |
| --- | --- | --- |
| Config-Vorlagen in `wbkit.shared.configuration` | objectflow, Workflow OFXConfig | umgesetzt |
| Component Scanning: Test-Configs scannen zusätzlich `wbkit.shared.testing`, Produktiv-Configs schließen `tests` aus | objectflow, `mw-tests`, `mw-anwendungsaufbau` | offen |
| Klären, ob „`base` importiert nichts“ auch wbkit meint (Einbinden per `include section` oder Kopieren) | `mw-anwendungsaufbau` | offen |
| JDBC-Treiber in die Anwendungs-Solution einbinden (Bibliothek in der Java-Facet) | `mw-anwendungsaufbau` | offen |
| DB-Zugang für Tests: wo `${DB_*}` gesetzt wird, Verweis auf die vorhandene lokale Test-Config | `mw-tests` | offen |
| VCS so einstellen, dass neue Dateien ohne Dialog aufgenommen werden; Plugin-Registrierung ohne absoluten Pfad | `INSTALL_INSTRUCTIONS.md` | offen |
| Fachliche Objekte nicht löschen, sondern einen Status vorsehen | `mw-domaenenmodell` | umgesetzt |

---

# Teil B – Tooling generisch

Werkzeuge, die MoAI mitliefert, und die Skill-Teile, die auf ihnen aufbauen. Beschrieben ist, **was** jedes Werkzeug leisten muss.

## B.1 Übersicht: wofür jedes Werkzeug primär gebraucht wird

| Werkzeug | Aufgabe in einem Satz | Primär gebraucht, weil … | Ohne das Werkzeug | Stufe |
| --- | --- | --- | --- | --- |
| **Struktur-Export** | exportiert bei jedem MoAI-Release die Struktur aller beteiligten Sprachen als versionierte Daten | der Builder offline arbeiten soll und Sprachänderungen sichtbar werden müssen (Z2, Z5) | Formen aus Dumps erraten; Änderungen fallen erst im Run auf | 1 |
| **Generischer Builder** | baut jeden Knoten jeder Sprache aus den exportierten Strukturen und prüft ihn dabei | Blueprints wortreich sind und Rollen, Kardinalität und Zuweisbarkeit sonst erst beim Insert auffallen (Z2, Z3) | Hand-JSON oder handgeschriebene Bausteine je Konzept | 1 |
| **Soll-Ist-Vergleich** | prüft nach dem Insert, ob gesetzte Werte und Referenzen erhalten blieben | Factories Werte still überschreiben können (Z5) | Kontrolle von Hand (A.4) oder Fehler erst im Test | 1 |
| **`mps_dump.py` (Ausbau)** | liest Dumps, Blueprints und Prüfberichte kompakt, gefiltert und gruppiert | große Antworten den Kontext füllen (Z7) | Nachbau in jedem Run | 1 |
| **Root kopieren** | übernimmt einen Root aus einem anderen Modell als Blueprint, mit Auswahl, Umbenennung und Ersetzung | der Server nicht über Modellgrenzen kopiert (Z6) | Konvertierung je Run, Referenzen zeigen ins Quellmodell | 1 |
| **Muster-Schicht** | bietet Kurzformen für Muster über mehrere Ebenen und erzeugt daraus die Blueprints der Skills | Struktur und `sampleNode` nur eine Ebene zeigen (Z3) | Muster je Run aus Dumps erschlossen | 2 |
| **Text → ObjectFlow** | macht aus Java-nahem Text mit Markern korrekte Knoten | der Parser keine MoWare-Konstrukte kennt (Z1) | jeder Rumpf als Syntaxbaum oder viele `update_node` | 2 |
| **Scaffolds** | erzeugen konventionskonforme Grundgerüste aus einer kleinen Spezifikation | sich Konventionsmuster in jeder App wiederholen (Z8) | app-spezifische Einzelskripte je Run | 3 |

Welche Werkzeuge mit einer Server-Erweiterung entfallen würden, steht in Teil C.

**Nicht übernommen:**
- die Referenz-Registry aus Run 3: Die Referenzregel (A.2) macht sie überflüssig;
- handgeschriebene Bausteine je Konzept (beide Runs): Sie werden durch den generischen Builder ersetzt;
- eine Prüfung gegen einen Katalog von Einzelfällen: An ihre Stelle treten Struktur aus dem Export, `dryRun` und Soll-Ist-Vergleich.

## B.2 Aufgaben je Werkzeug

**Struktur-Export**
- Bei jedem MoAI-Release `get_concept_details` mit `detail: "full"` für alle beteiligten Sprachen abfragen:
  ObjectFlow, ManMap, DataUX, BaseLanguage, collections, closures und die Sprachen, von denen sie erben (etwa `jetbrains.mps.lang.core`).
- Je Konzept ablegen:
  - Name, Abstraktheit, Superkonzept und Super-Interfaces;
  - Properties mit Typ und Enum-Werten;
  - Referenzen und Kinder mit Zielkonzept und Kardinalität.

  Live geprüft: `full` liefert `superConcept` und `superInterfaces`.
- Daraus die vollständige Konzepthierarchie über die Sprachgrenzen berechnen. Damit ist offline entscheidbar, ob ein Konzept in eine Rolle passt.
- Den Sprachstand (MPS, MoWare, Modul-Versionen) im Export vermerken.
- Den Unterschied zum vorigen Export ausgeben: neue, geänderte und entfallene Konzepte und Rollen. Daraus entstehen der Abschnitt
  „Verhaltensänderungen“ (A.4) und die Liste der zu prüfenden Muster.
- Läuft mit MPS und MCP beim Release, nicht beim Agenten im Projekt.

**Generischer Builder**
- Jeden Knoten jeder exportierten Sprache über Konzeptnamen, Rollen und Werte bauen, ohne konzeptspezifischen Code.
- Beim Bauen prüfen:
  - existiert die Rolle;
  - passt die Kardinalität (eins oder Liste);
  - fehlen Pflichtrollen;
  - wird ein abstraktes Konzept verwendet;
  - ist ein Enum-Wert gültig;
  - passt das Konzept laut Hierarchie zum Zielkonzept der Rolle.
- FQ-Namen, die Verschachtelung in Listen und das Auslassen leerer Rollen übernehmen.
- Referenzen nach der Regel aus A.2 setzen: über Namen, wo sie eindeutig auflösen, sonst persistent.
- Persistente Referenzen auf häufig gebrauchte Java-Stubs der Laufzeitmodule bereitstellen, beim Release mit dem Export erzeugt.
- Keine Namen einer Anwendung.

**Soll-Ist-Vergleich**
- Nach jedem Insert oder `SET CHILD` den eingefügten Knoten mit dem Blueprint vergleichen: Haben alle gesetzten Properties und Referenzen
  denselben Wert? Abweichungen mit Ort und beiden Werten melden.
- Neu entstandene Modellimporte gegen die Modulabhängigkeiten prüfen.
- Kommt ohne Wissen über einzelne Factories aus.

**`mps_dump.py` (Ausbau des vorhandenen Werkzeugs)**
- Zusätzlich zu `roots`, `models`, `node`, `tree` und `shape`:
  - Blueprints lesen;
  - Prüfberichte verdichten und nach Root und Fehlerart gruppieren;
  - absichtlich unaufgelöste Stellen (Marker-Code vor der Umsetzung) getrennt ausweisen;
  - in Dumps nach Konzept, Name oder Referenz suchen.

**Root kopieren**
- Einen Root aus einem Dump in einen einfügbaren Blueprint umsetzen, mit Referenzen über Namen, damit sie im Zielmodell auflösen.
- Teile auswählen (etwa Config-Sections), umbenennen, Text ersetzen (etwa `firma.app` → Paketname); Default-Properties weglassen.
- Melden, welche Referenzen im Ziel voraussichtlich nicht auflösen.

**Muster-Schicht**
- Kurzformen für Muster über mehrere Ebenen, gebaut über den generischen Builder. Beispiele:
  - Precondition mit Meldung;
  - Service-Methode mit Regeln;
  - Command mit Pages und Conclusions;
  - Custom SQL als Text mit markierten Variablen und Status-Konstanten;
  - Testmethode mit erwarteter Ausnahme.
- **Auswahl nach Regel, nicht nach Fund:** Ein Muster bekommt jedes Konstrukt, dessen Pflichtrollen selbst wieder konzeptspezifische Knoten
  verlangen. Das lässt sich aus dem Export bestimmen.
- Erzeugt die Blueprints, die in den Skills als Beispiele stehen, und ersetzt die heutigen festen Blueprints mit Platzhaltern.

**Text → ObjectFlow**
- Methodenrümpfe in Java-nahem Text annehmen. Ausdrückbar sein müssen alle Konzepte, die laut Export in Statement- und Expression-Rollen passen.
- Die Ausgabe des Parsers über den generischen Builder in Blueprints je Member umsetzen und die Art der Methode festlegen
  (normal, Service, Repository mit Typ).
- Identität erhalten: Konstruktoren und Testmethoden nur über den Rumpf ersetzen.
- Abbrechen und den Ort nennen, statt still Falsches zu erzeugen: bei unbekannten Markern, unaufgelösten Bezeichnern und mehrdeutigen Bindungen.

**Scaffolds**
- Aus einer kleinen Spezifikation in einem einzigen Bulk-Insert konventionskonforme Grundgerüste erzeugen:
  - Aggregat;
  - Suche;
  - Owner- und Edit-Commands;
  - Statusübergang;
  - Configs für Test und FX8.
- Die Konventionen stecken im Generator. Abweichungen eines Projekts (`AGENTS.md`) lassen sich in der Spezifikation ausdrücken.

**Laufzeitregeln für alle Werkzeuge**
- Python-Standardbibliothek, offline, Aufruf mit `python3 -I` (wie `mps_dump.py`).
- Eingaben und Ausgaben als Dateien im Temp-Verzeichnis, das die MCP-Tools lesen; kein Zustand im Arbeitsverzeichnis.
- Keine Projektreferenzen im Werkzeug.
- Jedes Werkzeug nennt den Sprachstand, gegen den es geprüft ist; der Builder liest ihn aus dem Export.

## B.3 Skill-Anpassungen, die das Tooling voraussetzen

| Anpassung | Wo | Setzt voraus |
| --- | --- | --- |
| **Ablauf für Methodenrümpfe** in MoWare-Roots: Skelett → alle Methoden als Text in einem Parser-Aufruf → Dump → Text → ObjectFlow → `SET CHILD` je Member → Soll-Ist-Vergleich. Ersetzt die heutige Vorgabe, solche Rümpfe als JSON zu schreiben. | `mps-baselanguage`, `objectflow-dsl` | Text → ObjectFlow |
| **Marker-Konvention** verbindlich dokumentiert: je Marker Zielkonstrukt, Beispiel, Grenzen | `objectflow-dsl` | Text → ObjectFlow |
| **Blueprints aus der Muster-Schicht** statt fester Vorlagen mit Platzhaltern | `references/blueprints` aller DSL-Skills | Muster-Schicht |
| **Kontrolle nach dem Insert** von Hand (A.4) durch den Soll-Ist-Vergleich ersetzen | `mps-node-editing` | Soll-Ist-Vergleich |
| **Verweis auf das Tooling:** Teil des Pakets, Ausgaben im Temp-Verzeichnis | `INSTALL_INSTRUCTIONS.md` | Stufe 1 |

## B.4 Vergleich der Runs und Entscheidungen

| Bereich | Run 3 | Run 4 | Entscheidung |
| --- | --- | --- | --- |
| **Bausteine** | handgeschrieben je Konzept, breiter Umfang | handgeschrieben je Konzept, flexiblere Grundform | **weder noch:** generischer Builder aus dem Struktur-Export; von Hand nur die Muster-Schicht |
| **Methodenrümpfe** | Syntaxbaum in Python; eindeutig, aber Fachlogik schwer lesbar | Java mit Markern → Parser → Reparatur; dicht und prüfbar, aber heuristisch | **Text mit Markern als Hauptweg**, Knoten über den generischen Builder; Abbruch statt stiller Fehlbindung |
| **Referenzen** | Ernten in eine Registry (wie vom Skill verlangt) | Namen, persistent nach außen und für Überladungen, Quick-Fix | **Namen als Standard** mit klaren Ausnahmen (A.2); Registry entfällt |
| **Identität beim Ersetzen** | nicht geregelt | Konstruktoren und Tests nur über den Rumpf | **Regel von Run 4**, in Skill und Werkzeug |
| **Dump → Blueprint** | Namen; Defaults weggelassen | Namen; Auswahl, Umbenennen, Ersetzen | **Run 4**, ergänzt um das Weglassen von Defaults aus Run 3 |
| **Custom SQL** | Liste aus Wörtern und Token | Fließtext mit markierten Variablen und Status | **Run 4**, als Teil der Muster-Schicht |
| **Commands und Oberfläche** | Bausteine mit festen App-Namen | Bulk-Insert eines Modells, app-spezifisch | **Bulk-Insert je Modell**; App-Spezifisches gehört in die Spezifikation der Scaffolds |
| **Diagnose** | eigene Baumansicht | eigene Baumansicht + Verdichtung der Prüfberichte | **`mps_dump.py` ausbauen**; beide Nachbauten waren unnötig |
| **Prüfung** | – | – | **Struktur im Builder, `dryRun`, Soll-Ist-Vergleich** statt Katalog von Einzelfällen |
| **Ablage** | Scratchpad, verloren | Projektordner, dokumentiert | **versioniert in MoAI** |

**Gemeinsam:** Beide Runs haben Konzeptformen an Beispiel-Roots gelernt und im Code festgehalten, statt die Sprachstruktur abzufragen.

**Trennend im Kern:** Run 3 umgeht MPS bei der Auflösung, Run 4 lässt MPS auflösen und repariert danach. Übernommen wird Run 4,
mit der Strenge von Run 3: Was mehrdeutig ist, wird persistent gesetzt oder führt zum Abbruch.

## B.5 Umsetzung, Qualitätssicherung und Abnahme

| Stufe | Inhalt | Voraussetzung |
| --- | --- | --- |
| **1 – Basis** | Struktur-Export, generischer Builder, Soll-Ist-Vergleich, Ausbau von `mps_dump.py`, Root kopieren; erster Abschnitt „Verhaltensänderungen“ aus dem Export-Vergleich | Teil A |
| **2 – Muster und Rümpfe** | Muster-Schicht und erzeugte Blueprints, Text → ObjectFlow mit Marker-Konvention, Ablauf für Rümpfe | Stufe 1 |
| **3 – Scaffolds** | Generatoren für Aggregat, Suche, Owner/Edit, Statusübergang, Config | stabile Muster-Schicht, abgestimmte Konventionen |

**Qualitätssicherung:**
- **Export-Vergleich bei jedem Release:** Unterschiede der Sprachstruktur werden geprüft, bevor Skills und Muster freigegeben werden.
- **Smoke-Test** gegen ein Sandbox-Projekt in MPS: Muster einfügen, Soll-Ist-Vergleich, bauen. Er fängt Verhaltensänderungen, die die
  Struktur nicht zeigt.
- Golden-Tests für Muster-Schicht und Text → ObjectFlow mit Fixtures aus beiden Runs und aus `org.modellwerkstatt.dataux.tests`.

**Abnahme:**
- Ein dritter Run baut die Fachlichkeit beider Runs nach – Fahrzeug und Lenker, Rechnung mit Positionen. Dabei lernt er keine Konzeptformen
  aus Dumps, baut kein mitgeliefertes Werkzeug nach und schreibt kein Hand-JSON für Methodenrümpfe. Alle Tests sind grün.
- Zahl der MCP-Aufrufe und Dauer werden mit Abschnitt 1 verglichen.
- Vorher misst ein Lauf nur mit Teil A, wie viel die Low Hanging Fruits allein bringen.

---

# Teil C – Feature Requests an den JetBrains MPS-MCP

Erweiterungen des Servers, formuliert für MPS allgemein und nicht für MoWare. Die rechte Spalte zeigt, welches Tooling aus
Teil B dadurch entfiele und was sich in den Skills vereinfacht.

| Feature Request | Nutzen | Überflüssiges Tooling | Vereinfachung in den Skills |
| --- | --- | --- | --- |
| **Parser löst im Scope der Zielposition auf:** Bezeichner, Typen und Aufrufe werden so aufgelöst, wie der Editor an dieser Stelle auflösen würde, einschließlich Spracherweiterungen (Properties von Konzepten, collections, Literale und Statements der eingebundenen Sprachen) und der Stubs aus den Modulabhängigkeiten | Methodenrümpfe aus Text ohne Nachbearbeitung | **Text → ObjectFlow**, Marker-Konvention, Stub-Referenzen im Builder | Ablauf für Rümpfe wird ein Parser-Aufruf |
| **Insert meldet Factory-Wirkungen:** welche Properties, Referenzen, Kinder und Modellimporte Factories gesetzt oder geändert haben | Überschreibungen sofort sichtbar | **Soll-Ist-Vergleich** | Kontrolle nach dem Insert entfällt |
| **`dryRun` mit Factories** (optional) | Wirkungen vor dem Schreiben sehen | Soll-Ist-Vergleich vor dem Insert | – |
| **Insert liefert eine Karte Name → Referenz** der neu entstandenen Knoten | stabile Referenzen ohne weiteres Lesen | jedes Ernten von Referenzen | Referenzregel wird einfacher |
| **Kopieren über Modellgrenzen** (`COPY_NODE` mit Zielmodell, Referenzen im Ziel neu aufgelöst) | Vorlagen übernehmen | **Root kopieren** | Config-Workflow wird ein Aufruf |
| **Kompakte, gefilterte Ausgaben:** `print_node` mit Tiefe, Rollenfilter und Projektion; `responseDetail: summary` für Parser, Insert und Prüfberichte | weniger Kontextverbrauch | große Teile von **`mps_dump.py`** | Verweise auf `mps_dump.py` werden seltener |
| **Struktur-Export als Aufruf:** Konzepthierarchie und Struktur mehrerer Sprachen inklusive geerbter Sprachen in einem Ergebnis | Export ohne eigene Zusammenführung | Teile des **Struktur-Exports** | – |
| **VM-Optionen und Umgebungsvariablen** in `create_run_configuration` und `execute_run_configuration` | Konventionen zum Start lassen sich einhalten | – | Hinweis „von Hand ergänzen“ entfällt |
| **Modale Dialoge erkennen und melden** statt Timeout | blockierte Aufrufe verständlich | – | VCS-Hinweis in der Installation entfällt |
| **Gleiche Namensauflösung bei ADD und DELETE** von Modellimporten | Importe zuverlässig entfernen | – | – |

**Was dauerhaft bleibt, auch wenn alle Requests umgesetzt sind:** der generische Builder (Zusammensetzen, Prüfen offline), die
Muster-Schicht (Muster über mehrere Ebenen) und die Scaffolds (Konventionen als Generator). Ihr Mehrwert liegt über dem Server.

---

## Offene Fragen und Risiken

- **Umfang des Exports:** Welche Sprachen genau nötig sind, damit die Hierarchie vollständig ist (geerbte Konzepte aus `lang.core` und
  weiteren), zeigt erst der erste Export.
- **`sampleNode`:** Er ist ein synthetischer Platzhalter mit einer Ebene und taugt nicht als Muster.
- **Marker-Konvention:** Sie stammt aus einem Run. Vor der Festschreibung prüfen, ob sie alle in Rümpfen zulässigen Konstrukte abdeckt und
  für Agenten eindeutig ist.
- **Grenze der Auflösung über Namen:** Wann Ketten zu lang werden, ist nur beobachtet, nicht ausgemessen.
- **Reihenfolge B gegen C:** Text → ObjectFlow lohnt sich nur, wenn der Parser-Request nicht absehbar umgesetzt wird.
- **Scaffolds und Konventionen:** Ein Generator schreibt Konventionen fest. Lassen sich Abweichungen nicht ausdrücken, umgehen Agenten ihn.

---

## Anhang: Belege aus den Runs

Einzelfunde, die zu den Fehlerklassen geführt haben. Sie sind Belege, kein Arbeitsprogramm.

| Fund | Klasse | Stand `ac05213` |
| --- | --- | --- |
| `mps_dump.py` in beiden Runs nachgebaut (`shape.py`, `compact.py`) | Z2, Z7 | vorhanden; kam mit `7ba6f7a` hinzu, drei Minuten vor dem Start von Run 3; für Run 4 einen Tag alt |
| Konzeptformen aus Dumps erschlossen, obwohl Doku-Tabellen und `get_concept_details` sie liefern | Z2 | vorhanden |
| `SaveWithMap` in ein `ExpressionStatement` gesetzt, `StaticRoleReference` als Ausdruck | Z2 | Struktur und Doku eindeutig; `dryRun` prüft Zuweisbarkeit |
| `DezimalLiteral` ohne Suffix `bd` | Z2 | in der Doku-Tabelle beschrieben |
| `PermissionHasReference` für Berechtigungsausdrücke | Z2 | fehlte in `7ba6f7a`, jetzt in `docu/objectflow.md` |
| Precondition mit Meldung, Service-Methode mit Validation, Command mit Pages nur über Dumps herausgefunden | Z3 | keine Muster |
| Registry, Platzhalter und erneutes Ernten in Run 3; Auflösungsschleifen bei langen Namensketten in Run 4 | Z4 | Ernten ist Standard |
| Festes `DateLiteral` wurde zum Serverdatum (Factory-Default, neu in MPS 2026.2) | Z5 | als Gotcha beschrieben |
| Modellimport auf `manmap.runtime` ohne Modulabhängigkeit | Z5 | offen |
| `this.`-Aufruf einer Service-Methode scheiterte erst in javac | – | in der Sprache gelöst: `this` ist in Services und Repositories nicht mehr möglich |
| wbkit-Config-Vorlage nicht gefunden; Component Scanning; JDBC-Treiber; DB-Zugang; VCS-Dialog | Z6 | Vorlage beschrieben, Rest offen |
