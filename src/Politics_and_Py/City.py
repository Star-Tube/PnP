from .Utils import get_v3


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

    def __str__(self):
        return self.name, self.cid

    def __repr__(self):
        return f"City({self.cid})"

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
