from .MultiIndex import MultiIndexable, MultiIndex
from .City import City


class Nation(MultiIndexable):
    def __init__(self):
        super().__init__()
        self.cities = MultiIndex(City)

    @staticmethod
    def get_labels():
        return "id", "name", "leader_name", "continent", "war_policy", "domestic_policy", "colour", "alliance_id", "alliance_position", "score", "population", "flag", "vacation", "beige", "espionage", "login", "soldiers", "tanks", "aircraft", "ships", "missiles", "nukes", "treasures", "iron_works", "arms_stockpile", "emergency_gasoline_reserve", "international_trade_centre", "nuclear_research_facility", "vital_defence_system", "center_for_civil_engineering", "urban_planning", "advanced_city_planning", "spy_satellite", "pirate_economy", "telecommunications_satellite", "green_technology", "arable_land_agency", "clinical_research_center", "specialized_police_training", "advanced_engineering_corps"

    @staticmethod
    def get_labels_alex():
        return {"id": "id", "name": "nation_name", "leader_name": "leader_name", "continent": "continent", "war_policy": "warpolicy", "domestic_policy": "dompolicy", "colour": "color", "alliance_id": "alliance_id", "score": "score", "population": "population", "flag": "flag", "vacation": "vmode", "beige": "beigeturns", "espionage": "espionage_available", "login": "last_active", "soldiers": "soldiers", "tanks": "tanks", "planes": "aircraft", "ships": "ships", "missiles": "missiles", "nukes": "nukes", "treasures": "treasures", "iron_works": "ironw", "bauxite_works": "bauxitew", "arms_stockpile": "armss", "emergency_gasoline_reserve": "egr", "mass_irrigation": "massirr", "international_trade_center": "itc", "missile_launch_pad": "mlp", "nuclear_research_facility": "nrf", "iron_defence": "irond", "vital_defence_system": "vds", "intelligence_agency": "cia", "center_for_civil_engineering": "cfce", "propaganda_bureau": "propb", "urban_planning": "uap", "city_planning": "city_planning", "advanced_city_planning": "adv_city_planning", "space_program": "space_program", "spy_satellite": "spy_satellite", "moon_landing": "moon_landing", "pirate_economy": "pirate_economy", "recycling_initiative": "recycling_initiative", "telecommunications_satellite": "telecom_satellite", "green_technology": "green_tech", "arable_land_agency": "arable_land_agency", "clinical_research_center": "clinical_research_center", "specialized_police_training": "specialized_police_training", "advanced_engineering_corps": "adv_engineering_corps"}

    def update(self, dict_: dict):
        for label, label_alex in self.get_labels_alex().items():
            self.dict_[label] = dict_[label_alex]
