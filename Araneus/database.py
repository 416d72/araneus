#!usr/bin/python3
# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE

from Araneus.helpers import *
from Araneus.configurations import *
from Araneus.connection import *

config = Configurations()
min_size = 0
if config.get_option('DATABASE', 'min_size_true', 'bool'):
    min_size = config.get_option('DATABASE', 'min_size', 'int')


class Database(Connection()):
    def __init__(self):
        """
        Manipulate database
        """
        pass

    def build(self):
        """
        Build a new database
        :return: bool
        """
        pass
