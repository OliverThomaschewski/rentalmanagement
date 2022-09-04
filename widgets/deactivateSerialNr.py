from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sqlite3
import math



class DeactivateSerialNr(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        

        self.resize(300, 200)


        self.deactivateLayout = QVBoxLayout(self)

        self.TypeComboB = QComboBox()
        conn = sqlite3.connect("db\\verleihverwaltung.db")
        query = f"""SELECT bezeichnung FROM artikeltyp WHERE aktiv = 1"""
        self.TypeComboB.activated.connect(self.addSerials)
        data = conn.execute(query).fetchall()
        self.TypeComboB.addItems([i[0] for i in data])

        conn.close()


        self.SerialComboB = QComboBox()
        self.deactivateButton = QPushButton("Deaktivieren")
        self.deactivateButton.clicked.connect(self.deactivateSerial)

        self.deactivateLayout.addWidget(self.TypeComboB)
        self.deactivateLayout.addWidget(self.SerialComboB)
        self.deactivateLayout.addWidget(self.deactivateButton)

    def deactivateSerial(self):

        serialNr = self.SerialComboB.currentText()
        conn = sqlite3.connect("db\\verleihverwaltung.db")
        query = f"""UPDATE artikel SET aktiv = 0
                    WHERE serien_nr = '{serialNr}' """

        conn.execute(query)
        conn.commit()
        conn.close()

        self.close()


    def addSerials(self):
        
        artikelTyp = self.TypeComboB.currentText()
        # Artikeltyp_id besorgen

        conn = sqlite3.connect("db\\verleihverwaltung.db")
        query = f""" SELECT artikeltyp_id from artikeltyp WHERE bezeichnung = '{artikelTyp}'"""

        artikelTypID = conn.execute(query).fetchall()[0][0]
        conn.commit()
        conn.close()

        conn = sqlite3.connect("db\\verleihverwaltung.db")
        query = f"""SELECT serien_nr 
                    FROM artikel 
                    WHERE aktiv = 1 AND artikeltyp_id = {artikelTypID}"""

        data = conn.execute(query).fetchall()
        self.SerialComboB.addItems([i[0] for i in data])

        conn.close()