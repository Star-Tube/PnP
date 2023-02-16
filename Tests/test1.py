# for now, you have to import using this line:
from src import Nation, _Nations
# import PnP

x = Nation(152003)

print("id check:")
print(id(x) == id(_Nations[152003]))

x.nation_name = "bob"

print("Attribute check:")
print(x.nation_name == _Nations[152003].nation_name)
