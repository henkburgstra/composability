from composability.util import PathInfo


class Test(object):
    def __init__(self):
        self.data = dict()

    def to_dict(self, p):
        d = self.data
        for item in p.items[1:]:
            x = d.get(item, {})
            key = p.keys[item]
            y = x.get(key, {})
            x[key] = y
            d[item] = x
            d = y
        return d

    def set(self, pad, value):
        p = PathInfo(pad)
        d = self.to_dict(p)
        if p.field:
            d[p.field] = value

    def get(self, pad):
        p = PathInfo(pad)
        d = self.to_dict(p)
        if p.field:
            return d.get(p.field)




t = Test()
t.set("patient(1)/behandelingen(2)/behandeldagen(3)/datum", "2016-02-11")
t.set("patient(1)/adres", "dromedarisstraat")
t.set("patient(1)/behandelingen(2)/dummy", "")
print(t.get("patient(1)/behandelingen(2)/behandeldagen(3)/datum"))
print(t.get("patient(1)/adres"))