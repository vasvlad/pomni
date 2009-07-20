import sys
sys.path.insert(0, '../../')
from libSM2sync.sync import Sync
from libSM2sync.sync import Server
from libSM2sync.sync import EventManager
from libSM2sync.client import Client
from libSM2sync.client import HttpService
from libSM2sync.sync import WSGI

def main(argv):
    """Main."""

    #sync = Sync(url=argv[1])
    #sync.start()
    #server = Server("url", "database")
    #http = HttpWrapper(server)
    mode = argv[1]
    if mode == "server":
        transport = WSGI()
        server = Server(transport, "url", "database")
        server.start()
    elif mode == "client":
        transport = HttpService("localhost:9999")
        client = Client(transport)
        client.process_server_history()
    else:
        print "unknown mode"




if __name__ == "__main__":
    sys.exit(main(sys.argv))
