import sys
from .File import read_file

def printusage():
    usage_list = read_file('resources/Usage.out')
    for u in usage_list:
        print(u)
    sys.exit(0)
