# Imports
import collections.abc as collections
from typing import Union

from .Exceptions import WrongID, NoID
from .Utils import get_v3
from .Config import _Request_Res

from .City import City
from .Nation import Nation
from .Treaty import Treaty
from .Alliance import Alliance

# Global Functions

# todo: Extrapolate this into a util function and a Nation.send_message() function and a Nations.send_message() function. Maybe also Alliance.send_message() and Alliances.send_message() functions.
'''
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
'''

def get_bankrecs(nation):
    if type(nation) is Nation:
        nation = nation.nid
    return get_v3(f"query{{bankrecs(or_id:{nation}){{"
                  f"    data{{id, date, sid, stype, rid, rtype, pid, note, {_Request_Res}, tax_id}}}}"
                  f"}}")['bankrecs']['data']


# Classes
class BaseCities(collections.MutableMapping):
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
            raise ValueError(cid)

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

    def update_short(self, cities=None):
        if cities is None:
            request = f"cities(id:{self.keys()}){{data{{ {City.request_data} }}}}"
            cities = get_v3(request)["cities"]["data"]
        for city in cities:
            try:
                self[city["id"]].update_short(city)
            except KeyError:
                self.__setitem__(city["id"], City(data=city))


class BaseNations(collections.MutableMapping):
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

    def __str__(self):
        try:
            return str({nid:nation.nation_name for nid,nation in self.mapping.items()})
        except AttributeError:
            # todo: log that this object should be updated
            return f"The Nations: {str(list(self.mapping.keys())).strip('[]')}"

    def __repr__(self):
        return str(self.mapping)

    def __len__(self) -> int:
        return len(self.mapping.keys())

    def __setitem__(self, nid=None, nation=None) -> None:
        if nation:
            if type(nation) is Nation:
                if nation.nid:
                    if nid:
                        if nation.nid == int(nid):
                            self.mapping[int(nid)] = nation
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
        elif type(nids) == str:
            try:
                return self.mapping[int(nids)]
            except ValueError as E:
                print(E) # Todo: add logging

    def __delitem__(self, nid):
        value = self[nid]
        del self.mapping[nid]
        self.pop(value, None)

    def update_long(self, nations=None, static=True, requirements=None):
        if nations is None:
            if static:
                request = f"{{nations(id: {list(self.keys())}, first:100){{data{{" \
                          f"{Nation.request_data} cities{{ {City.request_data} }}" \
                          f"}}}}}}"
                nations = get_v3(request)["nations"]["data"]
            else:
                nations = self.paginate(requirements, f"{Nation.request_data} cities{{ {City.request_data} }}")
        for nation in nations:
            try:
                self[int(nation["id"])].update_long(nation)
            except KeyError:
                self.__setitem__(nation["id"], Nation(nation["id"], nation))

    def update_short(self, nations=None, static=True, requirements=None):
        if nations is None:
            if static:
                request = f"{{nations(id: {self.keys()} first:100){{data{{ {Nation.request_data}}}}}"
                nations = get_v3(request)["nations"]["data"][0]
            else:
                nations = self.paginate(requirements, f"{Nation.request_data}")
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


class BaseAlliances(collections.MutableMapping):
    def __init__(self, *args, **kwargs):
        self.mapping = {}
        self.update(kwargs)
        for arg in args:
            self.__setitem__(
                arg)

    def __iter__(self):
        return self.mapping.__iter__()

    def __len__(self):
        return len(self.mapping.keys())

    def __setitem__(self, aaid):
        self.mapping[aaid] = Alliance(aaid)

    def __getitem__(self, aaids):
        if type(aaids) is int:
            return self.mapping[aaids]

    def __delitem__(self, aaid):
        value = self[aaid]
        del self.mapping[aaid]
        self.pop(value, None)


class BaseTreaties(collections.MutableMapping):
    def __init__(self, treaties=None):
        self.mapping = {}
        if treaties is not None:
            for treaty in treaties:
                self.__setitem__(treaty.tid, treaty)

    def __repr__(self):
        return str(list(self.mapping.__iter__()))

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

    def update_long(self, treaties=None):
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


# Global sources of truth

Treaties_ = BaseTreaties()
Cities_ = BaseCities()
Nations_ = BaseNations()
Alliances_ = BaseAlliances()

# On accidental run
if __name__ == "__main__":
    print("I am a package. Feel free to check my docs to see how to use me properly.")
