import wx
from composability.binder import Binder
from composability.registry import Registry
from composability.select import Or, Select
from composability.template import Template
from composability.wx_view import BoxPanel

class MockPatientBinder(Binder):

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
            return [dict(key="1", verwijzer="verwijzer #1"), dict(key="2", verwijzer="verwijzer #2")]
        if template.name == "behandeldagen":
            return [dict(key="1", datum="22-08-1965"), dict(key="2", datum="28-04-1971")]
        return []


r = Registry(".")
b = MockPatientBinder(r.load_template("patient"))
t = b.load()
app = wx.App(redirect=False)
frame = wx.Frame(None, title="Template Test", size=(600, 400))
sizer = wx.BoxSizer()
frame.SetSizer(sizer)
# ---
view = BoxPanel(frame, name="patient")
view.set_template(t)
view.render()
sizer.Add(view)
frame.Show()
#view.set_value("patient(1)/behandelingen(1)/begin", "11-11-2011")
app.MainLoop()