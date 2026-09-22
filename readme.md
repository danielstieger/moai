# MoAI – Dokumentation der modellwerkstatt MoWare-Werkbank

Dieses Repository bündelt die Dokumentation der **modellwerkstatt MoWare-Werkbank** und ihrer drei eng verzahnten domänenspezifischen Sprachen. Die auf JetBrains MPS basierende Werkbank unterstützt die Entwicklung von Geschäftsanwendungen vom fachlichen Modell über Persistenz und Anwendungsabläufe bis zur Benutzeroberfläche und zum ausführbaren Modul.

Die Architektur orientiert sich an ausgewählten Prinzipien des Domain-Driven Design: ObjectFlow beschreibt fachliche Daten, Regeln und Anwendungsfälle, ManMap verbindet diese Modelle mit relationalen Datenbanken, und DataUX macht sie in Oberflächen, Anwendungen und Batchjobs nutzbar. Generatoren und Laufzeitkomponenten übernehmen wiederkehrende technische Aufgaben, damit Fachbegriffe und Geschäftslogik im Modell sichtbar bleiben.

| Bereich | Verantwortung | Zentrale Konzepte | Dokumentation |
| --- | --- | --- | --- |
| **MoWare-Werkbank** | Architektur, Zusammenspiel der DSLs, Laufzeiten und Entwicklungsablauf | Fachmodell, Persistenz, UI, Generatoren | [Überblick](moware-werkbank.md) |
| **ObjectFlow**<br>`org.modellwerkstatt.objectflow` | Fachliche Datenstrukturen, Geschäftslogik, Commands und Querschnittsthemen | `Entity`, `ValueObject`, `DTO`, `Service`, `Command`, `OFXConfig`, `OFXTestSuit` | [Sprachreferenz](objectflow.md) |
| **ManMap**<br>`org.modellwerkstatt.manmap` | Relationale Persistenz, Repositories, explizites Laden und SQL-basierte Lesemodelle | `PersistenceDescription`, `EntityMapping`, `Repository`, `QueryFromMap`, `C2SqlBlock` | [Sprachreferenz](manmap.md) |
| **DataUX**<br>`org.modellwerkstatt.dataux` | Benutzeroberflächen sowie ausführbare Anwendungen und Batchjobs | `PagePane`, `DelegateForm`, `Table`, `AppUiModule`, `BatchJobModule` | [Sprachreferenz](dataux.md) |

Im Zusammenspiel definiert ObjectFlow den fachlichen Kern und koordiniert einen Anwendungsfall als Command. ManMap lädt die dafür benötigten Objektgraphen oder Lesemodelle und registriert Speicheroperationen in der ObjectFlow-Session. DataUX bindet die bereitgestellten Daten an Page Panes, Formulare und Tabellen; ein `AppUiModule` oder `BatchJobModule` bildet schließlich den ausführbaren Rahmen. Die Zuständigkeiten bleiben bewusst getrennt: Datenzugriff gehört in Repositories, wiederverwendbare Fachlogik in Datenstrukturen oder Services und Darstellung in DataUX.

Aus den MPS-Modellen wird Java-Code für unterschiedliche Einsatzgebiete generiert. UI-Anwendungen können als JavaFX-Desktop-Anwendung, Vaadin-Webanwendung oder schlanke HTML5-Anwendung für mobile Geräte betrieben werden; Batchjobs unterstützen automatisierte und interaktive Ausführung. Fachliche Tests lassen sich mit ObjectFlow-Testsuiten modellieren und über die MPS-Konsole ausführen.

Die Dokumentation richtet sich an Anwendungsentwickler und KI-Agenten. Der Überblick erklärt Architektur und Modellierungsentscheidungen, während die drei Sprachreferenzen Konzepte, Regeln, typische Abläufe, Fehlerbilder und technische Konzeptnamen vertiefen. Maßgebliche technische Quelle bleiben die geladenen MPS-Sprachdefinitionen und ihre Prüfregeln; die Dokumente dienen als verständliche und navigierbare Arbeitsgrundlage.
