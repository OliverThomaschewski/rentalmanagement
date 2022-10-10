from datetime import datetime, timedelta
from pickle import TRUE
import sqlite3
import smtplib
from email.mime.text import MIMEText
import os
import dotenv

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

        self.serienNummern = []
        self.name = rentalInfo[0][1]
        self.strasse = rentalInfo[0][2]
        self.stadt = str(rentalInfo[0][3]) + " " + rentalInfo[0][4]
        self.startdatum = rentalInfo[0][5]
        self.enddatum = rentalInfo[0][6]
        self.email = rentalInfo[0][7]

        for article in rentalInfo:
            self.serienNummern.append(article[0])

        self.rentalInfoLayout = QHBoxLayout(self)

        self.articlesList = QListWidget()
        self.articlesList.addItems(self.serienNummern)

        self.rentalInfoLayout.addWidget(self.articlesList)

        self.adressLayout = QVBoxLayout()

        self.rentalInfoLayout.addLayout(self.adressLayout)

        # StartDatum Zeile

        self.startDateLayout = QHBoxLayout()

        self.startLabel = QLabel("Startdatum")
        self.startDateLabel = QLabel(self.startdatum)

        self.startDateLayout.addWidget(self.startLabel)
        self.startDateLayout.addWidget(self.startDateLabel)

        self.adressLayout.addLayout(self.startDateLayout)

        # Enddatum

        self.endDateLayout = QHBoxLayout()

        self.endLabel = QLabel("Enddatum")
        self.endDateLabel = QLabel(self.enddatum)

        self.endDateLayout.addWidget(self.endLabel)
        self.endDateLayout.addWidget(self.endDateLabel)

        self.adressLayout.addLayout(self.endDateLayout)

        # Adresse

        self.nameLabel = QLabel(self.name)
        self.adressLayout.addWidget(self.nameLabel)

        self.strasseLabel = QLabel(self.strasse)
        self.adressLayout.addWidget(self.strasseLabel)

        self.stadtLabel = QLabel(self.stadt)
        self.adressLayout.addWidget(self.stadtLabel)

        self.emailLabel = QLabel(self.email)
        self.adressLayout.addWidget(self.emailLabel)

        self.closeButton = QPushButton("Got It")
        self.closeButton.clicked.connect(self.closeDialog)
        self.rentalInfoLayout.addWidget(self.closeButton)

        self.cancelButton = QPushButton("Storno")
        self.cancelButton.clicked.connect(self.cancelOrder)
        self.rentalInfoLayout.addWidget(self.cancelButton)

        self.ausleihe_id = ausleihe_id

    def closeDialog(self):
        self.close()

    def cancelOrder(self):

        reply = QMessageBox()
        reply.setText("Wirklich stornieren?")
        reply.setStandardButtons(QMessageBox.StandardButton.Yes |
                                 QMessageBox.StandardButton.No)
        ret = reply.exec()
        if ret == QMessageBox.StandardButton.Yes:
            
            
            cancel_ausleihe_query = f"""UPDATE ausleihe 
                                        SET storniert = 1
                                        WHERE ausleihe_id = {self.ausleihe_id}"""

            conn = sqlite3.connect("db\\verleihverwaltung.db")
            conn.execute(cancel_ausleihe_query)
            conn.commit()

           
            conn.close()

            self.sendCancelMail()
        else:
            reply.close()

        self.sendCancelMail
    def sendCancelMail(self):
        

        dotenv.load_dotenv("widgets\credentials.env")

        sender_mail = os.getenv("email")

        text = f"""Hallo {self.name.split()[0]},\n
hiermit bestätigen wir die Stornierung deiner Ausleihe.

Solltest du in Zukunft wieder etwas benötigen, schreib uns gerne.

Wir würden uns freuen, wenn wir dich in unserem Newsletter begrüßen dürfen.

Darin erhältst du Updates zu unseren Ausleihartikeln und zusätzlich 10% bei deiner nächsten Ausleihe.

Eintragen kannst du dich über folgenden Link: https://mailchi.mp/9a820de77a38/outleih-landing

Vielen dank für dein Vetrauen in uns und bis zum nächsten Mal.

Dein Outleih Team """

        mail = MIMEText(text)
        mail["subject"] = "Storno GoPro Ausleihe"
        sender = f"Outleih <{sender_mail}>"
        receiver = self.email

        s = smtplib.SMTP_SSL("smtp.strato.de", 465)

        dotenv.load_dotenv("widgets\credentials.env")
        login = os.getenv("stratoLOGIN")
        pw = os.getenv("stratoPW")
        s.login(login, pw)
        s.sendmail(sender, receiver, mail.as_string())
        s.quit()
