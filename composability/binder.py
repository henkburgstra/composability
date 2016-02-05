import copy

from .template import Template

class Binder(object):
    def __init__(self, template):
        self.template = template
        self.selection = None

    def load(self):
        t = self.load_template(self.template, selection=self.selection, data=None)
        return t

    def load_template(self, template, selection=None, data=None, anonymous=False):
        if data is None:
            t = copy.copy(template)
            data = self.load_data(template, selection=selection)
            t.name = "%s(%s)" % (t.name, data.get("key", "x"))  # TODO: uuid i.p.v. x
        else:
            t = template

        items = copy.copy(t.items)
        t.clear()
        self.load_template_items(t, items, selection=selection, data=data)
        if anonymous:
            t.name = "anon_"  # TODO: +uuid
        return t

    def load_template_items(self, template, items, selection=None, data=None):
        for item in items:
            item_t = copy.copy(item)
            if item_t.kind == Template.VK_CONTAINER:
                if item_t.name:
                    data_items = self.load_relationship_data(item_t, data)
                    for data_item in data_items:
                        item_t_copy = copy.copy(item_t)
                        item_t_copy.name = "%s/%s(%s)" % (template.name, item_t_copy.name, data_item.get("key", "x")) # TODO: uuid
                        rel_t = self.load_template(item_t_copy, data=data_item)
                        template.add(rel_t)
                    continue
                else:
                    item_t.name = template.name
                    item_t = self.load_template(item_t, selection=selection, data=data, anonymous=True)
            else:
                item_t.value = data.get(item_t.name)
            item_t.name = "%s/%s" % (template.name, item_t.name)
            template.add(item_t)


    def load_data(self, template, selection=None):
        return {}

    def load_relationship_data(self, template, parent_data):
        return []


    def load_item(self, template, path, selection):
        return {}



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

