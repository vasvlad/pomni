#!/usr/bin/python -tt7
# vim: sw=4 ts=4 expandtab ai

############# SimpleJSONRPCServer ##############  
import simplejson
import SocketServer
import sys
import traceback
try:
    import fcntl
except ImportError:
    fcntl = None

import SimpleXMLRPCServer

class SimpleJSONRPCDispatcher(SimpleXMLRPCServer.SimpleXMLRPCDispatcher):
    def _marshaled_dispatch(self, data, dispatch_method = None):
        id = None
        try:
            req = simplejson.loads(data)
            method = req['method']
            params = req['params']
            id     = req['id']

            if dispatch_method is not None:
                result = dispatch_method(method, params)
            else:
                result = self._dispatch(method, params)
            response = dict(id=id, result=result, error=None)
        except:
            extpe, exv, extrc = sys.exc_info()
            err = dict(type=str(extpe),
                       message=str(exv),
                       traceback=''.join(traceback.format_tb(extrc)))
            response = dict(id=id, result=None, error=err)
        try:
            return simplejson.dumps(response)
        except:
            extpe, exv, extrc = sys.exc_info()
            err = dict(type=str(extpe),
                       message=str(exv),
                       traceback=''.join(traceback.format_tb(extrc)))
            response = dict(id=id, result=None, error=err)
            return simplejson.dumps(response)


class SimpleJSONRPCRequestHandler(SimpleXMLRPCServer.SimpleXMLRPCRequestHandler):
    # Class attribute listing the accessible path components;
    # paths not on this list will result in a 404 error.
    rpc_paths = ('/', '/JSON')

class SimpleJSONRPCServer(SocketServer.TCPServer,
                          SimpleJSONRPCDispatcher):
    """Simple JSON-RPC server.

    Simple JSON-RPC server that allows functions and a single instance
    to be installed to handle requests. The default implementation
    attempts to dispatch JSON-RPC calls to the functions or instance
    installed in the server. Override the _dispatch method inhereted
    from SimpleJSONRPCDispatcher to change this behavior.
    """

    allow_reuse_address = True

    def __init__(self, addr, requestHandler=SimpleJSONRPCRequestHandler,
                 logRequests=True):
        self.logRequests = logRequests

        SimpleJSONRPCDispatcher.__init__(self, allow_none=True, encoding=None)
        SocketServer.TCPServer.__init__(self, addr, requestHandler)

        # [Bug #1222790] If possible, set close-on-exec flag; if a
        # method spawns a subprocess, the subprocess shouldn't have
        # the listening socket open.
        if fcntl is not None and hasattr(fcntl, 'FD_CLOEXEC'):
            flags = fcntl.fcntl(self.fileno(), fcntl.F_GETFD)
            flags |= fcntl.FD_CLOEXEC
            fcntl.fcntl(self.fileno(), fcntl.F_SETFD, flags)

###
### Client code
###
import xmlrpclib

class ResponseError(xmlrpclib.ResponseError):
    pass
class Fault(xmlrpclib.ResponseError):
    pass

def _get_response(file, sock):
    data = ""
    while 1:
        if sock:
            response = sock.recv(1024)
        else:
            response = file.read(1024)
        if not response:
            break
        data += response

    file.close()

    return data

class Transport(xmlrpclib.Transport):
    def _parse_response(self, file, sock):
        return _get_response(file, sock)

class SafeTransport(xmlrpclib.SafeTransport):
    def _parse_response(self, file, sock):
        return _get_response(file, sock)

class ServerProxy:
    def __init__(self, uri, id=None, transport=None, use_datetime=0):
        # establish a "logical" server connection

        # get the url
        import urllib
        type, uri = urllib.splittype(uri)
        if type not in ("http", "https"):
            raise IOError, "unsupported JSON-RPC protocol"
        self.__host, self.__handler = urllib.splithost(uri)
        if not self.__handler:
            self.__handler = "/JSON"

        if transport is None:
            if type == "https":
                transport = SafeTransport(use_datetime=use_datetime)
            else:
                transport = Transport(use_datetime=use_datetime)

        self.__transport = transport
        self.__id        = id

    def __request(self, methodname, params):
        # call a method on the remote server

        request = simplejson.dumps(dict(id=self.__id, method=methodname,
                                    params=params))

        data = self.__transport.request(
            self.__host,
            self.__handler,
            request,
            verbose=False
            )

        response = simplejson.loads(data)

        if response["id"] != self.__id:
            raise ResponseError("Invalid request id (is: %s, expected: %s)" \
                                % (response["id"], self.__id))
        if response["error"] is not None:
            raise Fault("JSON Error", response["error"])
        return response["result"]

    def __repr__(self):
        return (
            "<ServerProxy for %s%s>" %
            (self.__host, self.__handler)
            )

    __str__ = __repr__

    def __getattr__(self, name):
        # magic method dispatcher
        return xmlrpclib._Method(self.__request, name)


##################################################################
import sys
import random

from datetime import datetime

def randstr(length):
    return ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') \
        for i in xrange(length)])

class SyncEntity(list):
    def __init__(self, decks, total, packsize, compression):
        list.__init__(self)
        self.extend(decks)
        self.packsize = int(packsize)
        self.compression = int(compression)
        self.total = int(total)

    def genChunks(self):
        for cardid in xrange(self.total):
            yield {'_id': cardid, 'id': randstr(40), '_fact_id': cardid, 'fact_view_id': cardid,
                'grade': random.randint(1,5), 'easiness': 2.5, 'acq_reps': random.randint(1,100),
                'ret_reps': 0, 'lapses': 0, 'acq_reps_since_lapse': 10,
                'last_rep': 0.0, 'next_rep': 0.0, 'unseen': 1,
                'extra_data': randstr(40), 'seen_in_this_session': 10,
                'needs_sync': 1, 'active': 1, 'in_view': 1, 
                'facts': [{'_id': fact_id, 'id': randstr(36), 'card_type_id': random.randint(1,3),
                      'creation_date': str(datetime.now()),
                      'modification_date': str(datetime.now()),
                      'needs_sync': 1, 'key': 'qa'[random.randint(0,1)],
                      'value': randstr(200)} for fact_id in [0, 1]]}


    def genPayload(self):
        chunks = 0
        pack = []
        for chunk in self.genChunks():
            pack.append(chunk)
            chunks += 1
            if chunks >= self.packsize:
                yield pack
                chunks = 0
                pack = []
        if chunks:
            yield pack

class SyncServer(SyncEntity):
    def __init__(self, protocol, address, port, decks, total, packsize, compression):
        SyncEntity.__init__(self, decks, total, packsize, compression)
        self.address = address
        self.port = port
        self.protocol = protocol
        if protocol == 'xml-rpc':
            from SimpleXMLRPCServer import SimpleXMLRPCServer
            server = SimpleXMLRPCServer((address, port), allow_none=True)
        elif protocol == 'json-rpc':
            #from SimpleJsonRPCServer import SimpleJSONRPCServer as Server
            server = SimpleJSONRPCServer((address, port))
        else:
            raise RuntimeException("Unknown RPC protocol: %s" % protocol)
        
        server.register_function(self.applyPayload)
        server.register_function(self.append)
        server.register_function(self.__contains__)
        self.server = server

    def serve(self):
        self.server.serve_forever()

    def applyPayload(self, payload):
        print 'Got pack of %d items' % len(payload) 

class SyncClient(SyncEntity):
    def __init__(self, protocol, server_url, decks, total, packsize, compression):
        SyncEntity.__init__(self, decks, total, packsize, compression)
        self.server_url = server_url
        self._connection = None
        self.protocol = protocol

    @property
    def connection(self):
        if not self._connection:
            if self.protocol == 'xml-rpc':
                import xmlrpclib
                self._connection = xmlrpclib.Server(self.server_url)
            elif self.protocol == 'json-rpc':
                self._connection = ServerProxy(self.server_url)
            else:
                raise RuntimeException("Unknown RPC protocol: %s" % self.protocol)

        return self._connection

def server(proto, host, port, deck, total, packsize, compression):
    server = SyncServer(proto, host, int(port), [deck], total, packsize, compression)
    server.serve()

def client(proto, server_url, deck, total, packsize, compression):
    
    client = SyncClient(proto, server_url, [deck], total, packsize, compression)
    server = client.connection

    # create deck on server if needed
    if deck not in server:
        server.append(deck)

    for payload in client.genPayload():
        server.applyPayload(payload)

if __name__ == "__main__":
    sys.exit(globals()[sys.argv[1]](*sys.argv[2:]))

# Local Variables:
# mode: python
# py-indent-offset: 4
# indent-tabs-mode nil
# tab-width 4
# End:
