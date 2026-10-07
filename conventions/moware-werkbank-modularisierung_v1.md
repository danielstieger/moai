## Verbindliche Konventionen für den Aufbau einer Anwendung

Diese Konventionen sind der MoWare-Standard für den Aufbau einer Anwendung. Was ein Projekt davon abändert, steht in seiner `AGENTS.md`.

### Bounded Contexts und Bereiche

Eine Anwendung umfasst einen oder mehrere **Bounded Contexts**. Ein Bounded Context gliedert sich in **Bereiche**. Ein Bereich ist ein fachlich abgeschlossener Teil eines Bounded Context (im Sinne von DDD ein Modul) und tritt in zwei Arten auf:

| Art | DDD-Schicht | geschnitten nach | Benennung | Beispiel |
| --- | --- | --- | --- | --- |
| **Aggregat-Bereich** | Domain Layer | Fachobjekt | Substantiv | `rechnung`, `kunde` |
| **Use-Case-Bereich** | Application Layer | fachlicher Ablauf | Tätigkeit | `rechnungsexport`, `mahnlauf` |

- **KONVENTION:** Namen von Bounded Contexts und Bereichen sind deutsche Fachbegriffe, Aggregat-Bereiche als Substantiv, Use-Case-Bereiche als Tätigkeit. Technische Namen sind `base`, `rollen`, `sharedvalues`, `gate`, `domain`, `read`, `unit`, `tests` und `app`.

### Solutions und Modelle

- **KONVENTION:** Die Anwendung hat die Solution `<firma>.<app>` mit den Modellen `base`, `rollen` und `app`. Bei einem Bounded Context enthält sie alle Modelle; bei mehreren liegt jeder Bounded Context in einer eigenen Solution `<firma>.<app>.<boundedcontext>`.
- **KONVENTION:** Modellnamen folgen dem Muster `<firma>.<app>.<boundedcontext>.<bereich>.<modell>`. `base`, `rollen` und `app` gehören zur Anwendung (`<firma>.<app>.base`), `sharedvalues` und `gate.<fremdsystem>.<modell>` zum Bounded Context, `domain`, `read`, `unit` und `tests` zum Bereich. Bei einem Bounded Context entfällt das Segment `<boundedcontext>`: `<firma>.<app>.rechnung.domain`.
- **KONVENTION:** Modelle werden erst angelegt, wenn sie gebraucht werden. Ein Bereich muss nicht alle vier Modelle `domain`, `read`, `unit` und `tests` besitzen.
- **KONVENTION:** `tests`-Modelle liegen in derselben Solution wie die Modelle, die sie testen, es sei denn, der Bounded Context hat eine eigene Test-Solution.

Die folgende Tabelle ist verbindlich: Ein Modell enthält, was unter „Inhalt“ steht, importiert höchstens, was unter „darf importieren“ steht, und nie, was unter „gehört nicht hinein“ steht.

| Modell | Ebene | Inhalt | darf importieren | gehört nicht hinein |
| --- | --- | --- | --- | --- |
| `<firma>.<app>.base` | 1 | Alle `OFXConfig`s einschließlich Test-Konfigurationen, Static Ressources | nichts | – |
| `<firma>.<app>.rollen` | 2 | Roles and Permissions; bei Bedarf eine einfache Benutzerverwaltung mit Benutzer-Entity und Repository | Ebenen 1 und 2 | Commands und Oberfläche |
| `<firma>.<app>.rollen.unit` | 3 | Commands, Pages und Page Panes der Benutzerverwaltung | wie `unit` | wie `unit` |
| `…sharedvalues` | 2 | Status, Value Objects und Services, die nur auf diesen Werten arbeiten und keinem Bereich gehören; eines je Bounded Context | nur `base` | Entities, Repositories; Werte mit fachlicher Heimat (sie bleiben in deren Bereich) |
| `…gate.<fremdsystem>.read` | 2 | Lesende Anbindung eines Fremdsystems: read-only Entities, gemappt mit `EntityMapping` oder `nokeystore/read-only map`; Abfragen; bei Bedarf Lese-Services | nur `base`, `sharedvalues`, `rollen` | – |
| `…gate.<fremdsystem>.domain` | 2 | Schreibende Anbindung eines Fremdsystems: `EntityMapping`s und Repository | wie `gate.<fremdsystem>.read` | – |
| `…<bereich>.domain` | 2 | Die Aggregate: Entities, die verändert werden, Value Objects und ihre `EntityMapping`s; das Aggregat-Repository mit Laden, Checkout, Speichern und Löschen; Regeln und Services, die ein Aggregat prüfen oder verändern | Ebenen 1 und 2 | weitere Abfragen im Aggregat-Repository |
| `…<bereich>.read` | 2 | Alles, was nur liest: Abfragen und lesende Repositories; Lesemodelle als DTO mit Custom SQL oder als gemappte Abfrage; read-only Entities, gemappt mit `EntityMapping` oder `nokeystore/read-only map`, bei Bedarf mit eigener, lesender Persistence Description; Such- und Filter-DTOs; Regeln, Berechnungen und Services, die nur lesen | Ebenen 1 und 2 | Code, der Entities verändert |
| `…<bereich>.unit` | 3 | Commands mit oder ohne Page samt Pages, Page Panes und Menüs; DTOs, die nur einem Command und seinen Page Panes dienen | Ebenen 1 und 2; von anderen `unit` nur deren Commands | fachliche Logik (gehört ins `domain` oder `read`) |
| `<firma>.<app>.app` | 4 | `AppUI Module`, `BatchJob Module` | Ebenen 1 bis 3 | – |
| `…<bereich>.tests` | – | Tests der Regeln, der Persistenz, der Lesemodelle und der Commands; Testdaten nach den [Konventionen für Tests](moware-werkbank-tests_v1.md) | alle Modelle der Anwendung, andere `tests`, Modelle der Solution `org.modellwerkstatt.wbkit` | – |
| `…gate.<fremdsystem>.tests` | – | Tests des Gates; schreibende Mappings auf das Fremdsystem, die nur Tests brauchen | wie `tests` | – |

### Abhängigkeiten

- **KONVENTION:** Ein Modell importiert nie ein Modell einer höheren Ebene. Insbesondere importieren `domain` und `read` nie ein `unit` oder `app`.
- **KONVENTION:** Innerhalb eines Bounded Context dürfen Modelle derselben Ebene einander importieren, auch gegenseitig, wenn die Fachlichkeit zyklisch ist (`domain` und `read` desselben Bereichs, die `domain`-Modelle zweier Bereiche, zwei `unit`-Modelle), soweit die Tabelle nichts anderes festlegt.
- **KONVENTION:** Ein Aggregat-Bereich greift mit `domain` und `read` nie auf einen Use-Case-Bereich zu.
- **KONVENTION:** Zwischen Bounded Contexts gibt es keine Zyklen: Die Modelle zweier Kontexte importieren sich nicht gegenseitig. Braucht eine Regel einen Fakt aus einem Kontext, der selbst vom eigenen abhängt, liest ihn der Aufrufer und übergibt ihn dem Service.
- **KONVENTION:** Nur `tests`-Modelle importieren andere `tests` und Modelle der Solution `org.modellwerkstatt.wbkit`.
- **KONVENTION:** Das Gate ist die einzige Stelle, die Tabellen und Begriffe des Fremdsystems kennt; nach außen zeigt es Entities in der eigenen Fachsprache. Bei mehreren Bounded Contexts liegt ein Gate in dem Kontext, der es braucht.

### `domain`, `read` und `unit`

- **KONVENTION:** `domain` und `read` sind gleichrangiger ExpensiveCode und werden gleich sorgfältig getestet.
- **KONVENTION:** Alle Abfragen außer dem Laden des Aggregats liegen im `read`, gleich ob sie der Anzeige oder einer Entscheidung dienen. Ein Service im `domain` darf sie verwenden.
- **KONVENTION:** Das `read` verwendet das `domain`, wo es passt: Ein Lesemodell darf Entities read-only laden, und eine `nokeystore/read-only map` darf die Mappings der Entities einbinden. Verändert wird eine Entity nur über Checkout und Check-in des Aggregat-Repositories im `domain`.
- **KONVENTION:** Ein DTO, das nur einem Command und seinen Page Panes dient, ist CheapCode und liegt im `unit` bei seinem Command. Ein Service nimmt ein solches DTO nie entgegen; der Command übergibt die Werte einzeln. Ein DTO, das ein Service entgegennimmt oder ein Repository füllt, liegt im `read`; das gilt für alle Such- und Filter-DTOs.

### Bereiche schneiden

- **KONVENTION:** Invarianten gehören zum Aggregat und werden am vollständig geladenen Aggregat geprüft. Reicht eine Regel über das Aggregat hinaus, wird zuerst geprüft, ob das Aggregat richtig geschnitten ist. Bleibt die Regel aggregatübergreifend, liegt sie in einem Service, der die nötigen Fakten liest.
- **KONVENTION:** Ein Aggregat-Bereich enthält in der Regel ein Aggregat. Mehrere Aggregate liegen in einem Bereich, wenn keines ohne die anderen verwendet wird. Der Bereich heißt nach dem führenden Aggregat, wenn die anderen ihm nur zuarbeiten, sonst nach dem Fachbegriff für das Ganze; findet sich keiner, gehören die Aggregate in getrennte Bereiche. Jedes Aggregat bleibt eine eigene Konsistenzgrenze mit eigenem Repository.
- **KONVENTION:** Ein Use Case liegt in dem Bereich, zu dem er gehört, auch mit eigenen DTOs, Commands oder Lese-Services. Betrifft er zwei Bereiche und führt einer davon, liegt er im führenden Bereich; dessen Service liest die Fakten aus dem anderen.
- **KONVENTION:** Ein Use-Case-Bereich entsteht nur, wenn ein Ablauf mehrere eigenständige Bereiche gleichrangig verändert oder eigene Daten führt, die nur diesem Ablauf dienen.
- **KONVENTION:** Eine Übersicht liegt im `read` und `unit` des Bereichs, den sie zeigt und unter dem ein Benutzer sie suchen würde. Nur eine Auswertung, die mehrere eigenständige Bereiche gleichrangig zusammenführt, bekommt einen Use-Case-Bereich aus `read` und `unit`.
- **KONVENTION:** Ein Use-Case-Bereich darf eigene Aggregate besitzen, wenn sie nur diesem Ablauf dienen, etwa ein Exportlauf mit seinen Positionen samt Mapping und Repository. Werden sie auch von anderen Bereichen benötigt, erhalten sie einen eigenen Aggregat-Bereich.
- **KONVENTION:** Ein Use-Case-Bereich verändert ein Aggregat nur über dessen Wurzel und Services.

### Empfehlung: Namen der Elemente

Die folgenden Namen sind eine Empfehlung. Wer abweicht, muss das nicht begründen.

| Element | Modell | Name |
| --- | --- | --- |
| Aggregat-Repository | `domain` | `<Aggregat>Repo`, ein Fugen-s ist erlaubt: `RechnungsRepo` |
| Service, der prüft oder verändert | `domain` | `<Aggregat>Service` |
| Persistence Description | `domain` | `<Bereich>Persistenz` |
| Lesende Persistence Description | `read` | `<Bereich>Lesen` |
| Lesendes Repository | `read` | `<Thema>LeseRepo` |
| Lese-Service | `read` | Substantiv für das, was er liefert, etwa `RechnungSuche` |
| Testsuite | `tests` | `<Bereich>Tests` |
