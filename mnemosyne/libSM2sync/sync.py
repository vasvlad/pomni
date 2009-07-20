# vim: sw=4 ts=4 expandtab ai
#
# sync.py
#
# Max Usachev <maxusachev@gmail.com>, 
# Ed Bartosh <bartosh@gmail.com>, 
# Peter Bienstman <Peter.Bienstman@UGent.be>


import mnemosyne.version
import cgi
from time import sleep
from wsgiref.simple_server import make_server
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
import httplib, urllib

PROTOCOL_VERSION = 0.1
QA_CARD_TYPE = 1
VICE_VERSA_CARD_TYPE = 2
N_SIDED_CARD_TYPE = 3


class Sync(object):
    """Main class driving sync."""

    def __init__(self, url):
        self.url = url
        self.client = self.server = None

    def start(self):
        """Start syncing."""

        print "Sync:start"
        if self.handshake():
            self.client.process_history(self.get_server_history(), \
                self.server.hw_id)
            #self.server.process_history(self.client.get_history(), \
            #    self.client.hw_id)
            #self.done()
        else:
            #FIXME: make exeption instead of print
            print "error in handshaking"

    def connect(self):
        """Init Server connection."""

        print "Sync:connect"
        #FIXME: replace "database" by real database
        transport = WSGI()
        self.server = Server(transport, self.url, "database")
        self.server.start()

    def handshake(self):
        """Start handshaking."""

        print "Sync:handshake"
        if not self.server:
            self.connect()
        if not self.client:
            #FIXME: replace "database" by real database
            self.client = Client("database")
        return self.client.handshake(self.server)

    def done(self):
        """Finish syncing."""

        self.client.done()
        self.server.done()
            

from mnemosyne.libmnemosyne.component import Component
from mnemosyne.libmnemosyne.loggers.sql_logger import SqlLogger as events
class EventManager:
    def __init__(self, database):
        self.database = database

    def set_sync_params(self, params):
        pass 

    def get_events(self):
        """Creates history in XML."""
        events = self.database.get_history_events()
        history = Element("history")
        for item in events:
            event = {'event': item[0], 'time': item[1], 'id': item[2]}
            subelement = SubElement(history, "event")
            event_id = SubElement(subelement, "event_id")
            event_id.text = event['event'].__str__()
            self.create_event_element(event, subelement)
        #return ElementTree.tostring(history)
        print ElementTree.tostring(history)

    def create_event_element(self, event, subelement):
        """Creates xml representation of event."""
        event_id = event['event']
        if event_id == events.ADDED_TAG or event_id == events.UPDATED_TAG \
            or event_id == events.DELETED_TAG:
            return self.create_tag_element(event, subelement)
        elif event_id == events.ADDED_FACT or event_id == events.UPDATED_FACT \
            or event_id == events.DELETED_FACT:
            return self.create_fact_element(event, subelement)
        elif event_id == events.ADDED_CARD or event_id == events.UPDATED_CARD \
            or event_id == events.DELETED_CARD:
            return self.create_card_element(event, subelement)
        elif event_id == events.ADDED_CARD_TYPE or event_id == events.UPDATED_CARD_TYPE \
            or event_id == events.DELETED_CARD_TYPE:
            return self.create_card_type_element(event, subelement)

    def create_tag_element(self, event, element):
        """XML element for *_tag events."""
        tag = self.database.get_tag_by_id(event['id'])
        tag_id = SubElement(element, 'id')
        tag_id.text = tag['id']
        tag_name = SubElement(element, 'name')
        tag_name.text = tag['name']
        tag_timestamp = SubElement(element, 'timestamp')
        tag_timestamp.text = tag['timestamp']

    def create_fact_element(self, event, element):
        """XML element for *_fact events."""
        fact = self.database.get_fact_by_id(event['id'])
        fact_card_type_id = SubElement(element, 'card_type_id')
        fact_card_type_id.text = fact['card_type_id']
        #fact_data = ...
        fact_timestamp = Subelement(element, 'timestamp')
        fact_timestamp.text = fact['timestamp']

    def create_card_element(self, event, element):
        """XML elemrnt for *.card events."""
        event_id = SubElement(element, "event_id")
        event_id.text = event['event'].__str__()

    def create_card_type_element(self, event, element):
        event_id = SubElement(element, "event_id")
        event_id.text = event['event'].__str__()

    def apply_event(self, event):
        print "EventManager:apply_event()"
        print event



class WSGI:
    DEFAULT_MIME = "xml/text"

    def start(self, service):
        self.service = service
        self.httpd = make_server('', 9999, self.wsgi_app)
        print "starting server..."
        self.httpd.serve_forever()

    def get_method(self, environ, service):
        """
        Checks for method existence in service
        and checks for right request params.
        """

        def compare_args(list1, list2):
            """Compares two lists or tuples."""
            for item in list1:
                if not item in list2:
                    return False
            return True

        method = (environ['REQUEST_METHOD'] + \
            '_'.join(environ['PATH_INFO'].split('/'))).lower()
        if hasattr(service, method) and callable(getattr(service, method)):
            args = cgi.parse_qs(environ['QUERY_STRING'])
            args = dict([(key, value[0]) for key, value in args.iteritems()])
            if getattr(service, method).func_code.co_argcount-1 == len(args) \
                and compare_args(args.keys(), getattr(service, method). \
                    func_code.co_varnames):                
                return '200 OK', self.DEFAULT_MIME, method, args
            else:
                return '400 Bad Request', "text/plain", None, None
        else:
            return '404 Not Found', "text/plain", None, None

    def wsgi_app(self, environ, start_response):
        """Simple Server wsgi application."""
        status, mime, method, args = self.get_method(environ, self.service)
        headers = [('Content-type', mime)]
        start_response(status, headers)
        if method:
            return getattr(self.service, method)(**args)
        else:
            return status



class Server:
    def __init__(self, transport, url, database):
        self.transport = transport
        self.url = url
        self.database = database
        self.eman = EventManager(database)
        self.hw_id = "server_hw_id"
        self.app_name = 'Mnemosyne'
        self.app_version = mnemosyne.version.version
        self.protocol_version = PROTOCOL_VERSION
        self.cardtypes = N_SIDED_CARD_TYPE
        self.upload_media = True
        self.read_only = False

    def start(self):
        """Activate server."""
        self.transport.start(self)

    def login(self, login, password):
        """Check client existence."""

        return True

    def get_sync_params(self):
        """Gets server specific params."""

        return {'app_name': self.app_name, 'app_ver': self.app_version, \
            'protocol_ver': self.protocol_version, 'cardtypes': self.cardtypes,
            'upload_media': self.upload_media, 'read_only': self.read_only }

    def get_sync_history(self):
        """Gets all history events after the last sync."""
        print "Server:get_sync_history"
        #print "param1 =", param1
        #print "param2 =", param2
        #return self.eman.get_events()
        data = [{'time': '111', 'event': '1', 'text': "text1"},
                {'time': '222', 'event': '2', 'text': "text2"},
                {'time': '333', 'event': '3', 'text': "text3"}]
        # FIXME: make this lazy
        yield "<history>"
        for i in data:
            item = ElementTree.Element("item")
            time = ElementTree.SubElement(item, "time")
            time.text = i['time']
            event = ElementTree.SubElement(item, "event")
            event.text = i['event']
            text = ElementTree.SubElement(item, "text")
            text.text = i['time']
            yield ElementTree.tostring(item)
            #sleep(2)
        yield "</history>"

    def process_history(self, events, partnerid):
        """Process every event and add it to database."""

        for event in events:
            self.eman.apply_event(event, partnerid)

    def done(self):
        """Mark in database that sync was completed successfull."""
        pass
   
