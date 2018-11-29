# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE
from magic import from_file
from Araneus.connection import *


class Database(Connection):
    config = Configurations()
    min_size = 0
    if config.get_option('DATABASE', 'min_size_true', 'bool'):
        min_size = config.get_option('DATABASE', 'min_size', 'int') * 1024
    mechanism = config.get_option('ADVANCED', 'indexing_mechanism').lower()
    target = os.path.abspath(
        os.path.expanduser('~') + '/Dev/Linux/compile/firefox/')  # Currently only user's home folder will be indexed

    def __init__(self):
        """
        TODO: call a system command to get the total number of directories and build an algorithm to calculate an estimated time to animate the progress bar.
        """
        super().__init__()
        pass

    def build(self):
        """
        Build a new database
        :return: bool
        TODO: Multi processes | threads
        TODO: Asynchronous
        """
        try:
            super().create_tmp()
            super().drop()
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
            self.move_tmp_db()
            return True
        except:
            raise Exception

    def _walk(self):
        con = sqlite3.connect(self.tmp_db)
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
                    0,
                    f[0] + '/',
                    os.stat(f[0] + '/').st_mtime,
                    os.stat(f[0] + '/').st_atime,
                    'Directory',
                )
            )
            for file in f[2]:
                size = os.stat(f[0] + '/' + file).st_size
                if size < self.min_size:
                    continue
                cursor.execute(
                    "INSERT INTO `data` (`name`,`size`,`location`,`modified`,`accessed`,`type`) VALUES (?,?,?,?,?,?);",
                    (
                        file,
                        size,
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

    def move_tmp_db(self):
        try:
            copy2(self.tmp_db, self.std_db)
            os.remove(self.tmp_db)
            return True
        except Exception:
            return Exception
