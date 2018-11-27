#!usr/bin/python3
# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE
from Araneus.helpers import *


class History:
    history_file_location = str(os.path.expanduser('~')) + '/.config/Araneus/history.txt'

    def __init__(self):
        self.create()

    def create(self):
        """
        Create a new empty history file
        :return: bool
        """
        try:
            with open(self.history_file_location, 'w'):
                pass
            return True
        except Exception:
            return False

    def clear(self):
        """
        Clear history file data
        :return: bool
        """
        try:
            with open(self.history_file_location, 'w') as f:
                f.write('')
            return True
        except Exception:
            return False

    def add(self, term: str):
        """
        Prepend a search term to history file
        :param term: string
        :return: bool
        """
        try:
            with open(self.history_file_location, 'r') as f:
                original_data = f.read()
            with open(self.history_file_location, 'w') as f:
                f.write(term + '\n' + original_data)
            return True
        except Exception:
            return False

    def get(self, count: int = 10):

        """
        Fetch history at maximum count of 'count` argument
        :param count int
        :return: list || False
        """
        try:
            with open(self.history_file_location) as f:
                return [line.strip() for line in f][:count]
        except Exception:
            return False


# test = History()
# test.add('araneus')
# test.clear()
# print(test.get())
