import json


class ItemHubEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.__str__()
        if isinstance(obj, Item):
            return obj.__dict__
        if isinstance(obj, set):
            return list(obj)
