from composability.registry import Registry
from composability.binder import Binder


class MockPatientBinder(Binder):
    def load_item(self, template, path, selection):
        super(MockPatientBinder, self).load_item(template, path, selection)
        if path == "patient":
            return dict(
                naam="Burgstra",
                voornaam="Henk",
                opmerkingen="Geen",
                postcode="1000 AA",
                woonplaats="Amsterdam"
            )
        elif path == "patient/behandelingen":
            return {}

r = Registry(".")
t = r.load_template("patient")
b = MockPatientBinder()
d = b.load(t)
print(d)
