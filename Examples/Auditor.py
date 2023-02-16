# for now you have to import using this line:
from src import \
    Core as PnP

# import PnP

# Set Key
PnP.key(input("Please input api key: "))

# Get a Nation() object of the user
User = PnP.Nation(input("What is your Nation ID?"))
User.update_long()

