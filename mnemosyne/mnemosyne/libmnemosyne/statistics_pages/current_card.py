#
# current_card.py <Peter.Bienstman@UGent.be>
#

from mnemosyne.libmnemosyne.translator import _
from mnemosyne.libmnemosyne.statistics_page import CurrentCardStatPage
from mnemosyne.libmnemosyne.statistics_page import HtmlStatisticsPage


class CurrentCard(CurrentCardStatPage, HtmlStatisticsPage):

    name = _("Current card")

    def prepare_statistics(self, variant):
        """ Preparing for html widget """

        self.html = """<html<body>
        <style type="text/css">
        table { height: 100%;
                margin-left: auto; margin-right: auto;
                text-align: center}
        body  { background-color: white;
                margin: 0;
                padding: 0;
                border: thin solid #8F8F8F; }
        </style></head><table><tr><td>"""
        data = self.get_raw_data()
        if data.has_key('error'):
            self.html += data['error']
        else:
            self.html += "<br>".join(["%s %s" % (name, result) \
                                        for name, result in data.items()])
        self.html += "</td></tr></table></body></html>"
