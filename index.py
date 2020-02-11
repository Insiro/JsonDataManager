import sys
from Loader import Loader

if __name__ == "__main__":
    arg = sys.argv[1:]
    if "server" in arg:
        roader = Loader(runserver=True)
    else:
        roader = Loader()
    roader.cui()