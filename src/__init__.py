import glob, os, datetime


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return "%3.2f %s" % (num, x)
        num /= 1024.0


# iconD = "📁"
# iconF = ""
for file in glob.glob("/home/amr/Documents/kingstone/**", recursive = True):
    if os.path.islink(file) is True:
        continue
    # if os.path.isdir(file) is True:
    #     print("Directory")
    # elif os.path.isfile(file) is True:
    #     print("File")
    name = os.path.splitext(os.path.basename(file))
    fileName = name[0]
    extension = name[1]
    path = os.path.abspath(file)
    size = convert_bytes(os.stat(file).st_size)
    date = datetime.datetime.fromtimestamp(os.stat(file).st_mtime).__str__()[:19]
    print(fileName, extension, path, size, date)
