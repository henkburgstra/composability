class Transform(object):
    def __init__(self, value, **kwargs):
        self._value = value
        for k, v in kwargs.items():
            self.k = v

    def display(self):
        if self._value is None:
            return ""
        return self._value

    def store(self):
        return self._value


class TransformDate(Transform):
    def display(self):
        if self._value is None:
            return ""
        # TODO: robuuster maken
        y, m, d = self._value.split("-")
        return "-".join[d, m, y]

    def store(self):
        # TODO: robuuster maken
        d, m, y = self._value.split("-")
        return "-". join[y, m, d]