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

    def __init__(self, kind, name="", value=None, title="", orientation=None, display=None,
                 colcount=-1, colspan=1, rowspan=1, label_position=POS_ABOVE, background_colour=None):
        self.parent = None
        self.kind = kind
        self.name = name
        self.value = value
        self.title = title
        self.visible = True
        self.orientation = Template.ORI_HORIZONTAL if orientation is None else orientation
        self.display = Template.DISP_INLINE if display is None else display
        self.background_colour = background_colour
        self.colcount = colcount
        self.colspan = colspan
        self.rowspan = rowspan
        self.label_position = label_position
        self.items = []  #  child views
        self.items_dict = {}

    def __str__(self):
        return "%s: %s <%s>" % (self.kind, self.name, "Empty" if self.value == "" else self.value)

    def add(self, template):
        if template.background_colour is None:
            template.background_colour = self.background_colour
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

    def set_orientation(self, orientation):
        self.orientation = orientation
