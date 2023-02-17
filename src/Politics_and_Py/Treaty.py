from .Utils import get_v3
from .Core import Treaties_


class Treaty:
    __slots__ = "tid", "alliance_1", "alliance_2", "type", "date", "turns_left", "url"

    request_data = "id, date, treaty_type, treaty_url, turns_left, alliance1_id, alliance2_id"

    def __init__(self, tid=None, treaty=None):
        self.tid = tid
        Treaties_.__setitem__(treaty=self)
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
