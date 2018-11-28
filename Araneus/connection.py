#!usr/bin/python3
# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE

import sqlite3
from Araneus.configurations import *

if Configurations().get_option('DATABASE', 'min_size_true', 'bool'):
    min_size = Configurations().get_option('DATABASE', 'min_size', 'int')


class Connection:
    """
    Manages connection to the sqlite3 database
    """
    std_db = config_dir + 'database'
    table = 'data'

    def __init__(self):
        self.create()

    def create(self):
        """
        Creates the sqlite3 file
        :return: bool
        """
        try:
            """
            Create a new database with default table and columns
            """
            con = sqlite3.connect(self.std_db)
            cursor = con.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS {} "
                           "("
                           "`id` INTEGER PRIMARY KEY AUTOINCREMENT, "
                           "`name` TEXT,"
                           "`size` TEXT,"
                           "`location` TEXT,"
                           "`modified` TEXT,"
                           "`accessed` TEXT,"
                           "`type` TEXT"
                           "); ".format(self.table))
            con.commit()
            con.close()
            return True
        except Exception:
            raise Exception

    def insert(self, name, size, location, modified, accessed, file_type):
        """
        Insert a new record in database
        :param name: str
        :param size: str
        :param location: str
        :param modified: str
        :param accessed: str
        :param file_type: str
        :return: bool
        """
        try:
            command = "INSERT INTO `{}` (`name`,`size`,`location`,`modified`,`accessed`,`type`) VALUES (?,?,?,?,?," \
                      "?);".format(self.table)
            con = sqlite3.connect(self.std_db)
            cursor = con.cursor()
            cursor.execute(command, (name, size, location, modified, accessed, file_type))
            con.commit()
            con.close()
            return True
        except:
            raise Exception

    def get(self, search_term):
        """
        Get all records that match search key word
        :param search_term: str
        :return: list
        """
        try:
            con = sqlite3.connect(self.std_db)
            cursor = con.cursor()
            command = "SELECT * FROM `{}` WHERE `name` LIKE ?".format(self.table)
            cursor.execute(command, ("%" + search_term + "%",))
            return cursor.fetchall()
        except:
            raise Exception

    def fetch_all(self):
        try:
            con = sqlite3.connect(self.std_db)
            cursor = con.cursor()
            command = "SELECT * FROM `{}`".format(self.table)
            cursor.execute(command)
            return cursor.fetchall()
        except:
            raise Exception

    def drop(self):
        try:
            con = sqlite3.connect(self.std_db)
            cursor = con.cursor()
            cursor.execute("DROP TABLE `{}`".format(self.table))
            con.commit()
            con.close()
            return True
        except:
            raise Exception
