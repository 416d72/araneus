import unittest

from Araneus.configurations import *

conf = Configurations()


class TestPreferences(unittest.TestCase):

    def test_declare(self):
        self.assertTrue(conf.declare())

    def test_create_config_dir(self):
        self.assertTrue(conf.create_config_dir())

    def test_create_config_file(self):
        self.assertTrue(conf.create_config_file())

    def test_reset(self):
        self.assertTrue(conf.reset())

    def test_validate(self):
        self.assertTrue(conf.validate())

    def test_get_option(self):
        self.assertIsInstance(conf.get_option('GENERAL', 'Language'), str)

    def test_set_option(self):
        self.assertIsInstance(conf.set_option('GENERAL', 'Language', 'en'), str)


if __name__ == '__main__':
    unittest.main()
