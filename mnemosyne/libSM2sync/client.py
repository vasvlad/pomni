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
            self.config.mediadir(), self.get_media_file, \
            self.update_progressbar, events_updater)
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

            self.update_status("Backuping...")
            self.database.make_sync_backup()

            server_media_count = self.get_server_media_count()
            if server_media_count:
                self.update_status("Getting media from server. Please, wait...")
                server_media_history = self.get_media_history()
                self.eman.apply_media(server_media_history, server_media_count)

            client_media_count = self.eman.get_media_count()
            if client_media_count:
                self.update_status("Sending client media. Please, wait...")
                client_media_history = self.eman.get_media_history()
                self.send_client_media(client_media_history, client_media_count)

            server_history_length = self.get_server_history_length()
            server_cards_history = ''
            if server_history_length:
                self.update_status(\
                    "Getting history from server. Please, wait...")
                server_cards_history = self.get_server_history(\
                    server_history_length)
                #self.eman.apply_history(server_cards_history, server_history_length)

            client_history_length = self.eman.get_history_length()
            if client_history_length:
                self.update_status("Sending client history. Please, wait...")
                client_cards_history = self.eman.get_history()
                self.send_client_history(\
                    client_cards_history, client_history_length)
    
            if server_history_length:
                self.update_status("Applying server history. Please, wait...")
                self.eman.apply_history(\
                    server_cards_history, server_history_length)

            self.send_finish_request()

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
        """Stops syncing."""

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
            urllib2.urlopen(request).read()
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
            self.eman.update_partnerships_table()

    def set_params(self, params):
        """Uses for setting non-default params."""

        for key in params.keys():
            setattr(self, key, params[key])

    def get_server_media_count(self):
        """Gets number of media files to recieve."""

        if self.stopped:
            return
        self.update_events()
        try:
            return int(urllib2.urlopen(\
                self.uri + '/sync/server/history/media/count').read())
        except urllib2.URLError, error:
            raise SyncError("Getting server media count: " + str(error))

    def get_server_history_length(self):
        """Gets server history length."""

        if self.stopped:
            return
        self.update_events()
        try:
            return int(urllib2.urlopen(\
                self.uri + '/sync/server/history/length').read())
        except urllib2.URLError, error:
            raise SyncError("Getting server history length: " + str(error))

    def get_server_history(self, history_length):
        """Connects to server and gets server history."""

        if self.stopped:
            return
        self.update_events()
        count = 0
        hsize = float(history_length + 2)
        try:
            #return urllib2.urlopen(self.uri + '/sync/server/history')
            response = urllib2.urlopen(self.uri + '/sync/server/history')
            shistory = ''
            chunk = ''
            while chunk != "</history>\n":
                chunk = response.readline()
                shistory += chunk
                count += 1
                self.update_progressbar(count / hsize)
            import StringIO
            return StringIO.StringIO(shistory)
        except urllib2.URLError, error:
            raise SyncError("Getting server history: " + str(error))

    def get_media_history(self):
        """Gets media history from server."""

        if self.stopped:
            return
        self.update_events()
        try:
            return urllib2.urlopen(self.uri + '/sync/server/mediahistory'). \
                readline()
        except urllib2.URLError, error:
            raise SyncError("Getting server media history: " + str(error))
       
    def send_client_history(self, history, history_length):
        """Sends client history to server."""

        if self.stopped:
            return
        self.update_events()
        chistory = ''
        for chunk in history:
            chistory += chunk
        data = str(history_length) + '\n' + chistory + '\n'
        try:
            response = urllib2.urlopen(PutRequest(\
                self.uri + '/sync/client/history', data))
            if response.read() != "OK":
                raise SyncError("Sending client history: error on server side.")
        except urllib2.URLError, error:
            raise SyncError("Sending client history: " + str(error))

    def send_client_media(self, history, media_count):
        """Sends client media to server."""

        if self.stopped:
            return
        count = 0
        hsize = float(media_count)
        for child in ElementTree.fromstring(history).findall('i'):
            fname = child.find('id').text.split('__for__')[0]
            self.send_media_file(fname)
            count += 1
            self.update_progressbar(count / hsize)

    def send_finish_request(self):
        """Say to server thar sync is finished."""

        if self.stopped:
            return
        try:
            response = urllib2.urlopen(self.uri + '/sync/finish')
            if response.read() != "OK":
                raise SyncError("Finishing sync: error on server side.")
        except urllib2.URLError, error:
            raise SyncError("Finishing syncing: " + str(error))
        else:
            self.eman.update_last_sync_event()

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
