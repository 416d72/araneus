#!usr/bin/python3
# -*- coding: utf-8; -*-
import os
import sys

from Araneus.preferences import *
from Araneus.helpers import *

from PyQt5.QtWidgets import QMainWindow

print(load_ui('about'))

one_instance()

print(load_ui('about'))


class Main(QMainWindow):
    def __init__(self):
        pass


os.remove(lock_file)
