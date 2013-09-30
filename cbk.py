#!/usr/bin/env python

# chordbook.py
# A tool to manage books of chords for bands

# modules
import sys
import os.path
import optparse

from chordbook import libcbk
from chordbook._version import __version__

# parse commandline
p = optparse.OptionParser()

p.add_option("-i", "--input", action="store", type="string", dest="infile")
p.add_option("-o", "--output", action="store", type="choice", dest="output",
                choices=["text", "html"])
p.add_option("-v", "--version", action="store_true", dest="version")
p.add_option("-s", "--stdout", action="store_true", dest="stdout")

p.set_defaults( output="html",
                infile="chordbook/examples/test.cbk",
                stdout=False)

opt, args = p.parse_args()

# version reporting
if opt.version:
    print "This is ChordBook version", __version__
    sys.exit()

# output module importing
output_type = opt.output
output_module_name = "chordbook.output." + output_type
output_module = __import__(output_module_name, fromlist=[output_type])
output_classname = "Cbk" + output_type.title() + "Outputter"
output_class = getattr(output_module, output_classname)
o = output_class(output_type)

# set stdout option
if opt.stdout == True:
    o.stdout = True

# read input
if not os.path.isfile(opt.infile):
    raise RuntimeError("Can't find input file '%s'." % opt.infile)

book = libcbk.Book()
f = open(opt.infile)
book.load_json(f)
f.close()

# produce output
o.make_book(book)

