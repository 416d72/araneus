# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE
from Araneus.configurations import *


class History:
    history_file_location = config_dir + 'history.txt'
    c = Configurations()
    max_items = c.get_option("HISTORY", 'Max_items', 'int')

    def __init__(self):
        self.create()

    def create(self):
        """
        Create a new empty history file
        :return: bool
        """
        try:
            open(self.history_file_location).close()
            return True
        except IOError:
            return IOError("Failed to open the history file")

    def clear(self):
        """
        Clear history file data
        :return: bool
        """
        try:
            with open(self.history_file_location, 'w') as f:
                f.write('')
            return True
        except IOError:
            return IOError("Failed to open the history file")

    def add(self, term):
        """
        Prepend a search term to history file
        :param term: string
        :return: bool
        """
        try:
            with open(self.history_file_location, 'r') as f:
                original = f.read()
            with open(self.history_file_location, 'w') as f:
                f.write('{}\n{}'.format(term, original))
            return True
        except IOError:
            return IOError("Failed to open the history file")

    def get(self):
        """
        Fetch history keywords
        :return: list
        """
        try:
            with open(self.history_file_location, 'r') as f:
                all = 0
                original = []
                for i, d in enumerate(f):
                    all += i
                    original.append(d)
            if all > self.max_items:
                with open(self.history_file_location, 'w') as f:
                    for item in original[:self.max_items]:
                        f.write(item)
            return original[:self.max_items]
        except IOError:
            return IOError("Failed to open the history file")
