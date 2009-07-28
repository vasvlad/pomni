"""
Client.
"""

import mnemosyne.version
import base64
import urllib2
import uuid
import os
from sync import SyncError
from sync import EventManager
from sync import PROTOCOL_VERSION, N_SIDED_CARD_TYPE


#Overrides get_method method for using PUT request in urllib2
class PutRequest(urllib2.Request):
    def get_method(self):
        return "PUT"


class Client:
    """Base client class for syncing."""

    def __init__(self, uri, database, controller, config):
        #FIXME: remove from init. 
        self.config = config
        self.database = database
        self.uri = uri
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
       
        try:
            self.login()
            self.handshake()
            #server_history = self.get_server_history()
            self.backup_file = self.database.make_sync_backup()
            #self.eman.apply_history(server_history)
            #client_history = self.eman.get_history()
            #self.send_client_history(client_history)
        except SyncError, exception:
            #FIXME: replace by ErrorDialog
            print exception
            # move backed database back
        else:
            os.remove(self.backup_file)

    def login(self):
        """Logs on the server."""
        
        base64string = base64.encodestring("%s:%s" % (self.config['user_id'], \
            self.config['user_passwd']))[:-1]
        authheader =  "Basic %s" % base64string
        request = urllib2.Request(self.uri)
        request.add_header("AUTHORIZATION", authheader)
        try:
            urllib2.urlopen(request)
        except urllib2.URLError, error:
            if hasattr(error, 'code'):
                if error.code == 403:
                    raise SyncError(\
                        "Authentification failed: wrong login or password!")
            else:
                raise SyncError(str(error.reason))

    def handshake(self):
        """Handshaking with server."""

        cparams = "<params><client id='%s' name='%s' ver='%s' protocol='%s'" \
            " deck='%s' cardtypes='%s' extra='%s'/></params>\n" % (self.id, \
            self.name, self.version, self.protocol, self.deck, self.cardtypes, \
            self.extra)
        try:
            sparams = urllib2.urlopen(self.uri + '/sync/server/params').read()
            urllib2.urlopen(PutRequest(\
                self.uri + '/sync/client/params', cparams))
        except urllib2.URLError, error:
            raise SyncError("Handshaking: " + str(error))
        else:
            self.eman.set_sync_params(sparams)

    def set_params(self, params):
        """Uses for setting non-default params."""

        for key in params.keys():
            setattr(self, key, params[key])

    def get_server_history(self):
        """Connects to server and gets server history."""

        try:
            return urllib2.urlopen(self.uri + '/sync/server/history').read()
        except urllib2.URLError, error:
            raise SyncError("Getting server history: " + str(error))
        
    def send_client_history(self, history):
        """Sends client history to server."""

        try:
            urllib2.urlopen(PutRequest(\
                self.uri + '/sync/client/history', history))
        except urllib2.URLError, error:
            raise SyncError("Sending client history: " + str(error))
