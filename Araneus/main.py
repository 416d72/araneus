#!usr/bin/python3
# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE

import webbrowser
from Araneus.helpers import *
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        loadUi(load_ui('main_window'), self)
        self.triggers()

        self.show()

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
        print("Preferences")

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
        import Araneus.about

    def donate_url(self):
        try:
            webbrowser.open('https://github.com/akkk33/araneus')
        except Exception:
            print("Something went wrong while opening the web browser:", Exception)


def main():
    app = QApplication(sys.argv)
    main_window = Main()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
