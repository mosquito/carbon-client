# encoding: utf-8
from functools import wraps
from carbon.client import stat, metrics


def timeit(name, client=stat):
    def decorator(func):
        @wraps(func)
        def wrap(*args, **kwargs):
            client[name] = metrics.Timer
            watch = client[name].start()
            res = func(*args, **kwargs)
            client[name].stop(watch)
            return res
        return wrap
    return decorator
