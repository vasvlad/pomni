#
# activity_criterion_widget.py <Peter.Bienstman@UGent.be>
#

from mnemosyne.libmnemosyne.ui_component import UiComponent


class ActivityCriterionWidget(UiComponent):

    component_type = "activity_criterion_widget"
    instantiate = UiComponent.LATER

    def display_default_criterion(self):
        raise NotImplementedError        

    def display_criterion(self, criterion):
        raise NotImplementedError

    def get_criterion(self):
        raise NotImplementedError
