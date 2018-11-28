# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE
import unittest
from Araneus.database import *


class TestDatabase(unittest.TestCase):
    def test_build(self):
        Database().drop()
        self.assertTrue(Database().build())


if __name__ == '__main__':
    unittest.main()
