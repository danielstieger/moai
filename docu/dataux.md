# DataUX (org.modellwerkstatt.dataux) – Benutzeroberflächen und ausführbare Module

## Modellierungsumfang und Ausdrucksmöglichkeiten

`org.modellwerkstatt.dataux` ist eine der drei domänenspezifischen Sprachen der **modellwerkstatt MoWare-Werkbank**. Sie beschreibt Benutzeroberflächen und den ausführbaren Rahmen von Anwendungen und Batchjobs.

DataUX verbindet zwei Aufgabenbereiche:

1. **UI-Modellierung:** Eine Oberfläche wird aus einem fachlich gebundenen `Page Pane` (`PagePane`) sowie Formularen, Tabellen, Layouts und Aktionen aufgebaut.
2. **Anwendung und Batchjob:** Ausführbare Module konfigurieren Authentifizierung, Navigation beziehungsweise Batch-Verarbeitung und die zugehörige Laufzeitkonfiguration.

Die Sprache beschreibt vor allem, **welche fachlichen Daten wie visualisiert werden**. Generator und Laufzeit übernehmen die technische Umsetzung. An dafür vorgesehenen Stellen können BaseLanguage-Ausdrücke eingebettet werden, etwa für Beschriftungen, Farben, Bedingungen oder Command-Argumente.

`org.modellwerkstatt.dataux.structure.ApiDescription` ist veraltet und nicht mehr zu verwenden.

Name, Konzeptname und FQ-Name folgen der [Bezeichnung der Konzepte](moware-werkbank.md#bezeichnung-der-konzepte) in der Werkbank-Dokumentation.

## Teil I – UI-Modellierung

### Page Panes

Eine ObjectFlow-`Page` (`org.modellwerkstatt.objectflow.structure.PageCrtl`) gehört zu einem ObjectFlow-`Command` (`org.modellwerkstatt.objectflow.structure.Command`) und beschreibt eine Seite seines Interaktionsablaufs. Ein `Page Pane` ist das Gegenstück auf der UI-Seite: Es beschreibt den sichtbaren Inhalt dieser Page.

Ein `Page Pane` besitzt genau ein oberstes UI-Element. Dieses kann unmittelbar ein `Delegate Form` (`DelegateForm`) oder eine `Table` (`Table`) sein. Sollen mehrere Elemente kombiniert werden, bildet ein `Grid Layout` (`GridLayout`) oder `Tab Layout` (`TabLayout`) das oberste Element. Zusätzlich kann das `Page Pane` Menüeinträge enthalten.

Die Page stellt die Daten bereit; das `Page Pane` stellt sie dar. Eine UI-Bindung lädt keine Daten nach. Benötigte Referenzen und Listen müssen bereits durch den Command beziehungsweise seine Repositories geladen und an die Page übergeben worden sein.

#### Kapitellandkarte: UI-Komposition

| Name | Konzeptname | FQ-Name | Aufgabe |
| --- | --- | --- | --- |
| `Page Pane` | `PagePane` | `org.modellwerkstatt.dataux.structure.PagePane` | UI-Beschreibung für eine ObjectFlow-Page mit genau einem obersten UI-Element |
| `Delegate Form` | `DelegateForm` | `org.modellwerkstatt.dataux.structure.DelegateForm` | Formular aus typgerechten Property-Delegates |
| `Table` | `Table` | `org.modellwerkstatt.dataux.structure.Table` | Tabelle für eine gebundene Liste aus Entities oder DTOs |
| `Grid Layout` | `GridLayout` | `org.modellwerkstatt.dataux.structure.GridLayout` | Raster aus Zeilen und Spalten mit einem oder mehreren UI-Elementen |
| `Tab Layout` | `TabLayout` | `org.modellwerkstatt.dataux.structure.TabLayout` | Container für mehrere Tabs |
| `Tab` | `Tab` | `org.modellwerkstatt.dataux.structure.Tab` | Beschrifteter Tab mit genau einem UI-Element |
| `Include` | `Include` | `org.modellwerkstatt.dataux.structure.Include` | Einbindung eines bereits deklarierten bindbaren UI-Elements |
| `Custom UI Element` | `CustomElement` | `org.modellwerkstatt.dataux.structure.CustomElement` | Projektspezifisches UI-Element mit eigener Implementierungsklasse |
| `-1` | `MinWeight` | `org.modellwerkstatt.dataux.structure.MinWeight` | Minimalgewicht für Zeile oder Spalte im `Grid Layout`; nicht im `Delegate Form`. |
| `1*` | `OneWeight` | `org.modellwerkstatt.dataux.structure.OneWeight` | Gewicht 1 für Zeile/Spalte im `Grid Layout` und Spaltengewicht im `Delegate Form`. |
| `2*` | `TwoWeight` | `org.modellwerkstatt.dataux.structure.TwoWeight` | Gewicht 2 für Zeile/Spalte im `Grid Layout` und Spaltengewicht im `Delegate Form`. |
| `3*` | `ThreeWeight` | `org.modellwerkstatt.dataux.structure.ThreeWeight` | Gewicht 3 für Zeile/Spalte im `Grid Layout` und Spaltengewicht im `Delegate Form`. |
| `4*` | `FourWeight` | `org.modellwerkstatt.dataux.structure.FourWeight` | Gewicht 4 für Zeile/Spalte im `Grid Layout` und Spaltengewicht im `Delegate Form`. |
| `5*` | `FiveWeight` | `org.modellwerkstatt.dataux.structure.FiveWeight` | Gewicht 5 für Zeile/Spalte im `Grid Layout` und Spaltengewicht im `Delegate Form`. |
| `FLEXIBLE` | `FlexibleOption` | `org.modellwerkstatt.dataux.structure.FlexibleOption` | Erlaubt eine flexible Größenanpassung des `Grid Layout`s. |
| `FOCUS FORWARD 2` | `SkipFocusOption` | `org.modellwerkstatt.dataux.structure.SkipFocusOption` | Verschiebt den initialen Fokus im `Grid Layout` auf ein späteres Element. |
| `DISABLED` | `DisabledFOption` | `org.modellwerkstatt.dataux.structure.DisabledFOption` | Formular ist nicht editierbar. |
| `LABEL` | `LabelFOption` | `org.modellwerkstatt.dataux.structure.LabelFOption` | Beschriftung von Formular oder Tabelle; nicht am obersten Element eines `Page Pane`s. |
| `SELECT FIRST` | `SelectFirstFOption` | `org.modellwerkstatt.dataux.structure.SelectFirstFOption` | Selektiert das erste Tabellenelement bei der Initialisierung. |
| `SELECTION SUMMARY LINE` | `SelectionSummaryLineFOption` | `org.modellwerkstatt.dataux.structure.SelectionSummaryLineFOption` | Berechnet eine Zusammenfassung für ausgewählte Tabellenobjekte. |
| `TABLE SUMMARY LINE` | `TableSummaryLineFOption` | `org.modellwerkstatt.dataux.structure.TableSummaryLineFOption` | Berechnet eine Zusammenfassung über alle Tabellenobjekte. |
| `CUSTOM CSV EXPORT` | `TableCustomCsvExportFOption` | `org.modellwerkstatt.dataux.structure.TableCustomCsvExportFOption` | Passt den CSV-Export der Tabelle an. |

`Delegate Form`, `Table`, `Grid Layout`, `Tab Layout` und `Custom UI Element` können sowohl innerhalb eines `Page Pane`s als auch als eigenständige, wiederverwendbare Root Nodes deklariert werden.

#### Datenbindung und Selektion

DataUX bindet UI-Komponenten an fachliche Typen und deren Properties. Ein bindbares Element spezifiziert einen Entity- oder DTO-Typ (`boundClassifier`) und optional eine Property dieses Typs (`boundProperty`). Formulare, Tabellen, Custom Elements und Includes sind immer gebunden; nur Layouts innerhalb einer Hierarchie tragen keine Bindung und reichen den Kontext durch.

Jedes `Page Pane` besitzt einen gemeinsamen **Selektionskontext**. Für jeden darin verwendeten Entity- oder DTO-Typ kann eine aktuell selektierte Instanz existieren. Diese Selektion gehört nicht einer einzelnen Tabelle oder einem einzelnen Formular, sondern steht allen Komponenten des `Page Pane`s zur Verfügung.

Im Modell kann ein Element als `boundClassifier` jedoch nur Typen wählen, die vor ihm in der UI-Hierarchie bereitgestellt werden: die Inhaltstypen vorheriger Geschwister einschließlich ihrer Kindelemente sowie die Inhaltstypen umgebender Layouts, Formulare und Tabellen und deren vorheriger Geschwister. Nachfolgende Elemente zählen nicht. Ein einzelner Tab begrenzt diese Suche: Ein Element in einem Tab sieht nur, was im selben Tab vor ihm steht oder dem `Tab Layout` vorausgeht, nicht aber Elemente anderer Tabs. Soll ein Detail in einem Tab die Selektion eines Masters verwenden, steht der Master deshalb vor dem `Tab Layout` oder im selben Tab vor dem Detail.

##### Typbindung

Eine Bindung nur an einen Entity- oder DTO-Typ verwendet grundsätzlich die aktuelle Selektion dieses Typs. Ein an `Rechnung` gebundenes `Delegate Form` zeigt beispielsweise die aktuell selektierte `Rechnung`. Für eine `Table` ist diese reine Typbindung nur zulässig, wenn sie das oberste Element des `Page Pane`s ist oder in einem Layout der ersten Ebene liegt und an den Root-Typ des `Page Pane`s gebunden ist; jede andere Tabelle in der Hierarchie wird an eine Listen-Property eines selektierten Objekts gebunden.

Wird einem `Page Pane` auf Root-Ebene genau eine Instanz seines Root-Typs bereitgestellt – unmittelbar oder als Liste mit genau einem Element –, ist diese Instanz automatisch selektiert. Ein direkt an den Root-Typ gebundenes Formular kann sie deshalb ohne eine Tabelle mit `SELECT FIRST` unmittelbar anzeigen. Diese automatische Selektion gilt für das Root-Objekt; eine untergeordnete Liste wird nicht allein deshalb selektiert, weil sie nur ein Element enthält.

##### Property-Bindung

Eine Property-Bindung wird auf der aktuellen Selektion ihres Eigentümertyps ausgewertet. Bei einer selektierten `Rechnung` bezeichnet die Bindung `Rechnung.kunde` das `kunde`-Objekt genau dieser Rechnung. Ein `Delegate Form` kann so an eine Property gebunden werden, deren Typ eine Entity, ein DTO oder ein Value Object ist.

Das Formular liest diesen Bindungskontext, erzeugt oder verändert aber keine Selektion. Ein an `Rechnung.kunde` gebundenes Formular hängt daher nicht an einer eventuell vorhandenen `Kunde`-Selektion, sondern zeigt ausschließlich den `kunde` der aktuell selektierten `Rechnung`.

##### Tabellenbindung und Selektion

Eine `Table` benötigt eine Liste von Entities oder DTOs. Listen von Value Objects sind kein Tabellen-Bindungsmodell in DataUX.

Ist der Zeilentyp mit dem Root-Typ des `Page Pane`s identisch, kann die Tabelle direkt an diesen Typ gebunden werden und verwendet den Root-Datenbestand; das gilt nur für eine Tabelle als oberstes Element des `Page Pane`s oder innerhalb eines Layouts der ersten Ebene, etwa die Rechnungstabelle oben in einem `Grid Layout` mit darunterliegendem Rechnungsformular. Soll die Tabelle Objekte eines anderen Typs anzeigen, wird sie an eine Listen-Property eines selektierten Objekts gebunden. Eine Tabelle für `Rechnung.positionen` zeigt somit die Positionen der aktuell selektierten Rechnung; ihr Zeilentyp ist `Rechnungsposition`, nicht `Rechnung`.

Die Auswahl einer Tabellenzeile bestimmt die gemeinsame Selektion des Zeilentyps. Mit `SELECT FIRST` (`SelectFirstFOption`) kann eine Tabelle beim initialen Anzeigen das erste Element selektieren und so eine abhängige Detaildarstellung initialisieren.

Mehrere Tabellen mit demselben Zeilentyp teilen dieselbe Selektion. Enthält eine andere Tabelle dieselbe Laufzeitinstanz, markiert sie diese ebenfalls. Enthält sie die Instanz nicht, zeigt sie keine ausgewählte Zeile; die gemeinsame Selektion bleibt erhalten. Maßgeblich ist dieselbe Laufzeitinstanz, nicht nur eine gleiche fachliche ID oder fachliche Gleichheit. Für in die Session integrierte Entities ist diese Instanz je Identität eindeutig, für DTOs und andere No-Key-Ergebnisse nicht; siehe [Read-only, Checkout und Session-Identität](manmap.md#read-only-checkout-und-session-identität).

##### Leere Selektion

Für einen Entity- oder DTO-Typ kann keine Instanz selektiert sein. Ein ausschließlich an diesen Typ gebundenes Formular zeigt dann keine Daten. Tabellen können ihre Zeilen weiterhin darstellen, obwohl keine Zeile ausgewählt ist. Aktionen und Ausdrücke müssen diesen Zustand vertragen oder deaktiviert sein.

##### Master-Detail

Der gemeinsame Selektionskontext ermöglicht Master-Detail-Oberflächen ohne explizite Synchronisationslogik zwischen den Komponenten. Eine Rechnungsseite kann beispielsweise aus einer Tabelle der `Rechnung`-Objekte, einer Tabelle für `Rechnung.positionen` und einem Formular für die ausgewählte `Rechnungsposition` bestehen.

Die Bindungskette lautet sinngemäß:

`selektierte Rechnung -> positionen -> ausgewählte Rechnungsposition -> Detailformular`

Das Detailformular muss nicht wissen, aus welcher Tabelle die Selektion stammt. Auch beim Wechsel des Masters ist keine zusätzliche Synchronisationslogik erforderlich; die Laufzeit wertet abhängige Bindungen und Selektionen im gemeinsamen Kontext aus.

### Formulare, Tabellen und Delegates

Ein `Delegate Form` beschreibt ein Formular. Seine Bindung bestimmt das dargestellte Objekt, seine Delegates bestimmen die sichtbaren Felder und seine Spaltengewichte deren horizontale Aufteilung. Eine `Table` beschreibt eine Objektliste; ihre Delegates bilden die Spalten.

Der Delegate-Typ folgt dem fachlichen Property-Typ. Ein Delegate ersetzt keine fachliche Validierung. Fachliche Regeln gehören in das Domänenmodell beziehungsweise in Services und Commands; Delegate- und Formularoptionen steuern Darstellung und Interaktion.

#### Kapitellandkarte: Delegates

| Name | Konzeptname | FQ-Name | Aufgabe |
| --- | --- | --- | --- |
| `String` | `StringDelegate` | `org.modellwerkstatt.dataux.structure.StringDelegate` | Text-Property |
| `Integer` | `IntegerDelegate` | `org.modellwerkstatt.dataux.structure.IntegerDelegate` | Ganzzahlige Property |
| `BigDecimal` | `BigDecimalDelegate` | `org.modellwerkstatt.dataux.structure.BigDecimalDelegate` | Dezimalzahl |
| `DateTime` | `DateTimeDelegate` | `org.modellwerkstatt.dataux.structure.DateTimeDelegate` | Datum und Uhrzeit |
| `DateTime (Date Only)` | `DateTimeDateOnlyDelegate` | `org.modellwerkstatt.dataux.structure.DateTimeDateOnlyDelegate` | Nur Datumskomponente eines DateTime-Werts |
| `LocalDate` | `LocalDateDelegate` | `org.modellwerkstatt.dataux.structure.LocalDateDelegate` | Lokales Datum |
| `Status` | `StatusDelegate` | `org.modellwerkstatt.dataux.structure.StatusDelegate` | ObjectFlow-Statuswert |
| `Reference` | `ReferenceDelegate` | `org.modellwerkstatt.dataux.structure.ReferenceDelegate` | Referenz auf ein fachliches Objekt; nur im Formular |
| `Image` | `ImageDelegate` | `org.modellwerkstatt.dataux.structure.ImageDelegate` | Bilddarstellung, nur im Formular |
| `Upload` | `UploadDelegate` | `org.modellwerkstatt.dataux.structure.UploadDelegate` | Datei-Upload, nur im Formular |
| `Dummy` | `DummyDelegate` | `org.modellwerkstatt.dataux.structure.DummyDelegate` | Platzhalter zur Anordnung von Formularfeldern |
| `DISABLED` | `DisabledDOption` | `org.modellwerkstatt.dataux.structure.DisabledDOption` | Delegate im Formular nicht editierbar. |
| `OPTIONAL` | `OptionalDOption` | `org.modellwerkstatt.dataux.structure.OptionalDOption` | Hebt die Pflichteingabe auf. |
| `PICKER` | `PickerDOption` | `org.modellwerkstatt.dataux.structure.PickerDOption` | Datumsauswahl für Datums-Delegates; bei `DateTime` nicht mit `OVERWRITE FORMAT`. |
| `ISSUE UPDATE/SCANABLE` | `IssueUpdateDOption` | `org.modellwerkstatt.dataux.structure.IssueUpdateDOption` | Löst bei Scan oder Inhaltsänderung eine verfügbare Update-Conclusion (`SCAN_UPDATE`) aus. |
| `FORCE NUMERIC EDITOR` | `ForceNumericEditor` | `org.modellwerkstatt.dataux.structure.ForceNumericEditor` | Numerischer Editor für einen `String`-Delegate. |
| `ALTER` | `AlternativeDOption` | `org.modellwerkstatt.dataux.structure.AlternativeDOption` | Alternativer Editor für `Reference` und `Status`, sofern die Laufzeit ihn unterstützt. |
| `WIDE` | `WideDOption` | `org.modellwerkstatt.dataux.structure.WideDOption` | Blendet das Label aus und gibt dem Editor die gesamte Breite. |
| `NUM OF LINES` | `NumOfLinesDOption` | `org.modellwerkstatt.dataux.structure.NumOfLinesDOption` | Mehrzeiliger Text mit angegebener Zeilenzahl. |
| `TIME PICKER ONLY` | `TimeOnlyDOption` | `org.modellwerkstatt.dataux.structure.TimeOnlyDOption` | Erfasst nur die Uhrzeit; als Datum gilt immer das aktuelle. |
| `OVERWRITE LABEL` | `OverwriteLabelDOption` | `org.modellwerkstatt.dataux.structure.OverwriteLabelDOption` | Überschreibt die von der Datenstruktur vorgegebene Beschriftung. |
| `OVERWRITE FORMAT` | `OverwriteFormatDOption` | `org.modellwerkstatt.dataux.structure.OverwriteFormatDOption` | Überschreibt das von der Datenstruktur vorgegebene Format. |
| `WIDTH` | `WidthDOption` | `org.modellwerkstatt.dataux.structure.WidthDOption` | Spaltenbreite in Prozent; Pflicht je Tabellenspalte, Summe höchstens 100 %. |
| `EDITABLE` | `EditableDOption` | `org.modellwerkstatt.dataux.structure.EditableDOption` | Tabellenspalte (`Status`, `BigDecimal`) editierbar; höchstens eine je Tabelle, nicht mit `FOLD`. |
| `IMPORTANT` | `ImportantDOption` | `org.modellwerkstatt.dataux.structure.ImportantDOption` | Hebt ein wichtiges Tabellenfeld hervor; höchstens einmal je Tabelle. |
| `COLOR` | `DynColorDOption` | `org.modellwerkstatt.dataux.structure.DynColorDOption` | Berechnet die Farbe einer `BigDecimal`-Tabellenspalte dynamisch aus dem Wert. |
| `LONG DESC` | `StatusLongDescDOption` | `org.modellwerkstatt.dataux.structure.StatusLongDescDOption` | Verwendet in der Tabelle die Langbeschreibung eines Status. |
| `RIGHT ALIGN` | `RightAlignDOption` | `org.modellwerkstatt.dataux.structure.RightAlignDOption` | Richtet den Zelleninhalt einer `String`-Spalte rechtsbündig aus. |
| `FOLD` | `FoldDOption` | `org.modellwerkstatt.dataux.structure.FoldDOption` | Tabelle: Spalte zunächst ausgeblendet (Doppelklick auf Spaltenkopf); Formular unter h2forms: verstecktes, per Scan befüllbares Feld. |

Ein `Reference`-Delegate bietet die zulässigen Objekte zur Auswahl an. `scopeText` (projiziert als `reference description`) legt mit einem oder mehreren Pfaden fest, welche Properties des referenzierten Typs den angezeigten Text bilden: Für einen an `Rechnung.kunde` gebundenen Delegate verweist `name` auf `Kunde.name`. Die Auswahlmenge setzt die Scope-Funktion der Page mit `#Meta.setScope(…)`; siehe [ObjectFlow: Scopes](objectflow.md#scopes). Fehlt sie, führt eine Auswahl zu einer Exception. Ist der Delegate oder das Formular mit `DISABLED` gekennzeichnet, wird der Wert nur angezeigt und kein Scope benötigt.

#### Delegate-Optionen

| Name | Konzeptname | Kontext | Delegate-Typen | Wirkung |
| --- | --- | --- | --- | --- |
| `DISABLED` | `DisabledDOption` | Formular | alle | Delegate ist nicht editierbar |
| `OPTIONAL` | `OptionalDOption` | Formular | alle | Hebt die Pflichteingabe auf; siehe [Pflichtwerte, leere Eingaben und `null`](#pflichtwerte-leere-eingaben-und-null) |
| `PICKER` | `PickerDOption` | Formular | `LocalDate`, `DateTime (Date Only)`, `DateTime` | Verwendet nach Möglichkeit eine Datumsauswahl; bei `DateTime` nicht zusammen mit `OVERWRITE FORMAT` |
| `ISSUE UPDATE/SCANABLE` | `IssueUpdateDOption` | Formular | alle | Löst eine verfügbare Update-Conclusion aus |
| `FORCE NUMERIC EDITOR` | `ForceNumericEditor` | Formular | `String` | Verwendet für einen `StringDelegate` einen numerischen Editor |
| `ALTER` | `AlternativeDOption` | Formular und Tabelle | `Reference`, `Status` | Verwendet einen alternativen Editor, sofern die Laufzeitumgebung diesen unterstützt |
| `WIDE` | `WideDOption` | Formular | alle | Blendet nach Möglichkeit das Label links vom Editor aus und gibt dem Editor die gesamte Breite |
| `NUM OF LINES` | `NumOfLinesDOption` | Formular | `String` | Stellt den Text mehrzeilig mit der angegebenen Zeilenzahl dar |
| `TIME PICKER ONLY` | `TimeOnlyDOption` | Formular | `DateTime` | Erfasst nur die Uhrzeit; als Datum wird immer das aktuelle verwendet |
| `OVERWRITE LABEL` | `OverwriteLabelDOption` | Formular und Tabelle | alle | Überschreibt die von der Datenstruktur vorgegebene Beschriftung |
| `OVERWRITE FORMAT` | `OverwriteFormatDOption` | Formular, Tabelle und Custom Element | `String`, `Integer`, `BigDecimal`, `DateTime`, `DateTime (Date Only)`, `LocalDate`, `Image` | Überschreibt das von der Datenstruktur vorgegebene Format |
| `WIDTH` | `WidthDOption` | Tabelle | alle | Legt die Breite der Spalte in Prozent fest; Pflicht für jede Spalte, die Summe darf 100 % nicht überschreiten |
| `EDITABLE` | `EditableDOption` | Tabelle | `Status`, `BigDecimal` | Property wird editierbar dargestellt; höchstens eine Spalte pro Tabelle, nicht zusammen mit `FOLD` |
| `IMPORTANT` | `ImportantDOption` | Tabelle | alle | Hebt ein wichtiges Tabellenfeld hervor; höchstens einmal pro Tabelle |
| `COLOR` | `DynColorDOption` | Tabelle | `BigDecimal` | Berechnet die Farbe dynamisch aus dem Wert |
| `LONG DESC` | `StatusLongDescDOption` | Tabelle | `Status` | Verwendet die Langbeschreibung eines Status |
| `RIGHT ALIGN` | `RightAlignDOption` | Tabelle | `String` | Richtet den Zelleninhalt rechtsbündig aus |
| `FOLD` | `FoldDOption` | Formular und Tabelle | alle | Tabelle: Blendet die Spalte zunächst aus; der Benutzer kann sie per Doppelklick auf den Spaltenkopf einblenden (in h2forms ohne Wirkung). Formular unter h2forms: Das Feld wird nicht angezeigt, bleibt aber als verstecktes Feld erhalten und kann etwa mit `ISSUE UPDATE/SCANABLE` per Scan befüllt werden |

Jede Option darf pro Delegate höchstens einmal verwendet werden. `Reference`-Delegates sind in Tabellen nicht zulässig.

#### Pflichtwerte, leere Eingaben und `null`

`OPTIONAL` hebt die Pflichteingabe auf. Ein optionaler Text an `OPTIONAL` legt fest, wie der fehlende Wert dargestellt wird, etwa „weiß ich nicht“; ohne Angabe erscheint `--`. Was eine leere Eingabe liefert, zeigt die Tabelle:

| Delegate | Leere Eingabe ohne `OPTIONAL` | Leere Eingabe mit `OPTIONAL` | Grenzen aus der Property |
| --- | --- | --- | --- |
| `String` | Fehler bei `LENGTH` mit `min ≥ 1`, sonst `""` | `null` | `LENGTH`: minimale und maximale Länge |
| `Integer` | Eingabefehler | `0` | `RANGE`: Bereich |
| `BigDecimal` | Eingabefehler | `null` | `RANGE`: Bereich und Skala |
| `Reference`, `Status`, Datums-Delegates | Eingabe erforderlich | `null` | – |

Bei Strings steuert `LENGTH[min-max]` an der Business Property die Pflichteingabe: `min ≥ 1` erzwingt eine Eingabe, `min = 0` erlaubt ein leeres Feld. `OPTIONAL` ist dort nur nötig, wenn ein leeres Feld `null` statt `""` liefern und gegen `null` geprüft werden soll. Die Oberfläche trimmt Eingaben nicht, auch nicht für die Längenprüfung; ein fachlich gefordertes Trimmen gehört ins Modell.

Die Grenzen aus `LENGTH` und `RANGE` werden nicht zusätzlich als `validation` modelliert, außer die Regel ist fachlich zwingend oder die Eingabe kommt ohne Oberfläche, etwa aus einem Batch oder über eine Schnittstelle.

#### Optionen für Formulare und Tabellen

| Name | Konzeptname | Element | Wirkung |
| --- | --- | --- | --- |
| `DISABLED` | `DisabledFOption` | Formular | Formular ist nicht editierbar |
| `LABEL` | `LabelFOption` | Formular und Tabelle | Setzt die Beschriftung des Elements. Nicht zulässig am obersten Element eines `Page Pane`s; dort kommt die Beschriftung aus dem Seitentitel |
| `SELECT FIRST` | `SelectFirstFOption` | Tabelle | Selektiert das erste Tabellenelement bei der Initialisierung |
| `SELECTION SUMMARY LINE` | `SelectionSummaryLineFOption` | Tabelle | Berechnet eine Zusammenfassung für ausgewählte Tabellenobjekte |
| `TABLE SUMMARY LINE` | `TableSummaryLineFOption` | Tabelle | Berechnet eine Zusammenfassung über alle Tabellenobjekte |
| `CUSTOM CSV EXPORT` | `TableCustomCsvExportFOption` | Tabelle | Passt den CSV-Export an |

### Layouts, Tabs und Wiederverwendung

Ein `Grid Layout` ordnet UI-Elemente in Zeilen und Spalten an. Zeilen- und Spaltengewichte bestimmen die Größenverteilung. Die sichtbaren Gewichte `-1`, `1*`, `2*`, `3*`, `4*` und `5*` werden durch `MinWeight`, `OneWeight`, `TwoWeight`, `ThreeWeight`, `FourWeight` und `FiveWeight` repräsentiert. So steht beispielsweise ein kompaktes Rechnungsformular (Zeilengewicht `-1`) über der Tabelle der `Rechnung.positionen` (Zeilengewicht `1*`); beide nutzen in einer Spalte `1*` die volle Breite. Dieselben Gewichte werden auch im `Delegate Form` als Spaltengewichte verwendet, dort jedoch ohne `MinWeight`.

Für ein `Grid Layout` stehen insbesondere folgende Optionen zur Verfügung:

| Name | Konzeptname | Wirkung |
| --- | --- | --- |
| `FLEXIBLE` | `FlexibleOption` | Erlaubt eine flexible Größenanpassung |
| `FOCUS FORWARD 2` | `SkipFocusOption` | Verschiebt den initialen Fokus auf ein späteres Element |

Ein `Tab Layout` enthält mindestens einen `Tab` (`Tab`). Jeder Tab besitzt eine als Ausdruck modellierte Beschriftung und genau ein UI-Element.

Mit `Include` (`Include`) wird ein bereits deklariertes bindbares UI-Element wiederverwendet. Die Bindung ist dabei nach Elementart festgelegt: Ein als Root Node deklariertes Element wird nur typisiert, d. h. es gibt lediglich seinen Entity- oder DTO-Typ an und keine Property. Das `Include` ist immer gebunden: Es gibt den Typ und gegebenenfalls die Property an, auf der das eingebundene Element am Verwendungsort arbeitet, etwa `Rechnung.positionen` für eine wiederverwendbare Positionstabelle; sein Inhaltstyp muss dem Typ des eingebundenen Elements entsprechen. Ein `Grid Layout` oder `Tab Layout` innerhalb einer UI-Hierarchie wird nicht gebunden; nur als Root Node ist es typisiert. Die Einbindung erzeugt weder zusätzliche Daten noch einen unabhängigen Selektionsraum. Ein UI-Element wird nur benannt, wenn es mit `Include` wiederverwendet wird; für benannte Elemente erzeugt der Generator eine eigene Klasse.

Ein `Custom UI Element` (`CustomElement`) bindet eine projektspezifische UI-Implementierung ein. Es ist für Darstellungsfälle gedacht, die Form, Tabelle und Layouts nicht ausdrücken. Die fachliche Datenbindung, Delegates und Menüaktionen bleiben Teil des DataUX-Modells; nur die konkrete Darstellung wird projektspezifisch implementiert.

Die Zielgeräte sind bei der Layoutwahl ausdrücklich mitzudenken. Eine breite Desktop-Aufteilung ist nicht automatisch für mobile Datenerfassungsgeräte oder Smartphones geeignet. Für unterschiedliche Geräteklassen können eigene `Page Pane`s erforderlich sein.

### Menüs und Command-Aktionen

Ein `Page Pane` und eine `Table` besitzen Menüs, deren fachlicher Bezug unterschiedlich ist:

- Das Menü einer Tabelle richtet sich vor allem an die gebundenen Tabellenobjekte. Seine Aktionen arbeiten typischerweise mit der aktuell ausgewählten Zeile oder mit mehreren ausgewählten Zeilen.
- Das Menü eines `Page Pane`s gehört zum gesamten Seitenkontext. Seine Aktionen betreffen daher eher das gebundene Wurzelobjekt, den vollständigen Aggregatgraphen oder den übergreifenden Ablauf der Page.

Auch für ein `Custom UI Element` kann ein Menü modelliert werden. Ob und wie es sichtbar und bedienbar ist, hängt jedoch davon ab, ob die konkrete UI-Laufzeitkomponente diese Menüintegration unterstützt. Ein `Include` kann eigene Menüeinträge nur angeben, wenn es eine `Table` einbindet; damit wird das Tabellenmenü am jeweiligen Verwendungsort überschrieben. Beim Einbinden eines Custom Elements, Formulars oder Layouts sind Menüeinträge am Include nicht zulässig.

#### Kapitellandkarte: Menüs

| Name | Konzeptname | FQ-Name | Aufgabe |
| --- | --- | --- | --- |
| `Action` | `MenuAction` | `org.modellwerkstatt.dataux.structure.MenuAction` | Ruft einen ObjectFlow-Command mit optionalem Label und Argumenten auf |
| `Compound Action` | `MenuCompoundAction` | `org.modellwerkstatt.dataux.structure.MenuCompoundAction` | Verkettet mehrere Command-Aufrufe anhand ihrer Page-Conclusions |
| `PageConclusionReference` | `PageConclusionReference` | `org.modellwerkstatt.dataux.structure.PageConclusionReference` | Referenziert eine Conclusion des aufgerufenen Commands, die als automatische Conclusion ausgeführt wird |
| `USER_CANCEL` | `PageConclusionOptionUserCancel` | `org.modellwerkstatt.dataux.structure.PageConclusionOptionUserCancel` | Automatische Conclusion, die den Command wie einen Benutzerabbruch mit `cancel` beendet |
| `Submenu` | `MenuSub` | `org.modellwerkstatt.dataux.structure.MenuSub` | Gruppiert weitere Menüeinträge |
| `- - - -` | `MenuSeparator` | `org.modellwerkstatt.dataux.structure.MenuSeparator` | Trennt Menügruppen optisch |
| `getSelected` | `SelectedObject` | `org.modellwerkstatt.objectflow.structure.SelectedObject` | Action-Argument: das aktuell selektierte Objekt eines im `Page Pane` verwendeten Typs. |
| `getSelectedObjects` | `SelectedList` | `org.modellwerkstatt.objectflow.structure.SelectedList` | Action-Argument: die ausgewählten Objekte einer Mehrfachselektion. |

Ein `Submenu` (`MenuSub`) ohne Text ist das Overflow-Menü eines `Page Pane`s oder einer Tabelle. Die Sprache prüft dafür drei Regeln: Auf der obersten Menüebene stehen `Action`s vor einem `Submenu`, nach einem `Submenu` folgen nur weitere `Submenu`s oder Trennstriche („Actions should be placed left before overflows/sub menus (on lowest menu level at least).“); das textlose `Submenu` ist nur auf der obersten Ebene erlaubt („Action overflow (submenu) is only valid as top level menu in ux elements.“) und nur einmal („Only one overflow (submenu) can be used.“).

Eine `Action` (`MenuAction`) referenziert einen ObjectFlow-`Command`. Die im Command definierte Standardparametrisierung gilt auch für eine Action, sodass sie ohne explizite Argumente modelliert werden kann. Nur wenn der Aufrufkontext andere Werte verlangt, überschreibt die Action einzelne beziehungsweise alle Argumente mit Ausdrücken. Typische Quellen dafür sind:

- `getSelected()` (`org.modellwerkstatt.objectflow.structure.SelectedObject`) für das aktuell ausgewählte Objekt,
- `getSelectedObjects()` (`org.modellwerkstatt.objectflow.structure.SelectedList`) für die ausgewählten Objekte einer Mehrfachselektion,
- Konstanten für fest vorgegebene Aufrufvarianten.

Beschriftung, Icon und Hotkey einer Action kommen aus dem Command. Mit einem eigenen Label aus den statischen Ressourcen (`customLabel`) überschreibt die Action diese Vorgaben für diesen Menüeintrag.

Ein Doppelklick auf eine Tabellenzeile oder die Enter-Taste auf einer ausgewählten Zeile führt die erste Action im Menü der Tabelle aus, deren Hotkey `ENTER` ist; Actions in Submenüs zählen der Reihe nach mit. Die Hauptaktion einer Tabelle, etwa Öffnen oder Bearbeiten, erhält deshalb den Hotkey `ENTER`, als `defaultHotkey` am Command oder über das Label der Action.

Menüaktionen arbeiten immer im aktuellen UI-Kontext. Bei Tabellenaktionen ist deshalb typischerweise die Selektion des Zeilentyps maßgeblich; bei Page-Pane-Aktionen steht meist das gebundene Wurzelobjekt oder der gesamte Seitenablauf im Vordergrund. Das schränkt den Zugriff aber nicht auf diese Typen ein: An jeder Aktionsstelle kann mit einem typisierten `getSelected(...)` die gemeinsame Selektion eines beliebigen im `Page Pane` verwendeten Typs abgefragt werden, beispielsweise `getSelected(RechnungsSubPosition)` direkt in einer Page-Pane-Aktion.

Vor dem Modellieren einer Aktion ist deshalb zu klären:

- Welcher Typ ist an der Aufrufstelle selektiert?
- Welche Command-Parameter müssen befüllt werden?
- Soll die Aktion global, in einem Submenü oder nur an der fokussierten Komponente angeboten werden?

Eine `Compound Action` (`MenuCompoundAction`) ruft einen `GRAPH_OWNER_CMD` oder `GRAPH_OWNER_CMD(modal)` auf und verbindet ihn optional mit einem anschließenden `GRAPH_EDIT_CMD`. Sie benötigt immer ein eigenes Label (`customLabel`) und immer eine automatische Conclusion für den Owner; ohne sie ist eine einfache `Action` zu verwenden. Der Owner wird damit ohne sichtbare UI bis zu diesem Abschluss ausgeführt. Folgt ein `GRAPH_EDIT_CMD`, läuft er in derselben Session mit den vom Owner bereitgestellten Daten; der Owner muss dann genau eine Page besitzen, und `getSelected(...)` im Edit-Aufruf darf nur den Typ dieser Page verwenden. Für den `GRAPH_EDIT_CMD` ist eine automatische Conclusion optional und nur möglich, wenn er Pages hat. Successor-Commands des Owners werden nicht unterstützt, mit Ausnahme genau eines unbedingten Successors.

Damit kann beispielsweise aus einem Suchergebnis heraus eine Aktion auf einem vollständigen Aggregat ausgeführt werden: Der `GRAPH_OWNER_CMD` öffnet das ausgewählte Objekt, lädt den Aggregatgraphen vollständig und stellt die Session bereit. Anschließend führt der `GRAPH_EDIT_CMD` die fachliche Änderung aus. Dessen Conclusion bestätigt die Änderung; die Conclusion des Owners speichert und schließt den Aggregatgraphen. Ohne nachgelagerten `GRAPH_EDIT_CMD` eignet sich dasselbe Muster auch dazu, einen `GRAPH_OWNER_CMD` vollständig ohne UI auszuführen.

`PageConclusionReference` verweist dabei auf eine Abschlussart, d. h., der `Command` muss diese Conclusion deklarieren. `USER_CANCEL` (`PageConclusionOptionUserCancel`) modelliert einen Abbruch des Commands mit `cancel`, analog zu einem Benutzerabbruch.

### Typischer UI-Modellierungsablauf

1. Der ObjectFlow-Command und seine Pages legen fest, welche Daten und Aktionen der Ablauf benötigt.
2. Für jede Page wird der Root-Typ der UI bestimmt.
3. Das `Page Pane` erhält diesen Entity- oder DTO-Typ als Bindungskontext.
4. Das oberste UI-Element wird gewählt: Formular, Tabelle oder Layout.
5. Formulare und Tabellen werden an Typen beziehungsweise geeignete Properties gebunden.
6. Tabellen können über die Auswahl ihrer Zeilen Selektionen für weitere UI-Komponenten bestimmen.
7. Typgerechte Delegates beschreiben Felder und Tabellenspalten.
8. Menüs rufen Commands mit Argumenten aus dem aktuellen Bindungs- und Selektionskontext auf.

## Teil II – Anwendung und Batchjob

`AppUI Module` (`AppUiModule`) und `BatchJob Module` (`BatchJobModule`) sind ausführbare Einstiegspunkte. Die fachlichen Anwendungsfälle verbleiben in Commands, Services und Repositories.

Die Referenz `configuration` ist immer anzugeben, wird aber nur beim Start mit FX8, aus MPS oder im Standalone-Betrieb verwendet; im regulär bereitgestellten Laufzeitkontext ist sie nicht die Anwendungskonfiguration. Die in beiden Konzepten noch vorhandenen Bereiche `onStartup` und `onShutdown` sind nicht mehr zu verwenden (Deprecated).

### Anwendung mit `AppUI Module`

Ein `AppUI Module` beschreibt eine interaktive Anwendung. Neben Benutzerkontext und Modulmetadaten besitzt es Navigation und Einstiegspunkte:

#### Kapitellandkarte: Anwendung

| Name | Konzeptname | FQ-Name | Aufgabe |
| --- | --- | --- | --- |
| `AppUI Module` | `AppUiModule` | `org.modellwerkstatt.dataux.structure.AppUiModule` | Anwendung mit Benutzerkontext, Navigation und Tiles |
| `Tile` | `AppTile` | `org.modellwerkstatt.dataux.structure.AppTile` | Hervorgehobener Command-Einstieg mit optionalem Label- und Farbausdruck |
| `tileInit` | `TileInitFunction` | `org.modellwerkstatt.dataux.structure.TileInitFunction` | Initialisiert den Tile-Zustand |
| `startup command to run` | `StartupCommandCall` | `org.modellwerkstatt.dataux.structure.StartupCommandCall` | Command, der nach der Anmeldung gestartet wird |
| `isAuthenticated` | `AppAuthenticationFunction` | `org.modellwerkstatt.dataux.structure.AppAuthenticationFunction` | Initialisiert den Benutzerkontext: übernimmt den Benutzernamen in `userEnvironment` und setzt die Benutzer-ID; am `BatchJob Module` nur für eine gestartete UI wirksam. |

- `mainMenu` bildet das fachliche Start- beziehungsweise Hauptmenü.
- `extrasMenu` nimmt ergänzende, seltener benötigte Funktionen auf.
- `helpMenu` bündelt Hilfe- und Dokumentationsaktionen.
- `Tile` (`AppTile`) sind die Kacheln/Schaltflächen auf der Startoberfläche mit einer `Action` (siehe [Menüs und Command-Aktionen](#menüs-und-command-aktionen)) sowie optional dynamischem Text und dynamischer Farbe.
- `tileInit` (`TileInitFunction`) initialisiert Werte, die für Tiles benötigt werden.
- `startup command to run` (`StartupCommandCall`) startet nach der Anmeldung einen Command; eine optionale Bedingung legt fest, ob er ausgeführt wird. Ist er beendet, erscheinen die Tiles. Beim Einstieg über eine URL läuft zuerst der Start-Command und danach der über die URL angesprochene Command, siehe [Command-Optionen](objectflow.md#command-optionen).
- `VERSION` (`OptVersion`) und `OFFICIAL NAME` (`OptOfficialAppName`) beschreiben Modulmetadaten.

Die Funktion `isAuthenticated` (`AppAuthenticationFunction`) ist der vorgesehene Ort, um den Benutzerkontext des AppUI-Moduls zu initialisieren. Die Funktion erledigt das nicht automatisch: In ihrem Funktionskörper muss ausdrücklich modelliert werden, dass der von der Laufzeit gelieferte Benutzername in die `userEnvironment` übernommen und die zugehörige Benutzer-ID gesetzt wird. Diese ID wird üblicherweise über einen Service oder ein Repository zum Benutzernamen ermittelt und nicht als Konstante hinterlegt. Je nach Laufzeit stammt der Benutzername beispielsweise aus einer OAuth-Anmeldung oder aus einer Login-Maske. Authentifizierung und fachliche Berechtigungsprüfung bleiben trotzdem getrennte Aufgaben.

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

Tiles bilden die Startoberfläche der Anwendung. Sie werden nach dem Anwendungsstart sowie immer dann angezeigt, wenn kein Command mehr geöffnet beziehungsweise in Ausführung ist. Damit bieten sie zugleich Einstiegspunkte und eine kompakte Übersicht über den aktuellen Arbeitsstand.

`tileInit` bereitet den gemeinsamen Zustand dieser Startoberfläche vor. Die Funktion kann beispielsweise offene Aufgaben laden, Kennzahlen berechnen oder Daten für mehrere Tiles organisieren. Die einzelnen Tiles verwenden diese vorbereiteten Werte anschließend für dynamische Beschriftungen und Farben. So können sie den Anwendungsnutzern nicht nur eine Aktion anbieten, sondern unmittelbar relevante Informationen anzeigen.

Ein `Tile` kann Beschriftung und Farbe über BaseLanguage-Ausdrücke dynamisch bestimmen. Typische Anwendungsfälle für eingebettete Ausdrücke sind:

- dynamische Labels und Tile-Texte,
- Farben und Hervorhebungen,
- Argumente für Command-Aufrufe,
- Darstellungsoptionen, die vom aktuellen Zustand abhängen.

Welche Variablen sichtbar sind und welcher Ergebnistyp erwartet wird, hängt von der Einbettungsstelle ab. Ein Ausdruck in einer Tile-Funktion ist deshalb nicht automatisch in einer anderen UI-Funktion gültig.

Diese Ausdrücke sollen Darstellungs- und Interaktionslogik enthalten. Fachliche Berechnungen und Regeln bleiben in den zuständigen Entities, Value Objects, Services oder Commands und werden von dort aufgerufen. `tileInit` darf solche fachlichen Fähigkeiten aufrufen und ihre Ergebnisse für die Darstellung aufbereiten.

### Batchjob mit `BatchJob Module`

Ein `BatchJob Module` beschreibt eine ausführbare Hintergrundverarbeitung. Sein Kern sind ObjectFlow-Producer/Consumer-Paare (`org.modellwerkstatt.objectflow.structure.OFXProducerConsumerPair`). Mehrere Paare können in einem Modul zusammengefasst und jeweils separat geplant und parallelisiert werden.

#### Kapitellandkarte: Batchjob

| Name | Konzeptname | FQ-Name | Aufgabe |
| --- | --- | --- | --- |
| `BatchJob Module` | `BatchJobModule` | `org.modellwerkstatt.dataux.structure.BatchJobModule` | Definiert eine ausführbare Hintergrundverarbeitung. |
| Producer/Consumer-Paar | `OFXProducerConsumerPair` | `org.modellwerkstatt.objectflow.structure.OFXProducerConsumerPair` | Ermittelt und verarbeitet typisierte Arbeitseinheiten. |
| Exception-Strategie | `OFXExceptionStrategy` | `org.modellwerkstatt.objectflow.structure.OFXExceptionStrategy` | Legt die Reaktion auf technische Verarbeitungsfehler fest. |

Jedes Pair folgt einer Inbox-Denkweise:

1. Der Producer sucht oder berechnet Arbeitseinheiten und legt deren Entities beziehungsweise Schlüssel in eine typisierte Inbox.
2. Die konfigurierte Anzahl von Consumern entnimmt jeweils ein Inbox-Element und verarbeitet es, häufig über einen oder mehrere `GRAPH_OWNER_CMD`-Commands.
3. Eine Vorbedingung sollte erneut prüfen, ob die Arbeitseinheit noch verarbeitet werden muss. Das schützt unter anderem vor zwischenzeitlichen UI-Änderungen und macht Wiederholungen robuster.
4. Nach erfolgreicher Verarbeitung wird die Arbeitseinheit abgeschlossen; fachliche Abbrüche und technische Fehlschläge werden getrennt behandelt.

Die Inbox ist eine flüchtige In-Memory-Queue und keine persistente Jobwarteschlange. Vor jedem Producer-Lauf wird ihr bisheriger Inhalt gelöscht und aus dem Producer-Ergebnis neu aufgebaut. Bei einem Prozess- oder Jobneustart geht die Inbox ebenfalls verloren. Ein zuverlässiger Wiederanlauf setzt deshalb voraus, dass der Producer offene Arbeit erneut ermitteln kann. Die Consumer-Verarbeitung muss idempotent sein oder durch eine Vorbedingung erkennen, ob eine Arbeitseinheit bereits verarbeitet wurde.

Ein Inbox-Element wird vor seiner Verarbeitung aus der Queue genommen. Nach einem technischen Fehler wird es nur dann erneut eingestellt, wenn die Exception-Strategie ausdrücklich `READD_TO_INBOX` verlangt. Ohne diese Reaktion findet kein automatischer Retry desselben Inbox-Eintrags statt. Ein unerwartet beendeter Consumer gibt sein noch bekanntes Verarbeitungselement zwar an die Inbox zurück, wird aber ohne eine entsprechende Restart-Strategie nicht automatisch ersetzt.

Der Producer läuft nur, wenn kein Consumer des Pairs mehr arbeitet. Dadurch entsteht pro Durchlauf ein abgegrenzter Arbeitsvorrat. Bei mehreren Consumern werden die Elemente parallel verarbeitet; die Reihenfolge ihres Abschlusses ist dann nicht definiert.

Ein Pair darf auch nur aus einem Producer bestehen, wenn der gestartete Command die Arbeit vollständig erledigt und keine einzelnen Inbox-Elemente nachbearbeitet werden müssen. Ein solches Producer-only-Pair darf seine Inbox nicht füllen: Enthält sie Elemente, obwohl kein Consumer vorhanden ist, verwirft die Laufzeit sie wieder. `null`-Elemente aus einem Producer-Ergebnis werden ebenfalls nicht übernommen.

Auch ein Batchjob benötigt einen konsistenten technischen Benutzerkontext. Die Funktion `isAuthenticated` ist auch am `BatchJob Module` verpflichtend zu modellieren, wird aber nur für eine gegebenenfalls gestartete UI ausgeführt. Im Betrieb ohne UI kommt der Benutzerkontext aus der `OFXConfig`; siehe [User Environment und User Service](objectflow.md#user-environment-und-user-service). Der Benutzerkontext dient der Ausführung und Nachvollziehbarkeit, ist aber keine alleinige Sicherheitsgrenze.

#### Exception-Strategien und Wiederanlauf

Ein Batchjob besitzt eine verpflichtende Exception-Strategie (`org.modellwerkstatt.objectflow.structure.OFXExceptionStrategy`). Ihre Regeln werden der Reihe nach geprüft; die letzte Regel muss eine Default-Strategie sein. Eine Regel kann mehrere Laufzeitreaktionen kombinieren:

| Reaktion | Wirkung |
| --- | --- |
| `READD_TO_INBOX` | Stellt das fehlgeschlagene Element erneut in die Inbox ein |
| `DELAY_EXECUTION` | Wartet vor der weiteren Verarbeitung beziehungsweise Neuplanung |
| `CLEAR_INBOX` | Verwirft alle noch wartenden Inbox-Elemente und veranlasst eine Neuplanung |
| `CONSUMER_RESTART` | Beendet den betroffenen Consumer und startet einen Ersatz-Consumer |
| `SILENT_NO_LOG` | Unterdrückt die übliche Problemprotokollierung; der Vorgang bleibt als nicht protokollierte Exception gezählt |

Bei mehreren gleichzeitig fehlschlagenden Consumern wartet die Laufzeit, bis kein Consumer mehr arbeitet, und verwendet dann die längste angeforderte Verzögerung. Nach einem Producerfehler wird eine positive Wiederanlaufzeit auf mindestens fünf Minuten angehoben. Ein fachlicher Abbruch wird separat als *canceled* gezählt: Er ist kein technischer Fehler und stellt das betroffene Element nicht automatisch erneut in die Inbox.

Die Exception-Strategie ersetzt keine fachliche Problembehandlung innerhalb des verarbeiteten Commands. Die Laufzeit setzt außerdem kein fachliches Verarbeitungstimeout für ein einzelnes Inbox-Element. Blockierende Zugriffe auf externe Datenbanken, Dateitransfers oder entfernte Dienste müssen daher eigene Verbindungs- und Lese-Timeouts besitzen; andernfalls können sie einen Consumer dauerhaft binden und auch das Herunterfahren verzögern.

#### Kapitellandkarte: Batchoptionen

| Name | Konzeptname | FQ-Name | Aufgabe |
| --- | --- | --- | --- |
| `CRON` | `OptCronPairExp` | `org.modellwerkstatt.dataux.structure.OptCronPairExp` | Zeitplan für ein referenziertes Producer/Consumer-Paar |
| `DELAY` | `OptDelayPair` | `org.modellwerkstatt.dataux.structure.OptDelayPair` | Wartezeit zwischen vollständigen Durchläufen eines referenzierten Pairs |
| `CONSUMERS` | `OptNumConsumersPair` | `org.modellwerkstatt.dataux.structure.OptNumConsumersPair` | Anzahl paralleler Consumer eines referenzierten Paars |
| `DEPENDENT_CONSECUTIVE` | `OptBatchDependent` | `org.modellwerkstatt.dataux.structure.OptBatchDependent` | Paare werden abhängig und nacheinander behandelt |
| `RUN_IN_CONSOLE` | `OptRunInConsole` | `org.modellwerkstatt.dataux.structure.OptRunInConsole` | Nicht mehr unterstützt; der Checker meldet einen Fehler. Konsolenbetrieb wird in der `OFXConfig` konfiguriert |
| `OptIncludeBatchUi` | `OptIncludeBatchUi` | `org.modellwerkstatt.dataux.structure.OptIncludeBatchUi` | Bindet einen referenzierten Batchjob in einen UI-Modulkontext ein |
| `VERSION` | `OptVersion` | `org.modellwerkstatt.dataux.structure.OptVersion` | Version des Moduls |
| `OFFICIAL NAME` | `OptOfficialAppName` | `org.modellwerkstatt.dataux.structure.OptOfficialAppName` | Sichtbarer offizieller Modulname |

`CRON` (`OptCronPairExp`) beschreibt die Felder Sekunde, Minute, Stunde, Tag des Monats, Monat und Wochentag. `CRON`, `DELAY` und `CONSUMERS` referenzieren jeweils ein konkretes Pair. Bei mehreren Paaren muss daher jede Option bewusst dem richtigen Pair zugeordnet werden.

Aus diesen Optionen ergeben sich drei typische Betriebsweisen:

- **Zeitpunktausführung:** Ein `CRON`-Ausdruck startet den Producer zu einem bestimmten Zeitpunkt; die Consumer arbeiten die dadurch gefüllte Inbox ab.
- **Zeitfenster:** `DELAY` schaltet das Pair in den kontinuierlichen Modus und legt den Abstand zwischen vollständigen Durchläufen fest; innerhalb einer gefüllten Inbox arbeiten freie Consumer ohne diese Pause weiter. Zusätzliche `CRON`-Ausdrücke begrenzen diesen Modus auf Zeitfenster. Außerhalb des Fensters erhalten Consumer keine neue Arbeit; laufende Verarbeitungen dürfen enden und die restliche Inbox bleibt bis zum nächsten Fenster erhalten, solange der Prozess nicht neu gestartet wird.
- **Abhängige Folge:** Mit `DEPENDENT_CONSECUTIVE` werden mehrere Paare in ihrer modellierten Reihenfolge ausgeführt. Ein nachfolgendes Pair beginnt erst, wenn seine Vorgänger erfolgreich abgeschlossen sind. Nur das erste Pair darf `CRON` oder `DELAY` besitzen. Nach einem Fehler oder dem Verlassen des Zeitfensters beginnt die Kette beim erneuten Start wieder mit dem ersten Pair.

Im zeitpunktspezifischen Modus muss der CRON-Ausdruck mit einem konkreten Sekundenwert beginnen. Im Zeitfenstermodus beginnen die Ausdrücke dagegen mit einem Sekunden-Wildcard. Wird `DELAY` ohne `CRON` verwendet, läuft das Pair grundsätzlich ohne tägliche Zeitfensterbegrenzung. Die Auswertung verwendet die Standardzeitzone der JVM.

`CONSUMERS` legt die Anzahl der Consumer pro Pair fest und steuert damit die Parallelität pro Pair. Eine Erhöhung beschleunigt die Abarbeitung nur, wenn die verwendeten externen Systeme sowie Sperrstrategien dies vertragen. Ob ein Batchjob mit oder ohne UI läuft, legt nicht das Modul, sondern die `OFXConfig` fest: Für den Konsolenbetrieb ohne instanziierte UI wird dort als Anwendungsfabrik eine `new instance` der Klasse `org.modellwerkstatt.objectflow.job.console.ConsoleBatchJobAppFactory` konfiguriert. Die frühere Modul-Option `RUN_IN_CONSOLE` wird nicht mehr unterstützt und vom Checker als Fehler gemeldet. `OptIncludeBatchUi` bindet umgekehrt einen Batchjob in den UI-Kontext eines Moduls ein.

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

### Wahl zwischen Anwendung und Batchjob

Ein `AppUI Module` ist passend, wenn Benutzer über Menüs, Tiles und Pages mit Commands interagieren. Ein `BatchJob Module` ist passend, wenn Arbeit automatisch, zeitgesteuert oder in Producer/Consumer-Strukturen verarbeitet wird.

Beide Modulformen können dieselben fachlichen Services und Repositories verwenden. UI und Batch sollten die fachliche Logik nicht duplizieren, sondern unterschiedliche Einstiegspunkte in dieselben fachlichen Fähigkeiten bilden.

## Durchgängige Abläufe

### Interaktive Suche und Bearbeitung

1. Eine Menüaktion des `AppUI Module`s startet einen Such-Command.
2. Dessen erste Page stellt ein Filterobjekt bereit; ein `Page Pane` zeigt es in einem `Delegate Form`.
3. Nach der Suche stellt eine weitere Page eine Ergebnisliste bereit; eine `Table` zeigt die Ergebnisse.
4. Die ausgewählte Tabellenzeile wird zur gemeinsamen Selektion des Ergebnis- beziehungsweise Entity-Typs.
5. Eine Tabellenaktion startet den Bearbeitungs-Command mit der selektierten ID oder Instanz.
6. Der Bearbeitungs-Command ist ein `GRAPH_OWNER_CMD`; seine Page zeigt die geladene Rechnung in einem `DISABLED` `Delegate Form` über der Tabelle der Positionen. Die Änderungen führen `GRAPH_EDIT_CMD`s mit editierbaren Formularen aus, die über das `Submenu` der Tabelle beziehungsweise des `Page Pane`s gestartet werden.

### Batchverarbeitung mit optionaler UI

1. Ein `BatchJob Module` konfiguriert Pair, Zeitplan und Exception-Strategie.
2. Der Producer stellt die zu verarbeitenden Objekte oder Schlüssel bereit.
3. Ein Command verarbeitet jeweils eine Arbeitseinheit und kann definierte Pages besitzen.
4. Die `OFXConfig` entscheidet über UI- oder Konsolenbetrieb; für die Konsole wird die `ConsoleBatchJobAppFactory` als Anwendungsfabrik konfiguriert.
5. Wird der Batchjob in eine Anwendung eingebunden, können vorhandene Pages durch passende `Page Pane`s sichtbar gemacht werden.

## Weiterführende Dokumentation

- [MoWare-Werkbank im Überblick](moware-werkbank.md)
- [ObjectFlow – Fachliches Modell, Services und Anwendungsabläufe](objectflow.md)
- [ManMap – Persistenz und Lesemodelle](manmap.md)

## Dokumentstand

Diese Dokumentation beschreibt DataUX, Stand Oktober 2026, auf Basis von JetBrains MPS 2026.1.
