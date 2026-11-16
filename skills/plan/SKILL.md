---
name: plan
description: Einen MoWare-Bereich planen, bevor er modelliert wird. Verwenden, wenn der Nutzer `moai:plan` aufruft, einen neuen Bereich, ein Aggregat, einen Use Case oder eine Anwendung planen, entwerfen oder spezifizieren will oder eine Anforderung übergibt, die noch nicht modelliert ist. Füllt ein festes Template von innen nach außen aus (domain, read, tests, unit, app), fragt statt zu raten, schreibt den Plan in eine Datei und hält vor jeder Änderung in MPS für die Freigabe an.
---

# Einen MoWare-Bereich planen

Ein Plan beschreibt genau einen Bereich. Er steht als Datei im Anwendungsprojekt, folgt dem Template Abschnitt für Abschnitt und wird vom Nutzer freigegeben, bevor modelliert wird. Eine neue Anwendung oder ein neuer Bounded Context bekommt zuerst einen Zuschnitt-Plan, danach je Bereich einen Bereichsplan.

## Kritische Regeln

- **Vor der Freigabe des Plans wird in MPS nichts geändert.** Modelle lesen ist erlaubt.
- **Fachliches wird nie geraten.** Was weder die Anforderung noch die Konventionen noch ein vorhandenes Modell beantworten, wird gefragt. Was danach noch offen ist, steht als `KLÄREN: <Frage>` an der Stelle, an der es gebraucht wird, und gesammelt unter „Offene Fragen“. Ein Plan mit einer `KLÄREN:`-Markierung hat den Status „Entwurf“ und kann nicht freigegeben werden.
- **Das Template wird vollständig und in seiner Reihenfolge ausgefüllt.** Kein Abschnitt wird gelöscht; trifft einer nicht zu, steht dort „entfällt“ mit dem Grund.
- **Eine Abweichung von einer Konvention** steht nur im Abschnitt „Abweichungen von Konventionen“ und ist eine Entscheidung des Nutzers, nie des Agenten.
- Der Plan ist in der Fachsprache des Projekts geschrieben (Konventionen `allgemein`).

## Ablauf

1. **Eingabe.** Die Anforderung und der Bereich. Ist der Bereich nicht genannt oder sind Anwendung oder Bounded Context neu, zuerst den Zuschnitt planen mit [templates/zuschnitt.md](templates/zuschnitt.md); sonst [templates/bereich.md](templates/bereich.md).
2. **Lesen.** Alle Konventionen; `docu/moware-werkbank.md`; die Kapitellandkarten der drei DSL-Dokumente; danach nur die Teile der Dokumentation, die der Bereich berührt. Mit dem Argument `full` alle vier Dokumente vollständig. Wo Konventionen und Dokumentation liegen, steht im Sitzungskontext.
3. **Vorbild ansehen.** Einen vollständigen, konventionskonformen Bereich zeigen die Modelle `org.modellwerkstatt.wbkit.examples.fuhrparkapp.*` (ausgelieferte Solution `org.modellwerkstatt.wbkit`, nur lesbar): welche Roots in `domain`, `read`, `tests`, `unit` und `app` entstehen und wie sie heißen.
4. **Bestand ansehen.** Modelle und Roots des Bereichs mit `mps_mcp_get_project_structure` (`includeRootNodes`, `nodeDetail: "names"`) auflisten, damit der Plan Neues von Geändertem trennt. Eine Root nur lesen, wenn der Plan von ihrem Inhalt abhängt.
5. **Fragen, in einer Runde.** Alle fachlichen Lücken sammeln und dem Nutzer gemeinsam stellen. Eine fachliche Lücke ist zum Beispiel ein Wertebereich, ein Pflichtfeld, ein Schlüssel, ein Statusübergang und seine Bedingung, ein Recht, das Verhalten im Fehlerfall. Nicht gefragt wird, was die Konventionen bereits entscheiden.
6. **Template ausfüllen**, von oben nach unten, in die Datei `plan/<bereich>.md` (Zuschnitt: `plan/zuschnitt.md`) im Anwendungsprojekt, außerhalb von `moai_plugin/`. Die Akzeptanzkriterien nummerieren; Regeln und Tests verweisen auf diese Nummern. Die kursiven Hinweise ersetzen; Überschriften und Tabellenköpfe bleiben unverändert.
7. **Offenes markieren** mit `KLÄREN:` und unter „Offene Fragen“ aufführen.
8. **Anhalten.** Den Plan vorlegen: seinen Pfad, die offenen Fragen und die Abweichungen von Konventionen. Auf den Nutzer warten. Nach Antworten die Datei aktualisieren und erneut vorlegen; den Status erst auf „freigegeben“ setzen, wenn der Nutzer ausdrücklich freigibt und keine `KLÄREN:`-Markierung mehr steht.
9. **Übergeben.** In der Reihenfolge des Abschnitts „Reihenfolge der Umsetzung“ mit den DSL-Skills modellieren. Die Abschnitte 2, 3, 6 und 7 enthalten, was `moai_plugin/tools/scaffold.py` für seine Spezifikation braucht (`aggregat`, `werteobjekte`, `status`, `uebergaenge`, `testfaelle`, `suche`).
10. **Am Ende abgleichen.** Jede geplante Root und jeder geplante Test existiert; was über den Plan hinaus entstanden ist, wird in der Plandatei nachgetragen.
