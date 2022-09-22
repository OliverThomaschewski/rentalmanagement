from datetime import datetime, timedelta
from pickle import TRUE
import sqlite3
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *


class RentalInfo(QDialog):
    def __init__(self, parent, ausleihe_id):
        super().__init__(parent)
        self.parent = parent

        self.resize(300, 200)

        rentalinfo_query = f"""SELECT ausleiheninhalt.serien_nr, kontaktdaten.vorzuname, kontaktdaten.strasse, kontaktdaten.plz, kontaktdaten.stadt, ausleihe.startdatum, ausleihe.enddatum, kontaktdaten.email
                                FROM ausleihe
                                JOIN kontaktdaten ON kontaktdaten.kontaktdaten_id = ausleihe.kontaktdaten_id
                                JOIN ausleiheninhalt ON ausleiheninhalt.ausleihe_id = ausleihe.ausleihe_id
                                WHERE ausleiheninhalt.ausleihe_id = {ausleihe_id}"""

        conn = sqlite3.connect("db\\verleihverwaltung.db")
        rentalInfo = conn.execute(rentalinfo_query).fetchall()
        conn.commit()
        conn.close()

        serienNummern = []
        name = rentalInfo[0][1]
        strasse = rentalInfo[0][2]
        stadt = str(rentalInfo[0][3]) + " " + rentalInfo[0][4]
        startdatum = rentalInfo[0][5]
        enddatum = rentalInfo[0][6]
        email = rentalInfo[0][7]

        for article in rentalInfo:
            serienNummern.append(article[0])

        self.rentalInfoLayout = QHBoxLayout(self)

        self.articlesList = QListWidget()
        self.articlesList.addItems(serienNummern)

        self.rentalInfoLayout.addWidget(self.articlesList)

        self.adressLayout = QVBoxLayout()

        self.rentalInfoLayout.addLayout(self.adressLayout)

        # StartDatum Zeile

        self.startDateLayout = QHBoxLayout()

        self.startLabel = QLabel("Startdatum")
        self.startDateLabel = QLabel(startdatum)

        self.startDateLayout.addWidget(self.startLabel)
        self.startDateLayout.addWidget(self.startDateLabel)

        self.adressLayout.addLayout(self.startDateLayout)

        # Enddatum

        self.endDateLayout = QHBoxLayout()

        self.endLabel = QLabel("Enddatum")
        self.endDateLabel = QLabel(enddatum)

        self.endDateLayout.addWidget(self.endLabel)
        self.endDateLayout.addWidget(self.endDateLabel)

        self.adressLayout.addLayout(self.endDateLayout)

        # Adresse

        self.nameLabel = QLabel(name)
        self.adressLayout.addWidget(self.nameLabel)

        self.strasseLabel = QLabel(strasse)
        self.adressLayout.addWidget(self.strasseLabel)

        self.stadtLabel = QLabel(stadt)
        self.adressLayout.addWidget(self.stadtLabel)

        self.emailLabel = QLabel(email)
        self.adressLayout.addWidget(self.emailLabel)

        self.closeButton = QPushButton("Got It")
        self.closeButton.clicked.connect(self.closeDialog)
        self.rentalInfoLayout.addWidget(self.closeButton)

    def closeDialog(self):
        self.close()
