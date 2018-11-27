Here are things that I learnt through out making this app
-
### Python:
- Structuring files.
    - Using a helper file and `import` it in other files to use common functions in several scripts.
- Testing:
    - Unit tests with Python's `unittest`.
    - Automating tests by running a command `os.system('python -m unittest *_test.py')`.
    - Using `try` and `except` to facilitate tests.
-Files:
    - Handling `.json` files.
    - Handling `.ini` files for saving configurations using `configparser`.
    - Copying files with their permissions with `copy2` from `shutil` module.
    - Prepend text to a file thanks to [this answer](https://stackoverflow.com/a/4454598/7301680).
- Interacting with operating system:
    - Executing system commands with `os.system(command)`.
    - Getting user's home directory with `os.path.expanduser(~)`
    - Checking what OS is currently running with `sys.platform`.
    - Allowing only one instance by creating a `.pid` file and handling it.
- Tricks:
    - `lambda`, `with`, `if __name__ == "__main__"`
    - Opening a url in the default browser with `import webbrowser` and `webbrowser.open(url)`.
### QT
- Embedding shortcuts in QT designer app templates instead of using event listener in the controller.
- Figured out how to load several Qt windows thanks to this old answer [here](http://python.6.x6.nabble.com/QCoreApplication-exec-The-event-loop-is-already-running-tp1795366p1795378.html)
- Learnt how to control the visibility of columns in Qtreeview thanks to [that answer](https://stackoverflow.com/a/26675732/7301680)
 
And here are things that I'd like to learn deeper in the near future:
-
- Exception handling.
- Multi processing.
- Multi threading.
- Test Driven Development.
- Documentation.
- Cryptography.
- Security.
- Advanced web scraping.
- Live stream Face detection.