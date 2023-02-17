from .Utils import get_v3
from .Core import Alliances_
from .Nations import Nations
from .Nation import Nation
from .Treaties import Treaties
from .Treaty import Treaty


class Alliance:
    """
    Alliance(aaid=1234)

    Used to store, retrieve update and calculate information about a nation.
    """

    request_data = "id, name, acronym, score, color, date, acceptmem, flag, forumlink, irclink, money, coal, oil, " \
                   "uranium, iron, bauxite, lead, gasoline, munitions, steel, aluminum, food "

    __slots__ = "aaid", "nations", "treaties", "alliance_name", "acronym", "score", "color", "founded", "accepting_members", \
                "flag", "forum_link", "irc_link", "money", "coal", "oil", "uranium", "iron", "bauxite", "lead", \
                "gasoline", "munitions", "steel", "aluminum", "food"

    def __init__(self, aaid=None):
        self.aaid = aaid
        self.nations = Nations()
        self.treaties = Treaties()
        Alliances_[aaid] = self

    def __str__(self):
        try:
            return self.alliance_name
        except AttributeError:
            return self.__repr__()

    def __repr__(self):
        return f"Alliance({self.aaid})"

    def update_long(self, alliance=None):
        if alliance is None:
            request = f"query{{alliances(id: {self.aaid}) {{" \
                      f"data {{ {Alliance.request_data}, nations{{ { Nation.request_data } }}, " \
                      f"treaties{{ { Treaty.request_data } }} }} }} }}"
            alliance = get_v3(request)["alliances"]["data"][0]
        self.nations = Nations(*[nation["id"] for nation in alliance["nations"]])
        self.treaties = Treaties(*[treaty["id"] for treaty in alliance["treaties"]])

        self.update_short(alliance)

    def update_short(self, alliance=None):
        if alliance is None:
            request = f"query{{alliances(id: {self.aaid}) {{data {{ {Alliance.request_data} }}}}}}"
            alliance = get_v3(request)['alliances']['data'][0]
        self.alliance_name = alliance.pop("name")
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
