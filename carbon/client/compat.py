import sys


PY3 = sys.version_info > (3,)


try:
    basestring = basestring
except NameError:
    basestring = str


def b(obj):
    if PY3:
        if isinstance(obj, str):
            return obj.encode('utf-8')
    else:
        if not isinstance(obj, str):
            return obj.encode('utf-8')

    return obj
