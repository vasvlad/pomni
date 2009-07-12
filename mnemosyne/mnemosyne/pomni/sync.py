from mnemosyne.libmnemosyne.database import Database
from mnemosyne.libmnemosyne.loggers.sql_logger import SqlLogger as events


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

        result_list = []
        for event in events:
            if event[2]: # if id != None
                result_list.append({"event":event[0], "time":event[1], \
                    "id":event[2], "side":self.name})
        #print "get_events: result_list =", result_list
        return result_list

    def filter_events(self, events):
        """Remove all old events.Save only the new one."""

        result_dict = {}
        # now dict looks like: { key:[], ... }
        for event in events:
            result_dict[event["id"]] = []

        # now dict looks like: { key:[event1, event2, ...], ...}
        for event in events:
            result_dict[event["id"]].append(event)

        # save only last event for every id
        for key in result_dict:
            last_event = result_dict[key][0]
            for event in result_dict[key][:]:
                if event["time"] > last_event["time"]:
                    last_event = event
                result_dict[key].remove(event)
            result_dict[key] = {"time":last_event["time"], \
                "event":last_event["event"], "side":last_event["side"]}

        #print "filter events: result_dict =", result_dict
        return result_dict

    def apply(self, event):
        """Modify appropriate database."""

        if event["event"] == events.ADDED_CARD:
            self.add_card(self.other_side.get_card(event["id"]))




class Transport(HistoryManager):
    pass




class Client(HistoryManager):
    """Client class."""

    def __init__(self, database, transport=None):
        HistoryManager.__init__(self, database, "client")
        self.other_side = transport
        #self.sync()

    def sync(self):
        """Start syncing."""

        # get client and server filtered history
        events = self.hmanager.get_history(\
            self.other_side.get_events())

        # analize every event and applay it to appropriate side
        for event in events:
            if event["side"] != self.name:
                self.apply(event)
            else:
                self.other_side.apply(event)
        



class Server:
    """Server class."""

    def __init__(self, database, transport=None):
        HistoryManager.__init__(self, database, "server")
        self.other_side = transport

