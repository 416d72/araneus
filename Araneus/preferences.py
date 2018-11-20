import json
import os
import sys
from shutil import copy2
from pathlib import Path

conf_dir = str(Path.home()) + "/.config/Araneus/"
conf_file = conf_dir + "conf.json"
std_conf_file = str(os.getcwd() + os.sep + 'configurations' + os.sep + 'default-conf.json')


def check_os():
    """
    Checks if the current operating system is only Linux so that the app don't fail with other filesystems
    :return: Bool
    """
    if sys.platform.startswith('linux'):
        return True


def create_dir():
    """
    Creates Application's directory
    :return: Bool
    """
    if not os.path.exists(conf_dir):
        try:
            os.mkdir(conf_dir)
            return True
        except ValueError:
            return ValueError


def create_file():
    """
    Creates configurations file
    :return: Bool
    """
    if not os.path.isfile(conf_file):
        try:
            copy2(std_conf_file, conf_file)
            return True
        except ValueError:
            return ValueError


def parse():
    """
    Read configurations file
    :return: String|JSON
    """
    try:
        create_dir()
        create_file()
        return json.load(conf_file)
    except ValueError:
        return ValueError


def __main__():
    pass
