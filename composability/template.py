class Template(object):
    DISP_GROUP = "GROUP"
    DISP_INLINE = "INLINE"
    DISP_UNDER = "UNDER"
    DISP_RIGHT = "RIGHT"

    ORI_HORIZONTAL = "HORIZONTAL"
    ORI_VERTICAL = "VERTICAL"

    POS_ABOVE = "ABOVE"
    POS_LEFT = "LEFT"
    POS_BEFORE = "BEFORE"
    POS_AFTER = "AFTER"

    _attribute_defaults = dict(
        backgroun_colour="white",
        colcount=-1,
        colspan=1,
        rowspan=1,
        orientation=ORI_HORIZONTAL,
        display=DISP_INLINE,
        label_position=POS_ABOVE
    )

    _id_counter = dict()

    def __init__(self, kind, name="", title="", value=None, readonly=False, visible=True, attributes=None):
        self.parent = None
        self.kind = kind
        self.name = name
        self.title = title
        self.value = value
        self.readonly = readonly
        self.visible = True
        self.attributes = dict() if attributes is None else attributes
        self.items = []  #  child views
        self.items_dict = {}

    def __str__(self):
        return "%s: %s <%s>" % (self.kind, self.name, "Empty" if self.value == "" else self.value)

    def id_counter(self):
        counter = self._id_counter.get(self.kind, 0)
        counter += 1
        self._id_counter[self.kind] = counter
        return counter

    def attr(self, name):
        return self.attributes.get(name, self._attribute_defaults.get(name))

    def set_attr(self, name, value):
        self.attributes[name] = value

    def add(self, template):
        if template.attr("background_colour") is None:
            template.set_attr("background_colour", self.attr("background_colour"))
        template.parent = self
        self.items += [template]
        self.items_dict[template.name] = template

    def insert(self, sibling_name, pos, template):
        items = self.items
        self.items = []
        self.items_dict = {}
        for item in items:
            if item.name == sibling_name:
                if pos == self.POS_BEFORE:
                    self.add(template)
                    self.add(item)
                else:
                    self.add(item)
                    self.add(template)
            else:
                self.add(item)

    def get(self, name):
        return self.items_dict.get(name)

    def get_parent_name(self):
        if self.parent:
            return self.parent.name
        if self.name is None:
            return ""
        return "/".join(self.name.split("/")[:-1])

    def delete(self, template):
        if template.name in self.items_dict.keys():
            del self.items_dict[template.name]
            self.items.remove(template)

    def clear(self):
        self.items = []
        self.items_dict = {}
