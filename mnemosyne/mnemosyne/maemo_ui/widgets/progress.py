
from mnemosyne.libmnemosyne.ui_components.dialogs import ProgressDialog


class MaemoProgressDlg(ProgressDialog):

    def __init__(self, component_manager):
        ProgressDialog.__init__(self, component_manager)

    def set_range(self, minimum, maximum):
#        self.setRange(minimum, maximum)
        print "set_range"
        
    def set_text(self, text):
#        self.setLabelText(text)
        print "set_text"
        
    def set_value(self, value):
#        self.setValue(value)
        print "set_value"
