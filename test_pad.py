from composability.util import PathInfo


class Test(object):
    def __init__(self):
        self.data = dict()

    def set(self, pad, value):
        pi = PathInfo(pad)
        d = self.data
        for item in pi.items[1:]:
            x = d.get("item", {})
            key = pi.keys[item]
            y = x.get(key, {})
            x[key] = y
            d[item] = x



t = Test()
t.set("patient(1)/behandelingen(2)/behandeldagen(3)/datum", "2016-02-11")
t.set("patient(1)/adres", "dromedarisstraat")
t.set("patient(1)/behandelingen(2)/dummy", "")
print(t.data)
x = {
    "adres": "dromedarisstraat",
    "behandelingen": {
        "2": {
            "dummy": "",
            "behandeldagen": {
                "3": {
                    "datum": "2016-02-11"
                }
            }
        }
    }
}