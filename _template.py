import copy

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

    def __init__(self, kind, name, value=None, title="", orientation=None, display=None,
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
        self.items_dict = []

    def set_orientation(self, orientation):
        self.orientation = orientation

    def load(self):
        self.loader.load()
        return self.get(copy.copy(self.template), loader=self.loader)

    def get_visual_container(self, parent=None, data=None):
        for item in self.items:
            if item.kind == Template.VK_CONTAINER and not item.name:
                item_data = data
            else:
                item_data = data.get(item.name.split("/").pop())
            self.get(item, parent=parent, loader=item_data)

    def get_template_container(self, parent=None, data=None):
        for item_data in data.get("items", []):
            template_item = copy.deepcopy(self)
            self.get(template_item, parent=parent, loader=item_data)
            if template_item is not None:
                parent.add(template_item)
        #parent.delete(template)
        self.visible = False  # template  blijft in het model vanwege relatie-eigenschappen zoals start, limit...
        return parent

    def get_container(self, parent=None, data=None):
        for item in copy.copy(self.items):
            if item.kind == Template.VK_CONTAINER and not item.name:
                item_data = data
            else:
                item_name = item.name.split("/").pop()
                item_data = data.get(item_name)
            self.get(item, parent=self, loader=item_data)
        return self # TODO: ????

    def get(self, parent=None, loader=None):
        #  Er is altijd een hoofd entiteit met een natuurlijke key. Bij de fiatteer widget
        #  is de medewerker de hoofd entiteit met daaraan gekoppeld de behandeldagen / verrichtingen
        #  die gefiatteerd moeten worden.
        template = self
        if self.kind == Template.VK_CONTAINER:
            if loader is None:
                template = None
            #  Er zijn drie soorten containers:
            #  (1) Container zonder naam. Dit zijn visueel gegroepeerde velden van dezelfde
            #      entiteit als de parent.
            elif not self.name:
                template = self.get_visual_container(self, parent=parent, data=loader)
            #  (2) Container met key. Dit is een enkel item uit een relatie, bijvoorbeeld
            #      patient(1)/behandelingen(1)
            elif loader.get("key"):
                template.name = "%s(%s)" % (template.name, loader.get("key"))
                if parent is not None:
                    template.name = "%s/%s" % (parent.name, template.name)
                template = self.get_container(template, parent=parent, data=loader)
            #  (3) Container zonder key. Dit is een template voor een relatie, bijvoorbeeld
            #      patient/behandelingen waarvan de items nog moeten worden opgehaald
            else:
                template = self.get_template_container(template, parent=parent, data=loader)

            # if template is not None and parent is not None:
            #     template.name = "%s/%s" % (parent.name, template.name)

        else:
            if loader is None:
                value = ""  # TODO: default value gebaseerd op template.kind
            else:
                value = loader
            template.value = value
            template.name = "%s/%s" % (parent.name, template.name)

        return template

    def get_fields(self, template):
        fields = []
        for item in template.items:
            if item.kind == Template.VK_CONTAINER:
                # container is een visuele groep, velden doen mee voor deze tabel.
                if not item.name:
                    fields += self.get_fields(item)
            else:
                if item.kind not in (Template.VK_BUTTON,):
                    fields += [item.name] # TODO virtuele velden etc. uitsluiten

        return fields
