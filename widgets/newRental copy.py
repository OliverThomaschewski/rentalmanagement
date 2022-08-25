
from ast import Delete
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *


class NewRental(QWidget):
    # Calender for daterange

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.article_count = 0

        # Verticales Layout für new_rental Tab
        self.new_rental_tab_layout = QVBoxLayout(self)
        self.new_rental_tab_layout.setContentsMargins(40, 20, 40, 20)

        self.cal_start = QCalendarWidget()
        self.cal_end = QCalendarWidget()

        # Calender in horizontalem Tab anordnen

        self.cal_layout = QHBoxLayout()
        self.cal_layout.addWidget(self.cal_start)
        self.cal_layout.addWidget(self.cal_end)

        self.cal_frame = QFrame()

        self.cal_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.cal_frame.setLineWidth(3)
        self.cal_frame.setMidLineWidth(3)
        self.cal_frame.setLayout(self.cal_layout)

        self.new_rental_tab_layout.addWidget(self.cal_frame)

        # ARTICLE LINE

        self.articles_layout = QVBoxLayout()
        self.new_rental_line_layout = QHBoxLayout()

        # Dropdown, Ausgabezeilte, + Button

        self.article_cb = QComboBox()
        self.article_cb.setObjectName("article_cb_0")
        self.article_cb.setFixedSize(200, 20)
        self.article_cb.setPlaceholderText("Artikel wählen")

        self.article_label = QLabel("Hier wird Seriennummer angezeigt")
        self.article_label.setObjectName("article_label_0")

        self.add_line_pb = QPushButton()
        self.add_line_pb.setText("+")
        self.add_line_pb.setFixedWidth(20)
        self.add_line_pb.clicked.connect(self.addGroupBox)

        self.new_rental_line_layout.addWidget(self.article_cb)
        self.new_rental_line_layout.addWidget(self.article_label)
        self.new_rental_line_layout.addWidget(self.add_line_pb)

        # self.articles_layout.addLayout(self.new_rental_line_layout)

        #self.new_rental_line_frame = QFrame()
        # self.new_rental_line_frame.setFrameShape(QFrame.Shape.StyledPanel)
        # self.new_rental_line_frame.setLayout(self.articles_layout)

        # Groupbox test
        self.new_rental_line_gb = QGroupBox("Das ist Zeile 1")
        self.new_rental_line_gb.setLayout(self.new_rental_line_layout)

        self.articles_layout.addWidget(self.new_rental_line_gb)

        # Add to Overall Layout

        self.new_rental_tab_layout.addLayout(self.articles_layout)

        # PRICE LAYOUT

        self.price_layout = QVBoxLayout()

        self.price_la_layout = QHBoxLayout()
        self.price_le_layout = QHBoxLayout()

        self.days_la = QLabel("Anzahl Tage")
        self.weeks_la = QLabel("Anzahl Wochen")
        self.shipping_la = QLabel("Versandkosten")
        self.total_la = QLabel("Gesamtpreis")

        self.days_le = QLineEdit()
        # self.days_le.setFixedWidth(75)
        # self.days_le.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.weeks_le = QLineEdit()
        # self.weeks_le.setFixedWidth(75)
        self.shipping_le = QLineEdit()
        # self.shipping_le.setFixedWidth(75)
        self.total_le = QLineEdit()
        # self.total_le.setFixedWidth(75)

        self.price_la_layout.addWidget(self.days_la)
        self.price_la_layout.addWidget(self.weeks_la)
        self.price_la_layout.addWidget(self.shipping_la)
        self.price_la_layout.addWidget(self.total_la)

        self.price_le_layout.addWidget(self.days_le)
        self.price_le_layout.addWidget(self.weeks_le)
        self.price_le_layout.addWidget(self.shipping_le)
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

        # Adress fields

        self.name_label = QLabel("Name")
        self.name_label.setFixedWidth(50)
        self.surname_label = QLabel("Vorname")
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
        self.new_rental_tab_layout.addWidget(self.save_rental_bt)


    # class to save the artivels of the rental
    # class RentalContent(self):
        #serial_nr = None
"""
    def add_articleline(self):

        self.article_count += 1

        self.new_rental_line_layout_add = QHBoxLayout()
        self.new_rental_line_layout.setObjectName(f"nrll_{self.article_count}")
        # Dropdown, Ausgabezeilte, + Button

        self.article_cb = QComboBox()
        self.article_cb.setFixedSize(200, 20)
        self.article_cb.setPlaceholderText("Artikel wählen")
        self.article_cb.setObjectName(f"article_cb_{self.article_count}")

        self.article_label = QLabel(f"testlabel {self.article_count}")
        self.article_label.setObjectName(f"article_label_{self.article_count}")

        self.add_line_pb = QPushButton()
        self.add_line_pb.setText("+")
        self.add_line_pb.setFixedSize(20, 20)
        self.add_line_pb.clicked.connect(self.add_articleline)

        self.remove_line_pb = QPushButton()
        self.remove_line_pb.setText("-")
        self.remove_line_pb.setFixedWidth(20)
        self.remove_line_pb.clicked.connect(self.removeArticle)


        self.new_rental_line_layout_add.addWidget(self.article_cb, )
        self.new_rental_line_layout_add.addWidget(self.article_label)
        self.new_rental_line_layout_add.addWidget(self.add_line_pb)
        self.new_rental_line_layout_add.addWidget(self.remove_line_pb)

        #print(f"New rental line count ( in add): {self.new_rental_line_layout.count()}")





        # In Layout einbauen

        # self.articles_layout.addLayout(self.new_rental_line_layout_add)
        self.new_rental_line_gb.setLayout(self.new_rental_line_layout_add)


        #print(self.findChild(
            #QLabel, f"article_label_{self.article_count}").text())

        # Objekt Typ ausleiheninhalt erstellen und die benötigten Daten rein speichern und das in ner Liste speichern

"""

    def removeArticleLine(self):

        print(
            f"New rental line count ( in delete): {self.new_rental_line_layout_add.count()}")
        while self.new_rental_line_layout_add.count():
            item = self.new_rental_line_layout_add.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.setParent(None)
                print(
                    f"New rental line count ( in while): {self.new_rental_line_layout_add.count()}")

        self.article_count -= 1

    def removeArticleLine2(self):

        print(
            f"New rental line count ( in delete): {self.new_rental_line_layout_add.count()}")
        while self.new_rental_line_layout_add.count():
            item = self.new_rental_line_layout_add.takeAt(0)
            widget = item.widget()

            if widget is not None:
                widget.setParent(None)
            print(
                f"New rental line count ( in while): {self.new_rental_line_layout_add.count()}")

        self.article_count -= 1

    def removeArticle(self):

        count = self.new_rental_line_layout_add.count()
        item = self.new_rental_line_layout_add.itemAt(count - 2)
        self.new_rental_line_layout_add.removeItem(item)

        def addGroupBox(self):
            self.article_count += 1

            self.new_rental_line_layout_add = QHBoxLayout()
            self.new_rental_line_layout.setObjectName(f"nrll_{self.article_count}")
            # Dropdown, Ausgabezeilte, + Button

            self.article_cb = QComboBox()
            self.article_cb.setFixedSize(200, 20)
            self.article_cb.setPlaceholderText("Artikel wählen")
            self.article_cb.setObjectName(f"article_cb_{self.article_count}")

            self.article_label = QLabel(f"testlabel {self.article_count}")
            self.article_label.setObjectName(f"article_label_{self.article_count}")

            self.add_line_pb = QPushButton()
            self.add_line_pb.setText("+")
            self.add_line_pb.setFixedSize(20, 20)
            self.add_line_pb.clicked.connect(self.addGroupBox)

            self.remove_line_pb = QPushButton()
            self.remove_line_pb.setText("-")
            self.remove_line_pb.setFixedWidth(20)
            self.remove_line_pb.clicked.connect(self.removeArticle)

            self.new_rental_line_layout_add.addWidget(self.article_cb, )
            self.new_rental_line_layout_add.addWidget(self.article_label)
            self.new_rental_line_layout_add.addWidget(self.add_line_pb)
            self.new_rental_line_layout_add.addWidget(self.remove_line_pb)

            self.added_gb = QGroupBox("Das ist added")
            self.added_gb.setLayout(self.new_rental_line_layout_add)

            # In Layout einbauen

            self.articles_layout.addWidget(self.added_gb)
