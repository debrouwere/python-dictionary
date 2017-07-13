import collections
import functools
import re
from functools import partial


def identity(v):
    return v

def index(ix):
    def get_index(l):
        return l[ix]
    return get_index

def fallback(*fns):
    @functools.wraps(fns[0])
    def fallback_fn(*vargs, **kwargs):
        errors = []
        for fn in fns:
            try:
                return fn(*vargs, **kwargs)
            except Exception as error:
                errors.append(str(error))
        raise Exception(', '.join(errors))
    return fallback_fn

def harmonize(fn):
    @functools.wraps(fn)
    def harmonized_fn(*vargs, **kwargs):
        errors = []
        try:
            return fn(*vargs, **kwargs)
        except Exception as error:
            errors.append(str(error))
            for dim in reversed(range(len(vargs) + 1)):
                try:
                    return fn(*vargs[:dim])
                except Exception as error:
                    errors.append(str(error))
        raise Exception(', '.join(errors))
    return harmonized_fn

def dispatch(signatures):
    def specialized_fn(arg, *vargs, **kwargs):
        for signature, fn in signatures.items():
            if isinstance(arg, signature):
                return fn(arg, *vargs, **kwargs)
        raise TypeError()
    return specialized_fn

def invert(fn):
    @functools.wraps(fn)
    def inverted_fn(*vargs, **kwargs):
        return not fn(*vargs, **kwargs)
    return inverted_fn

def isin(options):
    def matches(value):
        return value in options
    return matches

def replace(mapping, s):
    for pattern, replacement in mapping.items():
        if s == pattern:
            return replacement
        else:
            s = re.sub(pattern, replacement, s)
    return s

def flatten(l):
    flattened = []
    for el in l:
        if isinstance(el, list):
            flattened.extend(el)
        else:
            flattened.append(el)
    return flattened


def humanize(s):
    return replace(s, {
        '-': ' ',
        '_': ' ',
    })

@functools.lru_cache(maxsize=None)
def namedtuple(name, keys):
    return namedtuple(name, keys)
