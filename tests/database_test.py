#!usr/bin/python3
# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE
import unittest
from Araneus.database import *

db = Database()


class TestDatabase(unittest.TestCase):
    def test_build(self):
        # self.assertTrue(db.build())
        pass

    def test_clean(self):
        # self.assertTrue(db.clean())
        pass


if __name__ == '__main__':
    unittest.main()
