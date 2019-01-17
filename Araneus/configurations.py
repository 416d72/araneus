# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE
import configparser
import re
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
            with open(config_dir + 'mlocate.txt', 'a'):
                pass
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
        except configparser.Error as e:
            return e

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
                return abs(config.getint(section, option))
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


class UpdatedbConfigurations:
    def __init__(self):
        self._conf_file = os.path.abspath('/etc/updatedb.conf')
        self._tmp_file = os.path.abspath('/tmp/Araneus_updatedb.conf')
        self._prefix = 'PRUNEPATHS'
        self._excludes = ''
        self._read()

    def _read(self):
        try:
            with open(self._conf_file, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith(self._prefix):
                        self._excludes = re.sub(f'({self._prefix})|=|\'|"', '', line).strip()
                    else:
                        raise IOError('Could not find Excludes section from \'updatedb.conf\' file')
        except FileNotFoundError as e:
            return e
        except PermissionError as e:
            return e
        except IOError as e:
            return e

    def toggle(self, include: bool):
        """
        Either include hidden files or exclude them
        :param include:
        :return:
        """
        spell = '.*/\..*'  # Like Harry Potter's spells
        if include:
            if spell in self._excludes:
                self._excludes = self._excludes.replace(spell, '')
        else:
            if spell not in self._excludes:
                self._excludes += f" {spell} "
        return self._create_temp()

    def _create_temp(self):
        try:
            copy2(self._conf_file, self._tmp_file)
            with open(self._tmp_file, 'r') as tmp_file:
                lines = tmp_file.readlines()
            for index, line in enumerate(lines):
                if line.startswith(self._prefix):
                    lines[index] = f"{self._prefix} = '{self._excludes}'"
                    break
            with open(self._tmp_file, 'w') as tmp_file:
                tmp_file.writelines(lines)
            return self._tmp_file
        except PermissionError as e:
            return e
        except FileNotFoundError as e:
            return e
