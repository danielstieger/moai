# ManMap (org.modellwerkstatt.manmap) - Persistenz und Lesemodelle

## Modellierungsumfang und Ausdrucksmöglichkeiten

`org.modellwerkstatt.manmap` ist eine der drei domänenspezifischen Sprachen der **modellwerkstatt moware werkbank** und dient der Modellierung des relationalen Datenzugriffs. Sie unterstützt zwei grundlegende Zugriffsarten: das Laden und Speichern des fachlichen Domänenmodells sowie die Bereitstellung gezielter Lesemodelle. (Im Folgenden bezeichnet **Name** die Bezeichnung, die in MPS typischerweise sichtbar ist oder eingegeben wird; der **Konzeptname** ist die technische AST-Bezeichnung und steht jeweils in Klammern. Der **FQ-Name** wird in den Konzepttabellen ergänzt - primär für KI-Agenten)

**Domänenmodell: Entitäten laden, bearbeiten und speichern.** `Entity-Mappings` (`EntityMapping`) innerhalb einer `Persistence Description` (`PersistenceDescription`) beschreiben die Abbildung zwischen Entitäten und dem relationalen Tabellenmodell. Sie ordnen die Eigenschaften einer Entität den Spalten der zugehörigen Datenbanktabelle zu. Repository-Methoden verwenden diese Mappings, um Entitäten zu laden und zusammengehörige Entitäten und Value Objects zu fachlichen Objektgraphen zusammenzustellen. Diese Graphen können verarbeitet, verändert und wieder gespeichert werden. Die Persistenzoperationen begleiten damit den Lebenszyklus der fachlichen Objekte. Umfang und Ablauf des Ladens werden explizit beschrieben; automatisches Lazy Loading findet nicht statt.

**Lesemodelle: Informationen gezielt abfragen und verwenden.** Benutzerdefinierte SQL-Abfragen liefern die Informationen, die für eine Suche, Darstellung oder Auswertung benötigt werden. `row mapper` (`RowMapperField`) beziehungsweise `nokeystore/read-only map` (`NoKeyMapperField`) überführen die Ergebnismengen in DTOs. Diese Lesemodelle können ausgewählte Felder, Informationen aus mehreren Tabellen oder direkt in der Datenbank berechnete Aggregationen enthalten. Sie werden für den jeweiligen Anwendungsfall geladen, verwendet und anschließend verworfen. Ein Zurückspeichern über das Lesemodell ist nicht vorgesehen.

**Zusammenwirken beider Zugriffsarten.** Beide Zugriffsarten werden in Repositories gekapselt und können innerhalb einer Anwendung kombiniert werden. Das Domänenmodell trägt die fachlichen Daten und ihr Verhalten und bildet die Grundlage für Änderungen. Lesemodelle stellen bedarfsgerecht aufbereitete Informationen bereit. Über enthaltene Identifikatoren kann bei Bedarf vom Lesemodell zum gezielten Laden der zugehörigen fachlichen Objekte übergegangen werden.





## Die zwei Zugriffswege im Überblick

| Fragestellung | Domänenmodell | Lesemodell / Custom SQL |
| --- | --- | --- |
| Primärer Zweck | Entitäten laden, bearbeiten, speichern und löschen | Suchlisten, Darstellungen, Auswertungen und direkte SQL-Operationen |
| Einstieg | `Entity-Mapping` (`EntityMapping`) in einer `Persistence Description` (`PersistenceDescription`) | `SQL` (`C2SqlBlock`) in einer Repository-Methode |
| Lesen | `get`/`where` auf einem Mapping (`QueryFromMap`) | `SQL` (`C2SqlBlock`) mit `sqlType=QUERY` |
| Schreiben | `save with` (`SaveWithMap`) und `delete with` (`DeleteWithMap`) | `SQL` (`C2SqlBlock`) mit `sqlType=STATEMENT` |
| Ergebnis | Entity beziehungsweise explizit aufgebauter Objektgraph | Skalarer Wert oder per Row-Mapper erzeugtes Objekt, häufig ein DTO |
| Session-Verhalten | Ergebnisse von `get`/`where` auf einem Mapping (`QueryFromMap`) werden in die ObjectFlow-Session integriert. | Ergebnisse von `nokeystore/read-only map` (`NoKeyMapperField`) sind read-only und nicht in die Session-Identity-Map integriert. |
| Lebensdauer | Begleitet einen fachlichen Bearbeitungs- und Speicherablauf | Wird für den Anwendungsfall geladen, verwendet und verworfen |


## Repositories und die vier Methodenarten

Ein `Repository` (`Repository`) bündelt den Datenbankzugriff. Es kann Repository-Methoden, Row-Mapper, No-Key-Mapper und einen im ganzen Repository sichtbaren `sql string` (`SqlStringField`) enthalten. Wie bei einer BaseLanguage-Klasse kann ein `Repository` auch ein Field enthalten. Repositories sind jedoch grundsätzlich als zustandslos zu betrachten und werden pro Applikation nur einmal instanziert.

Die Repository-Methoden interagieren mit einer laufenden Session. Das Command-Konzept der `org.modellwerkstatt.objectflow`-DSL verantwortet den Lebenszyklus der Session und der Datenbanktransaktion. ManMap bestimmt, wie Abfrageergebnisse in diese Session integriert werden und ob sie read-only oder veränderbar sind. Eine Repository-Methode ist deshalb nicht automatisch eine eigene Transaktionsgrenze. Eine Session Operation registriert einen später auszuführenden Repository-Aufruf, beispielsweise eine `CHECKIN`- oder `DELETE`-Methode. Im üblichen Command-Ablauf sammelt der Session Owner diese Operationen während der Bearbeitung. Erst beim vorgesehenen erfolgreichen Abschluss werden sie innerhalb der Datenbanktransaktion ausgeführt und anschließend committed. Bei Abbruch werden die vorgesehenen Speicheroperationen nicht ausgeführt. Das Registrieren einer Session Operation ist daher von ihrem Ausführen zu unterscheiden. Ein Aufruf einer Repository-Methode im Modell eröffnet nicht automatisch eine eigene Transaktion.

### Konzeptlandkarte

| Name | Konzeptname | FQ-Name | Rolle |
| --- | --- | --- | --- |
| `Repository` | `Repository` | `org.modellwerkstatt.manmap.structure.Repository` | Root Node für Datenbankzugriff und Mapper |
| `repo method` | `RepositoryInstanceMethodDeclaration` | `org.modellwerkstatt.manmap.structure.RepositoryInstanceMethodDeclaration` | Repository-Methode mit `repoMethodType` |
| `row mapper` | `RowMapperField` | `org.modellwerkstatt.manmap.structure.RowMapperField` | Wiederverwendbare Closure zur Konvertierung einer SQL-Zeile |
| `nokeystore/read-only map` | `NoKeyMapperField` | `org.modellwerkstatt.manmap.structure.NoKeyMapperField` | Read-only-Mapping für Ergebnisse ohne verwendbaren Schlüssel |
| `sql string` | `SqlStringField` | `org.modellwerkstatt.manmap.structure.SqlStringField` | Benannter, innerhalb des Repositorys wiederverwendbarer SQL-Text |

Die Property `repoMethodType` besitzt genau vier Werte:

| Methodenart | Zweck | Typische Operationen | Beziehung zur Session |
| --- | --- | --- | --- |
| `READONLY` | Daten ohne beabsichtigte Änderung laden | `get`/`where` auf einem Mapping (`QueryFromMap`) mit `ReadOnly`, Custom-SQL-Query | Gemappte Entitäten sind read-only; No-Key-Ergebnisse liegen außerhalb der Identity-Map. |
| `CHECKOUT` | Entitäten zur Bearbeitung laden oder erneut laden | `get`/`where` auf einem Mapping (`QueryFromMap`) mit `Checkout`, `reload` (`ReloadQuery`) | Geladene Entitäten werden veränderbar in die Session integriert. |
| `CHECKIN` | Änderungen speichern | `save with` (`SaveWithMap`) | Wird typischerweise als Session Operation registriert und beim erfolgreichen Abschluss ausgeführt. Auch Custom-SQL vom Typ Statement, wenn dieses DB-Änderungen vornimmt und in einer Transaktion ausgeführt werden soll! |
| `DELETE` | Geladene Entitäten löschen | `delete with` (`DeleteWithMap`) | Wird typischerweise als Session Operation registriert; abhängige Objekte müssen explizit behandelt werden. |

Der Methodentyp beschreibt die Rolle der Methode im Lebenszyklus. Er ersetzt nicht die konkrete Wahl von `ReadOnly` oder `Checkout` bei jeder Abfrage mit `get`/`where` auf einem Mapping (`QueryFromMap`) und erzeugt keine automatische Graph- oder Transaktionssemantik.

### Read-only, Checkout und Session-Identität

Ergebnisse von `get`/`where` auf einem Mapping (`QueryFromMap`) werden in die Identity-Map der laufenden ObjectFlow-Session integriert. Wiederholte Read-only-Abfragen auf dieselbe Entity verwenden innerhalb dieser Session dieselbe Objektidentität. Wird versucht, eine bereits read-only oder veränderbar geladene Entity erneut auszuchecken, wirft ManMap eine `IllegalStateException`; stattdessen ist die bereits in der Session vorhandene Instanz zu verwenden.

Read-only schützt eine Entity nicht erst beim Speichern: Bereits eine Änderung oder das Löschen des Objekts ist unzulässig. Ein durch ein `nokeystore/read-only map` (`NoKeyMapperField`) erzeugtes Ergebnis ist ebenfalls read-only, liegt selbst aber außerhalb der Session-Identity-Map. Reguläre Entities, die über Joins eines solchen No-Key-Mappings geladen werden, können dagegen in die Session integriert sein.

### Wiederverwendbarer SQL-Text

Ein `sql string` (`SqlStringField`) benennt einen wiederverwendbaren SQL-Text, der im gesamten Repository sichtbar ist. Er eignet sich für SQL-Fragmente, die von mehreren Repository-Methoden verwendet werden sollen; das Repository bleibt dabei zustandslos.



## `Persistence Description` (`PersistenceDescription`) und Mapping-Möglichkeiten

`Persistence Description` (`PersistenceDescription`) und `Repository` (`Repository`) sind die beiden rootfähigen ManMap-Konzepte. Eine `Persistence Description` (`PersistenceDescription`) gruppiert `Entity-Mapping` (`EntityMapping`)-Knoten. Jedes `Entity-Mapping` (`EntityMapping`) verbindet eine ObjectFlow-Klasse mit einer relationalen Tabelle und enthält die atomaren Mappings ihrer Eigenschaften und Beziehungen.

### Konzeptlandkarte

| Name | Konzeptname | FQ-Name | Aufgabe |
| --- | --- | --- | --- |
| `Persistence Description` | `PersistenceDescription` | `org.modellwerkstatt.manmap.structure.PersistenceDescription` | Gruppiert die Entity-Mappings eines Modells. |
| `Entity-Mapping` | `EntityMapping` | `org.modellwerkstatt.manmap.structure.EntityMapping` | Referenziert die Klasse, benennt die Tabelle und enthält Mapping-Elemente. |
| `Feld-Mapping` | `FieldMapping` | `org.modellwerkstatt.manmap.structure.FieldMapping` | Ordnet eine Property einer Spalte und optionalen Feldoptionen zu. |
| `Referenz-Mapping` | `ReferenceMapping` | `org.modellwerkstatt.manmap.structure.ReferenceMapping` | Mappt den Fremdschlüssel einer Objektbeziehung, einer Referenz zu einer anderen Entität |
| eingebettetes Mapping | `EmbeddedMapping` | `org.modellwerkstatt.manmap.structure.EmbeddedMapping` | Mappt Properties eines eingebetteten Value Objects. |
| `Listen-Mapping` | `ListMapping` | `org.modellwerkstatt.manmap.structure.ListMapping` | Beschreibt eine Listenbeziehung über ein Rückreferenz- oder Schlüsselmapping. |
| Mapping einbinden | `IncludeMapping` | `org.modellwerkstatt.manmap.structure.IncludeMapping` | Verwendet ein geeignetes bestehendes Mapping erneut. |

### Aufbau eines `Entity-Mappings` (`EntityMapping`)

Ein `Entity-Mapping` (`EntityMapping`) besitzt mindestens:

- die Referenz `classConcept` auf eine gemappte ObjectFlow-Entity-Instanz,
- ein `tableName` als Stringliteral,
- atomare Mappings im internen Child-Role `atomMpig`,
- optional Tabellenoptionen in `tableOption`.

### Felder, Schlüssel und Optionen

Ein `Feld-Mapping` (`FieldMapping`) referenziert die fachliche Property und enthält den Spaltennamen als Stringliteral. Wichtige Optionen sind:

| Bereich | Name (Konzeptname) | Bedeutung |
| --- | --- | --- |
| Schlüssel | `key` (`KeyOption`) | Markiert die für Persistenzoperationen verwendete Schlüssel-Property, falls sie nicht bereits an der ObjectFlow-Property markiert ist. |
| Automatische ID | `autoid` (`AutoidOption`) | Bezieht vor einem Insert eine ID aus einer Datenbank-Sequence und setzt sie an der Entity; benötigt einen Sequenznamen. |
| Schemahinweise | `index` (`IndexOption`), `notnull` (`NotnullOption`), `size` (`SizeOption`), `unique` (`UniqueOption`) | Beschreiben Anforderungen an Spalten. ManMap führt daraus keine allgemeinen Schema-Migrationen aus. |
| Audit | `created at` (`CreatedAtFieldOption`), `created by` (`CreatedByFieldOption`), `modified at` (`ModifiedAtFieldOption`), `modified by` (`ModifiedByFieldOption`) | Ordnen Audit-Informationen den entsprechenden Feldern zu. |
| Konkurrenzschutz | `optimistic` (`OptimisticOption`) | Aktiviert optimistische Sperrprüfung für ein schreibbares Entity-Mapping und ist für neue Entity-Mappings empfohlen. |
| Weitere Tabelle | zusätzliche Tabelle (`AdditionalTableName`) | Deklariert beispielsweise eine Archiv-Tabelle für dasselbe Mapping. |

An Properties von ObjectFlow-Entitäten und -Value-Objects können die ManMap-Feldoptionen direkt angegeben werden: `key` (`KeyOption`), `autoid` (`AutoidOption`), die vier Audit-Optionen sowie `index` (`IndexOption`), `notnull` (`NotnullOption`), `size` (`SizeOption`) und `unique` (`UniqueOption`). Sie gelten dann für die betreffende fachliche Property auch immer im Mapping.

### Automatische IDs und Sequences

`autoid` (`AutoidOption`) verbindet eine einzelne Schlüssel-Property mit einer Datenbank-Sequence. Bei einem Insert bezieht ManMap zuerst den nächsten Wert der angegebenen Sequence, setzt ihn an der Entity und verwendet ihn anschließend beim Einfügen der Tabellenzeile. Automatische IDs sind nur für einfache Schlüssel vorgesehen; zusammengesetzte Schlüssel sind ausgeschlossen. Die Entscheidung für ein Insert erfolgt anhand des noch nicht vergebenen Schlüssels, bevor die automatische ID bezogen wird.

Wird ein Mapping über `Mapping einbinden` (`IncludeMapping`) wiederverwendet, kann `OVERWRITE_AUTOID` (`OverWriteAutoIdOption`) für ein ausgewähltes Auto-ID-Feld eine andere Oracle-Sequence angeben. Für dieses Mapping wird dann nicht die ursprünglich am `autoid` (`AutoidOption`) deklarierte Sequence verwendet.

### Optimistic Locking und Audit

`optimistic` (`OptimisticOption`) verhindert, dass zwischenzeitliche Änderungen anderer Bearbeitungsvorgänge unbemerkt überschrieben werden. Hat sich der Datenbankstand seit dem Laden verändert, schlägt das Speichern mit einem Konflikt fehl.

Beim Insert werden die mit `created at/by` und `modified at/by` markierten Audit-Felder gesetzt; beim Update werden die `modified at/by`-Felder aktualisiert, wenn das Objekt geändert wurde. Die Zeitstempel stammen von der Datenbank. Audit erzwingen (`ForceAuditSaveOption`) führt die Audit-Aktualisierung auch für ein nicht geändertes Objekt aus, während Audit überspringen (`SkipAuditSaveOption`) sie auch für ein geändertes Objekt unterdrückt.

### Alternative Tabellen

Ein `Entity-Mapping` (`EntityMapping`) kann mit einer zusätzlichen Tabelle (`AdditionalTableName`) alternative physische Tabellen für dasselbe Mapping deklarieren, beispielsweise eine Archiv-Tabelle. Eine alternative Tabelle (`AdditionalTableReference`) kann gezielt für Abfragen sowie für `save with` (`SaveWithMap`) und `delete with` (`DeleteWithMap`) ausgewählt werden. Bei einer Abfrage mit Joins muss gegebenenfalls auch für die beteiligten Mappings die jeweils passende alternative Tabelle ausgewählt werden.

Die alternative Tabelle ändert nur das physische Tabellenziel. Sie ist keine zusätzliche Mapping-Instanz und erweitert deshalb nicht den Scope der Feldreferenzen (`MappingReference`).
### Referenzen, eingebettete Werte und Listen

`Referenz-Mapping` (`ReferenceMapping`) wählt die Entity-Property, welche auf die Ziel-Entität verweist; deren deklarierter Typ bestimmt somit den Entitätstyp der Referenz. Das enthaltene Schlüsselmapping ordnet anschließend die Schlüssel-Property der Ziel-Entität der Fremdschlüsselspalte in der Tabelle der Quell-Entität zu. Bei einem zusammengesetzten Zielschlüssel kann dieses Schlüsselmapping entsprechend mehrere Teilmappings enthalten. Das Mapping speichert beziehungsweise liest nur den Fremdschlüssel und lädt das Zielobjekt nicht automatisch.

`eingebettetes Mapping` (`EmbeddedMapping`) wählt eine Value-Object-Property und enthält die Mappings für deren einzelne Properties. Diese werden als Spalten derselben Tabellenzeile wie die umgebende Entität gespeichert; für das Value Object wird keine eigene Tabelle oder eigenständige Identität angelegt. Da `eingebettetes Mapping` (`EmbeddedMapping`) selbst als Schlüsselmapping verwendbar ist, kann es auch einen zusammengesetzten Value-Object-Schlüssel beschreiben.

Für Listen gibt es zwei wichtige Formen:

| Form | Verwendung |
| --- | --- |
| `Listen-Mapping` (`ListMapping`) mit Rückreferenz (`MappedFieldRef`) | Das Kindelement besitzt ein echtes `Referenz-Mapping` (`ReferenceMapping`) zurück auf den Parent. |
| `Listen-Mapping` (`ListMapping`) mit reiner Schlüsselreferenz (`KeyOnlyReferenceMapping`) | Die Kindtabelle trägt den Parent-Schlüssel, das Kindobjekt besitzt aber keine fachliche Rückreferenz. |

Beide Formen beschreiben nur die Beziehung. Sie laden die Liste nicht automatisch und führen beim Speichern des Parents nicht zu einem automatischen Speichern der Listenelemente.

### Grenzen von `Mapping einbinden` (`IncludeMapping`)

`Mapping einbinden` (`IncludeMapping`) dient der Wiederverwendung vorhandener Feldabbildungen. Es lädt oder speichert keinen Objektgraphen und ersetzt kein fachlich passendes Mapping. Wird ein `Entity-Mapping` in einem `nokeystore/read-only map` (`NoKeyMapperField`) eingebunden, bleibt das erzeugte Ergebnis trotz der wiederverwendeten Feldabbildungen read-only.


## Gemappte Abfragen mit `get`/`where` auf einem Mapping (`QueryFromMap`)

`get` erwartet einen Schlüssel und liefert eine Instanz oder `null`. Erkennt ManMap einen Integer-, String- oder zusammengesetzten Schlüssel nach seiner typabhängigen Null-Key-Semantik als nicht vergeben, liefert `get` unmittelbar `null`; dieselbe Schlüsselprüfung entscheidet bei `save with` (`SaveWithMap`) ohne erzwingende Option zwischen Insert und Update. Die konkreten Null-Key-Werte sind im Abschnitt „Insert oder Update“ aufgeführt.

`where` (`WhereQuery`) enthält im Child `filter` genau eine BaseLanguage-Expression und liefert eine Liste. Die geschweiften Klammern und die Parameterdarstellung im Editor sind eine Closure-ähnliche Projektion, aber keine BaseLanguage-Closure im AST. Weitere Operationen für `where` werden in der Reihenfolge der Projektion ergänzt, etwa `sortBy`, `limit` oder `size`.

`reload` (`ReloadQuery`) liest die gemappten Felder der übergebenen Entity erneut aus der Datenbank und aktualisiert diese Entity.


### Konzeptlandkarte

| Name | Konzeptname | FQ-Name | Ergebnis beziehungsweise Wirkung |
| --- | --- | --- | --- |
| Mapping mit `get(...)` | `GetQuery` | `org.modellwerkstatt.manmap.structure.GetQuery` | Liefert eine Instanz anhand des Schlüssels oder `null`, wenn der Schlüssel nicht vergeben ist. |
| Mapping mit `where(...)` | `WhereQuery` | `org.modellwerkstatt.manmap.structure.WhereQuery` | Liefert eine Liste anhand eines Filters. |
| `sortBy(...)` | `SortByQuery` | `org.modellwerkstatt.manmap.structure.SortByQuery` | Sortiert auf- oder absteigend. |
| `limit(...)` | `LimitQuery` | `org.modellwerkstatt.manmap.structure.LimitQuery` | Begrenzt die Anzahl der Ergebnisse. |
| `size` | `SizeQuery` | `org.modellwerkstatt.manmap.structure.SizeQuery` | Liefert die Anzahl der Ergebnisse. |
| `reload(...)` | `ReloadQuery` | `org.modellwerkstatt.manmap.structure.ReloadQuery` | Lädt gemappte Daten für eine vorhandene Instanz erneut. |
| `refJoin` | `RefJoinOption` | `org.modellwerkstatt.manmap.structure.RefJoinOption` | Lädt eine gemappte Referenz. |
| `listJoin` | `ListJoinOption` | `org.modellwerkstatt.manmap.structure.ListJoinOption` | Lädt eine gemappte Liste. |
| Name des gemappten Entity-Typs, kleingeschrieben | `MappingReference` | `org.modellwerkstatt.manmap.structure.MappingReference` | Adressiert ein Feld einer in `where` oder `sortBy` verfügbaren Mapping-Instanz. |


### Spezifikum - Filterausdrücke und gemappte Felder

Für den Modellierer lässt Feldreferenz (`MappingReference`) die in einer Abfrage verfügbare Mapping-Instanz wie eine Instanz der gemappten Entity erscheinen. Ein dargestellter Zugriff auf eine Entity-Property ist im AST eine BaseLanguage-Expression vom Konzept `MappingReference`. Sie besitzt zwei erforderliche Referenzen:

- `mappingSource` bestimmt die Mapping-Instanz, deren Felder verwendet werden können.
- `fieldMapping` bestimmt das konkrete `Feld-Mapping` (`FieldMapping`) innerhalb dieser Mapping-Instanz.

Der Typ der Feldreferenz entspricht grundsätzlich dem Typ der Property, auf die das ausgewählte `Feld-Mapping` (`FieldMapping`) verweist. Eine Feldreferenz kann nicht mit einem normalen Dot-Ausdruck weiter spezifiziert werden. Sie ist nur innerhalb von `where` (`WhereQuery`) und `sortBy` (`SortByQuery`) zulässig.

Der Scope von `mappingSource` wird aus dem umgebenden `get`/`where` auf einem Mapping (`QueryFromMap`) gebildet. Er enthält dessen Basismapping und die tatsächlich deklarierten Join-Optionen, die selbst eine Mapping-Instanz darstellen:

| Mapping-Instanz im Scope | Verfügbare Feld-Mappings |
| --- | --- |
| Basisabfrage (`QueryFromMap`) | Die `Feld-Mapping` (`FieldMapping`)-Knoten des von der Basisabfrage referenzierten `Entity-Mapping` (`EntityMapping`) |
| `refJoin` (`RefJoinOption`) | Die `Feld-Mapping` (`FieldMapping`)-Knoten des vom Join referenzierten Ziel-`Entity-Mapping` (`EntityMapping`) |
| `listJoin` (`ListJoinOption`) | Die `Feld-Mapping` (`FieldMapping`)-Knoten des Ziel-Entity-Mappings, das über die Rückreferenz des `Listen-Mapping` (`ListMapping`) bestimmt wird |

Nur auf der Abfrage vorhandene Ref- und List-Joins erweitern diesen Scope. Eine zusätzliche Tabelle (`AdditionalTableReference`) ist keine Mapping-Instanz und stellt deshalb keine weiteren Feldreferenzen bereit.

Die Property `option` von Feldreferenz (`MappingReference`) beeinflusst die Behandlung des gemappten Werts:

| Wert | Wirkung |
| --- | --- |
| `NOP` | Verwendet den gemappten Wert ohne zusätzliche Konvertierung. |
| `TO_LOCALDATE` | Behandelt den gemappten Wert als `LocalDate`; auch der Typ der Expression ist `LocalDate`. |
| `TO_LOWERCASE` | Verwendet den in Kleinbuchstaben umgewandelten gemappten Wert. |
| `TO_UPPERCASE` | Verwendet den in Großbuchstaben umgewandelten gemappten Wert. |

Ein `where`-Filter verwendet typischerweise normale BaseLanguage-Vergleiche auf Feldreferenzen: `==` und `!=` für Gleichheit beziehungsweise Ungleichheit sowie `<`, `<=`, `>` und `>=` für geordnete Werte. Mehrere Prädikate lassen sich mit `&&`, `||` und `!` kombinieren. Beide Seiten eines Vergleichs müssen typkompatibel sein, beispielsweise `int` mit `int`, `BigDecimal` mit einem `BigDecimal`-Ausdruck oder `DateTime` mit `DateTime`. Für einen Vergleich als `LocalDate` kann die Feldreferenz-Option `TO_LOCALDATE` eingesetzt werden. Klammern sollten die gewünschte boolesche Bindung eindeutig machen.

Darüber hinaus stellt ManMap drei eigene Prädikatkonzepte bereit:

- `in` (`InOperation`) prüft eine Feldreferenz (`MappingReference`) gegen eine als BaseLanguage-Expression angegebene Liste. Der Elementtyp der Liste muss zum Typ des gemappten Felds passen, etwa `list<int>`, `list<string>` oder eine Liste des passenden ObjectFlow-Status.
- `like` (`LikeOperator`) bildet einen SQL-`LIKE`-Vergleich aus einem String-Ausdruck und einem Stringmuster. Platzhalter wie `%` und `_` gehören in den übergebenen Musterwert; sie werden nicht automatisch ergänzt.
- `optional` (`OptionalOperator`) umschließt ein vollständiges Prädikat. Ist dessen relevanter Parameter nicht gesetzt, wird dieses Prädikat nicht in die SQL-Bedingung aufgenommen; dadurch lassen sich einzelne Suchkriterien beispielsweise innerhalb einer `||`- oder `&&`-Verknüpfung unabhängig aktivieren.

Der `optional` (`OptionalOperator`) lässt einen Filter bei `int` für den Wert `0` und bei `BigDecimal`, Datum/Zeit, String, Referenzen und ObjectFlow-Status für `null` weg. `boolean` wird nicht unterstützt. Diese Regeln unterscheiden sich von der Schlüsselprüfung für die Insert-/Update-Entscheidung beim Speichern von Entitäten; insbesondere gelten `-1` und der leere String nicht automatisch als ausgelassener optionaler Filter.

### Explizites Laden

Eine deklarierte Beziehung ist noch keine geladene Beziehung:

- Eine nicht geladene Referenz wirft beim Zugriff `org.modellwerkstatt.objectflow.runtime.OFXNotInitializedException`.
- Eine nicht geladene Liste ist leer (`size == 0`) und wirft diese Ausnahme nicht.
- `refJoin` (`RefJoinOption`) lädt eine Referenz über das zugehörige `Referenz-Mapping` (`ReferenceMapping`) und das Ziel-`Entity-Mapping` (`EntityMapping`).
- `listJoin` (`ListJoinOption`) lädt eine Liste als Teil der Abfrage.
- Alternativ kann eine separate `where`-Abfrage geladen und der Listen-Property explizit zugewiesen werden.

Eine leere Liste beweist daher nicht, dass in der Datenbank keine Kindzeilen vorhanden sind. Vor einer solchen Schlussfolgerung ist die Ladestrategie der Repository-Methode zu prüfen.

`debugMe` an `get`/`where` auf einem Mapping (`QueryFromMap`) schreibt generiertes SQL und Parameterwerte zur Diagnose nach `System.out`. Diese Option ist ein Diagnosehilfsmittel und keine normale Betriebsoption.


## Speichern mit `save with` (`SaveWithMap`)

`save with` (`SaveWithMap`) referenziert ein `Entity-Mapping` (`EntityMapping`) und erhält als Ausdruck die zu speichernde Entität oder – mit Batch-Option – eine geeignete Menge.

### Insert oder Update

Ohne erzwingende Option prüft ManMap den Schlüssel über `MMStaticAccessHelper.isNullKeyStaticHelper()`:

| Schlüsselform | Als „noch nicht vergeben“ behandelte Werte |
| --- | --- |
| einzelner Integer-Schlüssel | `null`, `0` oder `-1` |
| einzelner String-Schlüssel | `null` oder `""` |
| zusammengesetzter Value-Object-Schlüssel | Integer-Komponenten `< 0`; String-Komponenten `null` oder `""` |

Ein nicht vergebener Schlüssel führt zum Insert, ein vergebener Schlüssel zum Update. `insert` (`InsertSaveOption`) beziehungsweise `update` (`UpdateSaveOption`) erzwingen die jeweilige Operation. Bei zusammengesetzten Schlüsseln sollte eine dieser Optionen ausdrücklich gewählt werden. `autoid` (`AutoidOption`) bezieht die ID vor dem Insert von der Datenbank.

### Speichern von Objektgraphen

`save with` (`SaveWithMap`) speichert nur die durch das ausgewählte Mapping beschriebenen Spalten des übergebenen Objekts. Dabei wird auch der Fremdschlüssel einer gemappten Referenz gespeichert. Nicht automatisch gespeichert werden:

- das referenzierte Objekt selbst,
- Elemente eines `Listen-Mapping` (`ListMapping`),
- sonstige Teile eines fachlichen Objektgraphen.

Für einen Parent mit Kindern wird daher typischerweise zuerst der Parent gespeichert, dann der Parent-Schlüssel beziehungsweise die Rückreferenz an die Kinder gesetzt und schließlich jedes Kind über sein eigenes `Entity-Mapping` (`EntityMapping`) gespeichert.

### Save-Optionen

| Option | Verwendung |
| --- | --- |
| `insert` (`InsertSaveOption`) | Insert unabhängig von der automatischen Schlüsselprüfung erzwingen |
| `update` (`UpdateSaveOption`) | Update unabhängig von der automatischen Schlüsselprüfung erzwingen |
| `BATCH` (`BatchSaveOption`) | Viele Objekte effizient im JDBC-Batch speichern |
| Audit erzwingen (`ForceAuditSaveOption`) | Auditbehandlung für diesen Speichervorgang erzwingen |
| Audit überspringen (`SkipAuditSaveOption`) | Auditbehandlung für diesen Speichervorgang überspringen |
| alternative Tabelle (`AdditionalTableReference`) | Eine deklarierte alternative Tabelle für die Operation auswählen |

`BATCH` (`BatchSaveOption`) ist für Mengenoperationen gedacht. Für das Speichern eines einzelnen Objekts sollte sie nicht nur deshalb verwendet werden, weil sie verfügbar ist. Bei grösseren Mengen ist der Performance-Vorteil oft substantiell.


## Löschen mit `delete with` (`DeleteWithMap`)

`delete with` (`DeleteWithMap`) referenziert ein `Entity-Mapping` (`EntityMapping`) und löscht die übergebene, bereits geladene Entität anhand ihres Schlüssels.

Auch beim Löschen gibt es keine automatische Kaskade. Soll ein Objektgraph entfernt werden, werden abhängige Kindobjekte in der fachlich und relational korrekten Reihenfolge explizit gelöscht, typischerweise vor dem Parent. Ein `Listen-Mapping` (`ListMapping`) allein erzeugt kein Kaskadenverhalten.

Eine `DELETE`-Repository-Methode wird üblicherweise als Session Operation registriert. Dadurch wird die Löschoperation erst beim vorgesehenen erfolgreichen Session-Abschluss innerhalb der Transaktion ausgeführt.


## Custom SQL mit `SQL` (`C2SqlBlock`)

Das Konzept `SQL` (`C2SqlBlock`) ermöglicht die dynamische Zusammenstellung einer SQL-Anweisung. Innerhalb des Blocks können Java-Statements der BaseLanguage mit SQL-Textfragmenten des Konzepts `SQL-Text` (`C2SqlText`) kombiniert werden.

Der Kontrollfluss bestimmt, welche Textfragmente zur SQL-Anweisung beitragen: Alle im Programmablauf erreichten `SQL-Text`-Fragmente werden in ihrer Ausführungsreihenfolge aneinandergehängt. So kann beispielsweise ein `if` (`IfStatement`) dafür sorgen, dass eine zusätzliche SQL-Bedingung nur dann angefügt wird, wenn ein bestimmtes Suchkriterium gesetzt ist.

Innerhalb des `SQL`-Blocks stehen alle Variablen zur Verfügung, die im umgebenden Kontext sichtbar sind. Dadurch lässt sich die SQL-Anweisung abhängig von Parametern, Suchkriterien und zuvor berechneten Werten zusammensetzen.

### SQL Query und SQL Statement

Die Property `sqlType` legt fest, wie die zusammengesetzte SQL-Anweisung ausgeführt und ihr Ergebnis verarbeitet wird. Sie besitzt zwei Werte:

| Wert        | Zweck                                                                        | Ergebnis                                                                                                                                                                            |
| ----------- | ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `QUERY`     | Führt eine SQL-Abfrage aus und verarbeitet deren Ergebnismenge.              | Das Ergebnis-Mapping wird durch eine Closure der BaseLanguage, eine Row-Mapper-Referenz (`RowMapperFieldRef`) oder eine No-Key-Mapper-Referenz (`NoKeyMapperFieldRef`) beschrieben. |
| `STATEMENT` | Führt eine SQL-Anweisung zur Datenänderung aus, beispielsweise ein `UPDATE`. | Gibt die Anzahl der betroffenen Datenbankzeilen als `int` zurück. Ein Ergebnis-Mapping ist nicht vorgesehen.                                                                        |

Wird ein `STATEMENT` innerhalb einer session operation ausgeführt, unterliegt es deren Session- und Transaktionskontext. Die direkte SQL-Ausführung umgeht diesen Kontext nicht. Sie sollte gezielt eingesetzt werden, wenn eine Änderung unmittelbar per SQL erfolgen soll.

### Parameter in SQL-Text

Innerhalb von `SQL-Text` (`C2SqlText`) können Werte aus sichtbaren Variablen als SQL-Parameter verwendet werden. Die Referenz wird mit `:` (`C2SqlWordVarReference`) dargestellt.

Ein SQL-Textfragment kann beispielsweise so aussehen:

```sql
WHERE MEINE_TABELLE.ID = :local_id_var
```

Dabei verweist `local_id_var` auf eine im umgebenden Kontext sichtbare Variable. Ihr Wert wird bei der Ausführung als Parameter gebunden und nicht als SQL-Text eingefügt. Die technische Umsetzung erfolgt über benannte Parameter auf Basis von JDBC.

Neben einfachen Variablenreferenzen werden Zugriffe über den Dot-Operator (`.`) mit einer maximalen Verschachtelungstiefe von 1 unterstützt. In der SQL-Parameterdarstellung werden die Bestandteile durch Unterstriche verbunden. Ist die Variable `rechnung` im lokalen Kontext sichtbar, sind beispielsweise folgende Zugriffe möglich:

| Parameterdarstellung         | Zugriff                                                                 | Manmap-Konzept                                                                                                                            |
| ---------------------------- | ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| `:rechnung_id`               | Liest die Eigenschaft `id` von `rechnung`.                              | Property-Zugriff (`C2Dot`) mit Variablenreferenz (`C2SqlWordVarReference`) und Property-Referenz (`C2PropertyReference`).                 |
| `:rechnung_refLieferant_KEY` | Liest `KEY` über die Referenz `refLieferant` von `rechnung`.            | Property-Zugriff (`C2Dot`) mit Variablenreferenz (`C2SqlWordVarReference`) und Entity-Key-Property-Referenz (`C2EntityKeyPropReference`). |
| `:rechnung_methode`          | Verwendet den Rückgabewert einer parameterlosen Methode von `rechnung`. | Methodenzugriff (`C2Dot`) mit Variablenreferenz (`C2SqlWordVarReference`) und Methodenreferenz (`C2MethodReference`).                     |

Der aufgelöste Wert muss einen primitiven Typ besitzen. Bei einem Methodenzugriff muss die Methode parameterlos sein und einen primitiven Typ zurückgeben.

### Statuskonstanten in SQL-Text

Innerhalb von `SQL-Text` (`C2SqlText`) können auch deklarierte Statuswerte aus `org.modellwerkstatt.objectflow` referenziert werden. Dafür steht das Konzept `C2SqlStatusReference` zur Verfügung. So lässt sich eine SQL-Bedingung auf einen definierten Status beziehen, ohne dessen konkreten Wert im SQL-Text fest einzutragen.

### `+` (`C2SqlIntegration`)

`+` (`C2SqlIntegration`, FQ-Name `org.modellwerkstatt.manmap.structure.C2SqlIntegration`) ist ein Statement innerhalb eines `SQL`-Blocks (`C2SqlBlock`), mit dem dynamisch bereitgestellter SQL-Text eingebunden und mit Parameterwerten verknüpft werden kann. Der optionale Ausdruck `sqlString` liefert den SQL-Text; Werte können entweder als geordnete `arguments` oder als benannte Parameter (`SqlNamedParameter`) übergeben werden. Das Konzept ist vor allem für Legacy-Code oder stark dynamische SQL-Fragmente vorgesehen. Für normales SQL mit Variablen, Objekt-Properties oder Statuswerten sollten die spezifischen C2-Referenzknoten wie `C2SqlWordVarReference`, `C2Dot` und `C2SqlStatusReference` verwendet werden.

Innerhalb von `C2SqlIntegration` sind benannte Parameter für neue Verwendungen gegenüber positionalen Argumenten zu bevorzugen. Positionale Argumente und frei integrierte SQL-Fragmente sind vor allem für bestehenden oder besonders dynamischen Code vorgesehen. Die Parameterwerte werden gebunden und nicht als Text in das SQL eingesetzt. Diese Einordnung betrifft ausschließlich `C2SqlIntegration`, nicht die übrigen Parameterformen von C2.


### Row-Mapper und No-Key-Mapper


| Ergebnisform | Mapping im `SQL` (`C2SqlBlock`) | Repository-Member | Geeigneter Einsatz |
| --- | --- | --- | --- |
| kleiner skalarer Wert | Inline-Closure | keiner | Beispielsweise `count(*)` als Integer |
| wiederverwendbare freie Zeilenkonvertierung | `row mapper`-Referenz (`RowMapperFieldRef`) | `row mapper` (`RowMapperField`) | Wenn dieselbe Closure mehrfach genutzt wird |
| Ergebnis ohne verwendbaren Schlüssel | `nokeystore/read-only map`-Referenz (`NoKeyMapperFieldRef`) | `nokeystore/read-only map` (`NoKeyMapperField`) | DTO, Projektion, Aggregation oder Tabellenmodell |
| Entity-förmiges read-only Ergebnis | `nokeystore/read-only map`-Referenz (`NoKeyMapperFieldRef`) | `nokeystore/read-only map` (`NoKeyMapperField`) mit Mapping einbinden (`IncludeMapping`) | Vorhandenes `Entity-Mapping` (`EntityMapping`) für die Feldabbildung wiederverwenden |

#### `row mapper` (`RowMapperField`)

`row mapper` (`RowMapperField`) enthält eine Closure, die eine Ergebniszeile in einen Wert überführt. Ihr Zeilenparameter hat den Laufzeittyp `org.modellwerkstatt.manmap.runtime.IM3QueryFromSqlRowRef`. Dieser stellt mit `getAsInteger`, `getAsString`, `getAsDecimal`, `getAsDateTime` und `getAsLocalDate` typisierte Zugriffe bereit, jeweils wahlweise über den Spaltennamen oder den Spaltenindex. Indizierte Zugriffe beginnen entsprechend JDBC bei `1`, nicht bei `0`.

Für eine einmalige kleine skalare Abfrage kann dieselbe Logik als Inline-Closure im Ergebnis-Mapping eines `SQL`-Blocks (`C2SqlBlock`) stehen; auch dort besitzt der Zeilenparameter denselben Typ und dieselben Zugriffsregeln. Der Repository-Member ist sinnvoll, wenn die Konvertierung wiederverwendet werden soll.

#### `nokeystore/read-only map` (`NoKeyMapperField`)

`nokeystore/read-only map` (`NoKeyMapperField`) referenziert über `classConcept` den Ergebnistyp und enthält seine Feldmappings im Role `atomMpig`. Es kann alle Spalten selbst mappen oder über `Mapping einbinden` (`IncludeMapping`) ein geeignetes bestehendes Mapping wiederverwenden.

Jedes von einem `nokeystore/read-only map` (`NoKeyMapperField`) erzeugte Objekt ist read-only. Das gilt auch dann, wenn ein bestehendes `Entity-Mapping` (`EntityMapping`) eingebunden wird. Das No-Key-Ergebnis selbst wird nicht in die Session integriert, das heißt nicht in die Session-Identity-Map aufgenommen. Für transiente Such-, Tabellen- und Aggregationsergebnisse ist daher ein ObjectFlow-`DTO` zu verwenden.

Im Ergebnis-Mapping von direktem SQL referenziert Feldreferenz (`MappingReference`) ein einzelnes `Feld-Mapping` (`FieldMapping`). In diesem Kontext kann sie nicht direkt ein `Entity-Mapping` (`EntityMapping`) als SQL-Row-Mapper verwenden. Soll ein vollständiges Mapping wiederverwendet werden, führt der Pfad über `nokeystore/read-only map` (`NoKeyMapperField`) und dessen `Mapping einbinden` (`IncludeMapping`).

Bei Mappingfehlern sind zuerst SQL-Aliase und Ergebnisspalten mit den Namen der Mapper-Felder und den Properties der Zielklasse zu vergleichen. Danach ist zu prüfen, ob der `SQL` (`C2SqlBlock`) tatsächlich den beabsichtigten Mapper-Member referenziert.


## Datenbankportabilität und Schema

ManMap unterstützt Oracle und MySQL. Benutzerdefiniertes SQL bleibt dennoch an den jeweiligen Datenbankdialekt gebunden; insbesondere Funktionen, Datentypen und weitere SQL-Eigenheiten müssen zur eingesetzten Datenbank passen.

Schemaoptionen wie `notnull`, `size`, `index` und `unique` beschreiben Anforderungen beziehungsweise Metadaten des Mappings. ManMap ist kein allgemeines Werkzeug zur Migration bestehender Datenbankschemata.


## Durchgängige Abläufe

### Domänenmodell laden, bearbeiten und speichern

1. Eine `CHECKOUT`-Repository-Methode lädt die Root-Entity mit `get`/`where` auf einem Mapping (`QueryFromMap`) im Modus Checkout.
2. Benötigte Referenzen und Listen werden per Join oder separater Abfrage explizit geladen.
3. Der Command beziehungsweise Service verändert die in der Session integrierten Objekte.
4. Eine oder mehrere `CHECKIN`-Methoden werden als Session Operations registriert.
5. Beim erfolgreichen Abschluss führt die Session die Operationen innerhalb der Transaktion aus.
6. Parent und Kinder werden in der vorgesehenen Reihenfolge jeweils mit ihrem eigenen Mapping gespeichert.

### Lesemodell mit Custom SQL verwenden

1. Eine `READONLY`-Repository-Methode führt einen `SQL` (`C2SqlBlock`) mit `sqlType=QUERY` aus.
2. Ein `nokeystore/read-only map` (`NoKeyMapperField`) bildet jede Ergebniszeile auf ein DTO ab.
3. Die Anwendung zeigt oder verarbeitet die read-only DTOs.
4. Eine enthaltene ID kann an einen späteren `CHECKOUT`-Ablauf übergeben werden.
5. Die DTOs werden nicht zurückgespeichert und nach dem Anwendungsfall verworfen.


## Häufige Fehler und Diagnose

- **Mapping mit Lazy Loading verwechseln:** Ein `Referenz-Mapping` (`ReferenceMapping`) oder `Listen-Mapping` (`ListMapping`) beschreibt eine Beziehung, lädt sie aber nicht.
- **Leere Liste als leere Datenbankbeziehung interpretieren:** Eine nicht explizit geladene Liste ist ebenfalls leer.
- **Automatisches Graph-Speichern erwarten:** Referenzziele und Listenelemente müssen mit eigenen Mappings explizit gespeichert werden.
- **Automatisches Kaskadenlöschen erwarten:** Kinder müssen in geeigneter Reihenfolge explizit gelöscht werden.
- **Read-only-Entity verändern:** Herkunft aus `get`/`where` auf einem Mapping (`QueryFromMap`) mit `readOnly=true` oder aus einem No-Key-Mapping prüfen.
- **Dieselbe Entität mehrfach auschecken:** Alle `get`- und `where`-Abfragen derselben Session prüfen und die bereits geladene Instanz verwenden.
- **No-Key-Ergebnis für eine normale Entity halten:** No-Key-Ergebnisse bleiben read-only und liegen außerhalb der Session-Identity-Map. Sie weisen keinen fachlichen oder surrogatschlussel auf.
- **SQL-Feldreferenz (`MappingReference`) auf ein `Entity-Mapping` (`EntityMapping`) richten:** Für die Wiederverwendung eines `Entity-Mappings` (`EntityMapping`) im Custom SQL ist `Mapping einbinden` (`IncludeMapping`) innerhalb eines `nokeystore/read-only map` (`NoKeyMapperField`) zu verwenden.
- **Batch für Einzelobjekte verwenden:** `BATCH` (`BatchSaveOption`) ist für größere Mengen gedacht.
- **Repository-Methode als Transaktionsgrenze behandeln:** Den ObjectFlow-Session- und Command-Ablauf prüfen.
- **Name und Konzeptname verwechseln:** Name, Konzeptname und FQ-Name nach der eingangs festgelegten Schreibweise unterscheiden.


## Konzeptindex für Agenten

Der Index enthält die in dieser Dokumentation behandelten Konzepte, nicht alle Konzepte der Sprache. Für JSON-Blueprints sind die FQ-Namen zu verwenden. Vor einer Modelländerung müssen Referenzen, Child-Roles und Kardinalitäten über MPS MCP im aktuellen Projekt aufgelöst werden.

| Themenbereich | Name | Konzeptname | FQ-Name |
| --- | --- | --- | --- |
| Root | `Persistence Description` | `PersistenceDescription` | `org.modellwerkstatt.manmap.structure.PersistenceDescription` |
| Root | `Repository` | `Repository` | `org.modellwerkstatt.manmap.structure.Repository` |
| Repository | `repo method` | `RepositoryInstanceMethodDeclaration` | `org.modellwerkstatt.manmap.structure.RepositoryInstanceMethodDeclaration` |
| Repository | `sql string` | `SqlStringField` | `org.modellwerkstatt.manmap.structure.SqlStringField` |
| Mapping | Entity-Mapping | `EntityMapping` | `org.modellwerkstatt.manmap.structure.EntityMapping` |
| Mapping | Feld-Mapping | `FieldMapping` | `org.modellwerkstatt.manmap.structure.FieldMapping` |
| Mapping | Referenz-Mapping | `ReferenceMapping` | `org.modellwerkstatt.manmap.structure.ReferenceMapping` |
| Mapping | eingebettetes Mapping | `EmbeddedMapping` | `org.modellwerkstatt.manmap.structure.EmbeddedMapping` |
| Mapping | Listen-Mapping | `ListMapping` | `org.modellwerkstatt.manmap.structure.ListMapping` |
| Mapping | Mapping einbinden | `IncludeMapping` | `org.modellwerkstatt.manmap.structure.IncludeMapping` |
| Mapping | Rückreferenz verwenden | `MappedFieldRef` | `org.modellwerkstatt.manmap.structure.MappedFieldRef` |
| Mapping | reine Schlüsselreferenz | `KeyOnlyReferenceMapping` | `org.modellwerkstatt.manmap.structure.KeyOnlyReferenceMapping` |
| Mapping-Option | Schlüssel | `KeyOption` | `org.modellwerkstatt.manmap.structure.KeyOption` |
| Mapping-Option | automatische ID | `AutoidOption` | `org.modellwerkstatt.manmap.structure.AutoidOption` |
| Mapping-Option | Auto-ID-Sequence überschreiben | `OverWriteAutoIdOption` | `org.modellwerkstatt.manmap.structure.OverWriteAutoIdOption` |
| Mapping-Option | optimistic | `OptimisticOption` | `org.modellwerkstatt.manmap.structure.OptimisticOption` |
| Mapping-Option | weitere Tabelle | `AdditionalTableName` | `org.modellwerkstatt.manmap.structure.AdditionalTableName` |
| Query | `get`/`where` auf einem Mapping | `QueryFromMap` | `org.modellwerkstatt.manmap.structure.QueryFromMap` |
| Query | `get` | `GetQuery` | `org.modellwerkstatt.manmap.structure.GetQuery` |
| Query | `where` | `WhereQuery` | `org.modellwerkstatt.manmap.structure.WhereQuery` |
| Query | `sortBy` | `SortByQuery` | `org.modellwerkstatt.manmap.structure.SortByQuery` |
| Query | `limit` | `LimitQuery` | `org.modellwerkstatt.manmap.structure.LimitQuery` |
| Query | `size` | `SizeQuery` | `org.modellwerkstatt.manmap.structure.SizeQuery` |
| Query | `reload` | `ReloadQuery` | `org.modellwerkstatt.manmap.structure.ReloadQuery` |
| Query | `refJoin` | `RefJoinOption` | `org.modellwerkstatt.manmap.structure.RefJoinOption` |
| Query | `listJoin` | `ListJoinOption` | `org.modellwerkstatt.manmap.structure.ListJoinOption` |
| Query | alternative Tabelle | `AdditionalTableReference` | `org.modellwerkstatt.manmap.structure.AdditionalTableReference` |
| Query / Row-Mapping | gemapptes Feld | `MappingReference` | `org.modellwerkstatt.manmap.structure.MappingReference` |
| Query-Operator | `in` | `InOperation` | `org.modellwerkstatt.manmap.structure.InOperation` |
| Query-Operator | `like` | `LikeOperator` | `org.modellwerkstatt.manmap.structure.LikeOperator` |
| Query-Operator | `optional` | `OptionalOperator` | `org.modellwerkstatt.manmap.structure.OptionalOperator` |
| Speichern | `save with` | `SaveWithMap` | `org.modellwerkstatt.manmap.structure.SaveWithMap` |
| Speichern | Insert erzwingen | `InsertSaveOption` | `org.modellwerkstatt.manmap.structure.InsertSaveOption` |
| Speichern | Update erzwingen | `UpdateSaveOption` | `org.modellwerkstatt.manmap.structure.UpdateSaveOption` |
| Speichern | `BATCH` | `BatchSaveOption` | `org.modellwerkstatt.manmap.structure.BatchSaveOption` |
| Speichern | Audit erzwingen | `ForceAuditSaveOption` | `org.modellwerkstatt.manmap.structure.ForceAuditSaveOption` |
| Speichern | Audit überspringen | `SkipAuditSaveOption` | `org.modellwerkstatt.manmap.structure.SkipAuditSaveOption` |
| Löschen | `delete with` | `DeleteWithMap` | `org.modellwerkstatt.manmap.structure.DeleteWithMap` |
| Custom SQL | `SQL` | `C2SqlBlock` | `org.modellwerkstatt.manmap.structure.C2SqlBlock` |
| Custom SQL | SQL-Text | `C2SqlText` | `org.modellwerkstatt.manmap.structure.C2SqlText` |
| Custom SQL | Variable im SQL | `C2SqlWordVarReference` | `org.modellwerkstatt.manmap.structure.C2SqlWordVarReference` |
| Custom SQL | Objekt-Property im SQL | `C2Dot` | `org.modellwerkstatt.manmap.structure.C2Dot` |
| Custom SQL | Property-Referenz | `C2PropertyReference` | `org.modellwerkstatt.manmap.structure.C2PropertyReference` |
| Custom SQL | Statuswert im SQL | `C2SqlStatusReference` | `org.modellwerkstatt.manmap.structure.C2SqlStatusReference` |
| Custom SQL | `+` | `C2SqlIntegration` | `org.modellwerkstatt.manmap.structure.C2SqlIntegration` |
| Row-Mapping | `row mapper` | `RowMapperField` | `org.modellwerkstatt.manmap.structure.RowMapperField` |
| Row-Mapping | Row-Mapper verwenden | `RowMapperFieldRef` | `org.modellwerkstatt.manmap.structure.RowMapperFieldRef` |
| Row-Mapping | `nokeystore/read-only map` | `NoKeyMapperField` | `org.modellwerkstatt.manmap.structure.NoKeyMapperField` |
| Row-Mapping | No-Key-Mapper verwenden | `NoKeyMapperFieldRef` | `org.modellwerkstatt.manmap.structure.NoKeyMapperFieldRef` |

## Quellen für die Modellarbeit

Die fachliche Beschreibung in diesem Dokument ersetzt nicht die Prüfung der geladenen Sprache. Für konkrete Modelländerungen gelten die MPS-Sprachdefinition, ihre Constraints und die Validierung als technische Quelle der Wahrheit.
