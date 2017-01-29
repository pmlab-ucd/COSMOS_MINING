"""
Utilities
"""
import json
import os

class Dict2obj(object):
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [Dict2obj(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, Dict2obj(b) if isinstance(b, dict) else b)

class Utilities:
    @staticmethod
    def save_json(data, file_path):
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        with open(file_path, 'w') as outfile:
            json.dump(data, outfile)

    @staticmethod
    def load_json(file_path):
        if not os.path.exists(file_path):
            return None
        with open(file_path) as data_file:
            data = json.load(data_file)
            return data