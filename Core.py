# Imports
import requests
import json
import collections.abc as collections
from typing import Union

# Global Functions

def key(_):
    """Used to define the api key to be used"""
    global _Key
    _Key = _


def send_message(to, message, subject):
    """
    Takes in recipient, message and subject and sends the message. Returns any response to the action.

    :param to:
    :param message:
    :param subject:
    :return:
    """
    url = "https://politicsandwar.com/api/send-message/"
    if type(to) is Nation:
        payload = {"key": _Key, "to": to.nid, "message": message, "subject": subject}
        response = json.loads(requests.post(url, payload).text)
        return response
    elif type(to) is Nations:
        for nation in to:
            payload = {"key": _Key, "to": nation.nid, "message": message, "subject": subject}
            response = json.loads(requests.post(url, payload).text)
            yield response


def get(url, payload=None):
    """
    Used to make a call to an API.

    :param payload:
    :param url:
    :return:
    """
    response = json.loads(requests.post(url, json=payload).text)
    if "errors" in response.keys():
        raise InvalidRequest(response)
    return response


def get_v3(request):
    url = f"https://api.politicsandwar.com/graphql?api_key={_Key}"
    payload = {"query": request}
    response = get(url, payload)
    return response["data"]


def get_bankrecs(nation=None, nid=None):
    if nid is None:
        nid = nation.nid
    return get_v3(f"query{{bankrecs(or_id:{nid}){{data{{id, date, sid, stype, rid, rtype, pid, note, money, coal, oil, uranium, iron, bauxite, lead, gasoline, munitions, steel, aluminum, food, tax_id}}}}}}")['bankrecs']['data']


# Classes


class City:
    """
    City(cid=123)

    Used to store, retrieve update and calculate information about a city.
    """

    __slots__ = "cid", "name", "infra", "land", "nid", "powered", "founded", "imps", "coal_power_plant", \
        "oil_power_plant", "wind_power_plant", "nuclear_power_plant", "coal_mine", "oil_well", "uranium_mine", "farm", \
        "police_station", "barracks", "hospital", "recycling_center", "subway", "supermarket", "bank", "mall", \
        "stadium", "lead_mine", "iron_mine", "bauxite_mine", "gas_refinery", "aluminium_refinery", "steel_mill", \
        "munitions_factory", "factory", "airforcebase", "drydock", "pollution", "disease", "population", "commerce", \
        "crime", "age", "daily_gross_income", "revenue"

    def __init__(self, cid):
        self.cid = cid


class Cities(collections.MutableMapping):
    """
    Cities([123, 456])

    Used to store multiple City()'s and manage them more conveniently.
    """

    def __init__(self, *args, **kwargs):
        self.mapping = {}
        self.update(kwargs)
        for arg in args:
            self.__setitem__(arg, City(arg))

    def __iter__(self):
        return self.mapping.__iter__()

    def __len__(self) -> int:
        return len(self.mapping.keys())

    def __setitem__(self, cid=None, city=None) -> None:
        if city:
            if type(city) is City:
                if city.nid:
                    if cid:
                        if city.nid == cid:
                            self.mapping[cid] = city
                        else:
                            raise WrongCID
                    else:
                        self.mapping[city["nid"]] = city
                else:
                    raise NoCID
            else:
                raise TypeError
        elif type(cid) is int:
            self.mapping[cid] = City(cid)
        elif type(cid) is str:
            if cid.isnumeric():
                self.mapping[int(cid)] = City(int(cid))
            else:
                raise WrongCID
        else:
            raise ValueError

    def __getitem__(self, nid: Union[int, str]):
        if type(nid) is int:
            return self.mapping[nid]
        elif type(nid) is str:
            if nid.isnumeric():
                return self.mapping[int(nid)]

    def __delitem__(self, nid):
        value = self[nid]
        del self.mapping[nid]
        self.pop(value, None)


class Nation:
    __slots__ = "nid", "nation_name", "leader_name", "continent", "war_policy", "dom_policy", "colour", "score", \
                "population", "flag", "vacation", "beige", "projects", "alliance_id", "alliance_position", \
                "espionage", "login", "mil", "soldiers", "tanks", "planes", "ships", "missiles", "nukes", "treasures", \
                "cities"

    def __init__(self, nid=None):
        self.nid = nid

    def update_long(self, nation=None):
        if nation is None:
            request = f"""{{
                            nations(id: {[self.nid]} first:100){{data {{
                                id, alliance_id, alliance_position, nation_name, leader_name, continent, warpolicy, 
                                dompolicy, color, score, population, flag, vmode, beigeturns, espionage_available, 
                                last_active, soldiers, tanks, aircraft, ships, missiles, nukes, treasures {{name}}, 
                                ironw, bauxitew, armss, egr, massirr, itc, mlp, nrf, irond, vds, cia, cfce, propb, uap, 
                                city_planning, adv_city_planning, space_program, spy_satellite, moon_landing, 
                                pirate_economy, recycling_initiative, telecom_satellite, green_tech, arable_land_agency, 
                                clinical_research_center, specialized_police_training, adv_engineering_corps
                                cities{{
                                    id, name, date, infrastructure, land, powered, oilpower, windpower, coalpower, 
                                    nuclearpower, coalmine, oilwell, uramine, barracks, farm, policestation, hospital, 
                                    recyclingcenter, subway, supermarket, bank, mall, stadium, leadmine, ironmine, 
                                    bauxitemine, gasrefinery, aluminumrefinery, steelmill, munitionsfactory, factory, 
                                    airforcebase, drydock, date
                                }}
                            }}}}
                        }}"""
            nation = get_v3(request)['nations']['data'][0]
        cities = nation.pop("cities")
        self.update_short(nation)
        self.cities.update_long(cities=cities, projects=[x for x in [x for x, y in self.projects.items() if y is True] if x in ["recycling_initiative", "emergency_gasoline_reserve", "ironworks", "bauxiteworks", "arms_stockpile", "uranium_enrichment_program", "mass_irrigation", "international_trade_center", "clinical_research_center", "specialized_police_training_program", "telecoms_satellite", "green_technology"]])

    def update_short(self, nation=None):
        if nation is None:
            request = f"""{{
                nations(id: {[self.nid]} first:100){{data {{
                id, alliance_id, alliance_position, nation_name, leader_name, continent, warpolicy, dompolicy, color, 
                score, population, flag, vmode, beigeturns, espionage_available, last_active, soldiers, tanks, aircraft, 
                ships, missiles, nukes, treasures {{name}}, ironw, bauxitew, armss, egr, massirr, itc, mlp, nrf, irond, 
                vds, cia, cfce, propb, uap, city_planning, adv_city_planning, space_program, spy_satellite, 
                moon_landing, pirate_economy, recycling_initiative, telecom_satellite, green_tech, arable_land_agency, 
                clinical_research_center, specialized_police_training, adv_engineering_corps}}}}
            }}"""
            nation = get_v3(request)['nations']['data'][0]
        self.nation_name = nation.pop("nation_name")
        self.leader_name = nation.pop("leader_name")
        self.continent = nation.pop("continent")
        self.war_policy = nation.pop("warpolicy")
        self.dom_policy = nation.pop("dompolicy")
        self.colour = nation.pop("color")
        self.alliance_id = nation.pop("alliance_id")
        self.alliance_position = nation.pop("alliance_position")
        self.score = nation.pop("score")
        self.population = nation.pop("population")
        self.flag = nation.pop("flag")
        self.vacation = nation.pop("vmode")
        self.beige = nation.pop("beigeturns")
        self.espionage = nation.pop("espionage_available")
        self.login = nation.pop("last_active")  # need to cast to datetime
        self.mil = {
            "soldiers": nation["soldiers"], "tanks": nation["tanks"], "aircraft": nation["aircraft"],
            "ships": nation["ships"],
            "missiles": nation["missiles"], "nukes": nation["nukes"]
        }
        self.soldiers = nation.pop("soldiers")
        self.tanks = nation.pop("tanks")
        self.planes = nation.pop("aircraft")
        self.ships = nation.pop("ships")
        self.missiles = nation.pop("missiles")
        self.nukes = nation.pop("nukes")
        self.treasures = nation.pop("treasures")
        self.projects = {
            "iron_works": nation.pop("ironw"), "bauxite_works": nation.pop("bauxitew"),
            "arms_stockpile": nation.pop("armss"),
            "emergency_gasoline_reserve": nation.pop("egr"), "mass_irrigation": nation.pop("massirr"),
            "international_trade_centre": nation.pop("itc"), "missile_launch_pad": nation.pop("mlp"),
            "nuclear_research_facility": nation.pop("nrf"), "iron_defence": nation.pop("irond"),
            "vital_defence_system": nation.pop("vds"), "inteligence_agency": nation.pop("cia"),
            "center_for_civil_engineering": nation.pop("cfce"), "propoganda_bureau": nation.pop("propb"),
            "urban_planning": nation.pop("uap"), "city_planning": nation.pop("city_planning"),
            "advanced_city_planning": nation.pop("adv_city_planning"), "space_program": nation.pop("space_program"),
            "spy_satellite": nation.pop("spy_satellite"), "moon_landing": nation.pop("moon_landing"),
            "pirate_economy": nation.pop("pirate_economy"), "recycling_initiative": nation.pop("recycling_initiative"),
            "telecomuniactions_satellite": nation.pop("telecom_satellite"),
            "green_technology": nation.pop("green_tech"),
            "arable_land_agency": nation.pop("arable_land_agency"),
            "clinical_research_center": nation.pop("clinical_research_center"),
            "specialized_police_training": nation.pop("specialized_police_training"),
            "advanced_engineering_corps": nation.pop("adv_engineering_corps")
        }


class Nations(collections.MutableMapping):
    """
    Nations([123456, 654321])

    Used to store multiple Nation()'s and manage them more conveniently.
    """

    def __init__(self, *args, **kwargs):
        self.mapping = {}
        self.update(kwargs)
        for arg in args:
            self.__setitem__(arg, Nation(arg))

    def __iter__(self):
        return self.mapping.__iter__()

    def __len__(self) -> int:
        return len(self.mapping.keys())

    def __setitem__(self, nid=None, nation=None) -> None:
        if nation:
            if type(nation) is Nation:
                if nation.nid:
                    if nid:
                        if nation.nid == nid:
                            self.mapping[nid] = nation
                        else:
                            raise WrongNID
                    else:
                        self.mapping[nation["nid"]] = nation
                else:
                    raise NoNID
            else:
                raise TypeError
        elif nid:
            self.mapping[nid] = Nation(nid)
        else:
            raise ValueError

    def __getitem__(self, nid):
        return self.mapping[nid]

    def __delitem__(self, nid):
        value = self[nid]
        del self.mapping[nid]
        self.pop(value, None)


class Alliance:
    """
    Alliance(aaid=1234)

    Used to store, retrieve update and calculate information about a nation.
    """
    __slots__ = "aaid", "nations", "name", "acronym", "score", "color", "founded", "accepting_members", "flag", \
                "forum_link", "irc_link", "money", "coal", "oil", "uranium", "iron", "bauxite", "lead", "gasoline", \
                "munitions", "steel", "aluminum", "food"

    def __init__(self, aaid=None):
        self.aaid = aaid
        self.nations = Nations()

    def update_long(self, alliance=None):
        if alliance is None:
            request = f""
            alliance = get_v3(request)["alliances"]["data"][0]
        self.nations.update_long(alliance.pop("nations"))
        global _Treaties.update_long(alliance.pop("treaties"))

        self.update_short(alliance)


    def update_short(self, alliance=None):
        if alliance is None:
            request = f"query{{alliances(id: {self.aaid}) {{data {{id, name, acronym, score, color, date, acceptmem, flag, forumlink, irclink, money, coal, oil, uranium, iron, bauxite, lead, gasoline, munitions, steel, aluminum, food}}}}}}"
            alliance = get_v3(request)['alliances']['data'][0]
        self.name = alliance.pop("name")
        self.acronym = alliance.pop("acronym")
        self.score = alliance.pop("score")
        self.color = alliance.pop("color")
        self.founded = alliance.pop("date")
        self.accepting_members = alliance.pop("acceptmem")
        self.flag = alliance.pop("flag")
        self.forum_link = alliance.pop("forumlink")
        self.irc_link = alliance.pop("irclink")
        self.money = alliance.pop("money")
        self.coal = alliance.pop("coal")
        self.oil = alliance.pop("oil")
        self.uranium = alliance.pop("uranium")
        self.iron = alliance.pop("iron")
        self.bauxite = alliance.pop("bauxite")
        self.lead = alliance.pop("lead")
        self.gasoline = alliance.pop("gasoline")
        self.munitions = alliance.pop("munitions")
        self.steel = alliance.pop("steel")
        self.aluminum = alliance.pop("aluminum")
        self.food = alliance.pop("food")


class Treaty:
    def __init__(self):
        pass


class Treaties(collections.MutableSet):
    def __init__(self, treaties=None):
        self.elements = set()
        if treaties is not None:
            for treaty in treaties:
                if treaty not in self.elements:
                    self.elements.add(treaty)

    def __contains__(self, treaty: Treaty):
        if treaty in self.elements:
            return True
        return False

    def add(self, treaty: Treaty):
        if type(treaty) is Treaty:
            if treaty not in self.elements:
                self.elements.add(treaty)
                return True
            else:
                return False
        else:
            raise TypeError("Not a treaty")

    def discard(self, treaty: Treaty):
        if type(treaty) is Treaty:
            if treaty in self.elements:
                self.elements.discard(treaty)
                return True
            else:
                return False
        else:
            raise TypeError("Not a treaty")

    def __len__(self):
        return self.elements.__len__()

    def __iter__(self):
        return self.elements.__iter__()

    def update_long(self, treaties):
        pass


# Exceptions

class NoNID(Exception):
    pass


class NoAAID(Exception):
    pass


class InvalidRequest(Exception):
    pass


class WrongNID(Exception):
    pass


class WrongAAID(Exception):
    pass


class NoCityData(Exception):
    pass


class NoCID(Exception):
    pass


class WrongCID(Exception):
    pass


# Global Variables

_Key = ""
_Treaties = Treaties()

# On accidental run

if __name__ == "__main__":
    print("I am a package. Feel free to check my docs to see how to use me properly.")
