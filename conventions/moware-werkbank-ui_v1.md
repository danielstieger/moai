## Verbindliche Konventionen für Benutzeroberflächen

- **KONVENTION:** Jede Page eines Commands setzt einen Page Title.
- **KONVENTION:** Eine Oberfläche wird nicht in einen linken und einen rechten Bereich aufgeteilt. Jedes UI-Element verwendet die volle Breite (100 %); mehrere Elemente stehen untereinander. Das gilt für UI-Elemente wie Formulare, Tabellen und Layouts, nicht für die Spalten innerhalb eines Formulars oder einer Tabelle.
- **KONVENTION:** Menüeinträge eines Page Pane oder einer Tabelle stehen in einem `Submenu` (Overflow-Menü), auch die Hauptaktion der Tabelle mit Hotkey `ENTER`. Das `Submenu` auf oberster Ebene hat keinen Text.
- **KONVENTION:** Ein `Delegate Form`, das in ein `Grid Layout` eingebunden ist, erhält als Zeilengewicht immer `-1` (`MinWeight`, minimale Höhe). Den verbleibenden Platz bekommen die Tabellen.
- **KONVENTION:** Jede Tabelle setzt mit `LABEL` eine Beschriftung, die sagt, was sie anzeigt. Ausgenommen ist eine Tabelle als oberstes Element eines `Page Pane`; dort kommt die Beschriftung aus dem Page Title.
- **KONVENTION:** Die Default-Conclusion eines Commands hat den Hotkey `F12`. Ihre Beschriftung richtet sich nach dem Command-Typ: „OK“ beim `GRAPH_EDIT_CMD`, „Aktualisieren“ beim `SEARCH_CMD`, „Speichern & Schließen“ beim `GRAPH_OWNER_CMD`.
- **KONVENTION:** In einem Wizard (Command mit mehreren Pages, die nacheinander durchlaufen werden) wechseln die Conclusions „Zurück“ mit Hotkey `F3` und „Weiter“ mit Hotkey `F4` die Page.
- **KONVENTION:** Ein `GRAPH_OWNER_CMD` darf seine editierbare Maske selbst halten, etwa beim Anlegen eines neuen Objekts. Lädt der Owner ein bestehendes Aggregat, hält er nur Session und Navigation; die editierbaren Masken öffnen `GRAPH_EDIT_CMD`s.