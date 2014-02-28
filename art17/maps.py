import base64
import urllib
import flask
from jinja2 import Markup, escape
from art17 import models
from art17.common import get_default_period

maps = flask.Blueprint('maps', __name__)


@maps.app_template_filter('base64encode')
def base64encode(value):
    return base64.b64encode(value)


@maps.route('/<page>/map')
def maps_view(page):
    return flask.render_template('maps/view.html',
        region=flask.request.args.get('region'),
        species=flask.request.args.get('species'),
    )


@maps.route('/<page>/map/config.xml')
def config_xml(page):
    dataset_id = get_default_period()
    region = flask.request.args.get('region', '')
    species = flask.request.args.get('species', '')
    species_name = base64.urlsafe_b64decode(species.encode('ascii'))

    user = flask.g.get('user')
    roles = [r.name for r in user.roles] if user and user.id else []

    if region == '':
       rows = (
           models.db.session.query(
               models.EtcDataSpeciesRegion.region
           )
           .distinct()
           .filter_by(assesment_speciesname=species_name)
           .filter(models.EtcDataSpeciesRegion.dataset_id == dataset_id)
           .order_by(models.EtcDataSpeciesRegion.region)
       )
       region = '/%s/' % '|'.join(['^%s' % rec[0] for rec in rows])
    else:
       region = "/^%s/" % region

    results = (
        models.db.session.query(
            models.EtcDataSpeciesRegion.eu_country_code,
            models.EtcDataSpeciesRegion.code,
            models.EtcDataSpeciesRegion.conclusion_assessment,
            models.EtcDataSpeciesRegion.region
        )
        .filter(
            models.EtcDataSpeciesRegion.region.in_(
                region[1:-1].replace('^', '').split('|'))
        )
        .filter(models.EtcDataSpeciesRegion.dataset_id == dataset_id)
        .filter(models.EtcDataSpeciesRegion.assesment_speciesname
                == species_name)
    )


    assesment_speciesname=urllib.quote(species_name)

    countries_style = []
    countries = []
    species_code = ''

    def background_colour(value):
        colors = ['#70a800','#e69800','#e69800','#e69800','#d62b00',
                  '#d62b00','#d62b00','#b4b4b4','#FFFFFF']
        assessments = ['FV','U1','U1-','U1+','U2','U2-','U2+','XX','']

        RGBS = dict(zip(assessments, [x for x in colors]))
        colour = RGBS.get(value,'')
        if colour:
            return colour[1:]
        else:
            return ''

    def get_coordinates(region="/MED/", qstring="/FR|RO|IT/",
                        url="http://merlin.eea.europa.eu/cgi-bin/art17wsQ?%s"):
        """ open url and sort coordinates """
        params = urllib.urlencode({
            'mode':'ITEMNQUERY', 
            'LAYER': 'Europe_BIOGEO_MERGE30Jan', 
            'qlayer': 'Europe_BIOGEO_MERGE30Jan',
            'qitem': 'Country',
            'rg': region,
            'qstring': qstring})
        f = urllib.urlopen(url % params)
        line = f.readline()
        minx, miny, maxx, maxy = line.split()
        for line in f.readlines():
            cur_minx, cur_miny, cur_maxx, cur_maxy = line.split()
            minx = min(minx, cur_minx)
            maxx = max(maxx, cur_maxx)
            miny = min(miny, cur_miny)
            maxy = max(maxy, cur_maxy)
        return [minx, miny, maxx, maxy]

    for res in results:
        if res.eu_country_code == 'UK':
            country = 'GB'
        else: 
            if res.eu_country_code == 'EL':
               country = 'GR'
            else:
               country = res.eu_country_code
        species_code = res.code
        countries.append(country)
        countries_style.append('l=%s%s|%s' % (country, res.region, background_colour(res.conclusion_assessment)))

    qstring="/%s/" % '|'.join(countries)
    #extent = get_coordinates(region, qstring)
    extent = [2635945.400202,1385857.104555,6084637.867846,5307244.006638]

    rows = (
        models.db.session.query(
            models.t_restricted_species.c.eu_country_code,
        )
        .filter(models.t_restricted_species.c.assesment_speciesname
                == species_name)
        .filter(models.t_restricted_species.c.ext_dataset_id == dataset_id)
    )
    restricted_species_list = [r[0] for r in rows]
    restricted = not (
        (species_name.lower() not in restricted_species_list)
        or auth_roles['expert']
        or auth_roles['administrator']
    )

    body = flask.render_template('maps/config.xml',
        restricted=restricted,
        extent=','.join(str(v) for v in extent),
        assessment_speciesname=assesment_speciesname,
        countries_style=Markup('&'.join(escape(s) for s in countries_style)),
        region=region,
    )
    return flask.Response(body, content_type='text/xml')
