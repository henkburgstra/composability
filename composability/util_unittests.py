import unittest
from composability.util import *


class TestUtil(unittest.TestCase):
    def test_strip_key(self):
        for p in ("path(1)/with(2)/keys", "path(a)/with(b)/keys", "path(a-1)/with(b-2)/keys"):
            self.assertEqual("path/with/keys", strip_key(p))

    def test_path_info(self):
        p = PathInfo("this(1)/is(2)/a(3)/path(4)/name")
        self.assertEqual(p.field, "name")
        self.assertEqual(len(p.items), 4)
        self.assertEqual(p.keys["is"], "2")

    def test_dot_dict(self):
        d = DotDict(a=1, b=2, c=3)
        self.assertEqual(len(d.keys()), 3)
        self.assertEqual(d["a"], 1)
        self.assertEqual(d.c, 3)
