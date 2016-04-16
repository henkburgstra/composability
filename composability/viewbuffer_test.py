import unittest
from viewbuffer import ViewBuffer, BufferList


class TestViewBuffer(unittest.TestCase):
    def test_buffer_list(self):
        bl = BufferList()
        key = "patient(1)/behandelingen(2)/behandeldagen(3)/datum"
        value = "2016-02-11"
        bl.set_value(key, value)
        b = bl.get_value(key)
        self.assertEqual(b, value)

    def test_dict_access(self):
        bl = BufferList()
        key = "patient(1)/behandelingen(2)/behandeldagen(3)/datum"
        value = "2016-02-11"
        bl.set_value(key, value)
        data = bl.data
        bd = data.behandelingen["2"].behandeldagen["3"]
        self.assertEqual(str(bd.datum), value)
