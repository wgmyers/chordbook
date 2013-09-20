# html.py

# An html outputter for Chordbook

from _base import CbkOutputter

class html(CbkOutputter):

    def makebook(self, b):
        print "HTML class"
        super(html, self).makebook(b)
