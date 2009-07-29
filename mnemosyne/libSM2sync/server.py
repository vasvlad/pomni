"""
Server.
"""

import cgi
import uuid
import base64
import mnemosyne.version
from urlparse import urlparse
from sync import EventManager
from wsgiref.simple_server import make_server
from sync import PROTOCOL_VERSION
from sync import N_SIDED_CARD_TYPE

class Server:
    """Base server class for syncing."""

    DEFAULT_MIME = "xml/text"

    def __init__(self, uri, database, config):
        params = urlparse(uri)
        #FIXME: move from here
        self.config = config
        self.database = database
        self.host = params.scheme
        self.port = int(params.path)
        self.httpd = None
        self.logged = False
        self.eman = EventManager(database, None)
        self.id = hex(uuid.getnode())
        self.name = 'Mnemosyne'
        self.version = mnemosyne.version.version
        self.protocol = PROTOCOL_VERSION
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

        if environ.has_key('HTTP_AUTHORIZATION'):
            clogin, cpasswd = base64.decodestring(\
                environ['HTTP_AUTHORIZATION'].split(' ')[-1]).split(':')
            if clogin == self.config['login'] and \
                cpasswd == self.config['user_passwd']:
                self.logged = True
                status = '200 OK'
            else:
                status = '403 Forbidden'
            return status, "text/plain", None, None
        else:
            if not self.logged:
                return '403 Forbidden', "text/plain", None, None
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

    def set_params(self, params):
        """Uses for setting non-default params."""

        for key in params.keys():
            setattr(self, key, params[key])

    def get_sync_server_params(self, environ):
        """Gets server specific params and sends it to client."""

        return "<params><server id='%s' name='%s' ver='%s' protocol='%s' " \
            "cardtypes='%s' upload='%s' readonly='%s'/></params>" % (self.id, \
            self.name, self.version, self.protocol, self.cardtypes, \
            self.upload_media, self.read_only)

    def put_sync_client_params(self, environ):
        """Gets client specific params."""

        try:
            socket = environ['wsgi.input']
            client_params = socket.readline()
        except:
            return "CANCEL"
        else:
            self.eman.set_sync_params(client_params)
            return "OK"

    def get_sync_server_history(self, environ):
        """Gets self history events."""

        return self.eman.get_history()

    def put_sync_client_history(self, environ):
        """Gets client history and applys to self."""

        try:
            socket = environ['wsgi.input']
            client_history = socket.readline()
        except:
            return "CANCEL"
        else:
            old_file, backuped_file = self.database.make_sync_backup()
            self.eman.apply_history(client_history)
            import os
            os.remove(self.backup_file)
            self.logged = False
            return "OK"
