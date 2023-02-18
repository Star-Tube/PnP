from .MultiIndex import MultiIndexable, MultiIndex


class Treaty(MultiIndexable):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_labels():
        return "foo", "bar"
