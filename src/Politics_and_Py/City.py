from .MultiIndex import MultiIndexable


class City(MultiIndexable):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_labels():
        return "foo", "bar"
