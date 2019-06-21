import re
import logging
import requests
import flask
from jinja2 import Markup

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

layout = flask.Blueprint('layout', __name__)

header_pattern = (
    r'^.*'
    r'<title>(?P<title>[^<]*)</title>'
    r'.*'
    r'(?P<endofhead>)</head>'
    r'.*'
    r'<body>(?P<startofbody>)'
    r'.*'
    r'(?P<breadcrumbs><div class="breadcrumbitemlast">[^<]*</div>)'
    r'.*'
    r'(?P<leftcolumn><div id="leftcolumn">.*)<div id="workarea">'
    r'.*$'
)

