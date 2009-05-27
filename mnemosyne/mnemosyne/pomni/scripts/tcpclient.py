import sys
import socket

def parse_JSON(fileobj):
   import simplejson
   for data in fileobj:
       simplejson.loads(data)

import time   
if __name__ == "__main__":
    t1 = time.time()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("192.168.255.17", 9999))
    # The number of cards we ask for.
    sock.send("10000\n")
    parse_JSON(sock.makefile("r"))
    print time.time()-t1
