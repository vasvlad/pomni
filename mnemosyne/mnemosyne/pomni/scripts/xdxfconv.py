#!/usr/bin/python -tt
#vim: sw=4 ts=4 expandtab ai

import sys
import os
import xml.sax

from optparse import OptionParser
from xml.sax.handler import ContentHandler

from mnemosyne.libmnemosyne.card_types.three_sided import ThreeSided
from mnemosyne.libmnemosyne.component_manager import ui_controller_main, database, config, card_types
from mnemosyne import libmnemosyne

class XDXFHandler(ContentHandler):
    """ XDXF format handler """

    def __init__(self, output):
        self.tagnames = ('k', 'tr', 'ar')
        self.state = dict(zip(self.tagnames, [False] * len(self.tagnames)))
        self.key = self.transcription = ''
        self.translation = []
        self.output = output

    def startElement(self, name, attrs):
        self.state[name] = True

    def endElement(self, name):
        self.state[name] = False
        if name == 'ar':
            self.output.out(self)
            self.translation = []

    def characters(self, content):
        if self.state['k']:
            self.key = content.encode('utf8').strip()
        elif self.state['tr']:
            self.transcription = content.encode('utf8').strip()
        elif self.state['ar']:
            self.translation.extend([c.encode('utf8').strip() \
                for c in content.split("\n") \
                    if c and c.encode('utf8').strip() != self.key])

class TextOut(object):
    """ Text output """

    def __init__(self, fptr=sys.stdout):
        self.fptr = fptr
    
    def out(self, obj):
        if obj.transcription:
            self.fptr.write("%s\t[%s]\n%s" % (obj.key, obj.transcription, "\n".join(obj.translation)))
        else:
            self.fptr.write("%s\t%s" % (obj.key, "\n".join(obj.translation)))

class PickleOut(object):
    
    def __init__(self, dbname="default.mem", datadir=None, category=None, records=None):
        
        if datadir:
            datadir = os.path.abspath(datadir)
        elif os.path.exists(os.path.join(os.getcwdu(), ".mnemosyne")):
            datadir = os.path.abspath(os.path.join(os.getcwdu(), ".mnemosyne"))
        else:
            datadir = os.path.abspath(os.path.join(os.path.expanduser('~'), ".mnemosyne"))

        libmnemosyne.initialise(datadir)
        self.card_type = ThreeSided()
        self.dbname = dbname
        self.database = database()
        self.saved = False
        
        if records:
            self.records = records
        else:
            self.records = -1

        if not category:
            self.category = ['category1']
        else:
            self.category = [category]

        self.controller = ui_controller_main()

    def out(self, obj):
        """ Insert into the database """
        def fact_exists(name):
            for fact in self.database.facts:
                if fact.data['f'] == name:
                    return True
        
        if self.records and len(obj.key) > 3 and not fact_exists(obj.key): # skip duplicate names and short words
            fact = {'f': obj.key, 't': obj.translation}
            if obj.transcription:
                fact['p'] = obj.transcription
            else:
                fact['p'] = ''
       
            self.controller.create_new_cards(fact, self.card_type, 0, [self.category])
            self.records -= 1

        if not self.records:
            self.savedb()

    def savedb(self):
        if not self.saved:
            self.database.save(config()['path'])
            self.saved = True

    def __del__(self):
        """ Save the database on exit """
        self.savedb()

def parse_commandline(argv):
    """ Parse commandline, check options """
    
    parser = OptionParser(usage = "%prog [options] <xdxf file> [<output file>]")

    parser.add_option("-c", "--category", help="specify category name", metavar="catname")
    parser.add_option("-f", "--format", type="choice", choices=("pickle", "text"), default="pickle", metavar="format", \
        help="output format: pickle or text, [default: %default]")
    parser.add_option("-d", "--datadir", help="data directory")
    parser.add_option("-r", "--records", type="int", help="amount of records to load")

    options, argv = parser.parse_args(argv)

    if len(argv) < 2:
        parser.error("missed mandatory parameter <xdxf file>")

    return (options, argv)

def main(argv):

    opts, argv = parse_commandline(argv)

    parser = xml.sax.make_parser()

    outfn = None
    if len(argv) > 2:
        outfn = argv[2]

    if not opts.format or opts.format == 'pickle':
        out = PickleOut(outfn, opts.datadir, opts.category, opts.records)
    else:
        outfp = None 
        if outfn:
            outfp = open(outfn, 'w')
        out = TextOut(outfp)

    parser.setContentHandler(XDXFHandler(out))
    parser.parse(open(argv[1], 'r'))
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))

