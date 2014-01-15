import flask

layout = flask.Blueprint('layout', __name__)


@layout.record
def set_up_layout_template(state):
    app = state.app
    app.jinja_env.globals['layout_template'] = 'layout_default.html'
