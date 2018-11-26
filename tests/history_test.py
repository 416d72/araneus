#!usr/bin/python3
# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE
import unittest
from Araneus.history import *

h = History()


class TestHistory(unittest.TestCase):
    def test_create(self):
        self.assertTrue(h.create())

    def test_clear(self):
        self.assertTrue(h.clear())

    def test_append(self):
        self.assertTrue(h.add('amr'))

    def test_get(self):
        self.assertIsInstance(h.get(), list)
