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

    def __init__(self, uri, database, controller, config, log):
        #FIXME: remove from init. 
        self.config = config
        self.database = database
        self.log = log
        self.uri = uri
        self.eman = EventManager(database, log, controller, self.config.mediadir(), self.get_media_file)
        self.login = ''
        self.passwd = ''
        self.id = hex(uuid.getnode())
        self.name = 'Mnemosyne'
        self.version = mnemosyne.version.version
        self.deck = 'default'
        self.protocol = PROTOCOL_VERSION
        self.cardtypes = N_SIDED_CARD_TYPE
        self.extra = ''
        self.messenger = None
        self.progress_bar_updater = None
        self.stopped = False

    def set_user(self, login, passwd):
        """Sets user login and password."""

        self.login, self.passwd = login, passwd

    def test(self):
        import time
        size = 5
        for i in range(size):
            if self.stopped:
                return
            time.sleep(1)
            value = (i+1) / float(size)
            self.progress_bar_updater(value)
        self.progress_bar_updater(0)

    def set_messenger(self, messenger):
        """Sets UI messenger."""

        self.messenger = messenger

    def set_progress_bar_updater(self, progress_bar_updater):
        """Sets UI ProgressBar updater."""

        self.progress_bar_updater = progress_bar_updater

    def start(self):
        """Start syncing."""
       
        try:
            self.login()
            self.handshake()
            server_history = self.get_server_history()
            #client_history = self.eman.get_history()
            self.database.make_sync_backup()
            self.eman.apply_history(server_history)
            #self.send_client_history(client_history)
        except SyncError, exception:
            print exception #FIXME: replace by ErrorDialog
            self.database.restore_sync_backup()
        else:
            self.database.remove_sync_backup()
            print "Finished."

    def stop(self):
        self.stopped = True
        print "stopped"

    def login(self):
        """Logs on the server."""
        
        base64string = base64.encodestring("%s:%s" % \
            (self.login, self.passwd))[:-1]
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
            response = urllib2.urlopen(PutRequest(\
                self.uri + '/sync/client/params', cparams))
            if response.read() != "OK":
                raise SyncError("Handshaking: error on server side.")
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
            response = urllib2.urlopen(PutRequest(\
                self.uri + '/sync/client/history', history))
            if response.read() != "OK":
                raise SyncError("Sending client history: error on server side.")
        except urllib2.URLError, error:
            raise SyncError("Sending client history: " + str(error))

    def get_media_file(self, fname):
        """Gets media from server."""

        try:
            response = urllib2.urlopen(\
                self.uri + '/sync/server/media?fname=%s' % fname)
            data = response.read()
            if data != "CANCEL":
                fobj = open(os.path.join(self.config.mediadir(), fname), 'w')
                fobj.write(data)
                fobj.close()
        except urllib2.URLError, error:
            raise SyncError("Getting server media: " + str(error))

    def send_media_file(self, fname):
        """Sends media to server."""

        mfile = open(fname, 'r')
        data = mfile.read()
        mfile.close()

        try:
            request = PutRequest(self.uri + '/sync/client/media?fname=%s' % \
                os.path.basename(fname), data)
            request.add_header('CONTENT_LENGTH', len(data))
            response = urllib2.urlopen(request)
            if response.read() != "OK":
                raise SyncError("Sending client media: error on server side.")
        except urllib2.URLError, error:
            raise SyncError("Sending client media: " + str(error))
