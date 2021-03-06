"""Handle .cbk files"""

import json


# Constants for Tune.do_transpose()
IGNORE = [".", "/", "..", "//", "%", "NC", "N/C", "(+)"]

MAJORS = ["A", "Bb", "B", "C", "Db", "D",
          "Eb", "E", "F", "F#", "G", "Ab"]

MINORS = ["F#", "G", "Ab", "A", "Bb", "B",
          "C", "C#", "D", "Eb", "E", "F"]

MISSING = { 'A#':'Bb', 'B#':'C', 'C#':'Db', 'D#':'Eb', 'E#':'F',
            'G#':'Ab', 'Cb':'B', 'Db':'C#', 'Fb':'E', 'Gb':'F#' }

def get_keyname(chord):
    """Take key name which may have 'm' at end; strip 'm' if present"""
    if chord[len(chord) - 1] == "m":
        return chord[:len(chord) - 1]
    else:
        return chord

class Tune(object):

    """Handle individual tunes"""

    def __init__(self):
        self.key = ""
        self.transpose = ""
    
    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def do_transpose(self, chord):
        """Transpose a chord according to transpose element if present"""

        # Make sure we have a transpose attribute before we go any further
        if self.transpose == "":
            return chord

        # Don't transpose the empty string
        if chord == "":
            return chord

        # Don't try and transpose the untransposable
        if chord in IGNORE:
            return chord
        # Handle arbitrary time signatures reasonably (don't try transposing)
        if chord[0].isdigit():
            return chord
        # Allow notes delimited by [ ] containing one space
        if chord[0] == "[":
            return chord
        if chord[-1] == "]":
            return chord

        # Preserve prefixed '('
        prefix = ""
        if chord[0] == "(":
            prefix = "("
            chord = chord[1:]

        # Split chord into schord and suffix if present
        # Look mum, no regexes :)
        minor = False
        chord = chord + "    " # guarantee chord string is long enough 
        index = 1
        if chord[index] == "#" or chord[index] == "b":
            index += 1
        if ((chord[index] == "m") and (chord[index:index+4] != "maj7")) or \
            (chord[index:index+3] == "dim"):
            minor = True
        schord = chord[:index]
        suffix = chord[index:].strip() # lose spurious w/s we just added
            
        # Move c that distance
        kind = MAJORS
        if minor == True:
            kind = MINORS

        key = get_keyname(self.key)
        if key not in kind:
            key = MISSING[key]
        ikey = kind.index(key)
        transpose = get_keyname(self.transpose)
        if transpose not in kind:
            transpose = MISSING[transpose]
        tkey = kind.index(transpose)
        if schord not in kind:
            schord = MISSING[schord]
        ckey = kind.index(schord)

        schord = kind[(ckey + tkey - ikey) % 12]

        # If we have a slash bass note we need to transpose that too
        # FIXME - This code is horrorshow
        if ((len(suffix) > 1) and (suffix[-2] == "/")):
            suffix = suffix[:-1] + self.do_transpose(suffix[-1])
        elif ((len(suffix) > 2) and (suffix[-3] == "/") and (suffix[-1] == ")")):
            suffix = suffix[:-2] + self.do_transpose(suffix[-2]) + ")"
        elif ((len(suffix) > 2) and (suffix[-3] == "/")):
            suffix = suffix[:-2] + self.do_transpose(suffix[-2]+suffix[-1])
        elif ((len(suffix) > 3) and (suffix[-4] == "/") and (suffix[-1] == ")")):
            suffix = suffix[:-3] + self.do_transpose(suffix[-3]+suffix[-2]) + ")"

        newchord = prefix + schord + suffix

        # Return new key
        return newchord

    def process_section(self, section):
        """Take a section and return an array of bars of chords"""
        inbars = section.split("|")
        outbars = []
        nonchords = ["LR", "RR"]

        for bar in inbars:
            chords = bar.strip().split(" ")
            outchords = []
            for crd in chords:
                crd = crd.strip()
                if crd in nonchords:
                    outchords.append(crd)
                else:
                    outchords.append(self.do_transpose(crd.strip()))
            outbars.append(" ".join(outchords))

        return outbars

    def chunk_section(self, section):
        """Take a section and return an array of 4 bar chunks"""
        # Transform "|:" and ":|" into LR and RR
        section = section.replace("|:", "LR")
        section = section.replace(":|", "RR")

        bars = section.split("|")

        chunks = []
        sep = "|"
        for i in range(0, len(bars), 4):
            # Avoid orphans
            if i+7 > len(bars):
                chunks.append(sep.join(bars[i:]).strip())
                break
            else:
                chunks.append(sep.join(bars[i:i+4]).strip())

        return chunks

    def get_artist(self):
        """Return string containing composer / credit attributes if present"""

        artist = "Unknown"
        has_composer = False
        if hasattr(self, 'composer'):
            artist = self.composer
            has_composer = True
        if hasattr(self, 'credit'):
            if has_composer == True:
                artist += " - " + self.credit
            else:
                artist = self.credit
        return artist

class Book(object):

    """Handle the book of tunes"""

    def __init__(self):
        self.tunes = []
        self.band = ""
        self.version = ""
        self.filename = ""

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)

    def get_contents(self):
        """Return an array of the names of the tunes"""

        contents = []
        for tune in self.tunes:
            title = tune.name
            title += " - " + tune.get_artist()
            contents.append(title)
        contents.sort()

        return contents

    def sort_tunes(self):
        """Sort tunes by tune.name"""

        self.tunes.sort(key = lambda x: x.name)

    def load_json(self, infile):
        """Load json data"""

        json_data = json.load(infile)

        self.band = json_data['band']
        self.version = json_data['version']
        self.filename = infile.name

        for tune_data in json_data['tunes']:
            tune = Tune()
            for k in tune_data.keys():
                tune.__setattr__(k, tune_data[k])
            self.tunes.append(tune)

        self.sort_tunes()


    
