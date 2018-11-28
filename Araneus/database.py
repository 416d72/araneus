# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE
import time
from magic import from_file
from Araneus.connection import *


class Database(Connection):
    config = Configurations()
    min_size = 0
    if config.get_option('DATABASE', 'min_size_true', 'bool'):
        min_size = config.get_option('DATABASE', 'min_size', 'int')
    mechanism = config.get_option('ADVANCED', 'indexing_mechanism').lower()

    target = os.path.abspath(
        os.path.expanduser('~') + '/Dev/Python/Automation/')  # Currently only user's home folder will be indexed

    def build(self):
        """
        Build a new database
        :return: bool
        """
        try:
            if 'python' in self.mechanism:
                self._walk()
            elif 'find' in self.mechanism:
                # TODO: implement indexing using GNU find
                pass
            elif 'locate' in self.mechanism:
                # TODO: implement indexing using GNU locate
                pass
            elif 'fd' in self.mechanism:
                # TODO: implement indexing using the awesome fd package
                pass
            return True
        except:
            raise Exception

    def _walk(self):
        con = sqlite3.connect(self.std_db)
        cursor = con.cursor()
        cursor.execute('PRAGMA synchronous = OFF')
        cursor.execute('PRAGMA journal_mode = MEMORY')
        cursor.execute('BEGIN TRANSACTION')
        cursor.execute("CREATE TABLE IF NOT EXISTS data "
                       "("
                       "`id` INTEGER PRIMARY KEY AUTOINCREMENT, "
                       "`name` TEXT,"
                       "`size` TEXT,"
                       "`location` TEXT,"
                       "`modified` TEXT,"
                       "`accessed` TEXT,"
                       "`type` TEXT"
                       "); ")
        for f in os.walk(self.target):
            cursor.execute(
                "INSERT INTO `data` (`name`,`size`,`location`,`modified`,`accessed`,`type`) VALUES (?,?,?,?,?,?);",
                (
                    f[0].split('/')[-1],
                    '',
                    f[0] + '/',
                    os.stat(f[0] + '/').st_mtime,
                    os.stat(f[0] + '/').st_atime,
                    'Directory',
                )
            )
            for file in f[2]:
                cursor.execute(
                    "INSERT INTO `data` (`name`,`size`,`location`,`modified`,`accessed`,`type`) VALUES (?,?,?,?,?,?);",
                    (
                        file,
                        os.stat(f[0] + '/' + file).st_size,
                        f[0] + '/',
                        os.stat(f[0] + '/' + file).st_mtime,
                        os.stat(f[0] + '/' + file).st_atime,
                        from_file(f[0] + '/' + file,
                                  mime=True)
                    )
                )
        cursor.execute('END TRANSACTION')
        con.commit()
        con.close()
    
    @staticmethod
    def _convert(self, size: int):
        power = 2 ** 10
        n = 0
        d = {0: 'Bytes', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
        while size >= power:
            size /= power
            n += 1
        return "%.2f " % round(size, 2) + d[n], int(size)
