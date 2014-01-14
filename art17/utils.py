import re


patt = re.compile(r"(?<!\d)(\d+)(\.0*)?(?!\d)")


def str2num(s, default='N/A'):
    """ check if a string can be represented as integer"""
    if s is None:
        return default
    buffer = str(s)
    if buffer:
        return re.sub(patt, r"\1", buffer)
    else:
        return default
