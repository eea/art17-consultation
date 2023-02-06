# -*- coding: utf-8 -*-
import re
from decimal import Decimal

from bs4 import BeautifulSoup
from flask import current_app as app
from markupsafe import Markup
from path import Path

patt = re.compile(r"(?<!\d)(\d+)(\.0*)?(?!\d)")
valid_float = re.compile("^\s*((?=.*[1-9])\d*(?:\.\d{1,2})?|x)\s*$")
valid_numeric = re.compile(
    "^\s*(((\d*\.)?\d+\s*-\s*(\d*\.)?\d+"
    + "|(>|>>|≈|<)?\s*((\d*\.)?\d+))|N/A|X|x)\s*$"
)
valid_ref = re.compile(
    "^\s*((\d*\.)?\d+\s*-\s*(\d\.)?\d+" + "|(>|>>|≈|<)?\s*((\d*\.)?\d+)?|x)\s*$"
)
empty_str = re.compile("^\s*$")
operator = re.compile("^\s*" + "(>|>>|≈|<|x)?\s*$")


def str2num(s, default="N/A", number_format="%.2f"):
    """Check if a string can be represented as integer"""
    if s is None:
        return default
    if s == 0:
        return default
    if isinstance(s, Decimal):
        buffer = number_format % s
    else:
        buffer = str(s)
    if buffer:
        return re.sub(patt, r"\1", buffer)
    else:
        return default


def str1num(s, default="N/A"):
    return str2num(s, default=default, number_format="%.1f")


def parse_semicolon(s, sep="<br />"):
    """Replaces all semicolons found in the string ${s} with
    the given separator ${sep}"""
    if s is None:
        return s
    patt = re.compile(r";\s*")
    return patt.sub(sep, s)


def validate_field(s):
    """Checks if a field is a valid numeric or progress value"""
    if s:
        return bool(valid_numeric.match(s))
    return True


def validate_float(s):
    """Checks if a field is a valid float with 2 decimals"""
    if s:
        return bool(valid_float.match(s))
    return True


def validate_ref(s):
    """Checks if a field is a valid numeric or progress value"""
    if s:
        return bool(valid_ref.match(s))
    return True


def validate_operator(s):
    """Checks if the field is (>,>>,<, x , ≈ )"""
    if s:
        return bool(operator.match(s))
    return True


def validate_nonempty(s):
    """Checks if a ckeditor text is empty (whitespaces only)"""
    if s:
        soup = BeautifulSoup(s, "html.parser")
        return not bool(empty_str.match(soup.text.replace("\xa0", " ")))
    return False


def na_if_none(s, default="N/A"):
    if s is None:
        return default
    return s


def inject_static_file(filepath):
    data = None
    with open(Path(app.static_folder) / filepath, "r") as f:
        data = f.read()
    return Markup(data)


# See: https://gist.github.com/berlotto/6295018
_slugify_strip_re = re.compile(r"[^\w\s-]")
_slugify_hyphenate_re = re.compile(r"[-\s]+")


def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.

    From Django's "django/template/defaultfilters.py".
    """
    import unicodedata

    if not value:
        return ""
    if not isinstance(value, str):
        value = str(value)
    value = (
        unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()
    )
    value = _slugify_strip_re.sub("", value).strip().lower()
    value = _slugify_hyphenate_re.sub("-", value)
    return value
