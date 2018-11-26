#!usr/bin/python3
# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE

from Araneus.helpers import *
from Araneus.configurations import *
from Araneus.history import *
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi

conf = Configurations()
history = History()


class Preferences(QDialog):
    """
    This class controls preferences dialog and interacts with configurations model to read/modify
    application configurations
    """

    def __init__(self):
        super(Preferences, self).__init__()
        loadUi(load_ui('preferences'), self)
        self.retrieve()
        self.state_change()
        self.history_delete_btn.clicked.connect(lambda: self.clear_history())
        self.buttonBox.accepted.connect(lambda: self.save())
        self.show()

    def retrieve(self):
        """
        Sets the current settings
        :return: bool
        """
        # General tab
        self.general_language.setCurrentIndex(conf.get_option('GENERAL', 'Language', 'int'))
        self.general_autostart.setChecked(conf.get_option('GENERAL', 'Auto_start', 'bool'))
        self.general_start_minimized.setChecked(conf.get_option('GENERAL', 'Start_min', 'bool'))
        # History tab
        self.history_remember.setChecked(conf.get_option('HISTORY', 'Remember', 'bool'))
        self.history_max_number.setEnabled(self.history_remember.isChecked())
        self.history_max_number.setValue(conf.get_option('HISTORY', 'Max_items', 'int'))
        # Search tab
        self.search_hidden_files.setChecked(conf.get_option('SEARCH', 'Show_hidden_files', 'bool'))
        # Database tab
        self.db_auto_build.setChecked(conf.get_option('DATABASE', 'Auto_build', 'bool'))
        self.db_min_file_size_label.setChecked(conf.get_option('DATABASE', 'Min_size_true', 'bool'))
        self.db_min_file_size.setEnabled(self.db_min_file_size_label.isChecked())
        self.db_min_file_size.setValue(conf.get_option('DATABASE', 'Min_size', 'int'))

    def state_change(self):
        """
        Listen to events that happens when changing certain checkboxes that's affects other settings
        :return: None
        """
        self.history_remember.stateChanged.connect(lambda: self.history_max_number.setEnabled(
            self.history_remember.isChecked()))
        self.db_min_file_size_label.stateChanged.connect(lambda: self.db_min_file_size.setEnabled(
            self.db_min_file_size_label.isChecked()))

    def clear_history(self):
        """
        Clears the history file
        :return: None
        """
        history.clear()
        self.history_delete_label.setText('History is deleted!')

    def save(self):
        """
        Save any modified settings to configuration file
        TODO: link this method with the action that triggered when clicking `ok` button
        :return: None
        """
        # General tab
        conf.set_option('GENERAL', 'Language', self.general_language.currentIndex())
        conf.set_option('GENERAL', 'Auto_start', self.general_autostart.isChecked())
        conf.set_option('GENERAL', 'Start_min', self.general_start_minimized.isChecked())
        # History tab
        conf.set_option('HISTORY', 'Remember', self.history_remember.isChecked())
        conf.set_option('HISTORY', 'Max_items', self.history_max_number.value())
        # Search tab
        conf.set_option('SEARCH', 'Show_hidden_files', self.search_hidden_files.isChecked())
        # Database tab
        conf.set_option('DATABASE', 'Auto_build', self.db_auto_build.isChecked())
        conf.set_option('DATABASE', 'Min_size_true', self.db_min_file_size_label.isChecked())
        conf.set_option('DATABASE', 'Min_size', self.db_min_file_size.value())


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
