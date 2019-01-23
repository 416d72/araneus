# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE
from subprocess import Popen, PIPE
from time import time

from magic import from_file

from Araneus.connection import *


class Database(Connection):
    config = Configurations()
    min_size = 0
    if config.get_option('DATABASE', 'min_size_true', 'bool'):
        min_size = config.get_option('DATABASE', 'min_size', 'int') * 1024
    hidden = config.get_option('SEARCH', 'show_hidden_files', 'bool')

    def __init__(self):
        super().__init__()
        self.target = os.path.expanduser('~')

    def get_total_directories(self):
        """
        Com'n the title is clear
        :return: int
        """
        with open(self.mlocate_txt, 'r') as file:
            elements = file.readlines()
        return len(elements)

    def _hidden_files(self):
        """
        Handles hidden files based on user preferences
        :return:
        """
        u = UpdatedbConfigurations()
        return u.toggle(include=self.hidden)

    def automate(self):
        """
        Build a new database
        :return: mix
        """
        try:
            self._which()
            self._fill()
            self.move_tmp_db()
            self._empty_txt()
        except OSError as e:
            return e

    def _which(self):
        """
        Choosing any available GUI password prompt toolkit
        :return:
        """
        tools = {'pkexec': 'pkexec bash -c', 'kdesu': 'kdesu -c', 'kdesudo': 'kdesudo -c'}
        for tool in tools:
            which = Popen(['which', tool], stdout=PIPE)
            found = which.communicate()[0]
            if found:
                self._build(tools.get(tool))
                break
            else:
                return OSError("Couldn't find suitable GUI tool to execute certain commands with root permissions!")

    def _build(self, sudo: str):
        try:
            updated_conf_file = self._hidden_files()
            cmd = Popen([f'{sudo} "'  # GUI password prompt..
                         f'cp {self.updatedb_conf} {self.updatedb_conf_bak} && '  # Backup old conf file
                         f'cp {updated_conf_file} {self.updatedb_conf} && '  # Copy the new generated file
                         f'updatedb -l 0 -U {self.target} -o {self.mlocate_db} && '  # Update database
                         f'strings {self.mlocate_db} > {self.mlocate_txt}'  # Extract database to text file
                         f'"'], stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
            if not cmd.communicate()[0]:
                return False  # Error msg
        except FileNotFoundError as e:
            return e
        except PermissionError as e:
            return e
        except OSError as e:
            return e

    def _getline(self):
        """
        Get the first line to insert data starting from.
        :return:
        """
        cmd = Popen([f'grep -n -m 2 {self.target} {self.mlocate_txt} | tail -n1 | cut -f1 -d:'], stdin=PIPE,
                    stdout=PIPE, shell=True)
        return int(cmd.communicate()[0].decode("utf8"))

    def _fill(self):
        try:
            with open(self.mlocate_txt, 'r') as file:
                elements = file.read().split('\n')[self._getline():]
            con = sqlite3.connect(self.tmp_db)
            cursor = con.cursor()
            cursor.execute("PRAGMA synchronous = OFF")
            cursor.execute("BEGIN TRANSACTION")
            path = ''
            last = 0
            for item in elements:
                try:
                    location = f"{path}/{item}"
                    if os.path.isdir(item):  # It's a directory
                        properties = os.stat(item)
                        cursor.execute(
                            "INSERT INTO `directories` (`name`,`location`,`size`,`modified`,`accessed`) "
                            "VALUES (?,?,?,datetime(?),datetime(?))",
                            [location[location.rfind('/'):],
                             location,
                             properties.st_size,
                             properties.st_mtime,
                             properties.st_atime])
                        path = item
                        last = cursor.lastrowid
                    elif os.path.isfile(location):
                        properties = os.stat(location)
                        file_type = from_file(location, mime=True)
                        cursor.execute("INSERT INTO `files` "
                                       "(`parent`,`name`,`location`,`size`,`modified`,`accessed`,`type`) "
                                       "VALUES (?,?,?,?,datetime(?),datetime(?),?)",
                                       [last, item, location,
                                        properties.st_size,
                                        properties.st_mtime,
                                        properties.st_atime,
                                        file_type])
                except PermissionError:
                    continue
            cursor.execute('END TRANSACTION')
            con.commit()
            con.close()
            return True
        except sqlite3.Error as e:
            return e

    def move_tmp_db(self):
        try:
            copy2(self.tmp_db, self.std_db)
            os.remove(self.tmp_db)
            return True
        except IOError as e:
            return e

    def _empty_txt(self):
        try:
            with open(self.mlocate_txt, 'w') as file:
                file.write('')
        except IOError as e:
            return e


if __name__ == '__main__':
    start = time()
    d = Database()
    # print(d.read_txt())
    print(d.automate())
    print(f"Processed finished in {time() - start:.3f} seconds")
