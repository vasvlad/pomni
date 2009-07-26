#!/usr/bin/python -tt
#vim: sw=4 ts=4 expandtab ai

""" Converter from XDXF(http://xdxf.sourceforge.net/) 
    to Mnemosyne (http://www.mnemosyne-proj.org) database format 
"""

__copyright__ = """
Copyright (C) 2008 Ed Bartosh <bartosh@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.  THE SOFTWARE IS PROVIDED "AS
IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE
AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import sys
import os
import xml.sax

from optparse import OptionParser
from xml.sax.handler import ContentHandler

from mnemosyne import libmnemosyne
from mnemosyne.libmnemosyne.card_types.three_sided import ThreeSided
from mnemosyne.libmnemosyne.card_types.front_to_back import FrontToBack
from mnemosyne.libmnemosyne.component_manager import database, config
from mnemosyne.libmnemosyne.component_manager import ui_controller_main
from mnemosyne.libmnemosyne.category import Category
from mnemosyne.libmnemosyne.fact import Fact

class XDXFHandler(ContentHandler):
    """ XDXF format handler """

    def __init__(self, output):

        ContentHandler.__init__(self)

        self.tagnames = ("k", "tr", "ar")
        self.state = dict(zip(self.tagnames, [False] * len(self.tagnames)))
        self.key = self.transcription = ""
        self.translation = []
        self.output = output

    def startElement(self, name, attrs):
        """ callback for the start of an element """
        self.state[name] = True

    def endElement(self, name):
        """ callback for the end of an element """
        
        self.state[name] = False
        if name == "ar":
            self.output.out(self)
            self.translation = []

    def characters(self, content):
        """ callback for character data """

        if self.state["k"]:
            self.key = content.encode("utf8").strip()
            #self.key = content
        elif self.state["tr"]:
            #self.transcription = content
            self.transcription = content.encode("utf8").strip()
        elif self.state["ar"]:
            #self.translation.extend([c for c in content.split("\n") 
            #                            if c != self.key])

            #self.translation.extend([c.encode("utf8").strip() \
            #    for c in content.split("\n") \
            #        if c and c.encode("utf8").strip() != self.key])

            self.translation = content.encode("utf8").strip()

class TextOut(object):
    """ Text output """

    def __init__(self, fptr=sys.stdout):
        self.fptr = fptr
    
    def out(self, obj):
        """ main entry point. Called from XDXF parser """

        if obj.transcription:
            self.fptr.write("%s\t[%s]\n%s" % (obj.key, obj.transcription, 
                            "\n".join(obj.translation)))
        else:
            self.fptr.write("%s\t%s" % (obj.key, "\n".join(obj.translation)))

class MnemosyneOut(object):
    """ Output to Mnemosyne Db """
    
    def __init__(self, datadir=None, category=None, records=None):
        
        if datadir:
            datadir = os.path.abspath(datadir)
        elif os.path.exists(os.path.join(os.getcwdu(), ".mnemosyne")):
            datadir = os.path.abspath(os.path.join(os.getcwdu(), ".mnemosyne"))
        else:
            datadir = os.path.abspath(os.path.join(os.path.expanduser("~"), 
                        ".mnemosyne"))

        print 'datadir=', datadir

        libmnemosyne.initialise(datadir)

        self.card_type = FrontToBack()
        self.database = database()
        self.saved = False
        
        if records:
            self.records = records
        else:
            self.records = -1

        if not category:
            category = "English-Russian"
        
        self.category = category #Category(category)

        self.controller = ui_controller_main()

    def out(self, obj):
        """ main entry point. Called from XDXF parser """

        def fact_exists(name):
            """ Check if fact with the same key is 
                in database
            """
            return False
            for fact in self.database.facts:
                if fact.data["f"] == name:
                    return True
       
        # skip duplicate names and short words (ugly)
        if self.records and len(obj.key) > 3 and not fact_exists(obj.key):

            data = {"q": obj.key, "a": obj.translation}
            #if obj.transcription:
            #    data["p"] = obj.transcription

            #print 'f:', obj.key
            #print 't:', obj.translation
            #print 'p:', obj.transcription

            self.controller.create_new_cards(data, self.card_type, 0, 
                                            [self.category])
            self.records -= 1

        if not self.records:
            self.savedb()

    def savedb(self):
        """ Save the database if not saved yet """

        if not self.saved:
            self.database.save(config()["path"])
            self.saved = True

    def __del__(self):
        """ Save the database on exit """

        self.savedb()
        libmnemosyne.finalise()

def parse_commandline(argv):
    """ Parse commandline, check options """
    
    parser = OptionParser(usage = "%prog [options] <xdxf file>")

    parser.add_option("-c", "--category", help="specify category name", 
        metavar="category")
    parser.add_option("-f", "--format", type="choice", 
        choices=("mnemosyne", "text"), default="mnemosyne", metavar="format",
        help="output format: mnemosyne or text, [default: %default]")
    parser.add_option("-d", "--datadir", help="data directory")
    parser.add_option("-r", "--records", type="int", 
        help="amount of records to load")

    options, argv = parser.parse_args(argv)

    if len(argv) < 2:
        parser.error("missed mandatory parameter <xdxf file>")
    if not os.access(argv[1], os.R_OK):
        parser.error("file %s isn't readable or doesn't exist" % argv[1])

    return (options, argv)

def main(argv):
    """ Main """

    opts, argv = parse_commandline(argv)

    parser = xml.sax.make_parser()

    if not opts.format or opts.format == "mnemosyne":
        out = MnemosyneOut(opts.datadir, opts.category, opts.records)
    else:
        out = TextOut()

    parser.setContentHandler(XDXFHandler(out))
    parser.parse(open(argv[1], "r"))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))

