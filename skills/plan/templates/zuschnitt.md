# Plan: Zuschnitt `<firma>.<app>`

*Der Zuschnitt wird fortgeschrieben: Kommt ein Bounded Context oder ein Bereich hinzu, wird diese Datei ergänzt und erneut freigegeben.*

| | |
|---|---|
| Status | Entwurf / freigegeben |
| Bestehende Solutions und Modelle | *was es schon gibt; „keine“ bei einer neuen Anwendung* |

## Anforderung

*Wenige Sätze in Fachsprache: was die Anwendung leisten soll und für wen.*

## 1. Glossar

*Die Fachbegriffe der Anwendung; Bereichspläne und Modelle verwenden genau diese Namen.*

| Begriff | Bedeutung | Bounded Context |
|---|---|---|

## 2. Bounded Contexts

| Bounded Context | Fachlicher Inhalt | eigene Solution |
|---|---|---|

## 3. Bereiche

| Bereich | Bounded Context | Art (Aggregat / Use Case) | Aggregate bzw. Ablauf | Grund für den Schnitt |
|---|---|---|---|---|

## 4. Abhängigkeiten zwischen Bereichen

*Wer braucht einen Fakt oder ein Aggregat von wem; keine Zyklen zwischen Bounded Contexts.*

| Bereich | braucht von | wozu |
|---|---|---|

## 5. Gemeinsame Werte

*Status und Value Objects, die keinem Bereich gehören (`sharedvalues`).*

| Wert | verwendet von |
|---|---|

## 6. Fremdsysteme

| Fremdsystem | lesend / schreibend | Bounded Context | wozu |
|---|---|---|---|

## 7. Laufzeit und Konfiguration

*Die `OFXConfig`s im Modell `base`: je Laufzeitumgebung und für die Tests.*

| Konfiguration | Laufzeitumgebung | Zielgeräte | Datenbank |
|---|---|---|---|

## 8. Anmeldung und Rollen

*Woher der Benutzername kommt (Login-Maske, OAuth) und woher Benutzer-ID und Rollen stammen.*

| Rolle | darf |
|---|---|

## 9. Batchjobs

| Batchjob | Bereich | wozu | Zeitplan |
|---|---|---|---|

## 10. Abweichungen von Konventionen

*Leer heißt: keine. Jede Zeile braucht die Entscheidung des Nutzers; Abweichungen, die das Projekt festlegt, tragen als Grund „Projekt“.*

| Konvention | Abweichung | Grund |
|---|---|---|

## 11. Offene Fragen

*Alle `KLÄREN:`-Punkte aus den Abschnitten oben. Vor der Freigabe leer.*

## 12. Reihenfolge der Bereichspläne

*Bereiche, von denen andere abhängen, zuerst.*

1.
