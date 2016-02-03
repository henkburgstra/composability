import wx
from composability.controller import Controller
from composability.loader import Loader
from composability.binder import Binder, SQLBinder
from composability.registry import Registry
from composability.wx_view import BoxPanel


class PatientBinder(SQLBinder):
    def __init__(self, template):
        import sqlite3
        conn = sqlite3.connect(":memory:")
        c = conn.cursor()
        c.execute("""
            CREATE TABLE patient
            (key int, naam text, voornaam text, opmerkingen text, postcode text, woonplaats)""")
        c.execute("""
            INSERT INTO patient
            VALUES (1, 'Burgstra', 'Henk', '', '1000 AA', 'Amsterdam')""")
        c.execute("""
            CREATE TABLE behandeling
            (key int, verwijzer text, patient_key int)""")
        c.execute("""
            INSERT INTO behandeling
            VALUES (1, 'verwijzer #1', 1)""")
        c.execute("""
            INSERT INTO behandeling
            VALUES (2, 'verwijzer #2', 1)""")
        c.execute("""
            CREATE TABLE behandeldag
            (key int, datum text, behandeling_key text)""")
        c.execute("""
            INSERT INTO behandeldag
            VALUES(1, '01-01-2015', 1)""")
        c.execute("""
            INSERT INTO behandeldag
            VALUES(2, '02-01-2015', 1)""")
        c.execute("""
            INSERT INTO behandeldag
            VALUES(3, '03-01-2015', 2)""")
        c.execute("""
            INSERT INTO behandeldag
            VALUES(4, '04-01-2015', 2)""")
        conn.commit()
        self.conn = conn
        super(PatientBinder, self).__init__(template)
        self.loader = {
            "key": "1",
            "naam": "Burgstra",
            "voornaam": "Henk",
            "postcode": "1000 AA",
            "behandelingen": {
                    "items": [
                    {
                        "key": "1",
                        "metingen": {
                          "items": []
                        },
                        "behandeldagen": {
                            "items": [
                                {
                                    "key": "1",
                                    "datum": "22-08-1965"
                                },
                                {
                                    "key": "2",
                                    "datum": "05-03-1980"
                                }
                            ]
                        }
                    },
                    {
                        "key": "2",
                        "behandeldagen": {
                            "items": [
                                {
                                    "key": "3",
                                    "datum": "22-08-1965"
                                },
                                {
                                    "key": "4",
                                    "datum": "05-03-1980"
                                }
                            ]
                        }
                    }
                ]
            }
        }

    def get_data(self):
        super(PatientBinder, self).get_data()
        return self.loader

class TestBinder(Binder):
    def get_data(self):
        super(TestBinder, self).get_data()


if __name__ == "__main__":
    from composability.view import Or, Select
    view_registry = Registry("d:/projecten/python/validaties")
    app = wx.App(redirect=False)
    frame = wx.Frame(None, title="Template Test", size=(600, 400))
    sizer = wx.BoxSizer()
    frame.SetSizer(sizer)
    # ---
    view = BoxPanel(frame, name="patient")
    binder = Binder(view_registry.load_template("patient"), Loader())
    controller = Controller(view, binder)
    key = Select("patient/key")
    naam = Select("patient/naam")
    controller.select(Or(key.Eq("ACTB-T123456"), naam.Gte("Burg")))
    controller.load_view()
    view.set_value("patient(1)/behandelingen(1)/behandeldagen(2)/datum", "11-11-2011")
    sizer.Add(view)
    frame.Show()
    #view.remove("patient(1)/behandelingen(1)")
    app.MainLoop()
