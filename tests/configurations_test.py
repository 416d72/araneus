import unittest

from Araneus.configurations import *

configurations = Configurations()

print(os.path.dirname(__file__))


class TestPreferences(unittest.TestCase):
    def test_declare(self):
        self.assertTrue(configurations.declare())

    def test_create_config_dir(self):
        self.assertTrue(configurations.create_config_dir())

    def test_create_config_file(self):
        self.assertTrue(configurations.create_config_file())

    def test_reset(self):
        self.assertTrue(configurations.reset())

    def test_validate(self):
        self.assertTrue(configurations.validate('GENERAL', 'Language'))

    def test_get_option(self):
        self.assertIsInstance(configurations.get_option('GENERAL', 'Language'), str)

    def test_set_option(self):
        self.assertIsInstance(configurations.set_option('GENERAL', 'Language', 'en'), str)


if __name__ == '__main__':
    unittest.main()
