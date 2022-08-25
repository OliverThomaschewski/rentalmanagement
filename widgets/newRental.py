
from ast import Delete
from asyncio.windows_events import NULL
from datetime import date, timedelta, datetime
import datetime
import math
from pickle import NONE
import random
import sqlite3
from ssl import ALERT_DESCRIPTION_HANDSHAKE_FAILURE
from typing import ItemsView
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import pandas as pd
import numpy as np


class NewRental(QWidget):
    # Calender for daterange

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.article_count = 0
        self.current_article_price = 0
        self.article_list = []

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

        # ARTICLE LINE

        self.articles_layout = QVBoxLayout()
        self.new_rental_line_layout = QHBoxLayout()
        self.new_rental_line_layout.setObjectName("erstes")

        # Dropdown, Ausgabezeilte, + Button

        self.article_cb = QComboBox()
        self.article_cb.setObjectName("article_cb_0")
        self.article_cb.setFixedSize(200, 20)
        self.article_cb.setPlaceholderText("Artikel wählen")

        # Add Articles to ComboBox
        conn = sqlite3.connect("db\\verleihverwaltung.db")
        query = f"""SELECT bezeichnung FROM artikeltyp"""

        data = conn.execute(query).fetchall()
        conn.close()
        self.article_cb.addItems([i[0] for i in data])
        self.article_cb.activated.connect(self.addTotalPrice)

        self.article_label = QLabel("Hier wird Seriennummer angezeigt")
        self.article_label.setObjectName("article_label_0")

        self.article_price_label = QLabel()

        self.add_line_pb = QPushButton()
        self.add_line_pb.setText("+")
        self.add_line_pb.setFixedWidth(20)
        self.add_line_pb.clicked.connect(self.addGroupBox)

        self.new_rental_line_layout.addWidget(self.article_cb)
        self.new_rental_line_layout.addWidget(self.article_label)
        self.new_rental_line_layout.addWidget(self.article_price_label)
        self.new_rental_line_layout.addWidget(self.add_line_pb)

        self.new_rental_line_gb = QGroupBox()
        self.new_rental_line_gb.setLayout(self.new_rental_line_layout)

        self.articles_layout.addWidget(self.new_rental_line_gb)

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

        self.shipping_cb = QComboBox()
        self.shipping_cb.setFixedWidth(100)
        self.shipping_cb.addItem("Abholung")
        self.shipping_cb.addItem("Kostenlos")
        self.shipping_cb.activated.connect(self.addShippingCost)

        conn = sqlite3.connect("db\\verleihverwaltung.db")
        query = f"""SELECT bezeichnung FROM versandkosten"""
        data = conn.execute(query).fetchall()
        conn.close()

        self.shipping_cb.addItems([i[0] for i in data])

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

    def addGroupBox(self):

        
       
        

        self.article_count += 1

        self.new_rental_line_layout = QHBoxLayout()
        self.new_rental_line_layout.setObjectName(f"nrll_{self.article_count}")
        # Dropdown, Ausgabezeilte, + Button

        self.article_cb = QComboBox()
        self.article_cb.setFixedSize(200, 20)
        self.article_cb.setPlaceholderText("Artikel wählen")
        self.article_cb.setObjectName(f"article_cb_{self.article_count}")
        self.article_cb.activated.connect(self.addTotalPrice)

        # Add Articles to ComboBox
        conn = sqlite3.connect("db\\verleihverwaltung.db")
        query = f"""SELECT bezeichnung FROM artikeltyp"""

        data = conn.execute(query).fetchall()
        conn.close()
        self.article_cb.addItems([i[0] for i in data])

        self.article_label = QLabel(f"testlabel {self.article_count}")
        self.article_label.setObjectName(f"article_label_{self.article_count}")
        self.article_price_label = QLabel("")

        self.add_line_pb = QPushButton()
        self.add_line_pb.setText("+")
        self.add_line_pb.setFixedSize(20, 20)
        self.add_line_pb.clicked.connect(self.addGroupBox)

        self.remove_line_pb = QPushButton()
        self.remove_line_pb.setText("-")
        self.remove_line_pb.setFixedWidth(20)
        self.remove_line_pb.clicked.connect(self.removeGroupBox)

        self.new_rental_line_layout.addWidget(self.article_cb, )
        self.new_rental_line_layout.addWidget(self.article_label)
        self.new_rental_line_layout.addWidget(self.article_price_label)
        self.new_rental_line_layout.addWidget(self.add_line_pb)
        self.new_rental_line_layout.addWidget(self.remove_line_pb)

        gb_count = self.articles_layout.count()
        self.added_gb = QGroupBox()
        self.added_gb.setLayout(self.new_rental_line_layout)

        # In Layout einbauen

        self.articles_layout.insertWidget(gb_count, self.added_gb)

        zählen = self.articles_layout.count()
        print(f"anzahl der lines: {zählen}")
        self.item = self.articles_layout.itemAt(zählen-1)
        
        print()
        

    # FUNCTIONS

    def removeGroupBox(self):

        try:
            current_index = self.article_cb.currentIndex()

        except:
            return

        if current_index != -1:
            self.deductTotalPrice()
            count = self.articles_layout.count()
            item = self.articles_layout.itemAt(count-1)
            widget = item.widget()
            widget.deleteLater()
            self.article_count -= 1
        else:
            count = self.articles_layout.count()
            item = self.articles_layout.itemAt(count-1)
            widget = item.widget()
            widget.deleteLater()
            self.article_count -= 1
        
        

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

        msg = QMessageBox()
        msg.setWindowTitle("Wochenanzahl")
        msg.setText("Wochenanzahl korrekt?\n Versandart wählen")
        x = msg.exec()

    def saveNewRental(self):
       

        customer_id = NONE
        ausleihe_id = NONE
        gesamtpreis = float(self.total_le.text())
        start_date = self.cal_start.selectedDate().toString("yyyy-MM-dd")
        end_date = self.cal_end.selectedDate().toString("yyyy-MM-dd")
        shipping = NONE

        # Check if Shipping or pickup

        print(f"Shipping Index ist: {self.shipping_cb.currentIndex()}")
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
            print("Das ist die ID des bestehenden Kunden")
            print(customer_id)
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

        print(f" Ausleihe id der eingefügten Ausleihe{ausleihe_id}")

        
        
        # INSERT Contents of rental in ausleiheninhalt
        conn = sqlite3.connect("db\\verleihverwaltung.db")
        for serial_nr in self.article_list:
            insert_inhalt_query = f"""INSERT INTO ausleiheninhalt
                                        VALUES ({ausleihe_id}, '{serial_nr}')"""

            cursor = conn.cursor()
            cursor.execute(insert_inhalt_query)
            conn.commit()

        cursor.close()

    def addTotalPrice(self):

        
        if self.weeks_le.text() == "0":
            msg = QMessageBox()
            msg.setWindowTitle("Achtung")
            msg.setText("Datum auswählen")
            x = msg.exec()
            pass

        else:
            
            week_amount = float(self.weeks_le.text())
            current_total = float(self.total_le.text())

            article = self.article_cb.currentText()
            print(f"Derzeitig ausgewählter Artikel: {article}")

            get_price_query = f"""SELECT wochenpreis, artikeltyp_id from artikeltyp 
                                    WHERE bezeichnung = '{article}'"""

            conn = sqlite3.connect("db\\verleihverwaltung.db")
            cursor = conn.cursor()
            
            data = cursor.execute(get_price_query).fetchall()
            conn.commit()
            cursor.close()
            
            print(data)
            article_price = data[0][0]
            artikeltyp_id = data[0][1]
            


            get_serial_query = f"""SELECT serien_nr
                                    FROM artikel 
                                    WHERE artikeltyp_id = {artikeltyp_id}"""

            conn = sqlite3.connect("db\\verleihverwaltung.db")
            cursor = conn.cursor()
            
            data = cursor.execute(get_serial_query).fetchall()
            
            conn.commit()
            cursor.close()
            print(data)

            print()
            if self.shipping_cb.currentIndex() == 0:
                versand = 0
            else:
                versand = 1

            print(self.cal_start.selectedDate().toString("yyyy-MM-dd"))
            print(self.cal_end.selectedDate().toString("yyyy-MM-dd"))
            startdatum = datetime.datetime.strptime(self.cal_start.selectedDate().toString("yyyy-MM-dd"), "%Y-%m-%d")
            enddatum = datetime.datetime.strptime(self.cal_end.selectedDate().toString("yyyy-MM-dd"), "%Y-%m-%d")

            self.article_label.setText(self.checkAvailability(article, startdatum, enddatum, versand))

            
            

            if self.article_price_label.text() == "":
            
                
                self.article_price_label.setText(str(article_price)+" €")

                total_to_add = week_amount * float(article_price)
                new_total = current_total + total_to_add
                self.total_le.setText(str(new_total))
                

            else:
                print(f"Der artikelpreis ist: {article_price}")
                current_total -= float(self.article_price_label.text().split()[0])*week_amount
                self.article_price_label.setText(str(article_price)+" €")

                total_to_add = week_amount * float(article_price)
                new_total = current_total + total_to_add
                self.total_le.setText(str(new_total))

        self.addToList()

    def deductTotalPrice(self):
        
        self.deductfromList()
        current_total = float(self.total_le.text())
        week_amount = float(self.weeks_le.text())
        current_price = float(self.article_price_label.text().split()[0])
        total_to_deduct = week_amount * current_price
        new_total = current_total - total_to_deduct
        self.total_le.setText(str(new_total))


    def addToList(self):
        self.article_list.append(self.article_label.text())
        print(self.article_list)

    def deductfromList(self):
        try:
            self.article_list.remove(self.article_label.text())
            
        except:
            pass
        finally:
            print(self.article_list)

    def checkAvailability(self, artikeltyp, startNewAusleihe, endNewAusleihe, newAusleiheVersand):

        rentals_query = f"""SELECT artikeltyp.bezeichnung, ausleiheninhalt.serien_nr, ausleihe.ausleihe_id, ausleihe.startdatum, ausleihe.enddatum, ausleihe.versand
                    FROM ausleiheninhalt
                    JOIN ausleihe ON ausleihe.ausleihe_id = ausleiheninhalt.ausleihe_id
                    JOIN artikel ON artikel.serien_nr = ausleiheninhalt.serien_nr
                    JOIN artikeltyp ON artikeltyp.artikeltyp_id = artikel.artikeltyp_id
                    WHERE artikeltyp.bezeichnung = '{artikeltyp}'
                    """


        conn = sqlite3.connect("db\\verleihverwaltung.db")
        cursor = conn.cursor()
        data = cursor.execute(rentals_query).fetchall()


        conn.commit()
        cursor.close()
        column_name = ["bezeichnung", "seriennummer",
                    "ausleihe_id", "startdatum", "enddatum", "versand"]

        
        df = pd.DataFrame(data, columns=column_name)

        
        df["startdatum"] = pd.to_datetime(df["startdatum"])
        df["enddatum"] = pd.to_datetime(df["enddatum"])


        # Rueckgabe/Versanddatum der bestehenden Ausleihe berechnen und in den df einfügen

        df.loc[df["versand"] == 0, "versand_am"] = df["startdatum"] - timedelta(days=1)
        df.loc[df["versand"] == 0, "rueckgabe_am"] = df["enddatum"] + timedelta(days=2)

        df.loc[df["versand"] == 1, "versand_am"] = df["startdatum"] - timedelta(days=3)
        df.loc[df["versand"] == 1, "rueckgabe_am"] = df["enddatum"] + timedelta(days=3)


        if newAusleiheVersand == 0:
            anfrage_start = startNewAusleihe - timedelta(days=1)
            print(f"Start der Anfrage bei und inkl. abholung: {anfrage_start}")
            anfrage_ende = endNewAusleihe + timedelta(days=2)
            print(f"Ende der Anfrage bei und inkl. abholung: {anfrage_start}")
            

        else:
            anfrage_start = startNewAusleihe - timedelta(days=3)
            anfrage_ende = endNewAusleihe + timedelta(days=3)
            print(f"Start der Anfrage bei und inkl Versand: {anfrage_start}")
            print(f"Ende der Anfrage bei und inkl Versand: {anfrage_ende}")


        df["delta_ rueckgabeAlt_versandNeu"] = (
            anfrage_start - df["rueckgabe_am"]).dt.days
        df["delt_versandbestand_ rueckgabeNeu"] = (
            df["versand_am"] - anfrage_ende).dt.days


        df["überschneidung"] = np.where((df["delta_ rueckgabeAlt_versandNeu"] > 0) & (df["delt_versandbestand_ rueckgabeNeu"] < 0) | (
            df["delta_ rueckgabeAlt_versandNeu"] < 0) & (df["delt_versandbestand_ rueckgabeNeu"] > 0), 0, 1)
        
        #Get all Serial Numbers for Article Type

        serial_nr_query = f"""SELECT artikeltyp.bezeichnung, ausleiheninhalt.serien_nr, ausleihe.ausleihe_id, ausleihe.startdatum, ausleihe.enddatum, ausleihe.versand
                    FROM ausleiheninhalt
                    JOIN ausleihe ON ausleihe.ausleihe_id = ausleiheninhalt.ausleihe_id
                    JOIN artikel ON artikel.serien_nr = ausleiheninhalt.serien_nr
                    JOIN artikeltyp ON artikeltyp.artikeltyp_id = artikel.artikeltyp_id
                    WHERE artikeltyp.bezeichnung = '{artikeltyp}'
                    """


        conn = sqlite3.connect("db\\verleihverwaltung.db")
        cursor = conn.cursor()
        data = cursor.execute(serial_nr_query).fetchall()


        conn.commit()
        cursor.close()


        serial_nr_query = f"""SELECT artikel.serien_nr
                        FROM artikel
                        JOIN artikeltyp ON artikeltyp.artikeltyp_id = artikel.artikeltyp_id
                        WHERE artikeltyp.bezeichnung = '{artikeltyp}'
                    """


        conn = sqlite3.connect("db\\verleihverwaltung.db")
        cursor = conn.cursor()
        data = cursor.execute(serial_nr_query).fetchall()


        conn.commit()
        cursor.close()


        serial_nr = []
        for element in data:
            serial_nr.append(element[0])

        print(f"Liste der Seriennummer: {serial_nr}")
        verfügbare_serial = []
        nicht_verfügbare_serial = []

        
        for serial in serial_nr:
            df_serial = df.loc[df["seriennummer"] == f"{serial}"]
           

            if (df_serial["überschneidung"].mean() == 0 or df_serial.empty):
                
                verfügbare_serial.append(serial)

            else:
                
                nicht_verfügbare_serial.append(serial)

        print(f"Verfügbare Seriennummern: {verfügbare_serial}")
        
        if len(verfügbare_serial) == 0:
            return "Nicht verfügbar"
        else:
            return random.choice(verfügbare_serial)

    def addShippingCost(self):

        if (self.shipping_cb.currentIndex() > 1) :
            
            shipping_type = self.shipping_cb.currentText()

            shipping_price_query = f"""SELECT preis
                        FROM versandkosten
                        
                        WHERE bezeichnung = '{shipping_type}'
                    """


            conn = sqlite3.connect("db\\verleihverwaltung.db")
            cursor = conn.cursor()
            shipping_cost = cursor.execute(shipping_price_query).fetchall()[0][0]


            conn.commit()
            cursor.close()
            self.total_le.setText(str(shipping_cost))
            
        else:
            pass