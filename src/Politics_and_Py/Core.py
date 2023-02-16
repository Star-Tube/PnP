# Imports
import requests
import json
import collections.abc as collections
from typing import Union

from .Exceptions import WrongID, NoID
from .Utils import war_range, get_v3
from .Config import _Request_Res, Key

# Global Functions


def send_message(recipient, message: str, subject: str, sent: list = None):
    """
    Takes in recipient, message and subject and sends the message. Returns any response to the action.

    Recipient can be either a Nation(), an int() or a Nations() object. If it is given a Nations() object then it will
    send the message to every nation.

    Optional parameter sent will ignore nations with the given id.

    :param recipient:
    :param message:
    :param subject:
    :param sent:
    :return:
    """
    url = "https://politicsandwar.com/api/send-message/"
    sent = [6] + sent
    if type(recipient) is int:
        payload = {"key": Key, "to": recipient, "message": message, "subject": subject}
        response = json.loads(requests.post(url, payload).text)
        return response
    elif type(recipient) is Nation:
        payload = {"key": Key, "to": recipient.nid, "message": message, "subject": subject}
        response = json.loads(requests.post(url, payload).text)
        return response
    elif type(recipient) is Nations:
        for nation in recipient:
            if nation.nid not in sent:
                payload = {"key": Key, "to": nation.nid, "message": message, "subject": subject}
                response = json.loads(requests.post(url, payload).text)
                yield response


def get_bankrecs(nation):
    if type(nation) is Nation:
        nation = nation.nid
    return get_v3(f"query{{bankrecs(or_id:{nation}){{"
                  f"    data{{id, date, sid, stype, rid, rtype, pid, note, {_Request_Res}, tax_id}}}}"
                  f"}}")['bankrecs']['data']

# Classes


class City:
    """
    City(cid=123)

    Used to store data about a city.
    """

    request_data = "id, name, date, infrastructure, land, powered, oilpower, windpower, coalpower, nuclearpower, " \
                   "coalmine, oilwell, uramine, barracks, farm, policestation, hospital, recyclingcenter, subway, " \
                   "supermarket, bank, mall, stadium, leadmine, ironmine, bauxitemine, gasrefinery, aluminumrefinery, "\
                   "steelmill, munitionsfactory, factory, airforcebase, drydock, date"

    __slots__ = "cid", "name", "infra", "land", "nid", "powered", "founded", "imps", "coal_power_plant", \
        "oil_power_plant", "wind_power_plant", "nuclear_power_plant", "coal_mine", "oil_well", "uranium_mine", "farm", \
        "police_station", "barracks", "hospital", "recycling_center", "subway", "supermarket", "bank", "mall", \
        "stadium", "lead_mine", "iron_mine", "bauxite_mine", "gas_refinery", "aluminium_refinery", "steel_mill", \
        "munitions_factory", "factory", "airforcebase", "drydock", "pollution", "disease", "population", "commerce", \
        "crime", "age", "daily_gross_income", "revenue"

    def __init__(self, cid=None, data=None):
        if cid:
            self.cid = cid
        elif data:
            self.cid = data["id"]
        if data:
            self.update_short(data)


    def update_short(self, city=None):
        if city is None:
            request = f"cities(id:{self.cid}){{data{{ { City.request_data } }}}}"
            city = get_v3(request)["cities"]["data"][0]

        if self.cid == city.pop("id"):
            self.name = city.pop("name")
            self.founded = city.pop("date")
            self.infra = city.pop("infrastructure")
            self.land = city.pop("land")
            self.powered = city.pop("powered")
            self.oil_power_plant = city.pop("oilpower")
            self.wind_power_plant = city.pop("windpower")
            self.coal_power_plant = city.pop("coalpower")
            self.nuclear_power_plant = city.pop("nuclearpower")
            self.coal_mine = city.pop("coalmine")
            self.oil_well = city.pop("oilwell")
            self.uranium_mine = city.pop("uramine")
            self.barracks = city.pop("barracks")
            self.farm = city.pop("farm")
            self.police_station = city.pop("policestation")
            self.hospital = city.pop("hospital")
            self.recycling_center = city.pop("recyclingcenter")
            self.subway = city.pop("subway")
            self.supermarket = city.pop("supermarket")
            self.bank = city.pop("bank")
            self.mall = city.pop("mall")
            self.stadium = city.pop("stadium")
            self.lead_mine = city.pop("leadmine")
            self.iron_mine = city.pop("ironmine")
            self.bauxite_mine = city.pop("bauxitemine")
            self.gas_refinery = city.pop("gasrefinery")
            self.aluminium_refinery = city.pop("aluminumrefinery")
            self.steel_mill = city.pop("steelmill")
            self.munitions_factory = city.pop("munitionsfactory")
            self.factory = city.pop("factory")
            self.airforcebase = city.pop("airforcebase")
            self.drydock = city.pop("drydock")


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

    def __str__(self):
        return self.mapping.__str__()

    def __repr__(self):
        return self.mapping.__repr__()

    def __iter__(self):
        return self.mapping.__iter__()

    def __len__(self) -> int:
        return len(self.mapping.keys())

    def __setitem__(self, cid=None, city=None) -> None:
        if city:
            if type(city) is City:
                if city.cid:
                    if cid:
                        if city.cid == cid:
                            self.mapping[cid] = city
                        else:
                            raise WrongID("City", city.cid, cid)
                    else:
                        self.mapping[city["nid"]] = city
                else:
                    raise NoID
            else:
                raise TypeError
        elif type(cid) is int:
            self.mapping[cid] = City(cid)
        elif type(cid) is str:
            if cid.isnumeric():
                self.mapping[int(cid)] = City(int(cid))
            else:
                raise WrongID("City", "cid is not numeric")
        else:
            raise ValueError

    def __getitem__(self, cid: Union[int, str]):
        if type(cid) is int:
            return self.mapping[cid]
        elif type(cid) is str:
            if cid.isnumeric():
                return self.mapping[int(cid)]

    def __delitem__(self, cid):
        value = self[cid]
        del self.mapping[cid]
        self.pop(value, None)

    def update_short(self, cities):
        if cities is None:
            request = f"cities(id:{self.keys()}){{data{{ {City.request_data} }}}}"
            cities = get_v3(request)["cities"]["data"]
        for city in cities:
            try:
                self[city["id"]].update_short(city)
            except KeyError:
                self.__setitem__(city["id"], City(data=city))


class Nation:
    """
    Nation(nid=12346)

    Used to store and update a nation's data.
    """

    __slots__ = "nid", "nation_name", "leader_name", "continent", "war_policy", "dom_policy", "colour", "score", \
                "population", "flag", "vacation", "beige", "projects", "alliance_id", "alliance_position", \
                "espionage", "login", "mil", "soldiers", "tanks", "planes", "ships", "missiles", "nukes", "treasures", \
                "cities"

    request_data = "id, alliance_id, alliance_position, nation_name, leader_name, continent, warpolicy, dompolicy, " \
                   "color, score, population, flag, vmode, beigeturns, espionage_available, last_active, soldiers, " \
                   "tanks, aircraft, ships, missiles, nukes, treasures {name}, ironw, bauxitew, armss, egr, " \
                   "massirr, itc, mlp, nrf, irond, vds, cia, cfce, propb, uap, city_planning, adv_city_planning, " \
                   "space_program, spy_satellite, moon_landing, pirate_economy, recycling_initiative, " \
                   "telecom_satellite, green_tech, arable_land_agency, clinical_research_center, " \
                   "specialized_police_training, adv_engineering_corps, "

    def __init__(self, nid=None, nation=None):
        self.nid = nid
        self.cities = self.Cities()
        _Nations[nid] = self
        if nation is not None:
            self.update_long(nation)

    def update_long(self, nation=None):
        if nation is None:
            request = f"{{nations(id: {self.nid} first:100){{" \
                      f"data{{ {Nation.request_data} cities{{{City.request_data}}} }}" \
                      f"}}}}"
            nation = get_v3(request)['nations']['data'][0]
        try:
            self.cities = [int(x["id"]) for x in nation["cities"]]
            _Cities.update_short(nation.pop("cities"))
        except KeyError:
            pass
        self.update_short(nation)

    def update_short(self, nation=None):
        if nation is None:
            request = f"""{{nations(id: {self.nid} first:1){{data{{ {Nation.request_data} }}}}}}"""
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
        # Not sure if projects here should be a dictionary or if every seperate project should be it's own boolean slot
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
        return self

    def war_range(self):
        if self.score is int:
            return war_range(self.score)
        else:
            raise TypeError(f"{self.__name__}.score is not an int")

    class Cities(list):
        def __init__(self):
            super().__init__()

        def __setitem__(self, index, item):
            if item is int:
                super().__setitem__(index, item)
            if item is City:
                super().__setitem__(index, item.cid)

        def __str__(self):
            return [_Cities[cid] for cid in self]


class Nations(collections.MutableMapping):
    """
    Nations([123456, 654321])

    Used to store multiple Nation()'s and manage them more conveniently.
    """

    @staticmethod
    def paginate(check, data):
        for page in range(100):
            request = f"{{nations({check}, first:100, page:{page + 1}){{data{{{data}}}paginatorInfo{{count}}}}}}"
            response = get_v3(request)["nations"]
            nations = response["data"]
            if response["paginatorInfo"]["count"] == 0:
                break
            for nation in nations:
                yield nation

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
                            raise WrongID("Nation", nation.nid, nid)
                    else:
                        self.mapping[nation["nid"]] = nation
                else:
                    raise NoID
            else:
                raise TypeError
        elif nid:
            self.mapping[nid] = Nation(nid)
        else:
            raise ValueError

    def __getitem__(self, nids):
        if type(nids) == int:
            return self.mapping[nids]

    def __delitem__(self, nid):
        value = self[nid]
        del self.mapping[nid]
        self.pop(value, None)

    def update_long(self, nations=None, static=True, requirements=None):
        if nations is None:
            if static:
                request = f"{{nations(id: {self.keys()} first:100){{data{{" \
                          f"{Nation.request_data} cities{{ {City.request_data} }}" \
                          f"}}}}"
                nations = get_v3(request)["nations"]["data"][0]
            else:
                nations = Nations.paginate(requirements, f"{Nation.request_data} cities{{ {City.request_data} }}")
        for nation in nations:
            try:
                self[nation["id"]].update_long(nation)
            except KeyError:
                self.__setitem__(nation["id"], Nation(nation["id"], nation))

    def update_short(self, nations=None, static=True, requirements=None):
        if nations is None:
            if static:
                request = f"{{nations(id: {self.keys()} first:100){{data{{ {Nation.request_data}}}}}"
                nations = get_v3(request)["nations"]["data"][0]
            else:
                nations = Nations.paginate(requirements, f"{Nation.request_data}")
        for nation in nations:
            try:
                self[nation["id"]].update_short(nation)
            except KeyError:
                self.__setitem__(nation["id"], Nation(nation["id"], nation))

    def update_alliance(self, alliance=None, nations=None):
        for nation in nations:
            try:
                alliance.nations[nation["id"]] = self[nation["id"]].update_short(nation)
            except KeyError:
                _ = Nation(nation["id"], nation)
                alliance.nations[nation["id"]] = _
                self.__setitem__(nation["id"], _)


class Alliance:
    """
    Alliance(aaid=1234)

    Used to store, retrieve update and calculate information about a nation.
    """

    request_data = "id, name, acronym, score, color, date, acceptmem, flag, forumlink, irclink, money, coal, oil, " \
                   "uranium, iron, bauxite, lead, gasoline, munitions, steel, aluminum, food "

    __slots__ = "aaid", "nations", "treaties", "name", "acronym", "score", "color", "founded", "accepting_members", \
                "flag", "forum_link", "irc_link", "money", "coal", "oil", "uranium", "iron", "bauxite", "lead", \
                "gasoline", "munitions", "steel", "aluminum", "food"

    def __init__(self, aaid=None):
        self.aaid = aaid
        self.nations = Nations()
        self.treaties = Treaties()
        _Alliances[aaid] = self

    def update_long(self, alliance=None):
        if alliance is None:
            request = f"query{{alliances(id: {self.aaid}) {{" \
                      f"data {{ {Alliance.request_data}, nations{{ { Nation.request_data }, " \
                      f"treaties{{ { Treaty.request_data } }} }} }} }} }}"
            alliance = get_v3(request)["alliances"]["data"][0]
        _Nations.update_alliance(self, alliance.pop("nations"))
        _Treaties.update_alliance(self, alliance.pop("treaties"))

        self.update_short(alliance)

    def update_short(self, alliance=None):
        if alliance is None:
            request = f"query{{alliances(id: {self.aaid}) {{data {{ {Alliance.request_data} }}}}}}"
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


class Alliances(collections.MutableMapping):
    def __init__(self, *args, **kwargs):
        self.mapping = {}
        self.update(kwargs)
        for arg in args:
            self.__setitem__(arg, Alliance(arg))

    def __iter__(self):
        return self.mapping.__iter__()

    def __len__(self):
        return len(self.mapping.keys())

    def __setitem__(self, aaid=None, alliance=None):
        if alliance:
            if type(alliance) is Alliance:
                if alliance.aaid:
                    if aaid:
                        if alliance.aaid == aaid:
                            self.mapping[aaid] = alliance
                        else:
                            raise WrongID("Alliance", alliance.aaid, aaid)
                    else:
                        self.mapping[alliance.aaid] = alliance
                else:
                    raise NoID
            else:
                raise TypeError
        elif aaid:
            self.mapping[aaid] = Alliance(aaid)
        else:
            raise ValueError

    def __getitem__(self, aaids):
        if type(aaids) is int:
            return self.mapping[aaids]

    def __delitem__(self, aaid):
        value = self[aaid]
        del self.mapping[aaid]
        self.pop(value, None)


class Treaty:
    __slots__ = "tid", "alliance_1", "alliance_2", "type", "date", "turns_left", "url"

    request_data = "id, date, treaty_type, treaty_url, turns_left, alliance1_id, alliance2_id"

    def __init__(self, tid=None, treaty=None):
        self.tid = tid
        _Treaties.__setitem__(treaty=self)
        if treaty is not None:
            self.update_short(treaty)

    def update_short(self, treaty):
        if treaty is None:
            request = f"query{{treaties(id: {self.tid}) {{data {{ {Treaty.request_data} }}}}}}"
            treaty = get_v3(request)['treaties']['data'][0]
        self.tid = treaty.pop("id")
        self.date = treaty.pop("date")
        self.type = treaty.pop("treaty_type")
        self.url = treaty.pop("treaty_url")
        self.turns_left = treaty.pop("turns_left")
        self.alliance_1 = treaty.pop("alliance1_id")
        self.alliance_2 = treaty.pop("alliance2_id")
        return self


class Treaties(collections.MutableMapping):
    def __init__(self, treaties=None):
        self.mapping = {}
        if treaties is not None:
            for treaty in treaties:
                self.__setitem__(treaty.tid, treaty)

    def __iter__(self):
        return self.mapping.__iter__()

    def __len__(self):
        return self.mapping.__len__()

    def __setitem__(self, tid=None, treaty=None):
        if treaty:
            if type(treaty) is Treaty:
                if treaty.tid:
                    if tid:
                        if treaty.tid == tid:
                            self.mapping[tid] = treaty
                        else:
                            raise WrongID("Treaty", treaty.tid, tid)
                    else:
                        self.mapping[treaty.tid] = treaty
                else:
                    raise NoID
            else:
                raise TypeError
        elif tid:
            self.mapping[tid] = Treaty(tid)
        else:
            raise ValueError

    def __getitem__(self, tid):
        return self.mapping[tid]

    def __delitem__(self, tid):
        value = self[tid]
        del self.mapping[tid]
        self.pop(value, None)

    def update_long(self, treaties):
        if treaties is None:
            request = f"query{{treaties {{data {{ {Treaty.request_data} }}}}}}"
            treaties = get_v3(request)['treaties']['data']
        for treaty in treaties:
            self[treaty["id"]].update_short(treaty)

    def update_alliance(self, alliance, treaties):
        for treaty in treaties:
            try:
                alliance.treaties[treaty["id"]] = self[treaty["id"]].update_short(treaty)
            except KeyError:
                _ = Treaty(treaty["id"], treaty)
                alliance.nations[treaty["id"]] = _
                self.__setitem__(treaty["id"], _)


# Global Variables

_Treaties = Treaties()
_Cities = Cities()
_Nations = Nations()
_Alliances = Alliances()

# On accidental run

if __name__ == "__main__":
    print("I am a package. Feel free to check my docs to see how to use me properly.")
