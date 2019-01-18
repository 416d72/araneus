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

    def _build(self, password_tool):
        try:
            updated_conf_file = self._hidden_files()
            scanned_dirs = os.path.expanduser('~')
            os.system(f'{password_tool} '  # GUI password prompt..
                      f'"cp {self.updatedb_conf} {self.updatedb_conf_bak} && '  # Backup old conf file
                      f'cp {updated_conf_file} {self.updatedb_conf} && '  # Copy the new generated file
                      f'updatedb -l 0 {scanned_dirs} -o {self.mlocate_db} && '  # Update database
                      f'strings {self.mlocate_db} > {self.mlocate_txt}"')  # Extract database to text file
        except FileNotFoundError as e:
            return e
        except PermissionError as e:
            return e
        except OSError as e:
            return e

    def _fill(self):
        try:
            with open(self.mlocate_txt, 'r') as file:
                elements = file.read().split()
        except IOError as e:
            return e
        try:
            con = sqlite3.connect(self.tmp_db)
            cursor = con.cursor()
            cursor.execute("PRAGMA synchronous = OFF")
            cursor.execute("BEGIN TRANSACTION")
            last = 0
            path = ''
            for item in elements:
                if os.path.isdir(item):  # It's a directory
                    path = item
                    properties = os.stat(item)
                    cursor.execute(
                        "INSERT INTO `directories` (`name`,`location`,`size`,`modified`,`accessed`) "
                        "VALUES (?,?,?,?,?)",
                        [item.split('/')[-1],
                         item,
                         convert_size(properties.st_size),
                         convert_time(properties.st_mtime),
                         convert_time(properties.st_atime)])
                    last = cursor.lastrowid
                else:
                    if last is not 0:
                        location = f"{path}/{item}"
                        if os.path.isfile(location):
                            try:
                                properties = os.stat(location)
                                file_type = from_file(location, mime=True)
                            except IsADirectoryError:
                                cursor.execute("INSERT INTO `directories` "
                                               "(`name`,`location`,`size`,`modified`,`accessed`) "
                                               "VALUES (?,?,?,?,?)",
                                               [item, location,
                                                convert_size(properties.st_size),
                                                convert_time(properties.st_mtime),
                                                convert_time(properties.st_atime)]
                                               )
                                last = cursor.lastrowid
                                continue
                            except PermissionError:
                                continue
                            finally:
                                cursor.execute("INSERT INTO `files` (`parent`,`name`,`location`,`size`,`modified`,"
                                               "`accessed`,`type`) VALUES (?,?,?,?,?,?,?)",
                                               [last, item, location,
                                                convert_size(properties.st_size),
                                                convert_time(properties.st_mtime),
                                                convert_time(properties.st_atime),
                                                file_type])
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
    print(d.automate())
    print(f"Processed finished in {time() - start:.3f} seconds")
