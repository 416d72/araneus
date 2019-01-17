# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE
from magic import from_file

from Araneus.connection import *


class Database(Connection):
    config = Configurations()
    min_size = 0
    if config.get_option('DATABASE', 'min_size_true', 'bool'):
        min_size = config.get_option('DATABASE', 'min_size', 'int') * 1024
    hidden = config.get_option('SEARCH', 'show_hidden_files', 'bool')
    mechanism = config.get_option('ADVANCED', 'indexing_mechanism').lower()
    target = os.path.abspath(
        os.path.expanduser('~') + '/Dev/')  # Currently only user's home folder will be indexed

    def __init__(self):
        """
        Calling a system command to get the total number of directories in target and build an algorithm to
        update the progress bar in real time
        """
        super().__init__()
        # Linux way
        # command = 'cd %s ; ls -1R | grep ^d | wc' % self.target
        # process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        # total_dirs = float(process.communicate()[0].decode("utf-8").split()[0])

    def get_total_directories(self):
        """
        Com'n the title is clear
        :return: int
        """
        with open(self.mlocate_txt, 'r') as file:
            elements = file.readlines()
        return len(elements)

    def build(self):
        """
        Build a new database
        :return: mix
        """
        try:
            os.system(f'pkexec bash -c "updatedb && strings {self.mlocate_db} > {self.mlocate_txt}"')
            # TODO: add qt support
            super().create_tmp()
            self.fill()
            self.move_tmp_db()
            self.empty_txt()
        except OSError as e:
            return e

    def fill(self):
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
            for index, item in enumerate(elements[:20500]):
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

    def empty_txt(self):
        try:
            with open(self.mlocate_txt, 'w') as file:
                file.write('')
        except IOError as e:
            return e


if __name__ == '__main__':
    start = time()
    d = Database()
    fill = d.fill()
    print(f"Processed finished in {time() - start:.3f} seconds")
