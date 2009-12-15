#
# statistics_page.py <Peter.Bienstman@UGent.be>
#

import time

from mnemosyne.libmnemosyne.component import Component

DAY = 24 * 60 * 60 # Seconds in a day

class StatisticsPage(Component):

    """A self-contained piece of statistical information, typically displayed
    in the GUI as a page in a tabbed widget.

    Each StatisticsPage can have several 'variants', e.g. displaying the
    number of scheduled cards either for next week or for next month.

    For each StatisticsPage, there will be an associated widget (plotting
    widget, html browser, custom widget, ... ) that is in charge of displaying
    the information. This widget needs to be registered in the component
    manager as a 'statistics_widget' 'used_for' a particular StatisticsPage (or a
    parent class of a StatisticsPage).

    """
    
    component_type = "statistics_page"    
    instantiate = Component.LATER

    name = ""
    data = {}

    variants = [] # [(variant_id, variant_name)]
    show_variants_in_combobox = True
        
    def prepare_statistics(self, variant_id):

        """This method calculates the data for the requested variant and sets
        the approriate hints to be picked up by the corresponding widget.

        """

        raise NotImplementedError

    def get_raw_data(self):

        """This method returns the data(dictonary) for statistics

        """

        raise NotImplementedError


class CurrentCardStatPage(StatisticsPage):

    """A statistics for current card

    """
    raw_data = {}

    def __init__(self, component_manager):
        StatisticsPage.__init__(self, component_manager)

    def get_data(self):
        """ get data """

        card = self.review_controller().card
        if not card:
            self.raw_data['error'] = 'No current card.'
        elif card.grade == -1:
            self.raw_data['error'] = 'Unseen card, no statistics available yet.'
        else:
            self.raw_data['Grade'] = '%d' % card.grade 
            self.raw_data['Easiness'] = '%1.2f' % card.easiness 
            self.raw_data['Repetitions'] = '%d' % \
                                          (card.acq_reps + card.ret_reps)
            self.raw_data['Lapses'] = '%d' % card.lapses
            self.raw_data['Interval'] = '%d' % (card.interval / DAY)
            self.raw_data['Last repetition'] = '%s' % \
                        time.strftime("%B %d, %Y", time.gmtime(card.last_rep))
            self.raw_data['Next repetition'] = '%s' % \
                        time.strftime("%B %d, %Y", time.gmtime(card.next_rep))
            self.raw_data['Average thinking time (secs)'] = '%d' % \
                        self.database().average_thinking_time(card)
            self.raw_data['Total thinking time (secs)'] = '%d' % \
                        self.database().total_thinking_time(card)
        return self.raw_data

class PlotStatisticsPage(StatisticsPage):

    """A statistics page where the data is represented on a graphical plot.

    """
        
    def __init__(self, component_manager):
        StatisticsPage.__init__(self, component_manager)
        self.x = []
        self.y = []


class HtmlStatisticsPage(StatisticsPage):

    """A statistics page which generates html to displayed in a browser
    widget.

    """
        
    def __init__(self, component_manager):
        StatisticsPage.__init__(self, component_manager)
        self.html = None

