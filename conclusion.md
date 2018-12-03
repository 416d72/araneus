# Here are things that I learnt through out making this app
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
    - Getting file attributes with either `os.stat` or `os.path.get*`.
- Interacting with operating system:
    - Executing system commands with `os.system(command)` or `subprocess.getoutput(command)`.
    - Getting user's home directory with `os.path.expanduser(~)`
    - Checking what OS is currently running with `sys.platform`.
    - Allowing only one instance by creating a `.pid` file and handling it.
    - Opening a file in the default file manager in linux using command `xdg-open {location}`
- Tricks:
    - `lambda`, `with`, `if __name__ == "__main__"`, `yield`
    - Opening a url in the default browser with `import webbrowser` and `webbrowser.open(url)`.
    - Passing lists or tuples' items as method parameters like this:
        `method(*tuple)`
    - Converting from unix timestamp to time format using `datetime` like this:
        `datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')` 
### QT
- Embedding shortcuts in QT designer app templates instead of using event listener in the controller.
- Figured out how to load several Qt windows thanks to this old answer [here](http://python.6.x6.nabble.com/QCoreApplication-exec-The-event-loop-is-already-running-tp1795366p1795378.html)
- Learnt how to control the visibility of columns in Qtreeview thanks to [that answer](https://stackoverflow.com/a/26675732/7301680)
- Running methods in background thanks to [this awesome answer](https://stackoverflow.com/a/33453124/7301680)
# Other things that I'd like to learn deeper in the near future:
- Formatting strings
- Exception handling.
- Multi processing.
- Multi threading.
- Logging.
- Test Driven Development.
- Documentation.
- Cryptography.
- Security.
- Advanced web scraping.
- Live stream Face detection.