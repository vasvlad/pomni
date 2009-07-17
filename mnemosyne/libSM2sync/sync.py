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

    def go(self):
        if self.handshake():
            self.client.process_history(self.server.get_history(), self.server.id)
            self.server.process_history(self.client.get_history(), self.client.id)
        else:
            print "error in handshaking"

    def connect(self):
        self.server = Server(self.url, "database")
        self.server.connect()

    def handshake(self):
        if not self.server:
            self.connect()
        if not self.client:
            self.client = Client("database")
        return self.client.handshake(self.server)
            


class EventManager:
    def __init__(self, database):
        self.database = database

    def set_sync_params(self, params):
        pass

    def get_events(self):
        pass

    def apply_events(self, event):
        pass



class Client:
    def __init__(self, database):
        self.database = database
        self.eman = None

    def handshake(self, server):
        sync_params = self.get_sync_params()
        if server.login(sync_params['login'], sync_params['password']):
            self.eman = EventManager(self.database, server.get_sync_params())
            server.set_sync_params(sync_params)
            return True
        return False

    def get_history(self):
        return self.eman.get_events()

    def process_history(self, events, partnerid):
        for event in events:
            self.eman.apply_event(event, partnerid)

    def get_sync_params(self):
        params = {}
        params['app_name'] = 'Mnemosyne'
        params['app_version'] = mnemosyne.version.version
        params['protocol_version'] = PROTOCOL_VERSION
        params['login'] = 'mnemosyne'
        params['password'] = 'mnemosyne'
        params['cardtypes'] = N_SIDED_CARD_TYPE
        params['extradata'] = ''
        return params
        


class Server:
    def __init__(self, url, database):
        self.url = url
        self.database = database
        self.eman = EventManager(database)

    def connect(self):
        pass

    def login(self, login, password):
        return True

    def get_sync_params(self):
        params = {}
        params['app_name'] = 'Mnemosyne'
        params['app_version'] = mnemosyne.version.version
        params['protocol_version'] = PROTOCOL_VERSION
        params['cardtypes'] = N_SIDED_CARD_TYPE
        params['upload_media'] = True
        params['read_only'] = False
        return params

    def get_history(self):
        return eman.get_events()

    def process_history(self, events, partnerid):
        for event in events:
            self.eman.apply_event(event, partnerid)
