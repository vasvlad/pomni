import sys
sys.path.insert(0, '../../')
from libSM2sync.server import Server
from libSM2sync.server import WSGI
from libSM2sync.client import Client
from libSM2sync.client import HttpTransport

def main(argv):
    """Main."""

    if len(argv) < 3:
        print "USAGE: %s MODE HOST:PORT" % argv[0]
    else:
        mode = argv[1]
        uri = argv[2]
        if mode == "server":
            transport = WSGI(uri)
            server = Server(transport, "database")
            server.start()
        elif mode == "client":
            transport = HttpTransport(uri)
            client = Client(transport, "database")
            client.start()
        else:
            print "unknown mode"


if __name__ == "__main__":
    sys.exit(main(sys.argv))
