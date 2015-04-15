import json


class MyEncoder(json.JSONEncoder):
    # convert object to a dict
    def default(self, obj):
        d = {}
        d.update(obj.__dict__)
        return d
