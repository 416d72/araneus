import os, json
from pathlib import Path

conf_dir = str(Path.home()) + "/.config/Araneus/"
conf_file = conf_dir + "conf.json"


class Create:
    pass


class Read:
    def __init__(self):
        if not self.check_file_exists():
            Create()
        else:
            self.parse()

    def check_file_exists(self):
        if os.path.isfile(conf_file):
            return True

    def parse(self):
        return json.load(conf_file)


class Modify:
    def __init__(self):
        pass
