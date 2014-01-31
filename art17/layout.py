import flask
import requests

layout = flask.Blueprint('layout', __name__)


@layout.record
def set_up_layout_template(state):
    app = state.app
    zope_url = app.config.get('LAYOUT_ZOPE_URL')
    app.jinja_env.globals['layout_wiki'] = 'layout_wiki.html'

    if zope_url:
        app.jinja_env.globals['layout_template'] = 'layout_zope.html'
        app.before_request(load_zope_template)

    else:
        app.jinja_env.globals['layout_template'] = 'layout_default.html'


def load_zope_template():
    zope_url = flask.current_app.config['LAYOUT_ZOPE_URL']
    resp = requests.get(zope_url)
    flask.g.zope_layout = resp.json()

    art17_css = flask.render_template('header_styles.html')
    flask.g.zope_layout['standard_html_header'] = \
        flask.g.zope_layout['standard_html_header'].replace(
            '</head>', art17_css + '</head>')
