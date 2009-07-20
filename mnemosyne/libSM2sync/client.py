from sync import PROTOCOL_VERSION, N_SIDED_CARD_TYPE
from sync import EventManager
import mnemosyne.version
import httplib, urlparse, urllib
from xml.etree.cElementTree import iterparse
from xml.etree.ElementTree import parse

class Client:
    def __init__(self, transport):
        self.database = "database"
        self.hw_id = 'client_hw_id'
        self.app_name = 'Mnemosyne'
        self.app_version = mnemosyne.version.version
        self.protocol_version = PROTOCOL_VERSION
        self.login = 'mnemosyne'
        self.password = 'mnemosyne'
        self.cardtypes = N_SIDED_CARD_TYPE
        self.extradata = ''
        self.eman = EventManager(self.database)
        self.transport = transport

    def handshake(self, server):
        """Handshaking with server."""

        #if server.login(self.hw_id, self.login, self.password):
            #self.eman = EventManager(self.database, server.get_sync_params())
            #server.set_sync_params(self.get_sync_params())
            #return True
        #return False
        return True

    def get_history(self):
        """Gets all client history events after the last sync."""

        return self.eman.get_events()

    def parse_server_history(self, fileobj):
        """Parses xml history to single events."""
        context = iterparse(fileobj)
        for event, element in context:
            return (event, element)
            #    #return "1"
    
    def process_server_history(self):
        """Gets history from server and process it."""

        print "client:process_history()"
        history = self.transport.get_history()
        print history
        #for event in self.parse_server_history(self.transport.get_history):
            #self.eman.apply_event(event)
            #print event

    def get_sync_params(self):
        """Gets client specific params."""

        return {'app_name': self.app_name, 'app_ver': self.app_version, \
            'protocol_ver': self.protocol_version, 'extra': self.extradata, \
            'cardtypes': self.cardtypes}

    def done(self):
        """Mark in database that sync was completed successfull."""
        pass
        

class HttpService:
    """Http service for client."""

    def __init__(self, uri):
        params = urlparse.urlparse(uri)
        self.host = params.scheme
        self.port = params.path
        print "httpservice: host = %s, port = %s" % (self.host, self.port)

    def get_history(self):
        print "httpservice:get_history()"
        conn = httplib.HTTPConnection(self.host, self.port)
        conn.request('GET', '/sync/history')
        return conn.getresponse().read()
        #return urllib.urlopen("http://localhost:9999/sync/history")

        
