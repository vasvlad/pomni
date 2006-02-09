from xml.etree.cElementTree import Element, SubElement, tostring
import random
import time 
from datetime import datetime

import SocketServer

class MyTCPHandler(SocketServer.StreamRequestHandler):
    
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "%s asked for %d cards" % (self.client_address[0], int(self.data))
        # send those cards
        t1 = time.time()
        data = create_XML(cards=int(self.data))
        t2 = time.time()
        print t2-t1
        print len(data)
        self.request.send(data)


def randstr(length):
    return ''.join([random.choice('abcdefghijklmnopqrstuvwxyz') \
        for i in xrange(length)])

def create_XML(cards=10):
    data = "<mnemosyne>"
    root = Element("mnemosyne")
    for cardid in xrange(cards):
        data += """<card _fact_id="%s" _id="%s" acq_reps="%s" acq_reps_since_lapse="%s" active="%s" easiness="%s" extra_data="%s" fact_view_id="%s" grade="%s" id="%s" in_view="%s" lapses="%s" last_rep="%s" needs_sync="%s" next_rep="%s" ret_reps="%s" seen_in_this_session="%s" unseen="%s"><q>%s</q><a>%s</a></card>""" % (cardid, randstr(40), cardid, cardid,
                    random.randint(1,5), str(2.5), random.randint(1,100),
                    str(0), str(0), str(10),
                    str(0.0), str(0.0), str(1),
                    randstr(40), str(10),
                    str(1), str(1), str(1), randstr(40), randstr(40))
    data += "</mnemosyne>"
    return data


if __name__ == "__main__":
    HOST, PORT = "192.168.255.17", 9999

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
