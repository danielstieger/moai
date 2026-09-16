§ Ich habe hier aufgaben für dich vermerkt, die ich immer zwischen diese Dollarzeichen schreibe § 

# DataUX (`org.modellwerkstatt.dataux`) – Benutzeroberflächen und ausführbare Module

## Modellierungsumfang und Ausdrucksmöglichkeiten

`org.modellwerkstatt.dataux` ist eine der drei domänenspezifischen Sprachen der **modellwerkstatt moware werkbank**. Sie verbindet zwei Aufgabenbereiche:

1. **UI-Modellierung:** Eine Oberfläche wird aus fachlich gebundenen `PagePane`s, Formularen, Tabellen, Layouts und Aktionen aufgebaut.
2. **Application / Batchjob:** Ausführbare Module konfigurieren den Start und das Ende einer Anwendung, Authentifizierung, Menüs beziehungsweise Batch-Verarbeitung und die zugehörige Laufzeitkonfiguration.

Die Sprache beschreibt vor allem, **welche fachlichen Daten wie verwendet werden**. Generator und Laufzeit übernehmen die technische Umsetzung. An dafür vorgesehenen Stellen können BaseLanguage-Ausdrücke eingebettet werden, etwa für Beschriftungen, Farben, Bedingungen oder Lebenszykluslogik.

| Fragestellung           | UI-Modellierung                                            | Application / Batchjob                                                    |
| ----------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------- |
| Primärer Zweck          | Fachliche Daten anzeigen, bearbeiten und Aktionen anbieten | Ein ausführbares Modul und seinen Lebenszyklus konfigurieren              |
| Typischer Einstieg      | `PagePane`                                                 | `AppUI Module` (`AppUiModule`) oder `BatchJob Module` (`BatchJobModule`)  |
| Zentrale Zusammenarbeit | ObjectFlow-`Command` und dessen `Page`s                    | ObjectFlow-Konfiguration, Commands und Producer/Consumer-Paare            |
| Hauptstruktur           | Formulare, Tabellen, Layouts, Menüs                        | Start/Shutdown, Authentifizierung, Menüs/Tiles oder Batch-Paare           |
| Fachliche Daten         | Gebundene Entity- oder DTO-Instanzen und deren Properties  | Parameter, Variablen, konfigurierte Komponenten und Laufzeitkonfiguration |

## Teil I – UI-Modellierung

### Pages und `PagePane`s

Eine **Page** gehört zu einem ObjectFlow-`Command` und beschreibt eine Seite seines Interaktionsablaufs. Eine `PagePane` bildet das Gegenstück auf der UI-Seite: Sie beschreibt den sichtbaren Inhalt dieser Page.

Eine `PagePane` besitzt genau ein oberstes UI-Element. Dieses kann unmittelbar ein Formular oder eine Tabelle sein oder ein Layout, das weitere UI-Elemente enthält. Zusätzlich kann die `PagePane` Optionen und Menüaktionen enthalten.

| Begriff            | Bedeutung                                                                           |
| ------------------ | ----------------------------------------------------------------------------------- |
| Page               | Seite im Ablauf eines Commands; stellt Daten und Aktionen bereit                    |
| `PagePane`         | Wiederverwendbare UI-Beschreibung für eine Page                                     |
| Root-Typ           | Entity- oder DTO-Typ, der den fachlichen Bindungskontext der `PagePane` bestimmt    |
| gebundene Property | Optionaler Pfad zu einem Objekt oder einer Liste innerhalb des Bindungskontexts     |
| UI-Element         | Formular, Tabelle, Layout oder projektspezifisches Element innerhalb der `PagePane` |

Die Page stellt die Daten bereit; die `PagePane` stellt sie dar. Eine UI-Bindung lädt keine Daten nach. Benötigte Referenzen und Listen müssen deshalb bereits durch den Command beziehungsweise seine Repositories geladen und an die Page übergeben worden sein.

### Datenbindung und Selektion

DataUX bindet UI-Komponenten direkt an fachliche Typen und deren Properties. Zusätzlich besitzt eine `PagePane` einen gemeinsamen **Selektionskontext**.

Für jeden verwendeten Entity- oder DTO-Typ kann innerhalb einer `PagePane` eine aktuell selektierte Laufzeitinstanz existieren. Diese Selektion ist nicht Eigentum eines einzelnen Formulars oder einer einzelnen Tabelle, sondern steht allen Komponenten der `PagePane` zur Verfügung.

Dadurch entsteht ein erweiterter Binding-Mechanismus: Eine Komponente kann eine Selektion bestimmen, während eine andere Komponente dieselbe Selektion verwendet.

#### Typbindung

Eine Bindung nur an einen Entity- oder DTO-Typ verwendet grundsätzlich die aktuelle Selektion dieses Typs.

Ein `DelegateForm`, das beispielsweise an `Rechnung` gebunden ist, zeigt die aktuell selektierte `Rechnung`.

Wird einer `PagePane` auf Root-Ebene genau eine Instanz ihres Root-Typs bereitgestellt – entweder unmittelbar oder als Liste mit genau einem Element –, ist diese Instanz automatisch selektiert. Ein direkt an den Root-Typ gebundenes `DelegateForm` kann sie deshalb ohne vorherige Tabelleninteraktion anzeigen.

Diese automatische Selektion gilt für das Root-Objekt der `PagePane`. Untergeordnete Listen werden nicht allein deshalb selektiert, weil sie nur ein Element enthalten.

#### Property-Bindung

Eine Property-Bindung wird auf der aktuellen Selektion des angegebenen Eigentümertyps ausgewertet.

Ist beispielsweise eine `Rechnung` selektiert, bedeutet eine Bindung an

`Rechnung.kunde`

das `kunde`-Objekt dieser selektierten Rechnung.

Ein `DelegateForm` kann auf diese Weise an eine Property gebunden werden, deren Typ eine Entity, ein DTO oder ein Value Object ist. Das Formular zeigt das über die Property erreichte Objekt an.

Dabei erzeugt oder verändert ein `DelegateForm` selbst keine Selektion.

Ein an `Rechnung.kunde` gebundenes Formular hängt deshalb nicht an einer eventuell vorhandenen `Kunde`-Selektion. Es zeigt ausschließlich den `kunde` der aktuell selektierten `Rechnung`.

#### Tabellenbindung

Eine `Table` benötigt immer eine Liste von Entities oder DTOs.

Ist ihr Zeilentyp identisch mit dem Root-Typ der `PagePane`, kann die Tabelle direkt an diesen Typ gebunden werden. Sie verwendet dann den Root-Datenbestand der `PagePane`.

Beispiel:

* `PagePane` für `Rechnung`
* `Table` für `Rechnung`

Die Tabelle zeigt die von der Page bereitgestellten Rechnungen.

Soll eine Tabelle dagegen Objekte eines anderen Typs anzeigen, muss sie an eine Listen-Property gebunden werden.

Beispiel:

* selektierte `Rechnung`
* Bindung der Tabelle an `Rechnung.positionen`
* `positionen` liefert eine Liste von `Rechnungsposition`

Die Tabelle zeigt damit die Positionen der aktuell selektierten Rechnung.

Listen von Value Objects sind kein Tabellen-Bindungsmodell in DataUX.

#### Selektion durch Tabellen

Die Auswahl einer Tabellenzeile bestimmt die gemeinsame Selektion des Zeilentyps.

Wird beispielsweise in einer Tabelle eine `Rechnungsposition` ausgewählt, ist diese Laufzeitinstanz anschließend die selektierte `Rechnungsposition` der `PagePane`. Ein an `Rechnungsposition` gebundenes `DelegateForm` kann dadurch unmittelbar die Details dieser Position anzeigen.

Mit der Option `SELECT_FIRST` kann eine Tabelle beim initialen Anzeigen der `PagePane` ihr erstes Element selektieren. Dadurch kann auch ohne vorherige Benutzerinteraktion eine abhängige Detaildarstellung initialisiert werden.

### Mehrere Tabellen desselben Typs

Mehrere Tabellen mit demselben Zeilentyp verwenden dieselbe gemeinsame Selektion.

Wird in einer Tabelle eine Instanz ausgewählt, gilt diese Auswahl für den gesamten `PagePane`-Kontext.

Enthält eine andere Tabelle dieselbe Laufzeitinstanz, zeigt sie diese ebenfalls als ausgewählt. Enthält sie die Instanz nicht, zeigt sie keine ausgewählte Zeile; die gemeinsame Selektion bleibt davon unberührt.

Die Selektion bezieht sich dabei auf dieselbe Laufzeitinstanz, nicht lediglich auf eine gleiche fachliche ID oder fachliche Gleichheit.

### Leere Selektion

Für einen Entity- oder DTO-Typ kann auch keine Instanz selektiert sein.

Ein ausschließlich an diesen Typ gebundenes `DelegateForm` zeigt dann keine Daten.

Tabellen können ihre vorhandenen Zeilen weiterhin darstellen, auch wenn für ihren Zeilentyp keine Zeile selektiert ist.

Bei mehreren Root-Objekten besitzt eine `PagePane` daher zunächst nicht zwingend eine Root-Selektion: Eine Root-Tabelle kann alle Objekte anzeigen, während ein an den Root-Typ gebundenes `DelegateForm` erst nach einer Auswahl Daten darstellt.

### Master-Detail

Die gemeinsame Selektion ermöglicht Master-Detail-Oberflächen ohne explizite Synchronisationslogik zwischen den beteiligten UI-Komponenten.

Eine typische Rechnungsseite kann beispielsweise bestehen aus:

1. einer Tabelle der `Rechnung`-Objekte,
2. einer Tabelle für `Rechnung.positionen`,
3. einer durch die ausgewählte Tabellenzeile bestimmten Selektion der `Rechnungsposition`,
4. einem Formular für die selektierte `Rechnungsposition`.

Die Bindungskette lautet damit sinngemäß:

`selektierte Rechnung → positionen → ausgewählte Rechnungsposition → Detailformular`

Das Detailformular muss nicht wissen, aus welcher Tabelle seine Selektion stammt. Es ist lediglich an den Typ `Rechnungsposition` gebunden und zeigt dessen aktuelle Selektion.

Auch beim Wechsel eines Masters muss keine zusätzliche Synchronisationslogik modelliert werden. Die Laufzeit hält die abhängigen Bindungen und Selektionen konsistent.

### Formulare, Tabellen und Delegates

Ein `DelegateForm` beschreibt ein Formular. Seine Bindung bestimmt das dargestellte Objekt; seine Delegates bestimmen die sichtbaren Felder. Spaltengewichte legen die horizontale Aufteilung fest.

Ein `DelegateForm` kann entweder

* direkt an einen Entity- oder DTO-Typ und damit an dessen aktuelle Selektion oder
* an eine einzelne Property eines selektierten Entity- oder DTO-Objekts

gebunden werden.

Eine solche Property kann wiederum eine Entity, ein DTO oder ein Value Object liefern.

Ein `DelegateForm` liest seinen Bindungskontext, verändert jedoch keine Selektion.

Eine `Table` beschreibt eine Objektliste. Sie kann entweder den Root-Datenbestand einer `PagePane` oder eine Listen-Property eines selektierten Objekts darstellen.

Die Auswahl einer Tabellenzeile aktualisiert die gemeinsame Selektion ihres Zeilentyps.

Der Delegate-Typ folgt dem fachlichen Property-Typ, beispielsweise String, Integer, `BigDecimal`, Datum/Zeit, Status oder Referenz. Delegate-Optionen ergänzen Darstellung und Verhalten, etwa:

* Breite, Beschriftung und Ausrichtung,
* deaktivierte oder editierbare Darstellung,
* optionale Eingaben und Picker,
* Hervorhebung, Farbe oder Langbeschreibung,
* projektspezifische Hook- beziehungsweise Update-Logik.

Ein Delegate ersetzt keine fachliche Validierung. Fachliche Regeln gehören in das Domänenmodell beziehungsweise in Services und Commands; UI-Optionen steuern die Darstellung und Interaktion.

### Layouts, Tabs und Wiederverwendung

Ein `GridLayout` ordnet UI-Elemente in Zeilen und Spalten an. Zeilen- und Spaltengewichte bestimmen die Größenverteilung. So kann beispielsweise links eine Tabelle und rechts ein Formular stehen.

Ein `TabLayout` gruppiert UI-Elemente in Tabs. Jeder `Tab` besitzt eine Beschriftung und genau ein enthaltenes UI-Element.

Mit `Include` kann ein bereits deklariertes bindbares UI-Element wiederverwendet werden. Die Einbindung muss zur Datenbindung des umgebenden Kontexts passen. Sie erzeugt weder zusätzliche Daten noch einen unabhängigen Selektionsraum.

`CustomElement` bindet eine projektspezifische UI-Implementierung ein. Es ist sinnvoll, wenn Form, Table und Layouts den benötigten Darstellungsfall nicht ausdrücken. Die fachliche Datenbindung bleibt auch dann Teil des DataUX-Modells; nur die konkrete Darstellung wird projektspezifisch implementiert.

Die Zielgeräte sind bei der Layoutwahl mitzudenken. Eine breite Desktop-Aufteilung ist nicht automatisch für MDE-Geräte oder Smartphones geeignet. In `simpleone` existieren deshalb getrennte `PagePane`s für Desktop- und mobile Darstellungen desselben fachlichen Ablaufs.

### Menüs und Command-Aktionen

Eine `PagePane`, eine Tabelle oder ein dafür vorgesehenes UI-Element kann Menüeinträge bereitstellen. Eine `Action` (`MenuAction`) ruft einen ObjectFlow-`Command` auf; notwendige Argumente werden als Ausdrücke übergeben. Submenüs gruppieren weitere Einträge, Separatoren strukturieren längere Menüs.

Menüaktionen arbeiten mit dem aktuellen UI-Kontext. In Tabellenaktionen ist insbesondere die aktuelle Selektion des Zeilentyps relevant.

Vor dem Modellieren ist daher zu klären:

* Welcher Typ ist an der Aufrufstelle selektiert?
* Welche Command-Parameter müssen befüllt werden?
* Was geschieht bei leerer Selektion?
* Soll die Aktion global, im Overflow-Menü oder nur bei fokussierter Komponente angeboten werden?

Mehrstufige Abläufe können als Compound Action mehrere Commands verbinden. Page-Conclusions bestimmen dabei, unter welcher Abschlussart der Folgeablauf fortgesetzt wird.

### Ausdrücke und dynamische Darstellung

BaseLanguage-Ausdrücke werden nur an den von DataUX vorgesehenen Stellen eingebettet.

Typische Anwendungsfälle sind:

* dynamische Labels und Tile-Texte,
* Farben und Hervorhebungen,
* Aktivierungsbedingungen,
* Argumente für Command-Aufrufe,
* Darstellungsoptionen, die vom aktuellen Wert abhängen.

Welche Variablen sichtbar sind und welcher Ergebnistyp erwartet wird, hängt von der Einbettungsstelle ab.

Ausdrücke für die UI sollen Darstellungs- und Interaktionslogik enthalten; fachliche Berechnungen bleiben in den zuständigen fachlichen Komponenten und werden von dort aufgerufen.

### Typischer UI-Modellierungsablauf

1. Der Command und seine Pages legen fest, welche Daten und Aktionen der Ablauf benötigt.
2. Für jede Page wird der Root-Typ der UI bestimmt.
3. Die `PagePane` erhält diesen Entity- oder DTO-Typ als Bindungskontext.
4. Das oberste UI-Element wird gewählt: Formular, Tabelle oder Layout.
5. Formulare und Tabellen werden an Typen beziehungsweise geeignete Properties gebunden.
6. Tabellen können über die Auswahl ihrer Zeilen Selektionen für weitere UI-Komponenten bestimmen.
7. Delegates beschreiben Felder und Tabellenspalten.
8. Menüs rufen Commands mit Argumenten aus dem aktuellen Bindungs- und Selektionskontext auf.
9. Der Ablauf wird auch mit leerer Selektion, mehreren Root-Objekten und nicht geladenen Beziehungen geprüft.



## Teil II – Application / Batchjob

### Gemeinsamer Modulrahmen

`AppUI Module` (`AppUiModule`) und `BatchJob Module` (`BatchJobModule`) sind ausführbare Root-Konzepte. Beide bauen auf dem ObjectFlow-Container auf und besitzen einen gemeinsamen Rahmen:

| Bestandteil | Zweck |
| --- | --- |
| `configuration` | Optionale Standard-`OFXConfig`, insbesondere für den Start aus der Konsole |
| konfigurierte Komponenten | Im Modul verfügbare, konfigurierte Abhängigkeiten |
| Parameter und Variablen | Eingaben und Zustand des Modulcontainers |
| `onStartup` | Initialisierung beim Start |
| `onShutdown` | Aufräum- beziehungsweise Abschlusslogik |
| Authentifizierungsfunktion | Prüft beziehungsweise initialisiert den Benutzerkontext; bei Batchjobs ist sie vor allem bei vorhandener UI relevant |
| Moduloptionen | Metadaten und Laufzeitoptionen, etwa Version und offizieller Name |

Die Module definieren den technischen Rahmen, ersetzen jedoch nicht die fachlichen Commands, Services oder Repositories. Diese bleiben für den eigentlichen Anwendungsfall verantwortlich.


### Application mit `AppUI Module`

Ein `AppUI Module` beschreibt eine interaktive Anwendung. Neben dem gemeinsamen Modulrahmen besitzt es vor allem Navigation und Einstiegspunkte:

- `mainMenu`, `extrasMenu` und `helpMenu` strukturieren die Command-Aufrufe der Anwendung.
- Tiles bieten prominente, optional dynamisch beschriftete oder eingefärbte Einstiegspunkte.
- `tileInit` kann die für Tiles benötigten Werte initialisieren.
- Ein optionaler Startup-Command kann beim Start aufgerufen und über eine Bedingung aktiviert werden.
- `VERSION` und `OFFICIAL NAME` beschreiben sichtbare beziehungsweise paketierungsrelevante Modulmetadaten.

Eine Menüaktion oder ein Tile verweist auf einen ObjectFlow-Command. Das Modul stellt damit die Navigation bereit; der Command besitzt den fachlichen Ablauf und seine Pages, und die zugeordneten `PagePane`s beschreiben deren Oberfläche.

Der Zusammenhang ist:

```text
AppUI Module
  -> Menü / Tile
    -> ObjectFlow Command
      -> Page
        -> DataUX PagePane
```

Die Konfiguration und Authentifizierung werden zentral am Modul beschrieben. Fachliche Berechtigungen und Regeln sind dennoch in den dafür vorgesehenen fachlichen Komponenten zu prüfen und nicht allein durch das Ausblenden eines Menüeintrags zu ersetzen.


### Batchjob mit `BatchJob Module`

Ein `BatchJob Module` beschreibt eine ausführbare Hintergrundverarbeitung. Sein Kern sind ObjectFlow-Producer/Consumer-Paare. Ein Producer stellt Arbeit bereit; ein Consumer beziehungsweise ein vom Pair gestarteter Command verarbeitet sie. Mehrere Paare können in einem Modul zusammengefasst werden.

Ein Batchjob besitzt zusätzlich eine verpflichtende Exception-Strategie. Sie legt fest, wie Fehlerklassen oder passende Meldungen behandelt werden, beispielsweise durch verzögerte Wiederholung. Diese technische Fehlerstrategie ersetzt keine fachliche Fehlerbehandlung innerhalb des verarbeiteten Commands.

Wichtige Batch-Optionen sind:

| Option | Bedeutung |
| --- | --- |
| `CRON` (`OptCronPairExp`) | Zeitplan für ein bestimmtes Producer/Consumer-Paar |
| `DELAY` (`OptDelayPair`) | Wartezeit nach verarbeiteter Arbeit für ein bestimmtes Paar |
| `CONSUMERS` (`OptNumConsumersPair`) | Anzahl paralleler Consumer eines Paars |
| `DEPENDENT_CONSECUTIVE` (`OptBatchDependent`) | Paare werden abhängig und nacheinander behandelt |
| `RUN_IN_CONSOLE` (`OptRunInConsole`) | Start ohne instanziierte UI |
| Batch-UI einbinden (`OptIncludeBatchUi`) | Bindet einen Batchjob in einen UI-Modulkontext ein |
| `VERSION`, `OFFICIAL NAME` | Gemeinsame Modulmetadaten |

Zeitplan-, Delay- und Consumer-Optionen beziehen sich jeweils auf ein konkretes Pair. Bei mehreren Paaren muss deshalb bewusst entschieden werden, für welches Pair eine Option gilt.

Ein typischer Batchablauf lautet:

1. Das Modul startet mit seiner Konfiguration und führt gegebenenfalls `onStartup` aus.
2. Ein CRON-Ausdruck oder ein anderer Trigger aktiviert ein Producer/Consumer-Paar.
3. Der Producer ermittelt Arbeitseinheiten beziehungsweise Schlüssel.
4. Der Consumer oder ein aufgerufener Command verarbeitet die Arbeit.
5. Die Exception-Strategie entscheidet über technische Fehlerfolgen.
6. Beim Ende des Moduls wird `onShutdown` ausgeführt.


### Wahl zwischen Application und Batchjob

Ein `AppUI Module` ist passend, wenn Benutzer über Menüs, Tiles und Pages mit Commands interagieren. Ein `BatchJob Module` ist passend, wenn Arbeit automatisch, zeitgesteuert oder in Producer/Consumer-Strukturen verarbeitet wird.

Beide Formen dürfen auf dieselben fachlichen Services und Repositories zugreifen. UI und Batch sollten die fachliche Logik daher nicht duplizieren, sondern unterschiedliche Einstiegspunkte in dieselben fachlichen Fähigkeiten bilden.


## Durchgängige Abläufe

### Interaktive Suche und Bearbeitung

1. Eine Menüaktion des `AppUI Module` startet einen Such-Command.
2. Dessen erste Page stellt ein Filterobjekt bereit; eine `PagePane` zeigt es in einem `DelegateForm`.
3. Nach der Suche stellt eine weitere Page eine Ergebnisliste bereit; eine `Table` zeigt die Ergebnisse.
4. Die gewählte Tabellenzeile wird zur gemeinsamen Selektion des Ergebnis- beziehungsweise Entity-Typs.
5. Eine Tabellenaktion startet den Bearbeitungs-Command mit der selektierten ID oder Instanz.
6. Die Bearbeitungs-Page nutzt eine `PagePane` mit Formular, Detailtabelle und gegebenenfalls weiteren Detailformularen.

### Batchverarbeitung mit optionaler UI

1. Ein `BatchJob Module` konfiguriert Pair, Zeitplan und Exception-Strategie.
2. Der Producer stellt die zu verarbeitenden Objekte oder Schlüssel bereit.
3. Ein Command verarbeitet jeweils eine Arbeitseinheit und kann definierte Pages besitzen.
4. Beim reinen Konsolenbetrieb wird keine UI instanziiert.
5. Wird der Batchjob in eine Anwendung eingebunden, können vorhandene Pages durch passende `PagePane`s sichtbar gemacht werden.


## Häufige Fehler und Diagnose

- **UI-Bindung mit Laden verwechseln:** Eine gebundene Referenz oder Liste muss fachlich bereits geladen beziehungsweise bereitgestellt sein.
- **Unabhängige Tabellenselektionen erwarten:** Tabellen desselben Objekttyps teilen sich die Selektion innerhalb der `PagePane`.
- **Leere Selektion nicht berücksichtigen:** Formulare zeigen dann keine Daten; Aktionen müssen diesen Zustand vertragen oder deaktiviert sein.
- **Zeilen- und Parent-Typ verwechseln:** Bei einer Tabelle ist zwischen dem Objekt der Listen-Property und dem Zeilentyp zu unterscheiden.
- **Include als neuen Kontext verstehen:** `Include` verwendet eine bestehende UI-Beschreibung, erzeugt aber weder Daten noch eine eigene Selektion.
- **Fachlogik in UI-Ausdrücke verschieben:** Dynamische Labels und Farben sind UI-Aufgaben; Geschäftsregeln gehören in Domänenobjekte, Services oder Commands.
- **Command-Argumente aus dem falschen Selektionskontext bilden:** Vor allem Tabellenaktionen müssen den tatsächlich selektierten Zeilentyp verwenden.
- **Batchoption keinem Pair eindeutig zuordnen:** CRON, Delay und Consumer-Anzahl referenzieren jeweils ein konkretes Producer/Consumer-Paar.
- **Exception-Strategie als fachliche Fehlerbehandlung behandeln:** Sie steuert den technischen Umgang mit Ausnahmen, nicht die Domänenentscheidung.
- **Desktop-Layout unverändert mobil verwenden:** Für MDE beziehungsweise Smartphone sind oft eigene `PagePane`s sinnvoll.


## Offene Dokumentationsbereiche

### `API Description` (`ApiDescription`)

Die Modellierung von APIs, Endpoints, Operationen, Serialisierung und Antworten ist in dieser Fassung bewusst noch nicht beschrieben.

### Verwendete Konzepte

Ein vollständiger fachlicher Konzeptindex mit allen Delegate-, Form-, PagePane-, Menü-, Modul- und Optionskonzepten bleibt offen. Für konkrete Modelländerungen sind bis dahin die MPS-Sprachdefinition, die Projektbeispiele und die generierte lokale Skill-Referenz maßgeblich.


## Quellen für die Modellarbeit

Die Beschreibung beruht auf der bereitgestellten Hintergrundinformation sowie auf der live geladenen DataUX-Sprachdefinition und den Beispielen des geöffneten Projekts `simpleone`. Besonders aussagekräftig sind dort:

- `PPOrderEditor`: Grid mit Positions-Tabelle und gebundenem Kopfformular,
- `Search Order Pane`: Suchformular mit verschiedenen Delegate-Typen,
- `THE List of Orders`: Filter, Ergebnistabelle, dynamische Darstellung und Command-Aktionen,
- `App_Desktop_Order`: Menüs, Submenüs, Tiles, Konfiguration und Authentifizierung,
- `PrintingJob`: CRON-gesteuertes Pair, Exception-Strategie und Modulmetadaten.

Für konkrete Modelländerungen bleiben die geladene MPS-Sprache, ihre Constraints, die Typprüfung und die Validierung die technische Quelle der Wahrheit.
