# text.py

# A plaintext outputter for ChordBook

from _base import CbkOutputter

class text(CbkOutputter):

    def makebook(self, b):
        print "Text class"
        super(text, self).makebook(b)
