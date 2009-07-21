# vim: sw=4 ts=4 expandtab ai
#
# sync.py
#
# Max Usachev <maxusachev@gmail.com>, 
# Ed Bartosh <bartosh@gmail.com>, 
# Peter Bienstman <Peter.Bienstman@UGent.be>

from mnemosyne.libmnemosyne.tag import Tag
from mnemosyne.libmnemosyne.fact import Fact
from mnemosyne.libmnemosyne.card import Card
from mnemosyne.libmnemosyne.loggers.sql_logger import SqlLogger as events

from xml.etree import ElementTree

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
            


class EventManager:
    def __init__(self, database):
        self.database = database
        """
        self.action_dict = {
            events.ADDED_TAG: self.database.add_tag,
            events.UPDATED_TAG: self.database.update_tag,
            events.DELETED_TAG: self.database.delete_tag,
            events.ADDED_FACT: self.database.add_fact,
            events.UPDATED_FACT: self.database.update_fact,
            events.DELETED_FACT: self.database.delete_fact_and_related_data,
            events.ADDED_CARD: self.database.add_card,
            events.UPDATED_CARD: self.database.update_card,
            events.DELETED_CARD: self.database.delete_card,
            events.ADDED_CARD_TYPE: self.databse.add_card_type,
            events.UPDATED_CARD_TYPE: self.databse.update_card_type,
            events.DELETED_CARD_TYPE: self.database.delete_card_type,
        }
        """

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
        return '<item><type>tag</type><event>%s</event><id>%s</id><name>%s' \
            '</name><time>%s</time></item>' % (event['event'], event['id'], \
            tag.name, event['time'])

    def create_fact_element(self, event):
        """XML element for *_fact events."""

        fact = self.database.get_fact_by_id(event['id'])
        factdata = ''
        for key, value in fact.data.items():
            factdata += "<%s>%s</%s>" % (key, value, key)
        return '<item><type>fact</type><event>%s</event><cardtype_id>%s' \
            '</cardtype_id><time>%s</time><fact_data>%s</fact_data></item>' % \
            (event['event'], fact.card_type.id, event['time'], factdata)

    def create_card_element(self, event):
        """XML element for *_card events."""

        card = self.database.get_card_by_id(event['id'])
        return '<item><type>card</type><event>%s</event><id>%s</id>' \
            '<cardtype_id>%s</cardtype_id><tags>%s</tags><grade>%s</grade>' \
            '<easiness>%s</easiness><lastrep>%s</lastrep><nextrep>%s' \
            '</nextrep><factid>%s</factid><factviewid>%s</factviewid><time>' \
            '%s</time></item>' % (event['event'], card.id, \
            card.fact.card_type.id, ','.join([item.name for item in card.tags]),
            card.grade, card.easiness, card.last_rep, card.next_rep, \
            card.fact.id, card.fact_view.id, event['time'])
        
    def create_card_type_element(self, event):
        """XML element for *_card_type events."""

        #cardtype = self.database.get_cardtype(event['id'])
        return '<item><type>cardtype</type><event>%s</event><id>%s</id>' \
        '</item>' % (event['event'], event['id'])

    def create_repetition_element(self, event):
        """XML elemnt for repetition event."""

        card = self.database.get_card_by_id(event['id'])
        return '<item><type>repetition</type><event>%s</event><id>%s</id><grade>%s' \
            '</grade><easiness>%s</easiness><newinterval>%s</newinterval>' \
            '<thinkingtime>%s</thinkingtime><time>%s</time></item>' % \
            (event['event'], card.id, card.grade, card.easiness, \
            event['interval'], event['thinking'], event['time'])

    def apply_history(self, history):
        """Parses XML history and apply it to database."""

        for element in ElementTree.fromstring(history).findall('item'):
            event = int(element.find('event').text)
            obj = self.create_object_from_xml(element)
            #if event != events.REPETITION:
            #    self.action_dict[event](obj)
            #else:
            #    self.database.update_card(obj, repetition_only=True)

    def create_object_from_xml(self, item):
        """Cretaes real object from XML Element."""
        
        obj_type = item.find('type').text
        if obj_type == 'fact':
            cardtype = self.database.get_card_type( \
                item.find('cardtype_id').text)
            data = dict([(key, item.find('fact_data').find(key).text) \
                for key, value in cardtype.fields])
            creation_time = item.find('time').text
            return Fact(data, cardtype, creation_time)
        elif obj_type == 'card':
            fact = self.database.get_fact_by_id(item.find('factid').text)
            factview = None
            card = Card(fact, factview)
            card.id = item.find('id').text
            card.tags = set(item.find('tags').text.split('/'))
            card.grade = item.find('grade').text
            card.easiness = item.find('easiness').text
            card.last_rep = item.find('lastrep').text
            card.next_rep = item.find('nextrep').text
            return card
        elif obj_type == 'tag':
            return Tag(item.find('name').text, item.find('id').text)
        elif obj_type == 'cardtype':
            print "parsing cardtype from xml"
        elif obj_type == 'repetition':
            print 'repetition'
        return ""


