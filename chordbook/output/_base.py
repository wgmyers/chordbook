# _base.py

# Base class for ChordBook outputters

import chordbook.libcbk

class CbkOutputter(object):

    def __init__(self):
        pass

    def chunk_section(self, s):
        """Take a section and return an array of 4 bar chunks"""
        chords = s.split("|")

        chunks = []
        sep = "|"
        for i in range(0, len(chords), 4):
            chunks.append(sep.join(chords[i:i+4]).strip())

        return chunks

    def make_book(self, b):
        """Output internal representation of Book object"""
        print repr(b);
