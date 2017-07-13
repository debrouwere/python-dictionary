
# matches (all k=v of a and b)
def matches(*dicts):
    keys = set(flatten([list(d.keys()) for d in dicts]))
    for key in keys:
        reference = dicts[0].get(key)
        for d in dicts:
            if key not in d:
                return False
            elif d[key] != reference:
                return False
    return True

# equals (deep)
def equals():
    raise NotImplementedError()
