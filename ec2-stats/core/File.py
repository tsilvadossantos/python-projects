import os.path
import json
import re
import sys

class File(object):
    """Read file and return a list of data"""
    def __init__(self, filename = None):
        if filename != None:
            self.filename = filename
        self.data_loaded = {}

    def read_json_file(self):
        try:
            with open(self.filename, "r") as r:
                self.data_loaded = json.load(r)
                return self.data_loaded
        except:
            print 'Error reading the file: {}'.format(self.filename)
        return False

    def write_to_file(self, data, mode):
        f = open(self.filename, mode)
        f.write(data + '\n')
        f.close


    def abort_operation(self):
        sys.exit(1)
