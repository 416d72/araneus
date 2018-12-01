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
            with open(self.history_file_location, 'a'):
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
            if term is not "" and term not in self.get():
                with open(self.history_file_location, 'r') as f:
                    original = f.read()
                with open(self.history_file_location, 'w') as f:
                    f.write('{}\n{}'.format(term, original))
            self.sanitise()
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
                return f.read().split()
        except IOError:
            return IOError("Failed to open the history file")

    def sanitise(self):
        """
        Check if history file has more lines than user's preference and if it's true, it simply deletes the last line
        which is the oldest entry
        :return: bool
        """
        try:
            with open(self.history_file_location, 'r') as history_file:
                count = history_file.read().split()
            if len(count) > self.max_items:
                with open(self.history_file_location, 'w') as new_history_file:
                    new_history_file.writelines([item + '\n' for item in count[:-1]])
        except IOError:
            return IOError('Failed to open the history file')
