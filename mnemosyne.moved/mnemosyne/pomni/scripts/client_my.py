import sys
import socket

def parse_XML(fileobj): # Incrementally.
    from xml.etree.cElementTree import iterparse
    context = iterparse(fileobj, events=("start", "end"))
    root = None
    for event, elem in context:
        if event == "start" and root is None:
            root = elem     # The first element is root
        if event == "end" and elem.tag == "record":
          #... process record elements ...
          root.clear()

def parse_JSON(fileobj):
   import simplejson
   for data in fileobj:
       simplejson.loads(data)

import time   
if __name__ == "__main__":

    HOST, PORT = "192.168.255.17", 9999

    t1 = time.time()

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server
    sock.connect((HOST, PORT))
    # The number of cards we ask for.
    sock.send("10000\n")

    if len(sys.argv) > 1 and sys.argv[1] == 'json':
        parse_JSON(sock.makefile("r"))
    else:
        parse_XML(sock.makefile("r"))
        
    t2 = time.time()
    print t2-t1
