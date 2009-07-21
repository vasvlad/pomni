import sys
import os
sys.path.insert(0, '../../')
sys.path.insert(0, "../")
from libSM2sync.server import Server
from libSM2sync.server import WSGI
from libSM2sync.client import Client
from libSM2sync.client import HttpTransport
from pomni.factory import app_factory

def main(argv):
    """Main."""

    if len(argv) < 3:
        print "USAGE: %s MODE HOST:PORT" % argv[0]
    else:
        mode = argv[1]
        uri = argv[2]
        if mode == "server":
            app = app_factory()
            app.initialise(os.path.abspath(os.path.join(os.getcwdu(), ".pomni")))
            database = app.database()
            transport = WSGI(uri)
            server = Server(transport, database)
            server.start()
            app.finalise()
        elif mode == "client":
            transport = HttpTransport(uri)
            client = Client(transport, "database")
            client.start()
        else:
            print "unknown mode"


if __name__ == "__main__":
    sys.exit(main(sys.argv))
