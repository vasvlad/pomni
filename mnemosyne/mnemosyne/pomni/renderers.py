#
# html_css.py <Peter.Bienstman@UGent.be>
# html_maemo.py # Copyright (C) 2008 Pomni Development Team <pomni@googlegroups.com>

from mnemosyne.libmnemosyne.renderer import Renderer
import re

LARGE_HTML_MARGIN = 20
NORMAL_HTML_MARGIN = 70
HINT_SIZE = 20

class Html(Renderer):
    
    def __init__(self, component_manager):
        Renderer.__init__(self, component_manager)
        self._css = {} # {card_type: css}
        
    def css(self, card_type):
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
        html = "<html><head>" + self.css(fact.card_type) + \
            "</head><body><table><tr><td>"
        for field in fields:
            s = fact[field]
            #for f in self.filters():
            #    s = f.run(s)
            html += "<div id=\"%s\">%s</div>" % (field, s)
        html += "</td></tr></table></body></html>"
        return self.change_font_size(html)

    def render_text(self, text, field_name, card_type):
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

    def update_show_button(self, widget, text, next_is_image_card):
        """Render html text for show answer button."""

        if next_is_image_card:
            margin_top = LARGE_HTML_MARGIN
        else:
            margin_top = NORMAL_HTML_MARGIN
        html = "<html><p align=center style='margin-top:%spx; \
            font-size:%s;'>%s</p></html>" % (margin_top, HINT_SIZE, text)
        self.render_html(widget, html)




class Text(Renderer):
    def __init__(self, component_manager):
        Renderer.__init__(self, component_manager)
    
    def render_card_fields(self, fact, fields):
        txt = ''
        for field in fields:
            s = fact[field]
            for f in self.filters():
                s = f.run(s, fact)
            txt += s
        return txt

