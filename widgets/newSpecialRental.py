


from datetime import date, timedelta

import math
from pickle import NONE
import random
import sqlite3
import os
import dotenv
import paypalrestsdk
from paypalrestsdk import Invoice


from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import pandas as pd
import numpy as np

from widgets.activeRentals import ActiveRentalLine, ActiveRentals


class NewSpecialRental(QWidget):
    # Calender for daterange

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        
        self.object_list = []
        self.shippingCost = 0.0
        

        # Verticales Layout für new_rental Tab
        self.new_rental_tab_layout = QVBoxLayout(self)
        self.new_rental_tab_layout.setContentsMargins(40, 20, 40, 20)

        self.cal_start = QCalendarWidget()
        self.cal_end = QCalendarWidget()

        self.cal_end.activated.connect(self.calculateRentDuration)
        self.cal_end.selectionChanged.connect(self.calculateRentDuration)

        # Calender in horizontalem Tab anordnen

        self.cal_layout = QHBoxLayout()
        self.cal_layout.addWidget(self.cal_start)
        self.cal_layout.addWidget(self.cal_end)

        self.cal_frame = QFrame()

        self.cal_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.cal_frame.setLayout(self.cal_layout)

        self.new_rental_tab_layout.addWidget(self.cal_frame)

        # ADD / REMOVE BUTTONS
        self.addRemoveButtonLayout = QHBoxLayout()

        self.addButton = QPushButton("Artikel Hinzufügen")
        self.addButton.clicked.connect(self.addArticle)
        self.removeButton = QPushButton("Letzten Artikel entfernen")
        self.removeButton.clicked.connect(self.removeArticle)

        self.addRemoveButtonLayout.addWidget(self.addButton)
        self.addRemoveButtonLayout.addWidget(self.removeButton)
        self.new_rental_tab_layout.addLayout(self.addRemoveButtonLayout)

        # ARTICLE LINE

        self.articles_layout = QVBoxLayout()
        self.articles_layout.addWidget(AddArticle(self))
        self.addToList()

        # Group Box in Frame

        self.articles_layout_frame = QFrame()
        self.articles_layout_frame.setObjectName("frame1")

        self.articles_layout_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.articles_layout_frame.setLayout(self.articles_layout)

        # Add to Overall Layout

        self.new_rental_tab_layout.addWidget(self.articles_layout_frame)

        # PRICE LAYOUT

        self.price_layout = QVBoxLayout()

        self.price_la_layout = QHBoxLayout()
        self.price_le_layout = QHBoxLayout()

        self.days_la = QLabel("Anzahl Tage")
        self.days_la.setFixedWidth(100)
        self.weeks_la = QLabel("Anzahl Wochen")
        self.weeks_la.setFixedWidth(100)
        self.shipping_la = QLabel("Versandkosten")
        self.shipping_la.setFixedWidth(100)
        self.total_la = QLabel("Gesamtpreis")
        self.total_la.setFixedWidth(100)

        self.days_le = QLineEdit()
        self.days_le.setFixedWidth(100)
        self.days_le.setText("")

        self.weeks_le = QLineEdit()
        self.weeks_le.setFixedWidth(100)
        self.weeks_le.setText("0")
        self.weeks_le.textChanged.connect(self.durationChanged)

        self.shipping_cb = QComboBox()
        self.shipping_cb.setFixedWidth(100)
        self.shipping_cb.addItem("Abholung")
        self.shipping_cb.addItem("Kostenlos")
        # self.shipping_cb.activated.connect(self.addShippingCost)

        conn = sqlite3.connect("db\\verleihverwaltung.db")
        query = f"""SELECT bezeichnung FROM versandkosten"""
        data = conn.execute(query).fetchall()
        conn.close()

        self.shipping_cb.addItems([i[0] for i in data])
        self.shipping_cb.activated.connect(self.getShippingPrice)

        self.total_le = QLineEdit()
        self.total_le.setFixedWidth(100)
        self.total_le.setText("0")
        # self.total_le.textChanged.connect(self.updateTotalPrice)

        self.price_la_layout.addWidget(self.days_la)
        self.price_la_layout.addWidget(self.weeks_la)
        self.price_la_layout.addWidget(self.shipping_la)
        self.price_la_layout.addWidget(self.total_la)

        self.price_le_layout.addWidget(self.days_le)
        self.price_le_layout.addWidget(self.weeks_le)
        self.price_le_layout.addWidget(self.shipping_cb)
        self.price_le_layout.addWidget(self.total_le)

        self.price_layout.addLayout(self.price_la_layout)
        self.price_layout.addLayout(self.price_le_layout)

        self.price_frame = QFrame()
        self.price_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.price_frame.setLayout(self.price_layout)

        self.new_rental_tab_layout.addWidget(self.price_frame)

        # ADRESS LAYOUT

        # Dropdown for existing costumers

        self.existing_costumer_cb = QComboBox()
        self.existing_costumer_cb.setPlaceholderText("Kundenname")
        self.existing_costumer_cb.setFixedWidth(200)
        self.existing_costumer_cb.addItem("Neuer Kunde")

        conn = sqlite3.connect("db\\verleihverwaltung.db")
        query = f"""SELECT vorzuname FROM kontaktdaten"""

        data = conn.execute(query).fetchall()
        conn.close()
        self.existing_costumer_cb.addItems([i[0] for i in data])
        self.existing_costumer_cb.activated.connect(self.showExistingAdress)

        # Adress fields

        self.name_label = QLabel("Vorname")
        self.name_label.setFixedWidth(50)
        self.surname_label = QLabel("Nachname")
        self.surname_label.setFixedWidth(50)
        self.street_label = QLabel("Straße")
        self.street_label.setFixedWidth(50)
        self.plz_label = QLabel("PLZ")
        self.plz_label.setFixedWidth(50)
        self.city_label = QLabel("Stadt")
        self.city_label.setFixedWidth(50)
        self.email_label = QLabel("Email")
        self.email_label.setFixedWidth(50)

        self.name_field = QLineEdit()
        self.surname_field = QLineEdit()
        self.street_field = QLineEdit()
        self.plz_field = QLineEdit()
        self.city_field = QLineEdit()
        self.email_field = QLineEdit()

        self.adress_layout = QVBoxLayout()

        self.adress_layout_line1 = QHBoxLayout()
        self.adress_layout_line1.addWidget(self.name_label)
        self.adress_layout_line1.addWidget(self.name_field)
        self.adress_layout_line1.addWidget(self.surname_label)
        self.adress_layout_line1.addWidget(self.surname_field)
        self.adress_layout_line1.addWidget(self.street_label)
        self.adress_layout_line1.addWidget(self.street_field)

        self.adress_layout_line2 = QHBoxLayout()
        self.adress_layout_line2.addWidget(self.plz_label)
        self.adress_layout_line2.addWidget(self.plz_field)
        self.adress_layout_line2.addWidget(self.city_label)
        self.adress_layout_line2.addWidget(self.city_field)
        self.adress_layout_line2.addWidget(self.email_label)
        self.adress_layout_line2.addWidget(self.email_field)

        self.adress_layout.addWidget(self.existing_costumer_cb)
        self.adress_layout.addLayout(self.adress_layout_line1)
        self.adress_layout.addLayout(self.adress_layout_line2)

        self.adress_frame = QFrame()
        self.adress_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.adress_frame.setLayout(self.adress_layout)

        self.new_rental_tab_layout.addWidget(self.adress_frame)

        # Save Rental Button

        self.save_rental_bt = QPushButton("Leihe Speichern")
        self.save_rental_bt.setFixedSize(100, 20)
        self.save_rental_bt.clicked.connect(self.saveNewRental)
        self.new_rental_tab_layout.addWidget(self.save_rental_bt)

    def durationChanged(self):
        item = self.articles_layout.itemAt(0)
        widget = item.widget()
        widget.updateTotal()

    def addArticle(self):
        self.articles_layout.addWidget(AddArticle(self))

        self.addToList()

    def addToList(self):
        count = self.articles_layout.count()
        item = self.articles_layout.itemAt(count-1)
        widget = item.widget()

        self.object_list.append(widget)

    def removeArticle(self):
        count = self.articles_layout.count()

        if count == 1:
            pass
        else:
            item = self.articles_layout.itemAt(count-1)
            widget = item.widget()
            self.object_list.remove(widget)

            widget.deleteLater()

        item = self.articles_layout.itemAt(0)
        widget = item.widget()
        widget.updateTotal()

    def showExistingAdress(self):

        name = self.existing_costumer_cb.currentText()

        try:
            conn = sqlite3.connect("db\\verleihverwaltung.db")
            query = f"""SELECT vorzuname, strasse, plz, stadt, email FROM kontaktdaten
                        WHERE vorzuname = '{name}'"""

            data = conn.execute(query).fetchall()

            conn.close()

            vorzuname = data[0][0].split()
            self.name_field.setText(vorzuname[0])
            self.surname_field.setText(vorzuname[1])
            self.street_field.setText(data[0][1])
            self.plz_field.setText(str(data[0][2]))
            self.city_field.setText(data[0][3])
            self.email_field.setText(data[0][4])

        except:
            self.name_field.setText("")
            self.surname_field.setText("")
            self.street_field.setText("")
            self.plz_field.setText("")
            self.city_field.setText("")
            self.email_field.setText("")

    def calculateRentDuration(self):

        start_date = self.cal_start.selectedDate()
        end_date = self.cal_end.selectedDate()

        days_of_rental = start_date.daysTo(end_date)
        weeks_of_rental = math.ceil(days_of_rental/7)

        self.days_le.setText(str(days_of_rental))
        self.weeks_le.setText(str(weeks_of_rental))

        # Bei Wechsel des Datum soll Verfügbarkeit bei allen erneut überprüft werden

        item = self.articles_layout.itemAt(0)
        widget = item.widget()

        if widget.articles_cb.currentIndex() != -1:
            widget.getPrice()

        msg = QMessageBox()
        msg.setWindowTitle("Wochenanzahl")
        msg.setText("Wochenanzahl korrekt?\n Versandart wählen")
        x = msg.exec()

    def getShippingPrice(self):

        if self.shipping_cb.currentIndex() > 1:
            conn = sqlite3.connect("db\\verleihverwaltung.db")
            query = f"""SELECT preis 
                        FROM versandkosten
                        WHERE bezeichnung = '{self.shipping_cb.currentText()}'"""

            self.shippingCost = conn.execute(query).fetchall()[0][0]
            conn.close()

        else:
            self.shippingCost = 0.0

        item = self.articles_layout.itemAt(0)
        widget = item.widget()
        widget.updateTotal()

    def saveNewRental(self):

        customer_id = NONE
        ausleihe_id = NONE
        gesamtpreis = float(self.total_le.text())
        start_date = self.cal_start.selectedDate().toString("yyyy-MM-dd")
        end_date = self.cal_end.selectedDate().toString("yyyy-MM-dd")
        shipping = NONE

        # Check if Shipping or pickup

        if self.shipping_cb.currentIndex() == 0:
            shipping = 0
        else:
            shipping = 1

        vorzuname = self.name_field.text() + " " + self.surname_field.text()
        strasse = self.street_field.text()
        plz = int(self.plz_field.text())
        stadt = self.city_field.text()
        email = self.email_field.text()

        # Save the Adress and/or get the id of the Adress

        if (self.existing_costumer_cb.currentIndex() == -1 or self.existing_costumer_cb.currentIndex() == 0):

            insert_customer_query = f""" INSERT INTO kontaktdaten ( vorzuname,strasse, plz, stadt, email)
                                        VALUES ('{vorzuname}', '{strasse}', {plz}, '{stadt}', '{email}')"""

            conn = sqlite3.connect("db\\verleihverwaltung.db")
            cursor = conn.cursor()
            cursor.execute(insert_customer_query)
            conn.commit()
            customer_id = cursor.lastrowid
            cursor.close()

        else:
            get_id_query = f"""SELECT kontaktdaten_id 
                                FROM kontaktdaten
                                WHERE vorzuname = '{self.existing_costumer_cb.currentText()}'"""

            conn = sqlite3.connect("db\\verleihverwaltung.db")
            cursor = conn.cursor()
            customer_id = cursor.execute(get_id_query).fetchall()[0][0]

            conn.commit()
            cursor.close()

        # Save into Ausleihe and get Id of ausleihe (use id to insert values into ausleiheninhalt)

        insert_ausleihe_query = f"""INSERT INTO ausleihe (kontaktdaten_id, gesamtpreis, rechnungsdatum, startdatum, enddatum, versand)
                                    VALUES ({customer_id}, {gesamtpreis}, '{str(date.today())}', '{start_date}', '{end_date}', {shipping})"""

        conn = sqlite3.connect("db\\verleihverwaltung.db")
        cursor = conn.cursor()
        cursor.execute(insert_ausleihe_query)
        conn.commit()
        ausleihe_id = cursor.lastrowid
        cursor.close()

        # INSERT Contents of rental in ausleiheninhalt
        conn = sqlite3.connect("db\\verleihverwaltung.db")
        for object in self.object_list:
            insert_inhalt_query = f"""INSERT INTO ausleiheninhalt
                                        VALUES ({ausleihe_id}, '{object.serialNr}')"""

            cursor = conn.cursor()
            cursor.execute(insert_inhalt_query)
            conn.commit()

        cursor.close()
        self.createInvoice()

        self.reset()

    def createInvoice(self):

        startdatum = self.cal_start.selectedDate().toString("dd.MM.yyyy")
        enddatum = self.cal_end.selectedDate().toString("dd.MM.yyyy")
        rueckgabe_datum = self.cal_end.selectedDate()

        if self.shipping_cb.currentIndex() == 0:
            rueckgabe_datum = rueckgabe_datum.addDays(2).toString("dd.MM.yyyy")
        else:
            rueckgabe_datum = rueckgabe_datum.addDays(3).toString("dd.MM.yyyy")

        ausleiheninhalt = ""

        for article in self.object_list:

            ausleiheninhalt += article.article + "\n"

        
        dotenv.load_dotenv("widgets\credentials.env")
        paypal_id = os.getenv("paypalID")
        paypal_secret = os.getenv("paypalSECRET")
        
        paypalrestsdk.configure(

            {
                "mode": "live",
                "client_id": paypal_id,
                "client_secret": paypal_secret
            }
        )
        invoice = Invoice({

            'merchant_info': {
                "email": "mail@outleih.de",
                "first_name": "Oliver",
                "last_name": "Thomaschewski",
                "business_name": "Outleih",
                
                "phone": {
                    "country_code": "0049",
                    "national_number": "017623978262"
                },

                "address": {
                    "line1": "Friedrichsbergerstr. 4",
                    "city": "Berlin",
                    "postal_code": "10243"
                }

            },

            "logo_url": "https://github.com/OliverThomaschewski/verleihverwaltung/blob/main/images/Logo.png?raw=true",


            "billing_info": [{
                "email": self.email_field.text(),


            }],

            # Billing Info Ende




            "items": [{
                "name": "GoPro Paket",
                "description": ausleiheninhalt,
                "quantity": 1,
                "unit_price": {
                    "currency": "EUR",
                    "value": float(self.total_le.text())
                }
            },

            ],

            # Items Ende

            "shipping_info": {
                "first_name": self.name_field.text(),
                "last_name": self.surname_field.text(),


                "address": {
                    "line1": self.street_field.text(),
                    "city": self.city_field.text(),
                    "postal_code": self.plz_field.text()
                }

            },


            "note": f"""Ausleihe vom {startdatum} - {enddatum}
            Rückgabe bis spätestens {rueckgabe_datum}
            Bei verspäteter Rückgabe wird eine weitere Wochenleihe fällig""",


        }
        )

        if self.shipping_cb.currentIndex() != 0:
            invoice["shipping_cost"] = {
                "amount": {
                    "currency": "EUR",
                    "value": self.shippingCost
                }
            }

        invoice.create()
        invoice.send()



    def reset(self):
        

        # Resetting all text fields

        self.days_le.setText("")
        self.weeks_le.setText("0")
        self.shipping_cb.setCurrentIndex(-1)
        self.total_le.setText("")

        # Reset Adressline

        self.existing_costumer_cb.setCurrentIndex(-1)
        self.name_field.setText("")
        self.surname_field.setText("")
        self.street_field.setText("")
        self.plz_field.setText("")
        self.city_field.setText("")
        self.email_field.setText("")



class AddArticle(QWidget):

    def __init__(self, parent) -> None:

        super(QWidget, self).__init__(parent)

        self.parent = parent

        self.serialNr = None
        self.article = None
        self.weeklyPrice = 0.0

        self.articles_cb = QComboBox()
        self.articles_cb.setPlaceholderText("Artikel wählen")
        self.articles_cb.activated.connect(self.getPrice)
        

        # Hier comboxob für Seriennummern

        self.serialsComboBox = QComboBox()
        self.serialsComboBox.activated.connect(self.setSerialNr)
        self.availableSerial = QLabel("Hier Serial")
        self.weeklyPriceLabel = QLabel()
        

        self.articleLineLayout = QHBoxLayout(self)

        conn = sqlite3.connect("db\\verleihverwaltung.db")
        query = f"""SELECT bezeichnung FROM artikeltyp WHERE aktiv = 1"""

        articleTypes = conn.execute(query).fetchall()
        conn.close()
        self.articles_cb.addItems([article[0] for article in articleTypes])

        self.articleLineLayout.addWidget(self.articles_cb)
        self.articleLineLayout.addWidget(self.serialsComboBox)
        self.articleLineLayout.addWidget(self.weeklyPriceLabel)

    def setSerialNr(self):

        self.serialNr = self.serialsComboBox.currentText()
        

    def getPrice(self):

        artikelTyp = self.articles_cb.currentText()


        get_price_query = f"""SELECT wochenpreis
                                FROM artikeltyp 
                                WHERE bezeichnung = '{artikelTyp}'"""

        conn = sqlite3.connect("db\\verleihverwaltung.db")
        cursor = conn.cursor()

        price = cursor.execute(get_price_query).fetchall()[0][0]
        conn.commit()
        cursor.close()

        self.weeklyPriceLabel.setText(str(price))
        self.weeklyPrice = price

        self.updateTotal()

        selectedArticle = self.articles_cb.currentText()
        

        # Get Article ID

        conn = sqlite3.connect("db\\verleihverwaltung.db")
        query = f"""SELECT artikeltyp_id FROM artikeltyp WHERE bezeichnung = '{selectedArticle}'"""

        articleID = conn.execute(query).fetchall()[0][0]
        conn.close()

       
        # Seriennummern abrufen und in ComboBox packen

        conn = sqlite3.connect("db\\verleihverwaltung.db")
        query = f"""SELECT serien_nr FROM artikel WHERE artikeltyp_id = {articleID} AND aktiv = 1"""

        articleTypes = conn.execute(query).fetchall()
        conn.close()

        self.serialsComboBox.clear()
        self.serialsComboBox.addItems([article[0] for article in articleTypes])
        self.serialNr = self.serialsComboBox.currentText()
        self.article = self.articles_cb.currentText()
        

    def updateTotal(self):
        total = 0.0
        for item in self.parent.object_list:
            total += float(item.weeklyPrice)

        rentDuration = int(self.parent.weeks_le.text()
                           ) if self.parent.weeks_le.text() else 0
        total *= rentDuration
        total += self.parent.shippingCost
        total = round(total, 2)
        self.parent.total_le.setText(str(total))
