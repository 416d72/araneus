# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE

import sqlite3
from Araneus.configurations import *


class Connection:
    """
    Manages connection to the sqlite3 database
    """
    std_db = config_dir + 'database'
    tmp_db = config_dir + 'temporary_database'

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
            cursor.execute("CREATE TABLE IF NOT EXISTS `data` "
                           "("
                           "`id` INTEGER PRIMARY KEY AUTOINCREMENT, "
                           "`name` TEXT,"
                           "`size` TEXT,"
                           "`location` TEXT,"
                           "`modified` TEXT,"
                           "`accessed` TEXT,"
                           "`type` TEXT"
                           "); ")
            con.commit()
            con.close()
            return True
        except Exception:
            return Exception

    def create_tmp(self):
        """
        Creates the temporary sqlite3 file
        :return: bool
        """
        try:
            """
            Create a new temporary database with default table and columns
            """
            con = sqlite3.connect(self.tmp_db)
            cursor = con.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS `data` "
                           "("
                           "`name` TEXT,"
                           "`size` TEXT,"
                           "`location` TEXT,"
                           "`modified` TEXT,"
                           "`accessed` TEXT,"
                           "`type` TEXT"
                           "); ")
            con.commit()
            con.close()
            return True
        except Exception:
            return Exception

    def get(self, search_term):
        """
        Get all records that match search key word
        :param search_term: str
        :return: list
        """
        try:
            con = sqlite3.connect(self.std_db)
            cursor = con.cursor()
            command = "SELECT * FROM `data` WHERE `name` LIKE ?"
            cursor.execute(command, ("%" + search_term + "%",))
            return cursor.fetchall()
        except:
            return Exception

    def fetch_all(self):
        try:
            con = sqlite3.connect(self.std_db)
            cursor = con.cursor()
            command = "SELECT * FROM `data`"
            cursor.execute(command)
            return cursor.fetchall()
        except Exception:
            return Exception

    def drop(self):
        try:
            con = sqlite3.connect(self.std_db)
            cursor = con.cursor()
            cursor.execute("DROP TABLE `data`")
            con.commit()
            con.close()
            return True
        except Exception:
            return Exception
