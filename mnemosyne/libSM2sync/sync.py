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
        print history
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
        tag = self.database.get_tag_by_id(event['id'])
        return "<tag ev='%s' id='%s' name='%s'/>" % \
            (event['event'], tag.id, tag.name)

    def create_fact_element(self, event):
        fact = self.database.get_fact_by_id(event['id'])
        dkeys = ','.join(["%s" % key for key,val in fact.data.items()])
        dvalues = ' '.join(["dv%s='%s'" % (num, fact.data.values()[num]) \
            for num in range(len(fact.data))])
        return "<fact ev='%s' id='%s' ctid='%s' dk='%s' %s tm='%s'/>" % \
            (event['event'], fact.id, fact.card_type.id, dkeys, dvalues, \
            event['time'])

    def create_card_element(self, event):
        card = self.database.get_card_by_id(event['id'])
        return "<card ev='%s' id='%s' ctid='%s' fid='%s' fvid='%s'" \
            " tags='%s' gr='%s' e='%s' lr='%s' nr='%s' tm='%s'/>" % \
            (event['event'], card.id, card.fact.card_type.id, card.fact.id, \
            card.fact_view.id, ','.join([item.name for item in card.tags]), \
            card.grade, card.easiness, card.last_rep, card.next_rep, \
            event['time'])
        
    def create_card_type_element(self, event):
        cardtype = self.database.get_cardtype(event['id'])
        fields = [key for key,value in cardtype.fields]
        return "<ctype ev='%s' id='%s' name='%s' f='%s' uf='%s' ks='%s'" \
            " edata='%s'/>" % (event['event'], cardtype.id, cardtype.name, \
            ','.join(fields), ','.join(cardtype.unique_fields), '', '')

    def create_repetition_element(self, event):
        card = self.database.get_card_by_id(event['id'])
        return "<rep ev='%s' id='%s' gr='%s' e='%s' nint='%s' thtm='%s'" \
            " tm='%s'/>" % (event['event'], card.id, card.grade, card.easiness,\
            event['interval'], event['thinking'], event['time'])

    #FIXME: this is modified add_new_cards function from default_controller
    def add_card(self, fact, card_type, grade, tags):
        pass

    def apply_history(self, history):
        """Parses XML history and apply it to database."""

        for child in ElementTree.fromstring(history).getchildren():
            event = int(child.get('ev'))
            """
            obj = self.create_object_from_xml(child)
            if event == events.ADDED_FACT:
                if not self.database.has_fact_with_data(obj.data, \
                    obj.card_type):
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
            """

    def create_object_from_xml(self, item):
        """Creates real object from XML Element."""
        
        obj_type = item.tag
        if obj_type == 'fact':
            card_type = self.database.get_card_type(item.get('ctid'))
            dkeys = item.get('dk').split(',')
            dvalues = []
            for num in len(dkeys):
                dvalues.append(item.get("dv%s" % num))
            fact_data = dict([(key, value) for key, value in dkeys,dvalues])
            print "create_fact_from_xml, fact_data=", fact_data
            creation_time = item.get('tm')
            fact_id = item.get('id')
            return Fact(fact_data, card_type, creation_time, fact_id)
        elif obj_type == 'card':
            class DictClass(dict):
                pass
            card = DictClass()
            card.id = item.get('id')
            card_type = DictClass()
            card_type.id = item.get('ctid')
            card.fact = self.database.get_fact_by_id(item.get('fid'))
            card.tags = set(self.database.get_or_create_tag_with_name(tag_name) \
                for tag_name in item.get('tags').split(','))
            card.grade = int(item.get('gr'))
            card.easiness = int(item.get('e'))
            card.last_rep = int(item.get('lr'))
            card.next_rep = int(item.get('nr'))
            return card
        elif obj_type == 'tag':
            return Tag(item.get('name'), item.get('id'))
        elif obj_type == 'ctype':
            print "parsing cardtype from xml"
        elif obj_type == 'rep':
            print 'repetition'
        return ""


