from asyncio.windows_events import NULL
import math
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

import sqlite3
from widgets.deactivateArticleType import DeactivateArticleType
from widgets.deactivateSerialNr import DeactivateSerialNr

from widgets.newTypeDialog import NewTypeDialog






class Articles(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.article_tab_layout = QVBoxLayout(self)
        self.article_tab_layout.setContentsMargins(40, 20, 40, 20)

        # ADD NEW TYPE

        self.choose_type_layout = QHBoxLayout()

        # Add Type Button

        self.new_type_bt = QPushButton("Typ hinzufügen")
        self.new_type_bt.setFixedWidth(100)
        self.new_type_bt.clicked.connect(self.add_type)

        self.deactivateTypeButton = QPushButton("Typ deaktivieren")
        self.deactivateTypeButton.setFixedWidth(100)
        self.deactivateTypeButton.clicked.connect(self.deactivateArticleType)

        self.deactivateSerialButton = QPushButton("SerienNr deaktivieren")
        self.deactivateSerialButton.setFixedWidth(100)
        self.deactivateSerialButton.clicked.connect(self.deactivateSerialNr)

        # Put Type Layout together

        self.choose_type_layout.addWidget(self.new_type_bt)
        self.choose_type_layout.addWidget(self.deactivateTypeButton)
        self.choose_type_layout.addWidget(self.deactivateSerialButton)

        self.type_frame = QFrame()

        self.type_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.type_frame.setLayout(self.choose_type_layout)

        self.article_tab_layout.addWidget(self.type_frame)

        # ADD ARTICLE
        self.type_cb = QComboBox()
        self.type_cb.setPlaceholderText("Typ auswählen")
        self.type_cb.setFixedWidth(200)
        self.type_cb.activated.connect(self.showArticles)

        # Get Article Types and add to ComboBox
        conn = sqlite3.connect("db\\verleihverwaltung.db")
        query = f"""SELECT bezeichnung FROM artikeltyp WHERE aktiv = 1"""

        data = conn.execute(query).fetchall()
        self.type_cb.addItems([i[0] for i in data])

        conn.close()

        self.new_article_layout = QVBoxLayout()

        self.new_article_label_layout = QHBoxLayout()

        self.serial_nr_label = QLabel("Seriennummer")
        self.dummy_la = QLabel("")

        self.new_article_label_layout.addWidget(self.dummy_la)
        self.new_article_label_layout.addWidget(self.serial_nr_label)

        self.new_article_layout.addLayout(self.new_article_label_layout)

        self.new_article_le_layout = QHBoxLayout()
        self.serial_nr_le = QLineEdit()
        self.serial_nr_le.returnPressed.connect(self.addArticle)

        self.weekly_price_le = QLineEdit()
        self.new_article_bt = QPushButton("Speichern")
        self.new_article_bt.clicked.connect(self.addArticle)

        self.new_article_le_layout.addWidget(self.type_cb)
        self.new_article_le_layout.addWidget(self.serial_nr_le)
        self.new_article_le_layout.addWidget(self.new_article_bt)

        self.new_article_layout.addLayout(self.new_article_le_layout)

        self.new_article_frame = QFrame()

        self.new_article_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.new_article_frame.setLineWidth(3)
        self.new_article_frame.setMidLineWidth(3)
        self.new_article_frame.setLayout(self.new_article_layout)

        self.article_tab_layout.addWidget(self.new_article_frame)

        # List with articles in DataBase

        self.articles_list = QListWidget()

        self.article_tab_layout.addWidget(self.articles_list)

        # PRICE UPDATES

        self.update_layout = QHBoxLayout()

        self.update_price_label = QLabel("Neuer Wochenpreis")
        self.update_price_le = QLineEdit()
        self.update_price_le.returnPressed.connect(self.updatePrice)
        self.update_bt = QPushButton("Speichern")
        self.update_bt.clicked.connect(self.updatePrice)

        self.update_layout.addWidget(self.update_price_label)
        self.update_layout.addWidget(self.update_price_le)
        self.update_layout.addWidget(self.update_bt)

        self.update_frame = QFrame()

        self.update_frame.setFrameShape(QFrame.Shape.StyledPanel)

        self.update_frame.setLayout(self.update_layout)

        self.article_tab_layout.addWidget(self.update_frame)

        

    def add_type(self):
        dlg = NewTypeDialog(self)
        dlg.setWindowTitle("Typ hinzufügen")
        dlg.exec()

    def showArticles(self):

        self.articles_list.clear()

        artikeltyp = self.type_cb.currentText()
        freeSerialNumbers = []
        rentedSerialNumbers = []
        price = None

        # Get all Serial Numbers
        conn = sqlite3.connect("db\\verleihverwaltung.db")
        query = f"""SELECT artikel.serien_nr, artikeltyp.wochenpreis
                    FROM artikel
                    JOIN artikeltyp ON artikeltyp.artikeltyp_id = artikel.artikeltyp_id
                    WHERE artikeltyp.bezeichnung = '{artikeltyp}' AND artikel.aktiv = 1"""

        data = conn.execute(query).fetchall()

        conn.close()
        price = str(data[0][1]) + " €"

        for item in data:
            freeSerialNumbers.append(item[0])


        # Get Serial Numbers that are rented out until after today

        conn = sqlite3.connect("db\\verleihverwaltung.db")
        query = f"""SELECT artikel.serien_nr, artikeltyp.wochenpreis,ausleihe.startdatum, ausleihe.enddatum, ausleihe.ausleihe_id
                    FROM artikel
                    JOIN artikeltyp ON artikeltyp.artikeltyp_id = artikel.artikeltyp_id
                    LEFT JOIN ausleiheninhalt ON ausleiheninhalt.serien_nr = artikel.serien_nr
                    LEFT JOIN ausleihe ON ausleihe.ausleihe_id = ausleiheninhalt.ausleihe_id
                    WHERE artikeltyp.bezeichnung = '{artikeltyp}' AND (ausleihe.enddatum >= date() OR ausleihe.enddatum is NULL) AND artikel.aktiv = 1 AND storniert = 0"""

        data = conn.execute(query).fetchall()
    
        conn.close()

        # Showing Data in ListWidget, this could probably done prettier, but it works, yay!
       
        self.articles_list.addItem("Seriennummer\t\tWochenpreis\t\tStartdatum\t\tEnddatum\t\tAusleihe")
        try:
            for item in data:
                row = item[0] + "\t\t" + str(item[1]) + " €" + "\t\t" + str(item[2]) + "\t\t" + str(item[3]) + "\t\t" + str(item[4])
                self.articles_list.addItem(row)
                rentedSerialNumbers.append(item[0])
        except:
            pass


        for item in rentedSerialNumbers:
            if item in freeSerialNumbers:
                freeSerialNumbers.remove(item)
            else: 
                continue

        for item in freeSerialNumbers:
            self.articles_list.addItem(f"{item}\t\t{price}\t\tNicht verliehen")    


    def addArticle(self):

        try:
            # Get ID from Type
            conn = sqlite3.connect("db\\verleihverwaltung.db")
            
            query = f"""SELECT artikeltyp_id FROM artikeltyp WHERE bezeichnung = '{self.type_cb.currentText()}'"""
            artikeltyp_id = conn.execute(query).fetchall()[0][0]
            

            # INSERT new Article

            serien_nr = self.serial_nr_le.text()

            query = f"""INSERT INTO artikel (serien_nr, artikeltyp_id) VALUES ('{serien_nr}', {artikeltyp_id}) """
            conn.execute(query)
            conn.commit()
            conn.close()

            self.serial_nr_le.setText("")

            self.showArticles()

        except:
            msg = QMessageBox()
            msg.setWindowTitle("Achtung")
            msg.setText("Irgendwas ging schief!")
            x = msg.exec()

    def updatePrice(self):
        
        type = self.type_cb.currentText()
        new_wochenpreis = self.update_price_le.text()
        update_query = f"""UPDATE artikeltyp SET wochenpreis = {new_wochenpreis}
                    WHERE bezeichnung = '{type}'"""

        conn = sqlite3.connect("db\\verleihverwaltung.db")
        conn.execute(update_query)
        conn.commit()
        conn.close()

        self.showArticles()
        self.update_price_le.setText("")

    def setWeeklyPrice(self):

        # Amortisation is planned after 13 Weeks of Rental for Accessories
        amort_time = 13

        if self.price_le.text() == "":

            self.weekly_price_le.setText("")

        else:

            try:

                price = float(self.price_le.text())
                weekly_price = math.ceil(price/amort_time)
                self.weekly_price_le.setText(str(weekly_price))
            except:
                self.weekly_price_le.setText("Zahl eingeben")

    def deactivateArticleType(self):
        dlg =DeactivateArticleType(self)
        dlg.setWindowTitle("Artikeltyp löschen")
        dlg.exec()
    def deactivateSerialNr(self):

        dlg = DeactivateSerialNr(self)
        dlg.setWindowTitle("Seriennummer löschen")
        dlg.exec()
