#!usr/bin/python3
# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE

from Araneus.helpers import *
from Araneus.configurations import *
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

conf = Configurations()


class Preferences(QDialog):
    """
    This class controls preferences dialog and interacts with configurations model to read/modify
    application configurations
    TODO: Implement interface with configurations.py
    """

    def __init__(self):
        super(Preferences, self).__init__()
        loadUi(load_ui('preferences'), self)
        self.retrieve()
        self.state_change()
        self.show()

    def retrieve(self):
        """
        Show current settings
        :return: bool
        """
        # General tab
        self.general_language.setCurrentIndex(conf.get_option('GENERAL', 'Language', 'int'))
        self.general_autostart.setChecked(conf.get_option('GENERAL', 'Auto_start', 'bool'))
        self.general_start_minimized.setChecked(conf.get_option('GENERAL', 'Start_min', 'bool'))
        # History tab
        self.history_remember.setChecked(conf.get_option('HISTORY', 'Remember', 'bool'))
        self.history_max_number.setValue(conf.get_option('HISTORY', 'Max_items', 'int'))
        # Search tab
        self.search_hidden_files.setChecked(conf.get_option('SEARCH', 'Show_hidden_files', 'bool'))
        # Database tab
        self.db_auto_build.setChecked(conf.get_option('DATABASE', 'Auto_build', 'bool'))
        self.db_background_build.setChecked(conf.get_option('DATABASE', 'Background_build', 'bool'))
        self.db_min_file_size_label.setChecked(conf.get_option('DATABASE', 'Min_size_true', 'bool'))
        self.db_min_file_size.setValue(conf.get_option('DATABASE', 'Min_size', 'int'))

    def state_change(self):
        self.history_remember.stateChanged.connect(lambda: self.history_max_number.setEnabled(
            self.history_remember.isChecked()))
        self.db_min_file_size_label.stateChanged.connect(lambda: self.db_min_file_size.setEnabled(
            self.db_min_file_size_label.isChecked()))

    def save(self):
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
