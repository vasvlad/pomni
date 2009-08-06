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
from sync import UIMessenger
from sync import PROTOCOL_VERSION, N_SIDED_CARD_TYPE
from xml.etree import ElementTree


#Overrides get_method method for using PUT request in urllib2
class PutRequest(urllib2.Request):
    def get_method(self):
        return "PUT"


class Client(UIMessenger):
    """Base client class for syncing."""

    def __init__(self, uri, database, controller, config, log, messenger, \
            events_updater, status_updater, progress_updater):
        UIMessenger.__init__(self, messenger, events_updater, status_updater, \
            progress_updater)
        self.config = config
        self.database = database
        self.log = log
        self.uri = uri
        self.eman = EventManager(database, log, controller, \
            self.config.mediadir(), self.get_media_file, self.update_progressbar)
        self.login = ''
        self.passwd = ''
        self.id = hex(uuid.getnode())
        self.name = 'Mnemosyne'
        self.version = mnemosyne.version.version
        self.deck = 'default'
        self.protocol = PROTOCOL_VERSION
        self.cardtypes = N_SIDED_CARD_TYPE
        self.extra = ''
        self.stopped = False

    def set_user(self, login, passwd):
        """Sets user login and password."""

        self.login, self.passwd = login, passwd

    def start(self):
        """Start syncing."""
       
        try:
            self.update_status("Authorization...")
            self.login_()
            self.update_status("Handshaking...")
            self.handshake()
            self.update_status("Getting history from server. Please, wait...")
            server_history = self.get_server_history()
            self.update_status("Getting self history. Please, wait...")
            client_history = self.eman.get_history()
            self.update_status("Backuping...")
            self.database.make_sync_backup()
            self.update_status("Applying server history...")
            self.eman.apply_history(server_history)
            self.update_status("Sending client media. Please, wait...")
            self.send_client_media(client_history)
            self.update_status("Sending client history. Please, wait...")
            self.send_client_history(client_history)
            if self.stopped:
                raise SyncError("Aborted!")
        except SyncError, exception:
            self.show_message("Error: " + str(exception))
            self.update_status("Restoring backuped databse. Please, wait...")
            self.database.restore_sync_backup()
        else:
            self.update_status("Removing backup database...")
            self.database.remove_sync_backup()
            self.show_message("Finished!")

    def stop(self):
        self.stopped = True
        self.eman.stop()

    def login_(self):
        """Logs on the server."""
        
        self.update_events()
        base64string = base64.encodestring("%s:%s" % \
            (self.login, self.passwd))[:-1]
        authheader =  "Basic %s" % base64string
        request = urllib2.Request(self.uri)
        request.add_header("AUTHORIZATION", authheader)
        try:
            urllib2.urlopen(request, timeout=5)
        except urllib2.URLError, error:
            if hasattr(error, 'code'):
                if error.code == 403:
                    raise SyncError(\
                        "Authentification failed: wrong login or password!")
            else:
                raise SyncError(str(error.reason))

    def handshake(self):
        """Handshaking with server."""
    
        if self.stopped:
            return
        self.update_events()
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

        if self.stopped:
            return
        self.update_events()
        try:
            return urllib2.urlopen(self.uri + '/sync/server/history').read()
        except urllib2.URLError, error:
            raise SyncError("Getting server history: " + str(error))
       
    def send_client_history(self, history):
        """Sends client history to server."""

        if self.stopped:
            return
        self.update_events()
        try:
            response = urllib2.urlopen(PutRequest(\
                self.uri + '/sync/client/history', history))
            if response.read() != "OK":
                raise SyncError("Sending client history: error on server side.")
        except urllib2.URLError, error:
            raise SyncError("Sending client history: " + str(error))

    def send_client_media(self, history):
        """Sends client media to server."""

        if self.stopped:
            return
        self.update_events()
        for child in ElementTree.fromstring(history).findall('i'):
            if child.find('t').text == 'media':
                fname = child.find('id').text.split('__for__')[0]
                self.send_media_file(fname)

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

        mfile = open(os.path.join(self.config.mediadir(), fname), 'r')
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
