import discord
import json
from collections import namedtuple
from json import JSONEncoder

def readjson(file):
    def decoder(dict):
        return namedtuple('X', dict.keys())(*dict.values())

    try:
        with open(file, encoding='utf8') as f:
            t = json.load(f, object_hook=decoder)
            return t
    except FileNotFoundError:
        raise FileNotFoundError("Could not find JSON file")
