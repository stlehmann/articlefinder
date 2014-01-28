import re
__author__ = 'lehmann'


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