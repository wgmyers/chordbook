# _base.py

# Base class for ChordBook outputters

import libcbk

class CbkOutputter(object):

    def __init__(self):
        pass

    def makebook(self, b):

        print repr(b);
