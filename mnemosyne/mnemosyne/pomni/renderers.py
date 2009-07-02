#
# html_css.py <Peter.Bienstman@UGent.be>
# html_maemo.py # Copyright (C) 2008 Pomni Development Team <pomni@googlegroups.com>

from mnemosyne.libmnemosyne.renderer import Renderer

class Html(Renderer):
    
    def __init__(self, component_manager):
        Renderer.__init__(self, component_manager)
        self._css = {} # {card_type: css}
        
    def css(self, card_type):
        if card_type.id not in self._css:
            self._css[card_type.id] = """
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <style type="text/css">
            *{font-size:30px;}
            table {
                height:100%;
                margin-left: auto;
                margin-right: auto;
            }
            body { 
                color: black;
                background-color: white;
                margin: 0;
                padding: 0;
            }\n"""

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
            for f in self.filters():
                s = f.run(s)
            html += "<div id=\"%s\">%s</div>" % (field, s)
        html += "</td></tr></table></body></html>"
        return html

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

