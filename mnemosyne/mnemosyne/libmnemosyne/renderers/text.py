#
# html_css.py <Peter.Bienstman@UGent.be>
#

from mnemosyne.libmnemosyne.renderer import Renderer

class TextRenderer(Renderer):
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

