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
    r'.*$'
)


@layout.record
def set_up_layout_template(state):
    app = state.app
    zope_url = app.config.get('LAYOUT_ZOPE_URL')

    if zope_url:
        app.jinja_env.globals['layout_template'] = 'layout_zope.html'
        app.before_request(load_zope_template)

    else:
        app.jinja_env.globals['layout_template'] = 'layout_default.html'


def split_layout(header, footer):

    m = re.match(header_pattern, header, re.DOTALL)
    if m is None:
        logger.error("Could not match header: %r", header)
        return {}

    return {
        'start_to_title':
            Markup(header[:m.start('title')]),
        'title_to_endofhead':
            Markup(header[m.end('title'):m.start('endofhead')]),
        'endofhead_to_startofbody':
            Markup(header[m.end('endofhead'):m.start('startofbody')]),
        'startofbody_to_breadcrumbs':
            Markup(header[m.end('startofbody'):m.start('breadcrumbs')]),
        'breadcrumbs_to_content':
            Markup(header[m.end('breadcrumbs'):]),
        'content_to_end':
            Markup(footer),
    }


def load_zope_template():
    zope_url = flask.current_app.config['LAYOUT_ZOPE_URL']
    auth_header = flask.request.headers.get('Authorization')
    resp = requests.get(zope_url, headers={'Authorization': auth_header})
    resp_json = resp.json()
    flask.g.zope_layout = split_layout(
        resp_json['standard_html_header'],
        resp_json['standard_html_footer'],
    )
