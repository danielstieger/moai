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
- Persistente Speicherung aller produktiven Änderungen in DB.
- Interaktive DataUX-Anwendung mit Hauptmenü und den in diesem Dokument festgelegten Oberflächen.
- Manuell ausführbare OFX Test Suits für reproduzierbare Testdatensätze; kein automatischer Datenaufbau beim Start.
- Integrationstests für Repository- und Command-Abläufe.

Nicht Bestandteil von v1: Terminplanung, Abrechnung, Medikamente, Dokumente, Benutzerverwaltung, Mandantenfähigkeit, Löschfunktionen, Import/Export und externe Schnittstellen.


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

Gesetzte Kriterien werden logisch UND-verknüpft. Zusätzlich liste mit owner result.

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

# Zu diskutieren
- Implementierungsplan Repos / Services / Commands / UI
- Testplan Was testen, wo? warum? 


