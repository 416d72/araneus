import unittest

from Araneus.configurations import *

configurations = Configurations()


class TestPreferences(unittest.TestCase):
    def test_declare(self):
        configurations.declare()

    def test_create_config_dir(self):
        configurations.create_config_dir()

    def test_create_config_file(self):
        configurations.create_config_file()

    def test_reset(self):
        self.assertEqual(configurations.reset(), True)


if __name__ == '__main__':
    unittest.main()
