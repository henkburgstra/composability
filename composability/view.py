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


class ViewBuffer(object):
    def __init__(self, key, kind=View.VK_TEXT, transform=Transform):
        self.key = key
        self.kind = kind
        self.transform = transform
        self._original = None
        self._value = None

    def set(self, value):
        if self._original is None:
            self._original = value
        self._value = value

    def get(self):
        return self._value

    def get_display(self):
        return self.transform(self._value).display()

    def set_display(self, value):
        self.set(self.transform(value).store())

    def revert(self):
        self._value = self._original

    def flush(self):
        self._original = self._value = None


class BufferList(object):
    def __init__(self):
        self._buffers = dict()

    def is_dirty(self):
        for buf in self._buffers.values():
            if buf.is_dirty():
                return True
        return False

    def clear(self):
        self._buffers = dict()

    def revert(self):
        for buf in self._buffers.values():
            buf.revert()

    def flush(self):
        for buf in self._buffers.values():
            buf.flush()

    def get_value(self, key):
        buf = self._buffers.get(key)
        if buf is not None:
            return buf.get()

    def get_display(self, key):
        buf = self._buffers.get(key)
        if buf is None:
            return ""
        return buf.get_display()

    def set_value(self, key, value, kind=View.VK_TEXT):
        buf = self._buffers.get(key, ViewBuffer(key, kind=kind))
        buf.set(value)
        self._buffers[key] = buf