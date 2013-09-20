# html.py

# An html outputter for Chordbook

from _base import CbkOutputter

class html(CbkOutputter):

    def make_book(self, b):
        print "HTML class"
        super(html, self).make_book(b)
