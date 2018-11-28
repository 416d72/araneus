#!usr/bin/python3
# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE
import unittest
from Araneus.database import *


class TestDatabase(unittest.TestCase):
    def test_build(self):
        self.assertTrue(Database().build())

    def test_to_sql(self):
        self.assertIsInstance(Database().to_sql({''}))

    def test_clean(self):
        self.assertTrue(Database().drop())


if __name__ == '__main__':
    unittest.main()
