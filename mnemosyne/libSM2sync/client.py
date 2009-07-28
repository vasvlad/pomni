"""
Client.
"""

import mnemosyne.version
import httplib
import base64
import urllib2
import uuid
from urlparse import urlparse
from sync import EventManager
from sync import PROTOCOL_VERSION, N_SIDED_CARD_TYPE


class Client:
    """Base client class for syncing."""

    def __init__(self, uri, database, controller, config):
        #FIXME: remove from init. 
        self.config = config
        self.database = database
        self.uri = uri
        params = urlparse(uri)
        self.host = params.scheme
        self.port = params.path
        self.backup_file = None
        self.eman = EventManager(database, controller)
        self.id = hex(uuid.getnode())
        self.name = 'Mnemosyne'
        self.version = mnemosyne.version.version
        self.deck = 'default'
        self.protocol = PROTOCOL_VERSION
        self.cardtypes = N_SIDED_CARD_TYPE
        self.extra = ''

    def start(self):
        """Start syncing."""
        
        if self.login():
            self.handshake()
            #server_history = self.get_server_history()
            #self.backup_file = self.database.make_sync_backup()
            #self.eman.apply_history(server_history)
            #client_history = self.eman.get_history()
            #self.send_history(client_history)
        else:
            #FIXME: replace by Error Dialog.
            print "Authentification: wrong login or password!"

    def login(self):
        """Logs on the server."""
        
        base64string = base64.encodestring("%s:%s" % (self.config['user_id'], \
            self.config['user_passwd']))[:-1]
        authheader =  "Basic %s" % base64string
        #FIXME: it necessary for localhost
        if not self.uri.startswith("http://"):
            uri = "http://" + self.uri
        else:
            uri = self.uri
        request = urllib2.Request(uri)
        request.add_header("AUTHORIZATION", authheader)
        try:
            response = urllib2.urlopen(request)
        except IOError, exception:
            print exception
            return False
        else: 
            print response.read()
            return True

    def handshake(self):
        """Handshaking with server."""

        conn = httplib.HTTPConnection(self.host, self.port)
        conn.request('GET', '/sync/server/params')
        server_params = conn.getresponse().read()
        client_params = "<params><client id='%s' name='%s' ver='%s' " \
            "protocol='%s' deck='%s' cardtypes='%s' extra='%s'/></params>\n" \
            % (self.id, self.name, self.version, self.protocol, self.deck, \
            self.cardtypes, self.extra)
        conn.request('PUT', '/sync/client/params')
        conn.send(client_params)
        conn.close()
        self.eman.set_sync_params(server_params)

    def set_params(self, params):
        """Uses for setting non-default params."""

        for key in params.keys():
            setattr(self, key, params[key])

    def get_server_history(self):
        """Connects to server and gets server history."""

        conn = httplib.HTTPConnection(self.host, self.port)
        conn.request('GET', '/sync/server/history')
        server_history = conn.getresponse().read()
        conn.close()
        return server_history

    def send_history(self, history):
        """Sends client history to server."""

        conn = httplib.HTTPConnection(self.host, self.port)
        conn.request('PUT', '/sync/client/history')
        conn.send(history)
        response = conn.getresponse().read()
        conn.close()
        return response
        
    def done(self):
        """Finishes sync."""
        
        import os
        os.remove(self.backup_file)
