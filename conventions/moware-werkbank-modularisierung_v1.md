## Verbindliche Konventionen für den Aufbau einer Anwendung

Diese Konventionen sind der MoWare-Standard für den Aufbau einer Anwendung. Ein Projekt darf einzelne Konventionen abändern oder sie ganz durch eigene ersetzen. Es hält das in seiner `AGENTS.md` fest; dort steht, was abweicht und was stattdessen gilt. Steht dort nichts, gelten die Konventionen vollständig. Dateien unter `moai/` werden dafür weder geändert noch gelöscht.

### Bounded Contexts, Bereiche und Modelle

Eine Anwendung umfasst einen oder mehrere **Bounded Contexts**. Ein Bounded Context gliedert sich in **Bereiche**. Ein Bereich ist ein fachlich abgeschlossener Teil eines Bounded Context (im Sinne von DDD ein Module) und tritt in zwei Arten auf:

| Art | DDD-Schicht | geschnitten nach | Benennung | Beispiel |
| --- | --- | --- | --- | --- |
| **Aggregat-Bereich** | Domain Layer | Fachobjekt | Substantiv | `rechnung`, `kunde` |
| **Use-Case-Bereich** | Application Layer | fachlicher Ablauf | Tätigkeit | `rechnungsexport`, `mahnlauf` |

Ein Bereich besteht aus bis zu vier Modellen:

| Modell | Inhalt |
| --- | --- |
| `…<bereich>.domain` | Die Aggregate: Entities, die verändert werden, Value Objects und ihre `EntityMapping`s; das Aggregat-Repository mit Laden, Checkout, Speichern und Löschen; Regeln und Services, die ein Aggregat prüfen oder verändern |
| `…<bereich>.read` | Alles, was nur liest: Abfragen und lesende Repositories; Lesemodelle als DTO mit Custom SQL oder als gemappte Abfrage; read-only Entities mit Entity- oder No-Key-Mappern; Such- und Filter-DTOs; Regeln, Berechnungen und Services, die nur lesen |
| `…<bereich>.unit` | Commands (mit oder ohne Page) samt Pages, Page Panes und Menüs; DTOs, die nur einer Maske dienen |
| `…<bereich>.tests` | Tests der Regeln, der Persistenz, der Lesemodelle und der Commands; Service `TestDaten` |

Dazu kommen Modelle mit festem Namen:

| Modell | Inhalt |
| --- | --- |
| `<firma>.<app>.base` | Alle `OFXConfig`s einschließlich Test-Konfigurationen, Static Ressources |
| `<firma>.<app>.testbase` | Service `CS` |
| `<firma>.<app>.rollen` | Roles and Permissions |
| `…sharedvalues` | Status, Value Objects und Services darauf, die keinem Bereich gehören |
| `…gate.<fremdsystem>.read` | Anbindung eines Fremdsystems |
| `<firma>.<app>.app` | AppUI-Module, Batchjobs |

- **KONVENTION:** Jede Anwendung hat eine führende Solution `<firma>.<app>` mit den Modellen `base`, `testbase`, `rollen` und `app`. Bei einer kleinen Anwendung mit einem Bounded Context enthält sie alle Modelle. Bei mehreren Bounded Contexts liegt jeder in einer eigenen Solution `<firma>.<app>.<boundedcontext>`.
- **KONVENTION:** Bei einer Anwendung mit nur einem Bounded Context entfällt das Segment `<boundedcontext>` im Modellnamen: `<firma>.<app>.<bereich>.domain`.
- **KONVENTION:** Namen von Bounded Contexts und Bereichen sind deutsche Fachbegriffe, Aggregat-Bereiche als Substantiv, Use-Case-Bereiche als Tätigkeit. Technische Namen sind `base`, `testbase`, `rollen`, `sharedvalues`, `gate`, `domain`, `read`, `unit`, `tests` und `app`.
- **KONVENTION:** Modelle werden erst angelegt, wenn sie gebraucht werden. Ein Bereich muss nicht alle vier Modelle besitzen.

### Bereiche schneiden

- **KONVENTION:** Invarianten gehören zum Aggregat und werden am vollständig geladenen Aggregat geprüft. Reicht eine Regel über das Aggregat hinaus, wird zuerst geprüft, ob das Aggregat richtig geschnitten ist. Bleibt die Regel aggregatübergreifend, liegt sie in einem Service, der die nötigen Fakten liest.
- **KONVENTION:** Ein Aggregat-Bereich enthält in der Regel ein Aggregat. Mehrere Aggregate liegen in einem Bereich, wenn sie fachlich nur gemeinsam Sinn ergeben, also keines ohne die anderen verwendet wird. Der Bereich heißt nach dem führenden Aggregat, wenn die anderen ihm nur zuarbeiten, sonst nach dem Fachbegriff für das Ganze. Findet sich kein gemeinsamer Begriff, gehören die Aggregate in getrennte Bereiche. Jedes Aggregat bleibt eine eigene Konsistenzgrenze mit eigenem Repository.
- **KONVENTION:** Ein Use Case liegt in dem Bereich, zu dem er gehört, auch wenn er eigene DTOs, Commands oder einen eigenen Lese-Service mitbringt. Betrifft er zwei Bereiche und führt einer davon, liegt er im führenden Bereich; dessen Service liest die Fakten aus dem anderen.
- **KONVENTION:** Ein Use-Case-Bereich entsteht nur, wenn ein Ablauf mehrere eigenständige Bereiche gleichrangig verändert oder eigene Daten führt, die nur diesem Ablauf dienen.
- **KONVENTION:** Eine Übersicht liegt im `read` und `unit` des Bereichs, den sie zeigt und unter dem ein Benutzer sie suchen würde. Nur eine Auswertung, die mehrere eigenständige Bereiche gleichrangig zusammenführt, bekommt einen Use-Case-Bereich; er besteht dann aus `read` und `unit`.
- **KONVENTION:** Ein Use-Case-Bereich darf eigene Aggregate besitzen, wenn sie nur diesem Ablauf dienen, etwa ein Exportlauf mit seinen Positionen samt Mapping und Repository. Werden sie auch von anderen Bereichen benötigt, erhalten sie einen eigenen Aggregat-Bereich.
- **KONVENTION:** Ein Use-Case-Bereich verändert ein Aggregat nur über dessen Wurzel und Services.

### `domain`, `read` und `unit`

- **KONVENTION:** `domain` und `read` sind gleichrangiger ExpensiveCode und werden gleich sorgfältig getestet. Was ein Aggregat verändert oder seine Invarianten sichert, liegt im `domain`. Was nur liest, liegt im `read`, auch Regeln, Berechnungen und Services.
- **KONVENTION:** Das Aggregat-Repository im `domain` enthält nur Laden, Checkout, Speichern und Löschen des Aggregats. Alle weiteren Abfragen liegen im `read`, gleich ob sie der Anzeige oder einer Entscheidung dienen. Ein Service im `domain` darf Abfragen aus dem `read` verwenden.
- **KONVENTION:** Das `read` verwendet das `domain`, wo es passt: Ein Lesemodell darf Entities read-only laden, und ein No-Key-Mapper darf die Mappings der Entities einbinden. Verändert wird eine Entity nur über Checkout und Check-in des Aggregat-Repositories im `domain`.
- **KONVENTION:** Entities, die nur lesend verwendet werden, liegen im `read`. Das `read` darf dafür eine eigene, lesende Persistence Description haben.
- **KONVENTION:** Das `unit` enthält die Commands, die die fachliche Logik als Ablauf mit Session und gegebenenfalls Oberfläche ausführen, auch Commands ohne Page. Die Logik selbst liegt im `domain` oder im `read`.
- **KONVENTION:** Ein DTO, das nur einer Maske dient, ist CheapCode und liegt im `unit` bei seinem Command. Ein Service nimmt nie ein Masken-DTO entgegen; der Command übergibt die Werte einzeln. Ein DTO, das ein Service entgegennimmt oder ein Repository füllt, liegt im `read`; das gilt für alle Such- und Filter-DTOs.

### `sharedvalues`, `rollen` und Gates

- **KONVENTION:** Das Modell `sharedvalues` gehört zu einem Bounded Context und enthält Status, Value Objects und Services, die nur auf diesen Werten arbeiten. Es enthält nichts mit eigener Persistenz: keine Entities, keine Repositories. Hat ein Wert eine fachliche Heimat, bleibt er in deren Bereich. `sharedvalues` importiert nur `base`.
- **KONVENTION:** Das Modell `rollen` enthält die Roles and Permissions und darf von allen Modellen importiert werden. Es enthält keine Commands und keine Oberfläche. Eine einfache Benutzerverwaltung darf dazukommen: Benutzer-Entity und Repository liegen in `rollen`, ihre Commands und Pages in `rollen.unit`.
- **KONVENTION:** Ein Fremdsystem wird über ein Gate angebunden: `gate.<fremdsystem>.read`, benannt nach dem Fremdsystem. Darin liegen die read-only Entities mit Entity- oder No-Key-Mappern, die Abfragen und bei Bedarf Lese-Services. Das Gate ist die einzige Stelle, die Tabellen und Begriffe des Fremdsystems kennt; nach außen zeigt es Entities in der eigenen Fachsprache. Es importiert nur `base`, `sharedvalues` und `rollen`. Schreibt die Anwendung in das Fremdsystem, kommt `gate.<fremdsystem>.domain` dazu. Bei mehreren Bounded Contexts liegt ein Gate in dem Kontext, der es braucht.

### Abhängigkeiten

| Ebene | Modelle | importiert |
| --- | --- | --- |
| 1 | `base` | nichts |
| 2 | `rollen`, `sharedvalues`, Gates, `domain` und `read` aller Bereiche | Ebene 1 und Modelle der Ebene 2 |
| 3 | `unit` aller Bereiche | Ebenen 1 und 2; von anderen `unit`-Modellen nur deren Commands |
| 4 | `app` | alles |

- **KONVENTION:** Ein Modell importiert nie ein Modell einer höheren Ebene. Insbesondere importieren `domain` und `read` nie ein `unit` oder `app`.
- **KONVENTION:** Innerhalb eines Bounded Context dürfen Modelle derselben Ebene einander importieren, auch gegenseitig, wenn die Fachlichkeit zyklisch ist: `domain` und `read` desselben Bereichs, die `domain`-Modelle zweier Bereiche, zwei `unit`-Modelle.
- **KONVENTION:** Ein Aggregat-Bereich greift mit `domain` und `read` nie auf einen Use-Case-Bereich zu.
- **KONVENTION:** Ein `unit` darf die Commands jedes anderen `unit` starten, auch die eines Use-Case-Bereichs. Page Panes, Pages und Masken-DTOs eines anderen `unit` verwendet es nicht.
- **KONVENTION:** Zwischen Bounded Contexts gibt es keine Zyklen: Die Modelle zweier Kontexte importieren sich nicht gegenseitig. Braucht eine Regel einen Fakt aus einem Kontext, der selbst vom eigenen abhängt, liest ihn der Aufrufer und übergibt ihn dem Service.
- **KONVENTION:** `tests`-Modelle liegen in der Solution der Anwendung und dürfen alle Modelle importieren, auch andere `tests`. Nur `tests`-Modelle importieren `testbase` und andere `tests`. Braucht ein Test schreibende Mappings auf ein Fremdsystem, liegen sie in `gate.<fremdsystem>.tests`.

### Wohin gehört das?

| Was wird abgelegt? | Wohin |
| --- | --- |
| Entity, die verändert wird; ihr Mapping; Laden, Checkout, Speichern, Löschen | `<bereich>.domain` |
| Regel oder Service, der ein Aggregat prüft oder verändert | `<bereich>.domain` |
| Abfrage, Lesemodell, read-only Entity, Such- oder Filter-DTO | `<bereich>.read` |
| Regel, Berechnung oder Service, der nur liest | `<bereich>.read` |
| Command, Page, Page Pane, Menü, Masken-DTO | `<bereich>.unit` |
| Tests und Testdaten | `<bereich>.tests` |
| Status oder Value Object ohne fachliche Heimat | `sharedvalues` |
| Roles and Permissions | `rollen` |
| Daten eines Fremdsystems | `gate.<fremdsystem>.read` |
| Konfiguration, Ressourcen | `base` |
| AppUI-Modul, Batchjob | `app` |

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
