# PetClinic – vollständige Implementierungsspezifikation für MoWare

Dieses Dokument ist die verbindliche Implementierungsvorgabe für eine PetClinic-Anwendung auf Basis der MoWare-Werkbank. Ein umsetzender Agent, der Zugriff auf die vorhandene MoWare-Dokumentation hat, soll daraus die Anwendung vollständig modellieren, generieren, testen und lauffähig machen können, ohne weitere fachliche oder architektonische Entscheidungen treffen zu müssen.

Normative technische Quellen: objectflow.md, manmap.md, dataux.md und moware-werkbank.md. Dieses Dokument definiert die fachlichen und projektspezifischen Entscheidungen. Die genannten Dokumentationen definieren Syntax, Konzepte, Child-Roles, Constraints und Laufzeitsemantik. Bei technischen Abweichungen ist die geladene MPS-Sprachdefinition maßgeblich; die fachlichen Entscheidungen dieses Dokuments bleiben verbindlich.

| Attribut | Vorgabe |
| --- | --- |
| Dokumentstatus | Implementierungsvorgabe v1.0 |
| Produktname | PetClinic |
| Basis-Namensraum | org.modellwerkstatt.petclinic |
| Zielplattform | MoWare / JetBrains MPS 2026.1 |
| Datenbank | mariadb |
| UI | DataUX AppUI |
| Löschfunktionen | Nicht Bestandteil von v1 |
| Rollen/Berechtigungen | Keine fachlichen Rollen in v1; Commands ohne Permissions |

# 1. Lieferumfang

- Tierhalter suchen, neu anlegen, öffnen und bearbeiten.
- Haustiere eines Tierhalters anzeigen, neu anlegen und bearbeiten.
- Besuche eines Haustiers anzeigen, neu anlegen und bearbeiten.
- Tierärzte anzeigen, neu anlegen und bearbeiten.
- Tierarten anzeigen, neu anlegen und bearbeiten.
- Persistente Speicherung aller produktiven Änderungen in Oracle.
- Interaktive DataUX-Anwendung mit Hauptmenü und den in diesem Dokument festgelegten Oberflächen.
- Manuell ausführbare OFX Test Suits für reproduzierbare Testdatensätze; kein automatischer Datenaufbau beim Start.
- Integrationstests für Repository- und Command-Abläufe.

Nicht Bestandteil von v1: Terminplanung, Abrechnung, Medikamente, Dokumente, Benutzerverwaltung, Mandantenfähigkeit, Löschfunktionen, Import/Export und externe Schnittstellen.

# 2. Projektstruktur und Namenskonventionen

| Modell / Bereich | Inhalt |
| --- | --- |
| org.modellwerkstatt.petclinic.domain | ObjectFlow Entities und DTOs |
| org.modellwerkstatt.petclinic.persistence | ManMap Persistence Description und Repositories |
| org.modellwerkstatt.petclinic.commands | ObjectFlow Commands |
| org.modellwerkstatt.petclinic.ui | DataUX Page Panes und AppUI Module |
| org.modellwerkstatt.petclinic.config | OFX Config |
| org.modellwerkstatt.petclinic.tests | OFX Test Suits |

- ObjectFlow-Datenmodell: PetClinic Domain
- Persistence Description: PetClinic Persistence
- Repositories: OwnerRepository, PetTypeRepository, VetRepository
- OFX Config: PetClinic Config
- AppUI Module: PetClinic
- TestSuites: PetClinic Stammdaten, PetClinic Beispieldaten, PetClinic Integrationstests

Command-Namen werden entsprechend der ObjectFlow-Konvention mit Leerzeichen modelliert, nicht als CamelCase. Java-/technische Klassennamen, die generatorseitig entstehen, werden nicht manuell abweichend benannt.

# 3. Fachliches Datenmodell

## 3.1 Aggregatgrenzen

```text
Owner
└── Pet*
    └── Visit*

PetType       eigenständige Referenz-Entity
Vet           eigenständige Referenz-Entity
```

Owner ist Aggregate Root. Pet und Visit gehören zum Lebenszyklus des Owner-Aggregats. PetType und Vet sind eigenständige Referenz-Entities. Es werden keine weiteren Aggregate eingeführt.

- Owner.pets ist CONTAINMENT; Pet.owner ist OPPOSITE.
- Pet.visits ist CONTAINMENT; Visit.pet ist OPPOSITE.
- Pet.type ist eine normale Entity-Referenz.
- Visit.vet ist eine normale Entity-Referenz.

## 3.2 Entity Owner

| Property | Typ | Optionen / fachliche Vorgabe |
| --- | --- | --- |
| id | int | KEY; AUTOID; Sequence PC_OWNER_SEQ |
| firstName | string | LENGTH 1..30; Pflicht |
| lastName | string | LENGTH 1..30; Pflicht |
| address | string | LENGTH 1..255; Pflicht |
| city | string | LENGTH 1..80; Pflicht |
| telephone | string | LENGTH 1..20; Pflicht |
| pets | list<Pet> | CONTAINMENT; Rückreferenz Pet.owner |

- Alle Stringwerte werden vor Validierung und Speicherung getrimmt.
- firstName, lastName, address, city und telephone dürfen danach nicht leer sein.
- telephone wird als fachlicher String gespeichert; v1 erzwingt kein Telefonnummernformat.

## 3.3 Entity Pet

| Property | Typ | Optionen / fachliche Vorgabe |
| --- | --- | --- |
| id | int | KEY; AUTOID; Sequence PC_PET_SEQ |
| name | string | LENGTH 1..30; Pflicht |
| birthDate | LocalDate | Pflicht |
| type | PetType | Pflichtreferenz |
| owner | Owner | OPPOSITE zu Owner.pets |
| visits | list<Visit> | CONTAINMENT; Rückreferenz Visit.pet |

- name wird getrimmt und darf nicht leer sein.
- birthDate darf nicht nach dem aktuellen lokalen Datum liegen.
- type und owner müssen gesetzt sein.
- Innerhalb eines Owners darf es nicht zwei Pets mit gleichem Namen (case-insensitive, getrimmt) und gleichem birthDate geben.

## 3.4 Entity Visit

| Property | Typ | Optionen / fachliche Vorgabe |
| --- | --- | --- |
| id | int | KEY; AUTOID; Sequence PC_VISIT_SEQ |
| visitDate | LocalDate | Pflicht |
| description | string | LENGTH 1..1000; Pflicht |
| pet | Pet | OPPOSITE zu Pet.visits |
| vet | Vet | Pflichtreferenz |

- visitDate darf nicht vor pet.birthDate liegen.
- visitDate darf nicht nach dem aktuellen lokalen Datum liegen.
- description wird getrimmt und darf nicht leer sein.
- pet und vet müssen gesetzt sein.

## 3.5 Entity PetType

| Property | Typ | Optionen / fachliche Vorgabe |
| --- | --- | --- |
| id | int | KEY; AUTOID; Sequence PC_PET_TYPE_SEQ |
| name | string | LENGTH 1..40; fachlich eindeutig; Pflicht |

- name wird getrimmt.
- Leere Namen sind unzulässig.
- Eindeutigkeit wird case-insensitive geprüft.
- PetType wird in v1 nicht gelöscht.

## 3.6 Entity Vet

| Property | Typ | Optionen / fachliche Vorgabe |
| --- | --- | --- |
| id | int | KEY; AUTOID; Sequence PC_VET_SEQ |
| firstName | string | LENGTH 1..30; Pflicht |
| lastName | string | LENGTH 1..30; Pflicht |

- firstName und lastName werden getrimmt und dürfen nicht leer sein.
- Vet wird in v1 nicht gelöscht.

## 3.7 DTO OwnerSearchCriteria

| Property | Typ | Semantik |
| --- | --- | --- |
| lastName | string | Leerer String = kein Filter; sonst case-insensitive Teilstring |
| telephone | string | Leerer String = kein Filter; sonst Teilstring |
| petName | string | Leerer String = kein Filter; sonst case-insensitive Teilstring |

Gesetzte Kriterien werden logisch UND-verknüpft.

## 3.8 DTO OwnerSearchResult

| Property | Typ |
| --- | --- |
| ownerId | int |
| firstName | string |
| lastName | string |
| city | string |
| telephone | string |
| petCount | int |

OwnerSearchResult ist ausschließlich Lesemodell und wird niemals gespeichert.

# 4. Relationales Datenmodell

Wird vom Entwickler automatisch aus MPS generiert! Wichtig ist, dass die Entity-Mappings dazu korrekt ausgeführt worden sind. 

# 5. ManMap-Persistenz

## 5.1 Persistence Description PetClinic Persistence

| Entity | Tabelle | Mappings |
| --- | --- | --- |
| Owner | PC_OWNER | id→OWNER_ID; firstName→FIRST_NAME; lastName→LAST_NAME; address→ADDRESS; city→CITY; telephone→TELEPHONE; pets als ListMapping über Pet.owner |
| PetType | PC_PET_TYPE | id→PET_TYPE_ID; name→NAME |
| Pet | PC_PET | id→PET_ID; name→NAME; birthDate→BIRTH_DATE; owner als ReferenceMapping→OWNER_ID; type als ReferenceMapping→PET_TYPE_ID; visits als ListMapping über Visit.pet |
| Vet | PC_VET | id→VET_ID; firstName→FIRST_NAME; lastName→LAST_NAME |
| Visit | PC_VISIT | id→VISIT_ID; visitDate→VISIT_DATE; description→DESCRIPTION; pet als ReferenceMapping→PET_ID; vet als ReferenceMapping→VET_ID |

Alle schreibbaren Entity-Mappings erhalten optimistic, sofern die geladene Sprache dies für das konkrete Mapping zulässt. Auto-ID wird über die in Kapitel 3 angegebenen Sequences modelliert.

## 5.2 OwnerRepository

| Methode | Typ | Verbindliches Verhalten |
| --- | --- | --- |
| searchOwners(criteria) | READONLY | Custom SQL; liefert list<OwnerSearchResult> |
| checkoutOwner(ownerId) | CHECKOUT | lädt Owner inkl. pets, Pet.type, Pet.visits und Visit.vet explizit |
| saveOwner(owner) | CHECKIN | speichert ausschließlich PC_OWNER |
| savePet(pet) | CHECKIN | speichert ausschließlich PC_PET |
| saveVisit(visit) | CHECKIN | speichert ausschließlich PC_VISIT |

checkoutOwner darf kein Lazy Loading voraussetzen. Alle für die Owner-Übersicht benötigten Referenzen und Listen müssen innerhalb der Query-/Join-Struktur explizit geladen werden.

## 5.3 PetTypeRepository

| Methode | Typ | Verhalten |
| --- | --- | --- |
| listAll() | READONLY | alle PetTypes, sortiert nach name |
| findByName(name) | READONLY | case-insensitive exakter Name; maximal ein Ergebnis |
| checkoutById(id) | CHECKOUT | PetType zur Bearbeitung |
| save(petType) | CHECKIN | PetType speichern |

## 5.4 VetRepository

| Methode | Typ | Verhalten |
| --- | --- | --- |
| listAll() | READONLY | sortiert nach lastName, firstName |
| search(name) | READONLY | case-insensitive Teilstring über firstName oder lastName |
| checkoutById(id) | CHECKOUT | Vet zur Bearbeitung |
| findByFullName(firstName,lastName) | READONLY | exakte getrimmte Namen, für Testdatensatz-Erzeugung |
| save(vet) | CHECKIN | Vet speichern |

## 5.5 Speicherreihenfolge Owner-Aggregat

1. OwnerRepository.saveOwner(owner)
2. Für jedes Pet in owner.pets: OwnerRepository.savePet(pet)
3. Für jedes Pet in owner.pets und jeden Visit in pet.visits: OwnerRepository.saveVisit(visit)

Der Session Owner registriert diese Operationen in dieser Reihenfolge. GRAPH_EDIT_CMDs registrieren keine Session-Operationen.

# 6. ObjectFlow Commands

## 6.1 Allgemeine Vorgaben

- Kein Command enthält in v1 CAN_OPEN_RO oder CAN_OPEN_RW.
- Ändernde Unterabläufe sind GRAPH_EDIT_CMDs und verwenden die Session des Graph Owners.
- Nur Session Owner registrieren Persistenzoperationen.
- Validierungsfehler werden als korrigierbare Preconditions/Validierungen mit den in diesem Dokument festgelegten Meldungen ausgegeben.
- Neue Child-Entities werden erst nach erfolgreicher Validierung an ihre Containment-Liste angehängt.

## 6.2 Owners suchen

| Aspekt | Vorgabe |
| --- | --- |
| Typ | SEARCH_CMD |
| Variablen | criteria : OwnerSearchCriteria; results : list<OwnerSearchResult> |
| command init | criteria neu anlegen; results = searchOwners(criteria); Page Suche öffnen |
| Conclusion Suchen | Kriterien trimmen; results neu laden; auf Page bleiben |
| Conclusion Schließen | done |

Aktionen: Owner neu anlegen; Owner öffnen mit ownerId aus der selektierten Ergebniszeile.

## 6.3 Owner neu anlegen

| Aspekt | Vorgabe |
| --- | --- |
| Typ | GRAPH_OWNER_CMD_MODAL |
| Variable | owner : Owner |
| command init | new Owner(); Page Owner |
| Speichern | trimmen, validieren, done |
| FINAL_OK | saveOwner(owner) registrieren; owner pushen |

Fehlermeldungen: „Vorname ist erforderlich.“, „Nachname ist erforderlich.“, „Adresse ist erforderlich.“, „Ort ist erforderlich.“, „Telefon ist erforderlich.“

## 6.4 Owner öffnen

| Aspekt | Vorgabe |
| --- | --- |
| Typ | GRAPH_OWNER_CMD |
| Parameter | ownerId : int |
| Variable | owner : Owner |
| command init | checkoutOwner(ownerId); falls nicht vorhanden: „Der Tierhalter existiert nicht.“; Page Übersicht |
| Revert | owner als Graph-Wurzel bei FINAL_CANCEL/USER_CANCEL |
| FINAL_OK | Speicheroperationen gemäß 5.5 registrieren; owner pushen |

## 6.5 Owner bearbeiten

Typ GRAPH_EDIT_CMD; Parameter owner : Owner; Revert-Wurzel owner. Page Owner. Conclusion Übernehmen trimmt und validiert, dann done. Abbrechen ist USER_CANCEL. Keine Session-Operationen.

## 6.6 Pet hinzufügen

Typ GRAPH_EDIT_CMD; Parameter owner : Owner; lokale Variable pet : Pet. command init erzeugt Pet und setzt pet.owner = owner. Page Pet. PetType-Auswahl stammt aus PetTypeRepository.listAll().

- Übernehmen validiert name, birthDate, type und Dublette.
- Bei Dublette: „Ein Haustier mit gleichem Namen und Geburtsdatum existiert bereits.“
- Erst nach erfolgreicher Validierung wird pet an owner.pets angehängt.
- Keine Session-Operationen.

## 6.7 Pet bearbeiten

Typ GRAPH_EDIT_CMD; Parameter owner : Owner und pet : Pet; Revert-Wurzel owner. Page Pet. Die Dublettenprüfung ignoriert die aktuell bearbeitete Instanz. Keine Session-Operationen.

## 6.8 Visit hinzufügen

Typ GRAPH_EDIT_CMD; Parameter owner : Owner und pet : Pet; lokale Variable visit : Visit. command init setzt visit.pet = pet und visit.visitDate auf das aktuelle lokale Datum. Vet-Auswahl stammt aus VetRepository.listAll().

- visitDate vor pet.birthDate: „Besuchsdatum liegt vor dem Geburtsdatum des Haustiers.“
- visitDate in Zukunft: „Besuchsdatum darf nicht in der Zukunft liegen.“
- fehlender Vet: „Tierarzt ist erforderlich.“
- leere description: „Beschreibung ist erforderlich.“
- Erst nach erfolgreicher Validierung an pet.visits anhängen.

## 6.9 Visit bearbeiten

Typ GRAPH_EDIT_CMD; Parameter owner : Owner und visit : Visit; Revert-Wurzel owner. Page Visit. Gleiche Validierung wie beim Anlegen. Keine Session-Operationen.

## 6.10 Pet Types anzeigen

Typ SEARCH_CMD. Variable petTypes : list<PetType>. command init lädt listAll() und öffnet Liste. Aktionen: Pet Type neu anlegen und Pet Type bearbeiten. Nach erfolgreicher Rückkehr aus einem Änderungsablauf wird die Liste neu geladen.

## 6.11 Pet Type neu anlegen

Typ GRAPH_OWNER_CMD_MODAL. Variable petType : PetType. Page Pet Type. name trimmen; leer -> „Tierart ist erforderlich.“; bestehender Name case-insensitive -> „Tierart existiert bereits.“ FINAL_OK registriert PetTypeRepository.save(petType).

## 6.12 Pet Type bearbeiten

Typ GRAPH_OWNER_CMD_MODAL. Parameter petTypeId : int. checkoutById; nicht gefunden -> „Tierart existiert nicht.“ Gleiche Validierung; eigene ID bei Eindeutigkeitsprüfung ignorieren. FINAL_OK speichert.

## 6.13 Tierärzte anzeigen

Typ SEARCH_CMD. Variablen name : string und vets : list<Vet>. Leerer Name lädt listAll(); gesetzter Name verwendet search(name). Aktionen New und Edit.

## 6.14 Tierarzt neu anlegen

Typ GRAPH_OWNER_CMD_MODAL. Neue Vet-Entity; Page Tierarzt; Pflichtvalidierung Vor-/Nachname. FINAL_OK registriert VetRepository.save(vet).

## 6.15 Tierarzt bearbeiten

Typ GRAPH_OWNER_CMD_MODAL. Parameter vetId : int. checkoutById; nicht gefunden -> „Tierarzt existiert nicht.“ Page Tierarzt; Pflichtvalidierung; FINAL_OK save(vet).

# 7. DataUX

## 7.1 AppUI Module PetClinic

| Element | Vorgabe |
| --- | --- |
| OFFICIAL NAME | PetClinic |
| VERSION | 1.0 |
| mainMenu 1 | Owners → Owners suchen |
| mainMenu 2 | Vets → Tierärzte anzeigen |
| mainMenu 3 | Pet Types → Pet Types anzeigen |
| Startup Commands | keine |

## 7.2 Page Pane Owners suchen

Oberstes Element: Grid Layout mit Suchformular oben und Ergebnistabelle unten.

| Bereich | Inhalt |
| --- | --- |
| Suchformular | OwnerSearchCriteria.lastName, telephone, petName |
| Tabelle | OwnerSearchResult.lastName, firstName, city, telephone, petCount |
| Aktionen | Search, New Owner, Open Owner, Close |

Open Owner ist nur bei selektierter Ergebniszeile enabled und übergibt getSelected().ownerId.

## 7.3 Page Pane Owner Übersicht

Oberstes Element: Tab Layout mit den Tabs Owner und Visits.

| Tab | Inhalt |
| --- | --- |
| Owner | Read-only Owner-Form + Tabelle Owner.pets mit SELECT FIRST |
| Visits | Read-only Form des selektierten Pet + Tabelle Pet.visits mit SELECT FIRST |

- Owner-Form: firstName, lastName, address, city, telephone.
- Pet-Tabelle: name, birthDate, type.
- Visit-Tabelle: visitDate, vet, description.
- Aktionen im Owner-Kontext: Edit Owner, Add Pet.
- Aktionen mit Pet-Selektion: Edit Pet, Add Visit.
- Aktion mit Visit-Selektion: Edit Visit.
- Page-weite Aktionen: Save & Close und Cancel.

## 7.4 Page Pane Owner

Delegate Form mit firstName, lastName, address, city, telephone. Zweispaltig; Reihenfolge exakt wie genannt.

## 7.5 Page Pane Pet

Delegate Form mit name, birthDate und type. type wird als Picker dargestellt.

## 7.6 Page Pane Visit

Delegate Form mit visitDate, vet und description. vet als Picker; description breit und mehrzeilig.

## 7.7 Page Pane Pet Types Liste

Tabelle mit Spalte name. Aktionen New und Edit.

## 7.8 Page Pane Pet Type

Formular mit einzigem Feld name.

## 7.9 Page Pane Tierärzte Liste

Grid Layout mit Suchfeld name und Tabelle lastName, firstName. Aktionen Search, New und Edit.

## 7.10 Page Pane Tierarzt

Formular mit firstName und lastName.

# 8. Konfiguration

## 8.1 PetClinic Config

- OwnerRepository konfigurieren.
- PetTypeRepository konfigurieren.
- VetRepository konfigurieren.
- Passende IOFXUserEnvironment-Implementierung konfigurieren.
- Passende IOFXUserServices-Implementierung konfigurieren.

Für Tests wird ein stabiler technischer Benutzer verwendet: userName = "petclinic-test", userId = 1. Es gibt keine PetClinic-Benutzerstammdaten und keine Rollenprüfung in v1.

## 8.2 Interaktive Authentifizierung

Die Anwendung übernimmt den von der Laufzeit gelieferten Benutzernamen in die User Environment. Falls keine fachliche Benutzer-ID verfügbar ist, verwendet v1 die technische ID 1. Das ist keine fachliche Identität und darf nicht als Domänenobjekt modelliert werden.

# 9. Manuell ausführbare OFX Test Suits

## 9.1 Verbindliche Testdaten-Strategie

Die Testsuites werden ausschließlich manuell ausgeführt. Es gibt keine Stammdatenlogik in on startup oder on shutdown. Jeder Simple Test baut die für seinen Test benötigten Daten explizit auf. Die erzeugten Daten müssen innerhalb der Test-Session vollständig nutzbar sein. Es wird nicht vorausgesetzt, dass ein Simple Test seine Session in die Datenbank committed; Persistenz außerhalb des Testlaufs ist kein Abnahmekriterium für diese TestSuites.

Damit sind die TestSuites reproduzierbare Testdatensatz-Erzeuger und keine produktiven Datenbank-Seeder.

## 9.2 TestSuite PetClinic Stammdaten

Enthält genau folgende Simple Tests. Jeder Test erzeugt seine Daten selbst; kein Test hängt von einem vorher gelaufenen Test ab.

| Test | Erzeugter Datensatz |
| --- | --- |
| PetType Dog | PetType(name=Dog) |
| PetType Cat | PetType(name=Cat) |
| PetType Bird | PetType(name=Bird) |
| PetType Hamster | PetType(name=Hamster) |
| PetType Reptile | PetType(name=Reptile) |
| Vet James Carter | Vet(James, Carter) |
| Vet Helen Leary | Vet(Helen, Leary) |
| Vet Linda Douglas | Vet(Linda, Douglas) |

Jeder Test prüft unmittelbar nach Erzeugung die gesetzten Properties und die fachliche Validierung. Ein Test darf keine Daten aus einem anderen Simple Test voraussetzen.

## 9.3 TestSuite PetClinic Beispieldaten

Jeder Simple Test erzeugt ein in sich geschlossenes Owner-Aggregat inklusive der benötigten PetType- und Vet-Referenzobjekte innerhalb derselben Test-Session.

| Test | Datensatz |
| --- | --- |
| George Franklin | Owner George Franklin, 110 W. Liberty St., Madison, 6085551023; Pet Leo, Dog, 2019-09-07; Visit 2025-03-14 bei James Carter, 'Annual checkup' |
| Betty Davis | Owner Betty Davis, 638 Cardinal St., Sun Prairie, 6085551749; Pet Basil, Cat, 2020-08-06; Visit 2025-02-10 bei Helen Leary, 'Skin irritation' |
| Eduardo Rodriguez | Owner Eduardo Rodriguez, 2705 N. Stoughton Rd., Madison, 6085558763; Pet Rosy, Dog, 2021-04-17; zwei Visits: 'Vaccination' und 'Dental check' bei Linda Douglas |

Datumswerte dürfen für die Ausführung nicht in der Zukunft liegen. Falls ein festgelegtes Visit-Datum zum Ausführungszeitpunkt in der Zukunft wäre, ist stattdessen aktuelles Datum minus 30 Tage zu verwenden. birthDate bleibt unverändert, sofern es weiterhin in der Vergangenheit liegt.

## 9.4 TestSuite PetClinic Integrationstests

- OwnerRepository searchOwners findet nach Nachname.
- OwnerRepository searchOwners findet nach Telefonnummer.
- OwnerRepository searchOwners findet über petName.
- checkoutOwner lädt Owner, Pets, PetType, Visits und Vet vollständig.
- Owner neu anlegen validiert alle Pflichtfelder.
- Pet hinzufügen verhindert Dublette gleicher Name + birthDate beim selben Owner.
- Pet hinzufügen verhindert birthDate in der Zukunft.
- Visit hinzufügen verhindert Datum vor birthDate.
- Visit hinzufügen verhindert Datum in der Zukunft.
- PetType verhindert case-insensitive Dublette.
- Owner öffnen + Owner bearbeiten: Abbruch stellt den ursprünglichen In-Memory-Zustand wieder her.
- Owner öffnen + Pet hinzufügen + erfolgreicher Abschluss registriert Owner/Pet/Visit-Speicheroperationen in definierter Reihenfolge.

Command-Tests verwenden run command und erzwingen die vorgesehenen Conclusions gemäß ObjectFlow-Dokumentation.

# 10. Fachliche Validierung – vollständige Meldungsliste

| Situation | Meldung |
| --- | --- |
| Owner.firstName leer | Vorname ist erforderlich. |
| Owner.lastName leer | Nachname ist erforderlich. |
| Owner.address leer | Adresse ist erforderlich. |
| Owner.city leer | Ort ist erforderlich. |
| Owner.telephone leer | Telefon ist erforderlich. |
| Pet.name leer | Name des Haustiers ist erforderlich. |
| Pet.birthDate fehlt | Geburtsdatum ist erforderlich. |
| Pet.birthDate Zukunft | Geburtsdatum darf nicht in der Zukunft liegen. |
| Pet.type fehlt | Tierart ist erforderlich. |
| Pet Dublette | Ein Haustier mit gleichem Namen und Geburtsdatum existiert bereits. |
| Visit.visitDate fehlt | Besuchsdatum ist erforderlich. |
| Visit vor Geburt | Besuchsdatum liegt vor dem Geburtsdatum des Haustiers. |
| Visit Zukunft | Besuchsdatum darf nicht in der Zukunft liegen. |
| Visit.vet fehlt | Tierarzt ist erforderlich. |
| Visit.description leer | Beschreibung ist erforderlich. |
| PetType.name leer | Tierart ist erforderlich. |
| PetType Dublette | Tierart existiert bereits. |
| Vet.firstName leer | Vorname ist erforderlich. |
| Vet.lastName leer | Nachname ist erforderlich. |
| Owner ID unbekannt | Der Tierhalter existiert nicht. |
| PetType ID unbekannt | Tierart existiert nicht. |
| Vet ID unbekannt | Tierarzt existiert nicht. |

# 11. Reihenfolge der Implementierung

1. ObjectFlow Entities und DTOs exakt gemäß Kapitel 3 modellieren.
2. Oracle-DDL aus Kapitel 4 anlegen.
3. ManMap Persistence Description und Mappings gemäß Kapitel 5.1 modellieren.
4. Repositories und alle genannten Methoden implementieren.
5. OFX Config erstellen und Repository-Komponenten verdrahten.
6. ObjectFlow Commands in der Reihenfolge Owners suchen, Owner neu anlegen, Owner öffnen, Owner bearbeiten, Pet hinzufügen/bearbeiten, Visit hinzufügen/bearbeiten, PetType-Commands, Vet-Commands erstellen.
7. DataUX Page Panes implementieren.
8. AppUI Module und Hauptmenü erstellen.
9. TestSuites aus Kapitel 9 implementieren.
10. Alle Abnahmekriterien aus Kapitel 12 ausführen.

# 12. Abnahmekriterien

- Die Anwendung startet ohne Modell-/Generatorfehler.
- Das Hauptmenü enthält genau Owners, Vets und Pet Types.
- Owner-Suche funktioniert mit leerem Filter sowie mit jedem einzelnen Filter und Kombinationen.
- Ein Owner kann angelegt, gespeichert, erneut gesucht und geöffnet werden.
- Ein Owner kann bearbeitet und gespeichert werden.
- Ein Pet kann innerhalb eines geöffneten Owners angelegt und bearbeitet werden.
- Ein Visit kann innerhalb eines ausgewählten Pets angelegt und bearbeitet werden.
- PetType und Vet können angelegt und bearbeitet werden.
- Die Owner-Übersicht zeigt nach checkoutOwner alle benötigten Daten ohne Lazy-Loading-Fehler.
- Cancel eines editierenden Child-Commands hinterlässt keine fachlich sichtbaren Änderungen im Owner-Graphen.
- Owner-Abbruch stellt den Owner-Graphen gemäß Revert-Konfiguration wieder her.
- Keine UI-Bindung führt implizite Datenbankabfragen aus.
- Keine GRAPH_EDIT_CMD-Implementierung registriert Session-Operationen.
- Es existieren keine Delete-Aktionen, Delete-Commands oder Delete-Repository-Methoden.
- Alle Validierungsmeldungen entsprechen exakt Kapitel 10.
- Alle TestSuites lassen sich manuell starten und enthalten keine automatische on-startup-Testdatenlogik.

# 13. Nicht zu implementieren

- Keine Specialties für Tierärzte.
- Keine Termin-/Kalenderfunktion.
- Keine Rechnung oder Zahlung.
- Keine Medikamente oder Behandlungen als eigene Stammdaten.
- Keine Benutzer-, Rollen- oder Rechteverwaltung.
- Keine Datenlöschung.
- Keine Soft-Delete-Flags.
- Keine REST-API.
- Keine Batchjobs.
- Keine Datei-Uploads.
- Keine zusätzlichen DTOs außer den ausdrücklich genannten, es sei denn, die MPS-Sprache erzwingt einen technischen Adaptertyp; ein solcher Typ darf keine neue Fachsemantik einführen.

# 14. Referenzen auf die vorhandene MoWare-Dokumentation

- moware-werkbank.md – Architektur und Zuständigkeit der drei DSLs.
- objectflow.md – Entity/DTO, CONTAINMENT/OPPOSITE, Commands, Session, Revert, TestSuit, Roles/Permissions.
- manmap.md – Entity-Mappings, Reference/List Mapping, Repositories, READONLY/CHECKOUT/CHECKIN, Custom SQL.
- dataux.md – Page Pane, Form/Table, Master-Detail-Selektion, Menüs, AppUI Module.

Der umsetzende Agent soll die Dokumentation nur für die technische Umsetzung der hier festgelegten Entscheidungen heranziehen. Er soll keine fachlichen Alternativen ergänzen oder Entscheidungen aus diesem Dokument neu interpretieren.
