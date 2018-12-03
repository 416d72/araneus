# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE
import unittest
from Araneus.helpers import *


class TestHelpers(unittest.TestCase):
    def test_is_running(self):
        self.assertIsInstance(is_running(), IOError)

    def test_load_ui(self):
        self.assertIsInstance(load_ui('about'), str)


if __name__ == '__main__':
    unittest.main()
