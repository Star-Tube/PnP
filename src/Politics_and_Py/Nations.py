import collections.abc as collections
from .Core import Nations_


class Nations(collections.MutableSet):
    def __init__(self, *args):
        super(Nations, self).__init__()
        self.set = ()
        for arg in args:
            self.add(arg)

    @staticmethod
    def update_long():
        Nations_.update_long()

    def __str__(self):
        return str(self.set)

    def __contains__(self, item):
        return super(Nations, self).__contains__(item)

    def __iter__(self):
        return super(Nations, self).__iter__()

    def __len__(self):
        return self.set.__len__()

    def add(self, value) -> None:
        self.set = self.set + (value,)
        Nations_.__setitem__()

    def discard(self, value) -> None:
        self.set.__delattr__(value)

    def __getattr__(self, item):
        return Nations_[item]

    def items(self):
        return [(nid, Nations_[nid]) for nid in self.set]
