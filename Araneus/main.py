#!usr/bin/python3
# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE

from Araneus.helpers import *
from Araneus.configurations import *
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi

c = Configurations()


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        loadUi(load_ui('main_window'), self)
        self.triggers()
        self.get_view_columns()
        self.set_view_columns()
        self.show()

    def check_empty_db(self):
        """
        Checks if the database is empty and prompt the user to build it if empty.
        TODO: Implement connection to database.py
        :return: bool
        """
        pass

    def triggers(self):
        self.actionQuit.triggered.connect(lambda: sys.exit(QApplication(sys.argv).exec_()))
        self.actionPreferences.triggered.connect(self.preferences_dialog)
        self.actionBuild_All.triggered.connect(self.build_all_action)
        self.actionClean.triggered.connect(self.clean_all_action)
        self.actionAbout.triggered.connect(self.about_dialog)

    def preferences_dialog(self):
        """
        Showing preferences dialog
        :return: None
        """
        from Araneus.preferences import Preferences, new_window
        new_window()

    def get_view_columns(self):
        """
        Fetch current selected view columns
        :return: None
        """
        self.actionModified.setChecked(c.get_option('VIEW_COLUMNS', 'modified', 'bool'))
        self.actionCreated.setChecked(c.get_option('VIEW_COLUMNS', 'created', 'bool'))
        self.actionType.setChecked(c.get_option('VIEW_COLUMNS', 'type', 'bool'))

    def set_view_columns(self):
        """
        Save selected view columns in config file
        :return: None
        """
        self.actionModified.toggled.connect(lambda: c.set_option('VIEW_COLUMNS', 'modified',
                                                                 self.actionModified.isChecked()))
        self.actionCreated.toggled.connect(lambda: c.set_option('VIEW_COLUMNS', 'created',
                                                                self.actionCreated.isChecked()))
        self.actionType.toggled.connect(lambda: c.set_option('VIEW_COLUMNS', 'type',
                                                             self.actionType.isChecked()))

    def build_all_action(self):
        """
        Running 'Build' task
        :return: None
        """
        print("Building ...")

    def clean_all_action(self):
        """
        Running 'clean' task
        :return: None
        """
        print("Cleaned everything")

    def about_dialog(self):
        """
        Showing the about dialog
        :return: None
        """
        from Araneus.about import new_window
        new_window()


def main():
    main = QApplication(sys.argv)
    main_window = Main()
    sys.exit(main.exec_())


if __name__ == "__main__":
    main()
