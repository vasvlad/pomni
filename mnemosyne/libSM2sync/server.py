"""
Server.
"""

import os
import cgi
import uuid
import base64
import select
import mnemosyne.version
from urlparse import urlparse
from sync import EventManager
from sync import UIMessenger
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler
from sync import PROTOCOL_VERSION
from sync import N_SIDED_CARD_TYPE


class MyWSGIServer(WSGIServer):
    """Redefined WSGIServer class."""

    def __init__(self, host, port, app, handler_class=WSGIRequestHandler):
        WSGIServer.__init__(self, (host, port), handler_class)
        self.set_app(app)
        self.stopped = False
        self.update_events = None
        self.timeout = 1

    def stop(self):
        """Stops server."""

        self.stopped = True
        
    def serve_forever(self):
        """Starts  request handling."""

        while not self.stopped:
            self.update_events()
            if select.select([self.socket], [], [], self.timeout)[0]:
                self.handle_request()
            
       

class Server(UIMessenger):
    """Base server class for syncing."""

    DEFAULT_MIME = "xml/text"

    def __init__(self, uri, database, config, log, messenger, events_updater, \
                     status_updater, progress_updater):
        UIMessenger.__init__(self, messenger, events_updater, status_updater, \
                                progress_updater)
        params = urlparse(uri)
        self.host = params.scheme
        self.port = int(params.path)
        self.database = database
        self.config = config
        self.log = log
        self.eman = EventManager(self.database, self.log, None, \
            self.config.mediadir(), None, self.update_progressbar)
        self.httpd = MyWSGIServer(self.host, self.port, self.wsgi_app)
        self.httpd.update_events = events_updater
        self.login = None
        self.passwd = None
        self.logged = False
        self.id = hex(uuid.getnode())
        self.name = 'Mnemosyne'
        self.version = mnemosyne.version.version
        self.protocol = PROTOCOL_VERSION
        self.cardtypes = N_SIDED_CARD_TYPE
        self.upload_media = True
        self.read_only = False

    def set_user(self, login, passwd):
        """Sets server login and password."""

        self.login = login
        self.passwd = passwd

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
            if clogin == self.login and cpasswd == self.passwd:
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
                args = dict([(key, val[0]) for key, val in args.iteritems()])
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

        self.update_status("Waiting for client connection...")
        print "Server started at HOST:%s, PORT:%s" % (self.host, self.port)
        self.httpd.serve_forever()

    def stop(self):
        """Stops Server."""

        self.httpd.stop()
        self.eman.stop()

    def set_params(self, params):
        """Uses for setting non-default params."""

        for key in params.keys():
            setattr(self, key, params[key])

    def get_sync_server_params(self, environ):
        """Gets server specific params and sends it to client."""

        self.update_status("Sending server params to client...")
        return "<params><server id='%s' name='%s' ver='%s' protocol='%s' " \
            "cardtypes='%s' upload='%s' readonly='%s'/></params>" % (self.id, \
            self.name, self.version, self.protocol, self.cardtypes, \
            self.upload_media, self.read_only)

    def put_sync_client_params(self, environ):
        """Gets client specific params."""

        self.update_status("Receiving client params...")
        try:
            socket = environ['wsgi.input']
            client_params = socket.readline()
        except:
            return "CANCEL"
        else:
            self.eman.set_sync_params(client_params)
            return "OK"

    def get_sync_server_history_media_count(self, environ):
        """Gets self media files count."""

        return str(self.eman.get_media_count())

    def get_sync_server_history_length(self, environ):
        """Gets length of self history."""

        return str(self.eman.get_history_length())

    def get_sync_server_history(self, environ):
        """Gets self history events."""

        self.update_status("Sending history to client...")
        return self.eman.get_history()

    def put_sync_client_history(self, environ):
        """Gets client history and applys to self."""

        self.update_status("Receiving client history...")
        try:
            socket = environ['wsgi.input']
            client_history = socket.readline()
        except:
            return "CANCEL"
        else:
            self.update_status("Backuping...")
            self.database.make_sync_backup()
            self.update_status("Applying client history...")
            self.eman.apply_history(client_history)
            self.update_status("Remove backup history...")
            self.database.remove_sync_backup()
            self.database.con.commit()
            self.logged = False
            self.stop()
            self.show_message("Finished!")
            return "OK"

    def get_sync_server_media(self, environ, fname):
        """Gets server media file and sends it to client."""

        self.update_status("Sending media to client...")
        try:
            mediafile = open(os.path.join(self.config.mediadir(), fname))
            data = mediafile.read()
            mediafile.close()
        except:
            return "CANCEL"
        else:
            return data

    def put_sync_client_media(self, environ, fname):
        """Gets client media and applys to self."""

        self.update_status("Receiving client media...")
        try:
            socket = environ['wsgi.input']
            size = int(environ['CONTENT_LENGTH'])
            data = socket.read(size)
        except:
            return "CANCEL"
        else:
            mfile = open(os.path.join(self.config.mediadir(), fname), 'w')
            mfile.write(data)
            mfile.close()
            return "OK"

