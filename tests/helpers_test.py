#!usr/bin/python3
# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE
import unittest
from Araneus.helpers import *


class TestHelpers(unittest.TestCase):
    def test_is_running(self):
        self.assertFalse(is_running())

    def test_load_ui(self):
        self.assertIsInstance(load_ui('about'), str)


if __name__ == '__main__':
    unittest.main()
