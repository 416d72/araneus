#!usr/bin/python3
# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE

from Araneus.helpers import *

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QApplication, QShortcut
from PyQt5.QtGui import QKeySequence, QKeyEvent
from PyQt5.uic import loadUi


class Preferences(QDialog):
    def __init__(self):
        super(Preferences, self).__init__()
        loadUi(load_ui('preferences'), self)
        self.show()


app = QApplication(sys.argv)
pref = Preferences()
sys.exit(app.exec_())
