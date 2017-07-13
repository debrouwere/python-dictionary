from collections import Iterable


def keys(d):
    return set(d.keys())

def values(d):
    return list(d.values())

def predicate(key):
    def getter(d):
        return d[key]
    return getter

def pluck(l, key, strict=True, default=None):
    if strict:
        return [d[key] for d in l]
    else:
        return [d.get(key, default) for d in l]

# find, with regex and function support for matching as well as plain ol' `==`
def find(d, key=None, value=None):
    raise NotImplementedError()

def traverse(obj, segments, strict=True, default=None):
    if isinstance(segments, str):
        segments = [segment for segment in segments.split('.') if segment]

    if len(segments):
        first = segments[0]
        rest = segments[1:]

        if isinstance(obj, list):
            return traverse(pluck(obj, first, strict=strict, default=default), rest, strict=strict, default=default)
        elif isinstance(obj, dict):
            if strict:
                obj = obj[first]
            else:
                obj = obj.get(first, default)
            return traverse(obj, rest, strict=strict, default=default)
        else:
            return default
    else:
        return obj
