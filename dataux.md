# DataUX (org.modellwerkstatt.dataux) - Benutzeroberflächen und ausführbare Module

## Modellierungsumfang und Ausdrucksmöglichkeiten

`org.modellwerkstatt.dataux` ist eine der drei domänenspezifischen Sprachen der **modellwerkstatt moware werkbank**. Sie beschreibt Benutzeroberflächen und den ausführbaren Rahmen von Anwendungen und Batchjobs. (Im Folgenden bezeichnet **Name** die Bezeichnung, die in MPS typischerweise sichtbar ist oder eingegeben wird. Der **Konzeptname** ist die technische AST-Bezeichnung und steht jeweils in Klammern. Bei einem DataUX-Konzept genügt dort der kurze Konzeptname; gehört das angesprochene Konzept zu einer anderen DSL, steht in Klammern immer dessen **FQ-Name**. Die Konzepttabellen führen FQ-Namen zusätzlich explizit auf – primär für KI-Agenten.)

DataUX verbindet zwei Aufgabenbereiche:

1. **UI-Modellierung:** Eine Oberfläche wird aus fachlich gebundenen `Page Pane`s (`PagePane`), Formularen, Tabellen, Layouts und Aktionen aufgebaut.
2. **Application / Batchjob:** Ausführbare Module konfigurieren den Start und das Ende einer Anwendung, Authentifizierung, Navigation beziehungsweise Batch-Verarbeitung und die zugehörige Laufzeitkonfiguration.

Die Sprache beschreibt vor allem, **welche fachlichen Daten wie visualisiert werden**. Generator und Laufzeit übernehmen die technische Umsetzung. An dafür vorgesehenen Stellen können BaseLanguage-Ausdrücke eingebettet werden, etwa für Beschriftungen, Farben, Bedingungen, Command-Argumente oder Lebenszykluslogik.

## Teil I – UI-Modellierung

### Page Panes

Eine ObjectFlow-`Page` gehört zu einem `Command` und beschreibt eine Seite seines Interaktionsablaufs. Ein `Page Pane` (`PagePane`) ist das Gegenstück auf der UI-Seite: Es beschreibt den sichtbaren Inhalt dieser Page.

Ein `Page Pane` besitzt genau ein oberstes UI-Element. Dieses kann unmittelbar ein `Delegate Form` (`DelegateForm`) oder eine `Table` (`Table`) sein. Sollen mehrere Elemente kombiniert werden, bildet ein `Grid Layout` (`GridLayout`) oder `Tab Layout` (`TabLayout`) das oberste Element. Zusätzlich kann das `Page Pane` Menüeinträge enthalten.

Die Page stellt die Daten bereit; das `Page Pane` stellt sie dar. Eine UI-Bindung lädt keine Daten nach. Benötigte Referenzen und Listen müssen bereits durch den Command beziehungsweise seine Repositories geladen und an die Page übergeben worden sein.

#### Konzeptlandkarte der UI-Komposition

| Name | Konzeptname | FQ-Name | Rolle |
| --- | --- | --- | --- |
| `Page Pane` | `PagePane` | `org.modellwerkstatt.dataux.structure.PagePane` | UI-Beschreibung für eine ObjectFlow-Page mit genau einem obersten UI-Element |
| `Delegate Form` | `DelegateForm` | `org.modellwerkstatt.dataux.structure.DelegateForm` | Formular aus typgerechten Property-Delegates |
| `Table` | `Table` | `org.modellwerkstatt.dataux.structure.Table` | Tabelle für eine gebundene Liste aus Entities oder DTOs |
| `Grid Layout` | `GridLayout` | `org.modellwerkstatt.dataux.structure.GridLayout` | Raster aus Zeilen und Spalten mit einem oder mehreren UI-Elementen |
| `Tab Layout` | `TabLayout` | `org.modellwerkstatt.dataux.structure.TabLayout` | Container für mehrere Tabs |
| `Tab` | `Tab` | `org.modellwerkstatt.dataux.structure.Tab` | Beschrifteter Tab mit genau einem UI-Element |
| `Include` | `Include` | `org.modellwerkstatt.dataux.structure.Include` | Einbindung eines bereits deklarierten bindbaren UI-Elements |
| `Custom UI Element` | `CustomElement` | `org.modellwerkstatt.dataux.structure.CustomElement` | Projektspezifisches UI-Element mit eigener Implementierungsklasse |

`Delegate Form`, `Table`, `Grid Layout`, `Tab Layout` und `Custom UI Element` können sowohl innerhalb eines `Page Pane`s als auch als eigenständige, wiederverwendbare Root Nodes deklariert werden.

#### Datenbindung und Selektion

DataUX bindet UI-Komponenten an fachliche Typen und deren Properties. Ein bindbares Element spezifiziert einen Entity- oder DTO-Typ (`boundClassifier`) und optional eine Property dieses Typs (`boundProperty`). Fehlt eine explizite Bindung, kann der Kontext vom umgebenden Element übernommen werden.

Jedes `Page Pane` besitzt einen gemeinsamen **Selektionskontext**. Für jeden darin verwendeten Entity- oder DTO-Typ kann eine aktuell selektierte Instanz existieren. Diese Selektion gehört nicht einer einzelnen Tabelle oder einem einzelnen Formular, sondern steht allen Komponenten des `Page Pane`s zur Verfügung.

##### Typbindung

Eine Bindung nur an einen Entity- oder DTO-Typ verwendet grundsätzlich die aktuelle Selektion dieses Typs. Ein an `Rechnung` gebundenes `Delegate Form` zeigt beispielsweise die aktuell selektierte `Rechnung`.

Wird einem `Page Pane` auf Root-Ebene genau eine Instanz seines Root-Typs bereitgestellt – unmittelbar oder als Liste mit genau einem Element –, ist diese Instanz automatisch selektiert. Ein direkt an den Root-Typ gebundenes Formular kann sie deshalb ohne eine Tabelle mit `SELECT FIRST` unmittelbar anzeigen. Diese automatische Selektion gilt für das Root-Objekt; eine untergeordnete Liste wird nicht allein deshalb selektiert, weil sie nur ein Element enthält.

##### Property-Bindung

Eine Property-Bindung wird auf der aktuellen Selektion ihres Eigentümertyps ausgewertet. Bei einer selektierten `Rechnung` bezeichnet die Bindung `Rechnung.kunde` das `kunde`-Objekt genau dieser Rechnung. Ein `Delegate Form` kann so an eine Property gebunden werden, deren Typ eine Entity, ein DTO oder ein Value Object ist.

Das Formular liest diesen Bindungskontext, erzeugt oder verändert aber keine Selektion. Ein an `Rechnung.kunde` gebundenes Formular hängt daher nicht an einer eventuell vorhandenen `Kunde`-Selektion, sondern zeigt ausschließlich den `kunde` der aktuell selektierten `Rechnung`.

##### Tabellenbindung und Selektion

Eine `Table` benötigt eine Liste von Entities oder DTOs. Listen von Value Objects sind kein Tabellen-Bindungsmodell in DataUX.

Ist der Zeilentyp mit dem Root-Typ des `Page Pane`s identisch, kann die Tabelle direkt an diesen Typ gebunden werden und verwendet den Root-Datenbestand. Soll die Tabelle Objekte eines anderen Typs anzeigen, wird sie an eine Listen-Property eines selektierten Objekts gebunden. Eine Tabelle für `Rechnung.positionen` zeigt somit die Positionen der aktuell selektierten Rechnung; ihr Zeilentyp ist `Rechnungsposition`, nicht `Rechnung`.

Die Auswahl einer Tabellenzeile bestimmt die gemeinsame Selektion des Zeilentyps. Mit `SELECT FIRST` (`SelectFirstFOption`) kann eine Tabelle beim initialen Anzeigen das erste Element selektieren und so eine abhängige Detaildarstellung initialisieren.

Mehrere Tabellen mit demselben Zeilentyp teilen dieselbe Selektion. Enthält eine andere Tabelle dieselbe Laufzeitinstanz, markiert sie diese ebenfalls. Enthält sie die Instanz nicht, zeigt sie keine ausgewählte Zeile; die gemeinsame Selektion bleibt erhalten. Maßgeblich ist dieselbe Laufzeitinstanz, nicht nur eine gleiche fachliche ID oder fachliche Gleichheit. Durch die Session-Integration von Entities und DTOs ist die Instanz innerhalb der Session eindeutig.

##### Leere Selektion

Für einen Entity- oder DTO-Typ kann keine Instanz selektiert sein. Ein ausschließlich an diesen Typ gebundenes Formular zeigt dann keine Daten. Tabellen können ihre Zeilen weiterhin darstellen, obwohl keine Zeile ausgewählt ist.

##### Master-Detail

Der gemeinsame Selektionskontext ermöglicht Master-Detail-Oberflächen ohne explizite Synchronisationslogik zwischen den Komponenten. Eine Rechnungsseite kann beispielsweise aus einer Tabelle der `Rechnung`-Objekte, einer Tabelle für `Rechnung.positionen` und einem Formular für die ausgewählte `Rechnungsposition` bestehen.

Die Bindungskette lautet sinngemäß:

`selektierte Rechnung -> positionen -> ausgewählte Rechnungsposition -> Detailformular`

Das Detailformular muss nicht wissen, aus welcher Tabelle die Selektion stammt. Auch beim Wechsel des Masters ist keine zusätzliche Synchronisationslogik erforderlich; die Laufzeit wertet abhängige Bindungen und Selektionen im gemeinsamen Kontext aus.

### Formulare, Tabellen und Delegates

Ein `Delegate Form` (`DelegateForm`) beschreibt ein Formular. Seine Bindung bestimmt das dargestellte Objekt, seine Delegates bestimmen die sichtbaren Felder und seine Spaltengewichte deren horizontale Aufteilung. Eine `Table` (`Table`) beschreibt eine Objektliste; ihre Delegates bilden die Spalten.

Der Delegate-Typ folgt dem fachlichen Property-Typ. Ein Delegate ersetzt keine fachliche Validierung. Fachliche Regeln gehören in das Domänenmodell beziehungsweise in Services und Commands; Delegate- und Formularoptionen steuern Darstellung und Interaktion.

#### Konzeptlandkarte der Delegates

| Name | Konzeptname | FQ-Name | Typischer Zweck |
| --- | --- | --- | --- |
| `String` | `StringDelegate` | `org.modellwerkstatt.dataux.structure.StringDelegate` | Text-Property |
| `Integer` | `IntegerDelegate` | `org.modellwerkstatt.dataux.structure.IntegerDelegate` | Ganzzahlige Property |
| `BigDecimal` | `BigDecimalDelegate` | `org.modellwerkstatt.dataux.structure.BigDecimalDelegate` | Dezimalzahl |
| `DateTime` | `DateTimeDelegate` | `org.modellwerkstatt.dataux.structure.DateTimeDelegate` | Datum und Uhrzeit |
| `DateTime (Date Only)` | `DateTimeDateOnlyDelegate` | `org.modellwerkstatt.dataux.structure.DateTimeDateOnlyDelegate` | Nur Datumskomponente eines DateTime-Werts |
| `LocalDate` | `LocalDateDelegate` | `org.modellwerkstatt.dataux.structure.LocalDateDelegate` | Lokales Datum |
| `Status` | `StatusDelegate` | `org.modellwerkstatt.dataux.structure.StatusDelegate` | ObjectFlow-Statuswert |
| `Reference` | `ReferenceDelegate` | `org.modellwerkstatt.dataux.structure.ReferenceDelegate` | Referenz auf ein fachliches Objekt; die mit `scopeText` festgelegte Kurzbeschreibung bestimmt den im Dropdown angezeigten Text |
| `Image` | `ImageDelegate` | `org.modellwerkstatt.dataux.structure.ImageDelegate` | Bilddarstellung, nur im Formular |
| `Upload` | `UploadDelegate` | `org.modellwerkstatt.dataux.structure.UploadDelegate` | Datei-Upload, nur im Formular |
| `Dummy` | `DummyDelegate` | `org.modellwerkstatt.dataux.structure.DummyDelegate` | Platzhalter zur Anordnung von Formularfeldern |

#### Delegate-Optionen

| Name | Konzeptname | FQ-Name | Element | Wirkung |
| --- | --- | --- | --- | --- |
| `DISABLED` | `DisabledDOption` | `org.modellwerkstatt.dataux.structure.DisabledDOption` | Formular | Delegate ist nicht editierbar |
| `OPTIONAL` | `OptionalDOption` | `org.modellwerkstatt.dataux.structure.OptionalDOption` | Formular | Wert darf fehlen beziehungsweise `null` sein |
| `PICKER` | `PickerDOption` | `org.modellwerkstatt.dataux.structure.PickerDOption` | Formular | Verwendet nach Möglichkeit eine Auswahlkomponente |
| `ISSUE UPDATE/SCANABLE` | `IssueUpdateDOption` | `org.modellwerkstatt.dataux.structure.IssueUpdateDOption` | Formular | Löst eine verfügbare Update-Conclusion aus |
| `HOOK` | `DelegateHookDOption` | `org.modellwerkstatt.dataux.structure.DelegateHookDOption` | Formular | Bindet projektspezifische Delegate-Logik ein |
| `FORCE NUMERIC EDITOR` | `ForceNumericEditor` | `org.modellwerkstatt.dataux.structure.ForceNumericEditor` | Formular | Verwendet für einen `StringDelegate` einen numerischen Editor |
| `ALTER` | `AlternativeDOption` | `org.modellwerkstatt.dataux.structure.AlternativeDOption` | Formular | Verwendet für einen `ReferenceDelegate` oder `StatusDelegate` einen alternativen Editor, sofern die Laufzeitumgebung diesen unterstützt |
| `WIDE` | `WideDOption` | `org.modellwerkstatt.dataux.structure.WideDOption` | Formular | Blendet nach Möglichkeit das Label links vom Editor aus und gibt dem Editor die gesamte Breite |
| `OVERWRITE LABEL` | `OverwriteLabelDOption` | `org.modellwerkstatt.dataux.structure.OverwriteLabelDOption` | Formular und Tabelle | Überschreibt die von der Datenstruktur vorgegebene Beschriftung |
| `OVERWRITE FORMAT` | `OverwriteFormatDOption` | `org.modellwerkstatt.dataux.structure.OverwriteFormatDOption` | Formular und Tabelle | Überschreibt das von der Datenstruktur vorgegebene Format |
| `WIDTH` | `WidthDOption` | `org.modellwerkstatt.dataux.structure.WidthDOption` | Tabelle | Legt die Breite der Spalte fest |
| `EDITABLE` | `EditableDOption` | `org.modellwerkstatt.dataux.structure.EditableDOption` | Tabelle | Property wird editierbar dargestellt |
| `IMPORTANT` | `ImportantDOption` | `org.modellwerkstatt.dataux.structure.ImportantDOption` | Tabelle | Hebt ein wichtiges Tabellenfeld hervor |
| `COLOR` | `DynColorDOption` | `org.modellwerkstatt.dataux.structure.DynColorDOption` | Tabelle | Berechnet die Farbe dynamisch aus dem Wert |
| `LONG DESC` | `StatusLongDescDOption` | `org.modellwerkstatt.dataux.structure.StatusLongDescDOption` | Tabelle | Verwendet die Langbeschreibung eines Status |
| `FOLD` | `FoldDOption` | `org.modellwerkstatt.dataux.structure.FoldDOption` | Tabelle | Blendet die Spalte zunächst aus; der Benutzer kann sie per Doppelklick auf den Spaltenkopf einblenden |

Weitere Delegate-Optionen steuern unter anderem Ausrichtung, mehrzeilige Darstellung, Fokus und dynamische Scopes. Vor dem Einsatz muss geprüft werden, ob die Option für den konkreten Delegate- und Property-Typ zulässig ist.

#### Optionen für Formulare und Tabellen

| Name | Konzeptname | FQ-Name | Element | Wirkung |
| --- | --- | --- | --- | --- |
| `DISABLED` | `DisabledFOption` | `org.modellwerkstatt.dataux.structure.DisabledFOption` | Formular | Formular ist nicht editierbar |
| `LABEL` | `LabelFOption` | `org.modellwerkstatt.dataux.structure.LabelFOption` | Formular und Tabelle | Setzt die Beschriftung des Elements |
| `SELECT FIRST` | `SelectFirstFOption` | `org.modellwerkstatt.dataux.structure.SelectFirstFOption` | Tabelle | Selektiert das erste Tabellenelement bei der Initialisierung |
| `SELECTION SUMMARY LINE` | `SelectionSummaryLineFOption` | `org.modellwerkstatt.dataux.structure.SelectionSummaryLineFOption` | Tabelle | Berechnet eine Zusammenfassung für ausgewählte Tabellenobjekte |
| `TABLE SUMMARY LINE` | `TableSummaryLineFOption` | `org.modellwerkstatt.dataux.structure.TableSummaryLineFOption` | Tabelle | Berechnet eine Zusammenfassung über alle Tabellenobjekte |
| `CUSTOM CSV EXPORT` | `TableCustomCsvExportFOption` | `org.modellwerkstatt.dataux.structure.TableCustomCsvExportFOption` | Tabelle | Passt den CSV-Export an |

### Layouts, Tabs und Wiederverwendung

Ein `Grid Layout` (`GridLayout`) ordnet UI-Elemente in Zeilen und Spalten an. Zeilen- und Spaltengewichte bestimmen die Größenverteilung. Die sichtbaren Gewichte `-1`, `1*`, `2*`, `3*`, `4*` und `5*` werden durch `MinWeight`, `OneWeight`, `TwoWeight`, `ThreeWeight`, `FourWeight` und `FiveWeight` repräsentiert. So kann beispielsweise eine Tabelle links und ein Formular rechts oder ein kompaktes Suchformular oberhalb einer flexiblen Ergebnistabelle stehen. Dieselben Gewichte werden auch im `Delegate Form` als Spaltengewichte verwendet, dort jedoch ohne `MinWeight`.

Für ein `Grid Layout` stehen insbesondere folgende Optionen zur Verfügung:

| Name | Konzeptname | FQ-Name | Wirkung |
| --- | --- | --- | --- |
| `FLEXIBLE` | `FlexibleOption` | `org.modellwerkstatt.dataux.structure.FlexibleOption` | Erlaubt eine flexible Größenanpassung |
| `FOCUS FORWARD 2` | `SkipFocusOption` | `org.modellwerkstatt.dataux.structure.SkipFocusOption` | Verschiebt den initialen Fokus auf ein späteres Element |

Ein `Tab Layout` (`TabLayout`) enthält mindestens einen `Tab` (`Tab`). Jeder Tab besitzt eine als Ausdruck modellierte Beschriftung und genau ein UI-Element.

Mit `Include` (`Include`) wird ein bereits deklariertes bindbares UI-Element wiederverwendet. Die Einbindung muss zur Datenbindung des umgebenden Kontexts passen. Sie erzeugt weder zusätzliche Daten noch einen unabhängigen Selektionsraum. Eine explizite Bindung am Include oder am eingebundenen Element kann den geerbten Kontext gezielt anpassen.

Ein `Custom UI Element` (`CustomElement`) bindet eine projektspezifische UI-Implementierung ein. Es ist für Darstellungsfälle gedacht, die Form, Tabelle und Layouts nicht ausdrücken. Die fachliche Datenbindung, Delegates und Menüaktionen bleiben Teil des DataUX-Modells; nur die konkrete Darstellung wird projektspezifisch implementiert.

Die Zielgeräte sind bei der Layoutwahl ausdrücklich mitzudenken. Eine breite Desktop-Aufteilung ist nicht automatisch für mobile Datenerfassungsgeräte oder Smartphones geeignet. Für unterschiedliche Geräteklassen können eigene `Page Pane`s erforderlich sein.

### Menüs und Command-Aktionen

Ein `Page Pane` (`PagePane`) und eine `Table` (`Table`) besitzen Menüs, deren fachlicher Bezug unterschiedlich ist:

- Das Menü einer Tabelle richtet sich vor allem an die gebundenen Tabellenobjekte. Seine Aktionen arbeiten typischerweise mit der aktuell ausgewählten Zeile oder mit mehreren ausgewählten Zeilen.
- Das Menü eines `Page Pane`s gehört zum gesamten Seitenkontext. Seine Aktionen betreffen daher eher das gebundene Wurzelobjekt, den vollständigen Aggregatgraphen oder den übergreifenden Ablauf der Page.

Auch für ein `Custom UI Element` (`CustomElement`) kann ein Menü modelliert werden. Ob und wie es sichtbar und bedienbar ist, hängt jedoch davon ab, ob die konkrete UI-Laufzeitkomponente diese Menüintegration unterstützt. Ein `Include` (`Include`) kann eigene Menüeinträge angeben und damit das Menü des eingebundenen Elements am jeweiligen Verwendungsort überschreiben. Das ist insbesondere beim Einbinden einer Tabelle oder eines Custom Elements nützlich.

#### Konzeptlandkarte der Menüs

| Name | Konzeptname | FQ-Name | Aufgabe |
| --- | --- | --- | --- |
| `Action` | `MenuAction` | `org.modellwerkstatt.dataux.structure.MenuAction` | Ruft einen ObjectFlow-Command mit optionalem Label und Argumenten auf |
| `Compound Action` | `MenuCompoundAction` | `org.modellwerkstatt.dataux.structure.MenuCompoundAction` | Verkettet mehrere Command-Aufrufe anhand ihrer Page-Conclusions |
| kein eigener Alias | `PageConclusionReference` | `org.modellwerkstatt.dataux.structure.PageConclusionReference` | Referenziert die Abschlussart, unter der die Aktionskette fortgesetzt wird |
| `USER_CANCEL` | `PageConclusionOptionUserCancel` | `org.modellwerkstatt.dataux.structure.PageConclusionOptionUserCancel` | Behandelt einen Benutzerabbruch als Fortsetzungsfall |
| `Submenu` | `MenuSub` | `org.modellwerkstatt.dataux.structure.MenuSub` | Gruppiert weitere Menüeinträge |
| `- - - -` | `MenuSeparator` | `org.modellwerkstatt.dataux.structure.MenuSeparator` | Trennt Menügruppen optisch |

Ein Menü beginnt üblicherweise mit einem `Submenu` (`MenuSub`). Die Oberfläche stellt diese Gruppe als Overflow-Menü dar, vergleichbar mit dem bekannten Android-Muster. Nur wenige, außergewöhnlich wichtige Aktionen sollten direkt auf der obersten Ebene stehen; zu viele Top-Level-Aktionen nehmen Platz ein und verwässern die Priorisierung.

Eine `Action` (`MenuAction`) referenziert einen ObjectFlow-`Command`. Die im Command definierte Standardparametrisierung gilt auch für eine Action, sodass sie ohne explizite Argumente modelliert werden kann. Nur wenn der Aufrufkontext andere Werte verlangt, überschreibt die Action einzelne beziehungsweise alle Argumente mit Ausdrücken. Typische Quellen dafür sind:

- `getSelected()` (`org.modellwerkstatt.objectflow.structure.SelectedObject`) für das aktuell ausgewählte Objekt,
- `getSelectedObjects()` (`org.modellwerkstatt.objectflow.structure.SelectedList`) für die ausgewählten Objekte einer Mehrfachselektion,
- Konstanten für fest vorgegebene Aufrufvarianten.

Menüaktionen arbeiten immer im aktuellen UI-Kontext. Bei Tabellenaktionen ist deshalb typischerweise die Selektion des Zeilentyps maßgeblich; bei Page-Pane-Aktionen steht meist das gebundene Wurzelobjekt oder der gesamte Seitenablauf im Vordergrund. Das schränkt den Zugriff aber nicht auf diese Typen ein: An jeder Aktionsstelle kann mit einem typisierten `getSelected(...)` die gemeinsame Selektion eines beliebigen im `Page Pane` verwendeten Typs abgefragt werden, beispielsweise `getSelected(RechnungsSubPosition)` direkt in einer Page-Pane-Aktion.

Vor dem Modellieren einer Aktion ist deshalb zu klären:

- Welcher Typ ist an der Aufrufstelle selektiert?
- Welche Command-Parameter müssen befüllt werden?
- Soll die Aktion global, in einem Submenü oder nur an der fokussierten Komponente angeboten werden?

Eine `Compound Action` (`MenuCompoundAction`) verbindet einen `GRAPH_OWNER` optional mit einem anschließenden `GRAPH_EDIT`. Wird für den `GRAPH_OWNER` unmittelbar eine Page-Conclusion angegeben, kann er ohne sichtbare UI bis zu diesem Abschluss ausgeführt werden. Zusätzlich kann die Compound Action in derselben Session und mit den vom Owner bereitgestellten Daten direkt einen `GRAPH_EDIT` starten. Sowohl für den `GRAPH_OWNER` als auch für den `GRAPH_EDIT` lässt sich optional eine automatische Conclusion angeben.

Damit kann beispielsweise aus einem Suchergebnis heraus eine Aktion auf einem vollständigen Aggregat ausgeführt werden: Der `GRAPH_OWNER` öffnet das ausgewählte Objekt, lädt den Aggregatgraphen vollständig und stellt die Session bereit. Anschließend führt der `GRAPH_EDIT` die fachliche Änderung aus. Dessen Conclusion bestätigt die Änderung; die Conclusion des Owners speichert und schließt den Aggregatgraphen. Ohne nachgelagerten `GRAPH_EDIT` eignet sich dasselbe Muster auch dazu, einen `GRAPH_OWNER` vollständig ohne UI auszuführen.

`PageConclusionReference` verweist dabei auf eine Abschlussart, d.h. das `Command` muss diese Conclusion deklarieren; `USER_CANCEL` (`PageConclusionOptionUserCancel`) modelliert einen Abbruch des Commands mit "cancel" (Analog einem Benutzerabbruch).

### Typischer UI-Modellierungsablauf

1. Der ObjectFlow-Command und seine Pages legen fest, welche Daten und Aktionen der Ablauf benötigt.
2. Für jede Page wird der Root-Typ der UI bestimmt.
3. Das `Page Pane` (`PagePane`) erhält diesen Entity- oder DTO-Typ als Bindungskontext.
4. Das oberste UI-Element wird gewählt: Formular, Tabelle oder Layout.
5. Formulare und Tabellen werden an Typen beziehungsweise geeignete Properties gebunden.
6. Tabellen können über die Auswahl ihrer Zeilen Selektionen für weitere UI-Komponenten bestimmen.
7. Typgerechte Delegates beschreiben Felder und Tabellenspalten.
8. Menüs rufen Commands mit Argumenten aus dem aktuellen Bindungs- und Selektionskontext auf.

## Teil II – Application / Batchjob

`AppUI Module` (`AppUiModule`) und `BatchJob Module` (`BatchJobModule`) sind ausführbare Einstiegspunkte. Die fachlichen Anwendungsfälle verbleiben in Commands, Services und Repositories.

Die Referenz `configuration` dient ausschließlich dem Start mit FX8, aus MPS oder im Standalone-Betrieb; im regulär bereitgestellten Laufzeitkontext ist sie nicht die Anwendungskonfiguration. Die in beiden Konzepten noch vorhandenen Bereiche `onStartup` und `onShutdown` sind nicht mehr zu verwenden (Deprecated).

### Application mit `AppUI Module` (`AppUiModule`)

Ein `AppUI Module` (`AppUiModule`) beschreibt eine interaktive Anwendung. Neben Benutzerkontext und Modulmetadaten besitzt es Navigation und Einstiegspunkte:

- `mainMenu` bildet das fachliche Start- beziehungsweise Hauptmenü.
- `extrasMenu` nimmt ergänzende, seltener benötigte Funktionen auf.
- `helpMenu` bündelt Hilfe- und Dokumentationsaktionen.
- `Tile` (`AppTile`) sind die Kacheln/Schaltflächen auf der Startoberfläche mit einer `Action` (`MenuAction`) sowie optional dynamischem Text und dynamischer Farbe.
- `tileInit` (`TileInitFunction`) initialisiert Werte, die für Tiles benötigt werden.
- Ein optionaler Start-Command (`StartupCommandCall`) kann beim Start aufgerufen und über einen Ausdruck aktiviert werden.
- `VERSION` (`OptVersion`) und `OFFICIAL NAME` (`OptOfficialAppName`) beschreiben Modulmetadaten.

Die Funktion `isAuthenticated` (`AppAuthenticationFunction`) ist der vorgesehene Ort, um den Benutzerkontext des AppUI-Moduls zu initialisieren. Die Funktion erledigt das nicht automatisch: In ihrem Funktionskörper muss ausdrücklich modelliert werden, dass der von der Laufzeit gelieferte Benutzername in die `userEnvironment` übernommen und die zugehörige Benutzer-ID gesetzt wird. Diese ID wird üblicherweise über einen Service oder ein Repository zum Benutzernamen ermittelt und nicht als Konstante hinterlegt. Je nach Laufzeit stammt der Benutzername beispielsweise aus einer OAuth-Anmeldung oder aus einer Login-Maske. Authentifizierung und fachliche Berechtigungsprüfung bleiben trotzdem getrennte Aufgaben.

#### Konzeptlandkarte der Anwendung

| Name | Konzeptname | FQ-Name | Aufgabe |
| --- | --- | --- | --- |
| `AppUI Module` | `AppUiModule` | `org.modellwerkstatt.dataux.structure.AppUiModule` | Anwendung mit Benutzerkontext, Navigation und Tiles |
| `Tile` | `AppTile` | `org.modellwerkstatt.dataux.structure.AppTile` | Hervorgehobener Command-Einstieg mit optionalem Label- und Farbausdruck |
| `tileInit` | `TileInitFunction` | `org.modellwerkstatt.dataux.structure.TileInitFunction` | Initialisiert den Tile-Zustand |
| kein eigener Alias | `StartupCommandCall` | `org.modellwerkstatt.dataux.structure.StartupCommandCall` | Bedingter Command-Aufruf beim Anwendungsstart |
| `Action` | `MenuAction` | `org.modellwerkstatt.dataux.structure.MenuAction` | Verknüpft Menü oder Tile mit einem ObjectFlow-Command |

Das Modul stellt die Navigation bereit; der Command besitzt den fachlichen Ablauf und seine Pages, und die zugeordneten `Page Pane`s beschreiben deren Oberfläche:

```text
AppUI Module
  -> Menü / Tile
    -> ObjectFlow Command
      -> Page
        -> DataUX Page Pane
```

Der Benutzerkontext wird zentral am Modul initialisiert. Fachliche Berechtigungen müssen dennoch in den dafür vorgesehenen fachlichen Komponenten geprüft werden. Das Ausblenden eines Menüeintrags ist keine ausreichende Zugriffskontrolle.

#### Tiles und dynamische Darstellung

Tiles bilden die Startoberfläche der Anwendung. Sie werden nach dem Applikationsstart sowie immer dann angezeigt, wenn kein Command mehr geöffnet beziehungsweise in Ausführung ist. Damit bieten sie zugleich Einstiegspunkte und eine kompakte Übersicht über den aktuellen Arbeitsstand.

`tileInit` (`TileInitFunction`) bereitet den gemeinsamen Zustand dieser Startoberfläche vor. Die Funktion kann beispielsweise offene Aufgaben laden, Kennzahlen berechnen oder Daten für mehrere Tiles organisieren. Die einzelnen Tiles verwenden diese vorbereiteten Werte anschließend für dynamische Beschriftungen und Farben. So können sie den Anwendungsnutzern nicht nur eine Aktion anbieten, sondern unmittelbar relevante Informationen anzeigen.

Ein `Tile` (`AppTile`) kann Beschriftung und Farbe über BaseLanguage-Ausdrücke dynamisch bestimmen. Typische Anwendungsfälle für eingebettete Ausdrücke sind:

- dynamische Labels und Tile-Texte,
- Farben und Hervorhebungen,
- Argumente für Command-Aufrufe,
- Darstellungsoptionen, die vom aktuellen Zustand abhängen.

Welche Variablen sichtbar sind und welcher Ergebnistyp erwartet wird, hängt von der Einbettungsstelle ab. Ein Ausdruck in einer Tile-Funktion ist deshalb nicht automatisch im Modul-Lebenszyklus oder in einer anderen UI-Funktion gültig.

Diese Ausdrücke sollen Darstellungs- und Interaktionslogik enthalten. Fachliche Berechnungen und Regeln bleiben in den zuständigen Entities, Value Objects, Services oder Commands und werden von dort aufgerufen. `tileInit` darf solche fachlichen Fähigkeiten aufrufen und ihre Ergebnisse für die Darstellung aufbereiten.


### Batchjob mit `BatchJob Module` (`BatchJobModule`)

Ein `BatchJob Module` (`BatchJobModule`) beschreibt eine ausführbare Hintergrundverarbeitung. Sein Kern sind ObjectFlow-Producer/Consumer-Paare (`org.modellwerkstatt.objectflow.structure.OFXProducerConsumerPair`). Mehrere Paare können in einem Modul zusammengefasst und jeweils separat geplant und parallelisiert werden.

Jedes Pair folgt einer Inbox-Denkweise:

1. Der Producer sucht oder berechnet Arbeitseinheiten und legt deren Entities beziehungsweise Schlüssel in eine typisierte Inbox.
2. Die konfigurierte Anzahl von Consumern entnimmt jeweils ein Inbox-Element und verarbeitet es, häufig über einen oder mehrere `GRAPH_OWNER`-Commands.
3. Eine Vorbedingung sollte erneut prüfen, ob die Arbeitseinheit noch verarbeitet werden muss. Das schützt unter anderem vor zwischenzeitlichen UI-Änderungen und macht Wiederholungen robuster.
4. Nach erfolgreicher Verarbeitung wird die Arbeitseinheit abgeschlossen; fachliche Abbrüche und technische Fehlschläge werden getrennt behandelt.

Die Inbox ist eine flüchtige In-Memory-Queue und keine persistente Jobwarteschlange. Vor jedem Producer-Lauf wird ihr bisheriger Inhalt gelöscht und aus dem Producer-Ergebnis neu aufgebaut. Bei einem Prozess- oder Jobneustart geht die Inbox ebenfalls verloren. Ein zuverlässiger Wiederanlauf setzt deshalb voraus, dass der Producer offene Arbeit erneut ermitteln kann. Die Consumer-Verarbeitung muss idempotent sein oder durch eine Vorbedingung erkennen, ob eine Arbeitseinheit bereits verarbeitet wurde.

Ein Inbox-Element wird vor seiner Verarbeitung aus der Queue genommen. Nach einem technischen Fehler wird es nur dann erneut eingestellt, wenn die Exception-Strategie ausdrücklich `READD_TO_INBOX` verlangt. Ohne diese Reaktion findet kein automatischer Retry desselben Inbox-Eintrags statt. Ein unerwartet beendeter Consumer gibt sein noch bekanntes Verarbeitungselement zwar an die Inbox zurück, wird aber ohne eine entsprechende Restart-Strategie nicht automatisch ersetzt.

Der Producer läuft nur, wenn kein Consumer des Pairs mehr arbeitet. Dadurch entsteht pro Durchlauf ein abgegrenzter Arbeitsvorrat. Bei mehreren Consumern werden die Elemente parallel verarbeitet; die Reihenfolge ihres Abschlusses ist dann nicht definiert.

Ein Pair darf auch nur aus einem Producer bestehen, wenn der gestartete Command die Arbeit vollständig erledigt und keine einzelnen Inbox-Elemente nachbearbeitet werden müssen. Ein solches Producer-only-Pair darf seine Inbox nicht füllen: Enthält sie Elemente, obwohl kein Consumer vorhanden ist, verwirft die Laufzeit sie wieder. `null`-Elemente aus einem Producer-Ergebnis werden ebenfalls nicht übernommen.

Auch ein Batchjob benötigt einen konsistenten technischen Benutzerkontext. In seiner Authentifizierungsfunktion muss deshalb ausdrücklich modelliert werden, dass Benutzername und Benutzer-ID in der `userEnvironment` gesetzt werden; die Benutzer-ID wird wie bei einer App über einen Service oder ein Repository ermittelt. Der Benutzerkontext dient der Ausführung und Nachvollziehbarkeit, ist aber keine alleinige Sicherheitsgrenze.

#### Exception-Strategien und Wiederanlauf

Ein Batchjob besitzt eine verpflichtende Exception-Strategie (`org.modellwerkstatt.objectflow.structure.OFXExceptionStrategy`). Ihre Regeln werden der Reihe nach geprüft; die letzte Regel muss eine Default-Strategie sein. Eine Regel kann mehrere Laufzeitreaktionen kombinieren:

| Reaktion | Wirkung |
| --- | --- |
| `READD_TO_INBOX` | Stellt das fehlgeschlagene Element erneut in die Inbox ein |
| `DELAY_EXECUTION` | Wartet vor der weiteren Verarbeitung beziehungsweise Neuplanung |
| `CLEAR_INBOX` | Verwirft alle noch wartenden Inbox-Elemente und veranlasst eine Neuplanung |
| `CONSUMER_RESTART` | Beendet den betroffenen Consumer und startet einen Ersatz-Consumer |
| `JOB_SHUTDOWN` / `VM_SHUTDOWN` | Gegenwärtig nicht implementiert |
| `JOB_RESTART` / `VM_RESTART` | Gegenwärtig nicht implementiert |
| `SILENT_NO_LOG` | Unterdrückt die übliche Problemprotokollierung; der Vorgang bleibt als nicht protokollierte Exception gezählt |

Bei mehreren gleichzeitig fehlschlagenden Consumern wartet die Laufzeit, bis kein Consumer mehr arbeitet, und verwendet dann die längste angeforderte Verzögerung. Nach einem Producerfehler wird eine positive Wiederanlaufzeit auf mindestens fünf Minuten angehoben. Ein fachlicher Abbruch wird separat als *canceled* gezählt: Er ist kein technischer Fehler und stellt das betroffene Element nicht automatisch erneut in die Inbox.

Die Exception-Strategie ersetzt keine fachliche Problembehandlung innerhalb des verarbeiteten Commands. Die Laufzeit setzt außerdem kein fachliches Verarbeitungstimeout für ein einzelnes Inbox-Element. Blockierende Zugriffe auf externe Datenbanken, Dateitransfers oder entfernte Dienste müssen daher eigene Verbindungs- und Lese-Timeouts besitzen; andernfalls können sie einen Consumer dauerhaft binden und auch das Herunterfahren verzögern.

#### Konzeptlandkarte der Batch-Optionen

| Name | Konzeptname | FQ-Name | Bedeutung |
| --- | --- | --- | --- |
| `CRON` | `OptCronPairExp` | `org.modellwerkstatt.dataux.structure.OptCronPairExp` | Zeitplan für ein referenziertes Producer/Consumer-Paar |
| `DELAY` | `OptDelayPair` | `org.modellwerkstatt.dataux.structure.OptDelayPair` | Wartezeit zwischen vollständigen Durchläufen eines referenzierten Pairs |
| `CONSUMERS` | `OptNumConsumersPair` | `org.modellwerkstatt.dataux.structure.OptNumConsumersPair` | Anzahl paralleler Consumer eines referenzierten Paars |
| `DEPENDENT_CONSECUTIVE` | `OptBatchDependent` | `org.modellwerkstatt.dataux.structure.OptBatchDependent` | Paare werden abhängig und nacheinander behandelt |
| `RUN_IN_CONSOLE` | `OptRunInConsole` | `org.modellwerkstatt.dataux.structure.OptRunInConsole` | Start ohne instanziierte UI |
| kein eigener Alias | `OptIncludeBatchUi` | `org.modellwerkstatt.dataux.structure.OptIncludeBatchUi` | Bindet einen referenzierten Batchjob in einen UI-Modulkontext ein |
| `VERSION` | `OptVersion` | `org.modellwerkstatt.dataux.structure.OptVersion` | Version des Moduls |
| `OFFICIAL NAME` | `OptOfficialAppName` | `org.modellwerkstatt.dataux.structure.OptOfficialAppName` | Sichtbarer offizieller Modulname |

`CRON` (`OptCronPairExp`) beschreibt die Felder Sekunde, Minute, Stunde, Tag des Monats, Monat und Wochentag. `CRON`, `DELAY` und `CONSUMERS` referenzieren jeweils ein konkretes Pair. Bei mehreren Paaren muss daher jede Option bewusst dem richtigen Pair zugeordnet werden.

Aus diesen Optionen ergeben sich drei typische Betriebsweisen:

- **Zeitpunktausführung:** Ein `CRON`-Ausdruck startet den Producer zu einem bestimmten Zeitpunkt; die Consumer arbeiten die dadurch gefüllte Inbox ab.
- **Zeitfenster:** `DELAY` schaltet das Pair in den kontinuierlichen Modus und legt den Abstand zwischen vollständigen Durchläufen fest. Zusätzliche `CRON`-Ausdrücke begrenzen diesen Modus auf Zeitfenster. Außerhalb des Fensters erhalten Consumer keine neue Arbeit; laufende Verarbeitungen dürfen enden und die restliche Inbox bleibt bis zum nächsten Fenster erhalten, solange der Prozess nicht neu gestartet wird.
- **Abhängige Folge:** Mit `DEPENDENT_CONSECUTIVE` werden mehrere Paare in ihrer modellierten Reihenfolge ausgeführt. Ein nachfolgendes Pair beginnt erst, wenn seine Vorgänger erfolgreich abgeschlossen sind. Nur das erste Pair darf `CRON` oder `DELAY` besitzen. Nach einem Fehler oder dem Verlassen des Zeitfensters beginnt die Kette beim erneuten Start wieder mit dem ersten Pair.

Im zeitpunktspezifischen Modus muss der CRON-Ausdruck mit einem konkreten Sekundenwert beginnen. Im Zeitfenstermodus beginnen die Ausdrücke dagegen mit einem Sekunden-Wildcard. Wird `DELAY` ohne `CRON` verwendet, läuft das Pair grundsätzlich ohne tägliche Zeitfensterbegrenzung. Die Auswertung verwendet die Standardzeitzone der JVM.

`CONSUMERS` legt die Anzahl der Consumer pro Pair fest und steuert damit die Parallelität pro Pair. Eine Erhöhung beschleunigt die Abarbeitung nur, wenn die verwendeten externen Systeme sowie Sperrstrategien dies vertragen. `RUN_IN_CONSOLE` unterdrückt die UI-Instanziierung; `OptIncludeBatchUi` bindet umgekehrt einen Batchjob in den UI-Kontext eines Moduls ein.

Ein typischer Batchablauf lautet:

1. Ein CRON-Ausdruck, ein manueller Start oder ein anderer Trigger aktiviert ein Producer/Consumer-Paar.
2. Der Producer ermittelt Arbeitseinheiten beziehungsweise Schlüssel und füllt die Inbox.
3. Die konfigurierte Zahl von Consumern entnimmt Arbeitseinheiten aus der Inbox.
4. Der Consumer prüft die Vorbedingung und verarbeitet die Arbeit über die vorgesehenen Commands.
5. Bei Erfolg wird das Element abgeschlossen; bei einer technischen Ausnahme bestimmt die Exception-Strategie die Laufzeitreaktion.
6. Bei `DEPENDENT_CONSECUTIVE` wird nach erfolgreichem Abschluss mit dem nächsten Pair fortgefahren.

#### Manuelle Ausführung und Konsolenbetrieb

Die Laufzeit bietet pro Pair eine Operation zum manuellen Start des Producers. Sie stellt lediglich eine asynchrone Startnachricht ein; ihre unmittelbare Rückmeldung bedeutet noch nicht, dass der Producer oder das Pair abgeschlossen wurde. Ein manueller Lauf:

- darf das CRON-Zeitfenster umgehen,
- leert die Inbox und baut sie neu auf,
- wird nicht nachgeholt, wenn zum Ausführungszeitpunkt noch Consumer arbeiten,
- setzt bei einem Verarbeitungsfehler die restliche manuelle Inbox zurück und plant keinen automatischen Retry,
- führt im abhängigen Modus nur das ausdrücklich gestartete Pair aus und setzt die Pair-Kette nicht automatisch fort.

Ein manueller Producer-Lauf sollte deshalb nur bei einem eindeutig ruhenden Pair gestartet werden. Das Stoppen des Jobtimers verhindert neue zeitgesteuerte Starts, beendet aber keine bereits laufende Producer- oder Consumer-Verarbeitung. Das Deaktivieren eines Producers betrifft automatische Starts; ein manueller Start bleibt möglich. Das Zurücksetzen des Timerzustands macht ältere geplante Nachrichten ungültig und erzeugt die Zeitplanung neu.

Beim Start über die Konsolen-Laufzeit werden alle Paare als eine abhängige Kette genau einmal ausgeführt. Unabhängig von der modellierten Consumerzahl verwendet jedes Pair dabei nur einen Consumer. Dieser Modus eignet sich daher für kontrollierte Einmalläufe, ist aber kein realistischer Lasttest für die konfigurierte Parallelität des Serverbetriebs.

#### Monitoring und Betriebsdiagnose

Die Job-Laufzeit stellt für jedes Pair unter anderem folgende Werte bereit:

- aktuelle Inbox-Größe, Zeitpunkt und Dauer des letzten Fillups,
- Producerstatus, letzte Aktion und nächste geplante Läufe,
- erfolgreiche, fachlich abgebrochene und technisch fehlgeschlagene Verarbeitungen,
- durchschnittliche und maximale Laufzeiten von Producer und Consumern,
- protokollierte sowie durch `SILENT_NO_LOG` nicht protokollierte Exceptions,
- Jobname, Version, technischer Benutzer, Verbindungsziel und Laufzeitzeitzone.

Das HTML-Dashboard dient der lesenden Betriebsübersicht. Die aktiven Operationen — Producer manuell starten, Producer aktivieren oder deaktivieren, Jobtimer stoppen oder starten, Timerzustand neu aufbauen und detailliertes Tracing aktivieren — werden über die JMX-Schnittstelle angeboten. Ein Timerstopp oder deaktivierter Producer ist deshalb im Monitoring von einem fachlich leeren Lauf und von einem technischen Fehler zu unterscheiden.


### Wahl zwischen Application und Batchjob

Ein `AppUI Module` (`AppUiModule`) ist passend, wenn Benutzer über Menüs, Tiles und Pages mit Commands interagieren. Ein `BatchJob Module` (`BatchJobModule`) ist passend, wenn Arbeit automatisch, zeitgesteuert oder in Producer/Consumer-Strukturen verarbeitet wird.

Beide Modulformen können dieselben fachlichen Services und Repositories verwenden. UI und Batch sollten die fachliche Logik nicht duplizieren, sondern unterschiedliche Einstiegspunkte in dieselben fachlichen Fähigkeiten bilden.


## Durchgängige Abläufe

### Interaktive Suche und Bearbeitung

1. Eine Menüaktion des `AppUI Module`s startet einen Such-Command.
2. Dessen erste Page stellt ein Filterobjekt bereit; ein `Page Pane` zeigt es in einem `Delegate Form`.
3. Nach der Suche stellt eine weitere Page eine Ergebnisliste bereit; eine `Table` zeigt die Ergebnisse.
4. Die ausgewählte Tabellenzeile wird zur gemeinsamen Selektion des Ergebnis- beziehungsweise Entity-Typs.
5. Eine Tabellenaktion startet den Bearbeitungs-Command mit der selektierten ID oder Instanz.
6. Die Bearbeitungs-Page nutzt ein `Page Pane` mit Formular, Detailtabelle und gegebenenfalls weiteren Detailformularen.

### Batchverarbeitung mit optionaler UI

1. Ein `BatchJob Module` konfiguriert Pair, Zeitplan und Exception-Strategie.
2. Der Producer stellt die zu verarbeitenden Objekte oder Schlüssel bereit.
3. Ein Command verarbeitet jeweils eine Arbeitseinheit und kann definierte Pages besitzen.
4. Bei `RUN_IN_CONSOLE` wird keine UI instanziiert.
5. Wird der Batchjob in eine Anwendung eingebunden, können vorhandene Pages durch passende `Page Pane`s sichtbar gemacht werden.


## Häufige Fehler und Diagnose

- **UI-Bindung mit Laden verwechseln:** Eine gebundene Referenz oder Liste muss fachlich bereits geladen beziehungsweise bereitgestellt sein.
- **Unabhängige Tabellenselektionen erwarten:** Tabellen desselben Zeilentyps teilen sich die Selektion innerhalb eines `Page Pane`s.
- **Identität und fachliche Gleichheit verwechseln:** Die gemeinsame Selektion bezieht sich auf dieselbe Laufzeitinstanz.
- **Leere Selektion nicht berücksichtigen:** Formulare zeigen dann keine Daten; Aktionen und Ausdrücke müssen diesen Zustand vertragen oder deaktiviert sein.
- **Zeilen- und Parent-Typ verwechseln:** Bei einer Tabelle ist zwischen dem Eigentümer der Listen-Property und dem Zeilentyp zu unterscheiden.
- **Value-Object-Liste an eine Tabelle binden:** Tabellen erwarten Listen von Entities oder DTOs.
- **`Include` als neuen Kontext verstehen:** `Include` verwendet eine bestehende UI-Beschreibung, erzeugt aber weder Daten noch einen eigenen Selektionsraum.
- **Unpassenden Delegate-Typ verwenden:** Delegate und fachlicher Property-Typ müssen zusammenpassen.
- **Fachlogik in UI-Ausdrücke verschieben:** Dynamische Labels und Farben sind UI-Aufgaben; Geschäftsregeln gehören in fachliche Komponenten.
- **Command-Argumente aus dem falschen Selektionskontext bilden:** Tabellenaktionen benötigen häufig die selektierte Zeile und nicht das Parent-Objekt des `Page Pane`s.
- **Batchoption keinem Pair eindeutig zuordnen:** `CRON`, `DELAY` und `CONSUMERS` referenzieren jeweils ein konkretes Producer/Consumer-Paar.
- **`DELAY` als Pause zwischen Inbox-Elementen verstehen:** Die Verzögerung liegt zwischen vollständigen Pair-Durchläufen; innerhalb einer gefüllten Inbox arbeiten freie Consumer ohne diese Pause weiter.
- **Die Inbox als persistent ansehen:** Ihr Inhalt existiert nur im Arbeitsspeicher. Nach einem Neustart muss der Producer noch offene Arbeit erneut finden können.
- **Automatischen Retry voraussetzen:** Ein fehlgeschlagenes Element wird nur mit `READD_TO_INBOX` erneut eingestellt. `CLEAR_INBOX` verwirft auch die übrigen wartenden Elemente.
- **Manuellen Start während laufender Consumer auslösen:** Die Anforderung wird in diesem Zustand nicht für später vorgemerkt. Vor dem Start muss der Pair-Status geprüft werden.
- **Parallele Consumer bei reihenfolgeabhängiger Verarbeitung verwenden:** Mehrere Consumer schließen Elemente nicht zwingend in Inbox-Reihenfolge ab.
- **Externe Aufrufe ohne eigene Timeouts ausführen:** Die Job-Laufzeit begrenzt die Bearbeitungszeit eines einzelnen Inbox-Elements nicht zuverlässig.
- **Serverzeitzone übersehen:** CRON-Ausdrücke werden in der Standardzeitzone der JVM ausgewertet.
- **Exception-Strategie als fachliche Fehlerbehandlung behandeln:** Sie steuert den technischen Umgang mit Ausnahmen, nicht die Domänenentscheidung.
- **Desktop-Layout unverändert mobil verwenden:** Unterschiedliche Geräteklassen benötigen häufig eigene `Page Pane`s oder Anwendungsmodule.
- **Name und Konzeptname verwechseln:** Name, Konzeptname und FQ-Name nach der eingangs festgelegten Schreibweise unterscheiden.

## Konzeptindex für Agenten

Der Index enthält die in dieser Dokumentation behandelten wichtigen DataUX-Konzepte sowie die unmittelbar benötigten ObjectFlow-Konzepte, nicht alle Konzepte der Sprachen.

| Themenbereich | Name | Konzeptname | FQ-Name |
| --- | --- | --- | --- |
| UI-Root | `Page Pane` | `PagePane` | `org.modellwerkstatt.dataux.structure.PagePane` |
| UI-Element | `Delegate Form` | `DelegateForm` | `org.modellwerkstatt.dataux.structure.DelegateForm` |
| UI-Element | `Table` | `Table` | `org.modellwerkstatt.dataux.structure.Table` |
| UI-Element | `Grid Layout` | `GridLayout` | `org.modellwerkstatt.dataux.structure.GridLayout` |
| UI-Element | `Tab Layout` | `TabLayout` | `org.modellwerkstatt.dataux.structure.TabLayout` |
| UI-Element | `Tab` | `Tab` | `org.modellwerkstatt.dataux.structure.Tab` |
| UI-Element | `Include` | `Include` | `org.modellwerkstatt.dataux.structure.Include` |
| UI-Element | `Custom UI Element` | `CustomElement` | `org.modellwerkstatt.dataux.structure.CustomElement` |
| Layoutgewicht | `-1` | `MinWeight` | `org.modellwerkstatt.dataux.structure.MinWeight` |
| Layoutgewicht | `1*` | `OneWeight` | `org.modellwerkstatt.dataux.structure.OneWeight` |
| Layoutgewicht | `2*` | `TwoWeight` | `org.modellwerkstatt.dataux.structure.TwoWeight` |
| Layoutgewicht | `3*` | `ThreeWeight` | `org.modellwerkstatt.dataux.structure.ThreeWeight` |
| Layoutgewicht | `4*` | `FourWeight` | `org.modellwerkstatt.dataux.structure.FourWeight` |
| Layoutgewicht | `5*` | `FiveWeight` | `org.modellwerkstatt.dataux.structure.FiveWeight` |
| Delegate | `String` | `StringDelegate` | `org.modellwerkstatt.dataux.structure.StringDelegate` |
| Delegate | `Integer` | `IntegerDelegate` | `org.modellwerkstatt.dataux.structure.IntegerDelegate` |
| Delegate | `BigDecimal` | `BigDecimalDelegate` | `org.modellwerkstatt.dataux.structure.BigDecimalDelegate` |
| Delegate | `DateTime` | `DateTimeDelegate` | `org.modellwerkstatt.dataux.structure.DateTimeDelegate` |
| Delegate | `DateTime (Date Only)` | `DateTimeDateOnlyDelegate` | `org.modellwerkstatt.dataux.structure.DateTimeDateOnlyDelegate` |
| Delegate | `LocalDate` | `LocalDateDelegate` | `org.modellwerkstatt.dataux.structure.LocalDateDelegate` |
| Delegate | `Status` | `StatusDelegate` | `org.modellwerkstatt.dataux.structure.StatusDelegate` |
| Delegate | `Reference` | `ReferenceDelegate` | `org.modellwerkstatt.dataux.structure.ReferenceDelegate` |
| Delegate | `Image` | `ImageDelegate` | `org.modellwerkstatt.dataux.structure.ImageDelegate` |
| Delegate | `Upload` | `UploadDelegate` | `org.modellwerkstatt.dataux.structure.UploadDelegate` |
| Delegate | `Dummy` | `DummyDelegate` | `org.modellwerkstatt.dataux.structure.DummyDelegate` |
| Delegate-Option | `WIDTH` | `WidthDOption` | `org.modellwerkstatt.dataux.structure.WidthDOption` |
| Delegate-Option | `DISABLED` | `DisabledDOption` | `org.modellwerkstatt.dataux.structure.DisabledDOption` |
| Delegate-Option | `EDITABLE` | `EditableDOption` | `org.modellwerkstatt.dataux.structure.EditableDOption` |
| Delegate-Option | `OPTIONAL` | `OptionalDOption` | `org.modellwerkstatt.dataux.structure.OptionalDOption` |
| Delegate-Option | `PICKER` | `PickerDOption` | `org.modellwerkstatt.dataux.structure.PickerDOption` |
| Delegate-Option | `IMPORTANT` | `ImportantDOption` | `org.modellwerkstatt.dataux.structure.ImportantDOption` |
| Delegate-Option | `COLOR` | `DynColorDOption` | `org.modellwerkstatt.dataux.structure.DynColorDOption` |
| Delegate-Option | `LONG DESC` | `StatusLongDescDOption` | `org.modellwerkstatt.dataux.structure.StatusLongDescDOption` |
| Delegate-Option | `ISSUE UPDATE/SCANABLE` | `IssueUpdateDOption` | `org.modellwerkstatt.dataux.structure.IssueUpdateDOption` |
| Delegate-Option | `OVERWRITE LABEL` | `OverwriteLabelDOption` | `org.modellwerkstatt.dataux.structure.OverwriteLabelDOption` |
| Delegate-Option | `OVERWRITE FORMAT` | `OverwriteFormatDOption` | `org.modellwerkstatt.dataux.structure.OverwriteFormatDOption` |
| Delegate-Option | `HOOK` | `DelegateHookDOption` | `org.modellwerkstatt.dataux.structure.DelegateHookDOption` |
| Delegate-Option | `FOLD` | `FoldDOption` | `org.modellwerkstatt.dataux.structure.FoldDOption` |
| Delegate-Option | `FORCE NUMERIC EDITOR` | `ForceNumericEditor` | `org.modellwerkstatt.dataux.structure.ForceNumericEditor` |
| Delegate-Option | `ALTER` | `AlternativeDOption` | `org.modellwerkstatt.dataux.structure.AlternativeDOption` |
| Delegate-Option | `WIDE` | `WideDOption` | `org.modellwerkstatt.dataux.structure.WideDOption` |
| Formular-/Tabellenoption | `DISABLED` | `DisabledFOption` | `org.modellwerkstatt.dataux.structure.DisabledFOption` |
| Formular-/Tabellenoption | `LABEL` | `LabelFOption` | `org.modellwerkstatt.dataux.structure.LabelFOption` |
| Formular-/Tabellenoption | `SELECT FIRST` | `SelectFirstFOption` | `org.modellwerkstatt.dataux.structure.SelectFirstFOption` |
| Formular-/Tabellenoption | `SELECTION SUMMARY LINE` | `SelectionSummaryLineFOption` | `org.modellwerkstatt.dataux.structure.SelectionSummaryLineFOption` |
| Formular-/Tabellenoption | `TABLE SUMMARY LINE` | `TableSummaryLineFOption` | `org.modellwerkstatt.dataux.structure.TableSummaryLineFOption` |
| Formular-/Tabellenoption | `CUSTOM CSV EXPORT` | `TableCustomCsvExportFOption` | `org.modellwerkstatt.dataux.structure.TableCustomCsvExportFOption` |
| Gridlayout-Option | `FLEXIBLE` | `FlexibleOption` | `org.modellwerkstatt.dataux.structure.FlexibleOption` |
| Gridlayout-Option | `FOCUS FORWARD 2` | `SkipFocusOption` | `org.modellwerkstatt.dataux.structure.SkipFocusOption` |
| Menü | `Action` | `MenuAction` | `org.modellwerkstatt.dataux.structure.MenuAction` |
| Menü | `Compound Action` | `MenuCompoundAction` | `org.modellwerkstatt.dataux.structure.MenuCompoundAction` |
| Menü | kein eigener Alias | `PageConclusionReference` | `org.modellwerkstatt.dataux.structure.PageConclusionReference` |
| Menü | `USER_CANCEL` | `PageConclusionOptionUserCancel` | `org.modellwerkstatt.dataux.structure.PageConclusionOptionUserCancel` |
| Menü | `Submenu` | `MenuSub` | `org.modellwerkstatt.dataux.structure.MenuSub` |
| Menü | `- - - -` | `MenuSeparator` | `org.modellwerkstatt.dataux.structure.MenuSeparator` |
| Menüargument | `getSelected()` | `SelectedObject` | `org.modellwerkstatt.objectflow.structure.SelectedObject` |
| Menüargument | `getSelectedObjects()` | `SelectedList` | `org.modellwerkstatt.objectflow.structure.SelectedList` |
| Application | `AppUI Module` | `AppUiModule` | `org.modellwerkstatt.dataux.structure.AppUiModule` |
| Application | `Tile` | `AppTile` | `org.modellwerkstatt.dataux.structure.AppTile` |
| Application | `tileInit` | `TileInitFunction` | `org.modellwerkstatt.dataux.structure.TileInitFunction` |
| Application | kein eigener Alias | `StartupCommandCall` | `org.modellwerkstatt.dataux.structure.StartupCommandCall` |
| Modul | `isAuthenticated` | `AppAuthenticationFunction` | `org.modellwerkstatt.dataux.structure.AppAuthenticationFunction` |
| Moduloption | `VERSION` | `OptVersion` | `org.modellwerkstatt.dataux.structure.OptVersion` |
| Moduloption | `OFFICIAL NAME` | `OptOfficialAppName` | `org.modellwerkstatt.dataux.structure.OptOfficialAppName` |
| Batchjob | `BatchJob Module` | `BatchJobModule` | `org.modellwerkstatt.dataux.structure.BatchJobModule` |
| Batchjob | Producer/Consumer-Paar | `OFXProducerConsumerPair` | `org.modellwerkstatt.objectflow.structure.OFXProducerConsumerPair` |
| Batchjob | Exception-Strategie | `OFXExceptionStrategy` | `org.modellwerkstatt.objectflow.structure.OFXExceptionStrategy` |
| Batchoption | `CRON` | `OptCronPairExp` | `org.modellwerkstatt.dataux.structure.OptCronPairExp` |
| Batchoption | `DELAY` | `OptDelayPair` | `org.modellwerkstatt.dataux.structure.OptDelayPair` |
| Batchoption | `CONSUMERS` | `OptNumConsumersPair` | `org.modellwerkstatt.dataux.structure.OptNumConsumersPair` |
| Batchoption | `DEPENDENT_CONSECUTIVE` | `OptBatchDependent` | `org.modellwerkstatt.dataux.structure.OptBatchDependent` |
| Batchoption | `RUN_IN_CONSOLE` | `OptRunInConsole` | `org.modellwerkstatt.dataux.structure.OptRunInConsole` |
| Batchoption | kein eigener Alias | `OptIncludeBatchUi` | `org.modellwerkstatt.dataux.structure.OptIncludeBatchUi` |
