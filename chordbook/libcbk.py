# libcbk.py

# Library to read .cbk files

import json

class Tune(object):
    def __init__(self):
        pass 
    
    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def transpose(self, c):
        """Take a chord and transpose it according to transpose element if present"""

        # Not yet implemented. Return input
        return c

    def process_section(self, s):
        """Take a section and return an array of chords"""
        inchords = s.split("|")
        outchords = []

        for c in inchords:
            outchords.append(self.transpose(c.strip()))

        return outchords

    def chunk_section(self, s):
        """Take a section and return an array of 4 bar chunks"""
        chords = s.split("|")

        chunks = []
        sep = "|"
        for i in range(0, len(chords), 4):
            chunks.append(sep.join(chords[i:i+4]).strip())

        return chunks


class Book(object):
    def __init__(self):
        self.tunes = []

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def get_contents(self):
        """Return an array of the names of the tunes"""

        c = []
        for t in self.tunes:
            c.append(t.name)
        c.sort()

        return c

def load_json(infile):
    json_data = json.load(infile)

    b = Book()

    b.band = json_data['band']
    b.version = json_data['version']

    for tune_data in json_data['tunes']:
        t = Tune()
        for k in tune_data.keys():
            t.__setattr__(k, tune_data[k])
        b.tunes.append(t)

    return b


        

    
