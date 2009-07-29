# vim: sw=4 ts=4 expandtab ai
#
# sync.py
#
# Max Usachev <maxusachev@gmail.com>, 
# Ed Bartosh <bartosh@gmail.com>, 
# Peter Bienstman <Peter.Bienstman@UGent.be>

from mnemosyne.libmnemosyne.tag import Tag
from mnemosyne.libmnemosyne.fact import Fact
from mnemosyne.libmnemosyne.databases.SQLite_logging \
    import SQLiteLogging as events
from xml.etree import ElementTree

PROTOCOL_VERSION = 0.1
QA_CARD_TYPE = 1
VICE_VERSA_CARD_TYPE = 2
N_SIDED_CARD_TYPE = 3


class SyncError(Exception):
    """Sync exception class."""
    pass


class DictClass(dict):
    """Class for creating custom objects."""
    
    def __init__(self, attributes=None):
        for attr in attributes.keys():
            setattr(self, attr, attributes[attr])


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
        self.object_factory = {'tag': self.create_tag_object, 'fact': \
            self.create_fact_object, 'card': self.create_card_object, \
            'cardtype': self.create_cardtype_object}
        self.partner = {'role': None, 'id': None, 'name': 'Mnemosyne', \
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
            self.partner['id']):
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
        return "<i><t>tag</t><ev>%s</ev><id>%s</id><name>%s</name></i>" % \
            (event['event'], tag.id, tag.name)

    def create_fact_xml_element(self, event):
        fact = self.database.get_fact(event['id'], False)
        dkeys = ','.join(["%s" % key for key, val in fact.data.items()])
        dvalues = ''.join(["<dv%s>%s</dv%s>" % (num, fact.data.values()[num], \
        num) for num in range(len(fact.data))])
        return "<i><t>fact</t><ev>%s</ev><id>%s</id><ctid>%s</ctid><dk>%s</dk>"\
            "%s<tm>%s</tm></i>" % (event['event'], fact.id, fact.card_type.id, \
            dkeys, dvalues, event['time'])

    def create_card_xml_element(self, event):
        card = self.database.get_card(event['id'], False)
        return "<i><t>card</t><ev>%s</ev><id>%s</id><ctid>%s</ctid><fid>%s" \
            "</fid><fvid>%s</fvid><tags>%s</tags><gr>%s</gr><e>%s</e><lr>%s" \
            "</lr><nr>%s</nr><si>%s</si><ai>%s</ai><ni>%s</ni><ttm>%s</ttm>" \
            "<tm>%s</tm></i>" % (event['event'], card.id, \
            card.fact.card_type.id, card.fact.id, card.fact_view.id, \
            ','.join([item.name for item in card.tags]), card.grade, \
            card.easiness, card.last_rep, card.next_rep, event['s_int'], \
            event['a_int'], event['n_int'], event['t_time'], event['time'])
        
    def create_card_type_xml_element(self, event):
        cardtype = self.database.get_card_type(event['id'], False)
        fields = [key for key, value in cardtype.fields]
        return "<i><t>ctype</t><ev>%s</ev><id>%s</id><name>%s</name><f>%s</f>"\
        "<uf>%s</uf><ks>%s</ks><edata>%s</edata></i>" % (event['event'], \
        cardtype.id, cardtype.name, ','.join(fields), \
        ','.join(cardtype.unique_fields), '', '')

    def create_tag_object(self, item):
        return Tag(item.find('name').text, item.find('id').text)

    def create_fact_object(self, item):
        dkeys = item.find('dk').text.split(',')
        dvals = [item.find("dv%s" % num).text for num in range(len(dkeys))]
        fact_data = dict([(key, dvals[dkeys.index(key)]) for key in dkeys])
        card_type = self.database.get_card_type(\
            item.find('ctid').text, False)
        creation_time = int(item.find('tm').text)
        fact_id = item.find('id').text
        return Fact(fact_data, card_type, creation_time, fact_id)

    def create_card_object(self, item):
        def get_rep_value(value):
            """Return value for repetition event."""
            try: return int(value)
            except: return ''
        return DictClass({'id': item.find('id').text, 'fact_view': DictClass(\
            {'id': item.find('fvid').text}), 'fact': self.database.get_fact(\
            item.find('fid').text, False), 'tags': set(self.database.\
            get_or_create_tag_with_name(tag_name) for tag_name in item.find(\
            'tags').text.split(',')), 'grade': int(item.find('gr').text), \
            'easiness': float(item.find('e').text), 'acq_reps': 0, 'ret_reps': \
            0, 'lapses': 0, 'acq_reps_since_lapse': 0, 'ret_reps_since_lapse': \
            0, 'last_rep': int(item.find('lr').text), 'next_rep': int(\
            item.find('nr').text), 'extra_data': 0, 'scheduler_data': 0, \
            'active': True, 'in_view': True, 'timestamp': int(item.find(\
            'tm').text), 'scheduled_interval': get_rep_value(item.find(\
            'si').text), 'actual_interval': get_rep_value(item.find(\
            'ai').text), 'new_interval': get_rep_value(item.find('ni').text), \
            'thinking_time': get_rep_value(item.find('ttm').text)})

    def create_cardtype_object(self, item):
        return DictClass({'id': item.find('id').text, 'name': \
            item.find('name').text, 'fields': item.find('f').text.split(','), \
            'keyboard_shortcuts': {}, 'extra_data': {}, 'unique_fields': \
            item.find('uf').text.split(',')})

    def apply_history(self, history):
        """Parses XML history and apply it to database."""

        for child in ElementTree.fromstring(history).findall('i'):
            event = int(child.find('ev').text)
            obj = self.object_factory[child.find('t').text](child)
            if event == events.ADDED_FACT:
                if not self.database.duplicates_for_fact(obj):
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
                if not self.database.has_card_with_external_id(obj.id):
                    self.database.add_card(obj)
            elif event == events.UPDATED_CARD:
                self.database.update_card(obj)
            elif event == events.DELETED_CARD:
                self.database.delete_card(obj)
            elif event == events.REPETITION:
                self.database.log_repetition(obj.timestamp, obj.id, obj.grade, \
                obj.easiness, obj.acq_reps, obj.ret_reps, obj.lapses, \
                obj.acq_reps_since_lapse, obj.ret_reps_since_lapse, \
                obj.scheduled_interval, obj.actual_interval, obj.new_interval, \
                obj.thinking_time)
        self.database.update_last_sync_event(self.partner['id'])

