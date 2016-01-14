import abc
from .loader import Loader
from .binder import Binder, SQLBinder
from .controller import Message, Controller
from .registry import Registry
from .select import Connective, And, Or, Param, Select
from .template import Template

class View(object):
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

