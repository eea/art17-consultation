import re
from decimal import Decimal

patt = re.compile(r"(?<!\d)(\d+)(\.0*)?(?!\d)")


def str2num(s, default='N/A'):
    """ Check if a string can be represented as integer"""
    if s is None:
        return default
    if isinstance(s, Decimal):
        buffer = '%.2f' % s
    else:
        buffer = str(s)
    if buffer:
        return re.sub(patt, r"\1", buffer)
    else:
        return default
