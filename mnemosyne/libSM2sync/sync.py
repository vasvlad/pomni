# vim: sw=4 ts=4 expandtab ai
#
# sync.py
#
# Max Usachev <maxusachev@gmail.com>, 
# Ed Bartosh <bartosh@gmail.com>, 
# Peter Bienstman <Peter.Bienstman@UGent.be>

from mnemosyne.libmnemosyne.tag import Tag
from mnemosyne.libmnemosyne.fact import Fact
from mnemosyne.libmnemosyne.databases.SQLite_logging import SQLiteLogging as events
from xml.etree import ElementTree

PROTOCOL_VERSION = 0.1
QA_CARD_TYPE = 1
VICE_VERSA_CARD_TYPE = 2
N_SIDED_CARD_TYPE = 3


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
        self.partner = {'role': None, 'machine_id': None, 'name': 'Mnemosyne', \
            'ver': None, 'protocol': None, 'cardtypes': None, 'extra': \
            None, 'deck': None, 'upload': True, 'readonly': False}

    def set_sync_params(self, partner_params):
        """Sets other side specific params."""

        params = ElementTree.fromstring(partner_params).getchildren()[0]
        self.partner['role'] = params.tag
        for key in params.keys():
            self.partner[key] = params.get(key)

    def get_history(self):
        """Creates history in XML."""
        
        history = "<history>"
        for item in self.database.get_history_events(\
            self.partner['machine_id']):
            event = {'event': item[0], 'time': item[1], 'id': item[2], \
                's_int': item[3], 'a_int': item[4], 'n_int': item[5], \
                't_time': item[6]}
            history += str(self.create_event_element(event))
        history += "</history>\n"
        return history

    def create_event_element(self, event):
        """Creates XML representation of event."""

        event_id = event['event']
        if event_id in (events.ADDED_TAG, events.UPDATED_TAG, \
            events.DELETED_TAG):
            return self.create_tag_xml_element(event)
        elif event_id in (events.ADDED_FACT, events.UPDATED_FACT, \
            events.DELETED_FACT):
            return self.create_fact_xml_element(event)
        elif event_id in (events.ADDED_CARD, events.UPDATED_CARD, \
            events.DELETED_CARD):
            return self.create_card_xml_element(event)
        elif event_id in (events.ADDED_CARD_TYPE, events.UPDATED_CARD_TYPE, \
            events.DELETED_CARD_TYPE, events.REPETITION):
            return self.create_card_xml_element(event)
        else:
            return ''   # No need XML for others events. ?

    def create_tag_xml_element(self, event):
        tag = self.database.get_tag(event['id'], False)
        return "<tag ev='%s' id='%s' name='%s'/>" % \
            (event['event'], tag.id, tag.name)

    def create_fact_xml_element(self, event):
        fact = self.database.get_fact(event['id'], False)
        dkeys = ','.join(["%s" % key for key, val in fact.data.items()])
        dvalues = ' '.join(["dv%s='%s'" % (num, fact.data.values()[num]) \
            for num in range(len(fact.data))])
        return "<fact ev='%s' id='%s' ctid='%s' dk='%s' %s tm='%s'/>" % \
            (event['event'], fact.id, fact.card_type.id, dkeys, dvalues, \
            event['time'])

    def create_card_xml_element(self, event):
        card = self.database.get_card(event['id'], False)
        return "<card ev='%s' id='%s' ctid='%s' fid='%s' fvid='%s'" \
            " tags='%s' gr='%s' e='%s' lr='%s' nr='%s' sint='%s' aint='%s'" \
            " nint='%s' ttm='%s' tm='%s'/>" % (event['event'], card.id, \
            card.fact.card_type.id, card.fact.id, card.fact_view.id, \
            ','.join([item.name for item in card.tags]), card.grade, \
            card.easiness, card.last_rep, card.next_rep, event['s_int'], \
            event['a_int'], event['n_int'], event['t_time'], event['time'])
        
    def create_card_type_xml_element(self, event):
        cardtype = self.database.get_card_type(event['id'], False)
        fields = [key for key, value in cardtype.fields]
        return "<ctype ev='%s' id='%s' name='%s' f='%s' uf='%s' ks='%s'" \
            " edata='%s'/>" % (event['event'], cardtype.id, cardtype.name, \
            ','.join(fields), ','.join(cardtype.unique_fields), '', '')

    def create_object_from_xml(self, item):
        class DictClass(dict):
            pass
        obj_type = item.tag
        if obj_type == 'fact':
            dkeys = item.get('dk').split(',')
            dvals = [item.get("dv%s" % num) for num in range(len(dkeys))]
            fact_data = dict([(key, dvals[dkeys.index(key)]) for key in dkeys])
            card_type = self.database.get_card_type(item.get('ctid'), False)
            creation_time = int(item.get('tm'))
            fact_id = item.get('id')
            return Fact(fact_data, card_type, creation_time, fact_id)
        elif obj_type == 'card':
            card = DictClass()
            card.id = item.get('id')
            card.fact_view = DictClass()
            card.fact_view.id = item.get('fvid')
            card.fact = self.database.get_fact(item.get('fid'), False)
            card.tags = set(self.database.get_or_create_tag_with_name(\
                tag_name) for tag_name in item.get('tags').split(','))
            card.grade = int(item.get('gr'))
            card.easiness = float(item.get('e'))
            card.acq_reps, card.ret_reps = 0, 0
            card.lapses = 0
            card.acq_reps_since_lapse, card.ret_reps_since_lapse = 0, 0
            card.last_rep = int(item.get('lr'))
            card.next_rep = int(item.get('nr'))
            card.extra_data, card.scheduler_data = 0, 0
            card.active, card.in_view = True, True
            #for repetition event
            try:
                card.scheduled_interval = int(item.get('sint'))
            except ValueError:
                card.scheduled_interval = ''
            try:
                card.actual_interval = int(item.get('aint'))
            except ValueError:
                card.actual_interval = ''
            try:
                card.new_interval = int(item.get('nint'))
            except:
                card.new_interval = ''
            try:
                card.thinking_time = int(item.get('ttm'))
            except:
                card.thinking_time = ''
            return card
        elif obj_type == 'tag':
            return Tag(item.get('name'), item.get('id'))
        elif obj_type == 'ctype':
            cardtype = DictClass()
            cardtype.id = item.get('id')
            cardtype.name = item.get('name')
            cardtype.fields = item.get('f').split(',')
            cardtype.unique_fields = item.get('uf').split(',')
            cardtype.keyboard_shortcuts, cardtype.extra_data = {}, {}
            return cardtype

    def apply_history(self, history):
        """Parses XML history and apply it to database."""

        for child in ElementTree.fromstring(history).getchildren():
            event = int(child.get('ev'))
            obj = self.create_object_from_xml(child)
            if event == events.ADDED_FACT:
                if not self.database.has_fact_with_data(obj):
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
                if not has_card_with_external_id(obj.id):
                    self.database.add_card(obj)
            elif event == events.UPDATED_CARD:
                self.database.update_card(obj)
            elif event == events.DELETED_CARD:
                self.database.delete_card(obj)
            elif event == events.REPETITION:
                self.database.repetition(obj, obj.scheduled_interval, \
                    obj.actual_interval, obj.new_interval, obj.thinking_time)

