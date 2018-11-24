#!usr/bin/python3
# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE

from Araneus.helpers import *

from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi


class About(QDialog):
    def __init__(self):
        super(About, self).__init__()
        loadUi(load_ui('about'), self)
        self.show()


app = QApplication(sys.argv)
pref = About()
sys.exit(app.exec_())
