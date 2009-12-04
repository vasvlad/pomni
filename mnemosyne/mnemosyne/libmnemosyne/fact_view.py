#
# fact_view.py <Peter.Bienstman@UGent.be>
#

from mnemosyne.libmnemosyne.utils import CompareOnId


class FactView(CompareOnId):

    """Sequence of fields from a fact to form a question and an answer.
    A fact view needs an id string as well as a name, because the name can
    change for different translations.

    Note that id's should be unique, so a good naming convention is
    'card_type_id::fact_view_id'.
    
    """

    def __init__(self, id, name):
        #print "Fact_view.py __init__ method"
        self.id = id
        self.name = name
        self.q_fields = []
        self.a_fields = []
        self.a_on_top_of_q = False
        self.type_answer = False
        self.extra_data = {}
        #print "fact_view.id =", self.id
        #print "fact_view.name =", self.name
        #print "fact_view.q_fields =", self.q_fields
        #print "fact_view.a_fields =", self.a_fields
        #print "fact_view.required_fields =", self.required_fields
        #print "instance=", self

    
