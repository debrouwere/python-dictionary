from . import utils


def flip(d):
    return {v: k for k, v in d.items()}

def join(l, connector):
    if isinstance(l, (list, tuple)):
        return connector.join(l)
    else:
        return l

def deflate(obj, context=(), connector='_'):
    deflated = []

    for key, value in obj.items():
        key = context + (key,)

        if isinstance(value, dict):
            deflated.extend(deflate(value, key, connector=None).items())
        else:
            deflated.append((key, value))

    if connector is None:
        return dict(deflated)
    else:
        return {join(key, connector): value for key, value in deflated}


def inflate(obj, connector='_'):
    inflated = {}

    for key, value in obj.items():
        if connector is not None:
            key = key.split(connector)

        chunk = inflated
        for segment in key[:-1]:
            chunk = chunk.setdefault(segment, {})
        chunk[key[-1]] = value

    return inflated


def items(d):
    if isinstance(d, tuple):
        d = dict(d)
    return list(d.items())

# from records to columns
def columns(l):
    keys = set(utils.flatten([d.keys() for d in l]))
    return {key: pluck(l, key) for key in keys}

# from columns to records
def records(d):
    keys = tuple(d.keys())
    sets = zip(*d.values())
    #for values in sets:
    #    yield dict(zip(keys, values))
    return [dict(zip(keys, values)) for values in sets]
