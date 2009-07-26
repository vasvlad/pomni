"""
Client.
"""

import mnemosyne.version
import httplib
import uuid
from urlparse import urlparse
from sync import EventManager
from sync import PROTOCOL_VERSION, N_SIDED_CARD_TYPE


class Client:
    """Base client class for syncing."""

    def __init__(self, uri, database, controller):
        params = urlparse(uri)
        self.host = params.scheme
        self.port = params.path
        self.eman = EventManager(database, controller)
        self.hw_id = hex(uuid.getnode())
        self.app_name = 'Mnemosyne'
        self.app_version = mnemosyne.version.version
        self.protocol_version = PROTOCOL_VERSION
        self.login = 'mnemosyne'
        self.password = 'mnemosyne'
        self.cardtypes = N_SIDED_CARD_TYPE
        self.extradata = ''

    def start(self):
        """Start syncing."""
        
        #FIXME: replace by real machine id
        client_history = self.eman.get_history("test")
        server_history = self.get_server_history()
        print server_history
        #self.eman.apply_history(server_history)
        #self.send_history(client_history)

    def handshake(self, server):
        """Handshaking with server."""

        #if server.login(self.hw_id, self.login, self.password):
            #self.eman = EventManager(self.database, server.get_sync_params())
            #server.set_sync_params(self.get_sync_params())
            #return True
        #return False
        return True

    def get_server_history(self):
        """Connects to server and gets server history."""

        conn = httplib.HTTPConnection(self.host, self.port)
        conn.request('GET', '/sync/history')
        server_history = conn.getresponse().read()
        conn.close()
        return server_history

    def send_history(self, history):
        """Sends client history to server."""

        conn = httplib.HTTPConnection(self.host, self.port)
        conn.request('PUT', '/sync/history')
        conn.send(history)
        response = conn.getresponse().read()
        conn.close()
        return response
        
    def get_sync_params(self):
        """Gets client specific params."""

        return {'app_name': self.app_name, 'app_ver': self.app_version, \
            'protocol_ver': self.protocol_version, 'extra': self.extradata, \
            'cardtypes': self.cardtypes}

    def done(self):
        """Mark in database that sync was completed successfull."""
        pass
