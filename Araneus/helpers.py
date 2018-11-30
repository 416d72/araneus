# -*- coding: utf-8; -*-
# LICENSE: see Araneus/LICENSE
import os
import sys

pid_file = '/tmp/Araneus.pid'
config_dir = os.path.expanduser('~') + '/.config/Araneus/'


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
        return Exception


def load_ui(name):
    """
    Loads the full path to the UI template that was created with QT Designer which exists in UI directory
    :param name:
    :return: String
    """
    return str(os.path.abspath(os.getcwd()) + '/UI/' + name + '.ui')


def convert(size: int):
    """
    Convert size from Bytes to KB,MB,GB,TB.
    :param size: int
    :return: str
    """
    if size == 0:
        return ''
    elif size < 1024:
        return '%d Bytes' % size
    power = 2 ** 10
    n = 0
    d = {0: 'Bytes', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size >= power:
        size /= power
        n += 1
    return "%.2f " % round(size, 2) + d[n]


def about_dialog():
    """
    Showing the about dialog | Influenced by the about dialog from 'Zeal' app
    :return: None
    """
    from Araneus.about import new_window
    new_window()


if __name__ == "__main__":
    if is_running():
        sys.exit("Only one instance allowed")
    with open(pid_file, 'w') as f:
        f.write(f'{os.getpid()}')
