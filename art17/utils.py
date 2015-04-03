# -*- coding: utf-8 -*-
import re
from decimal import Decimal
from bs4 import BeautifulSoup
from markupsafe import Markup
from path import path
from flask import current_app as app


patt = re.compile(r"(?<!\d)(\d+)(\.0*)?(?!\d)")
valid_numeric = re.compile("^\s*" + "(" + "(\d\.)?\d+\s*-\s*(\d\.)?\d+" +
                           u"|(>|>>|≈|<)?\s*((\d\.)?\d+)" + ")" + "\s*$")
valid_ref = re.compile("^\s*" + "(" + "(\d\.)?\d+\s*-\s*(\d\.)?\d+" +
                       u"|(>|>>|≈|<)?\s*((\d\.)?\d+)?|x" + ")" + "\s*$")
empty_str = re.compile("^\s*$")


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
        return bool(valid_numeric.match(s))
    return True


def validate_ref(s):
    """ Checks if a field is a valid numeric or progress value
    """
    if s:
        return bool(valid_ref.match(s))
    return True


def validate_nonempty(s):
    """ Checks if a ckeditor text is empty (whitespaces only)
    """
    if s:
        soup = BeautifulSoup(s)
        return not bool(empty_str.match(soup.text.replace(u'\xa0', ' ')))
    return False


def na_if_none(s, default='N/A'):
    if s is None:
        return default
    return s


def inject_static_file(filepath):
    data = None
    with open(path(app.static_folder) / filepath, 'r') as f:
        data = f.read()
    return Markup(data)


_slugify_strip_re = re.compile(r'[^\w\s-]')
_slugify_hyphenate_re = re.compile(r'[-\s]+')


def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.

    From Django's "django/template/defaultfilters.py".
    """
    import unicodedata

    if not isinstance(value, unicode):
        value = unicode(value)
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(_slugify_strip_re.sub('', value).strip().lower())
    return _slugify_hyphenate_re.sub('-', value)
