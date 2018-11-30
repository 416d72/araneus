# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE
import configparser
from shutil import copy2
from Araneus.helpers import *

config = configparser.ConfigParser()


class Configurations:
    """
    Contains all methods for manipulate settings
    """
    conf_file_path = ''
    std_conf_file_path = ''

    def __init__(self):
        """
        - Checking os platform first
        - Setting file paths
        """
        self.declare()
        self.create_config_file()

    def declare(self):
        try:
            self.conf_file_path = config_dir + "conf.ini"
            self.std_conf_file_path = os.path.dirname(os.getcwd()) + "/Araneus/configurations/default-conf.ini"
            return True
        except ValueError:
            print(ValueError)

    @staticmethod
    def create_config_dir():
        """
        Creates Application's directory
        :return: Bool
        """
        if not os.path.exists(config_dir):
            try:
                os.mkdir(config_dir)
                return True
            except ValueError:
                return ValueError
        return True

    def create_config_file(self):
        """
        Creates configurations file
        :return: Bool
        """
        if os.path.isfile(self.conf_file_path):
            return True
        try:
            self.create_config_dir()
            copy2(self.std_conf_file_path, self.conf_file_path)
            return True
        except ValueError:
            return ValueError

    def reset(self):
        """
        Resets preferences by copying the original configurations file over the old one
        :return: None
        """
        try:
            self.create_config_file()
            copy2(self.std_conf_file_path, self.conf_file_path)
            return True
        except ValueError:
            return ValueError

    def validate(self):
        """
        Validate the config file
        :return: bool
        """
        try:
            config.read(self.std_conf_file_path)
            nconfig = configparser.ConfigParser()
            nconfig.read(self.conf_file_path)
            for section in config.sections():
                for (key, val) in config.items(section):
                    if not nconfig.has_option(section, key):
                        self.reset()
            return True
        except Exception:
            return False

    def get_option(self, section: str, option: str, method: str = 'str'):
        """
        Read configurations file
        :type section: str
        :param option: str
        :param method: str
        :return: mixed
        """
        try:
            self.validate()
            config.read(self.conf_file_path)
            if method == 'int':
                return config.getint(section, option)
            elif method == 'bool':
                return config.getboolean(section, option)
            else:
                return str(config.get(section, option))
        except ValueError:
            return ValueError("Error occurred while getting the required option value")

    def set_option(self, section: str, option: str, value: str):
        """
        Update a current value
        :param section: str
        :param option: str
        :param value: str
        :return: str
        """
        try:
            self.validate()
            config.read(self.conf_file_path)
            config[section][option] = str(value)
            with open(self.conf_file_path, 'w') as f:
                config.write(f)
            return self.get_option(section, option)
        except ValueError:
            return ValueError("Error occurred while changing preferences")
