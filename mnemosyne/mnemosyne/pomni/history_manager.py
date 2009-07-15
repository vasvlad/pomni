# This class needs for getting events from history table,
# filter them and delete old events, save only the last
# event for each id.


class HistoryManager:
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
