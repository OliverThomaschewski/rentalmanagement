from datetime import datetime, timedelta
from pickle import TRUE
import sqlite3
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *


class ActiveRentals(QWidget):
    # Calender for daterange

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.activeRentalsLayout = QVBoxLayout(self)

        # Headers

        self.activeRentalsHeaderLayout = QHBoxLayout()

        self.idLabel = QLabel("Ausleihe_ID")
        self.nameLabel = QLabel("Name")
        self.paidLabel = QLabel("Bezahlt")
        self.shippingTypeLabel = QLabel("Liefertyp")
        self.shippingDateLabel = QLabel("Versenden am")
        self.sentLabel = QLabel("verschickt")
        self.receivedLabel = QLabel("zurück erhalten")
        self.dummyLabel = QLabel()

        self.activeRentalsHeaderLayout.addWidget(self.idLabel)
        self.activeRentalsHeaderLayout.addWidget(self.nameLabel)
        self.activeRentalsHeaderLayout.addWidget(self.paidLabel)
        self.activeRentalsHeaderLayout.addWidget(self.shippingTypeLabel)
        self.activeRentalsHeaderLayout.addWidget(self.shippingDateLabel)
        self.activeRentalsHeaderLayout.addWidget(self.sentLabel)
        self.activeRentalsHeaderLayout.addWidget(self.receivedLabel)
        self.activeRentalsHeaderLayout.addWidget(self.dummyLabel)

        self.activeRentalsLayout.addLayout(self.activeRentalsHeaderLayout)

        rentals_query = f"""SELECT ausleihe_id, kontaktdaten.vorzuname, startdatum, versand, bezahldatum, versanddatum
                    FROM ausleihe
                    JOIN kontaktdaten ON kontaktdaten.kontaktdaten_id = ausleihe.kontaktdaten_id 
                    WHERE rueckgabedatum IS NULL
                """

        conn = sqlite3.connect("db\\verleihverwaltung.db")
        cursor = conn.cursor()
        rentals = cursor.execute(rentals_query).fetchall()

        conn.commit()
        cursor.close()

        for rental in rentals:

            line = ActiveRentalLine(self, rental)

            self.activeRentalsLayout.addWidget(line)


class ActiveRentalLine(QWidget):

    def __init__(self, parent, rental) -> None:

        super(QWidget, self).__init__(parent)

        self.ausleihe_id = rental[0]
        vorzuname = rental[1]
        startdatum = datetime.strptime(rental[2], '%Y-%m-%d')
        versandTyp = "Versand" if rental[3] == 1 else "Abholung"
        bezahldatum = rental[4]
        versendetdatum = rental[5]

        self.idLabel = QLabel(str(self.ausleihe_id))
        self.vorzunameLabel = QLabel(vorzuname)
        self.bezahltCheckBox = QCheckBox()

        self.versandTypLabel = QLabel(versandTyp)
        self.versandDatumLabel = QLabel()
        self.versendetCheckBox = QCheckBox()
        self.rueckgabeCheckBox = QCheckBox()
        self.infoButton = QPushButton("Info")
        self.infoButton.clicked.connect(self.showInfo)

        if bezahldatum is not None:
            self.bezahltCheckBox.setChecked(True)
        else:
            self.bezahltCheckBox.setChecked(False)

        if versendetdatum is not None:
            self.versendetCheckBox.setChecked(True)
        else:
            self.versendetCheckBox.setChecked(False)

        if versandTyp == "Versand":
            versanddatum = startdatum - timedelta(days=3)
        else:
            versanddatum = startdatum - timedelta(days=1)

        self.versandDatumLabel.setText(versanddatum.strftime('%Y-%m-%d'))

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
        self.activeRentalLayout.addWidget(self.rueckgabeCheckBox)
        self.activeRentalLayout.addWidget(self.infoButton)

    def updateShipping(self):

        shippedDate = datetime.today().strftime('%Y-%m-%d')
        print(shippedDate)

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


class RentalInfo(QDialog):
    def __init__(self, parent, ausleihe_id):
        super().__init__(parent)
        self.parent = parent

        self.resize(300, 200)

        rentalinfo_query = f"""SELECT ausleiheninhalt.serien_nr, kontaktdaten.vorzuname, kontaktdaten.strasse, kontaktdaten.plz, kontaktdaten.stadt, ausleihe.startdatum, ausleihe.enddatum
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

        self.closeButton = QPushButton("Got It")
        self.closeButton.clicked.connect(self.closeDialog)
        self.rentalInfoLayout.addWidget(self.closeButton)

    def closeDialog(self):
        self.close()
