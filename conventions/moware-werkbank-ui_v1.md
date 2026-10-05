## Verbindliche Konventionen für Benutzeroberflächen

- **KONVENTION:** Jede Page eines Commands setzt einen Page Title.
- **KONVENTION:** Eine Oberfläche wird nicht in einen linken und einen rechten Bereich aufgeteilt. Jedes UI-Element verwendet die volle Breite (100 %); mehrere Elemente stehen untereinander. Das gilt für UI-Elemente wie Formulare, Tabellen und Layouts, nicht für die Spalten innerhalb eines Formulars oder einer Tabelle.
- **KONVENTION:** Menüeinträge eines Page Pane oder einer Tabelle stehen in einem `Submenu` (Overflow-Menü), auch die Hauptaktion der Tabelle mit Hotkey `ENTER`. Das `Submenu` auf oberster Ebene hat keinen Text.
- **KONVENTION:** Ein `Delegate Form`, das in ein `Grid Layout` eingebunden ist, erhält als Zeilengewicht immer `-1` (`MinWeight`, minimale Höhe). Den verbleibenden Platz bekommen die Tabellen.
- **KONVENTION:** Jede Tabelle setzt mit `LABEL` eine Beschriftung, die sagt, was sie anzeigt. Ausgenommen ist eine Tabelle als oberstes Element eines `Page Pane`; dort kommt die Beschriftung aus dem Page Title.
