import sys
import os
sys.path.insert(0, '../../')
sys.path.insert(0, "../")
from libSM2sync.server import Server
from libSM2sync.client import Client
from maemo_ui.factory import app_factory

def main(argv):
    """Main."""

    if len(argv) < 3:
        print "USAGE: %s MODE HOST:PORT" % argv[0]
    else:
        mode = argv[1]
        uri = argv[2]
        if mode == "server":
            app = app_factory()
            app.initialise(os.path.abspath(os.path.join(os.getcwdu(), ".mnemosyne")))
            database = app.database()
            server = Server(uri, database, app.config())
            server.start()
            app.finalise()
        elif mode == "client":
            app = app_factory()
            app.initialise(os.path.abspath(os.path.join(os.getcwdu(), "testdb")))
            database = app.database()
            client = Client(uri, database, app.controller(), app.config())
            client.start()
            app.finalise()
        else:
            print "unknown mode"


if __name__ == "__main__":
    sys.exit(main(sys.argv))
