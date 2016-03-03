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

    @abc.abstractmethod
    def add(self, template):
        pass

    @abc.abstractmethod
    def get_value(self, name):
        pass

    @abc.abstractmethod
    def insert(self,template, pos, sibling_name):
        pass

    @abc.abstractmethod
    def remove(self, name):
        pass

    @abc.abstractmethod
    def set_controller(self, controller):
        pass

    @abc.abstractmethod
    def set_value(self, name, value):
        pass





