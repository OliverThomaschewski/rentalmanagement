# Verleihverwaltung 


## Inhaltsverzeichniss

1. [Beschreibung](#Beschreibung)

## Beschreibung

Das Programm gibt die Möglichkeit Ausleihen anzulegen und zu verwalten.


## Motivation

"Excel is ätzend"
"Ich studier doch Informatik, probier ich einfach mal rum"

## Stack

- Python (Benutzeroberfläche mit PYQT6)
- SQLite


## Installation

Die Installation erfolgt über das Kommando 

pyinstaller --onefile --noconsole -/Verleihverwaltung.py

Die Datenbank wird mit dem Code in dq.sql erstellt.

Zugangsdaten werden in einer credentials.env zur Verfügung gestellt.

## Funktionen der Programms

Im folgenden werden alle Funktionen und Besonderheiten bei der Bedienung erklärt.

### Tab "Neue Ausleihe"

Prüft die Verfügbarkeit der Artikel und Pakete und berechnet Gesamtpreise inklusive verschiedener Versandmöglichkeiten.

Derzeit muss die Reihenfolge Datum auswählen -> Versandart wählen -> Artikel hinzufügen eingehalten werden.
Zwar wird die Verfügbarkeit bei einer Änderung des Datums aktualisiert, wird allerdings zwischendurch die Versandart geändert, müssen die Artikel neu angeklickt werden.

Für eine effiziente Nutzung der Artikel werden aus allen verfügbaren Artikeln der mit der kleinsten Artikelnummer verwendet.

Pufferzeiten für den Versand und die Rückgabe werden wie folgt berechnet:

 - Bei Versand werden 3 Tage für den Versand und die Rückgabe zum Start - bzw. Enddatum hinzugefügt
 - Bei Abholung wird 1 Tag für die Abholung und 2 Tage für die Rückgabe hinzugefügt
 
Diese Pufferzeiten haben keinen Einfluss auf den Preis der Ausleihe.

Beim Speichern der Ausleihe wird automatisch eine PayPal - Rechnung über die PayPal API generiert und an den Ausleihenden verschickt.

### Tab "Aktive Ausleihen"

Enthält Übersicht über alle aktiven Ausleihen mit entsprechenden Angaben zum Versand und Rückgabedatum sortiert nach dem Startdatum der Ausleihe.

Über den Button ***Info*** können die Details der Ausleihe angezeigt werden. Ebenso gibt es die Möglichkeit, die Ausleihe zu stornieren.

Der Ausleiher erhält am letzten Tag seiner Ausleihe eine Email mit der Erinnerung für die Rückgabe.

Nachdem die Artikel zurückgegeben wurde, wird nach dem klicken aus "zurück erhalten" eine Bestätigungsmail an den Ausleiher geschickt.

*Update*

Der Tab wird beim öffnen des Programms geladen, somit werden neu angelegte Ausleihen nicht automatisch angezeigt, mit einem klick auf Update wird die neue Ausleihe am Ende angezeigt.



### Tab "Artikel Hinzufügen"


*Typ Hinzufügen*
Fügt einen neue Artikeltyp hinzu. Nach Angabe des Anschaffungspreises wird ein Wochenpreis vorgeschlagen, dieser kann aber geändert werden.

*Seriennummer*
Nach der Auswahl eines Typs kann ein neuer Artikel für diesen Typ mithilfe einer neuen Seriennummer angelegt werden.

*Typ deaktivieren*
Deaktivert einen gesamten Artikeltyp. Ist relevant, wenn ein Artikel komplett aus dem Verleihangebot genommen wird.

*SerienNr deaktivieren*
Deaktiviert nur eine bestimmte Seriennummer. Beispielsweise bei Verkauf oder Beschädigung des Artikels.

*Neuer Wochenpreis*

Gibt die Möglichkeit, den Wochenpreis eines schon vorhanden Artikels zu aktualisieren. Hierbei wird er in der Datenbank neu angelegt und der alte Eintrag inaktiv gesetzt. Somit wird der neue Preis nicht in den alten Ausleihen verwendet
was zu einer falschen Auswertung führen würde.

### Tab "Ausgaben"

Erfasst die Ausgaben mit dem entsprechenden Typ. Zeigt die letzten 10 Ausgaben an.

### Tab "Sonstige Einnahmen"

Hier können alle sonstigen Einnahmen hinterlegt werden, beispielweise durch den Verkauf von Ausleihartikeln oder Bezahlungen bei Beschädigungen von Artikeln.

### Tab "Special Ausleihe"

Gibt die Möglichkeit, Ausleihen unabhängig von der VErfügbarkeit zu hinterlegen. Dies ist nützlich, wenn sich das Rückgabedatum einer Ausleihe
mit dem Versanddatum einer anderen überschneidet und die Ausrüstung nach Rücksprache mit dem vorherigen Ausleiher früher zurückgegeben werden kann und die neue Ausleihe doch bedient werden kann.




## Zukünftige Funktionen

- Automatisches erstellen des Versandettikets und Email an den Ausleiher inklusive Trackingnummer


## "Bugs"

- Update der Verfügbarkeiten nach ändern der Versandart
- Automatisches neu Laden des "Aktive Ausleihen" Tabs
- Sonstige Einnahmen Tab mal schöner.

## Wäre cool, für den Scope aber egal

- Erstellen eines Benutzers mit automatischer Erstellung der Datenbank und Zugangsdaten




