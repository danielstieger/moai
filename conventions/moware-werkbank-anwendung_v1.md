## Verbindliche Konventionen für den Aufbau einer Anwendung

Eine Anwendung umfasst einen oder mehrere **Bounded Contexts**; jeder Bounded Context ist eine MPS-Solution. Ein Bounded Context gliedert sich in **Bereiche**. Ein Bereich ist ein fachlich abgeschlossener Teil eines Bounded Context (im Sinne von DDD ein Module) und tritt in zwei Arten auf:

| Art | DDD-Schicht | geschnitten nach | Benennung | Beispiel |
| --- | --- | --- | --- | --- |
| **Aggregat-Bereich** | Domain Layer | Fachobjekt | Substantiv | `rechnung`, `kunde` |
| **Use-Case-Bereich** | Application Layer | fachlicher Ablauf | Tätigkeit | `rechnungsexport`, `mahnlauf` |

| Ebene | Solution | Modell | Inhalt | hängt ab von |
| --- | --- | --- | --- | --- |
| Basis | `<firma>.<app>.base` | `<firma>.<app>.base` | Alle `OFX Config`s einschließlich Test-Konfigurationen, Static Resources | – |
| | | `<firma>.<app>.testbase` | Service `CS` | `base` |
| Bounded Context, Aggregat-Bereich | `<firma>.<app>.<boundedcontext>` | `…<boundedcontext>.<aggregat>.domain` | Entities, Value Objects, Entity-Mappings, Repositories für Laden, Checkout und Speichern, allgemeine Domänenservices; im Bereich für Benutzer auch Roles and Permissions | `base`, andere Aggregat-`domain`s |
| | | `…<boundedcontext>.<aggregat>.read` | Lesemodelle: DTOs einschließlich Such- und Filter-DTOs, Custom-SQL-Abfragen, Row Mapper und No-Key-Mapper, Repositories nur zum Lesen | `base`, eigenes `domain` |
| | | `…<boundedcontext>.<aggregat>.unit` | Commands für Anlegen, Bearbeiten und Suchen des Aggregats (mit oder ohne Page) samt Pages, Page Panes und Menüs; die fachliche Logik liegt im `domain`-Modell | `base`, eigenes `domain` und `read` |
| | | `…<boundedcontext>.<aggregat>.tests` | Tests der fachlichen Regeln, der Persistenz und der Commands; Service `TestDaten` | `testbase`, eigenes `domain`, `read` und `unit` |
| Bounded Context, Use-Case-Bereich | `<firma>.<app>.<boundedcontext>` | `…<boundedcontext>.<usecase>.domain` | Anwendungsfallservices sowie eigene Aggregate des Ablaufs mit Entities, Value Objects, Mappings und Repositories | `base`, eigenes `read`, Aggregat-`domain`s und -`read`s |
| | | `…<boundedcontext>.<usecase>.read` | Lesemodelle des Ablaufs: DTOs, Custom-SQL-Abfragen, Row Mapper und No-Key-Mapper, Repositories nur zum Lesen | `base`, Aggregat-`domain`s und -`read`s |
| | | `…<boundedcontext>.<usecase>.unit` | Commands, Pages, Page Panes und Menüs des Ablaufs | `base`, eigenes `domain` und `read`, Aggregat-`domain`s, -`read`s und -`unit`s |
| | | `…<boundedcontext>.<usecase>.tests` | Tests des Ablaufs, insbesondere mit `run command`; Service `TestDaten` | `testbase`, eigene Modelle, Aggregat-`domain`s, -`read`s, -`unit`s und -`tests` |
| Anwendung | `<firma>.<app>.app` | `<firma>.<app>.app` | AppUI-Module, Batchjobs | alle |

- **KONVENTION:** Eine Anwendung ist nach obiger Tabelle in Solutions und Modelle gegliedert. Namen von Bounded Contexts und Bereichen sind deutsche Fachbegriffe, Aggregat-Bereiche als Substantiv, Use-Case-Bereiche als Tätigkeit. Die Schichtnamen `base`, `testbase`, `domain`, `read`, `unit`, `tests` und `app` sind technische Namen.
- **KONVENTION:** Abhängigkeiten verlaufen nur nach unten: `app` → `unit` → `read` → `domain` → `base`; `unit` darf auch direkt auf `domain` zugreifen; `tests` → `testbase`. Use-Case-Bereiche dürfen auf `domain`, `read`, `unit` und `tests` von Aggregat-Bereichen zugreifen, jeweils in ihrer Schicht, nie umgekehrt. Zwischen Bereichen und zwischen Bounded Contexts gibt es keine Zyklen.
- **KONVENTION:** Use-Case-Bereiche werden angelegt, wenn ein Ablauf mehrere Aggregate umfasst oder eigene DTOs, Lesemodelle, Services oder Commands benötigt, die nicht zum Aggregat selbst gehören.
- **KONVENTION:** Modelle werden erst angelegt, wenn sie gebraucht werden. Ein Bereich muss nicht alle vier Modelle besitzen; eine kleine Anwendung kommt oft ganz ohne Use-Case-Bereiche aus.
- **KONVENTION:** Ein Use-Case-Bereich darf eigene Aggregate besitzen, wenn sie nur diesem Ablauf dienen, etwa ein Exportlauf mit seinen Positionen samt Mapping und Repository. Werden sie auch von anderen Bereichen benötigt, erhalten sie einen eigenen Aggregat-Bereich.
- **KONVENTION:** Ein Use-Case-Bereich verändert ein Aggregat nur über dessen Wurzel und Services.
- **KONVENTION:** Die fachliche Logik eines Aggregats – Erzeugen, Ändern, Prüfen – liegt in dessen `domain`-Modell, als Methode am Aggregat oder als Domänenservice. Das `unit`-Modell enthält die Commands, die diese Logik als Ablauf mit Session und gegebenenfalls Oberfläche ausführen, auch Commands ohne Page. Mehrstufige Abläufe über mehrere Aggregate bilden einen Use-Case-Bereich.
