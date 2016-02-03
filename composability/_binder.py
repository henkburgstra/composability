import copy

from template import Template

class Binder(object):

    def __init__(self, template, loader):
        self.template = template
        self.loader = loader
        self.loader.set_name(self.template.name)
        self.loader.set_fields(self.get_fields(self.template))
        self.selection = None       #  Select or Connective instance

    def select(self, selection):
        self.selection = selection     #  Select or Connective instance
        self.loader.select(selection)

    def load(self):
        self.loader.load()
        return self.get(copy.copy(self.template), loader=self.loader)

    def get_visual_container(self, template, parent=None, data=None):
        for item in template.items:
            if item.kind == Template.VK_CONTAINER and not item.name:
                item_data = data
            else:
                item_data = data.get(item.name.split("/").pop())
            self.get(item, parent=parent, loader=item_data)

    def get_template_container(self, template, parent=None, data=None):
        for item_data in data.get("items", []):
            template_item = copy.deepcopy(template)
            self.get(template_item, parent=parent, loader=item_data)
            if template_item is not None:
                parent.add(template_item)
        #parent.delete(template)
        template.visible = False  # template  blijft in het model vanwege relatie-eigenschappen zoals start, limit...
        return parent

    def get_container(self, template, parent=None, data=None):
        for item in copy.copy(template.items):
            if item.kind == Template.VK_CONTAINER and not item.name:
                item_data = data
            else:
                item_name = item.name.split("/").pop()
                item_data = data.get(item_name)
            self.get(item, parent=template, loader=item_data)
        return template

    def get(self, template, parent=None, loader=None):
        #  Er is altijd een hoofd entiteit met een natuurlijke key. Bij de fiatteer widget
        #  is de medewerker de hoofd entiteit met daaraan gekoppeld de behandeldagen / verrichtingen
        #  die gefiatteerd moeten worden.
        if template.kind == Template.VK_CONTAINER:
            if loader is None:
                template = None
            #  Er zijn drie soorten containers:
            #  (1) Container zonder naam. Dit zijn visueel gegroepeerde velden van dezelfde
            #      entiteit als de parent.
            elif not template.name:
                template = self.get_visual_container(template, parent=parent, data=loader)
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

class SQLBinder(Binder):
    def __init__(self, template):
        super(SQLBinder, self).__init__(template)
        self.sql = None

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

    def create_sql(self, template):
        table = template.name
        fields = self.get_fields(template)
        if self.selection:
            where = "WHERE %s" % str(self.selection)
        else:
            where = ""
        sql = """SELECT %s
        FROM %s
        %s
        """ % (", ".join(fields), table, where)
        return sql

    def get_data(self):
        if self.sql is None:
            self.sql = self.create_sql(self.template)
        print(self.sql)

