## Verbindliche Konventionen

- **KONVENTION:** Unsere Ubiquitous Language ist Deutsch. Alles, was Fachlichkeit in der Software ausdrückt, wird konsistent mit deutschen Fachbegriffen benannt – insbesondere Namespaces, Datenmodelle, Services, Methoden, etc.

### Aufbau einer Anwendung

Eine Anwendung umfasst einen oder mehrere **Bounded Contexts**; jeder Bounded Context ist eine MPS-Solution. Ein Bounded Context gliedert sich in **Bereiche**. Ein Bereich ist ein fachlich abgeschlossener Teil eines Bounded Context (im Sinne von DDD ein Module) und tritt in zwei Arten auf:

| Art | DDD-Schicht | geschnitten nach | Benennung | Beispiel |
| --- | --- | --- | --- | --- |
| **Aggregat-Bereich** | Domain Layer | Fachobjekt | Substantiv | `rechnung`, `kunde` |
| **Use-Case-Bereich** | Application Layer | fachlicher Ablauf | Tätigkeit | `rechnungsexport`, `mahnlauf` |

| Ebene | Solution | Modell | Inhalt | hängt ab von |
| --- | --- | --- | --- | --- |
| Basis | `<firma>.<app>.base` | `<firma>.<app>.base` | Alle `OFX Config`s einschließlich Test-Konfigurationen, Static Resources | – |
| | | `<firma>.<app>.testbase` | Service `CS` | `base` |
| Bounded Context, Aggregat-Bereich | `<firma>.<app>.<boundedcontext>` | `…<boundedcontext>.<aggregat>.domain` | Entities, Value Objects, Mappings, Repositories, allgemeine Domänenservices, generische DTOs; im Bereich für Benutzer auch Roles and Permissions | `base`, andere Aggregat-`domain`s |
| | | `…<boundedcontext>.<aggregat>.unit` | Commands für Anlegen, Bearbeiten und Suchen des Aggregats (mit oder ohne Page) samt Pages, Page Panes und Menüs; die fachliche Logik liegt im `domain`-Modell | `base`, eigenes `domain` |
| | | `…<boundedcontext>.<aggregat>.tests` | Tests der fachlichen Regeln, der Persistenz und der Commands; Service `TestDaten` | `testbase`, eigenes `domain` und `unit` |
| Bounded Context, Use-Case-Bereich | `<firma>.<app>.<boundedcontext>` | `…<boundedcontext>.<usecase>.domain` | Anwendungsfallservices, DTOs und Lesemodelle des Ablaufs, auch Repositories mit Custom SQL, Row Mapper oder No-Key-Mapper | `base`, Aggregat-`domain`s |
| | | `…<boundedcontext>.<usecase>.unit` | Commands, Pages, Page Panes und Menüs des Ablaufs | `base`, eigenes `domain`, Aggregat-`domain`s und -`unit`s |
| | | `…<boundedcontext>.<usecase>.tests` | Tests des Ablaufs, insbesondere mit `run command`; Service `TestDaten` | `testbase`, eigenes `domain` und `unit`, Aggregat-`domain`s, -`unit`s und -`tests` |
| Anwendung | `<firma>.<app>.app` | `<firma>.<app>.app` | AppUI-Module, Batchjobs | alle |

- **KONVENTION:** Eine Anwendung ist nach obiger Tabelle in Solutions und Modelle gegliedert. Namen von Bounded Contexts und Bereichen sind deutsche Fachbegriffe, Aggregat-Bereiche als Substantiv, Use-Case-Bereiche als Tätigkeit. Die Schichtnamen `base`, `testbase`, `domain`, `unit`, `tests` und `app` sind technische Namen.
- **KONVENTION:** Abhängigkeiten verlaufen nur nach unten: `app` → `unit` → `domain` → `base`, sowie `tests` → `testbase`. Use-Case-Bereiche dürfen auf `domain`, `unit` und `tests` von Aggregat-Bereichen zugreifen, jeweils in ihrer Schicht, nie umgekehrt. Zwischen Bereichen und zwischen Bounded Contexts gibt es keine Zyklen.
- **KONVENTION:** Use-Case-Bereiche werden angelegt, wenn ein Ablauf mehrere Aggregate umfasst oder eigene DTOs, Lesemodelle, Services oder Commands benötigt, die nicht zum Aggregat selbst gehören. Kleine Anwendungen mit wenigen solchen Abläufen kommen mit Aggregat-Bereichen aus.
- **KONVENTION:** Ein Use-Case-Bereich besitzt keine eigenen Aggregate. Braucht ein Ablauf eigenen dauerhaften Zustand mit fachlichen Regeln, ist das ein neues Aggregat und damit ein eigener Aggregat-Bereich.
- **KONVENTION:** Ein Use-Case-Bereich verändert ein Aggregat nur über dessen Wurzel und Services.
- **KONVENTION:** Die fachliche Logik eines Aggregats – Erzeugen, Ändern, Prüfen – liegt in dessen `domain`-Modell, als Methode am Aggregat oder als Domänenservice. Das `unit`-Modell enthält die Commands, die diese Logik als Ablauf mit Session und gegebenenfalls Oberfläche ausführen, auch Commands ohne Page. Mehrstufige Abläufe über mehrere Aggregate bilden einen Use-Case-Bereich.
