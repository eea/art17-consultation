import base64
import urllib
import flask
from jinja2 import Markup, escape
from art17 import models
from art17.common import get_default_period

maps = flask.Blueprint('maps', __name__)


@maps.route('/<page>/map')
def maps_view(page):
    if page == 'species':
        config_url = flask.url_for('.species_config_xml',
                                   region=flask.request.args.get('region'),
                                   species=base64.b64encode(
                                       flask.request.args.get('species')),
                                   _external=True,
                                   )

    elif page == 'habitats':
        config_url = flask.url_for('.habitats_config_xml',
                                   region=flask.request.args.get('region'),
                                   habitat=flask.request.args.get('habitat'),
                                   _external=True,
                                   )

    else:
        flask.abort(404)

    return flask.render_template('maps/view.html',
                                 config_url=config_url,
                                 )


@maps.route('/species/map/config.xml')
def species_config_xml():
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
        or 'admin' in roles
        or 'nat' in roles
    )

    body = flask.render_template('maps/config-species.xml',
                                 restricted=restricted,
                                 extent=','.join(str(v) for v in extent),
                                 assessment_speciesname=assesment_speciesname,
                                 countries_style=Markup('&'.join(
                                     escape(s) for s in countries_style)),
                                 region=region,
                                 )
    return flask.Response(body, content_type='text/xml')


@maps.route('/habitats/map/config.xml')
def habitats_config_xml():
    dataset_id = get_default_period()

    def select_habitat_regions(habitatcode):
        """
        SELECT DISTINCT 
          etc_data_habitattype_regions.region
        FROM
          etc_data_habitattype_regions
        WHERE <dtml-sqltest name="habitatcode" column="etc_data_habitattype_regions.habitatcode" type=string>
        """
        return (
            models.db.session.query(
                models.EtcDataHabitattypeRegion.region,
            )
            .distinct()
            .filter_by(dataset_id=dataset_id)
            .filter_by(habitatcode=habitatcode)
        )

    def getRegions(habitat):
        regions = ['^%s' % rec.region for rec in
                   select_habitat_regions(habitatcode=habitat)]
        return '|'.join(regions)

    def select_habitat_countries(region_list, habitatcode):
        """
        SELECT
          eu_country_code,
          code,
          conclusion_assessment,
          region
        FROM
          etc_data_habitattype_regions
        WHERE <dtml-sqltest region type="string" multiple="multiple">
        AND <dtml-sqltest habitatcode type=string>
        """
        return (
            models.db.session.query(
                models.EtcDataHabitattypeRegion.eu_country_code,
                models.EtcDataHabitattypeRegion.code,
                models.EtcDataHabitattypeRegion.conclusion_assessment,
                models.EtcDataHabitattypeRegion.region,
            )
            .filter(models.EtcDataHabitattypeRegion.region.in_(region_list))
            .filter_by(habitatcode=habitatcode)
            .filter_by(dataset_id=dataset_id)
        )

    def background_colour(value):
        colors = ('#9CB34D', '#D16E43', '#D16E43', '#D16E43', '#C22C15',
                  '#C22C15', '#C22C15', '#6F6C66', '#FFFFFF')
        assessments = ('FV', 'U1', 'U1-', 'U1+', 'U2', 'U2-', 'U2+', 'XX', '')

        RGBS = dict(zip(assessments, [x for x in colors]))
        colour = RGBS.get(value, '')
        if colour:
            return colour[1:]
        else:
            return ''

    region = flask.request.args.get('region', '')
    habitat = flask.request.args.get('habitat', '')
    if region == '':
        region = '/%s/' % getRegions(habitat)
    else:
        region = "/^%s/" % region
    results = select_habitat_countries(
        region_list=region[1:-1].replace('^', '').split('|'),
        habitatcode=habitat)

    countries_style = []
    countries = []
    habitat_code = ''

    for res in results:
        if res.eu_country_code == 'UK':
            country = 'GB'
        else: 
            if res.eu_country_code == 'EL':
                country = 'GR'
            else:
                country = res.eu_country_code
        habitat_code = res.code
        countries.append(country)
        countries_style.append('l=%s%s|%s' % (
            country,
            res.region,
            background_colour(res.conclusion_assessment)))

    qstring="/%s/" % '|'.join(countries)
    #extent = get_coordinates(region, qstring)
    extent = [2635945.400202,1385857.104555,6084637.867846,5307244.006638]

    body = flask.render_template('maps/config-habitats.xml',
                                 extent=','.join(str(v) for v in extent),
                                 habitat_code=habitat_code,
                                 countries_style=Markup('&'.join(
                                     escape(s) for s in countries_style)),
                                 region=region,
                                 )
    return flask.Response(body, content_type='text/xml')
