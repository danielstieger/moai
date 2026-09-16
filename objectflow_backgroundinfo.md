## Sessions, Commands und Transaktionen

> Arbeitsstand: Die folgenden Abläufe stammen aus der Beschreibung des Sprachverantwortlichen. Die vier Bezeichnungen wurden durch die Spracheingabe nicht eindeutig wiedergegeben. Die Zeilen beschreiben vorläufig vier Verhaltensweisen und legen keine technischen Typnamen fest.

| Beschriebener Typ | Session und Interaktion | Schreiben und Commit |
| --- | --- | --- |
| SEARCH Command | Startet eine Session im Hintergrund. Lädt Daten anhand von Filtern, kann sie aufbereiten und über mehrere Pages beziehungsweise Views anzeigen. | Die Session darf nicht committed werden; Änderungen dürfen über diese Session nicht in die Datenbank geschrieben werden. |
| GRAPH_OWNER Command | Startet eine eigene Session. Lädt Daten und bereitet sie auf; Benutzer können sie auch über die Oberfläche bearbeiten. | Zum Abschluss werden registrierte Session Operations innerhalb einer Datenbanktransaktion ausgeführt und committed. Der genaue Auslöser ist noch zu klären. |
| GRAPH_EDIT Command | Startet keine neue Session, sondern übernimmt eine bestehende Session eines Performers. Dient der Modellierung von Benutzerinteraktion. | Eigene Abschluss- und Commit-Befugnisse sind noch zu klären. |
| MODAL_GRAPH_OWNER | Modale Benutzerinteraktion, vergleichbar mit einem Dialogfenster. | Session-Zuordnung und Transaktionsverhalten sind noch zu bestätigen. |

Beim ändernden Command registriert der Anwendungsentwickler auszuführende Operationen auf einem **Session Operation Stack**. Zum beschriebenen Abschluss wird eine Datenbanktransaktion gestartet, die registrierten Operationen werden ausgeführt und die Transaktion wird committed. Die Reihenfolge der Abarbeitung, das Verhalten bei Fehlern und Abbruch sowie der genaue Abschlussmechanismus sind noch offen; aus dem Wort „Stack“ wird keine Ausführungsreihenfolge abgeleitet.

Die beschriebene Session begleitet Laden und Benutzerinteraktion. Die Datenbanktransaktion zur Ausführung der Session Operations beginnt dagegen erst beim genannten Abschluss. Session-Lebensdauer und diese Transaktionsdauer sind daher getrennt zu dokumentieren. Über weitere Transaktionen beim Laden trifft diese Beschreibung keine Aussage.