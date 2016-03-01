import uuid
import wx
from composability.binder import Binder
from composability.controller import Controller
from composability.registry import Registry
from composability.util import strip_key
from composability.select import Or, Select
from composability.template import Template
from composability.view import View
from composability.wx_view import BoxPanel

class MockBezoekBinder(Binder):
    def load_data(self, template, selection=None):
        if template.name == "bezoek":
            return dict(
                key="1",
                datum="2016-02-29"
            )

    def load_relationship_data(self, template, parent_data):
        if template.name == "verrichtingen":
            return [dict
                (
                    key=str(uuid.uuid1()), verrichting="verrichting #1"
                ), dict(
                    key=str(uuid.uuid1()), verrichting="verrichting #2"
                )
            ]
        return []

    def load_combo_options(self, template, data):
        if template.name.endswith("verrichting_selectie"):
            return [("A702", "Gehoor Audiometrie"), ("A704", "Spraak Audiometrie")]


class BezoekController(Controller):
    @property
    def Bezoek(self):
        return self.binder.buffers.data


app = wx.App(redirect=False)
locale = wx.Locale(wx.LANGUAGE_DUTCH)  # belangrijk voor o.a. DatePickerCtrl
frame = wx.Frame(None, title="Template Test", size=(900, 600))
sizer = wx.BoxSizer()
frame.SetSizer(sizer)

######################################################################
r = Registry(".")
view = BoxPanel(frame, name="bezoek")
b = MockBezoekBinder(r.get_template("bezoek"))
controller = BezoekController(b, view=view)
controller.load_view()
######################################################################
sizer.Add(view)
frame.Show()
app.MainLoop()
