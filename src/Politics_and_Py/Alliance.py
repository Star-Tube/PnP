from .MultiIndex import MultiIndex, MultiIndexable
from .Treaty import Treaty
from .Nation import Nation


class Alliance(MultiIndexable):
    def __init__(self):
        super().__init__()
        self.nations = MultiIndex(Nation)
        self.treaties = MultiIndex(Treaty)

    @staticmethod
    def get_labels():
        return "id", "name", "acronym", "score", "colour", "date", "accepting_members", "flag", "forum_link", "irc_link", "money", "coal", "oil", "uranium", "iron", "bauxite", "lead", "gasoline", "munitions", "steel", "aluminum", "food"

    @staticmethod
    def get_labels_alex():
        return {'id': 'id', 'name': 'name', 'acronym': 'acronym', 'score': 'score', 'colour': 'color', 'founded': 'date', 'accepting_members': 'acceptmem', 'flag': 'flag', 'forum_link': 'forumlink', 'irc_link': 'irclink', 'money': 'money', 'coal': 'coal', 'oil': 'oil', 'uranium': 'uranium', 'iron': 'iron', 'bauxite': 'bauxite', 'lead': 'lead', 'gasoline': 'gasoline', 'munitions': 'munitions', 'steel': 'steel', 'aluminum': 'aluminum', 'food': 'food'}

    def update(self, dict_: dict):
        for label, label_alex in self.get_labels_alex().items():
            self.dict_[label] = dict_[label_alex]
