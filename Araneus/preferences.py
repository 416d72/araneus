import configparser
import os
import sys
from shutil import copy2

config = configparser.ConfigParser()


def check_os():
    """
    Checks if the current operating system is only Linux so that the app won't fail with others
    :return: Bool
    """
    if sys.platform.startswith('linux'):
        return True


class Preferences:
    """
    Contains all methods for manipulate settings
    """

    def __init__(self):
        """
        - Checking os platform first
        - Setting file paths
        """
        self.conf_dir = str(os.path.expanduser("~")) + "/.config/Araneus/"
        self.conf_file_path = self.conf_dir + "conf.ini"
        self.std_conf_file_path = str(os.path.dirname(os.getcwd()) + "/Araneus/" + '/configurations/' +
                                      'default-conf.ini')
        self.create_config_file()

    def create_config_dir(self):
        """
        Creates Application's directory
        :return: Bool
        """
        if not os.path.exists(self.conf_dir):
            try:
                os.mkdir(self.conf_dir)
                return True
            except ValueError:
                return ValueError
        else:
            return True

    def create_config_file(self):
        """
        Creates configurations file
        :return: Bool
        """
        if not os.path.isfile(self.conf_file_path):
            try:
                self.create_config_dir()
                copy2(self.std_conf_file_path, self.conf_file_path)
                return True
            except ValueError:
                return ValueError
        else:
            return True

    def reset(self):
        """
        Resets preferences by copying the original configurations file over the old one
        :return: None
        """
        try:
            self.create_config_file()
            copy2(self.std_conf_file_path, self.conf_file_path)
        except ValueError:
            return "Couldn't reset settings!"

    def validate(self, section, option):
        config.read(self.conf_file_path)
        if not config.has_option(section, option):
            self.reset()

    def get_option(self, section, option):
        """
        Read configurations file
        :return: String
        """
        try:
            self.validate(section, option)
            return config[section][option]
        except ValueError:
            return ValueError("Error occurred while getting the required option value")

    def set_option(self, section, option, value):
        try:
            self.validate(section, option)
            config[section][option] = value
            with open(self.conf_file_path, 'w') as f:
                config.write(f)
        except ValueError:
            raise ValueError("Error occurred while changing preferences")
