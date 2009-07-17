import sys
sys.path.insert(0, '../../')
from libSM2sync.sync import Sync


def main(argv):
    """Main."""

    sync = Sync(url=argv[1])
    sync.go()



if __name__ == "__main__":
    sys.exit(main(sys.argv))
