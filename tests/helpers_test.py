# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE
import unittest

from Araneus.helpers import *


class TestHelpers(unittest.TestCase):
    def test_is_running(self):
        self.assertTrue(is_running())

    def test_load_ui(self):
        self.assertIsInstance(load_ui('about'), str)

    def test_convert_time(self):
        self.assertIsInstance(convert_time(int(1540454196.3441148)), str)


if __name__ == '__main__':
    unittest.main()
