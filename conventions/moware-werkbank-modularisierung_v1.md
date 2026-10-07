## Verbindliche Konventionen für den Aufbau einer Anwendung

Diese Konventionen sind der MoWare-Standard für den Aufbau einer Anwendung. Ein Projekt darf einzelne Konventionen abändern oder sie ganz durch eigene ersetzen. Es hält das in seiner `AGENTS.md` fest; dort steht, was abweicht und was stattdessen gilt. Steht dort nichts, gelten die Konventionen vollständig. Dateien unter `moai/` werden dafür weder geändert noch gelöscht.

### Bounded Contexts und Bereiche

Eine Anwendung umfasst einen oder mehrere **Bounded Contexts**. Ein Bounded Context gliedert sich in **Bereiche**. Ein Bereich ist ein fachlich abgeschlossener Teil eines Bounded Context (im Sinne von DDD ein Module) und tritt in zwei Arten auf:

| Art | DDD-Schicht | geschnitten nach | Benennung | Beispiel |
| --- | --- | --- | --- | --- |
| **Aggregat-Bereich** | Domain Layer | Fachobjekt | Substantiv | `rechnung`, `kunde` |
| **Use-Case-Bereich** | Application Layer | fachlicher Ablauf | Tätigkeit | `rechnungsexport`, `mahnlauf` |

- **KONVENTION:** Jede Anwendung hat eine führende Solution `<firma>.<app>` mit den Modellen `base`, `rollen` und `app`. Bei einer kleinen Anwendung mit einem Bounded Context enthält sie alle Modelle. Bei mehreren Bounded Contexts liegt jeder in einer eigenen Solution `<firma>.<app>.<boundedcontext>`.
- **KONVENTION:** Bei einer Anwendung mit nur einem Bounded Context entfällt das Segment `<boundedcontext>` im Modellnamen: `<firma>.<app>.<bereich>.domain`.
- **KONVENTION:** Namen von Bounded Contexts und Bereichen sind deutsche Fachbegriffe, Aggregat-Bereiche als Substantiv, Use-Case-Bereiche als Tätigkeit. Technische Namen sind `base`, `rollen`, `sharedvalues`, `gate`, `domain`, `read`, `unit`, `tests` und `app`.
- **KONVENTION:** Modelle werden erst angelegt, wenn sie gebraucht werden. Ein Bereich muss nicht alle vier Modelle `domain`, `read`, `unit` und `tests` besitzen.

### Modelle

| Modell | Ebene | Inhalt | darf importieren | zu vermeiden |
| --- | --- | --- | --- | --- |
| `<firma>.<app>.base` | 1 | Alle `OFXConfig`s einschließlich Test-Konfigurationen, Static Ressources | nichts | – |
| `<firma>.<app>.rollen` | 2 | Roles and Permissions; bei Bedarf eine einfache Benutzerverwaltung mit Benutzer-Entity und Repository | Ebenen 1 und 2 | Commands und Oberfläche; die der Benutzerverwaltung liegen in `rollen.unit` |
| `…sharedvalues` | 2 | Status, Value Objects und Services, die nur auf diesen Werten arbeiten und keinem Bereich gehören; eines je Bounded Context | nur `base` | Entities, Repositories; Werte mit fachlicher Heimat, die bleiben in deren Bereich |
| `…gate.<fremdsystem>.read` | 2 | Anbindung eines Fremdsystems: read-only Entities mit Entity- oder No-Key-Mappern, Abfragen, bei Bedarf Lese-Services | nur `base`, `sharedvalues`, `rollen` | Tabellen und Begriffe des Fremdsystems außerhalb des Gates |
| `…<bereich>.domain` | 2 | Die Aggregate: Entities, die verändert werden, Value Objects und ihre `EntityMapping`s; das Aggregat-Repository mit Laden, Checkout, Speichern und Löschen; Regeln und Services, die ein Aggregat prüfen oder verändern | Ebenen 1 und 2 | weitere Abfragen im Aggregat-Repository; Zugriff auf Use-Case-Bereiche |
| `…<bereich>.read` | 2 | Alles, was nur liest: Abfragen und lesende Repositories; Lesemodelle als DTO mit Custom SQL oder als gemappte Abfrage; read-only Entities mit Entity- oder No-Key-Mappern, bei Bedarf mit eigener, lesender Persistence Description; Such- und Filter-DTOs; Regeln, Berechnungen und Services, die nur lesen | Ebenen 1 und 2 | Entities verändern; Zugriff auf Use-Case-Bereiche |
| `…<bereich>.unit` | 3 | Commands mit oder ohne Page samt Pages, Page Panes und Menüs; DTOs, die nur einer Maske dienen | Ebenen 1 und 2; die Commands jedes anderen `unit` | fachliche Logik, die liegt im `domain` oder `read`; Pages, Page Panes und Masken-DTOs eines anderen `unit` |
| `<firma>.<app>.app` | 4 | AppUI-Module, Batchjobs | alles | – |
| `…<bereich>.tests` | – | Tests der Regeln, der Persistenz, der Lesemodelle und der Commands; Service `TestDaten` | alles, auch andere `tests` und die Solution `org.modellwerkstatt.wbkit` | – |

### Abhängigkeiten

- **KONVENTION:** Ein Modell importiert nie ein Modell einer höheren Ebene. Insbesondere importieren `domain` und `read` nie ein `unit` oder `app`.
- **KONVENTION:** Innerhalb eines Bounded Context dürfen Modelle derselben Ebene einander importieren, auch gegenseitig, wenn die Fachlichkeit zyklisch ist: `domain` und `read` desselben Bereichs, die `domain`-Modelle zweier Bereiche, zwei `unit`-Modelle.
- **KONVENTION:** Zwischen Bounded Contexts gibt es keine Zyklen: Die Modelle zweier Kontexte importieren sich nicht gegenseitig. Braucht eine Regel einen Fakt aus einem Kontext, der selbst vom eigenen abhängt, liest ihn der Aufrufer und übergibt ihn dem Service.
- **KONVENTION:** `tests`-Modelle liegen in der Solution der Anwendung. Nur `tests`-Modelle importieren andere `tests`. Braucht ein Test schreibende Mappings auf ein Fremdsystem, liegen sie in `gate.<fremdsystem>.tests`.

### `domain`, `read`, `unit` und Gates

- **KONVENTION:** `domain` und `read` sind gleichrangiger ExpensiveCode und werden gleich sorgfältig getestet.
- **KONVENTION:** Alle Abfragen außer dem Laden des Aggregats liegen im `read`, gleich ob sie der Anzeige oder einer Entscheidung dienen. Ein Service im `domain` darf sie verwenden.
- **KONVENTION:** Das `read` verwendet das `domain`, wo es passt: Ein Lesemodell darf Entities read-only laden, und ein No-Key-Mapper darf die Mappings der Entities einbinden. Verändert wird eine Entity nur über Checkout und Check-in des Aggregat-Repositories im `domain`.
- **KONVENTION:** Ein DTO, das nur einer Maske dient, ist CheapCode und liegt im `unit` bei seinem Command. Ein Service nimmt nie ein Masken-DTO entgegen; der Command übergibt die Werte einzeln. Ein DTO, das ein Service entgegennimmt oder ein Repository füllt, liegt im `read`; das gilt für alle Such- und Filter-DTOs.
- **KONVENTION:** Ein Gate ist benannt nach dem Fremdsystem und zeigt nach außen Entities in der eigenen Fachsprache. Schreibt die Anwendung in das Fremdsystem, kommt `gate.<fremdsystem>.domain` dazu. Bei mehreren Bounded Contexts liegt ein Gate in dem Kontext, der es braucht.

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
| Aggregat-Repository | `domain` | `<Aggregat>Repo` |
| Service, der prüft oder verändert | `domain` | `<Aggregat>Service` |
| Persistence Description | `domain` | `<Bereich>Persistenz` |
| Lesende Persistence Description | `read` | `<Bereich>Lesen` |
| Lesendes Repository | `read` | `<Thema>LeseRepo` |
| Lese-Service | `read` | Substantiv für das, was er liefert, etwa `RechnungSuche` |
| Testsuite | `tests` | `<Bereich>Tests` |
| Testdaten | `tests` | `TestDaten` |
