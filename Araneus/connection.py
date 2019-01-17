# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE

import sqlite3

from Araneus.configurations import *


class Connection:
    """
    Manages connection to the sqlite3 database
    """
    # updatedb.conf
    updatedb_conf = os.path.abspath('/etc/updatedb.conf')
    updatedb_conf_bak = updatedb_conf + '.BAK'
    # mlocate.db
    mlocate_db = config_dir + 'mlocate.db'
    mlocate_txt = config_dir + 'mlocate.txt'
    # database
    std_db = config_dir + 'araneus.db'
    tmp_db = config_dir + 'temp_database'

    def __init__(self):
        self.create_tmp()

    def create_tmp(self):
        """
        Creates the temporary sqlite3 file
        :return: bool
        """
        try:
            con = sqlite3.connect(self.tmp_db)
            cursor = con.cursor()
            cursor.execute("CREATE TABLE IF NOT EXISTS `directories` "
                           "("
                           "`id` INTEGER PRIMARY KEY AUTOINCREMENT,"
                           "`name` TEXT,"
                           "`location` TEXT,"
                           "`size` TEXT,"
                           "`modified` TEXT,"
                           "`accessed` TEXT"
                           "); ")
            con.commit()
            cursor.execute("CREATE TABLE IF NOT EXISTS `files` "
                           "("
                           "`id` INTEGER PRIMARY KEY AUTOINCREMENT,"
                           "`parent` INTEGER,"
                           "`name` TEXT,"
                           "`location` TEXT,"
                           "`size` TEXT,"
                           "`modified` TEXT,"
                           "`accessed` TEXT,"
                           "`type` TEXT,"
                           "FOREIGN KEY(`parent`) REFERENCES `directories`(`id`)"
                           "); ")
            con.commit()
            con.close()
            return True
        except sqlite3.Error as e:
            return e

    def get(self, search_term):
        """
        Get all records that match search key word
        :param search_term: str
        :return: list
        """
        try:
            con = sqlite3.connect(self.std_db)
            cursor = con.cursor()
            command = "SELECT * FROM `directories` WHERE `location` LIKE ?"
            cursor.execute(command, ("%" + search_term + "%",))
            return cursor.fetchall()
        except sqlite3.Error as e:
            return e

    def fetch_all(self):
        try:
            con = sqlite3.connect(self.std_db)
            cursor = con.cursor()
            command = "SELECT * FROM `data`"
            cursor.execute(command)
            return cursor.fetchall()
        except sqlite3.Error as e:
            return e
