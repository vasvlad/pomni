#
# html_css.py <Peter.Bienstman@UGent.be>
#

from mnemosyne.libmnemosyne.renderer import Renderer
from mnemosyne.libmnemosyne.component_manager import filters

# TODO: read card type css from $basedir/css/$card_type if it exits.
# TODO: add convenience functions to modify the css on disk:
#   set_background(card_type, color), set_font(card_type, fact_key, font),
#   set_alignment(card_type, fact_key, alignment), ...


class TextRenderer(Renderer):
    
    def render_card_fields(self, card, fields):
        fact = card.fact
        txt = ''
        for field in fields:
            key = field[0]
            s = fact[key]
            for f in filters():
                s = f.run(s, fact)
            txt += s
        return txt

