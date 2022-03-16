import PnP

# Set Key
PnP.key(input("Please input api key: "))

# Gather Requirements and Message information
min_cities = input("Please input minimum city count: ")
message = input("Please input message: \n")
subject = input("Please input subject: ")
requirements = f"alliance_id:0, min_cities: {min_cities}"

# Define a Nations() object to hold all our nations' data
nations = PnP.Nations()

# Use Nations.update_short() with static set to False to gather all valid nations to send the recruitment message to
nations.update_short(static=False, requirements=requirements)

# Use send_message() to finally send all the messages. It will iterate over the messages and send them all very quickly
PnP.send_message(nations, message, subject)

