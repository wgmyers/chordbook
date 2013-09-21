# libcbk.py

# Library to read .cbk files

import json

class Tune(object):
    def __init__(self):
        pass 
    
    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


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


        

    
