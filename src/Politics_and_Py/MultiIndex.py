
class MultiIndexable:
    def __init__(self):
        self.dict_ = dict()

    @staticmethod
    def create(self_type, dict_: dict):
        # return instance of self
        object_ = self_type()
        object_.update(dict_)
        return object_

    @staticmethod
    def get_labels_alex():
        raise NotImplemented


    def update(self, dict_: dict):
        for label, label_alex in self.get_labels_alex().items():
            self.dict_[label] = dict_[label_alex]

    def get_value(self, label):
        return self.dict_[label]


class MultiIndex:
    def __init__(self, type_name):
        self.type_name = type_name
        self.indexes = {index_label:dict() for index_label in type_name.get_labels()}

    def index(self, index_label):
        return self.indexes[index_label]

    def extend(self, iterable):
        for item in iterable:
            for index_label, inner_index in self.indexes.items():
                inner_index[item.get_value(index_label)] = item

    def update_all(self, list_of_dicts: list):
        existing_ids = self.indexes["id"].keys()
        given_ids = [dict_["id"] for dict_ in list_of_dicts]
        #  Delete old items
        for id_ in existing_ids:
            if id_ not in given_ids:
                del self.indexes["id"][id_]
        for dict_ in list_of_dicts:
            id_ = dict_["id"]
            if id_ in self.indexes["id"]:
                #  Update existing items
                item = self.indexes["id"][id_]
                item.update(dict_)
            else:
                #  Add new items
                item = self.type_name.create(self.type_name, dict_)
                self.indexes["id"][id_] = item
        self._rebuild()

    def _rebuild(self):
        items = tuple(item for item in self.indexes["id"].values())
        for index_label in tuple(self.indexes.keys()):
            self.indexes[index_label] = {item.get_value(index_label): item for item in items}
