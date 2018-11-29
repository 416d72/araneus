# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE

from Araneus.database import *
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi

db = Database()
c = Configurations()


class Main(QMainWindow):
    view_col_modified = c.get_option('VIEW_COLUMNS', 'modified', 'bool')
    view_col_accessed = c.get_option('VIEW_COLUMNS', 'accessed', 'bool')
    view_col_type = c.get_option('VIEW_COLUMNS', 'type', 'bool')

    def __init__(self):
        super(Main, self).__init__()
        loadUi(load_ui('main_window'), self)
        self.get_view_columns()
        self.triggers()
        self.set_view_columns()

    def check_empty_db(self):
        """
        Checks if the database is empty and prompt the user to build it if empty.
        :return: bool
        """
        db.create()
        if not db.fetch_all():
            self.build_db()

    def triggers(self):
        self.actionQuit.triggered.connect(lambda: sys.exit())
        self.actionPreferences.triggered.connect(self.preferences_dialog)
        self.actionBuild_All.triggered.connect(self.build_all_action)
        self.actionAbout.triggered.connect(self.about_dialog)

    def get_view_columns(self):
        """
        Fetch current selected view columns
        :return: None
        """
        self.actionModified.setChecked(self.view_col_modified)
        self.actionAccess.setChecked(self.view_col_accessed)
        self.actionType.setChecked(self.view_col_type)
        self.refresh_list()

    def set_view_columns(self):
        """
        Updates view columns on toggling settings
        :return: None
        """
        self.actionModified.toggled.connect(lambda: self.update_view_columns())
        self.actionAccess.toggled.connect(lambda: self.update_view_columns())
        self.actionType.toggled.connect(lambda: self.update_view_columns())

    def update_view_columns(self):
        """
        Updates configurations for selected view columns
        :return: None
        """
        self.view_col_modified = self.actionModified.isChecked()
        self.view_col_accessed = self.actionAccess.isChecked()
        self.view_col_type = self.actionType.isChecked()
        c.set_option('VIEW_COLUMNS', 'modified', self.view_col_modified)
        c.set_option('VIEW_COLUMNS', 'accessed', self.view_col_accessed)
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
        if self.view_col_accessed:
            self.treeWidget.showColumn(4)
        else:
            self.treeWidget.hideColumn(4)
        if self.view_col_type:
            self.treeWidget.showColumn(5)
        else:
            self.treeWidget.hideColumn(5)

    def build_db(self):
        """
        Show the build_db dialog
        :return: None
        """
        from Araneus.build_db import BuildDB, new_window
        bdb = BuildDB()
        bdb.buttonBox.accepted.connect(lambda: self.build_all_action())
        global pref
        pref = bdb

    @staticmethod
    def preferences_dialog(self):
        """
        Showing preferences dialog
        :return: None
        """
        from Araneus.preferences import new_window
        new_window()

    def build_all_action(self):
        """
        Running 'Build' task
        :return: None
        """
        self.statusBar().showMessage('Building')
        db.build()
        self.statusBar().showMessage('')

    @staticmethod
    def _convert(self, size: int):
        power = 2 ** 10
        n = 0
        d = {0: 'Bytes', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
        while size >= power:
            size /= power
            n += 1
        return "%.2f " % round(size, 2) + d[n], int(size)

    @staticmethod
    def about_dialog(self):
        """
        Showing the about dialog | Influenced by the about dialog from 'Zeal' app
        :return: None
        """
        from Araneus.about import new_window
        new_window()


def main():
    main_w = QApplication(sys.argv)
    main_window = Main()
    main_window.show()
    main_window.check_empty_db()
    sys.exit(main_w.exec_())


if __name__ == "__main__":
    main()
