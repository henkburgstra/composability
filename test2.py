import wx
from composability.binder import Binder
from composability.registry import Registry
from composability.select import Or, Select
from composability.template import Template
from composability.view import View
from composability.wx_view import BoxPanel

class MockPatientBinder(Binder):
    def load_item(self, template, path, selection):
        super(MockPatientBinder, self).load_item(template, path, selection)
        if path == "patient":
            return dict(
                key="1",
                naam="Burgstra",
                voornaam="Henk",
                opmerkingen="Geen",
                postcode="1000 AA",
                woonplaats="Amsterdam"
            )
        elif path == "patient/behandelingen":
            return {}

r = Registry(".")
t = Template(kind=View.VK_CONTAINER, name="patient(1)", attributes=dict(orientation=Template.ORI_VERTICAL,
    display=Template.DISP_INLINE, background_colour="#e6e5a8"))
t.add(Template(kind=View.VK_TEXT, name="patient(1)/naam", title="naam", value="Burgstra"))
adres = Template(kind=View.VK_CONTAINER, attributes=dict(orientation=Template.ORI_VERTICAL, display=Template.DISP_INLINE))
t.add(adres)
adres.add(Template(kind=View.VK_TEXT, name="patient(1)/straat", title="straat", value="Straat"))
behandeling1 = Template(kind=View.VK_CONTAINER, name="patient(1)/behandelingen(1)",
    attributes=dict(orientation=Template.ORI_VERTICAL, display=Template.DISP_RIGHT, background_colour="#c8e6be"))
t.add(behandeling1)
behandeling1.add(Template(kind=View.VK_TEXT, name="patient(1)/behandelingen(1)/begin", title="begin", value="01-01-2016"))
behandeling1.add(Template(kind=View.VK_TEXT, name="patient(1)/behandelingen(1)/eind", title="eind", value="31-05-2016"))
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
view.set_value("patient(1)/behandelingen(1)/begin", "11-11-2011")
app.MainLoop()