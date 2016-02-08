import re

re_path_key = re.compile("\([a-zA-Z0-9-]+\)")
re_path_info = re.compile("(.+)(\()([a-zA-Z0-9-]+)(\))")
re_path = re.compile("([\w-]*)(/|$)(.*)")


def strip_key(path):
    return re_path_key.sub("", path)


def path_info(path):
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
    details = dict(field=None, items=dict())
    parts = path.split("/")
    tail = parts.pop()
    if tail and "(" not in tail:
        details["field"] = tail
    while parts:
        part = parts.pop()
        m = re_path_info.match(part)
        if m:
            details["items"][m.group(1)] = m.group(3)
    return details


