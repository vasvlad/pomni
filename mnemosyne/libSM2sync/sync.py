# vim: sw=4 ts=4 expandtab ai
#
# sync.py
#
# Max Usachev <maxusachev@gmail.com>, 
# Ed Bartosh <bartosh@gmail.com>, 
# Peter Bienstman <Peter.Bienstman@UGent.be>


import mnemosyne.version


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

        if self.handshake():
            self.client.process_history(self.server.get_history(), \
                self.server.hw_id)
            self.server.process_history(self.client.get_history(), \
                self.client.hw_id)
            self.done()
        else:
            #FIXME: make exeption instead of print
            print "error in handshaking"

    def connect(self):
        """Init Server connection."""

        #FIXME: replace "database" by real database
        self.server = Server(self.url, "database")
        self.server.connect()

    def handshake(self):
        """Start handshaking."""

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
            


class EventManager:
    def __init__(self, database):
        self.database = database

    def set_sync_params(self, params):
        pass

    def get_events(self):
        pass

    def apply_event(self, event):
        pass



class Client:
    def __init__(self, database):
        self.database = database
        self.eman = None
        self.hw_id = 'client_hw_id'
        self.app_name = 'Mnemosyne'
        self.app_version = mnemosyne.version.version
        self.protocol_version = PROTOCOL_VERSION
        self.login = 'mnemosyne'
        self.password = 'mnemosyne'
        self.cardtypes = N_SIDED_CARD_TYPE
        self.extradata = ''

    def handshake(self, server):
        """Handshaking with server."""

        if server.login(self.hw_id, self.login, self.password):
            self.eman = EventManager(self.database, server.get_sync_params())
            server.set_sync_params(self.get_sync_params())
            return True
        return False

    def get_history(self):
        """Gets all history events after the last sync."""

        return self.eman.get_events()

    def process_history(self, events, partnerid):
        """Process every event and add it to database."""

        for event in events:
            self.eman.apply_event(event, partnerid)

    def get_sync_params(self):
        """Gets client specific params."""

        return {'app_name': self.app_name, 'app_ver': self.app_version, \
            'protocol_ver': self.protocol_version, 'extra': self.extradata, \
            'cardtypes': self.cardtypes}

    def done(self):
        """Mark in database that sync was completed successfull."""
        pass
        



class Server:
    def __init__(self, url, database):
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

    def connect(self):
        """Activate server connection."""
        pass

    def login(self, login, password):
        """Check client existence."""

        return True

    def get_sync_params(self):
        """Gets server specific params."""

        return {'app_name': self.app_name, 'app_ver': self.app_version, \
            'protocol_ver': self.protocol_version, 'cardtypes': self.cardtypes,
            'upload_media': self.upload_media, 'read_only': self.read_only }

    def get_history(self):
        """Gets all history events after the last sync."""

        return self.eman.get_events()

    def process_history(self, events, partnerid):
        """Process every event and add it to database."""

        for event in events:
            self.eman.apply_event(event, partnerid)

    def done(self):
        """Mark in database that sync was completed successfull."""
        pass
    
