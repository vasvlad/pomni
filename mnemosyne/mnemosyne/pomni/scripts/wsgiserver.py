import time, random
from wsgiref.simple_server import make_server

def randstr(length):
    return ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') \
            for i in xrange(length)])

def generate_JSON(cards=10000):
    import simplejson
    for cardid in xrange(cards):
        data = [cardid, randstr(40), cardid, cardid,
            random.randint(1,5), str(2.5),random.randint(1,100), str(0), str(0), str(10),
            str(0.0), str(0.0), str(1), randstr(40), str(10), str(1), str(1), str(1),
            randstr(40), randstr(40)]
        yield "%s\n" % str(data)

def wsgi_application1(environ, start_response):
    cards = int(environ['PATH_INFO'].split('/')[1])
    print "%s asked for %d cards" % (environ['REMOTE_ADDR'], cards)
    start_response('200 OK', [('Content-Type', 'text/json')])
    t1 = time.time()
    length = 0
    for chunk in generate_JSON(cards):
        yield chunk
        length += len(chunk)
    print time.time()-t1
    print length

from wsgiref.simple_server import ServerHandler, WSGIRequestHandler

class MyServerHandler(ServerHandler):
    def run(self, application):
        """Invoke the application"""
        try:
            self.setup_environ()
            self.result = application(self.environ, self.start_response, 
                                        self.request_handler.rfile)
            self.finish_response()
        except:
            try:
                self.handle_error()
            except:
                # If we get an error handling an error, just give up already!
                self.close()
                raise   # ...and let the actual server figure it out.
 

class MyWSGIRequestHandler(WSGIRequestHandler):
    def handle(self):
        self.raw_requestline = self.rfile.readline()
        if not self.parse_request(): # An error code has been sent, just exit
            return

        handler = MyServerHandler(
            self.rfile, self.wfile, self.get_stderr(), self.get_environ()
        )
        
        handler.request_handler = self      # backpointer for logging
        handler.run(self.server.get_app())

def wsgi_application(environ, start_response, socket):
    import simplejson
    if environ['HTTP_TRANSFER_ENCODING'] == 'chunked':
        i = 0
        while True:
            size = socket.readline()
            if size == '0\r\n':
                break
            simplejson.loads(socket.readline())
            i += 1
            if socket.readline() != '\r\n':
                start_response('400 Bad Request', [('Content-Type', 'text/html')])
                return ["Wrong format of HTTP chunk\n\r"]

    start_response('200 OK', [('Content-Type', 'text/json')])
    return ["%d\n\r" % i]

httpd = make_server('', 9999, wsgi_application, handler_class=MyWSGIRequestHandler)
httpd.serve_forever()

