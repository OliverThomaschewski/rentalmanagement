from datetime import datetime, timedelta
from pickle import TRUE
import sqlite3
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

class OtherRevenues(QWidget):
    

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        
        self.revLayout = QVBoxLayout(self)
        self.revItemsLayout = QHBoxLayout()

        self.revCal = QCalendarWidget()
        self.revCal.setFixedSize(200, 200)
        self.revTextLabel = QLabel("Bezeichnung")
        self.revTextLabel.setFixedWidth(200)
        self.revTextLine = QLineEdit()
        self.revTextLine.setFixedWidth(200)
        self.revTextLine.returnPressed.connect(self.setCursor)
        self.revAmtLabel = QLabel("Betrag")
        self.revAmtLabel.setFixedWidth(200)
        self.revAmtLine = QLineEdit()
        self.revAmtLine.returnPressed.connect(self.saveRev)
        self.revAmtLine.setFixedWidth(200)  
        self.saveButton = QPushButton("Speichern")
        self.saveButton.clicked.connect(self.saveRev)
        self.saveButton.setFixedWidth(200)

        self.linesLayout = QVBoxLayout()

        self.linesLayout.addWidget(self.revTextLabel)
        self.linesLayout.addWidget(self.revTextLine)
        self.linesLayout.addWidget(self.revAmtLabel)
        self.linesLayout.addWidget(self.revAmtLine)
        self.linesLayout.addWidget(self.saveButton)

        self.revItemsLayout.addWidget(self.revCal)
        self.revItemsLayout.addLayout(self.linesLayout)

        self.revLayout.addLayout(self.revItemsLayout)
        

    def saveRev(self):

        datum = self.revCal.selectedDate().toString("yyyy-MM-dd")
        bezeichnung = self.revTextLine.text()
        betrag = self.convertToFloat(self.revAmtLine.text())



        conn = sqlite3.connect("db\\verleihverwaltung.db")
        query = f"""INSERT INTO sonsteinnahmen (datum, bezeichnung, betrag) VALUES ('{datum}', '{bezeichnung}', {betrag})"""
        conn.execute(query)
        conn.commit()
        conn.close()

        self.revTextLine.setText("")
        self.revAmtLine.setText("")

    def convertToFloat(self, betrag):

        try:
            betrag = float(betrag)
        except:
            betrag = betrag.replace(",", ".")

        finally:
            return betrag

    def setCursor(self):
        self.revAmtLine.setFocus()