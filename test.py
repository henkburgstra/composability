from registry import Registry
from binder import Binder

r = Registry(".")
t = r.load_template("patient")
b = Binder()
d = b.load(t)
print(d)
