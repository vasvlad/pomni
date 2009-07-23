# vim: sw=4 ts=4 expandtab ai
#
# sync.py
#
# Max Usachev <maxusachev@gmail.com>, 
# Ed Bartosh <bartosh@gmail.com>, 
# Peter Bienstman <Peter.Bienstman@UGent.be>

from mnemosyne.libmnemosyne.tag import Tag
from mnemosyne.libmnemosyne.fact import Fact
from mnemosyne.libmnemosyne.loggers.sql_logger import SqlLogger as events

import copy
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
        """
        if self.handshake():
            self.client.process_history(self.get_server_history(), \
                self.server.hw_id)
            self.server.process_history(self.client.get_history(), \
                self.client.hw_id)
            self.done()
        else:
            #FIXME: make exeption instead of print
            print "error in handshaking"
        """

    def connect(self):
        """Init Server connection."""

        print "Sync:connect"

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
    """
    Class for manipulatig with client/server database:
    reading/writing history events, generating/parsing
    XML representation of history events.
    """

    def __init__(self, database, controller):
        # controller - mnemosyne.default_controller
        self.controller = controller
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
        """Creates XML representation of event."""

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
            return ''   # No need XML for others events. ?

    def create_tag_element(self, event):
        """Creates XML element for *_tag events."""

        tag = self.database.get_tag_by_id(event['id'])
        return '<item><type>tag</type><event>%s</event><id>%s</id><name>%s' \
            '</name><time>%s</time></item>' % (event['event'], event['id'], \
            tag.name, event['time'])

    def create_fact_element(self, event):
        """Creates XML element for *_fact events."""

        fact = self.database.get_fact_by_id(event['id'])
        factdata = ''
        for key, value in fact.data.items():
            factdata += "<%s>%s</%s>" % (key, value, key)
        return '<item><type>fact</type><event>%s</event><cardtype_id>%s' \
            '</cardtype_id><time>%s</time><fact_data>%s</fact_data><id>' \
            '%s</id></item>' % (event['event'], fact.card_type.id, \
            event['time'], factdata, fact.id)

    def create_card_element(self, event):
        """Creates XML element for *_card events."""

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
        """Creates XML element for *_card_type events."""

        #cardtype = self.database.get_cardtype(event['id'])
        return '<item><type>cardtype</type><event>%s</event><id>%s</id>' \
        '</item>' % (event['event'], event['id'])

    def create_repetition_element(self, event):
        """Creates XML element for repetition event."""

        card = self.database.get_card_by_id(event['id'])
        return '<item><type>repetition</type><event>%s</event><id>%s</id>' \
            '<grade>%s</grade><easiness>%s</easiness><newinterval>%s' \
            '</newinterval><thinkingtime>%s</thinkingtime><time>%s</time>' \
            '</item>' % (event['event'], card.id, card.grade, card.easiness, \
            event['interval'], event['thinking'], event['time'])

    #FIXME: this is modified add_new_cards function from default_controller
    def add_card(self, fact, card_type, grade, tags):
        if grade in [0,1]:
            raise AttributeError, "Use -1 as grade for unlearned cards."
        db = self.database
        duplicates = db.duplicates_for_fact(fact)
        #db.add_fact(fact)
        for card in card_type.create_related_cards(fact):
            if grade >= 2:
                #self.scheduler().set_initial_grade(card, grade)
                print 'sheduling'
            db.add_card(card)  
        merged_fact_data = copy.copy(fact.data)
        for duplicate in duplicates:
            for key in fact_data:
                if key not in card_type.required_fields():
                    merged_fact_data[key] += " / " + duplicate[key]
            db.delete_fact_and_related_data(duplicate)
        #fact.data = merged_fact_data
        #self.component_manager.get_current("edit_fact_dialog")\
        #  (fact, self.component_manager, allow_cancel=False).activate()
        #return
        #db.add_fact(fact)
        #cards = []
        #for card in card_type.create_related_cards(fact):
        #    #self.log().added_card(card)
        #    #if grade >= 2:
        #    #    self.scheduler().set_initial_grade(card, grade)
        #    card.tags = tags
        #    db.add_card(card)
        #    cards.append(card)
        db.save()
        #if self.review_controller().learning_ahead == True:
        #    self.review_controller().reset()
        #return cards # For testability.

    def apply_history(self, history):
        """Parses XML history and apply it to database."""

        for element in ElementTree.fromstring(history).findall('item'):
            event = int(element.find('event').text)
            obj = self.create_object_from_xml(element)
            if event == events.ADDED_FACT:
                if not self.database.has_fact_with_data(\
                    obj.data, obj.card_type):
                    self.database.add_fact(obj)
            elif event == events.UPDATED_FACT:
                self.database.update_fact(obj)
            elif event == events.DELETED_FACT:
                self.database.delete_fact_and_related_data(obj)
            elif event == events.ADDED_TAG:
                if not obj.name in self.database.tag_names():
                    self.database.add_tag(obj)
            elif event == events.UPDATED_TAG:
                self.database.update_tag(obj)
            elif event == events.DELETED_TAG:
                self.database.delete_tag(obj)
            elif event == events.ADDED_CARD:
                #FIXME
                self.add_card(obj.fact, obj.fact.card_type, obj.grade, obj.tags)
            elif event == events.UPDATED_CARD:
                # FIXME
                print "apdating card"
            elif event == events.DELETED_CARD:
                self.database.delete_card(obj)
            elif event == events.REPETITION:
                print "repetition"

    def create_object_from_xml(self, item):
        """Creates real object from XML Element."""
        
        obj_type = item.find('type').text
        if obj_type == 'fact':
            card_type = self.database.get_card_type( \
                item.find('cardtype_id').text)
            fact_data = dict([(key, item.find('fact_data').find(key).text) \
                for key, value in card_type.fields])
            creation_time = item.find('time').text
            fact_id = item.find('id').text
            return Fact(fact_data, card_type, creation_time, fact_id)
        elif obj_type == 'card':
            class DictClass(dict):
                pass
            card = DictClass()
            card.fact = self.database.get_fact_by_id(item.find('factid').text)
            tags = set(self.database.get_or_create_tag_with_name(tag_name) \
                for tag_name in item.find('tags').text.split(','))
            card.tags = tags
            card.grade = int(item.find('grade').text)
            return card
        elif obj_type == 'tag':
            return Tag(item.find('name').text, item.find('id').text)
        elif obj_type == 'cardtype':
            print "parsing cardtype from xml"
        elif obj_type == 'repetition':
            print 'repetition'
        return ""


