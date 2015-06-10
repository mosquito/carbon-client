#!/usr/bin/env python
# encoding: utf-8
from functools import wraps

from .. import stat, metrics


def timeit(name, client=stat):
    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            client[name] = metrics.Timer
            with client[name]:
                return func(*args, **kwargs)
        return wrap
    return decorator
