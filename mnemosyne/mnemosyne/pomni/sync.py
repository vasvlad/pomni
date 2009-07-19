import sys
sys.path.insert(0, '../../')
from libSM2sync.sync import Sync
from libSM2sync.sync import Server
from libSM2sync.sync import HttpWrapper




def main(argv):
    """Main."""

    #sync = Sync(url=argv[1])
    #sync.start()
    server = Server("url", "database")
    http = HttpWrapper(server)




if __name__ == "__main__":
    sys.exit(main(sys.argv))
