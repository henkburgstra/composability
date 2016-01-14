class Loader(object):
    def __init__(self):
        self.data = None
        self.name = None
        self.fields = None
        self.selection = None
        self.sql = None
        items = {}  # key: path, item: Loader instance or

    def set_name(self, name):
        self.name = name

    def set_fields(self, fields):
        self.fields = fields

    def select(self, selection):
        self.selection = selection

    def get(self, path):
        """
        :param path:
        :param parent:
        :return:
        """
        if not self.sql:
            self.create_sql()

    def load(self):
        if self.sql is None:
            self.create_sql()

    def create_sql(self):
        if self.selection:
            where = "WHERE %s" % str(self.selection)
        else:
            where = ""
        sql = """SELECT %s
        FROM %s
        %s
        """ % (", ".join(self.fields), self.name, where)
        return sql
