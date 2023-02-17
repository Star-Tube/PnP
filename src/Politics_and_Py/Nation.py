import collections.abc as collections
from .Utils import get_v3, war_range
from .Core import Nations_
from .Cities import Cities
from .City import City


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
        self.nid = int(nid)
        self.cities = Cities()
        Nations_[nid] = self
        if nation is not None:
            self.update_long(nation)

    def __str__(self):
        try:
            return f"{self.nation_name}"
        except AttributeError:
            return self.__repr__()

    def __repr__(self):
        return f"Nation({self.nid})"

    def update_long(self, nation=None):
        if nation is None:
            request = f"{{nations(id: {self.nid} first:100){{" \
                      f"data{{ {Nation.request_data} cities{{{City.request_data}}} }}" \
                      f"}}}}"
            nation = get_v3(request)['nations']['data'][0]
        try:
            self.cities = Cities(*tuple(int(x["id"]) for x in nation["cities"]))
            self.cities.update_short(cities=nation.pop("cities"))
        except KeyError as error:
            print(error)
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
