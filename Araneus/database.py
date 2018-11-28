#!usr/bin/python3
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
    mechanism = config.get_option('ADVANCED', 'Indexing_mechanism')

    target = os.path.expanduser('~') + '/Dev/Python/'  # Currently only user's home folder will be indexed

    script = ''

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
        command = "INSERT INTO `{}` (`name`,`size`,`location`,`modified`,`accessed`,`type`) VALUES (?,?,?,?,?," \
                  "?);".format(self.table)
        con = sqlite3.connect(self.std_db)
        cursor = con.cursor()
        cursor.execute('PRAGMA synchronous = OFF')
        cursor.execute('BEGIN TRANSACTION')
        for f in os.walk(self.target):
            path = f[0] + '/'
            cursor.execute(command, (
                f[0].split('/')[-1],
                '',
                path,
                time.ctime(os.stat(path).st_mtime),
                time.ctime(os.stat(path).st_atime),
                'Directory'), )
            for file in f[2]:
                cursor.execute(command, (
                    file,
                    self._convert(os.stat(path + file).st_size)[0],
                    path,
                    time.ctime(os.stat(path + file).st_mtime),
                    time.ctime(os.stat(path + file).st_atime),
                    from_file(path + file,
                              mime=True)))
        con.commit()
        con.close()

    def _convert(self, size: int):
        power = 2 ** 10
        n = 0
        d = {0: 'Bytes', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
        while size >= power:
            size /= power
            n += 1
        return "%.2f " % round(size, 2) + d[n], int(size)


#
s = time.time()
test = Database()
# test.drop()
# test.build()
# print(test.fetch_all())
print("%.3f seconds" % round(time.time() - s, 3))
