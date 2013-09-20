# text.py

# A plaintext outputter for ChordBook

from _base import CbkOutputter

class text(CbkOutputter):

    def make_contents(self, b):
        """Return a string for the contents of the output"""
        c = b.get_contents()

        s = ""
        for title in c:
            s += title
            s += "\n"

        return s

    def make_header(self, b):
        """Return a string for the header of the output"""
        s = b.band + " (version " + b.version + ")"
        s = s.encode('utf-8')
        s = s + "\n" + ("=" * len(s)) + "\n"
        return s

    def make_book(self, b):
        """Output plaintext version of book data"""
        s = self.make_header(b)
        print s

        s = self.make_contents(b)
        print s

        super(text, self).make_book(b)
