#!usr/bin/python3
# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE
import unittest
from Araneus.database import *

db = Database()


class TestDatabase(unittest.TestCase):
    def test_build(self):
        self.assertTrue(db.build())

    def test_bg_build(self):
        self.assertTrue(db.bg_build())

    def test_clean(self):
        self.assertTrue(db.clean())
