import re
from decimal import Decimal

patt = re.compile(r"(?<!\d)(\d+)(\.0*)?(?!\d)")
valid_ref = re.compile(
    '^\s*' + '(>|>>|~|<)?\s*(\d+)?(\.\d{0,2})?\s*' +
    '(-\s*(>|>>|~|<)?(\d+)?(\.\d{0,2})?\s*)?' + '$'
)


def str2num(s, default='N/A', number_format='%.2f'):
    """ Check if a string can be represented as integer"""
    if s is None:
        return default
    if isinstance(s, Decimal):
        buffer = number_format % s
    else:
        buffer = unicode(s)
    if buffer:
        return re.sub(patt, r"\1", buffer)
    else:
        return default


def str1num(s, default='N/A'):
    return str2num(s, default=default, number_format='%.1f')


def parse_semicolon(s, sep='<br />'):
    """ Replaces all semicolons found in the string ${s} with
    the given separator ${sep} """
    if s is None:
        return s
    patt = re.compile(r';\s*')
    return patt.sub(sep, s)


def validate_field(s):
    """ Checks if a field is a valid numeric or progress value
    """
    if s:
        return bool(valid_ref.match(s))
    return True
