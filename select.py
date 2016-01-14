class Connective(object):
    """
    A Connective instance joins two operands with a logical operator.
    An operand can either be a Select instance or another Connective instance.
    """
    def __init__(self, operator, *operands):
        self.operator = operator
        self.operands = operands

    def __str__(self):
        return "(%s)" % (" %s " % self.operator).join([str(operand) for operand in self.operands])

def And(*ops):
    return Connective("AND", *ops)

def Or(*ops):
    return Connective("OR", *ops)


class Param(object):
    def __init__(self, operator=None, value=None, values=None):
        self.operator = operator
        self.value = value
        if values is None:
            self.values = []
        else:
            self.values = values

    def __str__(self):
        if self.operator in ("IN", "NOT IN"):
            if type(self.values[0]) in (str, unicode):
                template = "'%s'"
            else:
                template = "%s"
            return "%s (%s)" % (self.operator, ", ".join([template % value for value in self.values]))

        if self.value is None:
            value = "<empty>"
        elif type(self.value) in (str, unicode):
            value = "'%s'" % self.value
        else:
            value = "%s" % self.value
        return "%s %s" % (self.operator, value)


class Select(object):
    """
    Select represents an entity item identified by a path and optionally a parameter.
    @path string
    @param Param
    """
    def __init__(self, path, param=None):
        self.path = path
        self.param = param

    def __str__(self):
        return "%s %s" % (self.translate(self.path), self.param)

    def translate(self, path):
        e = self.path.split("/")
        return "%s.%s" % (e[len(e) - 2], e[len(e) - 1])

    def Eq(self, value):
        return Select(self.path, param=Param(operator="=", value=value))

    def Ne(self, value):
        return Select(self.path, param=Param(operator="!=", value=value))

    def Gt(self, value):
        return Select(self.path, param=Param(operator=">", value=value))

    def Gte(self, value):
        return Select(self.path, param=Param(operator=">=", value=value))

    def Lt(self, value):
        return Select(self.path, param=Param(operator="<", value=value))

    def Lte(self, value):
        return Select(self.path, param=Param(operator="<=", value=value))

    def In(self, *values):
        return Select(self.path, param=Param(operator="IN", values=values))

    def Nin(self, *values):
        return Select(self.path, param=Param(operator="NOT IN", values=values))

if __name__ == "__main__":
    naam = Select("patient/naam")
    postcode = Select("patient/postcode")
    leeftijd = Select("patient/leeftijd")
    geslacht = Select("patient/geslacht")
    bejaarden = Or(
        And(geslacht.Eq("M"), leeftijd.Gte(67)),
        And(geslacht.Eq("V"), leeftijd.Gte(65))
    )

    print(Or(And(naam.Eq("henk"), postcode.Eq("1338 HS")), bejaarden, leeftijd.In(3, 5, 9)))