# for now you have to import using this line:
from src.Politics_and_Py import \
    Core as PnP

# import PnP

# Set Key
PnP.key(input("Please input api key: "))

# Get a Nation() object of the user
User = PnP.Nation(input("What is your Nation ID?"))
User.update_short()

# Find war range
war_range = User.war_range()

# Define a Nations() object to use for holding potential targets
nations = PnP.Nations()

# Define requirements for potential war targets
requirements = ""

# Update list to contain war targets
nations.update_short(static=False, requirements=requirements)

