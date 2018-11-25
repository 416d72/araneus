#!usr/bin/python3
# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE

from Araneus.helpers import *

from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi


class Preferences(QDialog):
    """
    This class controls preferences dialog and interacts with configurations model to read/modify
    application configurations
    TODO: Implement interface with configurations.py
    """

    def __init__(self):
        super(Preferences, self).__init__()
        loadUi(load_ui('preferences'), self)
        self.show()

    def ok(self):
        """
        Save any modified settings to configuration file
        TODO: link this method with the action that triggered when clicking `ok` button
        :return:
        """
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pref = Preferences()
    sys.exit(app.exec_())


def new_window():
    """
    Provide a method to reach this dialog from the main window
    :return: None
    """
    global pref
    pref = Preferences()
