CREATE TABLE kontaktdaten(
    kontaktdaten_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vorzuname TEXT UNIQUE,
    strasse TEXT,
    plz INTEGER,
    stadt TEXT,
    email TEXT
    
);

CREATE TABLE artikeltyp(
    artikeltyp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    bezeichnung TEXT,
    wochenpreis REAL
);

CREATE TABLE artikel(
    serien_nr TEXT PRIMARY KEY,
    artikeltyp_id INTEGER REFERENCES artikeltyp(artikeltyp_id),
    aktiv INTEGER DEFAULT 1
    
);

CREATE TABLE ausleihe(
    ausleihe_id INTEGER PRIMARY KEY AUTOINCREMENT,
    kontaktdaten_id INTEGER REFERENCES kontaktdaten(kontaktdaten_id),
    gesamtpreis REAL,
    rechnungsdatum TEXT,
    startdatum TEXT,
    enddatum TEXT,
    versand INTEGER,
    bezahldatum TEXT,
    versanddatum TEXT,
    rueckgabedatum TEXT,
    storniert INTEGER DEFAULT 0
    --returnmail INTEGER DEFAULT 0
);

CREATE TABLE ausleiheninhalt(
    ausleihe_id INTEGER REFERENCES ausleihe(ausleihe_id),
    serien_nr TEXT REFERENCES artikel(serien_nr)
);


CREATE TABLE ausgabentyp (
    bezeichnung TEXT PRIMARY KEY
);

CREATE TABLE ausgaben (
    ausgaben_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ausgabentyp TEXT REFERENCES ausgabentyp(bezeichnung),
    datum TEXT,
    betrag REAL
);



CREATE TABLE versandkosten(
    bezeichnung TEXT UNIQUE,
    preis REAL
);

CREATE TABLE sonsteinnahmen(
    datum TEXT,
    bezeichnung TEXT,
    betrag REAL

);
