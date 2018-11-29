# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE

import random
import time
from datetime import datetime
from Araneus.history import *
from Araneus.database import *
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.Qt import QTreeWidgetItem
from PyQt5.uic import loadUi

db = Database()
c = Configurations()
history = History()


class Main(QMainWindow):
    view_col_modified = c.get_option('VIEW_COLUMNS', 'modified', 'bool')
    view_col_accessed = c.get_option('VIEW_COLUMNS', 'accessed', 'bool')
    view_col_type = c.get_option('VIEW_COLUMNS', 'type', 'bool')

    def __init__(self):
        super(Main, self).__init__()
        loadUi(load_ui('main_window'), self)
        self.progressBar.hide()
        self.get_view_columns()
        self.triggers()
        self.set_view_columns()
        self.press()

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

    def press(self):
        """
        Key press trigger
        :return: None
        """
        self.search_btn.clicked.connect(lambda: self.fetch(self.search_bar.text()))
        self.search_bar.returnPressed.connect(lambda: self.fetch(self.search_bar.text()))

    def fetch(self, term):
        """
        Grab results from database
        :return: None
        """
        # Storing search term to history file:
        history.add(term)
        # Deleting all items from QTreeWidget
        self.treeWidget.clear()
        # Listing results
        if len(term) > 0:
            for result in db.get(term):
                if not c.get_option('SEARCH', 'Show_hidden_files', 'bool') and result[0].startswith('.'):
                    continue
                else:
                    item = QTreeWidgetItem(self.treeWidget)
                    item.setText(0, str(result[0]))  # Name
                    item.setText(1, self._convert(eval(result[1])))  # Size
                    item.setText(2, str(result[2]))  # Location
                    item.setText(3, datetime.utcfromtimestamp(float(result[3])).strftime('%Y-%m-%d %H:%M'))  # Modified
                    item.setText(4, datetime.utcfromtimestamp(float(result[4])).strftime('%Y-%m-%d %H:%M'))  # Accessed
                    item.setText(5, str(result[5]))  # Type
                    self.treeWidget.addTopLevelItem(item)

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

    def preferences_dialog(self):
        """
        Showing preferences dialog
        :return: None
        """
        from Araneus.preferences import Preferences
        global pref
        pref = Preferences()
        pref.buttonBox.accepted.connect(lambda: self.fetch(self.search_bar.text()))

    def build_all_action(self):
        """
        Running 'Build' task
        :return: None
        """
        self.progressBar.show()
        self.statusBar().showMessage('Building')
        for i in range(0, 15):
            time.sleep(0.04)
            self.progressBar.setValue(i)
        time.sleep(random.uniform(0, 1))
        self.progressBar.setValue(random.randint(16, 33))
        time.sleep(random.uniform(0, 1))
        db.build()
        self.progressBar.setValue(random.randint(34, 66))
        time.sleep(random.uniform(0, 1))
        self.progressBar.setValue(random.randint(67, 94))
        for i in range(95, 101):
            time.sleep(0.1)
            self.progressBar.setValue(i)
        self.progressBar.hide()
        self.statusBar().showMessage('')

    @staticmethod
    def about_dialog(self):
        """
        Showing the about dialog | Influenced by the about dialog from 'Zeal' app
        :return: None
        """
        from Araneus.about import new_window
        new_window()

    @staticmethod
    def _convert(size: int):
        if size == 0:
            return ''
        elif size < 1024:
            return '%d Bytes' % size
        power = 2 ** 10
        n = 0
        d = {0: 'Bytes', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
        while size >= power:
            size /= power
            n += 1
        return "%.2f " % round(size, 2) + d[n]


def main():
    main_w = QApplication(sys.argv)
    main_window = Main()
    main_window.show()
    main_window.check_empty_db()
    sys.exit(main_w.exec_())


if __name__ == "__main__":
    main()
