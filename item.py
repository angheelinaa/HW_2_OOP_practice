import datetime
import json
from json_tools import ItemHubEncoder


class Item:
    _id = -1
    _name = ""
    _description = ""
    _dispatch_time = datetime.datetime.now()
    _tags = set()
    _cost = 0

    _amount_items = 0
    _items = []    # статический лист, где по индексу id хранится item с этим id

    def __init__(self, name="", description="", dispatch_time=datetime.datetime.now(), cost=0):
        self._id = Item._amount_items
        Item._amount_items += 1
        self._name = name
        self._description = description
        self._dispatch_time = dispatch_time
        self._tags = set()
        self._cost = cost
        Item._items.append(self)

    def add_tag(self, tag):
        self._tags.add(tag)

    def rm_tag(self, tag):
        self._tags.remove(tag)

    def __str__(self):
        return f"Item {self._name} with dispatch time {self._dispatch_time} and tags {self._tags}"

    def __repr__(self):
        if len(self._tags) >= 3:
            return f"Item id {self._id} with tags {self._tags[0]}, {self._tags[1]}, {self._tags[2]}"
        return f"Item id {self._id} with tags {self._tags}"

    def __len__(self):
        return len(self._tags)

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        self._cost = value

    def __lt__(self, other):
        return self.cost < other.cost

    def add_tags(self, tags):
        for i in tags:
            self._tags.add(i)

    def rm_tags(self, tags):
        for i in tags:
            self._tags.remove(i)

    def is_tagged(self, tag):
        if type(tag) is str:
            return tag in self._tags
        return self._tags == set(tag)

    def copy(self):
        return Item(name=self._name, description=self._description, cost=self.cost)

    def get_date(self):
        return self._dispatch_time

    def get_name(self):
        return self._name

    def get_id(self):
        return self._id

    def __hash__(self):
        return hash(self._id)

    def dict_to_item(d):
        ins = Item(name=d['_name'], description=d['_description'], dispatch_time=d['_dispatch_time'])
        ins._tags = d['_tags']
        ins.cost = d['_cost']
        return ins

    def create_from_json(json_path):
        try:
            with open(json_path, 'r', encoding='UTF-8') as f:
                result = f.read()
            return json.loads(result, object_hook=dict_to_item)
        except FileNotFoundError:
            print(f'файла "{json_path}" нет')

    def save_as_json(self, filename):
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write(json.dumps(self, cls=ItemHubEncoder, ensure_ascii=False, indent=4))