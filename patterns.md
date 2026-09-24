# Angewendete Muster in eFWWS

## Zweck und Einordnung

Dieses Dokument beschreibt wiederkehrende Lösungs- und Strukturmuster, die in der Anwendung **eFWWS** tatsächlich eingesetzt werden. Grundlage sind die in [moware-werkbank.md](moware-werkbank.md), [objectflow.md](objectflow.md), [manmap.md](manmap.md) und [dataux.md](dataux.md) erläuterten Sprachkonzepte sowie eine projektweite Untersuchung der MPS-Modelle.

Der Blick ist bewusst empirisch:

- Ein Muster wird nicht allein deshalb beschrieben, weil die Werkbank es ermöglicht, sondern weil es im Projekt wiederholt oder architektonisch prägend vorkommt.
- Varianten und Widersprüche zur Dokumentation werden sichtbar gemacht.
- Eine Abweichung gilt nicht automatisch als Fehler. Für jede wesentliche Abweichung werden Nutzen, Risiko und geeignete Einsatzgrenzen betrachtet.
- Beispiele sind fachlich anonymisiert. Interne Modul-, Modell-, Typ- und Methodennamen sowie vollständig qualifizierte Namen werden nicht wiedergegeben.

Im Vordergrund stehen Fachmodell, Anwendungsablauf, Persistenz, Session- und Transaktionsverhalten sowie die Bindung der Oberfläche. Konfiguration, Rollen und Berechtigungen, Tests und allgemeine Wiederverwendungsmuster sind vorerst nicht Gegenstand dieser Analyse.


## Untersuchungsbasis

Die Analyse betrachtet das Projekt als Ganzes und ergänzt die qualitative Untersuchung repräsentativer Abläufe durch projektweite Strukturabfragen. Zum untersuchten Stand umfasst die Anwendung unter anderem:

| Baustein | Anzahl |
| --- | ---: |
| Entities | 132 |
| Value Objects | 86 |
| DTOs | 295 |
| Services | 284 |
| Commands | 488 |
| Repositories | 181 |
| Persistenzbeschreibungen | 68 |
| PagePanes | 375 |
| Pages | 423 |
| Repository-Methoden | 788 |
| benutzerdefinierte SQL-Blöcke | 353 |

Die Zahlen dienen der Einordnung, nicht als Qualitätsmaß. Sie können sich mit der Weiterentwicklung des Projekts verändern. Auffällig ist bereits das Verhältnis von DTOs zu Entities: Die Anwendung besitzt neben dem Domänenmodell eine stark ausgeprägte anwendungsfallbezogene Lese- und Darstellungsseite.

Bei den Commands ergibt sich folgende Verteilung:

| Command-Art | Anzahl | Typische Aufgabe |
| --- | ---: | --- |
| Graph Owner | 208 | Session und Transaktion besitzen, Bearbeitungsgraph koordinieren |
| modaler Graph Owner | 13 | abgeschlossener, häufig vorgeschalteter Dialogablauf |
| Graph Edit | 158 | Teil eines bereits geladenen Graphen bearbeiten |
| Search | 109 | suchen, auswählen und Folgeaktionen anbieten |

Von den 788 Repository-Methoden sind 487 lesend, 121 zum Checkout, 160 zum Check-in und 20 zum Löschen modelliert. Die Anwendung verwendet damit sowohl gemappte Domänenobjekte als auch spezielle Lesemodelle in erheblichem Umfang.


## Die drei verwendeten Geschäftsfälle

Die Muster werden möglichst an einem durchgehenden Leitfall erklärt. Nur dort, wo dieser Fall die beobachtete Struktur nicht sinnvoll trägt, wird ein ergänzender Fall verwendet.

### Leitfall: Auftragsbearbeitung

Ein Auftrag besteht aus einem fachlichen Kopf, mehreren Positionen, referenzierten Stammdaten und ergänzenden Aufgaben. Er kann gesucht, neu angelegt, über mehrere Seiten bearbeitet und abschließend gespeichert werden. Einzelne Positionen werden in untergeordneten Dialogen verändert. Der Leitfall deckt damit Aggregat, Checkout, Check-in, Graph Owner, Graph Edit, mehrseitige Führung und Session Operations ab.

### Ergänzungsfall: Stammdatensuche und -pflege

Eine Suche liefert eine read-only Ergebnisliste. Aus dieser Liste kann ein Stammdatensatz geöffnet oder eine Aktion auf mehreren ausgewählten Datensätzen ausgeführt werden. Dieser Fall macht Such-DTOs, No-Key-Mappings, gemeinsame Selektion, explizites Merge nach einer Bearbeitung und Entity-förmige Lesemodelle sichtbar.

### Ergänzungsfall: fachlicher Prüfvorgang

Eine fachliche Aktion prüft mehrere Bedingungen. Ein Teil der Prüfungen warnt, ein anderer bricht ab. In einer besonderen Variante wird ein Versuchszähler bereits vor einer möglicherweise abbrechenden Prüfung verändert. Dieser Fall zeigt, wo das Projekt bewusst von der einfachen Regel „erst vollständig prüfen, dann verändern“ abweicht.


## Architektur in einem Ablauf

Der typische interaktive Änderungsablauf lässt sich wie folgt zusammenfassen:

1. Ein Search Command ermittelt ein zweckgebundenes Lesemodell.
2. Eine ausgewählte ID startet einen Graph Owner.
3. Der Graph Owner eröffnet beziehungsweise besitzt Session und Transaktion.
4. Eine Checkout-Methode lädt die Root-Entity und baut benötigte Teile des Objektgraphen explizit auf.
5. Pages stellen den Ablaufkontext bereit; PagePanes binden und visualisieren ihn.
6. Graph-Edit-Commands ändern Teile des bereits ausgecheckten Graphen.
7. Der Graph Owner registriert Check-in- oder Delete-Methoden als Session Operations.
8. Bei erfolgreichem Abschluss werden die Operationen ausgeführt und die Transaktion wird committed.
9. Der aufrufende Suchablauf übernimmt das zurückkehrende Objekt mit einem expliziten Merge in seine read-only Ergebnisliste.

Die Schichten sind dabei nicht bloß technisch getrennt. Jede Seite beantwortet eine andere Frage:

| Bereich | Leitfrage |
| --- | --- |
| Domänenmodell | Welche fachlichen Objekte, Werte und Regeln bilden den Vorgang? |
| Repository und Mapping | Welche Daten werden in welchem Modus geladen und gespeichert? |
| Service | Welche fachliche oder anwendungsfallbezogene Operation wird ausgeführt? |
| Command | Wer besitzt Ablauf, Session, Transaktion und Abschluss? |
| Page | Welche Daten und Aktionen stehen in diesem Schritt zur Verfügung? |
| PagePane | Wie werden diese Daten für ein Gerät oder einen Nutzungskontext dargestellt? |


## Muster 1: Vertikaler Anwendungsfallschnitt

### Beobachtung

Commands und PagePanes liegen fast vollständig in anwendungsfallbezogenen Modellen. Auch der größere Teil der DTOs und viele Services befinden sich dort. Entities, Value Objects, Persistenzbeschreibungen und schreibende Repository-Operationen sind dagegen stärker in fachlichen Modellen konzentriert.

Projektweit liegen 462 von 488 Commands und 360 von 375 PagePanes in solchen Anwendungsfallschnitten. Von 295 DTOs befinden sich 201 dort. Das ist kein zufälliger Ablagestil, sondern eine tragende Projektstruktur.

### Form

Ein Anwendungsfallschnitt bündelt typischerweise:

- den Einstieg als Search, Graph Owner oder Graph Edit,
- die für diesen Ablauf benötigten DTOs,
- anwendungsfallbezogene Services und lesende Repositories,
- Pages und PagePanes,
- Übergänge zu nachfolgenden Commands.

Das stabile Fachmodell bleibt separat. Der Schnitt darf es verwenden, aber nicht duplizieren.

### Nutzen

- Der Ablauf kann von Einstieg bis Darstellung an einem fachlichen Zweck verstanden werden.
- Spezifische Such- und Anzeigeinformationen belasten das Domänenmodell nicht.
- Änderungen an einer Oberfläche oder Suche bleiben überwiegend lokal.

### Grenze

Die Trennung ist nicht streng geschichtet: Repositories kommen häufig auch im Anwendungsfallschnitt vor. Das widerspricht einer Lesart, nach der sämtliche Persistenz ausschließlich beim Domänenmodell liegen müsse. Im Projekt ist die entscheidende Grenze eine andere:

- fachliches Laden und Speichern des Aggregats liegt überwiegend nahe am Domänenmodell,
- zweckgebundene Queries und Lesemodelle liegen häufig nahe am Anwendungsfall.

Diese Asymmetrie ist konsistent und sollte bei neuen Modellen beibehalten werden.


## Muster 2: Fachliches Aggregat mit expliziter Außengrenze

### Beobachtung

Im Leitfall bildet der Auftrag die Root-Entity. Positionen sind enthaltene Entities, Mengen und Preise werden als Value Objects dargestellt, referenzierte Stammdaten bleiben eigenständige Entities. Zusätzlich gibt es berechnete oder nur für die Darstellung benötigte Properties.

### Form

Ein Aggregat besitzt:

- genau einen fachlichen Einstieg für die Bearbeitung,
- enthaltene Bestandteile mit einem klaren Lebenszyklusbezug zur Root-Entity,
- Referenzen auf außerhalb liegende Objekte,
- Value Objects für fachliche Werte ohne eigene Identität,
- fachliche Methoden für lokale Regeln und Zustandsübergänge.

Die Persistenzgrenze folgt nicht automatisch jeder Objektbeziehung. Eine Referenz im Modell bedeutet weder automatisches Laden noch automatisches Speichern.

### Präsentationseigenschaften

Das Projekt verwendet an Entities auch Properties für Anzeige, Auswahl oder abgeleitete Information. Diese werden ausdrücklich als Präsentationseigenschaften kenntlich gemacht. Dadurch kann eine Oberfläche mit einem fachlichen Objekt arbeiten, ohne jede temporäre Information persistent zu machen.

Das Muster ist nützlich, wenn die Information eng an eine konkrete Entity-Instanz gebunden ist. Wird die Darstellung jedoch umfangreich oder kombiniert sie viele Quellen, ist ein DTO das klarere Modell.

### Entscheidungsregel

| Information | Geeigneter Ort |
| --- | --- |
| persistenter fachlicher Zustand | Entity oder Value Object |
| lokale fachliche Berechnung | Methode am Domänenobjekt oder Domain Service |
| kleine, instanzbezogene Anzeigeinformation | Präsentationseigenschaft |
| anwendungsfallspezifische Kombination vieler Quellen | DTO |
| Suchzeile oder Auswertung ohne Änderungsabsicht | read-only Lesemodell |


## Muster 3: Expliziter Checkout-Plan für den Objektgraphen

### Beobachtung

Der häufigste Weg zum bearbeitbaren Objekt ist eine Checkout-Repository-Methode. Sie lädt nicht nur die Root-Entity, sondern beschreibt zugleich den benötigten Graphen. Im Leitfall werden der Auftragskopf, einzelne Referenzen, Positionen und ergänzende Aufgaben in getrennten Schritten geladen.

### Form

Ein Checkout folgt typischerweise diesem Ablauf:

1. Root-Entity über ihren Schlüssel laden.
2. Nichtvorhandensein früh als Precondition behandeln.
3. Benötigte Einzelreferenzen explizit laden oder gezielt joinen.
4. Kindlisten über eigene Abfragen laden.
5. Rückreferenzen zwischen Parent und Kind setzen, wenn sie fachlich benötigt werden.
6. Zusätzliche Teile des Bearbeitungsgraphen separat ergänzen.

Der Schlüssel wird dabei über die vorgesehene Schlüsselabstraktion des Objekts übergeben. Auf konkrete Schlüsselbestandteile wird nur zugegriffen, wenn dies fachlich oder technisch wirklich erforderlich ist.

### Tatsächliche Projektpraxis

Obwohl die Persistenzsprache einen Listen-Join unterstützt, wurde im untersuchten Projekt kein verwendeter Listen-Join gefunden. Listen werden stattdessen mit separaten Abfragen geladen und anschließend explizit zugeordnet. Referenz-Joins kommen vor, sind aber ebenfalls nicht der alleinige Weg.

Das ist eine wichtige Unterscheidung zwischen Sprachumfang und Projektmuster:

> Die Sprache ermöglicht das Laden einer Liste per Join; die Anwendung bevorzugt für Listen einen sichtbaren, schrittweisen Ladeplan.

### Nutzen und Kosten

Der explizite Plan macht Datenmenge, Session-Modus und Aufbau des Graphen nachvollziehbar. Er vermeidet überraschendes Lazy Loading. Der Preis ist zusätzlicher Modellcode und die Gefahr, dass ein benötigter Teilgraph vergessen wird.

### Diagnosehinweis

Eine leere Liste bedeutet nicht zwingend, dass keine Datensätze existieren. Sie kann auch bedeuten, dass die Liste in diesem Checkout-Pfad nicht geladen wurde. Bei Fehlern ist deshalb zuerst der Ladeplan zu prüfen.


## Muster 4: Expliziter Check-in des Aggregats

### Beobachtung

Der Objektgraph wird nicht kaskadierend durch das Speichern der Root-Entity persistiert. Im Leitfall speichert die Check-in-Methode den Kopf, die gefilterten oder geänderten Positionen und weitere Bestandteile explizit mit ihren jeweiligen Mappings.

### Form

Ein Check-in enthält eine erkennbare Speicherreihenfolge:

1. Root-Entity mit ihrem Mapping speichern.
2. Kinder mit deren eigenem Mapping speichern, bei größeren Mengen gegebenenfalls als Batch.
3. weitere abhängige Bestandteile speichern oder löschen,
4. Audit-Varianten nur bewusst einsetzen.

Die Check-in-Methode führt die fachliche Speicherung aus. Der aufrufende Graph Owner entscheidet dagegen, ob und wann diese Methode als Session Operation registriert und schließlich committed wird.

### Konsequenz

Mapping, Objektbeziehung und Speicheroperation sind drei verschiedene Dinge:

- Das Mapping beschreibt die relationale Abbildung.
- Das Fachmodell beschreibt Zugehörigkeit und Referenz.
- Der Check-in beschreibt die tatsächlich auszuführende Persistenz.

Werden diese Ebenen gedanklich vermischt, entstehen unvollständig gespeicherte Graphen oder ungewollte Annahmen über Kaskaden.


## Muster 5: Zwei Lesewege – Domänenobjekt und zweckgebundenes Lesemodell

### Beobachtung

Die Anwendung nutzt beide von ManMap vorgesehenen Lesewege intensiv:

- gemappte Abfragen für Entities und bearbeitbare Graphen,
- benutzerdefiniertes SQL mit read-only Mapping für Suchen, Listen und Auswertungen.

105 Root Nodes verwenden gemappte Abfragen, 116 benutzerdefiniertes SQL; 55 kombinieren beide Formen. Das Projekt folgt damit keinem „alles über das Domänenmodell“-Ansatz.

### Domänenweg

Der Domänenweg ist passend, wenn:

- Identität und Session-Integration benötigt werden,
- das Ergebnis fachliches Verhalten trägt,
- ein späterer Checkout oder Check-in vorgesehen ist,
- das vorhandene Mapping die Abfrage ausreichend ausdrückt.

### Lesemodellweg

Ein zweckgebundenes Lesemodell ist passend, wenn:

- nur ein Ausschnitt der Daten benötigt wird,
- mehrere Tabellen oder berechnete Werte zusammenkommen,
- das Ergebnis nur angezeigt, gefiltert oder ausgewertet wird,
- keine Änderung über das Ergebnis zurückgeschrieben werden soll.

Der typische Ergebnistyp ist ein DTO. Das read-only Mapping besitzt keinen für Session-Identität verwendeten Schlüssel; das Ergebnis wird nach dem Anwendungsfall verworfen.

### Praktische Heuristik

> Suchen liefern Identifikatoren und Anzeigeinformationen. Bearbeiten beginnt mit einem gezielten Checkout der fachlichen Entity.

So bleibt die Suche leichtgewichtig, während die Änderung auf einem vollständig kontrollierten Bearbeitungsgraphen stattfindet.


## Muster 6: Search → Auswahl → Bearbeitung → Merge

### Beobachtung

Ein Search Command besitzt typischerweise ein Filter-DTO, eine Ergebnisliste und eine Page. Die Page führt die Suche bei Initialisierung oder nach einer Aktion aus. Aus der Auswahl wird ein Graph Owner gestartet. Kehrt die Bearbeitung zurück, wird das Ergebnis explizit in die vorhandene read-only Liste übernommen.

### Form

1. Search Command initialisieren.
2. Suchparameter in einem DTO halten.
3. read-only Ergebnisse laden.
4. aktuelles oder mehrere ausgewählte Ergebnisse an eine Aktion übergeben.
5. fachliches Objekt im nachfolgenden Graph Owner bearbeiten.
6. zurückgegebenes Objekt mit `merge` in die Suchliste übernehmen.
7. den von `merge` gelieferten Wert weiterverwenden.

Der letzte Punkt ist wichtig: Merge kann die kanonische Ergebnisinstanz liefern. Ein bloßer Aufruf ohne Nutzung des Rückgabewerts kann dazu führen, dass anschließend mit einer nicht maßgeblichen Instanz weitergearbeitet wird.

### Terminierungsvarianten

Das Projekt enthält eine ältere und eine explizitere Terminierungsform nebeneinander. Die neue Form mit einem sichtbaren Termination Handler und explizitem Merge ist nur in einem kleineren Teil der Commands markiert. In Such- und Listenabläufen zeigt sie ihren größten Nutzen, weil das Zurückkehren und Aktualisieren des Lesemodells nachvollziehbar wird.

Die Koexistenz ist als evolutionärer Zustand zu verstehen. Für neue oder grundlegend überarbeitete Suchabläufe sollte die explizite Variante bevorzugt werden, ohne daraus eine unreflektierte Massenmigration abzuleiten.


## Muster 7: Graph Owner als Transaktionsbesitzer

### Beobachtung

Der Graph Owner ist das zentrale Ablaufmuster der Anwendung. Er lädt oder erzeugt den Bearbeitungsgraphen, bietet eine oder mehrere Pages an und entscheidet über erfolgreichen Abschluss oder Abbruch.

### Verantwortungen

Ein Graph Owner:

- besitzt Session und Transaktionsrahmen,
- checkt den fachlichen Graphen aus oder legt ihn an,
- hält die Root-Entity beziehungsweise das Root-DTO,
- koordiniert untergeordnete Graph Edits,
- registriert Check-in- und Delete-Aufrufe als Session Operations,
- committed nur bei erfolgreichem Abschluss,
- liefert ausgewählte oder aktualisierte Objekte an den Aufrufer zurück.

### Session Operation ist nicht sofortige Speicherung

Die Registrierung einer Check-in-Methode beschreibt eine beabsichtigte spätere Operation. Erst beim erfolgreichen Abschluss führt die Session sie aus. Bei Abbruch werden die vorgesehenen Änderungen verworfen. Dieses Muster trennt fachliche Bearbeitung und endgültige Persistenz.

Direktes Hinzufügen von Session Operations kommt im Projekt vor, ist aber selten. Es wird für Sonderfälle verwendet, in denen eine Operation nicht bereits durch die übliche Command-Struktur registriert wird, etwa für eine nachgelagerte Aktualisierung oder einen zusätzlichen technischen Abschluss. Für den Normalfall bleibt die deklarative Registrierung am Graph Owner vorzuziehen.


## Muster 8: Graph Edit als lokale Änderung ohne eigene Transaktion

### Beobachtung

Im Leitfall bearbeitet ein Graph Edit eine einzelne Position des bereits ausgecheckten Auftrags. Er erhält Parent und Kind über die Auswahl, verwendet bei Bedarf ein Eingabe-DTO und ruft beim Abschluss einen Service auf.

### Form

Ein Graph Edit:

- arbeitet im Graphen und in der Session des aufrufenden Graph Owners,
- verändert einen abgegrenzten Teil des Graphen,
- registriert normalerweise keine eigenen Check-ins,
- kann bei Abbruch lokale Änderungen am Teilobjekt zurücknehmen,
- gibt das bearbeitete Objekt oder eine relevante Auswahl zurück.

### Abgrenzung

| Frage | Graph Owner | Graph Edit |
| --- | --- | --- |
| besitzt Session und Transaktion? | ja | nein |
| lädt den vollständigen Bearbeitungsgraphen? | typischerweise | nein |
| registriert Check-in/Delete? | ja | normalerweise nein |
| bearbeitet lokalen Teilgraphen? | koordiniert | ja |
| kann eigenständig als fachlicher Vorgang enden? | ja | nur innerhalb des Owners |

Diese Trennung verhindert verschachtelte oder konkurrierende Transaktionsgrenzen.


## Muster 9: Seitenloser Graph Owner

### Beobachtung

Von 208 Graph Ownern enthalten 116 mindestens eine Page; 92 besitzen keine Page. Der Graph Owner wird im Projekt daher nicht nur als sichtbarer Editor, sondern häufig als transaktionale Anwendungsfallgrenze verwendet.

### Einsatz

Ein seitenloser Graph Owner eignet sich für:

- eine atomare Fachaktion ohne zusätzliche Eingabe,
- eine Aktion auf einer bereits vorhandenen Auswahl,
- einen automatischen Abschluss nach Prüfung und Mutation,
- die koordinierte Registrierung mehrerer Session Operations.

### Grenze

Sobald eine Entscheidung, Bestätigung oder Dateneingabe durch den Benutzer notwendig ist, sollte diese nicht in technischem Servicecode versteckt werden. Dann ist eine Page oder ein vorgeschalteter modaler Ablauf angemessen.


## Muster 10: Mehrseitige Bearbeitung mit spätem Commit

### Beobachtung

Der Leitfall wird über mehrere Pages geführt. Die Root-Entity wird einmal geladen oder erzeugt. Zwischen den Seiten bleibt derselbe Bearbeitungsgraph in derselben Session erhalten. Erst die letzte erfolgreiche Conclusion registriert die Speicherung und schließt ab.

### Form

1. Initialisierung und Checkout beziehungsweise Neuanlage.
2. erste Page für Stammdaten oder Grunddaten.
3. Graph Edits für untergeordnete Bestandteile.
4. Termination Handler berechnet oder prüft Übergangswerte.
5. weitere Page für Zusammenfassung oder Abschluss.
6. finale Conclusion registriert Check-in und commit.

### Nutzen

- Alle Seiten arbeiten auf einer konsistenten Objektidentität.
- Abbruch bleibt bis zum Schluss möglich.
- Zwischenschritte benötigen keine eigene Persistenz.

### Risiko

Je länger der Ablauf und je größer der Graph, desto länger lebt die Session. Umfang des Checkouts, Konfliktwahrscheinlichkeit und Speicherbedarf müssen deshalb zum tatsächlichen Bearbeitungsfall passen.


## Muster 11: Validierung vor Mutation

### Beobachtung

Preconditions sind das dominante Prüfmittel. Projektweit stehen 705 Preconditions nur 30 expliziten Validation Statements gegenüber. Viele Abläufe prüfen nacheinander und brechen beim ersten Fehler ab. In einem Neuanlageablauf werden mehrere Bedingungen jedoch bewusst in einem Validierungsblock gesammelt, bevor die Entity erzeugt oder verändert wird.

### Grundregel

Wenn eine Aktion keine teilweise Wirkung haben darf:

1. alle unabhängig prüfbaren Bedingungen ermitteln,
2. zusammengehörige Prüfungen in einem Validierungsblock sammeln,
3. erst nach erfolgreicher Prüfung fachlichen Zustand verändern,
4. erst danach Session Operations registrieren.

Gesammelte Validierung ist besonders sinnvoll bei Formulareingaben, weil mehrere Fehler in einem Durchlauf gemeldet werden können. Eine einzelne Precondition bleibt passend, wenn ohne ihr Ergebnis keine weitere sinnvolle Prüfung möglich ist.

### Warnings

Warnings sind Bestätigungen und kein harter Abbruch. Mutationen nach einer bestätigten Warning sind daher nicht dieselbe Problemklasse wie Mutationen vor einer abbrechenden Precondition.


## Muster 12: Fortsetzung innerhalb derselben Session

### Beobachtung

Nach einer erfolgreichen Neuanlage wird häufig unmittelbar der reguläre Bearbeitungsablauf gestartet. Dafür verwendet die Anwendung überwiegend Successor Commands. Projektweit wurden 74 Successor-Aufrufe, aber nur ein explizites Einreihen eines nächsten Commands nach dem Abschluss gefunden.

### Auswahlregel

| Gewünschte Semantik | Mechanismus |
| --- | --- |
| Folgeablauf gehört fachlich und transaktional zum aktuellen Vorgang | Successor |
| aktueller Vorgang muss zuerst vollständig committen | nächstes Command nach Abschluss einreihen |
| reine Unterbearbeitung desselben Graphen | Graph Edit oder untergeordneter Command-Aufruf |

Ein Successor ist damit nicht bloß Navigation. Er drückt die Absicht aus, den Ablauf innerhalb der bestehenden Session- und Transaktionslogik fortzusetzen.


## Muster 13: Page liefert Kontext, PagePane bindet Darstellung

### Beobachtung

Die Page enthält Daten, Initialisierung, Aktionen und Conclusion. Das PagePane stellt diese Informationen dar und bindet Tabellen, Formulare, Buttons und Layouts. Für denselben fachlichen Schritt können mehrere PagePanes existieren, beispielsweise für unterschiedliche Geräteklassen.

### Form

- Die Page ist Teil des Ablaufs und kennt dessen Daten.
- Das PagePane bindet auf Page, Root-Objekt, Auswahl oder abgeleitete Werte.
- Ein Geräte- oder Plattformwechsel wählt eine alternative Darstellung, nicht einen neuen Fachablauf.
- Das Binding zeigt vorhandene Daten; es ersetzt kein Laden.

Im Leitfall bindet eine Tabelle an die Positionsliste der ausgewählten Root-Entity. Zeilenaktionen starten Graph Edits mit der aktuellen Auswahl. Summen oder Statusinformationen werden im gleichen Pane angezeigt, stammen aber aus dem Page- oder Domänenkontext.

### Diagnosehinweis

Ist eine gebundene Tabelle leer, sind drei Ebenen getrennt zu prüfen:

1. Hat das Repository die Liste geladen?
2. Stellt die Page die richtige Instanz bereit?
3. Bindet das PagePane an den richtigen Pfad?

Ein korrektes Binding kann fehlende Datenbeladung nicht kompensieren.


## Muster 14: Gemeinsame Auswahl über mehrere Darstellungen

### Beobachtung

Im ergänzenden Stammdatenfall zeigen zwei Tabs dieselbe Ergebnisliste in unterschiedlichen Tabellenansichten. Beide verwenden dieselbe Selektion. Eine Auswahl in einer Darstellung steht dadurch auch der anderen Darstellung und den gemeinsamen Aktionen zur Verfügung.

### Nutzen

- verschiedene Sichten auf denselben Ergebnissatz,
- konsistente aktuelle Auswahl,
- kein manuelles Synchronisieren zweier Selektionsmodelle,
- gemeinsame Einzel- und Mehrfachaktionen.

Bei Mehrfachauswahl werden Compound Actions eingesetzt, die den gesamten ausgewählten Bestand an einen nachfolgenden Ablauf übergeben. Die implizit gemeinsame Selektion ist gewollt, muss aber beim Modellieren erkennbar bleiben. Zwei fachlich unabhängige Tabellen desselben Elementtyps dürfen nicht versehentlich dieselbe Auswahl teilen.


## Muster 15: Domain Service und anwendungsfallbezogener Service

### Beobachtung

Services treten sowohl nahe am Fachmodell als auch nahe am Anwendungsfall auf. Diese beiden Rollen sind unterscheidbar, auch wenn sie technisch mit demselben Sprachkonzept modelliert werden.

### Domain Service

Ein Domain Service:

- führt Regeln aus, die nicht natürlich zu genau einer Entity gehören,
- koordiniert mehrere fachliche Objekte,
- berechnet oder vollzieht fachliche Zustandsübergänge,
- bleibt von Pages und konkreter Darstellung unabhängig.

### Anwendungsfallbezogener Service

Ein anwendungsfallbezogener Service:

- bereitet Daten für einen Ablauf auf,
- verbindet mehrere Repositories,
- ergänzt Anzeige- und Auswahlinformationen,
- sortiert oder normalisiert einen geladenen Graphen,
- kapselt technische Orchestrierung, die nicht in Page oder Command ausufern soll.

### Regel

Fachliche Entscheidung gehört in das Domänenmodell oder einen Domain Service. Ablaufbezogene Zusammenstellung gehört in den Anwendungsfallschnitt. Ein Command koordiniert beides, soll aber nicht selbst zum großen Fachservice werden.


## Dokumentierte Varianten und Widersprüche

Die folgenden Punkte weichen von vereinfachten Regeln der Grunddokumentation ab oder präzisieren sie anhand der Projektpraxis.

### Variante A: Entity-förmiges read-only Lesemodell

#### Beobachtung

Die Dokumentation empfiehlt für No-Key-Ergebnisse typischerweise DTOs. Im Projekt existiert mindestens ein wichtiger Suchfall, in dem ein No-Key-Mapping ein vorhandenes Entity-Mapping einbindet und Entity-förmige Objekte erzeugt. Die Ergebnisse bleiben read-only und liegen außerhalb der normalen Session-Identität.

#### Warum das attraktiv ist

- vorhandene Feldabbildungen werden wiederverwendet,
- Anzeige und bestehende Bindings können denselben strukturellen Typ nutzen,
- Mapping-Duplikation wird reduziert.

#### Risiko

Der Typ sieht wie ein normales Domänenobjekt aus, besitzt in diesem Kontext aber andere Lebenszyklus- und Änderungsregeln. Entwickler können versehentlich fachliches Verhalten oder Mutationen erwarten, obwohl das Objekt nur eine Projektion ist.

#### Einsatzgrenze

Diese Form ist vertretbar, wenn:

- die Verwendung strikt read-only bleibt,
- Herkunft und Lebensdauer im Anwendungsfall erkennbar sind,
- vor einer Änderung ein echter Checkout erfolgt,
- der Nutzen der Mapping-Wiederverwendung die begriffliche Unschärfe rechtfertigt.

Für neue, stark zugeschnittene Suchzeilen bleibt ein DTO die klarere Standardwahl.


### Variante B: Repositories im Anwendungsfallschnitt

#### Beobachtung

Repositories sind nicht ausschließlich beim Domänenmodell angesiedelt. Viele liegen zusammen mit Commands und DTOs in anwendungsfallbezogenen Modellen. Besonders benutzerdefiniertes SQL und No-Key-Mappings konzentrieren sich dort, während Checkouts und Check-ins stärker im fachlichen Bereich liegen.

#### Bewertung

Dies widerspricht einer streng technischen oder schichtenorientierten Ablage, passt aber zum vertikalen Schnitt. Ein Repository ist hier nicht automatisch ein Domain Repository; es kann auch ein privater Datenzugang eines Lesefalls sein.

#### Regel

- Repository für Aggregatlebenszyklus: nahe am Fachmodell.
- Repository für Suche, Auswertung oder Page-spezifische Projektion: nahe am Anwendungsfall.
- Gemischte Verantwortung in einem Repository vermeiden.


### Variante C: Technischer Zustand in Services

#### Beobachtung

Services werden grundsätzlich einmal pro Anwendung instanziert und sollen daher fachlich zustandslos sein. Dennoch enthalten 19 von 284 Services Fields. Untersuchte Beispiele verwenden sie für:

- zeitlich begrenzte, anwendungsweite Caches,
- bei Konstruktion aufgebaute Nachschlagetabellen,
- verzögert erzeugte technische Clients.

Es wurde in diesen Beispielen kein benutzer- oder sessionbezogener veränderlicher Zustand festgestellt.

#### Bewertung

Die Regel „Services sind zustandslos“ muss präzisiert werden:

> Services halten keinen veränderlichen fachlichen Zustand eines Benutzers oder Vorgangs. Kontrollierter, anwendungsweiter technischer Zustand kann zulässig sein.

#### Bedingungen

Ein solcher Zustand braucht:

- definierte Lebensdauer und Invalidierung,
- Thread-Sicherheit,
- keine Vermischung verschiedener Benutzer oder Sessions,
- ein Verhalten, das auch bei leerem oder neu aufgebautem Cache korrekt bleibt,
- klare Trennung von fachlicher Wahrheit und Beschleunigung.


### Variante D: Mutation vor abbrechender Prüfung

#### Beobachtung

In einem fachlichen Prüfvorgang wird ein Versuchszähler erhöht, bevor eine nachfolgende Precondition die Aktion abbrechen kann. Das widerspricht der allgemeinen Empfehlung, erst zu validieren und danach zu mutieren.

#### Fachliche Absicht

Die Mutation ist Teil eines progressiven Bestätigungs- oder Wiederholungsverhaltens: Der nächste Versuch soll sich vom ersten unterscheiden. Der fehlgeschlagene Versuch ist damit selbst fachlich relevante Information.

#### Risiko

- Nach dem Abbruch ist der In-Memory-Zustand nicht mehr identisch zum Zustand vor der Aktion.
- Ein späterer Ablauf kann den Zähler unbeabsichtigt mitspeichern.
- Die Semantik ist für Leser überraschend, wenn sie nicht ausdrücklich benannt wird.

#### Einsatzgrenze

Mutation vor einer abbrechenden Prüfung ist nur dann ein tragfähiges Muster, wenn der Versuch selbst fachlicher Zustand ist. Sie sollte lokal dokumentiert, im Ablauf sichtbar und hinsichtlich Abbruch und Persistenz bewusst behandelt werden. Für gewöhnliche Eingabevalidierung bleibt sie ein Anti-Pattern.


### Variante E: Dirty-Status nach Initialisierung zurücksetzen

#### Beobachtung

Ein anwendungsfallbezogener Service merkt sich den Dirty-Status eines ausgecheckten Graphen, reichert ihn mit Anzeige- und Hilfsinformationen an, sortiert oder normalisiert Teile und stellt danach den ursprünglichen Dirty-Status wieder her.

#### Zweck

Reine Initialisierung für die Oberfläche soll nicht wie eine Benutzeränderung wirken und nicht unnötig einen Check-in auslösen.

#### Risiko

Wenn die „Initialisierung“ doch persistent relevante Werte verändert, kann das Zurücksetzen eine echte Änderung verbergen. Das Muster greift zudem in einen technischen Mechanismus der Session ein und ist daher schwerer zu verstehen als eine saubere Trennung der Daten.

#### Einsatzgrenze

Der Dirty-Status darf nur für nachweislich nicht persistente Anreicherung zurückgesetzt werden. Präsentationseigenschaften oder DTOs sind vorzuziehen, sobald sie den Zweck ausreichend erfüllen. Fachliche Normalisierung, die gespeichert werden soll, darf nicht auf diese Weise unsichtbar gemacht werden.


### Variante F: Sequentielle statt gesammelte Validierung

#### Beobachtung

Das Projekt verwendet sehr viele einzelne Preconditions, aber vergleichsweise wenige Validierungsblöcke. Das bedeutet nicht, dass die Prüfungen falsch sind. Es zeigt eine starke Präferenz für fail-fast Abläufe.

#### Bewertung

- Fail-fast ist passend, wenn eine fehlende Voraussetzung alle weiteren Prüfungen sinnlos macht.
- Gesammelte Validierung ist besser, wenn mehrere unabhängige Eingabefehler zugleich angezeigt werden sollen.
- Warnings dürfen den Ablauf nach Bestätigung fortsetzen.

Die Wahl sollte nach Benutzernutzen und Abhängigkeit der Prüfungen erfolgen, nicht nach einem einheitlichen Stilzwang.


### Variante G: Unterstützte, aber nicht verwendete Listen-Joins

#### Beobachtung

Die Sprache dokumentiert Listen-Joins, das Projekt verwendet sie im untersuchten Stand jedoch nicht. Gleichzeitig sind Listen-Mappings vorhanden. Mapping einer Beziehung und Ladeweg der Beziehung bleiben also praktisch getrennt.

#### Bewertung

Für das Projekt ist die belastbare Konvention: Kindlisten über eigene Queries laden und explizit zuweisen. Ein neuer Listen-Join wäre keine bloße Fortsetzung vorhandener Praxis, sondern eine bewusste neue Variante und müsste hinsichtlich Ergebnismenge, Duplikaten und Verständlichkeit begründet werden.


### Variante H: Alte und neue Terminierungssemantik nebeneinander

#### Beobachtung

Nur ein kleiner Teil der Commands trägt die neue explizite Terminierungsoption. Gleichzeitig zeigen gerade Suchabläufe mit nachfolgender Bearbeitung, dass der sichtbare Termination Handler und Merge die Rückkehrlogik besser ausdrücken.

#### Bewertung

Der Bestand ist heterogen. Neue Abläufe sollten die explizite Semantik verwenden, wo Rückgabewerte, Merge oder mehrere Folgezustände relevant sind. Bestehende Abläufe sollten nur migriert werden, wenn sie ohnehin fachlich geändert werden oder die alte Form konkrete Verständnis- oder Wartungsprobleme verursacht.


## Verbindliche Leitlinien für neue Anwendungsfälle

Die Analyse legt folgende projektnahe Standardentscheidungen nahe:

1. **Am Geschäftsvorgang schneiden.** Commands, Pages, PagePanes, spezifische DTOs und Lesezugriffe gehören zusammen.
2. **Aggregatgrenze vor dem Checkout bestimmen.** Nur der für den Ablauf benötigte Graph wird geladen.
3. **Ladeplan sichtbar halten.** Beziehungen im Mapping nicht mit geladenen Beziehungen verwechseln.
4. **Kindlisten standardmäßig separat laden.** Ein Join ist eine begründungspflichtige Alternative, nicht die bestehende Konvention.
5. **Graph explizit speichern.** Parent, Kinder und weitere Bestandteile benötigen erkennbare Speicheroperationen.
6. **Search und Edit trennen.** Die Suche liefert ein Lesemodell; die Änderung beginnt mit einem Checkout.
7. **DTO als Standard für No-Key-Projektionen verwenden.** Entity-förmige Projektionen nur bewusst und strikt read-only einsetzen.
8. **Graph Owner besitzt die Transaktion.** Graph Edits verändern nur den bereits besessenen Graphen.
9. **Session Operations spät registrieren.** Erst nach erfolgreicher fachlicher Bearbeitung und Prüfung.
10. **Vor Mutation validieren.** Abweichungen nur, wenn der fehlgeschlagene Versuch selbst fachliche Bedeutung besitzt.
11. **Merge nach Rückkehr explizit modellieren.** Den von Merge gelieferten Wert verwenden.
12. **Page und PagePane trennen.** Die Page stellt Kontext und Aktionen bereit; das Pane visualisiert und bindet.
13. **Binding nicht als Ladeoperation behandeln.** Leere Daten zuerst am Repository- und Page-Kontext diagnostizieren.
14. **Successor nach Transaktionsabsicht wählen.** Gleiche Session nur dann fortsetzen, wenn beide Schritte fachlich zusammengehören.
15. **Servicezustand technisch begrenzen.** Kein Benutzer- oder Vorgangszustand in anwendungsweit instanzierten Services.
16. **Dirty-Status nicht pauschal korrigieren.** Nur nach eindeutig nicht persistenter Anreicherung zurücksetzen.


## Entscheidungstabelle

| Problem | Bevorzugtes Muster | Zu vermeidende Abkürzung |
| --- | --- | --- |
| Liste für Suche oder Auswertung | DTO plus read-only No-Key-Mapping | vollständigen bearbeitbaren Graphen laden |
| einzelne Entity bearbeiten | ID aus Suche, dann Checkout im Graph Owner | read-only Suchergebnis verändern |
| Aggregat mit Kindern laden | Root und Kinder explizit abfragen und verbinden | automatisches Lazy Loading erwarten |
| Aggregat speichern | Check-in mit sichtbarer Reihenfolge | Kaskadenspeicherung annehmen |
| Teil des geladenen Graphen bearbeiten | Graph Edit | eigenen Graph Owner mit zweiter Session verschachteln |
| Aktion ohne Benutzeroberfläche | seitenloser Graph Owner | Transaktionslogik in beliebigem Service verstecken |
| mehrere unabhängige Eingabefehler | Validation Block vor Mutation | nach jeder Teilmutation separat abbrechen |
| nächster Schritt in gleicher Transaktion | Successor | committen und Zustand erneut zusammensuchen |
| nächster Schritt erst nach Commit | Command nach Abschluss einreihen | Successor verwenden und verfrüht externe Wirkung erwarten |
| unterschiedliche Geräteansicht | alternatives PagePane zur selben Page | Fachablauf duplizieren |
| zwei Sichten auf dieselbe Liste | gemeinsame Selektion bewusst nutzen | parallele, unverbundene Auswahlzustände pflegen |
| temporäre Anzeigeinformation | DTO oder Präsentationseigenschaft | persistentes Domänenfeld ohne fachliche Bedeutung |
| anwendungsweiter Cache | kontrollierter technischer Servicezustand | benutzerbezogene Daten im Singleton-Service |


## Prüffragen bei Reviews

### Fachmodell und Graph

- Was ist die Root-Entity dieses Vorgangs?
- Welche Objekte sind enthalten, welche nur referenziert?
- Welche Teile des Graphen werden für genau diesen Ablauf benötigt?
- Sind Präsentationsinformationen klar von persistentem Zustand getrennt?

### Persistenz

- Ist für jede benötigte Liste und Referenz sichtbar, wie sie geladen wird?
- Werden Parent und Kinder mit ihren jeweiligen Mappings gespeichert?
- Ist ein Lesemodell tatsächlich read-only?
- Beginnt eine Änderung mit einem Checkout statt mit der Mutation eines Suchergebnisses?

### Command und Session

- Gibt es genau einen erkennbaren Besitzer von Session und Transaktion?
- Registriert ein Graph Edit versehentlich eigene Persistenzoperationen?
- Werden Session Operations erst im erfolgreichen Pfad wirksam?
- Entspricht Successor beziehungsweise nachgelagerter Command der gewünschten Commit-Grenze?

### Validierung

- Werden alle unabhängig prüfbaren Fehler vor der ersten Mutation ermittelt?
- Ist jede Mutation vor einer abbrechenden Prüfung fachlich beabsichtigt?
- Ist der Unterschied zwischen Warning und Fehler für den Ablauf klar?

### Oberfläche

- Stellt die Page alle benötigten Daten und Aktionen bereit?
- Beschränkt sich das PagePane auf Darstellung und Binding?
- Ist bei mehreren Tabellen klar, ob Auswahl geteilt oder getrennt sein soll?
- Wird eine leere Darstellung nicht vorschnell als Datenbankergebnis interpretiert?


## Nicht als allgemeines Muster zu verallgemeinern

Ein einzelner Fund ist noch keine Empfehlung. Insbesondere sollten folgende Beobachtungen nicht ohne Kontext kopiert werden:

- Entity-förmige Objekte aus einem No-Key-Mapping,
- manuelles Wiederherstellen des Dirty-Status,
- Mutation vor einer abbrechenden Precondition,
- technischer, veränderlicher Zustand in einem Service,
- direktes Hinzufügen einer Session Operation,
- das Einreihen eines Commands nach dem Abschluss.

Diese Formen sind dokumentierte Ausnahmen oder Spezialvarianten. Wer sie neu einsetzt, sollte die oben genannten Bedingungen explizit prüfen und die Entscheidung am Modell kenntlich machen.


## Zusammenfassung

Die prägende Architektur der Anwendung ist kein reines Schichtenmodell. Sie kombiniert ein stabiles fachliches Modell mit vertikalen Anwendungsfallschnitten. Änderungen laufen über explizit geladene und gespeicherte Objektgraphen; Suchen und Darstellungen verwenden überwiegend zweckgebundene read-only Modelle. Der Graph Owner bildet die Session- und Transaktionsgrenze, Graph Edits verändern lokale Teile des Graphen, und Page/PagePane trennen Ablaufkontext von Darstellung.

Die wichtigsten Abweichungen von vereinfachten Lehrregeln sind kontrollierte Varianten: anwendungsfallnahe Repositories, Entity-förmige Lesemodelle, technischer Servicezustand, das Zurücksetzen des Dirty-Status und in einem Prüffall eine absichtliche Mutation vor dem Abbruch. Gerade diese Abweichungen sind architektonisch relevant. Sie sollten nicht verborgen, aber auch nicht pauschal als Fehler bewertet werden. Entscheidend sind klare Lebenszyklus-, Session- und Persistenzgrenzen.
