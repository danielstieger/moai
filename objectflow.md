# ObjectFlow (org.modellwerkstatt.objectflow) – Fachliches Modell, Services und Anwendungsabläufe

## Modellierungsumfang und Ausdrucksmöglichkeiten

`org.modellwerkstatt.objectflow` ist eine der drei domänenspezifischen Sprachen der **modellwerkstatt moware werkbank**. Sie beschreibt fachliche Datenstrukturen, Domänen- und Anwendungslogik sowie die Abläufe, in denen Benutzer, Batchjobs und Tests diese Logik ausführen.
ObjectFlow verbindet fünf Aufgabenbereiche:

1. **Datenmodellierung:** `Entity`, `Value Object` und `DTO` beschreiben fachliche Objekte, Werte und anwendungsbezogene Datencontainer.
2. **Domänenlogik:** Zustandsübergänge, Berechnungen und fachliche Prüfungen liegen in den Datenstrukturen selbst oder häufig in zustandslosen `Service`-Komponenten.
3. **Anwendungsabläufe:** `Command`s modellieren die mögliche Interaktion mit dem Endanwender. Sie können mehrere Pages mit Conclusions beinhalten, verwalten die Session und koordinieren Services und Repositories.
4. **Tests:** `OFX Test Suit`s führen fachliche Tests und vollständige Commands ohne Benutzeroberfläche aus.
5. **Querschnitt:** Konfiguration, Rollen und Berechtigungen, statische Ressourcen, Logging und Serialisierung ergänzen die fachlichen Bausteine.

Im Folgenden bezeichnet **Name** die Bezeichnung, die in MPS typischerweise sichtbar ist oder eingegeben wird. Der **Konzeptname** ist die technische AST-Bezeichnung und steht jeweils in Klammern. Bei einem ObjectFlow-Konzept genügt dort der kurze Konzeptname; gehört das angesprochene Konzept zu einer anderen DSL, steht in Klammern dessen **FQ-Name**. Die Konzepttabellen führen FQ-Namen zusätzlich explizit auf – primär für KI-Agenten.

Die Dokumentation beschreibt beobachtete und technisch bestätigte Praxis. Sie legt keine zusätzliche, von der Sprache nicht erzwungene Architektur fest. Wo sich aus bestehenden Anwendungen wiederkehrende Empfehlungen ergeben, werden diese als solche benannt.


## Teil I – Fachliche Datenmodellierung

### Entity, Value Object und DTO

ObjectFlow bildet fachliche Datenstrukturen mit `Entity`, `Value Object` und `DTO` ab. Die Unterscheidung folgt den Grundideen des Domain-Driven Design, ohne damit sämtliche DDD-Regeln technisch zu erzwingen:

- Eine **Entity** wird durch ihre Identität und ihren Lebenszyklus bestimmt. Eine Rechnung bleibt beispielsweise dieselbe Rechnung, wenn sich Anschrift, Positionen oder Status ändern; entscheidend ist ihre fachliche oder technische Identität, etwa Rechnungsnummer oder interne ID.
- Ein **Value Object** beschreibt einen fachlichen Wert ohne eigene Identität. Zwei Werte sind gleich, wenn ihre dafür ausgewählten Bestandteile gleich sind. Ein einfaches Beispiel ist ein Datum; ein zusammengesetztes Beispiel ist eine Gültigkeit aus Beginn und Toleranztagen. Value Objects sind im Anwendungscode im unveränderlichen Stil zu verwenden: Statt eine vorhandene Instanz schrittweise umzuschreiben, wird bei einer Änderung ein neuer Wert erzeugt. Dadurch bleiben Gleichheit, Wiederverwendung und Weitergabe des Werts nachvollziehbar.
- Ein **DTO** (*Data Transfer Object*) ist ein anwendungsbezogener Datencontainer ohne eigene fachliche oder technische Entity-Identität. DTOs eignen sich für Suchfilter, Projektionen, Aggregationen und die Übergabe zwischen Abläufen. Sie dürfen selbst Objektgraphen bilden und dabei Entities sowie Listen von Entitäten enthalten.

Fachliche Modelle bestehen typischerweise nicht aus isolierten Objekten, sondern aus Graphen. Eine Rechnung kann beispielsweise eine Liste von Rechnungspositionen referenzieren; Rechnung und Positionen können ihrerseits Value Objects wie Geldbetrag, Anschrift oder Gültigkeit verwenden. Referenzen drücken dabei den fachlichen Zusammenhang aus, Listen eine geordnete Menge gleichartiger Bestandteile.

Die drei rootfähigen Datenstrukturen besitzen Business Properties und können zusätzlich Konstruktoren und Methoden (BaseLanguage-Member) enthalten.

| Name | Konzeptname | Primärer Zweck | Identität und Lebenszyklus |
| --- | --- | --- | --- |
| `Entity` | `Entity` | Fachliches Objekt, das typischerweise über ManMap persistiert und innerhalb einer Session bearbeitet wird | Besitzt eine fachliche oder technische Identität; Gleichheit wird nicht nur aus allen Werten abgeleitet |
| `Value Object` | `ValueObject` | Zusammengesetzter fachlicher Wert, beispielsweise Geldbetrag oder zusammengesetzter Schlüssel | Keine eigenständige Entity-Identität; ausgewählte Properties können die Wertgleichheit bestimmen |
| `DTO` | `DTO` | Datencontainer für Suche, Darstellung, Aggregation oder Übergabe von Daten zwischen Abläufen | Nicht selbst als persistentes Domänenobjekt gedacht; konkretes Read-only- und Session-Verhalten hängt von seiner Erzeugung ab |

Die Modellierung einer Entity oder eines fachlichen Objektgraphen bewirkt noch keine Persistenz. Tabellen, Schlüssel, Referenzen sowie Lade- und Speicheroperationen werden mit `org.modellwerkstatt.manmap` beschrieben; die Einzelheiten stehen in [manmap.md](manmap.md).

### Business Properties

Eine Business Property (`BusinessProperty`) besteht mindestens aus Name, Typ und Property-Implementierung. Zusätzlich können Kurz- und Langbeschreibung, Zahlenformat, Dokumentation, Sichtbarkeit sowie ManMap-Feldoptionen modelliert werden.

| Bestandteil | Rolle |
| --- | --- |
| Name | Fachlicher und technischer Property-Name |
| Typ | BaseLanguage- beziehungsweise ObjectFlow-Typ der Property |
| Kurzbeschreibung | Kompakte, von Oberflächen verwendbare Beschriftung |
| Langbeschreibung | Ausführlichere Beschreibung für Darstellung und Dokumentation |
| Format | Standardformat für `BigDecimal`-Darstellungen (nach `java.text.DecimalFormat`) und Datumsdarstellungen (nach `org.joda.time.format.DateTimeFormatter`) |
| Property-Optionen | ManMap-Optionen wie `key`, `autoid`, Audit-, Größen- oder Indexhinweise |

Der Editor schränkt den Typ einer Business Property bewusst ein. Die folgende Liste ist vollständig; beliebige BaseLanguage- oder Java-Typen werden an dieser Stelle nicht angeboten.

| Möglicher Typ | FQ-Name des Typs oder Konzeptname | Bedeutung und Einschränkung |
| --- | --- | --- |
| `string` | `jetbrains.mps.baseLanguage.structure.StringType` | Der von MPS besonders unterstützte String-Typ. Er wird direkt angeboten und nicht als manuell gewählter `java.lang.String`-Classifier modelliert. |
| `int` | `jetbrains.mps.baseLanguage.structure.IntegerType` | Ganzzahliger primitiver Wert. Als Java-Primitive kann er nicht `null` sein. |
| `LocalDate` | `org.joda.time.LocalDate` | Datum ohne Uhrzeit. |
| `DateTime` | `org.joda.time.DateTime` | Zeitpunkt mit Datum und Uhrzeit. |
| `BigDecimal` | `java.math.BigDecimal` | Exakte Dezimalzahl, insbesondere für Geldbeträge und fachliche Rechenwerte. |
| deklarierter Status | `org.modellwerkstatt.objectflow.structure.StatusType` | Referenziert genau eine im Modell oder über Importe sichtbare `StatusDeclaration`. |
| deklarierte Entity | `org.modellwerkstatt.objectflow.structure.Entity` | Referenziert eine sichtbare ObjectFlow-Entity und bildet eine Beziehung im fachlichen Objektgraphen. |
| deklariertes Value Object | `org.modellwerkstatt.objectflow.structure.ValueObject` | Verwendet einen sichtbaren zusammengesetzten fachlichen Wert. |
| deklariertes DTO | `org.modellwerkstatt.objectflow.structure.DTO` | Referenziert einen sichtbaren anwendungsbezogenen Datencontainer. |
| `list<T>` | `jetbrains.mps.baseLanguage.collections.structure.ListType` | Modelliert eine Liste. Der Elementtyp `T` soll wiederum ein für die fachliche Datenstruktur geeigneter Typ sein. |
| `byte[]` | `jetbrains.mps.baseLanguage.structure.ArrayType` mit `jetbrains.mps.baseLanguage.structure.ByteType` | Binärdaten, beispielsweise ein Dokument oder Bildinhalt. |

Persistenzoptionen an einer Business Property werden von ManMap ausgewertet. Ihre genaue Wirkung ist in [manmap.md](manmap.md) beschrieben.

### Virtuelle Business Properties

Eine Business Property kann statt eines eigenen gespeicherten Werts eine benutzerdefinierte Property-Implementierung (`CustomPropertyImplementation`) besitzen. Ihr `get`-Accessor berechnet oder beschafft den Wert bei jedem Lesen; ein optionaler `set(value)`-Accessor verteilt einen zugewiesenen Wert auf andere Properties oder führt eine passende Aktualisierung aus. Ohne `set`-Accessor ist die virtuelle Property nur lesbar.

Virtuelle Properties behalten die fachlichen Metadaten einer Business Property – Typ, Kurz- und Langbeschreibung, Format und Dokumentation – und können deshalb wie normale Properties in Ausdrücken und DataUX-Bindings verwendet werden. Sie besitzen jedoch keinen eigenen Wert, der unabhängig persistiert werden könnte. Häufig kennzeichnet `PRESENTATION` eine nur für Berechnung oder Darstellung bestimmte Property.

Für eine Rechnung könnte beispielsweise `offenerBetrag` als virtuelle, nur lesbare Property aus `gesamtbetrag - bezahlterBetrag` berechnet werden. Eine solche Ableitung bleibt zentral im Fachmodell und steht zugleich für Anzeige, Meldungen und weitere Berechnungen zur Verfügung. Getter können keine Repositories oder Services aufrufen; für sie gilt dieselbe Infrastrukturgrenze wie für andere Methoden der Datenstruktur.

### Value-Object-Gleichheit

Ein `Value Object` kann über `equal properties` (`EqualPropertyReference`) festlegen, welche seiner Business Properties die Wertgleichheit bestimmen. Das ist insbesondere für zusammengesetzte Schlüssel und fachliche Werte nützlich. Die ausgewählten Properties sollen gemeinsam den fachlichen Wert repräsentieren; technische oder nur darstellungsbezogene Properties gehören üblicherweise nicht dazu.


### Null-Werte in Datenstrukturen

Anders als bei standard Java-Klassen werden die Properties von Datenstrukturen initialisiert. `string` beginnt als leere Zeichenkette, `int` als `0`, `BigDecimal` als `0.0`, ein Status mit seinem Default- beziehungsweise `ON_CREATION`-Element und eine Liste als leere Liste. Anwendungscode soll diese Werte deshalb nicht vorsorglich durch `null` ersetzen; insbesondere Listen werden als leere Listen verwendet.

Das bedeutet nicht, dass jeder enthaltene Referenzwert immer gesetzt ist. Datum/Zeit sowie Beziehungen zu Entities, Value Objects und DTOs können fachlich fehlen; auch die Laufzeit-Setter der Referenztypen unterstützen optionale Werte. `null` soll dann ausdrücklich „kein Wert vorhanden“ bedeuten und nicht als Ersatz für einen regulären Zustand dienen. `int` kann als primitiver Typ nicht `null` sein. In DataUX kennzeichnet die Delegate-Option `OPTIONAL`, dass ein Eingabewert fehlen darf; ohne diese Option setzt die Oberfläche einen erforderlichen Wert durch.

Der ObjectFlow ersetzt allgemeine Gleichheits- und Ungleichheitsausdrücke durch einen null-sicheren Vergleich: Zwei `null`-Werte gelten als gleich, genau ein `null`-Wert als ungleich; andernfalls wird `equals` verwendet. Die Laufzeit stellt zusätzlich einen null-sicheren `BigDecimal`-Vergleich über `compareTo` bereit, wenn die fachliche Gleichheit unabhängig von der Skala sein soll. Diese Hilfen verhindern NullPointerExceptions beim Vergleichen, ersetzen aber keine bewusste fachliche Entscheidung über optionale Werte.


### Beziehungen und Objektgraphen

Eine Business Property kann eine Entity, ein DTO oder ein Value Object sowie eine Liste geeigneter Elemente enthalten. Aus diesen Beziehungen entsteht der fachliche Objektgraph. Die Aggregatgrenze soll dabei bewusst erkennbar bleiben: Ein Graph bündelt die Objekte, die für eine fachliche Änderung gemeinsam konsistent gehalten werden müssen; bloße Querverweise auf andere Aggregate sind davon zu unterscheiden.

Mit `#Key` (`BPRefIdReference`) wird bei einer Entity-Beziehung ausdrücklich auf die Identität der referenzierten Entity statt auf das vollständige fachliche Objekt zugegriffen. Das Ergebnis besitzt den Schlüsseltyp der Ziel-Entity. Bei einem zusammengesetzten Schlüssel können dessen Bestandteile anschließend einzeln gelesen werden; bei einem einfachen Schlüssel kann das Ergebnis direkt verglichen oder weitergegeben werden.

Der wichtigste Einsatz ist das explizite Nachladen einer Beziehung. ManMap lädt Referenz-Properties nur dann als Objekt, wenn die Repository-Query dafür einen Reference Join enthält. Der Fremdschlüssel steht dagegen auch dann über `#Key` zur Verfügung. Eine geladene Rechnung kann daher beispielsweise ihren Kundenschlüssel an ein Repository übergeben, ohne dass die Kunden-Entity bereits Teil des geladenen Graphen ist:

```text
Kunde kunde = # KundenRepo.get(rechnung.kunde#Key);
boolean gleicherKunde = rechnung.kunde#Key.equals(gutschrift.kunde#Key);
```

Der erste Ausdruck lädt die Kunden-Entity gezielt über das Repository. Der zweite vergleicht zwei Beziehungen ausschließlich anhand ihrer Identität. Bei einem zusammengesetzten Schlüssel wäre zusätzlich ein Zugriff wie `rechnung.aussteller#Key.mandant` möglich. `#Key` selbst führt keinen Repository-Aufruf aus und lädt die Entity nicht nach.

Auf `rechnung.kunde` direkt zuzugreifen setzt dagegen voraus, dass die Kundenreferenz von der ursprünglichen Query mitgeladen wurde. Fehlt der entsprechende Reference Join, löst der Zugriff `OFXNotInitializedException` aus. Die Wahl ist deshalb bewusst zu treffen: Entweder lädt die ursprüngliche Query die benötigte Beziehung mit, oder der Ablauf verwendet zunächst `#Key` und lädt die Entity über einen passenden Entity-Mapper.

Mit `isNullKey` (`IsNull`) lässt sich prüfen, ob ein solcher Referenzschlüssel fachlich nicht gesetzt ist:

```text
rechnung.kunde#Key.isNullKey
```

Die Prüfung kennt die ObjectFlow/ManMap-Semantik leerer Schlüssel und ist deshalb aussagekräftiger als ein bloßer Vergleich mit Java-`null`: Auch die Leerwerte einfacher Schlüssel und die Bestandteile eines zusammengesetzten Value-Object-Schlüssels werden berücksichtigt. Das ist besonders bei optionalen Beziehungen sinnvoll, bevor der Schlüssel an ein Repository übergeben oder ein Bestandteil des Schlüssels gelesen wird. `isNullKey` prüft den Schlüssel; es prüft nicht, ob das referenzierte Objekt bereits geladen wurde.

### Status

Ein Status (`StatusDeclaration`) übernimmt in fachlichen Datenstrukturen die Rolle, die in reinem Java häufig ein `enum` erfüllt: Er begrenzt einen Wert auf eine benannte Menge zulässiger Zustände. Er kann jedoch mehr als ein einfaches Java-Enum. Ein Statuselement (`StatusElement`) besitzt neben seinem Namen einen technischen Persistenzwert, Kurz- und Langbeschreibung sowie optionale Metadaten für Erzeugung, Laden und Darstellung. Statuswerte können als Property-Typ verwendet, verglichen, in SQL referenziert und durch DataUX mit Beschriftung und Farbe dargestellt werden.

Wichtige Ausdrucksmittel sind:

| Name | Konzeptname | Bedeutung |
| --- | --- | --- |
| Status | `StatusDeclaration` | Deklariert die erlaubten Werte eines fachlichen Status |
| Statuselement | `StatusElement` | Einzelner Status mit Persistenzwert und Beschreibungen |
| Status-Typ | `StatusType` | Verwendet einen deklarierten Status als Property- oder Variablentyp |
| `of` | `StatusOfOperator` | Prüft, ob ein Wert einem oder mehreren Statuselementen entspricht |
| `fromDbValue` | `StatusFromDbValue` | Ermittelt ein Statuselement aus seinem Datenbankwert |

Die Optionen liegen entweder an der Statusdeklaration oder an einem einzelnen Statuselement:

| Name | Konzeptname | Ort | Wirkung |
| --- | --- | --- | --- |
| `ALLOW_NULL_PERSISTANCE` | `AllowNullStatusDeclOption` | Statusdeklaration | Erlaubt, für diesen Status einen fehlenden Wert zu persistieren. Die historische Schreibweise `PERSISTANCE` ist Teil der DSL. |
| `OPTIONAL_AS` | `OptionalAsStatusDeclOption` | Statusdeklaration | Legt eine abweichende sichtbare Beschriftung für den optionalen, nicht gesetzten Status fest. |
| `ON_CREATION` | `OnCreationStatusElemOption` | Statuselement | Verwendet dieses Element als Anfangszustand bei der Erzeugung eines Objekts. |
| `COLOR` | `ColorStatusElemOption` | Statuselement | Verknüpft das Element mit einer statischen ObjectFlow-Farbe für die Standarddarstellung. |
| `WHEN_NULL_WL` | `WhenNullOnDbStatusElemOption` | Statuselement | Verwendet dieses Element beim Laden, wenn der Persistenzwert `null` oder leer ist. |
| `WHEN_UNDEFINED_WL` | `WhenUndefinedStatusElemOption` | Statuselement | Verwendet dieses Element beim Laden, wenn der vorhandene Persistenzwert keinem deklarierten Element entspricht. |

`WHEN_NULL_WL` und `WHEN_UNDEFINED_WL` behandeln unterschiedliche Fälle. Ein leerer Wert kann fachlich erlaubt sein; ein unbekannter Wert weist dagegen häufig auf fehlerhafte Daten oder eine nicht abgestimmte Version hin. Der zweite Fallback darf diesen Fehler daher nur dann in einen normalen Status überführen, wenn dies fachlich ausdrücklich beabsichtigt ist.

### Methoden an Datenstrukturen

Entities, Value Objects und DTOs können BaseLanguage-Konstruktoren und -Methoden enthalten. Dort gehört allgemeine, objektbezogene Logik hin, die aus vielen Anwendungsfällen benötigt wird und allein mit dem Zustand des Objekts sowie expliziten Parametern auskommt. Typische Beispiele sind Berechnungen, Zustandsabfragen, Wertnormalisierung und Operationen, die ein Aggregat konsistent verändern, etwa das Hinzufügen oder Entfernen einer Position.

Von einer Datenstruktur aus ist kein Komponentenaufruf `#Component_Name.Methoden_Name()` (`OperationCall`) auf Services, Repositories oder andere Infrastrukturkomponenten möglich. Daraus folgen klare Entwurfsregeln:

- Eine Methode an einer Datenstruktur kann keine fehlenden Daten nachladen.
- Benötigte Werte werden vom Aufrufer vorab bereitgestellt oder als Parameter übergeben.
- Logik, die andere Aggregate, Repositories, Konfiguration oder weitere Komponenten benötigt, liegt in einem Service.
- Die Datenstrukturmethoden bleiben dadurch in unterschiedlichen Commands, Jobs und Tests wiederverwendbar und lassen sich ohne Laufzeitkonfiguration prüfen.

Die Grenze ist fachlich zu ziehen: Verhalten, das natürlich zu genau diesem Objekt oder Wert gehört, bleibt an der Datenstruktur. Eine allgemeine Domänenoperation über mehrere Objekte gehört in einen wiederverwendbaren Service. Die Koordination für einen konkreten Anwendungsfall gehört in einen anwendungsfallspezifischen Service oder Command.

### Dirty-Tracking, Read-only und unveränderliche Werte

Entitäten führen einen Dirty-Zustand. Wird einer normalen Business Property nach dem Laden über Manmap tatsächlich ein anderer Wert zugewiesen, wird die Entity dirty. Eine neu erzeugte Entity beginnt ebenfalls als neu und dirty. Nach dem Laden in eine ManMap-Session ist der Ausgangszustand "clean".

Listen benötigen eine zusätzliche Prüfung, weil ihr Inhalt auch über `add`, `remove` oder andere Listenoperationen verändert werden kann, ohne den Property-Setter erneut aufzurufen. Intern wird ein Hash-Wert des Listeninhalts geführt. Beim Abrufen des Dirty-Zustands vergleicht die Entity jede ihrer Listen mit diesem Ausgangswert. Ein hinzugefügtes, entferntes oder ausgetauschtes Element macht die Entity damit ebenfalls dirty; eine reine Umsortierung wird von dieser inhaltsbezogenen Prüfung nicht als Änderung behandelt.

Read-only und Checkout werden durch die Repository-Query festgelegt:

- Eine read-only geladene Entity ist in die Session integriert, darf aber nicht über ihre Business-Property-Setter verändert werden; ein Änderungsversuch führt zu `OFXIllegalAccessException`.
- Eine ausgecheckte Entity ist read/write und nimmt am Dirty-Tracking teil. Sie ist die richtige Form für einen Ablauf, der Änderungen später per Check-in speichern soll.
- Innerhalb derselben Session gilt die Identity Map. Eine bereits integrierte Entity wird nicht als zweite Instanz materialisiert; ein erneuter Checkout derselben Identität wird abgelehnt.

Value Objects besitzen dagegen keinen eigenen Entity-Dirty- oder Read-only-Zustand. Sie werden fachlich unveränderlich verwendet: Eine Änderung erzeugt ein neues Value Object, beispielsweise über einen Konstruktor oder eine `with...`-Methode, und weist dieses anschließend der Entity-Property zu. Dadurch wird die besitzende Entity zuverlässig dirty, und `equals` sowie `hashCode` bleiben stabil.

Der Session-weite Read-only- und Dirty-Zustand wird im Abschnitt [Session und Unit of Work](#session-und-unit-of-work) beschrieben.

## Teil II – Services und Domänenlogik

### Service-Komponenten

Ein `Service` (`Service`) ist eine von der Laufzeit verwaltete Komponente. Services werden über die ObjectFlow-Konfiguration instanziiert und innerhalb einer Anwendung daher nur einmal erzeugt. Sie sind zustandslos zu implementieren: Aufrufübergreifender sowie benutzer- oder sessionbezogener Zustand darf nicht in Feldern eines Services gespeichert werden.

Services bündeln vor allem:

- fachliche Operationen über mehrere Objekte,
- Zustandsübergänge und dazugehörige Prüfungen,
- wiederverwendbare Berechnungen,
- die Koordination mehrerer Repositories oder anderer Services,
- Logik, die sowohl aus UI-Commands als auch aus Jobs und Tests benötigt wird.

Für die Platzierung fachlicher Logik stehen vier Ebenen zur Verfügung. Nur zwei davon, allgemeiner Domänenservice und Anwendungsfallservice, werden technisch mit demselben ObjectFlow-Sprachkonzept `Service` modelliert. ObjectFlow besitzt keine getrennten Service-Untertypen für diese beiden Aufgaben; ihre Unterscheidung ergibt sich aus Verantwortung, Schnittstelle und Benennung. Datenstrukturmethoden und Commands sind dagegen eigene Modellierungsorte:

- **Datenstrukturmethode** – technisch eine BaseLanguage-Methode in einer Entity, einem Value Object oder DTO: allgemeines Verhalten eines einzelnen fachlichen Objekts oder Werts, ohne Infrastrukturzugriff.
- **Allgemeiner Domänenservice** – technisch ein `Service`: wiederverwendbare Geschäftslogik, die keinem einzelnen Objekt natürlich zugeordnet werden kann oder mehrere Objekte verbindet.
- **Anwendungsfallservice** – ebenfalls technisch ein `Service`: spezifischere Orchestrierung für eine fachliche Fähigkeit, die von mehreren Einstiegspunkten wie UI, Batch und Tests genutzt werden kann. Er darf Repositories und andere Komponenten koordinieren, enthält aber keine Page-Navigation.
- **Command** – technisch ein `Command`: konkreter Ablauf mit Parametern, Pages, Conclusions und Session-Grenze. Er ruft Datenstrukturmethoden und Services auf, dupliziert deren Regeln aber nicht.

Eine grundsätzlich gültige Domänenregel liegt damit in einer Entity, einem Value Object oder einem allgemeinen Domänenservice. Eine Prüfung, die zu einer Service-Operation gehört und in allen Aufrufkontexten gelten soll, kann als Precondition der Service Method modelliert werden. Eine rein use-case- oder interaktionsbezogene Prüfung gehört hingegen in den Anwendungsfallservice beziehungsweise Command und seine Page Conclusions.

### Service Methods

Eine Service Method (`ServiceInstanceMethodDeclaration`) besitzt Parameter, Rückgabetyp, Body und optional Preconditions. Zwei Methodenoptionen verändern ihre technische Verwendung:

| Name | Konzeptname | Bedeutung |
| --- | --- | --- |
| `API_METHOD` | `SimdApiMethod` | Kennzeichnet eine für die API-Integration vorgesehene Service Method |
| `TO_SESSION_OPS` | `SimdToSessionOps` | Der Aufruf wird im passenden Session-Kontext nicht sofort ausgeführt, sondern als Session Operation registriert |

Eine Methode mit `TO_SESSION_OPS` darf keine Preconditions besitzen. Eine solche Precondition würde erst während der Transaktionsausführung geprüft; die Laufzeit lehnt diese Kombination mit einer RuntimeException ab.

### Komponenten mit `#` aufrufen

Service- und Repository-Methoden werden mit dem Komponentenaufruf `#` (`OperationCall`) aufgerufen. Er ist nicht nur eine kürzere Schreibweise für einen Java-Methodenaufruf: Er kennt die konfigurierte Komponenteninstanz, die aktuelle Session und die Methodenart. Dadurch kann die Laufzeit entscheiden, ob der Aufruf sofort erfolgt oder als Session Operation registriert wird.

| Ziel des `OperationCall` | Typisches Verhalten |
| --- | --- |
| Normale Service Method | Wird unmittelbar ausgeführt |
| Service Method mit `TO_SESSION_OPS` | Wird im transaktionsfähigen Abschlusskontext als Session Operation registriert |
| ManMap-`READONLY`-Methode | Wird unmittelbar in der aktuellen Session ausgeführt |
| ManMap-`CHECKOUT`-Methode | Wird unmittelbar ausgeführt und integriert geladene Entities veränderbar in die Session |
| ManMap-`CHECKIN`- oder `DELETE`-Methode in `FINAL_OK` | Wird automatisch als Session Operation registriert |
| Dafür vorgesehener Aufruf in `FINAL_CANCEL` | Wird als Cancel-/Marker- beziehungsweise Journal-Operation in dem dafür vorgesehenen Cancel-Transaktionskontext behandelt |

Für normale fachliche Aufrufe ist `OperationCall` zu verwenden. Ein direkter Java-Aufruf ist nicht möglich. Er würde die Komponenten-, Session- und Transaktionssemantik umgehen.

### Explizite Session Operations

Mit `session operation add` (`SessionOperationAdd`) kann ein `OperationCall` ausdrücklich auf dem Operation Stack der aktuellen Session registriert werden. Der Aufruf wird dabei noch nicht ausgeführt.

Das hat zwei wichtige Konsequenzen:

1. Ein Rückgabewert oder eine durch den späteren Aufruf vorgenommene Änderung ist direkt nach `session operation add` noch nicht verfügbar.
2. Wird beispielsweise beim späteren Insert eine Entity-ID vergeben, kann diese ID nicht unmittelbar nach der Registrierung ausgegeben oder verwendet werden.

Service Methods mit `TO_SESSION_OPS` und passende ManMap-`CHECKIN`-/`DELETE`-Methoden übernehmen diese Registrierung automatisch, wenn sie in dem dafür vorgesehenen Kontext per `OperationCall` aufgerufen werden. Die zwei oben genannten Konsequenzen gelten dann ebenfalls.

### Preconditions, Validation, Guards und Exceptions

ObjectFlow unterscheidet fachlich beziehungsweise für den Benutzer behandelbare Probleme von unerwarteten Systemzuständen.

| Mechanismus | Zweck | Wirkung im Command-Ablauf |
| --- | --- | --- |
| Precondition (`Precondition`) | Verständliche, grundsätzlich korrigierbare Voraussetzung | Stoppt außerhalb einer `validation` den aktuellen Programmfluss; die Meldung wird in der UI angezeigt |
| `validation` (`ValidationStatement`) | Mehrere Voraussetzungen gemeinsam prüfen | Führt die enthaltenen Prüfungen aus und sammelt alle verletzten Preconditions in einem Problembericht, der dann ebenfalls in der UI angezeigt wird. |
| `guard` (`Guard`) | Unerwarteten beziehungsweise nicht durch den Benutzer korrigierbaren Zustand absichern | Beendet den Command in `FINAL_CANCEL` (Falls GRAPH_EDIT auch Parent GRAPH_OWNER); Benutzer erhalten eine neutrale Systemmeldung, Entwickler Diagnoseinformationen und Stacktrace |
| Exception | Technischer Ausnahmefall | Beendet den betroffenen Command in `FINAL_CANCEL` |

Bei einer Precondition beschreibt `condition` den gültigen Zustand: Nur wenn der Ausdruck `true` ergibt, läuft die Ausführung weiter. Bei `false` erzeugt die Precondition ein fachliches Problem. Für einen statischen benutzergerichteten Problemtext wird die ObjectFlow-Textprojektion `StringFormatString` verwendet, beispielsweise 'Hallo Fehler-Text', und kein BaseLanguage-String in doppelten Anführungszeichen. Platzhalter und Argumente können mit `%` ergänzt werden.

Die vollständige Projektionsform lässt sich schematisch so lesen:

```objectflow
precondition <condition> : <options> 'Hallo Fehler-Text' / <exception>
  'propertyName' : <value>;
```

Alle Teile außer `condition` und Problemtext sind optional. Mehrere Optionen werden durch Kommas getrennt. `CheckOptionRef` verweist auf Werte von `IOFXProblem.Opt`:

| Option | Wirkung |
| --- | --- |
| `WARNING_HINT` | Behandelt das Problem nur als Warnhinweis. Der Programmfluss wird nicht abgebrochen; der Text erscheint orange statt rot. |
| `PRIO_INFO` | Meldet beziehungsweise protokolliert das Problem mit Priorität Info. |
| `PRIO_ERROR` | Meldet beziehungsweise protokolliert das Problem mit Priorität Error. |
| `PRIO_FATAL` | Meldet beziehungsweise protokolliert das Problem mit Priorität Fatal. |

Nach dem Schrägstrich kann eine vorhandene Exception als Ausdruck weitergereicht werden. Sie bleibt dadurch als technische Ursache und mit ihrem Stacktrace am fachlichen Problem erhalten. Die anschließenden optionalen Schlüssel/Wert-Paare sind `LogStatementProperty`-Einträge. Sie ergänzen den Problembericht und die Diagnoseprotokollierung um strukturierte Werte, ohne den Benutzertext mit technischen Details zu überladen.

Wird eine Precondition während der Bearbeitung einer bereits angezeigten Page verletzt, wird nur die gerade ausgeführte Aktion unterbrochen. Die aktuelle Page und ihr `Page Pane` bleiben sichtbar. Der Benutzer kann seine Eingaben korrigieren, eine andere Page Conclusion wählen oder einen in den Menüs angebotenen Command zur Korrektur starten. Dasselbe gilt für einen `validation`-Block, nachdem alle enthaltenen Probleme gesammelt und angezeigt wurden.

Eine Precondition im `command init` wirkt früher: Sie verhindert, dass der Command seine erste Page erreicht. Die Meldung wird im UI-Kontext des Aufrufers angezeigt und dessen Oberfläche bleibt bestehen. Eine nicht warnende Precondition im Page Init ist dagegen problematisch, weil sie den Aufbau beziehungsweise die erneute Initialisierung der Page unterbricht. In Page Init sollen deshalb nur `WARNING_HINT`-Preconditions verwendet werden; notwendige abbrechende Prüfungen gehören in `command init` oder in eine Page Conclusion. Wird eine Precondition mittelbar in einem aufgerufenen Service ausgelöst, gilt die Wirkung des jeweiligen Aufruforts. Service-Preconditions müssen daher für alle möglichen Command- und Page-Abläufe geeignet sein.

Eine Precondition kann zusätzlich einen Command als Korrekturaktion anbieten. Nach einer fehlgeschlagenen Prüfung kann der Benutzer dadurch über eine Schaltfläche direkt eine Korrektur starten.

Ein Guard in einem `GRAPH_EDIT_CMD` besitzt ein besonderes Eskalationsverhalten: Er beendet nicht nur den Child-Command, sondern auch den zugehörigen Session Owner. Für den Endanwender erscheint sinngemäß die Meldung „Das Kommando konnte am System nicht ausgeführt werden“. Die technischen Details bleiben für Entwickler und Betrieb sichtbar. Eine normale Exception im `GRAPH_EDIT_CMD` besitzt dieses besondere Eskalationsverhalten nicht.

Ein häufiges Muster für ändernde Domänenlogik lautet:

1. Benötigte Fakten und Konfiguration laden.
2. Alle fachlichen Voraussetzungen in einem `validation`-Block prüfen.
3. Erst nach erfolgreicher Validation den fachlichen Graphen verändern.

Prüfungen und Änderungen sollen nicht abwechselnd ausgeführt werden. Schlägt eine spätere Prüfung fehl, nachdem frühere Anweisungen den Graphen bereits verändert haben, bleibt ein teilweise geänderter Zustand zurück. Welche Änderungen bereits erfolgt sind, ist dann nur schwer zuverlässig festzustellen und eine Korrektur wird unnötig kompliziert. Deshalb werden zuerst alle für die Änderung benötigten Voraussetzungen geprüft. Erst wenn dieser Prüfblock vollständig erfolgreich war, folgt die möglichst geradlinige Änderung des Graphen; in diesem Abschnitt sollen keine erwartbaren fachlichen Fehler mehr auftreten.

### Formatieren von Zeichenketten

Der formatierte ObjectFlow-String (`StringFormatString`) verbindet einen Formattext mit typisierten Werten. Er wird vor allem für Meldungen, Titel, Beschreibungen und Logging verwendet. Die Laufzeit `OFXStringFormatter2` ergänzt die üblichen Java-Formatierungen um fachliche Formate für Dezimalzahlen, Status sowie Datum und Uhrzeit.

| Platzhalter | Erwarteter Wert | Standarddarstellung beziehungsweise Bedeutung |
| --- | --- | --- |
| `%s` | beliebiger Wert beziehungsweise `string` | Zeichenkettendarstellung |
| `%d` | ganzzahliger Wert | dezimale Ganzzahl |
| `%f` | Gleitkomma- oder Dezimalwert | Java-Dezimalformat; Breite und Genauigkeit können angegeben werden |
| `%c` | Zeichen | einzelnes Zeichen |
| `%o` | ganzzahliger Wert | Oktaldarstellung |
| `%x` | ganzzahliger Wert | Hexadezimaldarstellung |
| `%bd` | `BigDecimal` | lokalisiertes ObjectFlow-Dezimalformat, standardmäßig `#,##0.00` |
| `%st` | Statuselement | Langbeschreibung des Status |
| `%sts` | Statuselement | Kurzbeschreibung des Status |
| `%stdb` | Statuselement | technischer Persistenzwert des Status |
| `%dt` | `DateTime` oder kompatibler Joda-Time-Wert | Datum und Uhrzeit, standardmäßig `dd.MM.yyyy HH:mm:ss` |
| `%ld` | `LocalDate`, `DateTime` oder kompatibler Joda-Time-Wert | Datum, standardmäßig `dd.MM.yy` |
| `%sld` | `LocalDate`, `DateTime` oder kompatibler Joda-Time-Wert | kurzes Datum, standardmäßig `dd.MMM` |
| `%tdt` | `LocalDate`, `DateTime` oder kompatibler Joda-Time-Wert | Uhrzeit, standardmäßig `HH:mm` |
| `%n` | kein Argument | Zeilenumbruch |
| `%%` | kein Argument | Prozentzeichen |

Für die Standardkonvertierungen und `%bd` unterstützt die Laufzeit auch Formatflags, Breite und Genauigkeit. Die konfigurierten Standardmuster können in der Laufzeitkonfiguration überschrieben werden. Ein nicht zum Platzhalter passender Typ führt zu einer Exception; `null` wird als `#NULL?` sichtbar gemacht. Dadurch fallen unbeabsichtigt fehlende Werte auf. Soll ein fehlender Wert dagegen fachlich leer oder mit einer Ersatzbeschriftung erscheinen, muss dies vor der Formatierung ausdrücklich entschieden werden.

### Literale für Datum, Zeitpunkt und Dezimalzahl

ObjectFlow ergänzt BaseLanguage um fachlich geeignete Literale. Sie vermeiden technische Konstruktoraufrufe und halten im Modell sichtbar, ob ein fester Wert oder die Serverzeit gemeint ist.

| Projektion | Konzeptname | Typ und Semantik |
| --- | --- | --- |
| `31.12.2026` | `DateLiteral` | Erzeugt ein festes `org.joda.time.LocalDate` aus Tag, Monat und Jahr. |
| `new_LocalDateFromServer()` | `DateLiteral` | Ermittelt das aktuelle Datum über den von der Laufzeit bereitgestellten Server-Zeitkontext. |
| `31.12.2026 14:30:0` | `DateTimeLiteral` | Erzeugt einen festen `org.joda.time.DateTime` aus Datum, Stunde, Minute und Sekunde. |
| `new_DateTimeFromServer()` | `DateTimeLiteral` | Ermittelt Datum und Uhrzeit über den Server-Zeitkontext. |
| `13.44bd` | `DezimalLiteral` | Erzeugt ein `java.math.BigDecimal`; das Suffix `bd` verhindert die ungenaue Gleitkomma-Semantik von `double`. |

Serverdatum und Serverzeitpunkt sind für fachliche Regeln den lokalen Uhren eines Clients immer vorzuziehen. Sie werden erst zur Laufzeit ausgewertet und können dadurch in einer Testkonfiguration zentral kontrolliert werden. Feste Literale eignen sich für fachliche Konstanten und Testdaten. Für Geld und andere exakte Dezimalwerte ist das `bd`-Literal zu verwenden; eine vorausgehende Berechnung mit `double` wird durch eine spätere Umwandlung in `BigDecimal` nicht nachträglich exakt. Auf java Double und Float ist stets zu verzichten!

### UI-Metadaten einer Property mit `#Meta` steuern

Mit `#Meta` (`BPMetaReference`) greift ObjectFlow nicht auf den fachlichen Wert einer Business Property zu, sondern auf ihre veränderbaren Laufzeitmetadaten. Ein Command kann damit die an diese Property gebundene DataUX-Darstellung situationsabhängig steuern, ohne dem statischen Aufbau einer `Page Pane` zu widersprechen.

Beispielsweise kann ein Rechnungsablauf folgende Laufzeitmetadaten setzen:

```text
rechnung.rabatt#Meta.setEnabled(false);
rechnung.zahlungsziel#Meta.setOptional(true);
rechnung.rechnungsdatum#Meta.requestFocus();
rechnung.status#Meta.setElements(Rechnungsstatus.Entwurf, Rechnungsstatus.Freigegeben);
rechnung.kunde#Meta.setScope(buchbareKunden);
```

Damit lassen sich für die konkrete Objekt- und Property-Instanz insbesondere Eingabefähigkeit, Optionalität, Fokus, auswählbare Statuselemente und der Scope einer Entity-Auswahl beeinflussen. Der fachliche Property-Wert bleibt dabei unverändert. `#Meta` eignet sich für dynamische UI-Regeln eines Ablaufs; dauerhaft geltende Beschriftungen, Anordnungen werden weiterhin in Business-Property-Metadaten der Deklaration beziehungsweise DataUX modelliert. Fachliche Gültigkeitsregeln müssen zusätzlich als Preconditions oder Validierung bestehen und dürfen nicht allein von einer deaktivierten Eingabe abhängen!

Ein nützliches Zusammenspiel ergibt sich bei einer feldbezogenen fachlichen Prüfung. Enthält beispielsweise der Empfängername einer Rechnung nicht erlaubte Zeichen, wird zuerst der Fokus auf die betroffene Property angefordert und danach die Precondition ausgelöst:

```objectflow
if (!rechnung.empfaengerName.matches("[A-Za-z0-9 .-]+")) {
  rechnung.empfaengerName#Meta.requestFocus();
  precondition false : 'Der Empfängername enthält nicht erlaubte Zeichen.';
}
```

Die Meldung erscheint typischerweise im allgemeinen Meldungsbereich oberhalb der Page und nicht unmittelbar am Feld. Durch `requestFocus()` steht der Cursor nach der Meldung dennoch an der richtigen Eingabestelle. Die Reihenfolge ist wesentlich: Wird die Precondition zuerst ausgelöst, erreicht der unterbrochene Programmfluss die Fokusanforderung nicht mehr.


## Teil III – Commands und Anwendungsabläufe

Ein `Command` (`Command`) modelliert einen ausführbaren Anwendungsfall oder einen abgegrenzten Teil einer Benutzerinteraktion. Er verbindet Eingaben, lokalen Ablaufzustand, fachliche Prüfungen, Pages und den erfolgreichen oder fehlerhaften Abschluss mit einer klaren Session-Grenze. Ein Command ist damit weder bloß eine UI-Aktion noch nur eine Methode: Er beschreibt den gesamten kontrollierten Ablauf zwischen Aufruf und Termination.

Bevor eine Command-Aktion gestartet werden kann, müssen ihre Parameter beziehungsweise Default-Selektionen verfügbar sein, alle Ausdrücke unter `generally enabled` `true` liefern und eine passende Command-Berechtigung erfüllt sein. Die Berechtigungen heißen konkret `CAN_OPEN_RO` für lesenden und `CAN_OPEN_RW` für ändernden Zugriff und werden jeweils mit einer Rolle verbunden. Eine Rollenprüfung kann zusätzlich Teil von `generally enabled` sein, soll die deklarierte Command-Berechtigung aber nicht ersetzen.

### Grundablauf eines Commands

Der reguläre Ablauf folgt einer festen Reihenfolge:

1. Der Aufrufer übergibt Parameter; Default-Ausdrücke wie `getSelected()` werden aus dem Aufrufkontext aufgelöst.
2. Lokale Variablen bilden den internen Zustand der Command-Instanz.
3. `command init` lädt oder erzeugt die benötigten Daten und kann den Start mit einer Precondition verhindern.
4. Nach erfolgreichem `command init` wird der Window Title berechnet.
5. Ohne explizite Abzweigung wird die erste deklarierte Page initialisiert und angezeigt. `page <Name>` kann stattdessen gezielt eine andere Page wählen; `done` überspringt die Pages und wechselt unmittelbar in `FINAL_OK`.
6. Auf einer Page führt der Benutzer Menüs oder Page Conclusions aus. Eine Conclusion kann auf derselben Page bleiben, zu einer anderen Page wechseln oder mit `done` den erfolgreichen Abschluss auslösen.
7. `FINAL_OK_CONCLUSION` führt den Erfolgsabschluss aus. Guards, Exceptions und technische Fehler führen nach `FINAL_CANCEL_CONCLUSION`; ein bewusster Benutzerabbruch führt nach `FINAL_USER_CANCEL`.

Typische Varianten lassen sich damit einheitlich lesen:

| Variante | Kontrollfluss |
| --- | --- |
| Eine Page | `command init` → Page Init → `Page Pane` → Conclusion mit `done` → `FINAL_OK` |
| Mehrere Pages | `command init` → erste Page → Conclusion mit `page ZweitePage` → deren Page Init → Conclusion mit `done` |
| Precondition in `command init` | Prüfung schlägt fehl → keine Page wird geöffnet → Meldung erscheint im aufrufenden UI |
| Precondition in einer Conclusion | Standardmäßig werden Editorwerte übernommen → Conclusion startet → Prüfung schlägt fehl → aktuelle Page bleibt zur Korrektur sichtbar |
| `done` in `command init` | Ein interaktionsloser oder bereits entscheidbarer Pfad überspringt alle Pages und führt `FINAL_OK` aus; ein anderer Zweig kann mit `page <Name>` dynamisch eine der vorhandenen Pages wählen |


### Die vier Command-Typen

Der Command-Typ bestimmt vor allem Eigentum und Abschluss der Session.

| Sichtbarer Typ | Session | Abschluss und Persistenz | Typischer Einsatz |
| --- | --- | --- | --- |
| `SEARCH_CMD` | Startet eine eigene Session | `FINAL_OK` beendet die Session ohne Commit; registrierte Session Operations werden nicht ausgeführt | Suche, Anzeige, Filterung und Read-only-Auswertung |
| `GRAPH_OWNER_CMD` | Startet eine eigene Session und besitzt den bearbeiteten Graphen | Bei `FINAL_OK` werden Session Operations in einer Transaktion ausgeführt und committed | Bearbeitung eines vollständigen fachlichen Graphen |
| `GRAPH_EDIT_CMD` | Übernimmt die Session seines Performers | Besitzt keinen eigenen Commit; erfolgreicher Abschluss kehrt zum Owner zurück | Teilbearbeitung und Benutzerinteraktion innerhalb eines vorhandenen Graphen |
| `GRAPH_OWNER_CMD_MODAL` | Wie `GRAPH_OWNER_CMD`: eigene Session | Wie `GRAPH_OWNER_CMD`: eigener Commit bei `FINAL_OK` | Eigenständige Bearbeitung in einer modalen UI |

`GRAPH_OWNER_CMD_MODAL` unterscheidet sich fachlich und transaktional nicht vom normalen Graph Owner. Nur die Oberfläche ist modal.

Ein `GRAPH_EDIT_CMD` kann technisch Session Operations registrieren. Diese werden bei einem Abbruch des Child-Commands jedoch nicht wieder vom Operation Stack entfernt. In der beobachteten Praxis sollen `GRAPH_EDIT_CMD`s deshalb keine Session Operations registrieren; der Session Owner übernimmt deren Registrierung.

### Aufbau eines Commands

Ein Command kann folgende Bestandteile enthalten:

| Bestandteil | Technische Form | Aufgabe | Typischer Inhalt |
| --- | --- | --- | --- |
| Parameter und Defaults | Typisierte Parameterdeklaration mit optionalem Ausdruck | Eingaben des Aufrufs festlegen | Schlüssel, ausgewählte Entity oder DTO, Filterwert; Default über `getSelected()` oder Konstante |
| `generally enabled` | Liste boolescher Ausdrücke, logisch UND-verknüpft | Sichtbare Command-Aktion fachlich aktivieren oder deaktivieren | Zulässiger Status, vorhandene Selektion, passende Betriebsart |
| Permissions | `CAN_OPEN_RO`- oder `CAN_OPEN_RW`-Eintrag mit Rolle | Lesenden beziehungsweise ändernden Zugriff erlauben | Beobachterrolle für Anzeige, Sachbearbeiterrolle für Änderung |
| Preconditions | Liste von `Precondition`-Knoten | Verständliche Voraussetzungen vor dem Start prüfen | Vollständige Parameter, fachlich erlaubter Ausgangszustand |
| Lokale Variablen | Typisierte Variablendeklaration | Zustand einer Command-Instanz halten | Geladener Graph, Filter-DTO, Ergebnisliste, Ablaufkennzeichen |
| Command Settings | Deklarative Einstellungen und Ausdrücke | Darstellung und Laufzeitverhalten konfigurieren | Label, Icon, Hotkey, Farbe, Revert-Objekte, Locks, Optionen |
| `command init` | Funktion ohne Rückgabewert | Ablauf vorbereiten und erste Kontrollentscheidung treffen | Checkout oder Suche, DTO-Aufbau, Precondition, `page …` oder `done` |
| Pages | `PageCrtl`-Knoten | Interaktionsschritte definieren | Page Init mit Rückgabewert, Bindung, Titel, Scopes, UI-Auswahl und Conclusions |
| `FINAL OK_CONCLUSION` | Funktion ohne Rückgabewert plus Successors und Selektionen | Erfolgreichen Abschluss vorbereiten | Check-in-Operationen registrieren, Ergebnisobjekte pushen |
| `FINAL CANCEL_CONCLUSION` | Funktion mit Problembericht plus Cancel-Operationen | Fachlichen oder technischen Abbruch behandeln | Diagnose, Fehlerstatus oder Journal in privater Cancel-Transaktion |
| `FINAL_USER_CANCEL` | Deklarierter Benutzerabbruch | Bewusstes Schließen oder Zurückgehen behandeln | Revert der dafür angegebenen Objekte |

### Parameter, Defaults und Selektion

Command-Parameter können beim Aufruf explizit gesetzt oder über Default-Ausdrücke belegt werden. Häufig verwendete Ausdrücke sind `getSelected()` (`SelectedObject`) und `getSelectedObjects()` (`SelectedList`). Sie beziehen sich auf die aktuelle Selektion des Aufrufkontexts. Eine Selektion kann auch Subtypen berücksichtigen, dann muss das "+ derived" aktiviert sein (Property `andDerived`).

Die Verfügbarkeit eines Commands hängt sowohl von passenden Argumenten und Selektionen als auch von `generally enabled`, Permissions und gegebenenfalls UI-spezifischen Bedingungen ab. Ein Default ersetzt keine Prüfung auf einen fachlich zulässigen Aufruf.

Ein Command zum Bearbeiten einer Rechnungsposition könnte beispielsweise zwei obligatorische Selektionen, einen zulässigen Rechnungsstatus und ändernden Zugriff für die Rolle `Sachbearbeiter` verlangen:

```objectflow
command 'Rechnungsposition bearbeiten'
command type: GRAPH_EDIT_CMD

command parameter and defaults:
Rechnung rechnung = getSelected(Rechnung)
Rechnungsposition position = getSelected(Rechnungsposition)

generally enabled:
rechnung.status of Entwurf, InBearbeitung

command permissions:
CAN_OPEN_RW role Sachbearbeiter()
```

Fehlt entweder die selektierte Rechnung oder die selektierte Rechnungsposition, ist der Command bereits wegen des nicht auflösbaren obligatorischen Defaults nicht verfügbar. Sind beide vorhanden, werden zusätzlich alle `generally enabled`-Ausdrücke geprüft. Erst wenn auch der Status passt und der Benutzer die erforderliche Rolle besitzt, kann der Command mit änderndem Zugriff gestartet werden.

### Command Init und Hintergrundinitialisierung

`command init` bereitet Variablen und Daten für den folgenden Ablauf vor. Mit der Option `IN_BACKGROUND` wird ausschließlich dieses `command init` im Hintergrund ausgeführt. Pages und der weitere Interaktionsablauf werden dadurch nicht allgemein zu einem Hintergrundjob.

Preconditions sollen vor fachlichen Änderungen geprüft werden. Im `command init` verhindert eine fehlgeschlagene Precondition den Start des interaktiven Ablaufs und zeigt ihre Meldung im aufrufenden UI. `WARNING_HINT` unterbricht den Ablauf weder hier noch im Page Init. Eine nicht warnende Precondition im Page Init soll vermieden werden, weil sie die Initialisierung der anzuzeigenden Page abbricht. Diese Regeln gelten ebenso, wenn die Precondition in einem vom jeweiligen Abschnitt aufgerufenen Service liegt.

Der Window Title wird nach `command init` berechnet. Dadurch dürfen sein Ausdruck und seine Formatargumente auf den dort aufgebauten lokalen Zustand zugreifen. Die Command-Property `newWindowTitleType` (`O2WindowTitleType`) bestimmt, wie der Text mit einem bereits vorhandenen Fenstertitel kombiniert wird:

| Wert | Projektion | Wirkung |
| --- | --- | --- |
| `ADDON` | `(addon)` | Ergänzt den bestehenden Fenstertitel um den Command-Titel. Dies ist der Standard. |
| `OVERWRITE` | `(overwrite)` | Ersetzt den Fenstertitel durch den Titel des aktuellen Commands. |
| `OVERWRITE_FORCED` | `(overwrite predecessor)` | Erzwingt die Ersetzung auch gegenüber dem vom Vorgänger-Command übernommenen Titel. |

### Pages und Page Conclusions

Eine Page (`PageCrtl`) ist der zentrale interaktive Schritt eines Commands. Sie verbindet das vom Command bereitgestellte Objekt mit einer sichtbaren DataUX-Darstellung und den möglichen Übergängen des Ablaufs. Page und `Page Pane` haben dabei getrennte Verantwortlichkeiten: ObjectFlow beschreibt Daten, Zustand und Kontrollfluss; DataUX beschreibt die sichtbare Darstellung und die Menüs.

| Bestandteil einer Page | Technische Form | Aufgabe |
| --- | --- | --- |
| Bindung | optionale Referenz auf Entity- oder DTO-Typ | Legt den Typ des von Page Init bereitgestellten Root-Objekts fest |
| Page Init | `PageInitConceptFunc`, liefert ein Objekt zurück | Lädt, aktualisiert oder liefert die anzuzeigenden Daten |
| Page Title und Subtitle | optionale Ausdrücke | Beschriften den Inhalt dieser Page nach ihrer Initialisierung |
| Scopes | `PageScopeConceptFunc` | Setzt Page-spezifische Auswahlmengen und andere `#Meta`-Werte |
| Page-Pane-Umschaltung | ein oder mehrere `PagePaneActionProviderLink` | Wählt abhängig von Bedingungen die passende DataUX-Darstellung |
| Termination Handler | null bis viele `PageCmdTermHandler` | Reagiert auf beendete Child- oder andere Commands und übernimmt gepushte Ergebnisse |
| Branching Commands | für die Page angebotene Commands | Stellt mögliche Child-Aktionen bereit; ihre sichtbare Platzierung wird in den Menüs der `Page Pane`s modelliert |
| Page Conclusions | null bis viele `PageConclusion`-Knoten | Bildet die regulären Schaltflächen am unteren Rand der UI und führt den nächsten Ablaufschritt aus |

#### Page Init und Datenbereitstellung

Bei einem `GRAPH_OWNER_CMD` wird der bearbeitete Graph üblicherweise bereits im `command init` ausgecheckt; Page Init liefert dann das vorbereitete Root-Objekt. Bei einem `SEARCH_CMD` lädt Page Init häufig die aktuelle Ergebnisliste anhand eines Filter-DTOs. Das sind bewährte Muster, keine strukturelle Beschränkung der Sprache.

Eine Conclusion kann mit `page <dieselbe Page>` bewusst auf die aktuelle Page zurückwechseln. Dadurch wird Page Init erneut ausgeführt und die Darstellung aktualisiert. So entsteht eine Refresh-Conclusion, ohne den Command neu zu starten. Ein Wechsel mit `page <andere Page>` initialisiert entsprechend den nächsten Interaktionsschritt.

#### Window Title, Page Title und Subtitle

Der Window Title gehört zum gesamten Command-Fenster und wird nach `command init` nach den Regeln von `O2WindowTitleType` gesetzt. Page Title und Subtitle gehören dagegen zu einer einzelnen Page. Ihre Ausdrücke werden nach Page Init berechnet und können daher den gerade geladenen Page-Zustand beschreiben. Ein mehrseitiger Command behält somit seinen Window Title, während Page Title und Subtitle je Interaktionsschritt wechseln können.

#### Scopes und Page-Pane-Umschaltung

Die Scope-Funktion (`PageScopeConceptFunc`) läuft nach Page Init und erneut nach der Termination eines Child-Commands. Sie eignet sich insbesondere dazu, die zulässigen Werte einer Reference- oder Status-Property über `#Meta` an den aktuellen Page-Zustand anzupassen. Sie lädt keine UI-Daten nach; benötigte Objekte müssen bereits durch Command oder Repository bereitgestellt sein.

Eine Page besitzt mindestens einen `PagePaneActionProviderLink`. Ein unbedingter Link wird als `-> : PagePane` projiziert; ein bedingter Link als `<Bedingung> : PagePane`. Damit kann dieselbe fachliche Page beispielsweise für unterschiedliche Geräteklassen oder für Administratoren und reguläre Benutzer verschiedene Oberflächen auswählen. Die Bedingungen sollen sich eindeutig verhalten; ein unbedingter Link kann als Fallback dienen. Die fachliche Logik bleibt trotz unterschiedlicher Darstellung in derselben Page und demselben Command.

#### Termination Handler

Ein `PageCmdTermHandler` wird ausgeführt, wenn während der Page ein weiterer Command beendet wurde. `ChildCmdTerminated` reagiert auf echte Child-Commands; `AnyCmdTerminated` kann auch andere passende Terminationen erfassen. Ein optionaler Classifier filtert nach dem Typ des gepushten Objekts. Je nach Variante erhält die Funktion Informationen darüber, ob der beendete Command erfolgreich war, ob er ein Child war und welches Objekt gepusht wurde.

Der Handler kann anschließend berechnete Werte aktualisieren, ein gepushtes Objekt mit `session merge` in den Parent-Graphen übernehmen oder die Selektion anpassen. Danach werden auch die Page-Scopes neu berechnet. Dieses explizite Verhalten ist besonders zusammen mit `NEWSTYLE_CMD_TERM_HANDLING` wichtig.

#### Page Conclusions

Eine `PageConclusion` besitzt ein Label, eine optionale `enabledWhen`-Bedingung, den Modus `ConclusionSaveType` und eine Funktion ohne Rückgabewert. Ihre Labels erscheinen typischerweise als Schaltflächen am unteren Rand der Page. Zusätzlich steht der Benutzerabbruch über Escape beziehungsweise Zurück zur Verfügung, solange der Command nicht die Option `NO_ESC` trägt.

`ConclusionSaveType` hat die Werte `save` (`SAVE_CONCLUSION`, Standard) und `no_save` (`NOSAVE_CONCLUSION`). `save` übernimmt vor der Conclusion die aktuellen Editorwerte in die gebundenen Objekte. Das soll auch bei nicht editierbaren oder situationsabhängig deaktivierten UI-Elementen der normale Modus bleiben; deaktiviert bedeutet nicht, dass die übrigen Page-Werte verworfen werden sollen. `no_save` ist nur passend, wenn die noch im Editor befindlichen Änderungen für diese Aktion ausdrücklich nicht übernommen werden dürfen.

Innerhalb der Conclusion steuern zwei spezielle Statements den weiteren Ablauf:

- `page <Name>` (`PageCommand`) wechselt auf die angegebene Page und führt deren Page Init aus. Ein Verweis auf die aktuelle Page wirkt als Refresh.
- `done` (`DoneCommand`) beendet den interaktiven Teil erfolgreich und führt `FINAL_OK_CONCLUSION` aus.

Ohne `page` oder `done` bleibt der Command auf der aktuellen Page. Schlägt eine Precondition in der Conclusion fehl, wird deren Funktion an dieser Stelle beendet; die Page bleibt sichtbar und der Benutzer kann anhand der Meldung korrigieren oder eine andere Aktion wählen.


### `FINAL_OK`, `FINAL_CANCEL` und `FINAL_USER_CANCEL`

`FINAL_OK` bezeichnet den erfolgreichen Abschluss eines Commands. Beim Session Owner entsteht daraus folgende Reihenfolge:

```text
FINAL-OK-Funktion
        │
        ▼
Session Operations in Registrierungsreihenfolge
        │
        ▼
gemeinsame Datenbanktransaktion
        │
        ▼
Commit
        │
        ▼
gegebenenfalls geplanter nächster Command
```

Schlägt eine Session Operation fehl, wird die Transaktion nicht committed. Ein `SEARCH_CMD` durchläuft zwar ebenfalls seinen erfolgreichen Command-Abschluss, seine Session wird anschließend aber ausdrücklich nicht committed.

`FINAL_CANCEL` ist ein vom Command beziehungsweise System ausgelöster Abbruch. Guards und Exceptions führen in diesen Abschluss. Registrierte normale Session Operations werden nicht als erfolgreicher Check-in ausgeführt. Für Fehlerstatus, Marker oder Journale stehen gesonderte Cancel-Operationen zur Verfügung, die in einem dafür vorgesehenen privaten Transaktionskontext ausgeführt werden können.

`FINAL_USER_CANCEL` entsteht durch eine bewusste Benutzeraktion, insbesondere Escape, Zurück oder Schließen. Die Command-Option `NO_ESC` deaktiviert den Abbruch über Escape.

### Revert beim Abbruch

Unter `revert on FINAL_ / USER_CANCEL` können Parameter beziehungsweise Variablen angegeben werden, deren Zustand bei einem Abbruch wiederhergestellt werden soll. Beim Command-Start zieht die Laufzeit dafür automatisch eine Kopie.

Bei Listen hängt diese Revert-Kopie von der Veränderbarkeit ihrer Elemente ab: Veränderbare Entity-Elemente werden kopiert; ausschließlich read-only geladene Elemente können als Referenzen wiederverwendet werden.

- Bei `FINAL_CANCEL` und `FINAL_USER_CANCEL` wird der ursprüngliche Zustand wiederhergestellt.
- Wird die Wurzel eines Graphen angegeben, wird der gesamte darunterliegende ObjectFlow-Graph zurückgesetzt.
- Nicht als Revert-Objekt erfasste Änderungen werden nicht allein aufgrund eines Child-Abbruchs automatisch zurückgenommen.
- Session Operations eines abgebrochenen `GRAPH_EDIT_CMD` werden durch Revert nicht aus dem Stack entfernt.

Revert ist damit eine In-Memory-Rücknahme des bearbeiteten ObjectFlow-Graphen und nicht mit einem Datenbank-Rollback gleichzusetzen. Die Datenbanktransaktion für den normalen Check-in beginnt ohnehin erst beim erfolgreichen Abschluss des Session Owners.

### Command-Optionen

| Name | Konzeptname | FQ-Name | Wirkung |
| --- | --- | --- | --- |
| `IN_BACKGROUND` | `CommandBackgroundOption` | `org.modellwerkstatt.objectflow.structure.CommandBackgroundOption` | Führt `command init` im Hintergrund aus |
| `NO_ESC` | `CommandNoEscOption` | `org.modellwerkstatt.objectflow.structure.CommandNoEscOption` | Deaktiviert `FINAL_USER_CANCEL` über Escape |
| `NEWSTYLE_CMD_TERM_HANDLING` | `CommandNoPushNewTermOption` | `org.modellwerkstatt.objectflow.structure.CommandNoPushNewTermOption` | Deaktiviert die alte automatische Übernahme gepushter Objekte; Termination und Merge werden explizit behandelt |
| `URL` | `CommandUrlOption` | `org.modellwerkstatt.objectflow.structure.CommandUrlOption` | Macht einen Command in webfähigen Laufzeiten über einen Pfad und optionale URL-Parameter startbar |

`URL` gilt für Turku- und H2-Laufzeiten. Wird ein URL-fähiger Command direkt aufgerufen, werden die Parameter aus der URL bereitgestellt und müssen nach `command init` in den Command-Kontext gepusht werden. Wird der Command aus einem bestehenden Fenster in einem neuen Browserfenster gestartet, passt die Laufzeit die Browser-URL ebenfalls an.

### Session und Unit of Work

Die ObjectFlow-Session begleitet den Command-Ablauf und hält die geladenen beziehungsweise neu integrierten Objekte. Sie ist längerlebig als die Datenbanktransaktion des abschließenden Check-ins.

```text
Session Owner startet
        │
        ├── Entities read-only laden
        ├── Entities auschecken
        ├── Graph bearbeiten
        ├── GRAPH_EDIT-Commands ausführen
        └── Session Operations registrieren
                    │
                    ▼
                 FINAL_OK
                    │
                    ▼
       kurze Datenbanktransaktion + Commit
```

Das Konzept `session` (`Session`) gibt bei Bedarf direkten Zugriff auf Interna der aktuellen Session. Es ist für Fälle gedacht, die durch die höherwertigen Sprachkonzepte nicht abgedeckt werden. Direkter Session-Zugriff erhöht die Kopplung an die Laufzeit und sollte deshalb gezielt bleiben.

Neu erzeugte Entities müssen Teil der Session werden, bevor Session- und UI-Mechanismen sie als bearbeiteten Graphen behandeln können. Dafür stellt die Session entsprechende Integrationsoperationen bereit.

#### Session-weites Read-only und Dirty

Mit `session.setReadOnly()` kann ein Command seine aktuelle Session ausdrücklich in den Read-only-Modus versetzen. In diesem Modus darf die Laufzeit keine speichernde Transaktion starten; generierte Insert- und Update-Operationen lehnen die Ausführung ebenfalls ab. Das ist insbesondere für Commands sinnvoll, die trotz umfangreicher Navigation und Repository-Zugriffe garantiert keine Daten speichern sollen.

Der Session-Schalter ist von der Read-only-Eigenschaft einzelner Entities zu unterscheiden. `session.setReadOnly()` markiert die Session, setzt aber bereits integrierte Entity-Instanzen nicht nachträglich einzeln auf read-only. Ob deren Setter Änderungen zulassen, hängt weiterhin davon ab, ob sie read-only geladen oder ausgecheckt wurden. Für einen konsistent lesenden Ablauf sollen daher sowohl passende read-only Repository-Methoden als auch – wenn der gesamte Command schreibgeschützt sein soll – der Session-Modus verwendet werden.

`session.isDirty()` beantwortet, ob die Session ungespeicherte Änderungen enthält. Die Prüfung berücksichtigt zunächst einen ausdrücklich gesetzten Session-Dirty-Zustand und durchläuft andernfalls die Key Stores aller in die Session integrierten Entity-Typen. Eine neu integrierte Entity ohne Schlüssel gilt als dirty; bei vorhandenen Entities wird deren Dirty-Zustand abgefragt. Diese Entity-Prüfung bezieht auch nachträgliche Änderungen an Listen ein. Der Aufruf betrachtet damit die gesamte Session und nicht nur das aktuell auf einer Page gebundene Objekt.

```text
session.setReadOnly();
boolean ungespeicherteAenderungen = session.isDirty();
```

`session.isDirty()` eignet sich beispielsweise für Abbruchrückfragen oder zur Entscheidung, ob ein speichernder Abschluss angeboten wird. Da die Prüfung die integrierten Entities bis zum ersten Treffer durchläuft, sollte sie nicht unnötig in engen Schleifen aufgerufen werden.

### Entities in der Session prüfen

`session entities` (`CheckedOutEntities`) liefert für einen Entity-Typ Informationen aus der aktuellen Session. Der Modus (`CheckedOutEntitiesType`) besitzt vier Werte:

| Projektion | Ergebnis |
| --- | --- |
| `(checked out)` | Ausgecheckte Entity-Instanzen des Typs |
| `(keys of checked out)` | Schlüssel der ausgecheckten Entities |
| `(all)` | Alle in der Session vorhandenen Entities des Typs |
| `(keys of all)` | Schlüssel aller Session-Entities des Typs |

Ein wichtiger Einsatz ist die Prüfung, ob eine Entity bereits ausgecheckt wurde. Dadurch lässt sich ein doppelter Checkout vermeiden, der von ManMap abgelehnt wird.

### Command nach dem Commit einplanen

`session queue next command` (`SessionQueueNextCommand`) plant einen Command für die Zeit nach dem erfolgreichen Abschluss des Session Owners. Der geplante Command startet erst, wenn Session Operations und Commit erfolgreich abgeschlossen sind.

- Bei `FINAL_CANCEL` wird er nicht gestartet.
- Bei fehlgeschlagenem Commit wird er nicht gestartet.
- Ohne UI – beispielsweise in Tests oder Jobs – wird die Einplanung ignoriert.

Dieses Konzept eignet sich für einen Folgeablauf, der einen bereits erfolgreich persistierten Zustand benötigt. Da der einzureihende Command und seine Argumente zur Laufzeit gewählt werden können, lassen sich damit auch längere fachliche Prozesse modellieren: Der aktuelle Schritt entscheidet anhand seines Ergebnisses, welcher Command nach dem Commit als nächster beginnt. Diese Entscheidung kann in einem wiederverwendbaren Service gekapselt sein, sofern er innerhalb des aktuellen UI-Command- und Session-Kontexts ausgeführt wird.

Jeder solche Übergang bildet eine klare Sicherungsgrenze: Erst der erfolgreiche Commit des aktuellen Session Owners gibt den nächsten Command frei. Ein mehrstufiger Workflow kann dadurch aus mehreren eigenständigen Commands mit jeweils eigener Benutzerinteraktion und Transaktion bestehen. Der Mechanismus ersetzt jedoch keine allgemeine Job- oder Workflow-Engine: Ohne UI wird die Queue ignoriert, und bei Abbruch oder fehlgeschlagenem Commit findet kein Übergang statt.

### Explizites Command-Termination-Handling und Session Merge

Im alten Termination-Modus übernahm beziehungsweise ersetzte die Laufzeit gepushte Entities in einem `SEARCH_CMD` teilweise automatisch. Die Option `NEWSTYLE_CMD_TERM_HANDLING` deaktiviert diesen Automatismus.

Der Parent reagiert stattdessen in einem Command-Termination-Handler auf das beendete Child:

1. Das Child pusht ein oder mehrere Objekte bei seinem Abschluss.
2. Der Parent erhält diese Objekte im Termination-Handler.
3. `session merge` (`MergeInto`) integriert die relevanten Werte explizit in ein Zielobjekt beziehungsweise eine Zielliste des Parent-Graphen.
4. Falls erforderlich, wird anschließend die Selektion ausdrücklich auf das integrierte Ziel gesetzt.

`MergeInto` kann primitive Werte und Schlüssel übernehmen, Listen elementweise anhand von Schlüsseln abgleichen und ein Ziel in der Session finden beziehungsweise integrieren. Der konkrete Merge-Modus bestimmt, ob Session- und Read-only-Zustand berücksichtigt werden. Entfernte Listenelemente werden nach den historischen Beschreibungen nicht automatisch aus jeder Zielliste gelöscht; dieses Detail ist bei neuen Verwendungen gegen die aktuelle Projektion und Tests zu prüfen.

Referenzbeispiele für die unterstützten Merge-Varianten liegen in der ObjectFlow-Testsuite `org.modellwerkstatt.objectflow.tests.ObjectFlowInfra.SessionAndMerge`. Anwendungsprojekte können zum Verständnis untersucht werden, sind aber keine zitierbare Spezifikation.

### Successor-Commands und weitere Ablaufmuster

Ein Command kann Successor-Commands deklarieren. Sie modellieren einen fachlichen Folgeablauf, der aus dem Abschluss des aktuellen Commands hervorgeht. Davon zu unterscheiden ist `session queue next command`: Dieses Konzept plant gezielt einen Command nach erfolgreichem Commit des Session Owners.

In bestehenden und historischen Modellen treten außerdem folgende Muster auf:

- Suche → Graph Owner → mehrere Graph Edits,
- Erzeugen eines Folgedokuments und anschließende Bearbeitung,
- Compound Actions, die mehrere Commands anhand ihrer Conclusions verketten,
- mehrfache Ausführung eines Commands auf selektierten Listenelementen,
- erneute Validierung eines Parent-Graphen nach dem Ende eines Child-Commands.

Diese Muster sind keine zusätzlichen Command-Typen. Ihre genaue Eignung hängt von Session-Grenze, Revert, Termination-Handling und Ziel-Laufzeit ab.


## Teil IV – Testing mit ObjectFlow

### `OFX Test Suit`

Eine `OFX Test Suit` (`OFXTestSuit`) ist eine eigenständig ausführbare Testsuite. Sie referenziert eine `OFX Config`, stellt konfigurierte Komponenten bereit und kann Start-/Ende-Logik sowie mehrere `Simple Test`s enthalten.

| Bestandteil | Aufgabe |
| --- | --- |
| Configuration | Wählt Komponenten und Laufzeitkonfiguration für den Test |
| Configured Components | Macht explizit benötigte Komponenten im Testkontext verfügbar |
| `on startup` | Wird unmittelbar vor dem ersten ausgeführten Test aufgerufen |
| `on shutdown` | Wird unmittelbar nach dem letzten ausgeführten Test aufgerufen |
| `Simple Test` | Testmethode mit eigener ObjectFlow-Session |
| Parameter und Variablen | Gemeinsamer Testsuite-Kontext |

Jeder `Simple Test` (`OFXTestMethod`) erhält eine eigene Session. Diese Session wird am Testende nicht committed. Dadurch lassen sich Services, Repositories und Command-Abläufe mit realistischem Session-Verhalten prüfen, ohne den normalen Command-Commit auszuführen.

### Testoptionen

| Name | Konzeptname | Bedeutung |
| --- | --- | --- |
| `PATH` | `OFXTestPathOption` | Deklariert ein vom Test verwendetes Verzeichnis |
| `DEBUG_TEST` | `OFXTestSuitDebugOption` | Aktiviert zusätzliche Debugausgabe für einen ausgewählten Test |
| `DEFAULT_DATETIME` | `OFXTestSuitDefaultDateTimeOption` | Fixiert Standarddatum und -zeit für reproduzierbare Tests |
| `DEPENDENT_TEST` | `OFXTestSuitDependentOption` | Kennzeichnet einen Test als abhängig und nicht eigenständig auszuführen |
| `INCLUDE_SUIT` | `OFXTestSuitIncludeSuit` | Bindet eine weitere Testsuite einschließlich Start-/Ende-Logik ein |
| `DONT_EXEC` | `OFXTestSuitNoExecOption` | Schließt einen ausgewählten Test von der normalen Ausführung aus |

### Commands ohne UI ausführen

`run command` (`OFXRunCmd`) führt einen Command ohne Benutzeroberfläche aus. Das ist zentral, um nicht nur einzelne Methoden, sondern einen vollständigen Anwendungsablauf zu testen.

Ein `run command` kann:

- den Command mit Argumenten starten,
- für erwartete Pages jeweils eine Conclusion angeben,
- vor einer Conclusion Testlogik ausführen,
- optionale Pages kennzeichnen,
- Successor-Commands mit eigenen Page-Antworten behandeln,
- auf die gebundenen Page-Objekte zugreifen.

Die Testbeschreibung simuliert damit die Entscheidungen, die sonst ein Benutzer über die UI trifft. Die DataUX-Darstellung wird nicht benötigt. UI-abhängige Mechanismen wie `session queue next command` werden bei einer Ausführung ohne UI ignoriert.

### Typische Testebenen

ObjectFlow unterstützt insbesondere folgende Testformen:

1. **Datenstruktur und Value Object:** Konstruktion, Berechnung, Gleichheit und Zustandsübergänge prüfen.
2. **Service:** Domänenoperationen und ihre Preconditions mit konfigurierten Komponenten ausführen.
3. **Repository und Session:** Laden, Checkout, Identity-Map und explizite Session-Integration prüfen.
4. **Command:** Mit `run command` Initialisierung, Pages, Conclusions, Revert, Successors und finalen Abschluss testen.
5. **Konfiguration:** Prüfen, ob die für den Ablauf benötigten Komponenten korrekt verdrahtet sind.

Da Tests nicht committen, sollen persistenzwirksame Erwartungen gezielt über Testdatenaufbau, gelesenen Zustand und die registrierten beziehungsweise aufgerufenen Operationen geprüft werden.

#### Repositories im Test ersetzen

Ein ManMap-`Repository` kann über seine `superclass`-Rolle ein anderes Repository erweitern. Damit lässt sich zu einem produktiven Repository eine Testimplementierung modellieren, die einzelne Methoden überschreibt und beispielsweise kontrollierte Fake-Daten liefert. Wird in der von der Testsuite verwendeten `OFX Config` diese Testimplementierung anstelle der produktiven Implementierung instanziert, werden `OperationCall`s auf die passende konfigurierte Testkomponente aufgelöst.

Für dasselbe Basis-Repository können mehrere Test-Repositories existieren, etwa für einen leeren Datenbestand, einen typischen Erfolgsfall oder einen simulierten Fehler. Die jeweilige Testkonfiguration wählt genau die benötigte Implementierung aus. Dadurch bleiben Service und Command unverändert und werden trotzdem mit einem gezielt kontrollierten Repository-Verhalten ausgeführt. Die Vererbung allein aktiviert das Test-Repository nicht; entscheidend ist seine Instanziierung und Auswahl in der tatsächlich von der Testsuite referenzierten Konfiguration.

## Teil V – Querschnittsthemen

### Konfiguration mit `OFX Config`

Eine `OFX Config` (`OFXConfig`) beschreibt die Laufzeitkomponenten und deren Abhängigkeiten. Konzeptionell entspricht sie einer modellierten, XML-generierenden IoC-Konfiguration: Komponenten werden bereitgestellt, Sections eingebunden und Properties überschrieben. Eine Dependency-Resolution-Strategie kann Komponenten anhand konfigurierter Packages finden.

Wichtige Möglichkeiten sind:

- wiederverwendbare Konfigurations-Sections einbinden,
- Properties einer eingebundenen Section überschreiben,
- eine primäre Implementierung gegenüber anderen Kandidaten auswählen,
- Komponenten-Scanning für Packages konfigurieren,
- unterschiedliche Konfigurationen für Entwicklung, Test und Deployment bereitstellen.

Services und Repositories werden über diese Konfiguration zu Laufzeitkomponenten. Ein `OperationCall` löst die passende konfigurierte Instanz auf.

### Rollen, Scopes und Identities

`Roles and Permissions` (`RolesAndPermissions`) bündelt drei Arten von Zugriffskonzepten:

| Name | Konzeptname | Aufgabe |
| --- | --- | --- |
| statische Rolle | `StaticRole` | Prüft anhand der User Environment, ob ein Benutzer eine Rolle besitzt; Rollen können weitere Rollen einschließen |
| Scope | `Scope` | Liefert die für einen Benutzer beziehungsweise Kontext zugänglichen Objekte eines Typs |
| Identity | `Identity` | Hält ein einzelnes, für den Anwendungskontext zentrales Objekt beziehungsweise dessen Schlüssel |

Commands deklarieren Zugriffsberechtigungen als `CAN_OPEN_RO role ...` oder `CAN_OPEN_RW role ...`. Damit wird nicht nur eine Rolle, sondern zugleich die erlaubte Zugriffsart des Commands festgelegt. Rollen sind hierarchisch modellierbar: Eine übergeordnete Rolle kann die Fähigkeiten einer weiteren Rolle einschließen.

Scopes sind nicht nur Berechtigungsflags, sondern liefern eine eingeschränkte Objektmenge. Sie können Parameter und lokale Variablen besitzen und Services beziehungsweise Repositories über `OperationCall` verwenden.

### User Environment und User Service

Die User Environment stellt den technischen und fachlichen Benutzerkontext einer laufenden Anwendung oder eines Jobs bereit. ObjectFlow-Ausdrücke können über die Session auf User Environment und User Service zugreifen. Typische Verwendungen sind Berechtigungsprüfung, Auswahl eines fachlichen Mandanten beziehungsweise Standorts und Auditinformationen.

Der Benutzerkontext ist Teil der Ausführung, ersetzt aber keine fachlichen Prüfungen. Insbesondere bei Jobs muss er ausdrücklich initialisiert werden.

### Statische Ressourcen

`Static Ressources` (`StaticRessources`) bündelt wiederverwendbare Labels und Farben für eine oder mehrere Plattformen. Ein Ressourcensatz kann einen anderen erweitern.

- Ein Label (`Label`) kann mehrere plattformspezifische Spezifikationen besitzen.
- Eine Farbe (`Color`) deklariert einen benannten Farbwert.
- Statuswerte, Commands und UI-Elemente können diese Ressourcen referenzieren.

Ressourcen halten wiederkehrende Darstellungsvorgaben zentral. Fachliche Zustände und Entscheidungen bleiben davon getrennt.

### Logging und Observability

Das Statement `log` (`LogStatement`) schreibt eine formatierte Meldung mit Log-Level und optionalen strukturierten Properties. Es ist gegenüber direkter Ausgabe auf `System.out` oder `System.err` zu bevorzugen, weil die Laufzeit Meldungen an ihre Observability- und Reporting-Infrastruktur weitergeben kann.

Preconditions, Guards und Exceptions besitzen unterschiedliche Zielgruppen:

- Precondition-Meldungen erklären dem Benutzer Problem und mögliche Korrektur.
- Guard-Meldungen schützen den Benutzer vor technischen Details; Diagnose und Stacktrace bleiben für Entwickler erhalten.
- Logs ergänzen fachlichen Kontext und strukturierte Werte für Betrieb und Analyse.

Trace-Ausgaben sollen im Produktivbetrieb gezielt bleiben. Sensible fachliche oder personenbezogene Daten gehören nicht unkontrolliert in Meldung oder Properties.

### Serialisierung und Serdes

Die ergänzende ObjectFlow-Serdes-Sprache stellt mit `CONV` Konvertierungs- und Serialisierungsmöglichkeiten bereit, beispielsweise für JSON. Projektspezifische Konverter können Properties auswählen, verändern oder besonders formatieren. Die genaue Menge verfügbarer Serdes-Konzepte ist versions- und projektspezifisch und muss vor einer neuen Verwendung in der aktuell geladenen Sprache geprüft werden.

Serialisierung ist kein Ersatz für DTO-Modellierung. Ein explizites DTO bleibt sinnvoll, wenn eine Schnittstelle nur einen stabilen Ausschnitt des fachlichen Modells veröffentlichen soll.


## Durchgängige Abläufe

### Rechnung suchen und bearbeiten

1. Ein `SEARCH_CMD` erzeugt ein Filter-DTO und zeigt seine erste Page.
2. Eine Page Conclusion ruft eine `READONLY`-Repository-Methode per `OperationCall` auf.
3. Das Repository liefert read-only Ergebnis-DTOs; eine Tabelle zeigt sie an.
4. Eine Aktion startet einen `GRAPH_OWNER_CMD` mit der ausgewählten Rechnungs-ID.
5. Dessen `command init` lädt die Rechnung und ihre Positionen per Checkout.
6. Ein `GRAPH_EDIT_CMD` bearbeitet eine Position innerhalb derselben Session.
7. Der Owner registriert die Check-in-Operationen.
8. Seine `FINAL_OK`-Funktion läuft; danach werden die Operationen in Registrierungsreihenfolge innerhalb einer Transaktion ausgeführt und committed.

### Suchergebnis nach Child-Command aktualisieren

1. Der Such-Command verwendet `NEWSTYLE_CMD_TERM_HANDLING`.
2. Ein Child-Command bearbeitet oder erzeugt eine Entity und pusht sie bei erfolgreichem Abschluss.
3. Der Termination-Handler des Such-Commands erhält das gepushte Objekt.
4. `session merge` integriert dessen Werte explizit in das passende Suchergebnis beziehungsweise ergänzt ein neues Ergebnis.
5. Die Selektion wird ausdrücklich auf das integrierte Objekt gesetzt.

### Command in einer Testsuite ausführen

1. Die `OFX Test Suit` wählt eine Testkonfiguration.
2. Ein `Simple Test` startet mit einer eigenen, nicht commitfähigen Test-Session.
3. `run command` ruft den zu prüfenden Command mit definierten Parametern auf.
4. Für jede erwartete Page wählt der Test eine Conclusion und prüft bei Bedarf das gebundene Objekt.
5. Successor-Commands werden über Successor-Handler beantwortet.
6. Nach dem Test wird die Session verworfen; `on shutdown` läuft nach dem letzten Test.


## Häufige Fehler und Diagnose

- **Service oder Repository direkt als Java-Objekt aufrufen:** Dadurch wird die Komponenten-, Session- und Transaktionssemantik von `OperationCall` umgangen.
- **Service als zustandsbehaftete Benutzerinstanz behandeln:** Services werden typischerweise einmal pro Anwendung instanziiert und sollen zustandslos bleiben.
- **Infrastrukturzugriff in eine Datenstrukturmethode verschieben:** Entities, Value Objects und DTOs können keinen `OperationCall` ausführen. Erforderliche Daten müssen vorab geladen oder als Parameter übergeben werden; die Koordination gehört in einen Service oder Command.
- **Value Objects nachträglich verändern:** Dadurch werden wertbezogene Gleichheit und die Weitergabe gemeinsam genutzter Werte schwer nachvollziehbar. Bei einer fachlichen Änderung ist ein neuer Wert zu erzeugen.
- **Virtuelle Property wie einen gespeicherten Wert behandeln:** Sie besitzt keinen eigenen Persistenzwert. Getter und Setter müssen den Wert vollständig aus den zugrunde liegenden Properties ableiten beziehungsweise dorthin zurückschreiben.
- **Entity-Beziehungen über sämtliche Objektwerte vergleichen:** Mit `#Key` wird ausdrücklich die Identität verglichen; bei zusammengesetzten Schlüsseln stehen anschließend deren einzelne Bestandteile zur Verfügung.
- **Nicht geladene Entity-Referenz direkt lesen:** Ohne Reference Join löst der Property-Zugriff `OFXNotInitializedException` aus. Über `#Key` kann die Ziel-Entity ausdrücklich per Repository geladen werden.
- **`isNullKey` mit dem Ladezustand verwechseln:** Die Operation prüft, ob der Beziehungsschlüssel gesetzt ist; eine Entity kann einen gültigen Schlüssel besitzen und trotzdem noch nicht als Objekt geladen sein.
- **Read-only Entity verändern:** Setter einer read-only geladenen Entity werfen `OFXIllegalAccessException`. Ändernde Abläufe benötigen einen gezielten Checkout.
- **Nur `session.setReadOnly()` als Entity-Schutz betrachten:** Der Schalter verhindert speichernde Session-Operationen, setzt bereits integrierte Entities aber nicht nachträglich einzeln auf read-only.
- **`null` als normalen Ersatzstatus verwenden:** Optionale Werte müssen fachlich und in DataUX ausdrücklich als optional modelliert werden; für reguläre Zustände ist ein Statuswert vorzuziehen.
- **Unpassenden String-Platzhalter verwenden:** `OFXStringFormatter2` prüft die erwarteten Typen zur Laufzeit und wirft bei einer falschen Kombination eine Exception.
- **Session-Operation mit unmittelbarem Aufruf verwechseln:** Nach der Registrierung sind Rückgabewerte und beim Speichern erzeugte IDs noch nicht vorhanden.
- **Session-Operationen im `GRAPH_EDIT_CMD` registrieren:** Sie bleiben auch nach einem Child-Abbruch im Stack. Die Registrierung gehört üblicherweise in den Session Owner.
- **Commit bei `SEARCH_CMD` erwarten:** Seine Session wird auch nach `FINAL_OK` nicht committed.
- **`GRAPH_OWNER_CMD_MODAL` für einen Graph Edit halten:** Er besitzt wie ein normaler Graph Owner eine eigene Session und einen eigenen Commit.
- **Precondition, Guard und Exception gleich behandeln:** Preconditions sind korrigierbare Benutzerprobleme; Guards und Exceptions beenden den Command technisch. Ein Guard im Graph Edit eskaliert zusätzlich zum Owner.
- **Mehrere Preconditions ohne `validation` sammeln wollen:** Außerhalb des Blocks stoppt bereits die erste verletzte Precondition den Programmfluss.
- **Prüfungen und Graphänderungen vermischen:** Schlägt eine spätere Prüfung fehl, bleibt ein schwer nachvollziehbarer teilweise geänderter Graph zurück. Zuerst vollständig validieren, danach ändern.
- **Abbrechende Precondition in Page Init auslösen:** Dadurch wird der Aufbau oder Refresh der Page unterbrochen. In Page Init nur Warnungen verwenden; abbrechende Prüfungen gehören in `command init` oder eine Conclusion.
- **`no_save` als normalen Conclusion-Modus verwenden:** `save` ist der Standard und übernimmt Editorwerte auch bei teilweise deaktivierter UI. `no_save` ist nur für bewusst zu verwerfende Editoränderungen gedacht.
- **Branching Command mit seiner Darstellung verwechseln:** Die Page bietet den Command an; sichtbar wird er erst durch einen passenden Menüeintrag im DataUX-`Page Pane`.
- **Precondition an einer `TO_SESSION_OPS`-Methode definieren:** Die Laufzeit lehnt dies ab.
- **Revert als Datenbank-Rollback verstehen:** Revert stellt kopierte In-Memory-Objekte wieder her; die Check-in-Transaktion wurde bei einem normalen Abbruch noch nicht begonnen.
- **Nur ein Kindobjekt statt der Graph-Wurzel für Revert auswählen:** Dann wird nicht automatisch der vollständige Aggregatgraph zurückgesetzt.
- **Dieselbe Entity erneut auschecken:** Mit `session entities` beziehungsweise den Schlüsselvarianten zuerst die bestehende Session prüfen.
- **Automatisches Merge im neuen Termination-Modus erwarten:** Gepushte Objekte müssen explizit übernommen, gemergt und gegebenenfalls selektiert werden.
- **`session queue next command` ohne UI verwenden:** Tests und Jobs ignorieren diesen Mechanismus.
- **`IN_BACKGROUND` als Hintergrundausführung des gesamten Commands verstehen:** Nur `command init` läuft im Hintergrund.
- **URL-Parameter nicht in den Command-Kontext pushen:** Nach der Initialisierung stehen sie sonst nicht wie normale Command-Parameter für den Ablauf bereit.
- **UI-Logik und Domänenlogik vermischen:** Darstellung gehört nach DataUX; wiederverwendbare fachliche Regeln gehören in Datenstrukturen oder Services.
- **`#Meta` als fachliche Validierung verwenden:** Deaktivierte oder eingeschränkte UI-Eingaben ersetzen keine serverseitige Precondition oder Validierung.
- **Name und Konzeptname verwechseln:** Name, Konzeptname und FQ-Name nach der eingangs festgelegten Schreibweise unterscheiden.


## Konzeptindex für Agenten

Der Index enthält die in dieser Dokumentation behandelten wichtigen Konzepte, nicht alle Konzepte der Sprache. Für JSON-Blueprints sind die FQ-Namen zu verwenden. Vor einer Modelländerung müssen Referenzen, Child-Roles und Kardinalitäten über MPS MCP im aktuellen Projekt aufgelöst werden.

| Themenbereich | Name | Konzeptname | FQ-Name |
| --- | --- | --- | --- |
| Datenstruktur | `Entity` | `Entity` | `org.modellwerkstatt.objectflow.structure.Entity` |
| Datenstruktur | `Value Object` | `ValueObject` | `org.modellwerkstatt.objectflow.structure.ValueObject` |
| Datenstruktur | `DTO` | `DTO` | `org.modellwerkstatt.objectflow.structure.DTO` |
| Datenstruktur | Business Property | `BusinessProperty` | `org.modellwerkstatt.objectflow.structure.BusinessProperty` |
| Datenstruktur | virtuelle Property-Implementierung | `CustomPropertyImplementation` | `jetbrains.mps.baseLanguage.structure.CustomPropertyImplementation` |
| Datenstruktur | `#Key` einer Entity-Beziehung | `BPRefIdReference` | `org.modellwerkstatt.objectflow.structure.BPRefIdReference` |
| Datenstruktur | `isNullKey` | `IsNull` | `org.modellwerkstatt.objectflow.structure.IsNull` |
| Datenstruktur | equal property | `EqualPropertyReference` | `org.modellwerkstatt.objectflow.structure.EqualPropertyReference` |
| Status | Status | `StatusDeclaration` | `org.modellwerkstatt.objectflow.structure.StatusDeclaration` |
| Status | Statuselement | `StatusElement` | `org.modellwerkstatt.objectflow.structure.StatusElement` |
| Status | Status-Typ | `StatusType` | `org.modellwerkstatt.objectflow.structure.StatusType` |
| Status | `of` | `StatusOfOperator` | `org.modellwerkstatt.objectflow.structure.StatusOfOperator` |
| Status | `fromDbValue` | `StatusFromDbValue` | `org.modellwerkstatt.objectflow.structure.StatusFromDbValue` |
| Statusoption | `ALLOW_NULL_PERSISTANCE` | `AllowNullStatusDeclOption` | `org.modellwerkstatt.objectflow.structure.AllowNullStatusDeclOption` |
| Statusoption | `OPTIONAL_AS` | `OptionalAsStatusDeclOption` | `org.modellwerkstatt.objectflow.structure.OptionalAsStatusDeclOption` |
| Statusoption | `ON_CREATION` | `OnCreationStatusElemOption` | `org.modellwerkstatt.objectflow.structure.OnCreationStatusElemOption` |
| Statusoption | `COLOR` | `ColorStatusElemOption` | `org.modellwerkstatt.objectflow.structure.ColorStatusElemOption` |
| Statusoption | `WHEN_NULL_WL` | `WhenNullOnDbStatusElemOption` | `org.modellwerkstatt.objectflow.structure.WhenNullOnDbStatusElemOption` |
| Statusoption | `WHEN_UNDEFINED_WL` | `WhenUndefinedStatusElemOption` | `org.modellwerkstatt.objectflow.structure.WhenUndefinedStatusElemOption` |
| Formatierung | formatierter String | `StringFormatString` | `org.modellwerkstatt.objectflow.structure.StringFormatString` |
| UI-Metadaten | `#Meta` einer Business Property | `BPMetaReference` | `org.modellwerkstatt.objectflow.structure.BPMetaReference` |
| Literal | Datum | `DateLiteral` | `org.modellwerkstatt.objectflow.structure.DateLiteral` |
| Literal | Zeitpunkt | `DateTimeLiteral` | `org.modellwerkstatt.objectflow.structure.DateTimeLiteral` |
| Literal | Dezimalzahl | `DezimalLiteral` | `org.modellwerkstatt.objectflow.structure.DezimalLiteral` |
| Service | `Service` | `Service` | `org.modellwerkstatt.objectflow.structure.Service` |
| Service | service method | `ServiceInstanceMethodDeclaration` | `org.modellwerkstatt.objectflow.structure.ServiceInstanceMethodDeclaration` |
| Serviceoption | `API_METHOD` | `SimdApiMethod` | `org.modellwerkstatt.objectflow.structure.SimdApiMethod` |
| Serviceoption | `TO_SESSION_OPS` | `SimdToSessionOps` | `org.modellwerkstatt.objectflow.structure.SimdToSessionOps` |
| Komponentenaufruf | `#` | `OperationCall` | `org.modellwerkstatt.objectflow.structure.OperationCall` |
| Prüfung | precondition | `Precondition` | `org.modellwerkstatt.objectflow.structure.Precondition` |
| Prüfung | Problemtext einer Precondition | `ProblemMessage` | `org.modellwerkstatt.objectflow.structure.ProblemMessage` |
| Prüfung | Precondition-Option | `CheckOptionRef` | `org.modellwerkstatt.objectflow.structure.CheckOptionRef` |
| Prüfung | Diagnoseeigenschaft | `LogStatementProperty` | `org.modellwerkstatt.objectflow.structure.LogStatementProperty` |
| Prüfung | validation | `ValidationStatement` | `org.modellwerkstatt.objectflow.structure.ValidationStatement` |
| Prüfung | guard | `Guard` | `org.modellwerkstatt.objectflow.structure.Guard` |
| Command | `Command` | `Command` | `org.modellwerkstatt.objectflow.structure.Command` |
| Command | Parameter | `ContainerParameter` | `org.modellwerkstatt.objectflow.structure.ContainerParameter` |
| Command | Variable | `ContainerVariable` | `org.modellwerkstatt.objectflow.structure.ContainerVariable` |
| Command | Page | `PageCrtl` | `org.modellwerkstatt.objectflow.structure.PageCrtl` |
| Command | Page Conclusion | `PageConclusion` | `org.modellwerkstatt.objectflow.structure.PageConclusion` |
| Command | Page-Wechsel | `PageCommand` | `org.modellwerkstatt.objectflow.structure.PageCommand` |
| Command | `done` | `DoneCommand` | `org.modellwerkstatt.objectflow.structure.DoneCommand` |
| Command | Page-spezifische Scopes | `PageScopeConceptFunc` | `org.modellwerkstatt.objectflow.structure.PageScopeConceptFunc` |
| Command | bedingte `Page Pane`-Auswahl | `PagePaneActionProviderLink` | `org.modellwerkstatt.objectflow.structure.PagePaneActionProviderLink` |
| Command | Termination Handler einer Page | `PageCmdTermHandler` | `org.modellwerkstatt.objectflow.structure.PageCmdTermHandler` |
| Commandberechtigung | `CAN_OPEN_RO` | `OpenPermissionCmd` | `org.modellwerkstatt.objectflow.structure.OpenPermissionCmd` |
| Commandberechtigung | `CAN_OPEN_RW` | `OpenSavePermissionCmd` | `org.modellwerkstatt.objectflow.structure.OpenSavePermissionCmd` |
| Commandoption | `IN_BACKGROUND` | `CommandBackgroundOption` | `org.modellwerkstatt.objectflow.structure.CommandBackgroundOption` |
| Commandoption | `NO_ESC` | `CommandNoEscOption` | `org.modellwerkstatt.objectflow.structure.CommandNoEscOption` |
| Commandoption | `NEWSTYLE_CMD_TERM_HANDLING` | `CommandNoPushNewTermOption` | `org.modellwerkstatt.objectflow.structure.CommandNoPushNewTermOption` |
| Commandoption | `URL` | `CommandUrlOption` | `org.modellwerkstatt.objectflow.structure.CommandUrlOption` |
| Session | session | `Session` | `org.modellwerkstatt.objectflow.structure.Session` |
| Session | session operation add | `SessionOperationAdd` | `org.modellwerkstatt.objectflow.structure.SessionOperationAdd` |
| Session | session entities | `CheckedOutEntities` | `org.modellwerkstatt.objectflow.structure.CheckedOutEntities` |
| Session | session merge | `MergeInto` | `org.modellwerkstatt.objectflow.structure.MergeInto` |
| Session | session queue next command | `SessionQueueNextCommand` | `org.modellwerkstatt.objectflow.structure.SessionQueueNextCommand` |
| Selektion | `getSelected()` | `SelectedObject` | `org.modellwerkstatt.objectflow.structure.SelectedObject` |
| Selektion | `getSelectedObjects()` | `SelectedList` | `org.modellwerkstatt.objectflow.structure.SelectedList` |
| Tests | `OFX Test Suit` | `OFXTestSuit` | `org.modellwerkstatt.objectflow.structure.OFXTestSuit` |
| Tests | `Simple Test` | `OFXTestMethod` | `org.modellwerkstatt.objectflow.structure.OFXTestMethod` |
| Tests | `run command` | `OFXRunCmd` | `org.modellwerkstatt.objectflow.structure.OFXRunCmd` |
| Tests | Run-Command-Page | `OFXRunCmdPage` | `org.modellwerkstatt.objectflow.structure.OFXRunCmdPage` |
| Tests | Successor-Handler | `OFXRunCmdSuccessorHandler` | `org.modellwerkstatt.objectflow.structure.OFXRunCmdSuccessorHandler` |
| Konfiguration | `OFX Config` | `OFXConfig` | `org.modellwerkstatt.objectflow.structure.OFXConfig` |
| Berechtigungen | Roles and Permissions | `RolesAndPermissions` | `org.modellwerkstatt.objectflow.structure.RolesAndPermissions` |
| Berechtigungen | static role | `StaticRole` | `org.modellwerkstatt.objectflow.structure.StaticRole` |
| Berechtigungen | scope | `Scope` | `org.modellwerkstatt.objectflow.structure.Scope` |
| Berechtigungen | identity | `Identity` | `org.modellwerkstatt.objectflow.structure.Identity` |
| Ressourcen | Static Ressources | `StaticRessources` | `org.modellwerkstatt.objectflow.structure.StaticRessources` |
| Ressourcen | Label | `Label` | `org.modellwerkstatt.objectflow.structure.Label` |
| Ressourcen | Color | `Color` | `org.modellwerkstatt.objectflow.structure.Color` |
| Observability | log | `LogStatement` | `org.modellwerkstatt.objectflow.structure.LogStatement` |
