import unittest
import json
from Araneus.preferences import *


def test_os():
    assert check_os() is True
