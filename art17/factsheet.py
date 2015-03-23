from flask import Blueprint, render_template
from flask.views import MethodView

factsheet = Blueprint('factsheets', __name__)


class SpeciesFactSheet(MethodView):

    def get(self):
        return render_template('factsheet/species.html')


class HabitatFactSheet(MethodView):

    def get(self):
        return render_template('factsheet/habitat.html')


factsheet.add_url_rule('/species/factsheet/',
                       view_func=SpeciesFactSheet.as_view('factsheet-species'))
factsheet.add_url_rule('/habitat/factsheet/',
                       view_func=SpeciesFactSheet.as_view('factsheet-habitat'))
