# -*- coding: utf-8 -*-
import re
import HTMLParser
__author__ = 'lehmann'


def abstractmethod(method):
    """
    Decorator for abstract methods.

    """
    def default_abstract_method(*args, **kwargs):
        raise NotImplementedError('call to abstract method ' + repr(method))
    default_abstract_method.__name__ = method.__name__
    return default_abstract_method


def extract_number(text):
    """
    Extract a floating point number as text from a given string.

    """
    return "".join(re.findall(r"[-+]?[0-9]*[\,.]?[0-9]", text))


def limit_str(str_, len_):
    """
    Limit length of string to len_. Fill with Spaces if required.
    """
    return str_.ljust(len_)[:len_]

def extract_float(str_):
    """
    Extracts a float from a given String. Decimal is ',' and Thousand
    seperator is ",".

    @rtype: float

    """
    pattern = re.compile(r"\b[0-9]{1,3}(\.[0-9]{3})*(,[0-9]+)?\b|,[0-9]+\b")
    res = pattern.search(str_).group()

    if not res:
        return

    res = res.replace(".", "")
    res = res.replace(",", ".")

    return float(res)


def html_to_str(html):
    return html #HTMLParser.HTMLParser().unescape(html)