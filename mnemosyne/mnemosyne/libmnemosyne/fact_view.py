#
# fact_view.py <Peter.Bienstman@UGent.be>
#


class FactView(object):

    """Sequence of fields from a fact to form a question and an answer.
    A fact view needs an id string as well as a name, because the name can
    change for different translations. 
    
    """

    def __init__(self, id, name):
        #print "Fact_view.py __init__ method"
        self.id = id
        self.name = name
        self.q_fields = []
        self.a_fields = []
        self.required_fields = []
        self.a_on_top_of_q = False
        self.type_answer = False
        self.extra_data = {}
        #print "fact_view.id =", self.id
        #print "fact_view.name =", self.name
        #print "fact_view.q_fields =", self.q_fields
        #print "fact_view.a_fields =", self.a_fields
        #print "fact_view.required_fields =", self.required_fields
        #print "instance=", self

    def __eq__(self, other):
        return self.id == other.id   

    
