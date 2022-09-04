from collections import namedtuple
from datetime import date, datetime, timedelta
from pickle import NONE, TRUE
import random
import sqlite3
from tabnanny import check
import pandas as pd
import numpy as np




rentals_query = f"""SELECT *
                    FROM ausleihe 
                    WHERE rueckgabedatum IS NULL
                """


conn = sqlite3.connect("db\\verleihverwaltung.db")
cursor = conn.cursor()
data = cursor.execute(rentals_query).fetchall()


conn.commit()
cursor.close()

print(data)


SELECT artikel.serien_nr, artikeltyp.bezeichnung, ausleihe.startdatum, ausleihe.enddatum
FROM artikel
JOIN artikeltyp ON artikeltyp.artikeltyp_id = artikel.artikeltyp_id
LEFT JOIN ausleiheninhalt ON ausleiheninhalt.serien_nr = artikel.serien_nr
LEFT JOIN ausleihe ON ausleihe.ausleihe_id = ausleiheninhalt.ausleihe_id
WHERE artikeltyp.bezeichnung = 'Testartikel' AND (ausleihe.enddatum >= date() OR ausleihe.enddatum = NULL)

