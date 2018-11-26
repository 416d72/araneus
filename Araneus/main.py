#!usr/bin/python3
# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE

from Araneus.helpers import *
from Araneus.configurations import *
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi

c = Configurations()


class Main(QMainWindow):
    view_col_modified = c.get_option('VIEW_COLUMNS', 'modified', 'bool')
    view_col_created = c.get_option('VIEW_COLUMNS', 'created', 'bool')
    view_col_type = c.get_option('VIEW_COLUMNS', 'type', 'bool')

    def __init__(self):
        super(Main, self).__init__()
        loadUi(load_ui('main_window'), self)
        self.get_view_columns()
        self.triggers()
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
        self.actionQuit.triggered.connect(lambda: sys.exit())
        self.actionPreferences.triggered.connect(self.preferences_dialog)
        self.actionBuild_All.triggered.connect(self.build_all_action)
        self.actionClean.triggered.connect(self.clean_all_action)
        self.actionAbout.triggered.connect(self.about_dialog)

    @staticmethod
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
        self.actionModified.setChecked(self.view_col_modified)
        self.actionCreated.setChecked(self.view_col_created)
        self.actionType.setChecked(self.view_col_type)
        self.refresh_list()

    def set_view_columns(self):
        """
        Updates view columns on toggling settings
        :return: None
        """
        self.actionModified.toggled.connect(lambda: self.update_view_columns())
        self.actionCreated.toggled.connect(lambda: self.update_view_columns())
        self.actionType.toggled.connect(lambda: self.update_view_columns())

    def update_view_columns(self):
        """
        Updates configurations for selected view columns
        :return: None
        """
        self.view_col_modified = self.actionModified.isChecked()
        self.view_col_created = self.actionCreated.isChecked()
        self.view_col_type = self.actionType.isChecked()
        c.set_option('VIEW_COLUMNS', 'modified', self.view_col_modified)
        c.set_option('VIEW_COLUMNS', 'created', self.view_col_created)
        c.set_option('VIEW_COLUMNS', 'type', self.view_col_type)
        self.refresh_list()

    def refresh_list(self):
        """
        Refresh list when changing view columns settings or typing a search term
        :return: None
        """
        if self.view_col_modified:
            self.treeWidget.showColumn(3)
        else:
            self.treeWidget.hideColumn(3)
        if self.view_col_created:
            self.treeWidget.showColumn(4)
        else:
            self.treeWidget.hideColumn(4)
        if self.view_col_type:
            self.treeWidget.showColumn(5)
        else:
            self.treeWidget.hideColumn(5)

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

    @staticmethod
    def about_dialog(self):
        """
        Showing the about dialog | Influenced by the about dialog from 'Zeal' app
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
