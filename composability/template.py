class Template(object):
    # view kinds
    VK_UNDEFINED = "UNDEFINED"
    VK_CONTAINER = "CONTAINER"
    VK_LABEL = "LABEL"
    VK_HYPERLINK = "HYPERLINK"
    VK_TEXT = "TEXT"
    VK_BUTTON = "BUTTON"

    DISP_GROUP = "GROUP"
    DISP_INLINE = "INLINE"
    DISP_UNDER = "UNDER"
    DISP_RIGHT = "RIGHT"

    ORI_HORIZONTAL = "HORIZONTAL"
    ORI_VERTICAL = "VERTICAL"

    def __init__(self, kind, name="", value=None, title="", orientation=None, display=None,
                 background_colour=None):
        self.parent = None
        self.kind = kind
        self.name = name
        self.value = value
        self.title = title
        self.visible = True
        self.orientation = Template.ORI_HORIZONTAL if orientation is None else orientation
        self.display = Template.DISP_INLINE if display is None else display
        self.background_colour = background_colour
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

    def delete(self, template):
        if template.name in self.items_dict.keys():
            del self.items_dict[template.name]
            self.items.remove(template)

    def clear(self):
        self.items = []
        self.items_dict = {}

    def set_orientation(self, orientation):
        self.orientation = orientation