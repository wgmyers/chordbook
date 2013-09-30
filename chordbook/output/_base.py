"""Base class for ChordBook outputters"""

import os


class CbkOutputter(object):

    """Base class for ChordBook outputters"""

    def __init__(self, outputdir):
        """Subclasses should call this then set their own file suffix"""
        self.outputdir = outputdir
        self.output = ""
        self.stdout = False
        self.outputfilesuffix = "repr.txt"

    def make_book(self, book):
        """Store internal representation of Book object"""

        # Just do a repr() on the book object
        self.output = repr(book)

        # Subclasses need to call this at the end of their make_book() 
        self.output_book(book.filename)

    def output_book(self, filename):
        """ Either print output to stdout or save it as file.
            Filename of json data file given as argument used
            to derive output filename"""

        if self.stdout == True:
            print self.output
        else:
            # create output file name from given filename
            root, suffix = os.path.splitext(os.path.basename(filename))
            outputfile = ".".join([root, self.outputfilesuffix])

            # check outputdir exists, create it if not
            if os.path.isdir(self.outputdir) == False:
                os.mkdir(self.outputdir)
            
            # write the file
            outfile = os.path.join(self.outputdir, outputfile)

            ofile = open(outfile, "w")
            ofile.write(self.output)
            ofile.close()
