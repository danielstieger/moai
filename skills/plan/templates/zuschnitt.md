# Plan: Zuschnitt `<firma>.<app>`

| | |
|---|---|
| Status | Entwurf / freigegeben |
| Bestehende Solutions und Modelle | *was es schon gibt; „keine“ bei einer neuen Anwendung* |

## Anforderung

*Wenige Sätze in Fachsprache: was die Anwendung leisten soll und für wen.*

## 1. Bounded Contexts

| Bounded Context | Fachlicher Inhalt | eigene Solution |
|---|---|---|

## 2. Bereiche

| Bereich | Bounded Context | Art (Aggregat / Use Case) | Aggregate bzw. Ablauf | Grund für den Schnitt |
|---|---|---|---|---|

## 3. Abhängigkeiten zwischen Bereichen

*Wer braucht einen Fakt oder ein Aggregat von wem; keine Zyklen zwischen Bounded Contexts.*

| Bereich | braucht von | wozu |
|---|---|---|

## 4. Gemeinsame Werte

*Status und Value Objects, die keinem Bereich gehören (`sharedvalues`).*

| Wert | verwendet von |
|---|---|

## 5. Fremdsysteme

| Fremdsystem | lesend / schreibend | Bounded Context | wozu |
|---|---|---|---|

## 6. Laufzeit und Konfiguration

*Die `OFXConfig`s im Modell `base`: je Laufzeitumgebung und für die Tests.*

| Konfiguration | Laufzeitumgebung | Datenbank |
|---|---|---|

## 7. Rollen

| Rolle | darf |
|---|---|

## 8. Abweichungen von Konventionen

*Leer heißt: keine. Jede Zeile braucht die Entscheidung des Nutzers.*

| Konvention | Abweichung | Grund |
|---|---|---|

## 9. Offene Fragen

*Alle `KLÄREN:`-Punkte aus den Abschnitten oben. Vor der Freigabe leer.*

## 10. Reihenfolge der Bereichspläne

*Bereiche, von denen andere abhängen, zuerst.*

1.
