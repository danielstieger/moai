# DataUX (`org.modellwerkstatt.dataux`) – Benutzeroberflächen und ausführbare Module

## Modellierungsumfang und Ausdrucksmöglichkeiten

`org.modellwerkstatt.dataux` ist eine der drei domänenspezifischen Sprachen der **modellwerkstatt moware werkbank**. Sie verbindet zwei Aufgabenbereiche:

1. **UI-Modellierung:** Eine Oberfläche wird aus fachlich gebundenen `PagePane`s, Formularen, Tabellen, Layouts und Aktionen aufgebaut.
2. **Application / Batchjob:** Ausführbare Module konfigurieren den Start und das Ende einer Anwendung, Authentifizierung, Menüs beziehungsweise Batch-Verarbeitung und die zugehörige Laufzeitkonfiguration.

Die Sprache beschreibt vor allem, **welche fachlichen Daten wie verwendet werden**. Generator und Laufzeit übernehmen die technische Umsetzung. An dafür vorgesehenen Stellen können BaseLanguage-Ausdrücke eingebettet werden, etwa für Beschriftungen, Farben, Bedingungen oder Lebenszykluslogik.

| Fragestellung | UI-Modellierung | Application / Batchjob |
| --- | --- | --- |
| Primärer Zweck | Fachliche Daten anzeigen, bearbeiten und Aktionen anbieten | Ein ausführbares Modul und seinen Lebenszyklus konfigurieren |
| Typischer Einstieg | `PagePane` | `AppUI Module` (`AppUiModule`) oder `BatchJob Module` (`BatchJobModule`) |
| Zentrale Zusammenarbeit | ObjectFlow-`Command` und dessen `Page`s | ObjectFlow-Konfiguration, Commands und Producer/Consumer-Paare |
| Hauptstruktur | Formulare, Tabellen, Layouts, Menüs | Start/Shutdown, Authentifizierung, Menüs/Tiles oder Batch-Paare |
| Fachliche Daten | Gebundene Entity- oder DTO-Instanzen und deren Properties | Parameter, Variablen, konfigurierte Komponenten und Laufzeitkonfiguration |


## Teil I – UI-Modellierung

### Pages und `PagePane`s

Eine **Page** gehört zu einem ObjectFlow-`Command` und beschreibt eine Seite seines Interaktionsablaufs. Eine `PagePane` bildet das Gegenstück auf der UI-Seite: Sie beschreibt den sichtbaren Inhalt dieser Page.

Eine `PagePane` besitzt genau ein oberstes UI-Element. Dieses kann unmittelbar ein Formular oder eine Tabelle sein oder ein Layout, das weitere UI-Elemente enthält. Zusätzlich kann die `PagePane` Optionen und Menüaktionen enthalten.

| Begriff | Bedeutung |
| --- | --- |
| Page | Seite im Ablauf eines Commands; stellt Daten und Aktionen bereit |
| `PagePane` | Wiederverwendbare UI-Beschreibung für eine Page |
| gebundener Klassifikator | Entity- oder DTO-Typ, der den Bindungskontext der `PagePane` bestimmt |
| gebundene Property | Optionaler Pfad zu einem einzelnen Objekt oder einer Liste innerhalb des Kontexts |
| UI-Element | Formular, Tabelle, Layout oder projektspezifisches Element innerhalb der `PagePane` |

Die Page stellt die Daten bereit; die `PagePane` stellt sie dar. Eine UI-Bindung lädt keine Daten nach. Benötigte Referenzen und Listen müssen deshalb bereits durch den Command beziehungsweise seine Repositories geladen und an die Page übergeben worden sein.


### Datenbindung und gemeinsame Selektion

Die Datenbindung folgt fachlichen Objekten und ihren Beziehungen. Innerhalb einer `PagePane` gibt es für jeden Objekttyp – Entity oder DTO – genau eine gemeinsame Selektion. Sie bezeichnet das aktuell ausgewählte Objekt dieses Typs.

Komponenten nutzen diese Selektion unterschiedlich:

| Bindung | Bedeutung |
| --- | --- |
| an einen Objekttyp | Verwendet das aktuell selektierte Objekt dieses Typs |
| an eine einzelne Property | Zeigt oder bearbeitet einen Wert des gebundenen Objekts |
| an eine Listen-Property | Stellt deren Elemente bereit, typischerweise als Tabellenzeilen |

Wird nur ein Objekt eines Typs bereitgestellt, wird es automatisch zur Selektion dieses Typs. Bei mehreren Objekten kann eine Tabelle die Selektion durch die ausgewählte Zeile bestimmen. Davon abhängige Formulare und Tabellen reagieren auf dieselbe gemeinsame Selektion.

#### Mehrere Tabellen desselben Typs

Mehrere Tabellen mit demselben Zeilentyp besitzen keine unabhängigen Selektionen. Wird in einer Tabelle ein Objekt gewählt, gilt diese Auswahl für den gesamten `PagePane`-Kontext:

- Enthält eine andere Tabelle dasselbe Objekt, zeigt sie es ebenfalls als ausgewählt.
- Enthält sie das Objekt nicht, zeigt sie keine ausgewählte Zeile; die gemeinsame Selektion bleibt trotzdem bestehen.

#### Leere Selektion

Ohne selektiertes Objekt zeigt ein daran gebundenes `DelegateForm` keine Daten. Tabellen können ihre vorhandenen Zeilen weiterhin anzeigen, besitzen jedoch keine ausgewählte Zeile.

#### Master-Detail

Die gemeinsame Selektion ermöglicht Master-Detail-Oberflächen ohne separate Synchronisationslogik. Eine typische Rechnungsseite besteht beispielsweise aus:

1. einem Formular für die selektierte `Rechnung`,
2. einer Tabelle für deren `positionen`,
3. einer durch die Tabellenzeile bestimmten Selektion der `Rechnungsposition`,
4. einem Formular für die selektierte Position.

Entscheidend ist die Bindungskette: Das Rechnungsformular folgt der `Rechnung`, die Tabelle folgt deren Listen-Property, und das Positionsformular folgt dem Zeilentyp der Tabelle.


### Formulare, Tabellen und Delegates

Ein `DelegateForm` beschreibt ein Formular. Seine Bindung bestimmt das aktuell dargestellte Objekt; seine Delegates bestimmen die sichtbaren Felder. Spaltengewichte legen die horizontale Aufteilung fest.

Eine `Table` beschreibt eine Objektliste. Die Tabellenbindung bestimmt die Liste und den Zeilentyp. Delegates werden hier als Spalten verwendet. Die Auswahl einer Zeile aktualisiert die gemeinsame Selektion des Zeilentyps.

Der Delegate-Typ folgt dem fachlichen Property-Typ, beispielsweise String, Integer, `BigDecimal`, Datum/Zeit, Status oder Referenz. Delegate-Optionen ergänzen Darstellung und Verhalten, etwa:

- Breite, Beschriftung und Ausrichtung,
- deaktivierte oder editierbare Darstellung,
- optionale Eingaben und Picker,
- Hervorhebung, Farbe oder Langbeschreibung,
- projektspezifische Hook- beziehungsweise Update-Logik.

Ein Delegate ersetzt keine fachliche Validierung. Fachliche Regeln gehören in das Domänenmodell beziehungsweise in Services und Commands; UI-Optionen steuern die Darstellung und Interaktion.


### Layouts, Tabs und Wiederverwendung

Ein `GridLayout` ordnet UI-Elemente in Zeilen und Spalten an. Zeilen- und Spaltengewichte bestimmen die Größenverteilung. So kann beispielsweise links eine Tabelle und rechts ein Formular stehen.

Ein `TabLayout` gruppiert UI-Elemente in Tabs. Jeder `Tab` besitzt eine Beschriftung und genau ein enthaltenes UI-Element.

Mit `Include` kann ein bereits deklariertes bindbares UI-Element wiederverwendet werden. Die Einbindung muss zur Datenbindung des umgebenden Kontexts passen. Sie erzeugt weder zusätzliche Daten noch einen unabhängigen Selektionsraum.

`CustomElement` bindet eine projektspezifische UI-Implementierung ein. Es ist sinnvoll, wenn Form, Table und Layouts den benötigten Darstellungsfall nicht ausdrücken. Die fachliche Datenbindung bleibt auch dann Teil des DataUX-Modells; nur die konkrete Darstellung wird projektspezifisch implementiert.

Die Zielgeräte sind bei der Layoutwahl mitzudenken. Eine breite Desktop-Aufteilung ist nicht automatisch für MDE-Geräte oder Smartphones geeignet. In `simpleone` existieren deshalb getrennte `PagePane`s für Desktop- und mobile Darstellungen desselben fachlichen Ablaufs.


### Menüs und Command-Aktionen

Eine `PagePane`, eine Tabelle oder ein dafür vorgesehenes UI-Element kann Menüeinträge bereitstellen. Eine `Action` (`MenuAction`) ruft einen ObjectFlow-`Command` auf; notwendige Argumente werden als Ausdrücke übergeben. Submenüs gruppieren weitere Einträge, Separatoren strukturieren längere Menüs.

Menüaktionen arbeiten mit dem aktuellen UI-Kontext. In Tabellenaktionen ist insbesondere die aktuelle Selektion des Zeilentyps relevant. Vor dem Modellieren ist daher zu klären:

- Welcher Typ ist an der Aufrufstelle selektiert?
- Welche Command-Parameter müssen befüllt werden?
- Was geschieht bei leerer Selektion?
- Soll die Aktion global, im Overflow-Menü oder nur bei fokussierter Komponente angeboten werden?

Mehrstufige Abläufe können als Compound Action mehrere Commands verbinden. Page-Conclusions bestimmen dabei, unter welcher Abschlussart der Folgeablauf fortgesetzt wird.


### Ausdrücke und dynamische Darstellung

BaseLanguage-Ausdrücke werden nur an den von DataUX vorgesehenen Stellen eingebettet. Typische Anwendungsfälle sind:

- dynamische Labels und Tile-Texte,
- Farben und Hervorhebungen,
- Aktivierungsbedingungen,
- Argumente für Command-Aufrufe,
- Darstellungsoptionen, die vom aktuellen Wert abhängen.

Welche Variablen sichtbar sind und welcher Ergebnistyp erwartet wird, hängt von der Einbettungsstelle ab. Ausdrücke für die UI sollen Darstellungs- und Interaktionslogik enthalten; fachliche Berechnungen bleiben in den zuständigen fachlichen Komponenten und werden von dort aufgerufen.


### Typischer UI-Modellierungsablauf

1. Der Command und seine Pages legen fest, welche Daten und Aktionen der Ablauf benötigt.
2. Für jede Page wird der gebundene Entity- oder DTO-Typ bestimmt.
3. Die `PagePane` erhält diesen Typ als Bindungskontext.
4. Das oberste UI-Element wird gewählt: Formular, Tabelle oder Layout.
5. Formulare und Tabellen werden an Typen beziehungsweise Properties gebunden.
6. Delegates beschreiben Felder und Tabellenspalten.
7. Menüs rufen Commands mit Argumenten aus dem aktuellen Bindungs- und Selektionskontext auf.
8. Der Ablauf wird auch mit leerer Selektion, mehreren Objekten und nicht geladenen Beziehungen geprüft.


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
