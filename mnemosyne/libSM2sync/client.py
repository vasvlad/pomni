import mnemosyne.version
import httplib
from urlparse import urlparse
from sync import EventManager
from sync import PROTOCOL_VERSION, N_SIDED_CARD_TYPE


class Client:
    """Base client class for syncing."""

    def __init__(self, transport, database):
        self.transport = transport
        self.eman = EventManager(database)
        self.hw_id = 'client_hw_id'
        self.app_name = 'Mnemosyne'
        self.app_version = mnemosyne.version.version
        self.protocol_version = PROTOCOL_VERSION
        self.login = 'mnemosyne'
        self.password = 'mnemosyne'
        self.cardtypes = N_SIDED_CARD_TYPE
        self.extradata = ''

    def start(self):
        """Start syncing."""
        
        print "getting server history..."
        server_history = self.transport.get_history()
        print "applying server history to self..."
        self.eman.apply_history(server_history)
        # print "getting client history..."
        # client_history = self.eman.get_history()
        # print "sending client history..."

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

        return self.eman.get_history()

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
       


class HttpTransport:
    """Http transport for client."""

    def __init__(self, uri):
        params = urlparse(uri)
        self.host = params.scheme
        self.port = params.path
        print "HttpTransport: HSOT:%s, PORT:%s" % (self.host, self.port)

    def get_history(self):
        """Gets history from Server."""

        conn = httplib.HTTPConnection(self.host, self.port)
        conn.request('GET', '/sync/history')
        return conn.getresponse().read()
        #return urllib.urlopen("http://localhost:9999/sync/history")

        
