from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sqlite3
import math



class DeactivateArticleType(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.parent = parent
        self.resize(300, 200)


        self.deactivateLayout = QVBoxLayout(self)

        self.deactivateComboB = QComboBox()
        self.deactivateButton = QPushButton("Deaktivieren")
        self.deactivateButton.clicked.connect(self.deactivateType)

        self.deactivateLayout.addWidget(self.deactivateComboB)
        self.deactivateLayout.addWidget(self.deactivateButton)

        conn = sqlite3.connect("db\\verleihverwaltung.db")
        query = f"""SELECT bezeichnung FROM artikeltyp WHERE aktiv = 1"""

        articleTypes = conn.execute(query).fetchall()
        conn.commit()
        conn.close()
        self.deactivateComboB.addItems([article[0] for article in articleTypes])


    def deactivateType(self):

        artikeltyp = self.deactivateComboB.currentText()
        conn = sqlite3.connect("db\\verleihverwaltung.db")
        query = f"""UPDATE artikeltyp SET aktiv = 0
                    WHERE bezeichnung = '{artikeltyp}' """

        conn.execute(query)
        conn.commit()
        conn.close()

        # Get artikeltyp_id um alle Seriennummern zu deaktivieren
        conn = sqlite3.connect("db\\verleihverwaltung.db")
        query = f""" SELECT artikeltyp_id from artikeltyp WHERE bezeichnung = '{artikeltyp}'"""

        artikelTypID = conn.execute(query).fetchall()[0][0]
        conn.commit()
        conn.close()

       

        # Deaktiviere alle zugehörigen Artikel

        conn = sqlite3.connect("db\\verleihverwaltung.db")
        query = f"""UPDATE artikel SET aktiv = 0
                    WHERE artikeltyp_id = '{artikelTypID}' """


        conn.execute(query)
        conn.commit()
        conn.close()

        self.close()

        



