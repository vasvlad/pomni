#!/usr/bin/python -tt
# vim: sw=4 ts=4 expandtab ai
#
# statistics.py <vlad@gas.by>
#

import time

from mnemosyne.libmnemosyne.component import Component

DAY = 24 * 60 * 60 # Seconds in a day.

class Statistics(Component):
    """ Statistics Data """


    component_type = "statistics"
    instantiate = Component.LATER


class CurrentCardStatisctcs(Statistics):
    """ Statistics of current card """

    def __init__(self, component_manager):
        Statistics.__init__(self, component_manager)
        self.data = {}

    def get_data(self):
        """ get data """

        card = self.review_controller().card
        if not card:
            self.data['error'] = 'No current card.'
        elif card.grade == -1:
            self.data['error'] = 'Unseen card, no statistics available yet.'
        else:
            self.data['Grade'] = '%d' % card.grade 
            self.data['Easiness'] = '%1.2f' % card.easiness 
            self.data['Repetitions'] = '%d' % (card.acq_reps + card.ret_reps) 
            self.data['Lapses'] = '%d' % card.lapses
            self.data['Interval'] = '%d' % (card.interval / DAY)
            self.data['Last repetition'] = '%s' % \
                        time.strftime("%B %d, %Y", time.gmtime(card.last_rep)) 
            self.data['Next repetition'] = '%s' % \
                        time.strftime("%B %d, %Y", time.gmtime(card.next_rep)) 
            self.data['Average thinking time (secs)'] = '%d' % \
                        self.database().average_thinking_time(card)
            self.data['Total thinking time (secs)'] = '%d' % \
                        self.database().total_thinking_time(card)
        return self.data 

