import sys
import random
import time 
from datetime import datetime
import SocketServer

class MyTCPHandler(SocketServer.StreamRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "%s asked for %d cards" % (self.client_address[0], int(self.data))
        # send those cards
        t1 = time.time()
        length = 0
        for chunk in generate_JSON(cards=int(self.data)):
            self.request.send(chunk)
            length += len(chunk)
        print time.time()-t1
        print length

def randstr(length):
    return ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') \
        for i in xrange(length)])

def generate_JSON(cards=10):
    import simplejson
    for cardid in xrange(cards):
        data = [cardid, randstr(40), cardid, cardid, 
            random.randint(1,5), str(2.5),random.randint(1,100), str(0), str(0), str(10),
            str(0.0), str(0.0), str(1), randstr(40), str(10), str(1), str(1), str(1), 
            randstr(40), randstr(40)]
        yield "%s\n" % simplejson.dumps(data)

if __name__ == "__main__":
    server = SocketServer.TCPServer(("192.168.255.17", 9999), MyTCPHandler)
    server.serve_forever()
