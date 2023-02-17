from src.Politics_and_Py import *
from config import Key
key(Key)
test_nation = Nation(54586)
# test Nation.update_long()
test_nation.update_long()
print(test_nation.cities)
print(Cities_)

#test Nations.update_long()
test_nations = Nations(152003, 54586)
test_nations.update_long()
print([nation for nation in test_nations.mapping.items()])
