# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE
import unittest
from Araneus.connection import *


class TestConnection(unittest.TestCase):
    def test_create(self):
        self.assertTrue(Connection().create())

    def test_insert(self):
        self.assertTrue(Connection().insert("test", "test", "test", "test", "test", "test"))

    def test_get(self):
        self.assertIsInstance(Connection().get("test"), list)

    def test_fetch_all(self):
        self.assertIsInstance(Connection().fetch_all(), list)

    def test_drop(self):
        self.assertTrue(Connection().drop())


if __name__ == '__main__':
    unittest.main()
