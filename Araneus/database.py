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
        pass

    def build(self):
        """
        Build a new database
        :return: mix
        """
        try:
            self.mlocate()
            super().create_tmp()
            self.move_tmp_db()
        except:
            raise Exception

    def mlocate(self):
        try:
            subprocess.call(['gksu', 'updatedb'])
            subprocess.call(['gksu', f'strings {self.mlocate_db}'])
        except OSError:
            print(OSError.strerror)

    def move_tmp_db(self):
        try:
            copy2(self.tmp_db, self.std_db)
            os.remove(self.tmp_db)
            return True
        except Exception:
            return Exception
