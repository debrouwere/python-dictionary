import collections
import types

from . import utils
from .transform import defaults


def sort(d, key):
    if isinstance(key, str):
        key = property(key)

    raise NotImplementedError()
    return OrderedDict()

def blob(d=None, **values):
    if d is not None:
        if isinstance(d, dict):
            values = d
        else:
            return d

    values = {key: blob(value) for key, value in values.items()}
    return types.SimpleNamespace(**values)

def namedtuple(name, d):
    if isinstance(d, collections.OrderedDict):
        keys = d.keys()
    else:
        keys = set(d.keys())

    values = [d[key] for key in keys]
    return utils.namedtuple(name, keys)(values)

def options(keywords, **options):
    return blob(defaults(keywords, **options))
