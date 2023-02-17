import collections.abc as collections
from .Core import Cities_


class Cities(collections.MutableSet):
    def __init__(self, *args):
        super(Cities, self).__init__()
        self.set = ()
        for arg in args:
            self.add(arg)

    @staticmethod
    def update_short(cities=None):
        Cities_.update_short(cities=cities)

    def __str__(self):
        return f"{self.set}"

    def __repr__(self):
        return str(self.set)

    def __contains__(self, item):
        return super(Cities, self).__contains__(item)

    def __iter__(self):
        return super(Cities, self).__iter__()

    def __len__(self):
        return self.set.__len__()

    def items(self):
        return [(cid, Cities_[int(cid)]) for cid in self.set]

    def add(self, value) -> None:
        self.set = self.set + (value,)
        Cities_.__setitem__(cid=value)

    def discard(self, value) -> None:
        super(Cities, self).discard(value)
