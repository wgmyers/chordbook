# libcbk.py

# Library to read .cbk files

import json

class Tune(object):
    def __init__(self):
        pass 
    
    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def do_transpose(self, c):
        """Take a chord and transpose it according to transpose element if present"""

        keys = [
                ["A", "B", "C#", "D", "E", "F#", "G#"],
                ["Bb", "C", "D", "Eb", "F", "G", "A"],
                ["B", "C#", "D#", "E", "F#", "Ab", "A#"],  # non-standard, readable
                ["C", "D", "E", "F", "G", "A", "B"],
                ["Db", "Eb", "F", "Gb", "Ab", "Bb", "C"],
                ["D", "E", "F#", "G", "A", "B", "C#"],
                ["Eb", "F", "G", "Ab", "Bb", "C", "D"],
                ["E", "F#", "G#", "A", "B", "C#", "D#"],
                ["F", "G", "A", "Bb", "C", "D", "E"],
                ["F#", "Ab", "Bb", "B", "Db", "Eb", "F"],  # ditto
                ["G", "A", "B", "C", "D", "E", "F#"],
                ["Ab", "Bb", "C", "Db", "Eb", "F", "G"],
                ]

        majors = []
        minors = []
        for k in keys:
            majors.append(k[0])
            minors.append(k[5])

        # Split c into chord and suffix if present
        # Look mum, no regexes :)
        minor = False
        c = c + "    " # guarantee we have enough chars for below to work
        index = 1
        if c[index] == "#" or c[index] == "b":
            index += 1
        if c[index] == "m" and c[index:index+3] != "maj7":
            #index += 1
            minor = True
        chord = c[:index]
        suffix = c[index:].strip() # lose spurious w/s we just added
            
        # Move c that distance
        ki = majors
        if minor == True:
            ki = minors

        ikey = ki.index(self.key)
        tkey = ki.index(self.transpose)
        ckey = ki.index(chord)

        chord = ki[(ckey + tkey - ikey) % 12]

        newchord = chord + suffix

        # Return new key
        return newchord

    def process_section(self, s):
        """Take a section and return an array of chords"""
        inchords = s.split("|")
        outchords = []

        for c in inchords:
            outchords.append(self.do_transpose(c.strip()))

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


        

    
