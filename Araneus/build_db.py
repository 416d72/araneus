# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE

from Araneus.helpers import *
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
from PyQt5.uic import loadUi



class BuildDB(QDialog):
    """
    This class controls build_db dialog and interacts with Database model to build a new database.
    """

    def __init__(self):
        super(BuildDB, self).__init__()
        loadUi(load_ui('empty_db'), self)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pref = BuildDB()
    sys.exit(app.exec_())


def new_window():
    """
    Provide a method to reach this dialog from the main window
    :return: None
    """
    global pref
    pref = BuildDB()
