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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = About()
    sys.exit(app.exec_())


def new_window():
    global window
    window = About()
