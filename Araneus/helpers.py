#!/usr/bin/python3
# -*- coding: utf-8; -*-
# LICENSE: see LICENSE.txt
import os
import sys

lock_file = '/tmp/Araneus.lock'


def check_os():
    """
    Checks if the current operating system is only Linux so that the app won't fail with others
    :return: None
    """
    if not sys.platform.startswith('linux'):
        sys.exit('This operating system is not supported!')


def one_instance():
    """
    Allows for only one instance of the app by creating a .lock file in /tmp directory and checking if it exists
    :return: None | Error message
    """
    check_os()
    if os.path.isfile(lock_file):
        sys.exit()
    else:
        try:
            with open(lock_file, 'w+') as file:
                file.write("Araneus Instance")
        except ValueError:
            sys.exit(ValueError)


def load_ui(name):
    return str(os.path.abspath(os.getcwd()) + '/UI/' + name + '.ui')
