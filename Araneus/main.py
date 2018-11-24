#!usr/bin/python3
# -*- coding: utf-8; -*-
from Araneus.preferences import *


def check_os():
    """
    Checks if the current operating system is only Linux so that the app won't fail with others
    :return: Bool
    """
    if sys.platform.startswith('linux'):
        return True
