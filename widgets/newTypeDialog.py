from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import sqlite3
import math



class NewTypeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

        self.resize(300, 200)

        self.input_type_layout = QHBoxLayout()
        self.input_price_layout = QHBoxLayout()
        self.input_weekly_price_layout = QHBoxLayout()
        self.input_buttons_layout = QHBoxLayout()
        self.input_layout = QVBoxLayout()

        self.type_la = QLabel("Typ")
        self.type_le = QLineEdit()

        self.input_type_layout.addWidget(self.type_la)
        self.input_type_layout.addWidget(self.type_le)

        self.input_layout.addLayout(self.input_type_layout)

        self.price_la = QLabel("Anschaffungspreis")
        self.price_la.setFixedWidth(100)
        self.price_le = QLineEdit()
        self.price_le.textChanged.connect(self.setWeeklyPrice)

        self.input_price_layout.addWidget(self.price_la)
        self.input_price_layout.addWidget(self.price_le)

        self.input_layout.addLayout(self.input_price_layout)

        self.weekly_price_la = QLabel("Wochenpreis")
        self.weekly_price_la.setFixedWidth(100)
        self.weekly_price_le = QLineEdit()

        self.input_weekly_price_layout.addWidget(self.weekly_price_la)
        self.input_weekly_price_layout.addWidget(self.weekly_price_le)

        self.input_layout.addLayout(self.input_weekly_price_layout)

        self.ok_bt = QPushButton("Speichern")
        self.ok_bt.clicked.connect(self.save_type)
        self.cancel_bt = QPushButton("Schließen")
        self.cancel_bt.clicked.connect(self.close_dialog)

        self.input_buttons_layout.addWidget(self.ok_bt)
        self.input_buttons_layout.addWidget(self.cancel_bt)

        self.input_layout.addLayout(self.input_buttons_layout)

        self.setLayout(self.input_layout)

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

    def save_type(self):
        try:
            wochenpreis = self.convertToFloat(self.weekly_price_le.text())
            type = self.type_le.text()
            conn = sqlite3.connect("db\\verleihverwaltung.db")
            query = f"""INSERT INTO artikeltyp (bezeichnung, wochenpreis) 
                        VALUES ('{type}', {wochenpreis}) """

            conn.execute(query)
            conn.commit()
            conn.close()
            
            self.type_le.setText("")
            self.price_le.setText("")
            self.weekly_price_le.setText("")

            self.parent.type_cb.addItem(type)
            self.parent.type_cb.setCurrentIndex(self.parent.type_cb.count()-1)

        except Exception as e:
            msg = QMessageBox()
            msg.setWindowTitle("Achtung")
            msg.setText(f"Irgendwas ging schief: {e}")
            x = msg.exec()

        
        
        

    def close_dialog(self):
        self.close()

        

    def convertToFloat(self, eingabe):

        if not eingabe:
            return float(0)

        try:
            value = float(eingabe)
        except ValueError:
            value = float(eingabe.replace(",", "."))
        finally:
            return value



