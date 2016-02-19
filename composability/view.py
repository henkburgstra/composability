import abc


class View(object):
    """
    View defines the interface for View classes.
    """
    __metaclass__ = abc.ABCMeta
    # view kinds
    VK_PLACEHOLDER = "PLACEHOLDER"
    VK_CONTAINER = "CONTAINER"
    VK_LABEL = "LABEL"
    VK_HYPERLINK = "HYPERLINK"
    VK_TEXT = "TEXT"
    VK_DATE = "DATE"
    VK_BUTTON = "BUTTON"
    VK_COMBO = "COMBO"

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


