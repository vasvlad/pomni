from mnemosyne.libmnemosyne.database import Database
from mnemosyne.libmnemosyne.loggers.sql_logger import SqlLogger as events
import socket
import simplejson
from pomni.history_manager import HistoryManager


class Transport:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        #self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """Connects to server."""

        try:
            self.sock.connect((self.address, self.port))
            return True
        except:
            return False

    def send_command(self, command, data=None):
        """Send command and associated data to server."""

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.address, self.port))
        sock.send(command)
        if data:
            sock.send(data)
        result = self.parse_JSON(sock.makefile('r'))
        sock.close()
        return result

    def parse_JSON(self, fileobj):
        """Parses data from socket file object."""

        return simplejson.loads(fileobj.read())

    def apply(self, event):
        pass



class Client(HistoryManager):
    """Client class."""

    def __init__(self, database, transport=None):
        HistoryManager.__init__(self, database, "client")
        self.other_side = transport

    def sync(self):
        """Start syncing."""

        # get client and server filtered history
        events = self.get_history(self.other_side.send_command("history"))

        # analize every event and apply it to appropriate side
        for event in events:
            print event
            if event["side"] != self.name:
                self.apply(event)
            else:
                self.other_side.apply(event)
      
    def apply(self, event):
        """Update database on self side."""

        event_id = event["event"]
        if event_id == events.ADDED_CARD:
            card_fields = self.other_side.send_command('get_card', event['id'])
            # create card object
            # self.add_card(card)
            print "client: adding new card:", card_fields
        elif event_id == events.DELETED_CARD:
            #card = self.get_card_by_id(event['id'])
            #self.delete_card(card)
            print "client: deleting card with id:", event['id']
        elif event_id == events.UPDATED_CARD:
            card_fields = self.other_side.send_command('get_card', event['id'])
            # create card object
            # self.update_card(card)
            print "client: updating card:", card_fields
        elif event_id == events.ADDED_FACT:
            fact = self.other_side.send_command('get_fact', event['id'])
            # self.add_fact(fact)
            print "client: adding new fact:", fact
        elif event_id == events.DELETED_FACT:
            fact = self.other_side.send_command('get_fact', event['id'])
            # self.delete_fact_and_related_data(fact)
            print "client: deleting fact:", fact
        elif event_id == events.UPDATED_FACT:
            fact = self.other_side.send_command('get_fact', event['id'])
            # self.update_fact(fact)
            print "client: updating fact:", fact
        elif event_id == events.ADDED_TAG:
            tag = self.other_side.send_command('get_tag', event['id'])
            # self.add_tag(tag)
            print "client: adding new tag:", tag
        elif event_id == events.DELETED_TAG:
            tag = self.other_side.send_command('get_tag', event['id'])
            # self.delete_tag(tag)
            print "client: deleting tag:", tag
        elif event_id == events.UPDATED_TAG:
            tag = self.other_side.send_command('get_tag', event['id'])
            # self.update_tag(tag)
            print "client: updating tag:", tag
        elif event_id == events.ADDED_CARD_TYPE:
            card_type = self.other_side.send_command('get_card_type', event['id'])
            # self.add_card_type(card_type)
            print "client: adding new card_type:", card_type
        elif event_id == events.DELETED_CARD_TYPE:
            card_type = self.other_side.send_command('get_card_type', event['id'])
            # self.delete_card_type(card_type)
            print "client: deleting card_type:", card_type
        elif event_id == events.UPDATED_CARD_TYPE:
            card_type = self.other_side.send_command('get_card_type', event['id'])
            # self.update_card_type(card_type)
            print "client: updating card_type:", card_type
            
        


class Server(HistoryManager):
    """Server class."""

    def __init__(self, database, transport=None):
        HistoryManager.__init__(self, database, "server")
        self.other_side = transport

    def handler(self):
        command, data = self.other_side.receive()
        if command == "get_card_by_id":
            card = self.database.get_card_by_id(data)
