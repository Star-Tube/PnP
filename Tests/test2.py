# for now, you have to import using this line:
from src.Core import Treaty, _Treaties
# import PnP

x = Treaty(1)

print("id check:")
print(id(x) == id(_Treaties[1]))

x.type = "xyz"

print("Attribute check:")
print(x.type == _Treaties[1].type)
