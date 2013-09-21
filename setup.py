# setup.py

from distutils.core import setup

import re
VERSIONFILE="./_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % VERSIONFILE) 


setup(  name="ChordBook",
        version=verstr,
        author="Wayne Myers",
        author_email="wgmyers@gmail.com",
        description="A tool to manage books of chords for bands.",
        py_modules=['libcbk'],
        packages=['output'],
        scripts=['chordbook.py'],
        url="https://github.com/wgmyers/chordbook",
        )
