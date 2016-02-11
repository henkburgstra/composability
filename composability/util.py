import re

re_path_key = re.compile("\([a-zA-Z0-9-]+\)")
re_path_info = re.compile("(.+)(\()([a-zA-Z0-9-]+)(\))")
re_path = re.compile("([\w-]*)(/|$)(.*)")


def strip_key(path):
    return re_path_key.sub("", path)


class PathInfo(object):
    re_item_key = re.compile("(.+)(\()([a-zA-Z0-9-]+)(\))")

    def __init__(self, path):
        """
        given a :param path this(1)/is(2)/a(3)/path(4)/name, return
         a dictionary {
            "field": "name",
            "items": {
                "this": "1",
                "is": "2",
                "a": "3",
                "path": "4"
            }
        if a path contains multiple elements with the same name,
        the dictionary contains the last element only.
        :return: dictionary
        """
        self.field = None
        self.items = []
        self.keys = dict()

        parts = path.split("/")
        tail = parts.pop()

        if tail and "(" not in tail:
            self.field = tail
        elif tail:
            parts += [tail]

        parts.reverse()
        while parts:
            part = parts.pop()
            m = self.re_item_key.match(part)
            if m:
                item = m.group(1)
                key = m.group(3)
                self.items += [item]
                self.keys[item] = key


class DotDict(dict):
    def __init__(self, **kwds):
        self.update(kwds)
        self.__dict__ = self
