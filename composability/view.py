import abc


class View(object):
    """
    View defines the interface for View classes.
    """
    __metaclass__ = abc.ABCMeta
    # view kinds
    VK_UNDEFINED = "UNDEFINED"
    VK_CONTAINER = "CONTAINER"
    VK_LABEL = "LABEL"
    VK_HYPERLINK = "HYPERLINK"
    VK_TEXT = "TEXT"
    VK_DATE = "DATE"
    VK_BUTTON = "BUTTON"

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


class Transform(object):
    def __init__(self, value, **kwargs):
        self._value = value
        for k, v in kwargs.items():
            self.k = v

    def display(self):
        if self._value is None:
            return ""
        return self._value

    def store(self):
        return self._value


class TransformDate(Transform):
    def display(self):
        if self._value is None:
            return ""
        # TODO: robuuster maken
        y, m, d = self._value.split("-")
        return "-".join[d, m, y]

    def store(self):
        # TODO: robuuster maken
        d, m, y = self._value.split("-")
        return "-". join[y, m, d]


