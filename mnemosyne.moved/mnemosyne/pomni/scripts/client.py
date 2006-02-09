from xml.etree.cElementTree import Element, SubElement, iterparse

import socket
import StringIO

def parse_XML(fileobj): # Incrementally.
    context = iterparse(fileobj, events=("start", "end"))
    root = None
    for event, elem in context:
        if event == "start" and root is None:
            root = elem     # The first element is root
        if event == "end" and elem.tag == "record":
          #... process record elements ...
          root.clear()

import time   
if __name__ == "__main__":

    HOST, PORT = "localhost", 9999

    t1 = time.time()

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server
    sock.connect((HOST, PORT))
    # The number of cards we ask for.
    sock.send("10000\n")

    parse_XML(sock.makefile("r"))
        
    t2 = time.time()
    print t2-t1
