# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE
from datetime import datetime
from Araneus.history import *
from Araneus.database import *
from PyQt5.QtCore import QThread, QObject, pyqtSlot, pyqtSignal, QStringListModel, QPoint
from PyQt5.QtWidgets import QMainWindow, QApplication, QTreeWidgetItem, QCompleter, QMenu, QAction
from PyQt5.QtGui import QCursor
from PyQt5.QtSvg import QSvgWidget
from PyQt5.uic import loadUi

db = Database()
c = Configurations()


# noinspection PyArgumentList
class Worker(QObject):
    started = pyqtSignal(int)
    progress = pyqtSignal(int)
    finished = pyqtSignal(int)
    stop = pyqtSignal(int)

    current_progress = 0

    @pyqtSlot()
    def build(self):
        """
        Loop through given method and extract data and passing it via signal
        :return: None
        """
        self.started.emit(0)
        for progress in db.build():
            self.current_progress += 1
            self.progress.emit(self.current_progress)
        self.finished.emit(0)
        self.stop.emit(0)
        self.current_progress = 0


class Main(QMainWindow):
    view_col_modified = c.get_option('VIEW_COLUMNS', 'modified', 'bool')
    view_col_accessed = c.get_option('VIEW_COLUMNS', 'accessed', 'bool')
    view_col_type = c.get_option('VIEW_COLUMNS', 'type', 'bool')
    total_dirs = 0
    svgWidget = None

    # noinspection PyArgumentList
    def __init__(self):
        super(Main, self).__init__()
        self.worker = Worker()
        self.thread = QThread()
        loadUi(load_ui('main_window'), self)
        self.statusBar().showMessage('Ready')
        self.search_bar.setFocus()
        self.get_view_columns()
        self.triggers()
        self.set_view_columns()
        self.press()
        self.completer = QCompleter()
        self.search_bar.setCompleter(self.completer)

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
            self.build_db_dialog('new')

    def triggers(self):
        self.actionQuit.triggered.connect(lambda: sys.exit())
        self.actionPreferences.triggered.connect(self.preferences_dialog)
        self.actionBuild_All.triggered.connect(lambda: self.build_all_action())
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

    def history(self, add_new: str = ''):
        """
        Get last entered keywords
        :return: None
        """
        history = History()
        # Add a new entry to history file
        history.add(add_new)
        model = QStringListModel()
        self.completer.setModel(model)
        model.setStringList(history.get())

    def press(self):
        """
        Key press trigger
        :return: None
        """
        self.search_btn.clicked.connect(lambda: self.fetch(self.search_bar.text()))
        self.search_bar.returnPressed.connect(lambda: self.fetch(self.search_bar.text()))
        self.search_bar.textChanged.connect(lambda: self.history())

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
            self.treeWidget.itemDoubleClicked.connect(self.view_item)
            self.treeWidget.customContextMenuRequested.connect(self.view_context_menu)

    def view_item(self, mode: str = 'name'):
        """
        View file or directory in the default app
        :return: None
        """
        name = self.treeWidget.currentItem().text(0)
        path = self.treeWidget.currentItem().text(2)
        item_type = self.treeWidget.currentItem().text(5)
        if item_type == 'Directory' or mode == 'location':
            """
            Open directory or select 'open containing directory' from context menu
            """
            command = subprocess.call(["xdg-open", path])
        else:
            command = subprocess.call(["xdg-open", path + name])
        if command == 4:  # Location doesn't exist
            self.build_db_dialog('update')

    def view_context_menu(self):
        """
        Yes as you expected, This shows a context menu upon right clicking on an item.
        TODO: add icons
        :return: None
        """
        item_type = self.treeWidget.currentItem().text(5)
        mouse = QCursor.pos()  # Get current mouse position
        menu = QMenu(self)
        menu.setFocus(True)
        # Adding custom actions
        action_open = menu.addAction('open')
        action_open_dir = None
        if item_type is not "Directory":
            # If the current selected item is a directory, there's no need to add an option to Open containing directory
            action_open_dir = menu.addAction('Open containing directory')
        menu.addSeparator()
        action_cut = menu.addAction('Cut')
        action_copy = menu.addAction('Copy')
        action_paste = menu.addAction('Paste')
        menu.addSeparator()
        action_delete = menu.addAction('Delete from disk')
        # Showing the menu right at the mouse position
        action = menu.exec_(mouse)
        # Controlling actions:
        if action_open == action:
            self.view_item()
        elif action == action_open_dir:
            self.view_item('location')

    def context_menu(self, event):
        """
        Shows context menu when right clicking a result item
        :param event:
        :return:
        """
        pass

    def build_db_dialog(self, msg: str):
        """
        TODO: convert this to be a global warning message which contents changes based on the event output
        Show the build_db dialog
        :param msg contains a custom message to be shown instead of the default
        :return: None
        """
        from Araneus.build_db import BuildDB
        bdb = BuildDB()
        if msg == 'new':
            bdb.diag_empty_db.show()
        else:
            bdb.setWindowTitle('Location is not accessible!')
            bdb.diag_out_of_date_db.show()
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
        Running 'Build' task in a new thread
        :return: None
        """
        self.worker.moveToThread(self.thread)
        self.worker.progress.connect(self.update_status_bar)
        self.worker.started.connect(self.before_build)
        self.worker.finished.connect(self.after_building)
        self.worker.stop.connect(self.thread.quit)
        self.thread.started.connect(self.worker.build)
        self.thread.start()

    def before_build(self):
        """
        Things to do before building a new database
        :return: None
        """
        self.total_dirs = db.get_total_directories()
        self.actionBuild_All.setDisabled(True)
        # SVG animation bar
        self.svgWidget = QSvgWidget(load_animation('bar'))
        self.svgWidget.setGeometry(0, 0, 1080, 3)
        self.svgWidget.setStyleSheet("background-color:White;")
        self.loading.addWidget(self.svgWidget)
        self.svgWidget.show()

    def after_building(self):
        """
        Things to do after building is complete
        :return: None
        """
        self.search_bar.setDisabled(True)
        db.move_tmp_db()
        self.search_bar.setDisabled(False)
        self.statusBar().showMessage('Ready')
        self.search_bar.setEnabled(1)
        self.search_btn.setEnabled(1)
        self.svgWidget.hide()

    def update_status_bar(self, current):
        """
        Guess what !!
        :param current represents the current directory being scanned
        :return: None
        """
        self.statusBar().showMessage('Building.. {} / {}'.format(current, self.total_dirs))

    @staticmethod
    def about_dialog():
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
    # TODO: show maximized
    # main_window.showMaximized()
    main_window.check_empty_db()
    sys.exit(main_w.exec_())


if __name__ == "__main__":
    main()
