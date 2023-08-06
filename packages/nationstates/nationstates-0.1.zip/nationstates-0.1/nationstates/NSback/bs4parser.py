import json
from xmltodict import parse
import json


class SuperDict(dict):

    def __init__(self, *arg, **kw):
        super(SuperDict, self).__init__(*arg, **kw)

    def json(self):
        return json.JSONEncoder().encode(self)

    def __getattr__(self, attr):
        try:
            return self.get(attr)
        except:
            self.__dict__[attr] = value
            return value


class SuperDict(dict):

    def __init__(self, *arg, **kw):
        super(SuperDict, self).__init__(*arg, **kw)

    def __getattr__(self, attr):
        try:
            return self.get(attr)
        except:
            return self.__dict__[attr]

    @property
    def json(self):
        return json.JSONEncoder().encode(self)


def make_lower(x):
    if isinstance(x, list):
        gen_list = [SuperDict(make_lower(y)) if isinstance(
            make_lower(y), dict) else make_lower(y) for y in x]
        return gen_list
    if isinstance(x, str):
        return x
    if isinstance(x, dict):
        newdict = {}
        for key in x.keys():
            if key[0] in ["@", "#"]:
                thiskey = key[1:].lower()
            else:
                thiskey = key.lower()
            this_lower = make_lower(x[key])
            newdict[thiskey] = SuperDict(this_lower) if isinstance(
                this_lower, dict) else this_lower
        return newdict
    if x is None:
        return None


def parsetree(xml):
    return make_lower(parse(xml))
