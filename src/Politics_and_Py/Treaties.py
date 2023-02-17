import collections.abc as collections
from .Core import Treaties_


class Treaties(collections.MutableSet):
    def __init__(self, *args):
        super(Treaties, self).__init__()
        self.set = ()
        for arg in args:
            self.add(arg)

    @staticmethod
    def update_long():
        Treaties_.update_long()

    def __str__(self):
        return str(self.set)

    def __contains__(self, item):
        return super(Treaties, self).__contains__(item)

    def __iter__(self):
        return super(Treaties, self).__iter__()

    def __len__(self):
        return self.set.__len__()

    def add(self, value) -> None:
        self.set = self.set + (value,)
        Treaties_.__setitem__(tid=value)

    def discard(self, value) -> None:
        self.set.__delattr__(value)

    def __getattr__(self, item):
        return Treaties_[item]

    def items(self):
        return [(tid, Treaties_[tid]) for tid in self.set]
