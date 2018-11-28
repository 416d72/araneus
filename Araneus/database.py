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

    target = os.path.expanduser('~') + '/Dev/Python/1-Basics'  # Currently only user's home folder will be indexed

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
        for f in os.walk(self.target):
            result = []
            path = f[0] + '/'
            # result.append([
            #     f[0].split('/')[-1],
            #     # subprocess.getoutput('du -sh %s' % path).split()[0], # Isn't really necessary and consumes more
            #     # processing power
            #     '',
            #     path,
            #     time.ctime(os.stat(path).st_mtime),
            #     time.ctime(os.stat(path).st_atime),
            #     'Directory'
            # ])
            super().insert(
                f[0].split('/')[-1],
                '',
                path,
                time.ctime(os.stat(path).st_mtime),
                time.ctime(os.stat(path).st_atime),
                'Directory')
            for file in f[2]:
                # result.append([
                #     file,
                #     self._convert(os.stat(path + file).st_size)[0],
                #     path,
                #     time.ctime(os.stat(path + file).st_mtime),
                #     time.ctime(os.stat(path + file).st_atime),
                #     from_file(path + file, mime=True)
                # ])
                super().insert(
                    file,
                    self._convert(os.stat(path + file).st_size)[0],
                    path,
                    time.ctime(os.stat(path + file).st_mtime),
                    time.ctime(os.stat(path + file).st_atime),
                    from_file(path + file,
                              mime=True))

    def to_sql(self, file: dict):
        """
        Converts dictionary values to string SQL commands
        Here I've reached a point where I must choose security or performance !
So I'm sticking with security till I figure a way to have both ..
        :param file: Dictionary contains both column names in database with their values
        :return: bool
        """
        pass

    def _convert(self, size: int):
        power = 2 ** 10
        n = 0
        d = {0: 'Bytes', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
        while size >= power:
            size /= power
            n += 1
        return "%.2f " % round(size, 2) + d[n], int(size)


s = time.time()
test = Database()
test.build()
print("%.3f seconds" % round(time.time() - s, 3))
