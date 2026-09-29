# MoAI – Agent Plugin für modellwerkstatt MoWare

MoAI bündelt Agent-Skills und Dokumentation für die drei MoWare-Sprachen
ObjectFlow, ManMap und DataUX sowie wiederverwendbare Arbeitsabläufe für
JetBrains MPS. Das Paket ist dafür vorgesehen, als versioniertes Git-Submodule
in einem MoWare-Anwendungsprojekt zu liegen und zugleich als Agent-Plugin
installiert zu werden.

## Inhalt

```text
moai/
├── .codex-plugin/plugin.json   Codex-Kompatibilitätsmanifest
├── skills/                     MoWare- und MPS-Skills
├── docu/                       Architektur- und Sprachdokumentation
├── MPS_AGENT_GUIDE.md          Allgemeine MPS-Arbeitsregeln
└── PROJECT_AGENTS.md           Vorlage für das Anwendungsprojekt
```

Die MoWare-Skills sind:

- `objectflow-dsl` für Fachmodell, Services, Commands, Tests und Konfiguration;
- `manmap-dsl` für Persistenzabbildungen, Repositories, Queries und SQL;
- `dataux-dsl` für Oberflächen, Anwendungen und Batchjobs.

Zusätzliche MPS-Skills unterstützen Node Editing, BaseLanguage,
Modellmanipulation, Sprachuntersuchung, MPS Console und Run-Konfigurationen.
`mps-mcp-workflow` ist der Einstiegspunkt für MPS-Arbeiten.

`mps-dsl-memory` ist ein explizit aufzurufender Maintainer-Skill. Er ist nicht
für die automatische Aktualisierung durch Paketnutzer oder Projekt-Agenten
bestimmt.

## Dokumentation

- [MoWare-Werkbank](docu/moware-werkbank.md) – Architektur und Zusammenspiel;
- [ObjectFlow](docu/objectflow.md) – Fachmodell und Geschäftslogik;
- [ManMap](docu/manmap.md) – relationale Persistenz und Repositories;
- [DataUX](docu/dataux.md) – Benutzeroberflächen, Anwendungen und Batchjobs.

Die Dokumentation beschreibt die beabsichtigte fachliche Semantik. Für die
technische AST-Struktur, Roles, Kardinalitäten, Referenzen und Prüfregeln sind
die geladenen MPS-Sprachmodelle maßgeblich.

## Einbindung als Git-Submodule

Im Root des Anwendungsprojekts:

```bash
git submodule add https://github.com/danielstieger/moai.git moai
git submodule update --init --recursive
```

Anschließend `moai/PROJECT_AGENTS.md` als `AGENTS.md` in das Projekt-Root
kopieren oder mit einer vorhandenen `AGENTS.md` zusammenführen. Die Vorlage
kennzeichnet `moai/` als paketierte Abhängigkeit und verweist Agenten auf die
installierten MoAI-Skills und die Dokumentation.

## Aktualisierung

Das Anwendungsprojekt bestimmt über seinen Submodule-Commit, welche MoAI-Version
verwendet wird. Eine Aktualisierung wird im Anwendungsprojekt durchgeführt und
anschließend als neuer Submodule-Stand versioniert:

```bash
git submodule update --remote --merge moai
git add moai
```

Paketdateien unter `moai/` werden bei gewöhnlicher Anwendungsentwicklung nicht
direkt verändert. Projektspezifische Anweisungen und Skills bleiben außerhalb
des Submodules.

## Voraussetzungen

- JetBrains MPS mit geöffnetem Zielprojekt;
- aktivierte MPS-MCP-Integration für modellbewusste Agent-Arbeit;
- installiertes und aktiviertes MoAI-Plugin in der verwendeten Agent-Runtime.
