import collections
import datetime
import math
import time

from . import utils
from .reshape import items


def simplify_numeric(obj, **options):
    if obj.dtype.name.startswith('int'):
        return int(obj)
    else:
        return float(obj)

SERIALIZERS = (
    ('dtype', simplify_numeric),
)

def simplify(obj, force=False, skip=False, strict=True, allow_nan=False, convert_dates=True, quantize=utils.identity, serializers=()):
    if force and skip or strict and skip:
        raise ValueError()

    serializers = SERIALIZERS + serializers
    options = dict(
        force=force,
        skip=skip,
        strict=strict,
        allow_nan=allow_nan,
        convert_dates=convert_dates,
        quantize=quantize,
        serializers=serializers,
        )
    """
    `force` will convert every element, converting it to a string (using `str` or `repr`)
    if necessary

    `skip` will skip any elements that cannot be simplified instead of leaving them
    as-is; these elements are ommitted from the simplified dictionary

    `strict` will raise an error if an object needs to be simplified but we don't know how,
    unless `force` is True or `skip` is True

    This function works in depth, and can accept dictionaries, lists of dictionaries
    or any other kind of object.

    * _asdict()
    * __dict__ (but ignore _ and __)
    * serialize()
    * _dtype
    * iterator -> list
    * nan, inf -> none
    * for match, serialize in serializers: if isinstance(obj, match) then serialize
    * for match, serialize in serializers: if isinstance(match, str) and hasattr(obj, match) then serialize
      (= duck typing)
    * convert_dates: `iso` or `timestamp` (True => 'iso')
    * str or repr
    """
    if isinstance(obj, (str, int, bool, type(None))):
        return obj
    elif isinstance(obj, float):
        if math.isfinite(obj):
            return quantize(obj)
        else:
            if allow_nan:
                return obj
            else:
                return None
    elif hasattr(obj, 'items'):
        return {simplify(key, **options): simplify(value, **options) for key, value in obj.items()}
    elif isinstance(obj, collections.Iterable) and not isinstance(obj, str):
        return [simplify(value, **options) for value in obj]
    elif hasattr(obj, '_asdict'):
        return simplify(obj._asdict())
    elif hasattr(obj, 'serialize'):
        return simplify(obj.serialize())
    elif convert_dates and isinstance(obj, (datetime.date, datetime.datetime)):
        if convert_dates == 'timestamp':
            return time.mktime(obj.timetuple())
        elif convert_dates == 'iso' or convert_dates is True:
            return obj.isoformat()
        else:
            raise ValueError(f'`convert_dates` must be "timestamp" or "iso", but received {convert_dates}')
    else:
        for predicate, serialize in serializers:
            if isinstance(predicate, str) and hasattr(obj, predicate):
                return simplify(serialize(obj, **options), **options)
            elif isinstance(predicate, type) and isinstance(obj, predicate):
                return simplify(serialize(obj, **options), **options)

        if force:
            return str(obj)
        elif skip:
            # TODO
            return ValueError()
        elif strict:
            raise ValueError(f'Could not serialize {obj} {type(obj)}.')
        else:
            return obj
