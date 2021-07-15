import os.path
import jinja2
from flask import render_template
from flask.ext.script import Manager

from art17.models import EtcDataSpeciesRegion, EtcDataHabitattypeRegion
from art17.app import create_app


COUNTRY = 'ro'
BIOREGIONS = [
    u'MED', u'CON', u'ATL', u'ALP', u'BLS', u'PAN', u'BOR', u'MAC', u'STE',
    u'MMED', u'MATL', u'MMAC', u'MBAL', u'MBLS'
]

app = create_app()
app.jinja_loader = jinja2.FileSystemLoader(
    os.path.abspath(os.path.dirname(__file__)))
mgr = Manager(app)


def valid_regions(data):
    return [region for region in BIOREGIONS if region in data.keys()]


def _get_report(model_cls, template):
    data = {}
    qs = model_cls.query.filter_by(country=COUNTRY)
    for species in qs:
        data.setdefault(species.subject, {})
        region_key = species.region
        if region_key in data[species.subject]:
            print("* already exists, switch key: ", (
                species.code, species.region, species.region_ms
            ))
            region_key = species.region_ms
        data[species.subject][region_key] = species
    result = render_template(template, objects=data, BIOREGIONS=BIOREGIONS,
                             valid_regions=valid_regions)
    file_out = "out-" + template
    with open(file_out, "wb") as fh:
        fh.write(result.encode('utf-8'))
    print("Done", file_out, "written")


@mgr.command
def get_species():
    return _get_report(EtcDataSpeciesRegion, 'species.html')


@mgr.command
def get_habitat():
    return _get_report(EtcDataHabitattypeRegion, 'habitat.html')


if __name__ == '__main__':
    mgr.run()

