
from datetime import datetime, timedelta
from pickle import TRUE
import sqlite3
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from widgets.activeRentalLine import ActiveRentalLine


from widgets.rentalInfo import RentalInfo


class ActiveRentals(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.activeRentalsLayout = QVBoxLayout(self)

        # Update Button
        self.updateButton = QPushButton("Update")
        self.updateButton.clicked.connect(self.updateLines)
        self.activeRentalsLayout.addWidget(self.updateButton)

        # Headers

        self.activeRentalsHeaderLayout = QHBoxLayout()

        self.idLabel = QLabel("Ausleihe_ID")
        self.nameLabel = QLabel("Name")
        self.paidLabel = QLabel("Bezahlt")
        self.shippingTypeLabel = QLabel("Liefertyp")
        self.shippingDateLabel = QLabel("Versenden am")
        self.sentLabel = QLabel("verschickt")
        self.returnDateLabel = QLabel("Rückgabe am")
        self.receivedLabel = QLabel("zurück erhalten")
        self.dummyLabel = QLabel()

        self.activeRentalsHeaderLayout.addWidget(self.idLabel)
        self.activeRentalsHeaderLayout.addWidget(self.nameLabel)
        self.activeRentalsHeaderLayout.addWidget(self.paidLabel)
        self.activeRentalsHeaderLayout.addWidget(self.shippingTypeLabel)
        self.activeRentalsHeaderLayout.addWidget(self.shippingDateLabel)
        self.activeRentalsHeaderLayout.addWidget(self.sentLabel)
        self.activeRentalsHeaderLayout.addWidget(self.returnDateLabel)
        self.activeRentalsHeaderLayout.addWidget(self.receivedLabel)
        self.activeRentalsHeaderLayout.addWidget(self.dummyLabel)

        self.activeRentalsLayout.addLayout(self.activeRentalsHeaderLayout)

        rentals_query = f"""SELECT ausleihe_id, kontaktdaten.vorzuname, startdatum, versand, bezahldatum, versanddatum, enddatum, returnmail
                    FROM ausleihe
                    JOIN kontaktdaten ON kontaktdaten.kontaktdaten_id = ausleihe.kontaktdaten_id 
                    WHERE rueckgabedatum IS NULL AND storniert = 0 
                    ORDER BY startdatum
                """

        conn = sqlite3.connect("db\\verleihverwaltung.db")
        cursor = conn.cursor()
        rentals = cursor.execute(rentals_query).fetchall()

        conn.commit()
        cursor.close()

        for rental in rentals:

            line = ActiveRentalLine(self, rental)

            self.activeRentalsLayout.addWidget(line)

    def updateLines(self, rental):

        count = self.activeRentalsLayout.count()

        item = self.activeRentalsLayout.itemAt(count-1)
        widget = item.widget()

        latest_id = widget.ausleihe_id

        rentals_query = f"""SELECT ausleihe_id, kontaktdaten.vorzuname, startdatum, versand, bezahldatum, versanddatum, enddatum
                    FROM ausleihe
                    JOIN kontaktdaten ON kontaktdaten.kontaktdaten_id = ausleihe.kontaktdaten_id 
                   WHERE ausleihe_id > {latest_id} AND storniert = 0
                """

        conn = sqlite3.connect("db\\verleihverwaltung.db")
        cursor = conn.cursor()
        rentals = cursor.execute(rentals_query).fetchall()

        conn.commit()
        cursor.close()

        if len(rentals) == 0:
            pass
        for rental in rentals:

            line = ActiveRentalLine(self, rental)

            self.activeRentalsLayout.addWidget(line)
