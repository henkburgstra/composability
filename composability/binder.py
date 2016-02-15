import copy
import uuid

from .view import View
from composability.viewbuffer import BufferList


class Binder(object):
    """
    Binder binds data to a template
    """
    def __init__(self, template):
        self.template = template
        self.selection = None
        self.buffers = BufferList()

    def get_template(self, name=None):
        if name is None:
            return self.template
        else:
            return self.template.get(name)

    def load(self):
        """
        Call load_template to load data and bind it to a template.
        :return: a Template instance filled with data.
        """
        t = self.load_template(self.template, selection=self.selection, data=None)
        return t

    def load_template(self, template, selection=None, data=None, anonymous=False):
        """
        Load data and bind it to a template
        @param template: Template instance to fill
        @param selection: Select instance used to select data
        @param data:data to bind to template
        @param anonymous:specified that the template is anonymous: a nameless container to visually group elements
        @return: a Template instance filled with data
        """
        if data is None:
            t = copy.copy(template)
            data = self.load_data(template, selection=selection)
            key_value = self.data_get_key_value(t, data)
            if not key_value:
                key_value = str(uuid.uuid1())
            t.name = "%s(%s)" % (t.name, key_value)
        else:
            t = template

        items = copy.copy(t.items)
        t.clear()
        self.load_template_items(t, items, selection=selection, data=data)
        if anonymous:
            t.name = "anon_" + str(uuid.uuid1())
        return t

    def load_template_items(self, template, items, selection=None, data=None):
        items = self.filter_template_items(template, items, selection=selection, data=data)
        for item in items:
            item_t = copy.copy(item)
            value = None
            if item_t.kind == View.VK_CONTAINER:
                if item_t.name:
                    for rel_t in self.load_relationship_items(item_t, template.name, data):
                        template.add(rel_t)
                    continue
                else:
                    item_t.name = template.name
                    item_t = self.load_template(item_t, selection=selection, data=data, anonymous=True)
            else:
                value = self.data_get_value(item_t, data)
                if item_t.kind == View.VK_COMBO:
                    combo_options = self.load_combo_options(item_t, data)
                    if combo_options is None:
                        combo_options = []
                    item_t.options = combo_options

            item_t.name = "%s/%s" % (template.name, item_t.name)

            if item_t.kind != View.VK_CONTAINER:
                self.buffers.set_value(item_t.name, value, item_t.kind)
                item_t.value = self.buffers.get_display(item_t.name)

            template.add(item_t)

        self.after_load_template_items(template, items, selection=selection, data=data)

    def filter_template_items(self, template, items, selection=None, data=None):
        return items

    def after_load_template_items(self, template, items, selection=None, data=None):
        pass

    def load_data(self, template, selection=None):
        return {}

    def load_relationship_items(self, template, parent_name, parent_data):
        items = []
        for data in self.load_relationship_data(template, parent_data):
            t_copy = copy.copy(template)
            key_value = self.data_get_key_value(t_copy, data)
            if not key_value:
                key_value = str(uuid.uuid1())
            t_copy.name = "%s/%s(%s)" % (parent_name, t_copy.name, key_value)
            t = self.load_template(t_copy, data=data)
            items += [t]
        return items

    def load_relationship_data(self, template, parent_data):
        return []

    def load_combo_options(self, template, data):
        """
        Load the options for a combobox.
        @param template: Template instance
        @param data: data instance
        @return: overridden methods should return a list of tuples. The tuples should contain a key and description:
        [("T", "Tomato"), ("P", "Potato")]
        """
        return []

    def data_get_value(self, template, data):
        """
        Get a single value from data. The default implementation assumes that @param data is a dictionary-like
        object, Override this method if @param data is not dictionary-like
        @param template: Template instance
        @param data: data to get the value from
        @return: value
        """
        return data.get(template.name)

    def data_get_key_value(self, template, data):
        """
        Get the key value from @param data. The default implementation assumes that @param data is a dictionary-like
        object and that the key name is "key". Override this method if @param data is not dictionary-like
        or if the key name is different from "key".
        @param template: Template instance
        @param data: data to get the key value from
        @return: key value
        """
        return data.get("key")


    def get_fields(self, template):
        fields = []
        for item in template.items:
            if item.kind == View.VK_CONTAINER:
                # container is een visuele groep, velden doen mee voor deze tabel.
                if not item.name:
                    fields += self.get_fields(item)
            else:
                if item.kind not in (View.VK_BUTTON,):
                    fields += [item.name] # TODO virtuele velden etc. uitsluiten

        return fields


class SQLBinder(Binder):
    def __init__(self, template):
        super(SQLBinder, self).__init__(template)
        self.sql = None

    def get_fields(self, template):
        fields = []
        for item in template.items:
            if item.kind == View.VK_CONTAINER:
                # container is een visuele groep, velden doen mee voor deze tabel.
                if not item.name:
                    fields += self.get_fields(item)
            else:
                if item.kind not in (View.VK_BUTTON,):
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

