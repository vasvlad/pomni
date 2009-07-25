"""
Server.
"""

import cgi
import uuid
import mnemosyne.version
from urlparse import urlparse
from sync import EventManager
from wsgiref.simple_server import make_server
from sync import PROTOCOL_VERSION
from sync import N_SIDED_CARD_TYPE

class Server:
    """Base server class for syncing."""

    DEFAULT_MIME = "xml/text"

    def __init__(self, uri, database):
        params = urlparse(uri)
        self.host = params.scheme
        self.port = int(params.path)
        self.httpd = None
        self.eman = EventManager(database, None)
        self.hw_id = hex(uuid.getnode())
        self.app_name = 'Mnemosyne'
        self.app_version = mnemosyne.version.version
        self.protocol_version = PROTOCOL_VERSION
        self.cardtypes = N_SIDED_CARD_TYPE
        self.upload_media = True
        self.read_only = False

    def get_method(self, environ):
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
        if hasattr(self, method) and callable(getattr(self, method)):
            args = cgi.parse_qs(environ['QUERY_STRING'])
            args = dict([(key, value[0]) for key, value in args.iteritems()])
            if getattr(self, method).func_code.co_argcount-2 == len(args) \
                and compare_args(args.keys(), getattr(self, method). \
                    func_code.co_varnames):                
                return '200 OK', self.DEFAULT_MIME, method, args
            else:
                return '400 Bad Request', "text/plain", None, None
        else:
            return '404 Not Found', "text/plain", None, None

    def wsgi_app(self, environ, start_response):
        """Simple Server wsgi application."""

        status, mime, method, args = self.get_method(environ)
        headers = [('Content-type', mime)]
        start_response(status, headers)
        if method:
            return getattr(self, method)(environ, **args)
        else:
            return status

    def start(self):
        """Activate server."""

        self.httpd = make_server(self.host, self.port, self.wsgi_app)
        print "Server started at HOST:%s, PORT:%s" % (self.host, self.port)
        self.httpd.serve_forever()

    def login(self, login, password):
        """Check client existence."""

        return True

    def get_sync_params(self):
        """Gets server specific params."""

        return {'app_name': self.app_name, 'app_ver': self.app_version, \
            'protocol_ver': self.protocol_version, 'cardtypes': self.cardtypes,
            'upload_media': self.upload_media, 'read_only': self.read_only }

    def get_sync_history(self, environ):
        """Gets self history events."""

        #FIXME: replace "test" by real machine id
        return self.eman.get_history("test")

    def put_sync_history(self, environ):
        """Gets client history and applys to self."""

        socket = environ['wsgi.input']
        client_history = socket.readline()
        self.eman.apply_history(client_history)
        return "OK"

    def done(self):
        """Mark in database that sync was completed successfull."""

        pass
   
