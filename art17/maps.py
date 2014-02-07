import flask

maps = flask.Blueprint('maps', __name__)


@maps.route('/<page>/map')
def maps_view(page):
    return flask.render_template('maps/view.html')


@maps.route('/<page>/map/config.xml')
def config_xml(page):
    body = flask.render_template('maps/config.xml')
    return flask.Response(body, content_type='text/xml')
