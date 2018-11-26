#!/usr/bin/python3
# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE
import os
import sys

pid_file = '/tmp/Araneus.pid'


def check_os():
    """
    Checks if the current operating system is only Linux so that the app won't fail with others
    :return: None
    """
    if not sys.platform.startswith('linux'):
        sys.exit('This operating system is not supported!')


def is_running():
    """
        Allows for only one instance of the app by creating a .pid file in /tmp directory and checking if it exists
        :return: int or False
        """
    check_os()
    try:
        with open(pid_file, 'r') as f:
            pid = int(next(f))
        return os.kill(pid, 0)
    except Exception:
        return False


def load_ui(name):
    """
    Loads the full path to the UI template that was created with QT Designer which exists in UI directory
    :param name:
    :return: String
    """
    return str(os.path.abspath(os.getcwd()) + '/UI/' + name + '.ui')


if __name__ == "__main__":
    if is_running():
        sys.exit("Only one instance allowed")
    with open(pid_file, 'w') as f:
        f.write(f'{os.getpid()}')
