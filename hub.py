import datetime
from item import Item
import json
from json_tools import ItemHubEncoder


class Hub:
    _items = list()
    _date = datetime.datetime.now()
    _hub = None

    def __new__(cls):
        if cls._hub is None:
            cls._hub = object.__new__(cls)
        return cls._hub

    def add_item(self, item):
        if type(item) == Item:
            self._items.append(item)

    def get_item(self, index):
        return self._items[index]

    def __str__(self):
        return f"Hub contains items {self._items} with date {self._date}"

    def __repr__(self):
        if len(self._items) >= 3:
            return f"Items: {self._items[0]}, {self._items[1]}, {self._items[2]}"
        return f"Items: {self._items}"

    def __len__(self):
        return len(self._items)

    def reset(cls):
        'Метод для тестирования, чтобы вернуть экземпляр синглтона в нулевое состояние'
        cls._hub = None
        cls._items = []

    def __getitem__(self, position):
        return self._items[position]

    def find_by_id(self, id):
        for pos, item in enumerate(self._items):
            if item.get_id() == id:
                return (pos, item)
        return (-1, None)

    def find_by_tags(self, tags):
        result = []
        for i in self._items:
            count = 0
            for t in tags:
                if i.is_tagged(t):
                    count += 1
            if count == len(tags):
                result.append(i)
        return result

    def rm_item(self, i):
        if i in self._items:
            self._items.remove(i)
        elif type(i) is int:
            for item in self._items:
                if item.get_id() == i:
                    self._items.remove(item)

    def drop_items(self, items):
        for i in items:
            for j in self._items:
                if i == j:
                    self._items.remove(i)

    def clear(self):
        self._items = []

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    def find_most_valuable(self, amount=1):
        if len(self._items) <= amount:
            return self._items
        sorted_items = sorted(self._items, key=lambda x: x.cost, reverse=True)
        return [sorted_items[i] for i in range(amount)]

    def find_by_date(self, *args):
        if len(args) == 1:
            return [i for i in self._items if i.get_date() <= args[0]]
        elif len(args) == 2:
            return [i for i in self._items if args[0] < i.get_date() < args[1]]
        else:
            raise Exception('Передано слишком много параметров')

    def dict_to_hub(d):
        ins = Item(name=d['_name'], description=d['_description'], dispatch_time=d['_dispatch_time'])
        ins._tags = d['_tags']
        ins.cost = d['_cost']
        return ins

    def read_from_json(self, json_path):
        try:
            with open(json_path, 'r', encoding='UTF-8') as f:
                result = f.read()
            json.loads(result, object_hook=lambda d: self._items.append(dict_to_hub(d)))
        except FileNotFoundError:
            print(f'файла "{json_path}" нет')

    def save_as_json(self, filename):
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write(json.dumps(self._items, cls=ItemHubEncoder, ensure_ascii=False, indent=4))