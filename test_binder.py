import wx
from composability.binder import Binder
from composability.controller import Controller
from composability.registry import Registry
from composability.util import strip_key
from composability.select import Or, Select
from composability.template import Template
from composability.wx_view import BoxPanel

class MockPatientBinder(Binder):
    b = -1
    d = -1
    def load_data(self, template, selection=None):
        if template.name == "patient":
            return dict(
                key="1",
                naam="Burgstra",
                voornaam="Henk",
                opmerkingen="Geen",
                postcode="1000 AA",
                woonplaats="Amsterdam"
            )

    def load_relationship_data(self, template, parent_data):
        if template.name == "behandelingen":
            self.b += 2
            return [dict(key=str(self.b), verwijzer="verwijzer #1"), dict(key=str(self.b+1), verwijzer="verwijzer #2")]
        if template.name == "behandeldagen":
            self.d += 2
            return [dict(key=str(self.d), datum="22-08-1965"), dict(key=str(self.d+1), datum="28-04-1971")]
        if template.name == "pager":
            return [{}] # teruggeven van data zorgt ervoor dat de "pager" afgebeeld wordt.
        return []


class PatientController(Controller):
    def view_left_clicked(self, src, msg):
        a_path = strip_key(src)
        if a_path == "patient/opslaan":
            pass
        elif a_path == "patient/pager/bijladen":
            self.load_behandelingen()
        elif a_path == "patient/behandelingen/verwijderen":
            self.view.remove(msg.data["view"].Name)

    def load_behandelingen(self):
        behandelingen_t = self.binder.get_template("behandelingen")
        if behandelingen_t is None:
            return
        for t in self.binder.load_relationship_items(behandelingen_t, "patient(1)", {}):
            if t is not None:
                self.view.add(t)


app = wx.App(redirect=False)
frame = wx.Frame(None, title="Template Test", size=(800, 600))
sizer = wx.BoxSizer()
frame.SetSizer(sizer)

######################################################################
r = Registry(".")
view = BoxPanel(frame, name="patient")
b = MockPatientBinder(r.load_template("patient"))
t = b.load()
controller = PatientController(view, b)
controller.load_view()
######################################################################

# view.set_template(t)
# view.render()
sizer.Add(view)
frame.Show()
app.MainLoop()