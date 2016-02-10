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

class ViewBuffer(object):
    def __init__(self, key):
        self.key = key
        self._original = None
        self._value = None

    def set(self, value):
        if self._original is None:
            self._original = value
        self._value = value

    def get(self):
        return self._value

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

    def set_value(self, key, value):
        buf = self._buffers.get(key, ViewBuffer(key))
        buf.set(value)
        self._buffers[key] = buf