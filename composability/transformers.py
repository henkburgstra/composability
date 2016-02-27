import re

dd_mm_yyyy = re.compile("(\d{1,2})(-|/)(\d{1,2})(-|/)(\d{4})")
yyyy_mm_dd = re.compile("(\d{4})(-|/)(\d{1,2})(-|/)(\d{1,2})")


class Transform(object):
    def __init__(self, value, **kwargs):
        self._value = value
        for k, v in kwargs.items():
            setattr(self, "_%s" % k, v)

    def __str__(self):
        return self._value

    def display(self):
        if self._value is None:
            return ""
        return self._value

    def store(self):
        return self._value


class TransformDate(Transform):
    def __init__(self, value, **kwargs):
        super(TransformDate, self).__init__(value, **kwargs)
        if getattr(self, "_y", None) is None or getattr(self, "_m", None) is None or getattr(self, "_d", None) is None:
            m = dd_mm_yyyy.match(value)
            if m is not None:
                self._d = int(m.group(1))
                self._m = int(m.group(3))
                self._y = int(m.group(5))
                return
            m = yyyy_mm_dd.match(value)
            if m is not None:
                self._y = int(m.group(1))
                self._m = int(m.group(3))
                self._d = int(m.group(5))
                return

    def __str__(self):
        return self.display()

    @classmethod
    def fromYMD(cls, y, m, d):
        return cls("%04d-%02d-%02d" % (y, m, d), y=y, m=m, d=d)

    def d(self):
        return self._d

    def m(self):
        return self._m

    def y(self):
        return self._y

    def display(self):
        return "-".join(["%02d" % self._d, "%02d" % self._m, "%04d" % self._y])

    def store(self):
        return "-". join(["%04d" % self._y, "%02d" % self._m, "%02d" % self._d])