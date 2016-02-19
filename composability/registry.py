import copy
import json
import os

from .template import Template
from .view import View

class Registry(object):
    def __init__(self, def_path):
        self.def_path = def_path
        self.templates = {}

    # TODO; implementeer keyword "modify"

    def extend_def(self, p):
        name = p.get("extend")
        if not name:
            return
        parent = self.get_template(name)
        if parent is None:
            return
        p = copy.copy(p)
        del p["extend"]
        before = p.get("before")
        after = p.get("after")
        if before is None:
            sibling_name = after
        else:
            sibling_name = before
        i = 0
        found = None
        for sibling in parent.items:
            if sibling.name == sibling_name:
                found = sibling
            i += 1
        if found is None:
            return
        if after is not None:
            i += 1
        parent.items.insert(i, self.load_def_item(p))
        return parent

    def include_def_item(self, p):
        name = p.get("include")
        if not name:
            return
        return self.get_template(name)

    def load_def_item(self, d):
        extended = self.extend_def(d)
        if extended is not None:
            return extended
        include = self.include_def_item(d)
        name = d.get("name", "")  # TODO: UID
        title = d.get("title", "")
        display = d.get("display")
        if include is None:
            template = Template(
                d.get("kind", View.VK_TEXT),
                name,
                title=title,
                orientation=d.get("orientation"),
                display=display,
                colcount=d.get("colcount", -1),
                background_colour=d.get("background_colour")
            )
            items = d.get("items", [])
            for item in items:
                template.add(self.load_def_item(item))
        else:
            template = include
            template.name = name
            template.title = title
            template.display = display

        return template

    def load_template(self, name):
        with open(os.path.join(self.def_path, "%s.json" % name), "r") as f:
            d = json.load(f)
            template = self.load_def_item(d)
        return template

    def get_template(self, name):
        template = self.templates.get(name)
        if template is not None:
            return template
        template = self.load_template(name)
        if template is not None:
            self.templates[name] = template
        return template
