from datetime import datetime, timedelta, date
from pickle import TRUE
from queue import Empty
import sqlite3
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import smtplib
from email.mime.text import MIMEText
import os
import dotenv

from widgets.rentalInfo import RentalInfo


class ActiveRentalLine(QWidget):

    def __init__(self, parent, rental) -> None:

        super(QWidget, self).__init__(parent)

        self.ausleihe_id = rental[0]
        self.vorzuname = rental[1]
        self.startdatum = datetime.strptime(rental[2], '%Y-%m-%d')
        self.versandTyp = "Versand" if rental[3] == 1 else "Abholung"
        self.bezahldatum = rental[4]
        self.versendetdatum = rental[5]
        self.enddatum = datetime.strptime(rental[6], '%Y-%m-%d')

        self.idLabel = QLabel(str(self.ausleihe_id))
        self.vorzunameLabel = QLabel(self.vorzuname)
        self.bezahltCheckBox = QCheckBox()

        self.versandTypLabel = QLabel(self.versandTyp)
        self.versandDatumLabel = QLabel()
        self.versendetCheckBox = QCheckBox()
        self.rueckgabeDatumLabel = QLabel()
        self.rueckgabeCheckBox = QCheckBox()
        self.infoButton = QPushButton("Info")
        self.infoButton.clicked.connect(self.showInfo)

        if self.bezahldatum is None or len(self.bezahldatum) == 0:
            self.bezahltCheckBox.setChecked(False)
        else:
            self.bezahltCheckBox.setChecked(True)

        if self.versendetdatum is not None:
            self.versendetCheckBox.setChecked(True)
        else:
            self.versendetCheckBox.setChecked(False)

        if self.versandTyp == "Versand":
            versanddatum = self.startdatum - timedelta(days=3)
            rueckgabedatum = self.enddatum + timedelta(days=3)
        else:
            versanddatum = self.startdatum - timedelta(days=1)
            rueckgabedatum = self.enddatum + timedelta(days=2)


        """
        Hier sollte die Funktion aufgerufen werden um Erinnerungsemails für die Rückgabe zu schicken
        if self.enddatum <= datetime.today() and rental[7] == 0:
            self.sendReminder()
        """

        self.versandDatumLabel.setText(versanddatum.strftime('%Y-%m-%d'))
        self.rueckgabeDatumLabel.setText(rueckgabedatum.strftime('%Y-%m-%d'))

        self.bezahltCheckBox.toggled.connect(self.updatePaid)
        self.versendetCheckBox.toggled.connect(self.updateShipping)
        self.rueckgabeCheckBox.toggled.connect(self.updateReceived)

        self.activeRentalLayout = QHBoxLayout(self)

        self.activeRentalLayout.addWidget(self.idLabel)
        self.activeRentalLayout.addWidget(self.vorzunameLabel)
        self.activeRentalLayout.addWidget(self.bezahltCheckBox)
        self.activeRentalLayout.addWidget(self.versandTypLabel)
        self.activeRentalLayout.addWidget(self.versandDatumLabel)
        self.activeRentalLayout.addWidget(self.versendetCheckBox)
        self.activeRentalLayout.addWidget(self.rueckgabeDatumLabel)
        self.activeRentalLayout.addWidget(self.rueckgabeCheckBox)
        self.activeRentalLayout.addWidget(self.infoButton)

    def updateShipping(self):

        shippedDate = datetime.today().strftime('%Y-%m-%d')

        if self.sender().isChecked() is True:
            update_query = f"""UPDATE ausleihe SET versanddatum = '{shippedDate}'
                        WHERE ausleihe_id = '{self.ausleihe_id}'"""

            conn = sqlite3.connect("db\\verleihverwaltung.db")
            conn.execute(update_query)
            conn.commit()
            conn.close()
        else:
            update_query = f"""UPDATE ausleihe SET versanddatum = ''
                        WHERE ausleihe_id = '{self.ausleihe_id}'"""

            conn = sqlite3.connect("db\\verleihverwaltung.db")
            conn.execute(update_query)
            conn.commit()
            conn.close()

    def updatePaid(self):

        paidDate = datetime.today().strftime('%Y-%m-%d')

        if self.sender().isChecked() is True:

            update_query = f"""UPDATE ausleihe SET bezahldatum = '{paidDate}'
                        WHERE ausleihe_id = '{self.ausleihe_id}'"""

            conn = sqlite3.connect("db\\verleihverwaltung.db")
            conn.execute(update_query)
            conn.commit()
            conn.close()
        else:
            update_query = f"""UPDATE ausleihe SET bezahldatum = ''
                        WHERE ausleihe_id = '{self.ausleihe_id}'"""

            conn = sqlite3.connect("db\\verleihverwaltung.db")
            conn.execute(update_query)
            conn.commit()
            conn.close()

    def updateReceived(self):

        receivedDate = datetime.today().strftime('%Y-%m-%d')

        if self.sender().isChecked() is True:
            update_query = f"""UPDATE ausleihe SET rueckgabedatum = '{receivedDate}'
                        WHERE ausleihe_id = '{self.ausleihe_id}'"""

            conn = sqlite3.connect("db\\verleihverwaltung.db")
            conn.execute(update_query)
            conn.commit()
            conn.close()
            self.sendReceivedMail()
        else:

            update_query = f"""UPDATE ausleihe SET rueckgabedatum = ''
                        WHERE ausleihe_id = '{self.ausleihe_id}'"""

            conn = sqlite3.connect("db\\verleihverwaltung.db")
            conn.execute(update_query)
            conn.commit()
            conn.close()

    def showInfo(self):
        dlg = RentalInfo(self, self.ausleihe_id)
        dlg.setWindowTitle("Info")
        dlg.exec()

    def sendReceivedMail(self):

        query = f"""SELECT kontaktdaten.vorzuname, kontaktdaten.email
                    FROM ausleihe
                    JOIN kontaktdaten ON ausleihe.kontaktdaten_id = kontaktdaten.kontaktdaten_id
                    WHERE ausleihe.ausleihe_id = {self.ausleihe_id}
                        """

        conn = sqlite3.connect("db\\verleihverwaltung.db")
        cursor = conn.cursor()
        data = cursor.execute(query).fetchall()

        conn.commit()
        cursor.close()

        vorname = data[0][0].split()[0]
        email = data[0][1]

        dotenv.load_dotenv("widgets\credentials.env")

        sender_mail = os.getenv("email")

        text = f"""Hallo {vorname},\n
hiermit bestätigen wir die Rückgabe deiner Ausleihe.

Solltest du in Zukunft wieder etwas benötigen, schreib uns gerne.

Gerne kannst du unserem Ebay Kleinanzeigen Unternehmensprofil folgen.

Klicke dazu einfach auf folgenden Link und anschließend auf "Folgen":

https://www.ebay-kleinanzeigen.de/pro/outleih

Vielen dank für dein Vetrauen in uns und bis zum nächsten Mal.

Dein Outleih Team """


        mail = MIMEText(text)
        mail["subject"] = "Rückgabebestätigung Outleih"
        sender = f"Outleih <{sender_mail}>"
        receiver = email

        s = smtplib.SMTP_SSL("smtp.strato.de", 465)

        dotenv.load_dotenv("widgets\credentials.env")
        login = os.getenv("stratoLOGIN")
        pw = os.getenv("stratoPW")
        s.login(login, pw)
        s.sendmail(sender, receiver, mail.as_string())
        s.quit()

    def sendReminder(self):
        query = f"""SELECT kontaktdaten.vorzuname, kontaktdaten.email,
                    FROM ausleihe
                    JOIN kontaktdaten ON ausleihe.kontaktdaten_id = kontaktdaten.kontaktdaten_id
                    WHERE ausleihe.ausleihe_id = {self.ausleihe_id}
                        """

        conn = sqlite3.connect("db\\verleihverwaltung.db")
        cursor = conn.cursor()
        data = cursor.execute(query).fetchall()

        conn.commit()
        cursor.close()

        vorname = data[0][0].split()[0]
        email = data[0][1]

        dotenv.load_dotenv("widgets\credentials.env")

        sender_mail = os.getenv("email")

        text = f"""Hallo {vorname},\n
Wir hoffen mit der Kamera hat alles geklappt und du konntest ein paar tolle Aufnahmen machen.

Solltest du die Kamera zurücksenden, schicke uns doch bitte die Trackingnummer zu sobald du das Paket abgegeben hast.

Bringst du die Kamera selbst zurück, gib einfach kurz Bescheid, wann du sie bringen möchtest.

Dein Outleih Team """


        mail = MIMEText(text)
        mail["subject"] = "Rückgabe GoPro"
        sender = f"Outleih <{sender_mail}>"
        receiver = email

        s = smtplib.SMTP_SSL("smtp.strato.de", 465)

        dotenv.load_dotenv("widgets\credentials.env")
        login = os.getenv("stratoLOGIN")
        pw = os.getenv("stratoPW")
        s.login(login, pw)
        s.sendmail(sender, receiver, mail.as_string())
        s.quit()

        update_query = f"""UPDATE ausleihe SET returnmail = 1
                    WHERE ausleihe_id = '{self.ausleihe_id}'"""

        conn = sqlite3.connect("db\\verleihverwaltung.db")
        conn.execute(update_query)
        conn.commit()
        conn.close()

