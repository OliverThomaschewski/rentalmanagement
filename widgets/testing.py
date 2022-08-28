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