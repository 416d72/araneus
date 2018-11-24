import unittest

from Araneus.preferences import *


class TestPreferences(unittest.TestCase):

    def test_create_config_dir(self):
        self.assertEqual(Preferences().create_config_dir(), True)

    def test_create_config_file(self):
        self.assertEqual(Preferences().create_config_file(), True)

    def test_reset(self):
        self.assertEqual(Preferences().reset(), True)


if __name__ == '__main__':
    unittest.main()
