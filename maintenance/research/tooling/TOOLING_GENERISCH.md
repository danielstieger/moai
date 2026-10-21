# Skill-Anpassungen und generisches Tooling für MoAI – Ergebnis aus zwei Runs

Zwei unabhängige Runs haben mit MoAI und dem MPS-MCP je eine Anwendung gebaut. Beide sind auf dieselben zentralen
Probleme gestoßen und haben dafür dieselben Arten von Hilfsskripten geschrieben:

- **Run 3**: Fuhrpark (`2026_2/mjfuhrpark`), Skripte in `mjfuhrpark/example_tooling/`
- **Run 4**: Rechnungsverwaltung (`2026_2/rechnung`), Skripte und Begründung in `rechnung/example_tooling/` (`TOOLING.md`)

Dieses Dokument leitet daraus zwei Arten von Änderungen an MoAI ab: **angepasste Skills** (Inhalt und Struktur) und
**ein generisches Tooling**, das MoAI mitliefert. Beschrieben sind Fehlerklassen und Aufgaben, keine Einzelfälle und keine
Implementierung. Einzelfunde stehen nur als Belege im Anhang.

---

## Kurzfassung

- Es gibt **acht zentrale Probleme** (Abschnitt 2). Für jedes ist festgelegt, was Skills lösen, was Tooling löst und was nur der MCP-Server lösen kann.
- **Das meiste Wissen war schon da und wurde nicht gefunden.**
  - Doku-Tabellen nennen jedes Konzept mit Projektion.
  - `mps_mcp_get_concept_details` liefert die Struktur jedes Konzepts, `dryRun` prüft Rollen und Zuweisbarkeit.
  - `mps_dump.py` liest große Dumps.

  Beide Runs haben trotzdem Formen aus Dumps erraten und `mps_dump.py` nachgebaut. Das ist ein Problem der **Skill-Struktur**, nicht des Inhalts.
- **Skills allein reichen nicht.** Muster über mehrere Ebenen lassen sich als feste JSON-Vorlagen nicht zusammensetzen, und der
  Java-Parser kennt keine MoWare-Konstrukte.
- **Kern des Tooling ist ein generischer Builder.** Er nutzt die Struktur aller beteiligten Sprachen, die bei jedem MoAI-Release
  exportiert wird, und kennt kein Konzept fest. Von Hand gepflegt wird nur eine dünne Schicht für Muster über mehrere Ebenen.
- **Hauptweg für Methodenrümpfe:** Text mit Markern (Run 4) über dem generischen Builder.
- **Verhalten ändert sich mit der Version** (in MPS 2026.2 setzen Factories beim Einfügen Defaults). Dagegen hilft kein Katalog,
  sondern ein Soll-Ist-Vergleich nach dem Einfügen und ein Vergleich der Sprachstrukturen zwischen Releases.

---

## 1. Grundlage und Abgrenzung

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

| Werkzeugart | Run 3 | Run 4 | Schon in MoAI (beide Stände) |
| --- | --- | --- | --- |
| Blueprint-Builder für Strukturen und Ausdrücke | `gen.py`, `ex.py` | `bp.py` | – (feste Blueprints mit Platzhaltern) |
| Builder für Commands und Oberfläche | `ui.py` | Helfer in `build_unit.py` | – |
| Methodenrümpfe aus Text | – (bewusst umgangen) | `of_fix.py` + Marker-Konvention | – |
| Dump → Blueprint | `tobp.py` | `to_blueprint.py` | – |
| Baumansicht für Dumps | `shape.py` | `compact.py` | **`mps-mcp-workflow/scripts/mps_dump.py`** (`tree`, `node`, `shape`, `roots`) |
| Prüfberichte verdichten | – | `problems.py` | – |
| Referenzen aus Dumps ernten | `harvest.py`, `harvest2.py` | – | als Ablauf in `mps-baselanguage` vorgeschrieben |
| Struktur eines Konzepts | aus Dumps erraten | aus Dumps erraten | **`get_concept_details`** mit `detail: "shape"`/`"full"` |
| Prüfung von Rollen und Zuweisbarkeit | – | – | **`dryRun`** beim Insert |

**Abgrenzung:**
- Projekte ändern `moai/` nicht. Skills und Tooling sind Teil des MoAI-Pakets. Das Tooling wird nicht ins Projekt kopiert und schreibt nichts ins Projekt.
- Anwendungsspezifisches gehört weder in Skills noch ins Tooling: Namen von Rollen, Labels und Commands einer App.
- Was nur der MCP-Server sauber leisten kann, steht in Abschnitt 7. Das Tooling überbrückt es höchstens.

---

## 2. Die zentralen Probleme

| | Problem | Wie es sich zeigte | Skills | Tooling | MCP-Server |
| --- | --- | --- | --- | --- | --- |
| **Z1** | **Methodenrümpfe mit Fachlogik** | Der Parser kennt keine MoWare-Konstrukte (Business Properties, collections, Literale, Status, Preconditions, Komponentenaufrufe, Testerwartungen) und bindet gleichnamige Parameter anderer Methoden falsch. Der Skill schickt diesen Fall ins Hand-JSON. Run 3 baute Syntaxbäume in Python, Run 4 Java mit Markern und Reparatur. | Ablauf für Rümpfe | **Text → ObjectFlow** | Parser mit ObjectFlow-Kontext |
| **Z2** | **Vorhandenes Wissen wird nicht gefunden** | Projektionen und Konzepte stehen in den Doku-Tabellen, die Struktur liefert `get_concept_details`, Rollen prüft `dryRun`, Dumps liest `mps_dump.py`. Beide Agenten erschlossen Formen trotzdem aus Dumps und bauten `mps_dump.py` nach. | **Skill-Struktur**: ein Einstieg, vorhandene Werkzeuge zuerst | generischer Builder macht die Struktur direkt nutzbar | – |
| **Z3** | **Muster über mehrere Ebenen** | Struktur und `sampleNode` zeigen eine Ebene; der `sampleNode` ist ein Platzhalter, kein echtes Beispiel. Ein Konstrukt wie Precondition mit Meldung, eine Service-Methode mit Validation (6–15 KB JSON) oder ein Command mit Pages braucht mehrere Ebenen. Feste Vorlagen mit Platzhaltern decken nur Skelette ab. | Musterbeispiele | **generischer Builder + Muster-Schicht** | – |
| **Z4** | **Referenzen stabil setzen** | Der Skill verlangt, persistente Referenzen per `print_node` zu ernten. Run 3 folgte ihm (Registry, Platzhalter, erneutes Ernten nach dem Ersetzen). Run 4 löste über Namen auf und reparierte per Quick-Fix; bei langen Property-Ketten über fremde Entities gab es Auflösungsschleifen und Timeouts. `SET CHILD` vergibt neue IDs und bricht Referenzen auf ersetzte Member. | **neue Referenzregel** | Builder und Text → ObjectFlow setzen sie um | Insert liefert eine Karte von Namen auf Referenzen |
| **Z5** | **Verhalten ändert sich mit der Version** | In MPS 2026.2 laufen beim Einfügen aus JSON die Factories; früher war das ein Bug. Sie setzen Defaults, die gesetzte Werte überschreiben, und Importe ohne Modulabhängigkeit. Der Checker schweigt; erst ein Test oder der Build zeigt es. | Verhaltensänderungen je Release | **Soll-Ist-Vergleich**, Strukturvergleich zwischen Releases | Insert meldet von Factories geänderte Werte |
| **Z6** | **Umgebung und Setup** | Config-Vorlagen schwer zu finden bzw. nicht über Modellgrenzen kopierbar; Component Scanning zwischen Test und Produktiv; JDBC-Treiber fehlt; DB-Zugang unklar; VCS-Dialog blockiert MCP-Aufrufe; keine VM-Optionen in Run-Konfigurationen. | **Konventionen, Workflows, Installation** | Root kopieren, Config-Scaffold | `COPY_NODE` mit Zielmodell, VM-Optionen, modale Dialoge |
| **Z7** | **Kontextverbrauch** | Dumps und Prüfberichte mit 20–40 KB; der Parser liefert bei Marker-Code sehr große Antworten. | Verweis auf `mps_dump.py` an den Stellen, wo Dumps entstehen | **`mps_dump.py` ausbauen** | kompakte Ausgaben |
| **Z8** | **Wiederholte Konventionsmuster** | Commands, Page Panes, Such-DTOs, Owner/Edit-Paare und Configs folgen in jeder App denselben Regeln. Beide Runs schrieben dafür app-spezifische Skripte. | Konventionen (bestehen) | **Scaffolds** | – |

Hinzu kommt, dass Wissen zwischen den Runs verloren ging: Die Skripte von Run 3 lagen im Scratchpad und waren danach weg.
Das spricht dafür, das Tooling in MoAI zu versionieren, statt es Projekten zu überlassen.

---

## 3. Zwei Hebel und ihre Grenzen

**Was Skills lösen.**
- **Z2** ist das größte und billigste Feld. Die Information war vorhanden, aber auf Doku-Tabellen, drei Skills und ein Skript verteilt.
  Kein Skill führte beim Einstieg dorthin. Der Nachbau von `mps_dump.py` in beiden Runs ist der deutlichste Beleg.
- **Z4** hat ein Skill sogar verursacht: Die Vorgabe, Referenzen zu ernten, führte in Run 3 zu Registry, Platzhaltern und
  zusätzlichen `print_node`-Aufrufen.
- **Z5 und Z6** sind Wissen über Umgebung und Versionen, das ein Agent nicht selbst ableiten kann.

**Was Skills nicht lösen.**
- **Z1:** Der Parser kennt keine MoWare-Konstrukte.
- **Z3:** Auch ein perfekt dokumentiertes Muster für eine Service-Methode bleibt 15 KB JSON, und feste Vorlagen lassen sich nicht zusammensetzen.

Zwischen den Runs flossen Erkenntnisse aus Run 3 in MoAI ein. Run 4 hat trotzdem Builder und Parser-Reparatur noch einmal gebaut.

**Folgerung:**

| Reihenfolge | Hebel | Wirkt auf | Aufwand |
| --- | --- | --- | --- |
| 1 | Skills: Struktur, Abläufe, Umgebung | Z2, Z4, Z5, Z6, Z7 | gering, sofort |
| 2 | Generisches Tooling | Z1, Z2, Z3, Z5, Z7, Z8, Teile von Z6 | mittel |
| 3 | MCP-Server | Z1, Z4, Z5, Z6, Z7 dauerhaft | außerhalb von MoAI |

Skills und Tooling sind gekoppelt: Die Skills führen zum Wissen und beschreiben Regeln und Muster, das Tooling wendet sie an
und prüft sie. Das Tooling ersetzt keine fehlende Doku.

---

## 4. Skill-Anpassungen nach Fehlerklassen

Stand: MoAI `ac05213`. „Umgesetzt“ heißt, dass der Inhalt in diesem Stand vorhanden ist.

### 4.1 Skill-Struktur und Auffindbarkeit (Z2, Z7)

Ziel: Ein Agent findet vorhandenes Wissen und vorhandene Werkzeuge, bevor er selbst sucht, errät oder nachbaut.

| Anpassung | Stand |
| --- | --- |
| **Einheitlicher Einstieg „unbekanntes Konstrukt“** am Anfang jedes DSL-Skills, in allen gleich: Projektion in der Doku-Tabelle nachschlagen → Konzeptname → Struktur mit `get_concept_details` (`shape`) → echte Instanz suchen (`FIND_INSTANCES` im Paketbeispiel) → mit `mps_dump.py` lesen → Insert mit `dryRun`. | offen (die Schritte stehen einzeln in `mps-language-analysis`, `mps-mcp-workflow` und den Doku-Tabellen) |
| **Vorhandene Werkzeuge zuerst:** jeder DSL-Skill nennt die mitgelieferten Werkzeuge (`mps_dump.py`, später das Tooling aus Abschnitt 5) mit dem Satz „nicht nachbauen“. | offen (`mps_dump.py` steht nur in `mps-mcp-workflow`) |
| **Verweis an der Entstehungsstelle:** Wo ein Skill einen großen Dump erzeugen lässt (`print_node deep`, `get_concept_details` einer Sprache, Prüfberichte), steht der Aufruf von `mps_dump.py` direkt daneben. | offen |
| **Rollen der Teile festlegen:** `SKILL.md` = Einstieg und Abläufe; `references/` = Nachschlagen; Doku-Tabellen = Projektion → Konzept; Blueprints = aus dem Builder erzeugte Muster (5.2). Kein Wissen doppelt an zwei Orten. | offen |

### 4.2 Abläufe, die gegen die Erfahrung stehen (Z1, Z4)

| Anpassung | Stand |
| --- | --- |
| **Ablauf für Methodenrümpfe** in MoWare-Roots: Skelett → alle Methoden als Text in einem Parser-Aufruf → Dump → Text → ObjectFlow → `SET CHILD` je Member → Soll-Ist-Vergleich → Prüfung. Heute steht in `mps-baselanguage`: Rümpfe mit Business Properties, Status oder `#` entstehen als JSON. | offen (setzt Tooling voraus) |
| **Referenzregel statt Ernten:** standardmäßig über Namen. Persistent für Stubs, Überladungen, Ziele in fremden Modellen und lange Property-Ketten über fremde Entities. Ernten nur, wenn eine Auflösung über Namen nachweislich scheitert. | offen (heute ist Ernten der Standard) |
| **Identität erhalten:** Konstruktoren und Testmethoden nur über den Rumpf ersetzen; Methoden eines Roots gemeinsam ersetzen, damit Referenzen zwischen ihnen über Namen stimmen. | teilweise (Hinweis auf das Neuerzeugen beim Umschreiben ganzer Roots vorhanden) |
| **Reparatur nach der Auflösung über Namen:** `FIX_REFERENCES` und Quick-Fixes (`autoApplyQuickFixes`) im Ablauf nennen. | dokumentiert in `mps-mcp-workflow`, im Ablauf für Rümpfe offen |

### 4.3 Muster über mehrere Ebenen (Z3)

| Anpassung | Stand |
| --- | --- |
| **Auswahl der Muster nach Regel, nicht nach Fund:** Ein Muster bekommt jedes Konstrukt, dessen Pflichtrollen selbst wieder konzeptspezifische Knoten verlangen. Das lässt sich aus den exportierten Strukturen bestimmen (5.2). | offen |
| **Muster als Blueprints, erzeugt aus der Muster-Schicht des Builders** und mit ihm getestet; die heutigen festen Blueprints werden ersetzt. | offen |
| **Ein vollständiges Musterbeispiel je Aufgabe** (Aggregat, Service mit Regeln, Commands und Oberfläche, Tests) an zentraler Stelle in `sandbox.md`, etwa `org.modellwerkstatt.objectflow.tests.OrderDocument` für das Aggregat. | nur Einzelteile verlinkt |

### 4.4 Versionsabhängiges Verhalten (Z5)

| Anpassung | Stand |
| --- | --- |
| **Abschnitt „Verhaltensänderungen“ je MoAI-Release:** was sich gegenüber der Vorversion in MPS, MoWare oder MCP geändert hat, etwa dass Factories beim Einfügen jetzt laufen und Defaults setzen. | offen (der Einzelfall `DateLiteral` steht in den Gotchas) |
| **Soll-Ist-Vergleich im Ablauf:** nach jedem Insert prüfen, ob gesetzte Werte erhalten blieben (Tooling 5.2). | offen |
| **Modulabhängigkeiten nach dem Insert prüfen:** Factories können Importe setzen, ohne die Abhängigkeit anzulegen. | offen |

### 4.5 Umgebung und Setup (Z6)

| Anpassung | Stand |
| --- | --- |
| Config-Vorlagen in `wbkit.shared.configuration` | umgesetzt (Workflow OFXConfig) |
| Component Scanning: Test-Configs scannen zusätzlich `wbkit.shared.testing`, Produktiv-Configs schließen `tests` aus | offen |
| Klären, ob „`base` importiert nichts“ auch wbkit meint (Einbinden per `include section` oder Kopieren) | offen |
| JDBC-Treiber in die Anwendungs-Solution einbinden (Bibliothek in der Java-Facet) | offen |
| DB-Zugang für Tests: wo `${DB_*}` gesetzt wird, Verweis auf die vorhandene lokale Test-Config | offen |
| `INSTALL_INSTRUCTIONS.md`: VCS so einstellen, dass neue Dateien ohne Dialog aufgenommen werden; Plugin-Registrierung ohne absoluten Pfad | offen |
| Fachliche Objekte nicht löschen, sondern einen Status vorsehen | umgesetzt (`mw-domaenenmodell`) |

---

## 5. Generisches Tooling

### 5.1 Übersicht: wofür jedes Werkzeug primär gebraucht wird

| Werkzeug | Aufgabe in einem Satz | Primär gebraucht, weil … | Ohne das Werkzeug | Entfällt, wenn … | Stufe |
| --- | --- | --- | --- | --- | --- |
| **Struktur-Export** | exportiert bei jedem MoAI-Release die Struktur aller beteiligten Sprachen als versionierte Daten | der Builder offline arbeiten soll und Sprachänderungen sichtbar werden müssen (Z2, Z5) | Formen aus Dumps erraten; Änderungen fallen erst im Run auf | nie: er ist die Grundlage | 1 |
| **Generischer Builder** | baut jeden Knoten jeder Sprache aus den exportierten Strukturen und prüft ihn dabei | Blueprints wortreich sind und Rollen, Kardinalitäten und Zuweisbarkeit sonst erst beim Insert auffallen (Z2, Z3) | Hand-JSON oder handgeschriebene Bausteine je Konzept | nie: bleibt die Basis | 1 |
| **Muster-Schicht** | bietet Kurzformen für Muster über mehrere Ebenen | Struktur und `sampleNode` nur eine Ebene zeigen (Z3) | Muster je Run aus Dumps erschlossen | der MCP-Server Muster liefert (nicht absehbar) | 2 |
| **Soll-Ist-Vergleich** | prüft nach dem Insert, ob gesetzte Werte und Referenzen erhalten blieben | Factories Werte still überschreiben können (Z5) | Fehler erst im Test oder Build | der Insert geänderte Werte selbst meldet | 1 |
| **`mps_dump.py` (Ausbau)** | liest Dumps, Blueprints und Prüfberichte kompakt, gefiltert und gruppiert | große Antworten den Kontext füllen (Z7) | Nachbau in jedem Run | der MCP-Server kompakte Ausgaben liefert | 1 |
| **Root kopieren** | übernimmt einen Root aus einem anderen Modell als Blueprint, mit Auswahl, Umbenennung und Ersetzung | der MCP-Server nicht über Modellgrenzen kopiert (Z6) | Konvertierung je Run, Referenzen zeigen ins Quellmodell | `COPY_NODE` ein Zielmodell kennt | 1 |
| **Text → ObjectFlow** | macht aus Java-nahem Text mit Markern korrekte Knoten | der Parser keine MoWare-Konstrukte kennt (Z1) | jeder Rumpf als Syntaxbaum oder viele `update_node` | der MCP-Parser ObjectFlow-Kontext kennt | 2 |
| **Scaffolds** | erzeugen konventionskonforme Grundgerüste aus einer kleinen Spezifikation | sich Konventionsmuster in jeder App wiederholen (Z8) | app-spezifische Einzelskripte je Run | nie: Mehrwert über dem MCP-Server | 3 |

**Nicht übernommen:**
- die Referenz-Registry aus Run 3: Die Referenzregel (4.2) macht sie überflüssig;
- handgeschriebene Bausteine je Konzept (beide Runs): Sie werden durch den generischen Builder ersetzt;
- eine Prüfung gegen einen Katalog von Einzelfällen: An ihre Stelle treten Struktur aus dem Export, `dryRun` und Soll-Ist-Vergleich.

### 5.2 Aufgaben je Werkzeug

**Struktur-Export**
- Bei jedem MoAI-Release `get_concept_details` mit `detail: "full"` für alle beteiligten Sprachen abfragen:
  ObjectFlow, ManMap, DataUX, BaseLanguage, collections, closures und die Sprachen, von denen sie erben (etwa `jetbrains.mps.lang.core`).
- Je Konzept ablegen:
  - Name, Abstraktheit, Superkonzept und Super-Interfaces;
  - Properties mit Typ und Enum-Werten;
  - Referenzen und Kinder mit Zielkonzept und Kardinalität.
- Daraus die vollständige Konzepthierarchie über die Sprachgrenzen berechnen. Damit ist offline entscheidbar, ob ein Konzept in eine Rolle passt.
- Den Sprachstand (MPS, MoWare, Modul-Versionen) im Export vermerken.
- Den Unterschied zum vorigen Export ausgeben: neue, geänderte und entfallene Konzepte und Rollen. Daraus entstehen die
  Verhaltensänderungen in den Skills (4.4) und die Liste der zu prüfenden Muster.
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
- Referenzen nach der Regel aus 4.2 setzen: über Namen, wo sie eindeutig auflösen, sonst persistent.
- Persistente Referenzen auf häufig gebrauchte Java-Stubs der Laufzeitmodule bereitstellen, beim Release mit dem Export erzeugt.
- Keine Namen einer Anwendung.

**Muster-Schicht**
- Kurzformen für Muster über mehrere Ebenen, gebaut über den generischen Builder. Beispiele:
  - Precondition mit Meldung;
  - Service-Methode mit Regeln;
  - Command mit Pages und Conclusions;
  - Custom SQL als Text mit markierten Variablen und Status-Konstanten;
  - Testmethode mit erwarteter Ausnahme.
- Welche Muster nötig sind, folgt aus der Regel in 4.3. Ob ein Muster mit der aktuellen Sprache noch passt, zeigt der Unterschied der Exporte.
- Erzeugt die Blueprints, die in den Skills als Beispiele stehen.

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

**Text → ObjectFlow**
- Methodenrümpfe in Java-nahem Text annehmen. Was dabei ausdrückbar sein muss, ergibt sich aus den Konstrukten, die in Methodenrümpfen
  vorkommen dürfen; laut Export sind das alle Konzepte, die in Statement- und Expression-Rollen passen.
- Die Ausgabe des Parsers über den generischen Builder in Blueprints je Member umsetzen und die Art der Methode festlegen
  (normal, Service, Repository mit Typ).
- Identität erhalten: Konstruktoren und Testmethoden nur über den Rumpf ersetzen.
- Abbrechen und den Ort nennen, statt still Falsches zu erzeugen: bei unbekannten Markern, unaufgelösten Bezeichnern und mehrdeutigen Bindungen.
- Die Marker-Konvention ist verbindlich im Skill dokumentiert: je Marker Zielkonstrukt, Beispiel, Grenzen.

**Scaffolds**
- Aus einer kleinen Spezifikation in einem einzigen Bulk-Insert konventionskonforme Grundgerüste erzeugen:
  - Aggregat;
  - Suche;
  - Owner- und Edit-Commands;
  - Statusübergang;
  - Configs für Test und FX8.
- Die Konventionen stecken im Generator. Abweichungen eines Projekts (`AGENTS.md`) lassen sich in der Spezifikation ausdrücken.

### 5.3 Laufzeitregeln für alle Werkzeuge

- Python-Standardbibliothek, offline, Aufruf mit `python3 -I` (wie `mps_dump.py`).
- Eingaben und Ausgaben als Dateien im Temp-Verzeichnis, das die MCP-Tools lesen; kein Zustand im Arbeitsverzeichnis.
- Keine Projektreferenzen im Werkzeug.
- Jedes Werkzeug nennt den Sprachstand, gegen den es geprüft ist; der Builder liest ihn aus dem Export.

---

## 6. Vergleich der Runs und Entscheidungen

| Bereich | Run 3 | Run 4 | Entscheidung |
| --- | --- | --- | --- |
| **Bausteine** | handgeschrieben je Konzept, breiter Umfang | handgeschrieben je Konzept, flexiblere Grundform | **weder noch:** generischer Builder aus dem Struktur-Export; von Hand nur die Muster-Schicht |
| **Methodenrümpfe** | Syntaxbaum in Python; eindeutig, aber Fachlogik schwer lesbar | Java mit Markern → Parser → Reparatur; dicht und prüfbar, aber heuristisch | **Text mit Markern als Hauptweg**, Knoten über den generischen Builder; Abbruch statt stiller Fehlbindung |
| **Referenzen** | Ernten in eine Registry (wie vom Skill verlangt) | Namen, persistent nach außen und für Überladungen, Quick-Fix | **Namen als Standard** mit klaren Ausnahmen (4.2); Registry entfällt |
| **Identität beim Ersetzen** | nicht geregelt | Konstruktoren und Tests nur über den Rumpf | **Regel von Run 4**, in Skill und Werkzeug |
| **Dump → Blueprint** | Namen; Defaults weggelassen | Namen; Auswahl, Umbenennen, Ersetzen | **Run 4**, ergänzt um das Weglassen von Defaults aus Run 3 |
| **Custom SQL** | Liste aus Wörtern und Token | Fließtext mit markierten Variablen und Status | **Run 4**, als Teil der Muster-Schicht |
| **Commands und Oberfläche** | Bausteine mit festen App-Namen | Bulk-Insert eines Modells, app-spezifisch | **Bulk-Insert je Modell**; App-Spezifisches gehört in die Spezifikation der Scaffolds |
| **Diagnose** | eigene Baumansicht | eigene Baumansicht + Verdichtung der Prüfberichte | **`mps_dump.py` ausbauen**; beide Nachbauten waren unnötig |
| **Prüfung** | – | – | **Struktur im Builder, `dryRun`, Soll-Ist-Vergleich** statt Katalog von Einzelfällen |
| **Ablage** | Scratchpad, verloren | Projektordner, dokumentiert | **versioniert in MoAI** |

**Gemeinsam:** Beide Runs haben Konzeptformen an Beispiel-Roots gelernt und im Code festgehalten, statt die Sprachstruktur abzufragen.
Diesen Schritt übernehmen künftig Struktur-Export und Skill-Einstieg.

**Trennend im Kern:** Run 3 umgeht MPS bei der Auflösung, Run 4 lässt MPS auflösen und repariert danach. Übernommen wird Run 4,
mit der Strenge von Run 3: Was mehrdeutig ist, wird persistent gesetzt oder führt zum Abbruch.

---

## 7. Was in den MCP-Server gehört

| Erweiterung | Macht überflüssig |
| --- | --- |
| Parser mit ObjectFlow-Kontext (Business Properties, collections, Literale, Status, Precondition, Stubs aus den Modulabhängigkeiten) | Text → ObjectFlow |
| Insert meldet, welche Werte Factories gesetzt oder geändert haben | Soll-Ist-Vergleich |
| Insert liefert eine Karte von Namen auf Referenzen der neuen Knoten | jedes Ernten von Referenzen |
| `COPY_NODE` mit Zielmodell | Root kopieren |
| Kompakte, gefilterte Ausgabe für `print_node`, `responseDetail: summary` für Parser und Prüfberichte | Teile von `mps_dump.py` |
| VM-Optionen in Run-Konfigurationen, Erkennen modaler Dialoge, gleiche Namensauflösung bei ADD und DELETE von Modellimporten | – (kein Werkzeug möglich) |

---

## 8. Umsetzung

| Stufe | Inhalt | Voraussetzung |
| --- | --- | --- |
| **0 – Skills** | Skill-Struktur und Einstieg (4.1), Referenzregel und Identität (4.2), Umgebung und Setup (4.5) | keine |
| **1 – Basis-Tooling** | Struktur-Export, generischer Builder, Soll-Ist-Vergleich, Ausbau von `mps_dump.py`, Root kopieren; Verhaltensänderungen (4.4) aus dem ersten Export-Vergleich | Stufe 0 |
| **2 – Muster und Rümpfe** | Muster-Schicht und daraus erzeugte Blueprints (4.3), Text → ObjectFlow mit Marker-Konvention, Ablauf für Rümpfe (4.2) | Stufe 1 |
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
- Getrennt gemessen wird ein Lauf nur mit Stufe 0, um die Wirkung der Skill-Struktur allein zu sehen.

---

## 9. Offene Fragen und Risiken

- **Umfang des Exports:** Welche Sprachen genau nötig sind, damit die Hierarchie vollständig ist (geerbte Konzepte aus `lang.core` und
  weiteren), zeigt erst der erste Export.
- **`sampleNode`:** Er ist ein synthetischer Platzhalter mit einer Ebene und taugt nicht als Muster. Echte Muster kommen aus der Muster-Schicht
  und den Paketbeispielen.
- **Marker-Konvention:** Sie stammt aus einem Run. Vor der Festschreibung prüfen, ob sie alle in Rümpfen zulässigen Konstrukte abdeckt und
  für Agenten eindeutig ist.
- **Grenze der Auflösung über Namen:** Wann Ketten zu lang werden, ist nur beobachtet, nicht ausgemessen.
- **Abgrenzung zum MCP-Server:** Text → ObjectFlow lohnt sich nur, wenn der ObjectFlow-Parser nicht absehbar kommt.
- **Scaffolds und Konventionen:** Ein Generator schreibt Konventionen fest. Lassen sich Abweichungen nicht ausdrücken, umgehen Agenten ihn.

---

## Anhang: Belege aus den Runs

Einzelfunde, die zu den Fehlerklassen geführt haben. Sie sind Belege, kein Arbeitsprogramm.

| Fund | Klasse | Stand `ac05213` |
| --- | --- | --- |
| `mps_dump.py` in beiden Runs nachgebaut (`shape.py`, `compact.py`) | Z2, Z7 | Skript seit `7ba6f7a` vorhanden |
| Konzeptformen aus Dumps erschlossen, obwohl Doku-Tabellen und `get_concept_details` sie liefern | Z2 | vorhanden |
| `SaveWithMap` in ein `ExpressionStatement` gesetzt, `StaticRoleReference` als Ausdruck | Z2 | Struktur und Doku eindeutig; `dryRun` prüft Zuweisbarkeit |
| `DezimalLiteral` ohne Suffix `bd` | Z2 | in der Doku-Tabelle beschrieben |
| `PermissionHasReference` für Berechtigungsausdrücke | Z2 | fehlte in `7ba6f7a`, jetzt in `docu/objectflow.md` |
| Precondition mit Meldung, Service-Methode mit Validation, Command mit Pages nur über Dumps herausgefunden | Z3 | keine Muster |
| Registry, Platzhalter und erneutes Ernten in Run 3; Auflösungsschleifen bei langen Namensketten in Run 4 | Z4 | Ernten ist Standard |
| Festes `DateLiteral` wurde zum Serverdatum (Factory-Default) | Z5 | als Gotcha beschrieben |
| Modellimport auf `manmap.runtime` ohne Modulabhängigkeit | Z5 | offen |
| `this.`-Aufruf einer Service-Methode scheiterte erst in javac | – | in der Sprache gelöst: `this` ist in Services und Repositories nicht mehr möglich |
| wbkit-Config-Vorlage nicht gefunden; Component Scanning; JDBC-Treiber; DB-Zugang; VCS-Dialog | Z6 | Vorlage beschrieben, Rest offen |
