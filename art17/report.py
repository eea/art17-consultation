from flask import Blueprint, jsonify, render_template, request, url_for, views, abort
from sqlalchemy import func
from werkzeug.datastructures import MultiDict

from art17.common import (
    favourable_ref_title_habitat,
    favourable_ref_title_species,
    generate_map_url,
    get_default_period,
)
from art17.forms import ReportFilterForm
from art17.mixins import HabitatMixin, MixinsCommon, SpeciesMixin
from art17.models import Dataset

report = Blueprint("report", __name__)


class Report(views.View):
    def dispatch_request(self):
        period = request.args.get("period") or get_default_period()
        try:
            period = int(period)
        except ValueError:
            abort(404)
        group = request.args.get("group")
        country = request.args.get("country")
        region = request.args.get("region")
        self.objects = []
        self.setup_objects_and_data(period, group, country, region)

        countries = self.get_countries(period)
        regions = self.get_regions_by_country(period, country)
        report_filter_form = ReportFilterForm(
            MultiDict(dict(period=period, group=group, country=country, region=region))
        )
        report_filter_form.group.choices = self.get_groups(period)
        report_filter_form.country.choices = countries
        report_filter_form.region.choices = regions

        countries_map = dict(countries)
        regions_map = dict(regions)
        period_query = Dataset.query.get(period)
        period_name = period_query.name if period_query else ""

        current_selection = self.get_current_selection(
            period_name,
            group,
            countries_map.get(country, country),
            regions_map.get(region, region),
        )

        context = self.get_context()
        context.update(
            {
                "objects": self.objects,
                "current_selection": current_selection,
                "report_filter_form": report_filter_form,
                "region": region,
                "country": country,
                "show_report_headers": True,
                "dataset": period_query,
                "generate_map_url": generate_map_url,
            }
        )

        return render_template(self.template_name, **context)

    def get_current_selection(self, period_name, group, country_name, region_name):
        if not group or country_name == "-":
            return []
        return [period_name, group, country_name, region_name]

    def setup_objects_and_data(self, period, group, country, region):
        GROUPS_2006 = {
            "Bogs, mires & fens": "bogs, mires & fens",
            "Coastal habitats": "coastal habitats",
            "Dunes habitats": "dunes habitats",
            "Forests": "forests",
            "Freshwater habitats": "freshwater habitats",
            "Grasslands": "grasslands",
            "Heath & scrub": "heath & scrub",
            "Rocky habitats": "rocky habitats",
            "Sclerophilus scrub": "sclerophyllous scrub",
            "bogs, mires & fens": "bogs, mires & fens",
            "coastal habitats": "coastal habitats",
            "dunes habitats": "dunes habitats",
            "forests": "forests",
            "freshwater habitats": "freshwater habitats",
            "grasslands": "grasslands",
            "heath & scrub": "heath & scrub",
            "rocky habitats": "rocky habitats",
            "sclerophyllous scrub": "sclerophyllous scrub",
        }
        filter_args = {}
        if not group:
            return
        if period == "1":
            group = GROUPS_2006.get(group, group)

        filter_args["dataset_id"] = period
        if country:
            filter_args["eu_country_code"] = country
        if region:
            filter_args["region"] = region
        self.objects = (
            self.model_cls.query.filter(
                func.lower(self.model_cls.group) == func.lower(group)
            )
            .filter_by(**filter_args)
            .order_by(self.model_cls.subject)
        )


class SpeciesReport(SpeciesMixin, Report):

    template_name = "report/species.html"

    def get_context(self):
        return {
            "groups_url": url_for("common.species-groups"),
            "regions_url": url_for(".species-report-regions"),
            "countries_url": url_for(".species-report-countries"),
            "favourable_ref_title": favourable_ref_title_species,
        }


class HabitatReport(HabitatMixin, Report):

    template_name = "report/habitat.html"

    def get_context(self):
        return {
            "groups_url": url_for("common.habitat-groups"),
            "regions_url": url_for(".habitat-report-regions"),
            "countries_url": url_for(".habitat-report-countries"),
            "favourable_ref_title": favourable_ref_title_habitat,
        }


@report.route("/species/report/regions", endpoint="species-report-regions")
def species_regions():
    try:
        period = int(request.args.get("period", ""))
    except ValueError:
        abort(404)
    try:
        country = request.args["country"]
    except KeyError:
        abort(400)
    data = SpeciesMixin.get_regions_by_country(period, country)
    return jsonify([list(row) for row in data])


@report.route("/species/report/countries", endpoint="species-report-countries")
def species_countries():
    try:
        period = int(request.args.get("period", ""))
    except ValueError:
        abort(404)
    data = MixinsCommon.get_countries(period)
    return jsonify([list(row) for row in data])


@report.route("/habitat/report/regions", endpoint="habitat-report-regions")
def habitat_regions():
    try:
        period = int(request.args.get("period", ""))
    except ValueError:
        abort(404)
    try:
        country = request.args["country"]
    except KeyError:
        abort(400)
    data = HabitatMixin.get_regions_by_country(period, country)
    return jsonify([list(row) for row in data])


@report.route("/habitat/report/countries", endpoint="habitat-report-countries")
def habitat_countries():
    try:
        period = int(request.args.get("period", ""))
    except ValueError:
        abort(404)

    data = MixinsCommon.get_countries(period)
    return jsonify([list(row) for row in data])


report.add_url_rule(
    "/species/report/", view_func=SpeciesReport.as_view("species-report")
)
report.add_url_rule(
    "/habitat/report/", view_func=HabitatReport.as_view("habitat-report")
)
