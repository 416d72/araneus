import glob
import os
import datetime


class Database:

    def convert_bytes(num):
        """
        this function will convert bytes to MB.... GB... etc
        """
        for x in ['bytes', 'KB', 'MB', 'GB']:
            if num < 1024.0:
                return "%3.2f %s" % (num, x)
            num /= 1024.0

    def build_file_db():
        file_type = ""
        for file in glob.glob("/home/amr/Documents/kingstone/D**", recursive = True):
            if os.path.islink(file) is True:
                continue
            name = os.path.splitext(os.path.basename(file))
            file_name = name[0]
            extension = name[1][1:]
            path = os.path.abspath(file)
            size = convert_bytes(os.stat(file).st_size)
            date = datetime.datetime.fromtimestamp(os.stat(file).st_mtime).__str__()[:19]
            if os.path.isdir(file) is True:
                file_type = "Directory"
            elif os.path.isfile(file) is True:
                file_type = extension + " file"
