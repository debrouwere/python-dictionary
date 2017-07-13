"""
TODO: have all functions return ordered dictionaries, and decorate them to
downcast these to a regular dictionary if a regular dictionary was what
was provided

TODO: convert functions to iterators that yield wherever possible,
but put these in `dictionary.iterators` and provide equivalents
that convert to actual dicts, ordered dicts and lists wherever possible
(loop through exports, decorate with a simple `unwrap` function)

TODO: vectorize where it makes sense (which is practically everywhere)

Maybe split up into a couple of logical units

* transform (= almost everything)
* simplify (= simplify, inflate, deflate)
* evaluate (= matches, equals)
* cast (= blob, namedtuple)
"""

import collections
import functools
import itertools
import types

from slugify import slugify as _slugify

from snakify import snakify as _snakify
from vectorize import vectorize

from . import navigate, reshape, utils


def update(destination, *sources):
    for source in sources:
        destination.update(source)
    return destination

# a more generic version of `pick`, which returns separate dictionaries
# with what was retained and what was dropped, and which accepts either
# a test function or a list of whitelisted keys
def whitelist(d, test, exception=None):
    if isinstance(test, collections.Iterable):
        test = utils.isin(test)

    whitelisted = {}
    blacklisted = {}
    for k, v in d.items():
        if test(k):
            whitelisted[k] = v
        elif exception:
            raise exception(key)
        else:
            blacklisted[k] = v

    return (whitelisted, blacklisted)

def blacklist(d, test, exception=None):
    test = utils.invert(test)
    return whitelist(d, test, exception)

def pick(d, *keys):
    retained, dropped = whitelist(d, keys)
    return retained

def omit(d, *keys):
    retained, dropped = blacklist(d, keys)
    return retained

# intersection or union of keys
def intersection():
    raise NotImplementedError()

def union():
    raise NotImplementedError()

def defaults(properties, **defaults):
    return merge(defaults, properties)

def first(key):
    def get_first(*ds):
        for d in ds:
            try:
                return d[key]
            except Exception:
                pass
        raise KeyError()
    return get_first


# TODO: have a deep but non-recursive mode (only work on leaves)
def transform(d, keys=utils.identity, values=utils.identity, deep=False):
    """
    e.g.

        >>> dictionary.transform({'a': {'name': 'x', 'age': 55}}, keys='name', values='age')
        {'x': 55}

    """

    if isinstance(d, list):
        return [transform(el, keys, values, deep) for el in d]
    elif not isinstance(d, dict):
        return d

    dispatchers = {
        # convert strings into getters
        str: first,
        # convert dictionaries into mappers
        dict: lambda d: functools.partial(utils.replace, d),
        collections.OrderedDict: lambda d: functools.partial(utils.replace, d),
        # pass through functions
        types.FunctionType: utils.identity,
    }

    key_fn = dispatchers[keys.__class__](keys)
    value_fn = dispatchers[values.__class__](values)

    # harmonize functions so they can accept key and value or just one
    key_fn = utils.harmonize(key_fn)
    value_fn = utils.harmonize(value_fn)

    transformed = {}
    for key, value in d.items():
        if deep:
            key = transform(key, keys, values, deep)
            value = transform(value, keys, values, deep)
        k = key_fn(key, value)
        v = value_fn(value, key)
        transformed[k] = v

    return transformed

def rekey(d, transformation, deep=False):
    return transform(d, keys=transformation, deep=deep)

reindex = rekey

def revalue(d, transformation, deep=False):
    return transform(d, values=transformation, deep=deep)

def slugify(d, **kwargs):
    fn = functools.partial(_slugify, **kwargs)
    return rekey(d, fn)

def snakify(d, **kwargs):
    fn = functools.partial(_snakify, **kwargs)
    return rekey(d, fn)

def humanize(d):
    return rekey(d, utils.humanize)


def dictionary(l, fn, reverse=False, *vargs, **kwargs):
    if reverse:
        return {fn(el, *vargs, **kwargs): el for el in l}
    else:
        return {el: fn(el, *vargs, **kwargs) for el in l}

forwards = dictionary
backwards = functools.partial(dictionary, reverse=True)

def merge(*dicts):
    merged = {}
    for d in dicts:
        merged.update(d)
    return merged

# like itertools.groupby but also supports strings as keyfuncs
def groupby(iterable, key=utils.identity):
    if isinstance(key, str):
        key = navigate.predicate(key)
    return itertools.groupby(iterable, key)

def indexby(iterable, key=utils.identity, strict=True, index=0):
    for key, values in groupby(iterable, key):
        values = list(values)
        n = len(values)
        if strict and n > 1:
            raise ValueError(f'Cannot construct a unique index. {n} objects share the key "{key}".')
        yield (key, values[index])

# TODO: harmonize these functions with groupby and indexby to provide an interface
# that allows for both single- and multi-key, and for flat multikeys and trees
# (so in concrete terms: allow key functions, strict mode and index selection;
# optionally pass the results through `deflate` with or without a joiner)
#
# (multikey trees and paths are very useful for very quickly generating a fast
# indexed/searchable data structure)
#
# (once harmonization is complete, rename these functions to `groupby`
# and `indexby` and ditch the old ones)

def tree(l, *keys, connector=None):
    indexed = {}
    for el in l:
        branch = indexed
        for key in keys[:-1]:
            value = getattr(el, key)
            branch = branch.setdefault(value, {})
        value = getattr(el, keys[-1])
        branch.setdefault(value, []).append(el)
    return indexed


def _must_be_unique(l):
    if len(l) > 1:
        raise ValueError()
    else:
        return l


def path(l, *keys, connector=None, strict=True, index=0):
    indexed = tree(l, *keys, connector=connector)

    if strict:
        transform(indexed, values=_must_be_unique)
    elif index:
        indexed = transform(indexed, values=utils.index(index))

    if connector is not None:
        indexed = reshape.deflate(indexed, connector=connector)

    return indexed
