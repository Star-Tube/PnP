from src.Politics_and_Py import *
from config import Key
key(Key)

test_nation = Nation(54586)
# test Nation.update_long()
test_nation.update_long()
print(f"test_nation: {test_nation.cities.items()}")
print("Cities_: ", Cities_)
print()

#  test Nations.update_long()
test_nations = Nations(152003, 54586)
print(test_nations)
test_nations.update_long()
print(test_nations.items())
print(Nations_)
print()

#  test Alliance.update_long()
test_alliance = Alliance(7450)
print(test_alliance)
test_alliance.update_long()
print(test_alliance)
print(test_alliance.nations)
print(test_alliance.treaties)
print(Nations_)
print(Treaties_)
