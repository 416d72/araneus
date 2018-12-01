# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE
import time
from datetime import datetime
from Araneus.history import *
from Araneus.database import *
from PyQt5.QtWidgets import QMainWindow, QApplication, QCompleter
from PyQt5.Qt import QTreeWidgetItem, QRunnable, QThreadPool, QObject, pyqtSignal
from PyQt5.uic import loadUi

db = Database()
c = Configurations()
history = History()


class Communicate(QObject):
    myGUI_signal = pyqtSignal(str)


def MyThread(callbackFunc):
    # Setup the signal-slot mechanism.
    src = Communicate()
    src.myGUI_signal.connect(callbackFunc)
    src.myGUI_signal.emit(callbackFunc)


class ProcessRunnable(QRunnable):
    """
    Manages multiple threads to be used while building database.
    """

    def __init__(self, target):
        QRunnable.__init__(self)
        self.t = target

    def run(self):
        self.t()

    def start(self):
        QThreadPool.globalInstance().start(self)


class Main(QMainWindow):
    view_col_modified = c.get_option('VIEW_COLUMNS', 'modified', 'bool')
    view_col_accessed = c.get_option('VIEW_COLUMNS', 'accessed', 'bool')
    view_col_type = c.get_option('VIEW_COLUMNS', 'type', 'bool')

    def __init__(self):
        # TODO: add icons to UI
        # TODO: show last entered keywords
        super(Main, self).__init__(parent=None)
        self.thread()
        loadUi(load_ui('main_window'), self)
        self.progressBar.hide()
        self.statusBar().showMessage('Ready')
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
            self.search_bar.setEnabled(0)
            self.search_btn.setEnabled(0)
            self.statusBar().showMessage('No database found!')
            self.build_db()

    def triggers(self):
        self.actionQuit.triggered.connect(lambda: sys.exit())
        self.actionPreferences.triggered.connect(self.preferences_dialog)
        self.actionBuild_All.triggered.connect(lambda: ProcessRunnable(target=self.build_all_action).start())
        # self.actionBuild_All.triggered.connect(lambda: self.build_all_action())
        self.actionAbout.triggered.connect(about_dialog)

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

    def history(self, add_new: str = ''):
        """
        Get last entered keywords
        :return: None
        """
        if add_new:
            history.add(add_new)
        pass

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
        # Checking if database exists:
        c.create_config_file()
        db.create()
        self.check_empty_db()
        self.statusBar().showMessage('Ready')
        # Storing search term to history file:
        self.history(term)
        # Deleting all items from QTreeWidget
        self.treeWidget.clear()
        # Listing results
        if len(term) > 0:
            for result in db.get(term):
                if not c.get_option('SEARCH', 'Show_hidden_files', 'bool') and result[0].startswith('.'):
                    continue
                else:
                    # Setting item and it's properties
                    item = QTreeWidgetItem(self.treeWidget)
                    item.setText(0, str(result[0]))  # Name
                    item.setText(1, convert(eval(result[1])))  # Size
                    item.setText(2, str(result[2]))  # Location
                    item.setText(3, datetime.utcfromtimestamp(float(result[3])).strftime('%Y-%m-%d %H:%M'))  # Modified
                    item.setText(4, datetime.utcfromtimestamp(float(result[4])).strftime('%Y-%m-%d %H:%M'))  # Accessed
                    item.setText(5, str(result[5]))  # Type
                    # Generating context menu.
                    # menu = QMenu(self)
                    # open_action = QAction('Open', self)
                    # open_action.triggered.connect(lambda: print('Open'))
                    # menu.addAction(open_action)
                    # menu.popup(QCursor.pos())

                    # Adding the item
                    self.treeWidget.addTopLevelItem(item)
            for i in range(6):
                self.treeWidget.resizeColumnToContents(i)

    def context_menu(self, event):
        """
        Shows context menu when right clicking a result item
        :param event:
        :return:
        """
        pass

    def build_db(self):
        """
        Show the build_db dialog
        :return: None
        """
        from Araneus.build_db import BuildDB
        bdb = BuildDB()
        bdb.buttonBox.accepted.connect(lambda: ProcessRunnable(target=self.build_all_action).start())
        # bdb.buttonBox.accepted.connect(lambda: self.build_all_action())
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
        # self.actionBuild_All.setDisabled(True)
        # self.progressBar.show()
        self.statusBar().showMessage('Building')
        db.build()
        # for progress in db.build():
        #     self.update_progress_bar(progress)
        #     self.statusBar().showMessage('Building')
        # self.progressBar.setValue(100)
        # self.progressBar.hide()
        self.statusBar().showMessage('Ready')
        self.search_bar.setEnabled(1)
        self.search_btn.setEnabled(1)
        # self.actionBuild_All.setDisabled(False)


def main():
    main_w = QApplication(sys.argv)
    main_window = Main()
    main_window.show()
    # TODO: show maximized
    # main_window.showMaximized()
    main_window.check_empty_db()
    sys.exit(main_w.exec_())


if __name__ == "__main__":
    main()
