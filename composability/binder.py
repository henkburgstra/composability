import copy
import uuid

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
            t.name = "%s(%s)" % (t.name, data.get("key", uuid.uuid1()))
        else:
            t = template

        items = copy.copy(t.items)
        t.clear()
        self.load_template_items(t, items, selection=selection, data=data)
        if anonymous:
            t.name = "anon_" + uuid.uuid1()
        return t

    def load_template_items(self, template, items, selection=None, data=None):
        for item in items:
            item_t = copy.copy(item)
            if item_t.kind == Template.VK_CONTAINER:
                if item_t.name:
                    data_items = self.load_relationship_data(item_t, data)
                    for data_item in data_items:
                        item_t_copy = copy.copy(item_t)
                        item_t_copy.name = "%s/%s(%s)" % (template.name, item_t_copy.name,
                                                          data_item.get("key", uuid.uuid1()))
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

