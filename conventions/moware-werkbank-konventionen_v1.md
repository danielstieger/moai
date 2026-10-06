## Verbindliche Konventionen

- **KONVENTION:** Unsere Ubiquitous Language ist Deutsch. Alles, was Fachlichkeit in der Software ausdrückt, wird konsistent mit deutschen Fachbegriffen benannt – insbesondere Namespaces, Datenmodelle, Services, Methoden, etc.
- **KONVENTION:** Ein `GRAPH_OWNER_CMD` darf seine editierbare Maske selbst halten, etwa beim Anlegen eines neuen Objekts. Lädt der Owner ein bestehendes Aggregat, hält er nur Session und Navigation; die editierbaren Masken öffnen `GRAPH_EDIT_CMD`s.
