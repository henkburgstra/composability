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

class MockPatientBinder(Binder):
    def load_data(self, template, selection=None):
        if template.name == "patient":
            return dict(
                key="1",
                naam="Henk Burgstra",
                geboortedatum="1965-08-22",
                geslacht="M",
                voornaam="Henk",
                eigen_naam="Burgstra",
                huisarts="2",
                opmerkingen="Geen",
                postcode="1000 AA",
                woonplaats="Amsterdam"
            )

    def load_relationship_data(self, template, parent_data):
        if template.name == "behandelingen":
            return [dict(key=str(uuid.uuid1()), verwijzer="verwijzer #1"), dict(key=str(uuid.uuid1()), verwijzer="verwijzer #2")]
        if template.name == "behandeldagen":
            return [dict(key=str(uuid.uuid1()), datum="22-08-1965"), dict(key=str(uuid.uuid1()), datum="28-04-1971")]
        if template.name == "pager":
            return [{}] # teruggeven van data zorgt ervoor dat de "pager" afgebeeld wordt.
        return []

    def load_combo_options(self, template, data):
        if template.name.endswith("geslacht"):
            return [("0", "Onbekend"), ("M", "Mannelijk"), ("V", "Vrouwelijk")]
        if template.name.endswith("huisarts"):
            return [("1", "Jansen"), ("2", "Pietersen"), ("3", "Klaasen")]
        elif template.name.endswith("sjabloon"):
            return [("A", "Sjabloon A"), ("B", "Sjabloon B")]


class PatientController(Controller):
    @property
    def patient(self):
        return self.binder.buffers.data

    def view_left_clicked(self, src, msg):
        a_path = strip_key(src)
        if a_path == "patient/opslaan":
            pass
        elif a_path == "patient/invoegen":
            self.invoegen()
        elif a_path == "patient/pager/bijladen":
            self.load_behandelingen()
        elif a_path == "patient/behandelingen/verwijderen":
            self.view.remove(msg.data["view"].Name)

    def view_changed(self, src, msg):
        super(PatientController, self).view_changed(src, msg)
        print (msg.data.get("value"))
        if src.endswith(")/huisarts"):
            print(msg.data.get("value"))

    def invoegen(self):
        text = Template(kind=View.VK_TEXT, name="patient(1)/ingevoegd", title="Ingevoegd")
        self.view.insert(text, Template.POS_AFTER, "patient(1)/invoegen")

    def load_behandelingen(self):
        behandelingen_t = self.binder.get_template("behandelingen")
        if behandelingen_t is None:
            return
        for t in self.binder.load_relationship_items(behandelingen_t, "patient(1)", {}):
            if t is not None:
                self.view.add(t)


class MockMetingBinder(Binder):
    def load_data(self, template, selection=None):
        return {}

    def load_data(self, template, selection=None):
        return {}

    def load_relationship_data(self, template, parent_data):
        return [dict(key=str(uuid.uuid1()), datum="22-08-1965"), dict(key=str(uuid.uuid1()), datum="28-04-1971")]


class MetingController(Controller):
    @property
    def meting(self):
        return self.binder.buffers.data

    def view_changed(self, src, msg):
        print("meting gewijzigd")


app = wx.App(redirect=False)
locale = wx.Locale(wx.LANGUAGE_DUTCH)  # belangrijk voor o.a. DatePickerCtrl
frame = wx.Frame(None, title="Template Test", size=(900, 600))
sizer = wx.BoxSizer()
frame.SetSizer(sizer)

######################################################################
r = Registry(".")
view = BoxPanel(frame, name="patient")
b = MockPatientBinder(r.get_template("patient"))
mb = MockMetingBinder(r.get_template("meting"))
mb.buffers = b.buffers  # zorg dat patient.behandelingen.metingen beschikbaar komt.
controller = PatientController(b, view=view)
m_controller = MetingController(mb)
controller.register_controller("patient/behandelingen/metingen", m_controller)
key = Select("patient/key")
naam = Select("patient/naam")
# selection = Or(key.Eq("ACTB-T123456"), naam.Gte("Burg"))
controller.select(Or(key.Eq("ACTB-T123456"), naam.Gte("Burg")))
controller.load_view()
######################################################################

patient = controller.patient

sizer.Add(view)
frame.Show()
app.MainLoop()

print("------------")
for behandeling in patient.behandelingen.values():
    for behandeldag in behandeling.behandeldagen.values():
        print(behandeldag.datum.get_display())
        print(behandeldag.datum)  # bij gratie van __str__
    for meting in behandeling.metingen.values():
        print(meting.datum.get_display())
