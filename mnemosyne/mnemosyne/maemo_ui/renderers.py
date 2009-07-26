#!/usr/bin/python -tt7
# vim: sw=4 ts=4 expandtab ai
#
# Mnemosyne. Learning tool based on spaced repetition technique
#
# Copyright (C) 2008 Pomni Development Team <pomni@googlegroups.com>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA

"""
Html renderer.
"""

from mnemosyne.libmnemosyne.renderer import Renderer
import re

LARGE_HTML_MARGIN = 20
NORMAL_HTML_MARGIN = 70
HINT_SIZE = 20

class Html(Renderer):
    """Hildon Html renderer."""
    
    def __init__(self, component_manager):
        Renderer.__init__(self, component_manager)
        self._css = {} # {card_type: css}
        
    def css(self, card_type):
        """Creates css."""

        if card_type.id not in self._css:
            self._css[card_type.id] = """
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <style type="text/css">*{font-size:30px;}
            table {height:100%;margin-left:auto;margin-right:auto;}\n"""
            for key in card_type.keys():
                self._css[card_type.id] += "div#"+ key + \
                    " {text-align: center;}\n"
            self._css[card_type.id] += "</style>"
        return self._css[card_type.id]

    def render_card_fields(self, fact, fields):
        """Renders cards fileds."""

        html = "<html><head>" + self.css(fact.card_type) + \
            "</head><body><table><tr><td>"
        for field in fields:
            text = fact[field]
            #for filter in self.filters():
            #    text = filter.run(text)
            html += "<div id=\"%s\">%s</div>" % (field, text)
        html += "</td></tr></table></body></html>"
        return self.change_font_size(html)

    def render_text(self, text, field_name, card_type):
        """Renders text card fields."""

        html = "<html><head>" + self.css(card_type) + \
            "</head><body><table><tr><td><div id=\"%s\">"
        html += "<div id=\"%s\">%s</div>" % (field_name, text)
        html += "</td></tr></table></body></html>"
        return self.change_font_size(html)

    def change_font_size(self, text):
        """Replace html font-size."""

        return re.sub('(.*\{font-size):[0-9]{1,2}(px;\}.*)', '\\1:%d\\2' \
            % self.config()['font_size'], text)

    def render_html(self, widget, text="<html><body> </body></html>"):
        """Render html text and set it to widget."""

        document = widget.document
        document.clear()
        document.open_stream('text/html')
        document.write_stream(text)
        document.close_stream()

    def render_hint(self, widget, text, next_is_image_card):
        """Render html text for show answer button."""

        if next_is_image_card:
            margin_top = LARGE_HTML_MARGIN
        else:
            margin_top = NORMAL_HTML_MARGIN
        html = "<html><p align=center style='margin-top:%spx; \
            font-size:%s;'>%s</p></html>" % (margin_top, HINT_SIZE, text)
        self.render_html(widget, html)




class Text(Renderer):
    """Simple text renderer."""

    def __init__(self, component_manager):
        Renderer.__init__(self, component_manager)
    
    def render_card_fields(self, fact, fields):
        """Renders card fields."""

        txt = ''
        for field in fields:
            text = fact[field]
            for flt in self.filters():
                text = flt.run(text, fact)
            txt += text
        return txt
