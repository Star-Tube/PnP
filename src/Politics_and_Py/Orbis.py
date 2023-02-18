from .MultiIndex import MultiIndex
from .Alliance import Alliance
from .Nation import Nation
from .City import City
from .Treaty import Treaty

from .Utils import get_v3


class Orbis:
    def __init__(self):
        self.treaties = MultiIndex(Treaty)
        self.cities = MultiIndex(City)
        self.nations = MultiIndex(Nation)
        self.alliances = MultiIndex(Alliance)

    def test(self):
        key = input("Your key is: ")
        get_v3()


if __name__ == "__main__":
    orbis = Orbis()
    orbis.test()
