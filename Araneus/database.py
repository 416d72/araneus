# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE
import subprocess
from magic import from_file
from Araneus.connection import *


class Database(Connection):
    config = Configurations()
    min_size = 0
    if config.get_option('DATABASE', 'min_size_true', 'bool'):
        min_size = config.get_option('DATABASE', 'min_size', 'int') * 1024
    mechanism = config.get_option('ADVANCED', 'indexing_mechanism').lower()
    target = os.path.abspath(
        os.path.expanduser('~') + '/Dev/')  # Currently only user's home folder will be indexed
    counter = 0

    def __init__(self):
        """
        Calling a system command to get the total number of directories in target and build an algorithm to
        update the progress bar in real time
        """
        super().__init__()
        command = 'cd %s ; ls -1R | grep ^d | wc' % self.target
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        self.total_dirs = int(process.communicate()[0].decode("utf-8").split()[0])

    def build(self):
        """
        Build a new database
        :return: bool
        """
        try:
            super().create_tmp()
            if 'python' in self.mechanism:
                return self._walk()
            elif 'find' in self.mechanism:
                # TODO: implement indexing using GNU find
                pass
            elif 'locate' in self.mechanism:
                # TODO: implement indexing using GNU locate
                pass
            elif 'fd' in self.mechanism:
                # TODO: implement indexing using the awesome fd package
                pass
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
        for directory in os.walk(self.target):
            cursor.execute(
                "INSERT INTO `data` (`name`,`size`,`location`,`modified`,`accessed`,`type`) VALUES (?,?,?,?,?,?);",
                (
                    directory[0].split('/')[-1],
                    0,
                    directory[0] + '/',
                    os.stat(directory[0] + '/').st_mtime,
                    os.stat(directory[0] + '/').st_atime,
                    'Directory',
                )
            )
            for file in directory[2]:
                size = os.stat(directory[0] + '/' + file).st_size
                if size < self.min_size:
                    continue
                cursor.execute(
                    "INSERT INTO `data` (`name`,`size`,`location`,`modified`,`accessed`,`type`) VALUES (?,?,?,?,?,?);",
                    (
                        file,
                        size,
                        directory[0] + '/',
                        os.stat(directory[0] + '/' + file).st_mtime,
                        os.stat(directory[0] + '/' + file).st_atime,
                        from_file(directory[0] + '/' + file,
                                  mime=True)
                    )
                )
            # self.counter += 1
            # percent = 100 * self.counter / self.total_dirs
            # yield percent
        cursor.execute('END TRANSACTION')
        con.commit()
        con.close()
        self.move_tmp_db()

    def move_tmp_db(self):
        try:
            copy2(self.tmp_db, self.std_db)
            os.remove(self.tmp_db)
            return True
        except Exception:
            return Exception
