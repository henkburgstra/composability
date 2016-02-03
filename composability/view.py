import abc

class View(object):
    """
    View defines the interface for View classes.
    """
    __metaclass__ = abc.ABCMeta

    # def on_change(self):
    #     self.controller.view_changed(self)
    #
    # def on_focus(self):
    #     self.controller.view_focused(self)
    #
    # def on_click(self):
    #     self.controller.view_clicked(self)
    def add(self, template):
        pass
