# ObjectFlow (org.modellwerkstatt.objectflow) – Fachliches Modell, Services und Anwendungsabläufe

## Modellierungsumfang und Ausdrucksmöglichkeiten

`org.modellwerkstatt.objectflow` ist eine der drei domänenspezifischen Sprachen der **modellwerkstatt moware werkbank**. Sie beschreibt fachliche Datenstrukturen, Domänen- und Anwendungslogik sowie die Abläufe, in denen Benutzer, Batchjobs und Tests diese Logik ausführen. Persistenz wird mit ManMap beschrieben; die sichtbare Benutzeroberfläche und ausführbare Application- beziehungsweise Batchjob-Module werden mit DataUX modelliert.

ObjectFlow verbindet fünf Aufgabenbereiche:

1. **Datenmodellierung:** `Entity`, `Value Object` und `DTO` beschreiben fachliche Objekte, Werte und anwendungsbezogene Datencontainer.
2. **Domänenlogik:** Zustandsübergänge, Berechnungen und fachliche Prüfungen liegen in den Datenstrukturen selbst oder in zustandslosen `Service`-Komponenten.
3. **Anwendungsabläufe:** `Command`s koordinieren Parameter, Session, Pages, Conclusions und die Interaktion mit Services und Repositories.
4. **Tests:** `OFX Test Suit`s führen fachliche Tests und vollständige Commands ohne Benutzeroberfläche aus.
5. **Querschnitt:** Konfiguration, Rollen und Berechtigungen, statische Ressourcen, Logging und Serialisierung ergänzen die fachlichen Bausteine.

Im Folgenden bezeichnet **Name** die Bezeichnung, die in MPS typischerweise sichtbar ist oder eingegeben wird. Der **Konzeptname** ist die technische AST-Bezeichnung und steht jeweils in Klammern. Bei einem ObjectFlow-Konzept genügt dort der kurze Konzeptname; gehört das angesprochene Konzept zu einer anderen DSL, steht in Klammern dessen **FQ-Name**. Die Konzepttabellen führen FQ-Namen zusätzlich explizit auf – primär für KI-Agenten.

Die Dokumentation beschreibt beobachtete und technisch bestätigte Praxis. Sie legt keine zusätzliche, von der Sprache nicht erzwungene Architektur fest. Wo sich aus bestehenden Anwendungen wiederkehrende Empfehlungen ergeben, werden diese als solche benannt.


## Teil I – Fachliche Datenmodellierung

### Entity, Value Object und DTO

Die drei rootfähigen Datenstrukturen besitzen Business Properties und können zusätzlich BaseLanguage-Member wie Konstruktoren und Methoden enthalten.

| Name | Konzeptname | Primärer Zweck | Identität und Lebenszyklus |
| --- | --- | --- | --- |
| `Entity` | `Entity` | Fachliches Objekt, das typischerweise über ManMap persistiert und innerhalb einer Session bearbeitet wird | Besitzt eine fachliche oder technische Identität; Gleichheit wird nicht nur aus allen Werten abgeleitet |
| `Value Object` | `ValueObject` | Zusammengesetzter fachlicher Wert, beispielsweise Geldbetrag oder zusammengesetzter Schlüssel | Keine eigenständige Entity-Identität; ausgewählte Properties können die Wertgleichheit bestimmen |
| `DTO` | `DTO` | Datencontainer für Suche, Darstellung, Aggregation oder Übergabe zwischen Abläufen | Nicht selbst als persistentes Domänenobjekt gedacht; konkretes Read-only- und Session-Verhalten hängt von seiner Erzeugung ab |

Eine `Entity` wird nicht allein durch ihre ObjectFlow-Deklaration persistent. Tabellen, Schlüssel, Referenzen und Speicheroperationen werden mit `org.modellwerkstatt.manmap` beschrieben. Umgekehrt darf ein DTO fachliche Methoden besitzen, bleibt aber ein anwendungsbezogener Datencontainer und wird nicht über ein normales Entity-Mapping zurückgespeichert.

Ein durch ein ManMap-`nokeystore/read-only map` erzeugtes DTO ist read-only und liegt außerhalb der Session-Identity-Map. Ein innerhalb eines Commands neu erzeugtes DTO unterliegt nicht automatisch dieser Einschränkung. Herkunft und beabsichtigte Verwendung sind deshalb bei DTOs wichtiger als der Klassenname allein.

### Business Properties

Eine Business Property (`BusinessProperty`) besteht mindestens aus Name, Typ und Property-Implementierung. Zusätzlich können Kurz- und Langbeschreibung, Zahlenformat, Dokumentation, Sichtbarkeit sowie ManMap-Feldoptionen modelliert werden.

| Bestandteil | Rolle |
| --- | --- |
| Name | Fachlicher und technischer Property-Name |
| Typ | BaseLanguage- beziehungsweise ObjectFlow-Typ der Property |
| Kurzbeschreibung | Kompakte, von Oberflächen verwendbare Beschriftung |
| Langbeschreibung | Ausführlichere Beschreibung für Darstellung und Dokumentation |
| Zahlenformat | Standardformat für numerische Darstellungen |
| Property-Optionen | ManMap-Optionen wie `key`, `autoid`, Audit-, Größen- oder Indexhinweise |

Typische Property-Typen sind primitive Werte, `string`, `BigDecimal`, Datum/Zeit-Typen, Status, Value Objects, Referenzen auf Entities beziehungsweise DTOs und Listen geeigneter Elementtypen. Der in ObjectFlow verwendete Typ `string` ist nicht mit einer manuell modellierten Verwendung von `java.lang.String` gleichzusetzen. Dezimalliterale werden in MPS beispielsweise als `13.44bd` eingegeben.

Persistenzoptionen an einer Business Property gehören fachlich zur Datenstruktur, werden technisch aber von ManMap ausgewertet. Ihre genaue Wirkung ist deshalb in [manmap.md](manmap.md) beschrieben.

### Beziehungen und Objektgraphen

Eine Property kann ein anderes fachliches Objekt oder eine Liste solcher Objekte referenzieren. ObjectFlow beschreibt damit den fachlichen Graphen; es lädt ihn jedoch nicht automatisch aus einer Datenbank. ManMap-Repositories entscheiden explizit, welche Referenzen und Listen geladen werden.

Für die Bearbeitung ist die Aggregatgrenze wichtig: Revert, Session-Integration und Speichern beziehen sich auf die tatsächlich in der Session vorhandenen Objekte. Eine deklarierte, aber nicht geladene Beziehung ist nicht automatisch Teil des bearbeiteten Graphen.

### Value-Object-Gleichheit

Ein `Value Object` kann über `equal properties` (`EqualPropertyReference`) festlegen, welche seiner Business Properties die Wertgleichheit bestimmen. Das ist insbesondere für zusammengesetzte Schlüssel und fachliche Werte nützlich. Die ausgewählten Properties sollen gemeinsam den fachlichen Wert repräsentieren; technische oder nur darstellungsbezogene Properties gehören üblicherweise nicht dazu.

### Status

Ein Status (`StatusDeclaration`) deklariert eine benannte Menge von Statuselementen (`StatusElement`). Ein Statuselement besitzt einen technischen Persistenzwert sowie Kurz- und Langbeschreibung. Statuswerte können als Property-Typ verwendet, verglichen, in SQL referenziert und durch DataUX mit Beschriftung und Farbe dargestellt werden.

Wichtige Ausdrucksmittel sind:

| Name | Konzeptname | Bedeutung |
| --- | --- | --- |
| Status | `StatusDeclaration` | Deklariert die erlaubten Werte eines fachlichen Status |
| Statuselement | `StatusElement` | Einzelner Status mit Persistenzwert und Beschreibungen |
| Status-Typ | `StatusType` | Verwendet einen deklarierten Status als Property- oder Variablentyp |
| `of` | `StatusOfOperator` | Prüft, ob ein Wert einem oder mehreren Statuselementen entspricht |
| `fromDbValue` | `StatusFromDbValue` | Ermittelt ein Statuselement aus seinem Datenbankwert |

Statusoptionen unterstützen unter anderem einen Initialwert bei der Objekterzeugung (`ON_CREATION`), eine Standardfarbe (`COLOR`) und die Behandlung leerer oder unbekannter Persistenzwerte. Solche Fallbacks sollten bewusst gewählt werden: Ein unbekannter Datenbankwert kann auf einen Daten- oder Versionsfehler hinweisen und darf nicht versehentlich als normaler fachlicher Zustand erscheinen.

### Formatierte Strings

Der formatierte ObjectFlow-String (`StringFormatString`) verbindet einen Formattext mit typisierten Werten. Er wird unter anderem für Meldungen, Titel, Beschreibungen und Logging verwendet. Die Formatierung berücksichtigt die von der Laufzeit bereitgestellten Konventionen für Zahlen, Status- sowie Datums- und Zeitwerte.

Formatierung ist von fachlicher Berechnung zu trennen. Ein Geldbetrag wird beispielsweise fachlich als Dezimalwert beziehungsweise Value Object berechnet; erst für Meldung oder Oberfläche wird er formatiert.

### Methoden an Datenstrukturen

Entities, Value Objects und DTOs können BaseLanguage-Konstruktoren und -Methoden enthalten. Wiederkehrende objektbezogene Regeln können dadurch nahe an den betroffenen Daten liegen. In bestehenden Anwendungen werden Methoden beispielsweise für Berechnungen, Zustandsabfragen sowie das konsistente Hinzufügen oder Entfernen von Elementen eines Aggregats verwendet.

Logik, die mehrere Aggregate, Repositories oder andere Komponenten benötigt, wird dagegen typischerweise in einem Service gebündelt.


## Teil II – Services und Domänenlogik

### Service-Komponenten

Ein `Service` (`Service`) ist eine von der Laufzeit verwaltete Komponente. Services werden über die ObjectFlow-Konfiguration verdrahtet und innerhalb einer Anwendung typischerweise einmal instanziiert. Sie sind deshalb grundsätzlich zustandslos zu behandeln: Aufrufübergreifender, benutzer- oder sessionbezogener Zustand gehört nicht in Service-Felder.

Services bündeln vor allem:

- fachliche Operationen über mehrere Objekte,
- Zustandsübergänge und dazugehörige Prüfungen,
- wiederverwendbare Berechnungen,
- die Koordination mehrerer Repositories oder anderer Services,
- Logik, die sowohl aus UI-Commands als auch aus Jobs und Tests benötigt wird.

Die beobachtete Abgrenzung lautet:

- Eine grundsätzlich gültige Domänenregel kann in einer Entity, einem Value Object oder Service liegen.
- Eine Prüfung, die zu einer Service-Operation gehört und in allen Aufrufkontexten gelten soll, kann als Precondition der Service Method modelliert werden.
- Eine rein use-case- oder interaktionsbezogene Prüfung gehört in den Command beziehungsweise seine Page Conclusion.
- Ein Command koordiniert Ablauf und Session; er soll wiederverwendbare Domänenlogik nicht duplizieren.

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
| Dafür vorgesehener Aufruf in `FINAL_CANCEL` | Wird als Cancel-/Marker- beziehungsweise Journal-Operation in dem dafür vorgesehenen Transaktionskontext behandelt |

Für normale fachliche Aufrufe ist `OperationCall` zu verwenden. Ein direkter Java-Aufruf würde die Komponenten-, Session- und Transaktionssemantik umgehen.

### Explizite Session Operations

Mit `session operation add` (`SessionOperationAdd`) kann ein `OperationCall` ausdrücklich auf dem Operation Stack der aktuellen Session registriert werden. Der Aufruf wird dabei noch nicht ausgeführt.

Das hat zwei wichtige Konsequenzen:

1. Ein Rückgabewert oder eine durch den späteren Aufruf vorgenommene Änderung ist direkt nach `session operation add` noch nicht verfügbar.
2. Wird beispielsweise beim späteren Insert eine Entity-ID vergeben, kann diese ID nicht unmittelbar nach der Registrierung ausgegeben oder verwendet werden.

Service Methods mit `TO_SESSION_OPS` und passende ManMap-`CHECKIN`-/`DELETE`-Methoden übernehmen diese Registrierung automatisch, wenn sie in dem dafür vorgesehenen Kontext per `OperationCall` aufgerufen werden.

### Preconditions, Validation, Guards und Exceptions

ObjectFlow unterscheidet fachlich beziehungsweise für den Benutzer behandelbare Probleme von unerwarteten Systemzuständen.

| Mechanismus | Zweck | Wirkung im Command-Ablauf |
| --- | --- | --- |
| Precondition (`Precondition`) | Verständliche, grundsätzlich korrigierbare Voraussetzung | Stoppt außerhalb einer `validation` den aktuellen Programmfluss; die Meldung wird in der UI angezeigt |
| `validation` (`ValidationStatement`) | Mehrere Voraussetzungen gemeinsam prüfen | Führt die enthaltenen Prüfungen aus und sammelt alle verletzten Preconditions in einem Problembericht |
| `guard` (`Guard`) | Unerwarteten beziehungsweise nicht durch den Benutzer korrigierbaren Zustand absichern | Beendet den Command in `FINAL_CANCEL`; Benutzer erhalten eine neutrale Systemmeldung, Entwickler Diagnoseinformationen und Stacktrace |
| Exception | Technischer Ausnahmefall | Beendet den betroffenen Command in `FINAL_CANCEL` |

Eine Precondition kann zusätzlich einen Command als Korrekturaktion anbieten. Nach einer fehlgeschlagenen Prüfung kann der Benutzer dadurch über ein Menü eine Reparatur ausführen oder eine andere Page Conclusion wählen.

Ein Guard in einem `GRAPH_EDIT_CMD` besitzt ein besonderes Eskalationsverhalten: Er beendet nicht nur den Child-Command, sondern auch den zugehörigen Session Owner. Für den Endanwender erscheint sinngemäß die Meldung „Das Kommando konnte am System nicht ausgeführt werden“. Die technischen Details bleiben für Entwickler und Betrieb sichtbar. Eine normale Exception im `GRAPH_EDIT_CMD` besitzt dieses besondere Eskalationsverhalten nicht.

Ein häufiges Muster für ändernde Domänenlogik lautet:

1. Benötigte Fakten und Konfiguration laden.
2. Alle fachlichen Voraussetzungen in einem `validation`-Block prüfen.
3. Erst nach erfolgreicher Validation den fachlichen Graphen verändern.


## Teil III – Commands und Anwendungsabläufe

### Die vier Command-Typen

Ein `Command` (`Command`) beschreibt einen Anwendungsfall oder einen Teil einer Benutzerinteraktion. Der Command-Typ bestimmt vor allem Eigentum und Abschluss der Session.

| Sichtbarer Typ | Session | Abschluss und Persistenz | Typischer Einsatz |
| --- | --- | --- | --- |
| `SEARCH_CMD` | Startet eine eigene Session | `FINAL_OK` beendet die Session ohne Commit; registrierte Session Operations werden nicht ausgeführt | Suche, Anzeige, Filterung und Read-only-Auswertung |
| `GRAPH_OWNER_CMD` | Startet eine eigene Session und besitzt den bearbeiteten Graphen | Bei `FINAL_OK` werden Session Operations in einer Transaktion ausgeführt und committed | Bearbeitung eines vollständigen fachlichen Graphen |
| `GRAPH_EDIT_CMD` | Übernimmt die Session seines Performers | Besitzt keinen eigenen Commit; erfolgreicher Abschluss kehrt zum Owner zurück | Teilbearbeitung und Benutzerinteraktion innerhalb eines vorhandenen Graphen |
| `MODAL_GRAPH_OWNER_CMD` | Wie `GRAPH_OWNER_CMD`: eigene Session | Wie `GRAPH_OWNER_CMD`: eigener Commit bei `FINAL_OK` | Eigenständige Bearbeitung in einer modalen UI |

`MODAL_GRAPH_OWNER_CMD` unterscheidet sich fachlich und transaktional nicht vom normalen Graph Owner. Nur die Oberfläche ist modal.

Ein `GRAPH_EDIT_CMD` kann technisch Session Operations registrieren. Diese werden bei einem Abbruch des Child-Commands jedoch nicht wieder vom Operation Stack entfernt. In der beobachteten Praxis sollen `GRAPH_EDIT_CMD`s deshalb keine Session Operations registrieren; der Session Owner übernimmt deren Registrierung.

### Aufbau eines Commands

Ein Command kann folgende Bestandteile enthalten:

| Bestandteil | Aufgabe |
| --- | --- |
| Parameter und Defaults | Eingaben des Aufrufs; Defaults können aus Selektion oder Konstanten entstehen |
| `generally enabled` | Zusätzliche Bedingungen für die Verfügbarkeit einer Command-Aktion |
| Permissions | Erforderliche Rollen beziehungsweise Zugriffsart |
| Preconditions | Voraussetzungen vor Beginn des Ablaufs |
| Lokale Variablen | Zustand innerhalb der Command-Ausführung |
| Command Settings | Label, Icon, Hotkey, Farbe, Revert-Objekte, Locks und Optionen |
| `command init` | Initialisierung; wird vor der ersten Page ausgeführt |
| Pages | Interaktionsschritte mit Page Init, Bindung, Conclusions und UI-Zuordnung |
| `FINAL OK_CONCLUSION` | Erfolgreicher Command-Abschluss |
| `FINAL CANCEL_CONCLUSION` | Fachlicher oder technischer Abbruch |
| `FINAL_USER_CANCEL` | Expliziter Abbruch durch den Benutzer |

### Parameter, Defaults und Selektion

Command-Parameter können beim Aufruf explizit gesetzt oder über Default-Ausdrücke belegt werden. Häufig verwendete Ausdrücke sind `getSelected()` (`SelectedObject`) und `getSelectedObjects()` (`SelectedList`). Sie beziehen sich auf die aktuelle Selektion des Aufrufkontexts. Eine abgeleitete Selektion kann auch Subtypen berücksichtigen.

Die Verfügbarkeit einer Aktion hängt sowohl von passenden Argumenten und Selektionen als auch von `generally enabled`, Permissions und gegebenenfalls UI-spezifischen Bedingungen ab. Ein Default ersetzt keine Prüfung auf einen fachlich zulässigen Aufruf.

### Command Init und Hintergrundinitialisierung

`command init` bereitet Variablen und Daten für den folgenden Ablauf vor. Mit der Option `IN_BACKGROUND` wird ausschließlich dieses `command init` im Hintergrund ausgeführt. Pages und der weitere Interaktionsablauf werden dadurch nicht allgemein zu einem Hintergrundjob.

Preconditions sollen vor fachlichen Änderungen geprüft werden. In Page Init sollen grundsätzlich keine abbrechenden Preconditions verwendet werden; Warnungen können dagegen Feedback geben, ohne den Ablauf zu zerstören.

### Pages und Page Conclusions

Eine Page (`PageCrtl`) beschreibt einen Interaktionsschritt des Commands. Sie kann:

- an eine Entity oder ein DTO gebunden sein,
- im Page Init Daten laden beziehungsweise bereitstellen,
- dynamische Titel und Untertitel berechnen,
- Scopes bereitstellen,
- ein oder mehrere DataUX-`Page Pane`s auswählen,
- auf beendete Child-Commands reagieren,
- branching Commands anbieten,
- mehrere Page Conclusions definieren.

Eine normale Page Conclusion beendet nicht zwangsläufig den gesamten Command. Sie kann Editorwerte in die gebundenen Objekte übernehmen, Logik ausführen, die aktuelle Page neu initialisieren, zu einer anderen Page wechseln oder schließlich eine finale Conclusion auslösen.

Page und `Page Pane` haben getrennte Verantwortlichkeiten: ObjectFlow beschreibt Daten und Ablauf, DataUX die sichtbare Darstellung und Menüs.

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

Dieses Konzept eignet sich für einen Folgeablauf, der einen bereits erfolgreich persistierten Zustand benötigt.

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

Commands können erforderliche Rollen deklarieren. Die Projektion unterscheidet insbesondere lesenden und ändernden Zugriff. Rollen sind hierarchisch modellierbar: Eine übergeordnete Rolle kann die Fähigkeiten einer weiteren Rolle einschließen.

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
- **Session Operation mit unmittelbarem Aufruf verwechseln:** Nach der Registrierung sind Rückgabewerte und beim Speichern erzeugte IDs noch nicht vorhanden.
- **Session Operations im `GRAPH_EDIT_CMD` registrieren:** Sie bleiben auch nach einem Child-Abbruch im Stack. Die Registrierung gehört üblicherweise in den Session Owner.
- **Commit bei `SEARCH_CMD` erwarten:** Seine Session wird auch nach `FINAL_OK` nicht committed.
- **`MODAL_GRAPH_OWNER_CMD` für einen Graph Edit halten:** Er besitzt wie ein normaler Graph Owner eine eigene Session und einen eigenen Commit.
- **Precondition, Guard und Exception gleich behandeln:** Preconditions sind korrigierbare Benutzerprobleme; Guards und Exceptions beenden den Command technisch. Ein Guard im Graph Edit eskaliert zusätzlich zum Owner.
- **Mehrere Preconditions ohne `validation` sammeln wollen:** Außerhalb des Blocks stoppt bereits die erste verletzte Precondition den Programmfluss.
- **Precondition an einer `TO_SESSION_OPS`-Methode definieren:** Die Laufzeit lehnt dies ab.
- **Revert als Datenbank-Rollback verstehen:** Revert stellt kopierte In-Memory-Objekte wieder her; die Check-in-Transaktion wurde bei einem normalen Abbruch noch nicht begonnen.
- **Nur ein Kindobjekt statt der Graph-Wurzel für Revert auswählen:** Dann wird nicht automatisch der vollständige Aggregatgraph zurückgesetzt.
- **Dieselbe Entity erneut auschecken:** Mit `session entities` beziehungsweise den Schlüsselvarianten zuerst die bestehende Session prüfen.
- **Automatisches Merge im neuen Termination-Modus erwarten:** Gepushte Objekte müssen explizit übernommen, gemergt und gegebenenfalls selektiert werden.
- **`session queue next command` ohne UI verwenden:** Tests und Jobs ignorieren diesen Mechanismus.
- **`IN_BACKGROUND` als Hintergrundausführung des gesamten Commands verstehen:** Nur `command init` läuft im Hintergrund.
- **URL-Parameter nicht in den Command-Kontext pushen:** Nach der Initialisierung stehen sie sonst nicht wie normale Command-Parameter für den Ablauf bereit.
- **UI-Logik und Domänenlogik vermischen:** Darstellung gehört nach DataUX; wiederverwendbare fachliche Regeln gehören in Datenstrukturen oder Services.
- **Name und Konzeptname verwechseln:** Name, Konzeptname und FQ-Name nach der eingangs festgelegten Schreibweise unterscheiden.


## Konzeptindex für Agenten

Der Index enthält die in dieser Dokumentation behandelten wichtigen Konzepte, nicht alle Konzepte der Sprache. Für JSON-Blueprints sind die FQ-Namen zu verwenden. Vor einer Modelländerung müssen Referenzen, Child-Roles und Kardinalitäten über MPS MCP im aktuellen Projekt aufgelöst werden.

| Themenbereich | Name | Konzeptname | FQ-Name |
| --- | --- | --- | --- |
| Datenstruktur | `Entity` | `Entity` | `org.modellwerkstatt.objectflow.structure.Entity` |
| Datenstruktur | `Value Object` | `ValueObject` | `org.modellwerkstatt.objectflow.structure.ValueObject` |
| Datenstruktur | `DTO` | `DTO` | `org.modellwerkstatt.objectflow.structure.DTO` |
| Datenstruktur | Business Property | `BusinessProperty` | `org.modellwerkstatt.objectflow.structure.BusinessProperty` |
| Datenstruktur | equal property | `EqualPropertyReference` | `org.modellwerkstatt.objectflow.structure.EqualPropertyReference` |
| Status | Status | `StatusDeclaration` | `org.modellwerkstatt.objectflow.structure.StatusDeclaration` |
| Status | Statuselement | `StatusElement` | `org.modellwerkstatt.objectflow.structure.StatusElement` |
| Status | Status-Typ | `StatusType` | `org.modellwerkstatt.objectflow.structure.StatusType` |
| Status | `of` | `StatusOfOperator` | `org.modellwerkstatt.objectflow.structure.StatusOfOperator` |
| Status | `fromDbValue` | `StatusFromDbValue` | `org.modellwerkstatt.objectflow.structure.StatusFromDbValue` |
| Formatierung | formatierter String | `StringFormatString` | `org.modellwerkstatt.objectflow.structure.StringFormatString` |
| Service | `Service` | `Service` | `org.modellwerkstatt.objectflow.structure.Service` |
| Service | service method | `ServiceInstanceMethodDeclaration` | `org.modellwerkstatt.objectflow.structure.ServiceInstanceMethodDeclaration` |
| Serviceoption | `API_METHOD` | `SimdApiMethod` | `org.modellwerkstatt.objectflow.structure.SimdApiMethod` |
| Serviceoption | `TO_SESSION_OPS` | `SimdToSessionOps` | `org.modellwerkstatt.objectflow.structure.SimdToSessionOps` |
| Komponentenaufruf | `#` | `OperationCall` | `org.modellwerkstatt.objectflow.structure.OperationCall` |
| Prüfung | precondition | `Precondition` | `org.modellwerkstatt.objectflow.structure.Precondition` |
| Prüfung | validation | `ValidationStatement` | `org.modellwerkstatt.objectflow.structure.ValidationStatement` |
| Prüfung | guard | `Guard` | `org.modellwerkstatt.objectflow.structure.Guard` |
| Command | `Command` | `Command` | `org.modellwerkstatt.objectflow.structure.Command` |
| Command | Parameter | `ContainerParameter` | `org.modellwerkstatt.objectflow.structure.ContainerParameter` |
| Command | Variable | `ContainerVariable` | `org.modellwerkstatt.objectflow.structure.ContainerVariable` |
| Command | Page | `PageCrtl` | `org.modellwerkstatt.objectflow.structure.PageCrtl` |
| Command | Page Conclusion | `PageConclusion` | `org.modellwerkstatt.objectflow.structure.PageConclusion` |
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
