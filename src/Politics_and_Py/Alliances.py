import collections.abc as collections
from .Core import Alliances_



class Alliances(collections.MutableSet):
    def __init__(self, *args):
        super(self).__init__()
        for arg in args:
            self.add(arg)

    def __contains__(self, item):
        return super(Alliances, self).__contains__(item)

    def __iter__(self):
        return super(Alliances, self).__iter__()

    def __len__(self):
        return super(Alliances, self).__len__()

    def add(self, value) -> None:
        super(Alliances, self).add(value)

    def discard(self, value) -> None:
        super(Alliances, self).discard(value)

    def __getitem__(self, item):
        return Alliances_[item]
