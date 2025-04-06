# for now you have to import using this line:
from src.Politics_and_Py import Core as PnP_Core
from src.Politics_and_Py import Config as PnP_Config


def main(nid: int):
    # Get a Nation() object of the client
    user = PnP_Core.Nation(nid)
    user.update_long()

    for insufficient_mil in user.mmr_check(mmr):
        print(f"{user} has insufficient {insufficient_mil}")


    for cid, city in user.cities.items():
        if city.infra % 250 != 0:
            print(city, " has ", city.infra, " infra. This is not good.")
        if city.land % 400 != 0 and city.land % 500 != 0:
            print(city, " has ", city.land, " land. This is not ideal.")
        if not city.powered:
            print(city, " is not powered. This is not good.")

    print()





if __name__ == "__main__":
    PnP_Config.key(input("Please input api key:\n"))
    mmr = input("Please input mmr requirement as 4 numerals (e.g. 0351):\n")
    while True:
        main(int(input("What is your Nation ID?\n").strip()))
