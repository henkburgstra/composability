import re

re_path_key = re.compile("\([a-zA-Z0-9-]+\)")
re_path = re.compile("([\w-]*)(/|$)(.*)")


def strip_key(path):
    return re_path_key.sub("", path)