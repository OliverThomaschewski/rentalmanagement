from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *

import sys
from widgets.activeRentals import ActiveRentals
from widgets.articles import Articles

from widgets.newRental import NewRental


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Verleihverwaltung")
        self.resize(1200, 600)

        self.tabs = QTabWidget()

        self.setCentralWidget(self.tabs)

        self.new_rental_tab = NewRental(self)
        self.active_rentals_tab = ActiveRentals(self)
        self.articles_tab = Articles(self)

        self.tabs.addTab(self.new_rental_tab, "Neue Ausleihe")
        self.tabs.addTab(self.active_rentals_tab, "Aktive Ausleihen")
        self.tabs.addTab(self.articles_tab, "Artikel Hinzufügen")

        

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
