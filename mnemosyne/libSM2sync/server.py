import cgi
import mnemosyne.version
from urlparse import urlparse
from sync import EventManager
from wsgiref.simple_server import make_server
from sync import PROTOCOL_VERSION
from sync import N_SIDED_CARD_TYPE


class WSGI:
    """WSGI service for Server."""

    DEFAULT_MIME = "xml/text"

    def __init__(self, uri):
        params = urlparse(uri)
        self.host = params.scheme
        self.port = int(params.path)
        self.service = None
        self.httpd = None

    def start(self, service):
        """Start server."""

        self.service = service
        self.httpd = make_server(self.host, self.port, self.wsgi_app)
        print "Starting server. HOST:%s, PORT:%s" % (self.host, self.port)
        self.httpd.serve_forever()

    def get_method(self, environ, service):
        """
        Checks for method existence in service
        and checks for right request params.
        """

        def compare_args(list1, list2):
            """Compares two lists or tuples."""
            for item in list1:
                if not item in list2:
                    return False
            return True

        method = (environ['REQUEST_METHOD'] + \
            '_'.join(environ['PATH_INFO'].split('/'))).lower()
        if hasattr(service, method) and callable(getattr(service, method)):
            args = cgi.parse_qs(environ['QUERY_STRING'])
            args = dict([(key, value[0]) for key, value in args.iteritems()])
            if getattr(service, method).func_code.co_argcount-1 == len(args) \
                and compare_args(args.keys(), getattr(service, method). \
                    func_code.co_varnames):                
                return '200 OK', self.DEFAULT_MIME, method, args
            else:
                return '400 Bad Request', "text/plain", None, None
        else:
            return '404 Not Found', "text/plain", None, None

    def wsgi_app(self, environ, start_response):
        """Simple Server wsgi application."""

        status, mime, method, args = self.get_method(environ, self.service)
        headers = [('Content-type', mime)]
        start_response(status, headers)
        if method:
            return getattr(self.service, method)(**args)
        else:
            return status



class Server:
    """Base server class for syncing."""

    def __init__(self, transport, database):
        self.transport = transport
        self.eman = EventManager(database)
        self.hw_id = "server_hw_id"
        self.app_name = 'Mnemosyne'
        self.app_version = mnemosyne.version.version
        self.protocol_version = PROTOCOL_VERSION
        self.cardtypes = N_SIDED_CARD_TYPE
        self.upload_media = True
        self.read_only = False

    def start(self):
        """Activate server."""

        self.transport.start(self)

    def login(self, login, password):
        """Check client existence."""

        return True

    def get_sync_params(self):
        """Gets server specific params."""

        return {'app_name': self.app_name, 'app_ver': self.app_version, \
            'protocol_ver': self.protocol_version, 'cardtypes': self.cardtypes,
            'upload_media': self.upload_media, 'read_only': self.read_only }

    def get_sync_history(self):
        """Gets all history events after the last sync."""

        print self.eman.get_history()

    def process_history(self, events, partnerid):
        """Process every event and add it to database."""

        for event in events:
            self.eman.apply_event(event, partnerid)

    def done(self):
        """Mark in database that sync was completed successfull."""
        pass
   
