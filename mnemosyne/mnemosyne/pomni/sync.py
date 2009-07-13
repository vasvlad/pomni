from mnemosyne.libmnemosyne.database import Database
from mnemosyne.libmnemosyne.loggers.sql_logger import SqlLogger as events
import socket
import simplejson

class HistoryManager(Database):
    """
    Works with database history table.
    """

    def __init__(self, database, name):
        self.database = database
        self.name = name

    def get_history(self, server_events = []):
        """Returns filtered history events."""

        return self.filter_events(self.get_events(\
            self.database.get_history_events()) + server_events)

    def get_events(self, events):
        """Returns modified history events."""

        return [{"event":event[0], "time":event[1], "id":event[2], \
            "side":self.name} for event in events]

    def filter_events(self, events, filter = [None]):
        """Remove all old events. Save only the new ones."""

        result_list = []
        tmp_dict = {}
        # now dict looks like: { key:[], ... }
        for event in events:
            tmp_dict[event["id"]] = []

        # now dict looks like: { key:[event1, event2, ...], ...}
        for event in events:
            tmp_dict[event["id"]].append(event)

        # save only last event for every id
        for key in tmp_dict:
            last_event = tmp_dict[key][0]
            for event in tmp_dict[key][:]:
                if event["time"] > last_event["time"]:
                    last_event = event
                tmp_dict[key].remove(event)
            if key not in filter:
                result_list.append({"id":key, "event":last_event["event"], \
                    "time": last_event["time"], "side": last_event["side"]})

        return result_list

    def apply(self, event):
        """Modify database on self side."""

        event_id = event["event"]
        if event_id == events.ADDED_CARD:
            card = self.other_side.get_card_by_id(event["id"])
            self.add_card(card)
        elif event_id == events.DELETED_CARD:
            card = self.other_side.get_card_by_id(event["id"])
            self.delete_card(card)
        elif event_id == events.UPDATED_CARD:
            card = self.other_side.get_card_by_id(event["id"])
            self.update_card(card)



class Transport:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """Connects to server."""

        try:
            self.sock.connect((self.address, self.port))
            return True
        except:
            return False

    def send_command(self, command, data=None):
        """Send command and associated data to server."""

        if not self.sock:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connect()
        self.sock.send(command)
        if data:
            self.sock.send(data)
        return self.parse_JSON(self.sock.makefile('r'))

    def parse_JSON(self, fileobj):
        """Parses data from socket file object."""

        return simplejson.loads(fileobj.read())



class Client(HistoryManager):
    """Client class."""

    def __init__(self, database, transport=None):
        HistoryManager.__init__(self, database, "client")
        self.other_side = transport

    def sync(self):
        """Start syncing."""

        # get client and server filtered history
        events = self.get_history(self.other_side.send_command("history"))
        for event in events:
            print event

        # analize every event and apply it to appropriate side
        #for event in events:
        #    if event["side"] != self.name:
        #        self.apply(event)
        #    else:
        #        print "Client send event to Server via Transport..."
        #        self.other_side.apply(event)
       


class Server(HistoryManager):
    """Server class."""

    def __init__(self, database, transport=None):
        HistoryManager.__init__(self, database, "server")
        self.other_side = transport

    def handler(self):
        command, data = self.other_side.receive()
        if command == "get_card_by_id":
            card = self.database.get_card_by_id(data)
