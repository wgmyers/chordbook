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
<!-- <link rel="stylesheet" href="{{CSS_LOC}}" type="text/css" /> -->
<style type="text/css">

body {
    font-family: Helvetica, Arial, sans-serif;
    background-color: #faf0e6;
    margin: 0% 5%;
}

h1, h2, h5, p {
    text-align: center;
    padding: 0%;
    margin: 0%;
}

h3 {
    padding: 0%;
    margin: 0%;
}

h4 {
    padding: 0% 10%;
    margin: 0%;
    background-color: #b0e0e6;
}

p {
    margin: 0px;
    padding: 0px;
}

table {
    width: 100%;
}

td {
    width: 25%;
}

td.bar {
    border-right: 1px solid black;
}

td.directive {
    text-align: right;
}

.titlepage {

    background-color: #ffefd5;
    height: 100%;
    border: thin solid #000;
    margin-top: 10px;
}

.tune {
   
    page-break-before: always;
    background-color: #ffefd5;
    height: 100%;
    margin: 5% 0%;
    border: thin solid #000;

}

.chords {
    text-align: center;
    font-size: 20pt;
}

.spacer {
    height: 600px;
}

@media print {
    .spacer { display: none; }
}

</style>
</head>
<body>
"""

    html_foot = """
<p class="spacer">&nbsp;</p>
</body>
</html>
"""

    def strip_spaces(self, s):
        """Take a string and strip spaces from it"""
        s = s.replace(" ", "")
        return s

    def replace_entities(self, c):
        """Take a bar of chords, replace suitable HTML entities"""

        # replace '#' with &#x266f
        c = c.replace("#", "&#x266f;")
        # replace m7b5 with oslash
        c = c.replace("m7b5", "&oslash;7")
        # replace 'b' with &#x266d
        c = c.replace("b", "&#x266d;")
        # replace 'maj7' with &Delta;
        c = c.replace("maj7", "&Delta;")

        return c

    def make_tune(self, t):
        """Format an individual tune"""
        s = "<div class=\"tune\">\n"
        anchor = self.strip_spaces(t.name)
        s += "<table><tr>"
        key = t.key
        if t.transpose:
            key = t.transpose + " (orig " + t.key + ")"
        s += "<td><a name=\"" + anchor + "\"></a><h3>" + t.name + \
                "</h3></td><td class=\"directive\"><i>" + t.time + \
                " " + key + "</i></td>\n"
        s += "</tr></table>"
        

        seen = {}
        for section in t.structure:
            if section.title() in seen:
                s += "<h5>" + section.title() + "</h5>\n"
            else:
                s += "<h4>" + section.title() + "</h4>\n"
                s += "<table>\n"
                chunks = t.chunk_section(t.__getattribute__(section))
                for chunk in chunks:
                    s += "<tr>"
                    chords = t.process_section(chunk)
                    i = 0
                    for c in chords:
                        # Replace plaintext with musical HTML equivalents
                        c = self.replace_entities(c)
                        if (i < len(chords) - 1):
                            s += "<td class=\"bar\">"
                        else:
                            s+= "<td>"
                        s += "<p class=\"chords\">" + c + "</p></td>"
                        i += 1
                    s += "</tr>"
                seen[section.title()] = True
                s += "</table>\n"

        s +="</div>\n<p class=\"spacer\">&nbsp;</p>\n"

        return s

    def make_contents(self, b):
        """Make the contents part of the HTML output"""
        c = b.get_contents()

        s = "<h2>Contents</h2>\n<ol>"

        for title in c:
            anchor = self.strip_spaces(title)
            s += "<li><a href=\"#" + anchor + "\">" + title + "</a></li>\n"

        s += "</ol>\n"

        s += "</div>\n<p class=\"spacer\">&nbsp;</p>\n"

        return s

    def make_header(self, b):
        """Make the header part of the HTML output"""
        s = "<div class=\"titlepage\">\n"
        s += "<h1>" + b.band + "</h1>\n"
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


