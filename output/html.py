# html.py

# An html outputter for Chordbook

from _base import CbkOutputter

class html(CbkOutputter):

    # FIXME - templating should be external
    # For now let's just put it here
    html_head = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<title>{{TITLE}}</title>
<link rel="stylesheet" href="{{CSS_LOC}}" type="text/css" />
</head>
<body>
"""

    html_foot = """
</body>
</html>
"""

    def make_tune(self, t):
        """Format an individual tune"""
        s = "<a name=\"\"></a><h3>" + t.name + "</h3>\n"

        seen = {}
        for section in t.structure:
            if section.title() in seen:
                s += "<h5>" + section.title() + "</h5>\n"
            else:
                s += "<h4>" + section.title() + "</h4>\n"
                chunks = self.chunk_section(t.__getattribute__(section))
                for c in chunks:
                    s += "<p style=\"chords\">" + c + "</p>\n"
                seen[section.title()] = True

        return s

    def make_contents(self, b):
        """Make the contents part of the HTML output"""
        c = b.get_contents()

        s = "<h2>Contents</h2>\n<ol>"

        for title in c:
            s += "<li><a href=\"\">" + title + "</a></li>\n"

        s += "</ol>\n"

        return s

    def make_header(self, b):
        """Make the header part of the HTML output"""
        s = "<h1>" + b.band + "</h1>\n"
        s += "<p><i>Version " + b.version + "</i></p>\n"

        return s

    def make_book(self, b):
        """Output HTML version of book data"""

        o = self.html_head

        o = o.replace("{{TITLE}}", b.band)

        s = self.make_header(b)
        o += s

        s = self.make_contents(b)
        o += s

        for t in b.tunes:
            o += self.make_tune(t)

        o += self.html_foot

        print o


