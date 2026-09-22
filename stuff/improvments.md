# Verbesserungsmaßnahmen für DSL-Dokumentation und Agenten-Skills

Dieses Dokument konkretisiert die vier priorisierten Verbesserungsmaßnahmen. Offene Entscheidungen sind als Fragen im Format `<<frage>>:` formuliert. Die Antwort kann jeweils direkt nach dem Doppelpunkt ergänzt werden.

## 1. Verbindlichkeit und Herkunft von Aussagen kennzeichnen

### Konkrete Verbesserung

Für Regeln in DSL-Dokumentationen und generierten DSL-Skills wird eine einheitliche Klassifikation eingeführt:

| Kennzeichnung | Bedeutung |
| --- | --- |
| `AST-MUSS` | Durch Struktur, Rolle oder Kardinalität des MPS-Metamodells vorgeschrieben |
| `MPS-CONSTRAINT` | Durch Constraint, Scope oder Typprüfung erzwungen |
| `GENERATOR` | Voraussetzung oder Verhalten des Generators |
| `RUNTIME` | Tatsächliches Verhalten einer konkreten Laufzeitimplementierung |
| `ARCHITEKTUR` | Projektweite fachliche oder technische Architekturregel |
| `EMPFEHLUNG` | Bewährte Vorgehensweise, aber nicht technisch erzwungen |

Jede nicht offensichtliche Regel soll erkennen lassen, aus welcher Kategorie sie stammt. Besonders wichtig ist das, wenn ein Konzept strukturell noch vorhanden ist, aber von Generator oder Runtime nicht mehr unterstützt wird. Beispiel: `onStartup` und `onShutdown` können im Metamodell vorhanden sein, obwohl die aktuelle Runtime sie nicht ausführt.

Runtime-Aussagen sollen zusätzlich die untersuchte Laufzeit und, soweit ermittelbar, deren Version oder Quellstand nennen. Wenn die Herkunft einer Aussage nicht sicher bestimmt werden kann, wird sie als ungeklärt markiert und nicht als MUSS-Regel formuliert.

### Offene Fragen

<<Sollen die Kennzeichnungen sowohl in den fachlichen DSL-Dokumentationen als auch in den generierten DSL-Skills verwendet werden?>>:

<<Sollen die vorgeschlagenen deutschen Kennzeichnungen verwendet werden, oder bevorzugst du kurze englische Bezeichnungen wie STRUCTURE, CONSTRAINT, GENERATOR, RUNTIME, ARCHITECTURE und RECOMMENDATION?>>:

<<Sollen die Kennzeichnungen direkt vor jeder einzelnen Regel stehen oder nur auf Abschnitts- und Tabellenzeilenebene verwendet werden?>>:

<<Soll für Runtime-Aussagen immer die konkrete Laufzeitvariante angegeben werden, beispielsweise FX8, H2Forms, TurkuForms oder Job-Runtime?>>:

<<Wie sollen widersprüchliche Quellen priorisiert werden, beispielsweise Metamodell erlaubt etwas, aber Runtime implementiert es nicht?>>:

## 2. Cross-DSL-Verträge explizit dokumentieren

### Konkrete Verbesserung

Übergänge zwischen ObjectFlow, ManMap und DataUX werden als überprüfbare Verträge dokumentiert. Ein Vertrag erhält ein einheitliches Schema:

- Quell-DSL und Ziel-DSL
- beteiligte Konzepte mit FQ-Namen
- strukturelle Referenzen und Child-Roles
- Voraussetzungen vor dem Übergang
- bereitgestellte Daten und Typen
- Session- und Lebensdaueranforderungen
- Regeln für Laden, Speichern und Conclusions
- Verhalten bei `null`, leerer Selektion oder nicht geladenen Referenzen
- erlaubte beziehungsweise typische Parameterquellen
- zuständige Validierung: MPS, Generator, Runtime oder Architekturprüfung
- mindestens ein positiver Referenzfall und ein typischer Fehlerfall

Mindestens folgende Verträge sollen beschrieben werden:

1. ObjectFlow `Command`/`Page` → DataUX `PagePane`
2. DataUX `MenuAction`/`MenuCompoundAction` → ObjectFlow `Command`
3. DataUX-Selektion → ObjectFlow-Command-Parameter
4. ObjectFlow Entity/DTO → ManMap Mapping und Repository
5. ManMap Query/Join → geladener ObjectFlow-Graph und Sessionzustand
6. ManMap Save/Delete → ObjectFlow-Aggregat, Schlüssel und Transaktionszustand
7. DataUX `BatchJobModule` → ObjectFlow Producer/Consumer-Pair und Exception-Strategie
8. `GRAPH_OWNER` → `GRAPH_EDIT` einschließlich Session, Aggregatgraph und Conclusions

Fremde DSL-Konzepte werden in einer DSL-Dokumentation im Fließtext immer mit FQ-Namen angegeben, wenn der Konzeptname in Klammern steht.

### Offene Fragen

<<Sollen die Cross-DSL-Verträge zentral in einer gemeinsamen Datei oder verteilt in den jeweils beteiligten DSL-Skills gepflegt werden?>>:

<<Falls die Verträge verteilt werden: Welche DSL soll bei einem Vertrag die führende beziehungsweise maßgebliche Beschreibung besitzen?>>:

<<Sollen die Verträge zusätzlich in den fachlichen Dateien dataux.md, manmap.md und einer ObjectFlow-Dokumentation erscheinen, oder nur in den Agenten-Skills?>>:

<<Welche weiteren Cross-DSL-Übergänge fehlen in der oben genannten Liste?>>:

<<Sollen Session-, Transaktions- und Aggregatregeln als verbindliche Architekturregeln behandelt werden, auch wenn MPS sie nicht vollständig prüfen kann?>>:

<<Sollen positive und negative Referenzmodelle aus realen Projektmodellen verwendet werden dürfen, sofern keine fachlichen Projektdaten in die Dokumentation übernommen werden?>>:

## 3. DataUX-Kompatibilitätsmatrizen erstellen

### Konkrete Verbesserung

Für DataUX werden getrennte Matrizen für strukturelle Zulässigkeit und tatsächliche Runtime-Unterstützung erstellt. Ein bloßes „in MPS modellierbar“ darf nicht mit „in jeder UI-Laufzeit funktionsfähig“ gleichgesetzt werden.

Geplante Matrizen:

1. Property-Typ → zulässige Delegate-Konzepte
2. Delegate-Konzept → zulässige Delegate-Optionen
3. Form/Table → zulässige Formular- und Tabellenoptionen
4. UI-Element → zulässige Parent- und Child-Rollen
5. UI-Element → Menüunterstützung
6. `Include` → überschreibbare Bestandteile
7. Command- und Parametertyp → geeignete Action-Form
8. Layout beziehungsweise UI-Muster → geeignete Geräteklasse
9. Feature → Unterstützung je Runtime-Frontend

Jeder Matrixeintrag erhält nach Möglichkeit einen Status:

- `MPS-erlaubt`
- `MPS-verboten`
- `Runtime-unterstützt`
- `Runtime-eingeschränkt`
- `Runtime-nicht unterstützt`
- `ungeklärt`

Die MPS-Zulässigkeit wird aus Live-Deskriptoren, Constraints, Typprüfung und validierten Referenzmodellen abgeleitet. Runtime-Aussagen werden aus Implementierung, Tests oder bestätigtem Projektwissen abgeleitet. Unbekannte Kombinationen werden nicht geraten.

### Offene Fragen

<<Für welche UI-Laufzeiten soll die erste Runtime-Matrix erstellt werden: FX8, H2Forms, TurkuForms oder weitere?>>:

<<Sollen unterschiedliche Versionen derselben UI-Laufzeit getrennt betrachtet werden?>>:

<<Soll die vollständige Matrix in dataux.md stehen oder als ausführliche Skill-Referenz geführt und in dataux.md nur zusammengefasst werden?>>:

<<Welche Property-Typen haben für die erste Delegate-Matrix höchste Priorität?>>:

<<Sollen projektspezifische Delegate- oder CustomElement-Implementierungen in dieselbe Matrix aufgenommen oder getrennt dokumentiert werden?>>:

<<Wie sollen Kombinationen behandelt werden, die MPS erlaubt, die aber nur in einzelnen Projekten oder Frontends funktionieren?>>:

<<Sollen Geräteklassen wie Desktop, MDE-Gerät, Tablet und Smartphone als eigene Kompatibilitätsdimension aufgenommen werden?>>:

