import re
import time
import logging


logger = logging.getLogger("articlefinder.core.utilities")


def abstractmethod(method):
    """
    Decorator for abstract methods.

    """
    def default_abstract_method(*args, **kwargs):
        raise NotImplementedError('call to abstract method ' + repr(method))

    default_abstract_method.__name__ = method.__name__

    # pass along the decorated function's docstring and repr
    default_abstract_method.__doc__ = method.__doc__
    default_abstract_method.__repr__ = method.__repr__

    return default_abstract_method


def limit(str_, len_):
    """
    Limit length of string to len_. Fill with Spaces if required.

    :returns: basestring

    >>> limit("This ist a test string.", 10)
    This is a

    >>> len(limit("one", 10))
    10
    """
    return str_.ljust(len_)[:len_]


def extract_float(str_):
    """
    Extracts a float from a given String. Decimal is ',' and Thousand
    seperator is ".".

    :returns: float -- The extracted number

    >>> extract_float("The number is 12.567,57.")
    12567.57

    """
    pattern = re.compile(r"\b[0-9]{1,3}(\.[0-9]{3})*(,[0-9]+)?\b|,[0-9]+\b")
    res = pattern.search(str_)

    if res is None:
        return 0.0

    res = res.group()
    res = res.replace(".", "")
    res = res.replace(",", ".")

    return float(res)

def timeit(func):
    def wrapper(*args, **kwargs):
        t1 = time.clock()
        res = func(*args, **kwargs)
        diff = time.clock() - t1
        print("%s: %.3f" % (func.__name__, diff))
        return res, func.__name__
    return wrapper

def attr_at_index(x, index=0, attr='text'):
    """
    Get an attribute of an element inside a list.

    """
    try:
        if attr == 'text':
            return x[index].text
        else:
            return x[index].get(attr)
    except IndexError:
        return ""