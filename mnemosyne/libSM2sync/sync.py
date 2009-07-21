# vim: sw=4 ts=4 expandtab ai
#
# sync.py
#
# Max Usachev <maxusachev@gmail.com>, 
# Ed Bartosh <bartosh@gmail.com>, 
# Peter Bienstman <Peter.Bienstman@UGent.be>


import mnemosyne.version
import cgi
from wsgiref.simple_server import make_server
from urlparse import urlparse

PROTOCOL_VERSION = 0.1
QA_CARD_TYPE = 1
VICE_VERSA_CARD_TYPE = 2
N_SIDED_CARD_TYPE = 3


class Sync(object):
    """Main class driving sync."""

    def __init__(self, url):
        self.url = url
        self.client = self.server = None

    def start(self):
        """Start syncing."""

        print "Sync:start"
        if self.handshake():
            self.client.process_history(self.get_server_history(), \
                self.server.hw_id)
            #self.server.process_history(self.client.get_history(), \
            #    self.client.hw_id)
            #self.done()
        else:
            #FIXME: make exeption instead of print
            print "error in handshaking"

    def connect(self):
        """Init Server connection."""

        print "Sync:connect"
        #FIXME: replace "database" by real database
        transport = WSGI()
        self.server = Server(transport, self.url, "database")
        self.server.start()

    def handshake(self):
        """Start handshaking."""

        print "Sync:handshake"
        if not self.server:
            self.connect()
        if not self.client:
            #FIXME: replace "database" by real database
            self.client = Client("database")
        return self.client.handshake(self.server)

    def done(self):
        """Finish syncing."""

        self.client.done()
        self.server.done()
            

from mnemosyne.libmnemosyne.loggers.sql_logger import SqlLogger as events
class EventManager:
    def __init__(self, database):
        self.database = database

    def set_sync_params(self, params):
        pass 

    def get_history(self):
        """Creates history in XML."""
        history = "<history>"
        for item in self.database.get_history_events():
            event = {'event': item[0], 'time': item[1], 'id': item[2], \
                'interval': item[3], 'thinking': item[4]}
            history += self.create_event_element(event).__str__()
        history += "</history>"
        return history

    def create_event_element(self, event):
        """Creates xml representation of event."""
        event_id = event['event']
        if event_id == events.ADDED_TAG or event_id == events.UPDATED_TAG \
            or event_id == events.DELETED_TAG:
            return self.create_tag_element(event)
        elif event_id == events.ADDED_FACT or event_id == events.UPDATED_FACT \
            or event_id == events.DELETED_FACT:
            return self.create_fact_element(event)
        elif event_id == events.ADDED_CARD or event_id == events.UPDATED_CARD \
            or event_id == events.DELETED_CARD:
            return self.create_card_element(event)
        elif event_id == events.ADDED_CARD_TYPE or \
            event_id == events.UPDATED_CARD_TYPE or \
            event_id == events.DELETED_CARD_TYPE:
            return self.create_card_type_element(event)
        elif event_id == events.REPETITION:
            return self.create_repetition_element(event)
        else:
            return ''

    def create_tag_element(self, event):
        """XML element for *_tag events."""
        tag = self.database.get_tag_by_id(event['id'])
        return '<item><event>%s</event><id>%s</id><name>%s</name><time>%s' \
            '</time></item>' % (event['event'], event['id'], tag.name,
            event['time'])

    def create_fact_element(self, event):
        """XML element for *_fact events."""
        fact = self.database.get_fact_by_id(event['id'])
        factdata = ''
        for key, value in fact.data.items():
            factdata += "<%s>%s</%s>" % (key, value, key)
        return '<item><event>%s</event><cardtype_id>%s</cardtype_id>' \
            '<time>%s</time><fact_data>%s</fact_data></item>' % \
            (event['event'], fact.card_type.id, event['time'], factdata)

    def create_card_element(self, event):
        """XML element for *.card events."""
        card = self.database.get_card_by_id(event['id'])
        return '<item><event>%s</event><id>%s</id><cardtype_id>%s' \
            '</cardtype_id><tags>%s</tags><grade>%s</grade><easiness>%s' \
            '</easiness><lastrep>%s</lastrep><nextrep>%s</nextrep><factid>' \
            '%s</factid><factviewid>%s</factviewid><time>%s</time></event>' \
            '</item>' % (event['event'], card.id, card.fact.card_type.id, \
            ','.join([item.name for item in card.tags]), card.grade, \
            card.easiness, card.last_rep, card.next_rep, card.fact.id, \
            card.fact_view.id, event['time'])

    def create_card_type_element(self, event):
        #cardtype = self.database.get_cardtype(event['id'])
        return '<item><event>%s</event><id>%s</id></item>' % \
            (event['event'], event['id'])

    def create_repetition_element(self, event):
        card = self.database.get_card_by_id(event['id'])
        return '<item/><event>%s</event><id>%s</id><grade>%s</grade><easiness>'\
            '%s</easiness><newinterval>%s</newinterval><thinkingtime>%s' \
            '</thinkingtime><time>%s</time></item>' % (event['event'], card.id,\
            card.grade, card.easiness, event['interval'], event['thinking'],\
            event['time'])

    def apply_event(self, event):
        print "EventManager:apply_event()"
        print event

