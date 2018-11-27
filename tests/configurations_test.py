import unittest

from Araneus.configurations import *


class TestPreferences(unittest.TestCase):

    def test_declare(self):
        self.assertTrue(Configurations().declare())

    def test_create_config_dir(self):
        self.assertTrue(Configurations().create_config_dir())

    def test_create_config_file(self):
        self.assertTrue(Configurations().create_config_file())

    def test_reset(self):
        self.assertTrue(Configurations().reset())

    def test_validate(self):
        self.assertTrue(Configurations().validate())

    def test_get_option(self):
        self.assertIsInstance(Configurations().get_option('GENERAL', 'Language'), str)

    def test_set_option(self):
        self.assertIsInstance(Configurations().set_option('GENERAL', 'Language', 0), str)


if __name__ == '__main__':
    unittest.main()
