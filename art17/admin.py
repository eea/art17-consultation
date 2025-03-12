from flask import abort
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from art17.common import admin_perm
from art17.models import (
    Config,
    Dataset,
    DicCountryCode,
    EtcDataHcoveragePressure,
    EtcDataHcoverageThreat,
    EtcDataSpopulationPressure,
    EtcDataSpopulationThreat,
    EtcDicBiogeoreg,
    EtcDicConclusion,
    EtcDicDecision,
    EtcDicHdHabitat,
    EtcDicMethod,
    EtcDicPopulationUnit,
    EtcDicSpeciesType,
    EtcDicTrend,
    EtcQaErrorsHabitattypeManualChecked,
    EtcQaErrorsSpeciesManualChecked,
    db,
)


class CustomAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if not admin_perm.can():
            return abort(404)
        return super(CustomAdminIndexView, self).index()


class ProtectedModelView(ModelView):

    def is_accessible(self):
        return admin_perm.can()

    def inaccessible_callback(self, name, **kwargs):
        return abort(404)


class DatasetModelView(ProtectedModelView):
    form_columns = (
        "id",
        "name",
        "schema",
        "species_map_url",
        "sensitive_species_map_url",
        "habitat_map_url",
    )
    column_list = (
        "id",
        "name",
        "schema",
        "species_map_url",
        "sensitive_species_map_url",
        "habitat_map_url",
    )
    column_filters = ["id", "schema"]


class DicCountryCodeModelView(ProtectedModelView):
    form_columns = ("dataset_id", "code", "codeEU", "name")
    column_list = ("dataset_id", "code", "codeEU", "name")
    column_filters = ["dataset_id", "code", "codeEU", "name"]


class DicEunisCodeModelView(ProtectedModelView):
    form_columns = ("code", "level", "label", "description")
    column_list = ("code", "level", "label", "description")
    column_filters = ["code", "level"]


class EtcDataHcoveragePressureModelView(ProtectedModelView):
    form_columns = (
        "dataset_id",
        "eu_country_code",
        "region",
        "habitatcode",
        "pressure",
    )
    column_list = ("dataset_id", "eu_country_code", "region", "habitatcode", "pressure")
    column_filters = ["dataset_id", "eu_country_code", "region", "habitatcode"]


class EtcDataHcoverageThreatModelView(ProtectedModelView):
    form_columns = ("dataset_id", "eu_country_code", "region", "habitatcode", "threat")
    column_list = ("dataset_id", "eu_country_code", "region", "habitatcode", "threat")
    column_filters = ["dataset_id", "eu_country_code", "region", "habitatcode"]


class EtcDataSpopulationPressureModelView(ProtectedModelView):
    form_columns = (
        "dataset_id",
        "eu_country_code",
        "region",
        "n2000_species_code",
        "assesment_speciesname",
        "pressure",
    )
    column_list = (
        "dataset_id",
        "eu_country_code",
        "region",
        "n2000_species_code",
        "assesment_speciesname",
        "pressure",
    )
    column_filters = ["dataset_id", "eu_country_code", "region", "n2000_species_code"]


class EtcDataSpopulationThreatModelView(ProtectedModelView):
    form_columns = (
        "dataset_id",
        "eu_country_code",
        "region",
        "n2000_species_code",
        "assesment_speciesname",
        "threat",
    )
    column_list = (
        "dataset_id",
        "eu_country_code",
        "region",
        "n2000_species_code",
        "assesment_speciesname",
        "threat",
    )
    column_filters = ["dataset_id", "eu_country_code", "region", "n2000_species_code"]


class EtcDicBiogeoregModelView(ProtectedModelView):
    form_columns = ("dataset_id", "reg_code", "reg_name", "ordine", "order")
    column_list = ("dataset_id", "reg_code", "reg_name", "ordine", "order")
    column_filters = [
        "dataset_id",
        "reg_code",
        "reg_name",
    ]


class EtcDicConclusionModelView(ProtectedModelView):
    form_columns = ("dataset_id", "conclusion", "details", "order")
    column_list = ("dataset_id", "conclusion", "details", "order")
    column_filters = ["dataset_id", "conclusion"]


class EtcDicDecisionModelView(ProtectedModelView):
    form_columns = ("dataset_id", "decision", "details", "order")
    column_list = ("dataset_id", "decision", "details", "order")
    column_filters = ["dataset_id", "decision"]


class EtcDicHdHabitatModelView(ProtectedModelView):
    form_columns = (
        "dataset_id",
        "group",
        "habcode",
        "name",
        "shortname",
        "priority",
        "annex_I_comments",
        "marine",
    )
    column_list = (
        "dataset_id",
        "group",
        "habcode",
        "name",
        "shortname",
        "priority",
        "annex_I_comments",
        "marine",
    )
    column_filters = ("dataset_id", "group", "habcode", "name")


class EtcDicMethodModelView(ProtectedModelView):
    form_columns = ("dataset_id", "method", "details", "order")
    column_list = ("dataset_id", "method", "details", "order")
    column_filters = ("dataset_id", "method")


class EtcDicPopulationUnitModelView(ProtectedModelView):
    form_columns = ("dataset_id", "code", "details", "population_units", "order")
    column_list = ("dataset_id", "code", "details", "population_units", "order")
    column_filters = ("dataset_id", "code")


class EtcDicSpeciesTypeModelView(ProtectedModelView):
    form_columns = (
        "dataset_id",
        "SpeciesTypeID",
        "SpeciesType",
        "Assesment",
        "Note",
        "abbrev",
    )
    column_list = (
        "dataset_id",
        "SpeciesTypeID",
        "SpeciesType",
        "Assesment",
        "Note",
        "abbrev",
    )
    column_filters = ("dataset_id", "SpeciesTypeID", "SpeciesType", "Assesment")


class EtcDicTrendModelView(ProtectedModelView):
    form_columns = ("id", "dataset_id", "trend", "details")
    column_list = ("id", "dataset_id", "trend", "details")
    column_filters = ("id", "dataset_id", "trend")


class EtcQaErrorsHabitattypeManualCheckedModelView(ProtectedModelView):
    form_columns = (
        "dataset_id",
        "country",
        "eu_country_code",
        "region",
        "habitatcode",
        "filename",
        "suspect_value",
        "error_code",
        "error_description",
        "field",
        "text",
    )
    column_list = (
        "dataset_id",
        "country",
        "eu_country_code",
        "region",
        "habitatcode",
        "filename",
        "suspect_value",
        "error_code",
        "error_description",
        "field",
        "text",
    )
    column_filters = (
        "dataset_id",
        "country",
        "eu_country_code",
        "region",
        "habitatcode",
        "field",
    )


class EtcQaErrorsSpeciesManualCheckedModelView(ProtectedModelView):
    form_columns = (
        "dataset_id",
        "country",
        "eu_country_code",
        "region",
        "assesment_speciesname",
        "filename",
        "suspect_value",
        "error_code",
        "error_description",
        "field",
        "text",
    )
    column_list = (
        "dataset_id",
        "country",
        "eu_country_code",
        "region",
        "assesment_speciesname",
        "filename",
        "suspect_value",
        "error_code",
        "error_description",
        "field",
        "text",
    )
    column_filters = (
        "dataset_id",
        "country",
        "eu_country_code",
        "region",
        "assesment_speciesname",
        "field",
    )


class ConfigModelView(ProtectedModelView):
    form_columns = ("id", "start_date", "end_date", "admin_email", "default_dataset_id")
    column_list = ("id", "start_date", "end_date", "admin_email", "default_dataset_id")
    column_filters = ("id", "default_dataset_id")


def admin_register(app):
    admin = Admin(
        app,
        name="Article 17",
        template_mode="bootstrap3",
        index_view=CustomAdminIndexView(),
    )
    admin.add_view(DatasetModelView(Dataset, db.session))
    admin.add_view(DicCountryCodeModelView(DicCountryCode, db.session))
    admin.add_view(
        EtcDataHcoveragePressureModelView(
            EtcDataHcoveragePressure, db.session, category="EtcData"
        )
    )
    admin.add_view(
        EtcDataHcoverageThreatModelView(
            EtcDataHcoverageThreat, db.session, category="EtcData"
        )
    )
    admin.add_view(
        EtcDataSpopulationPressureModelView(
            EtcDataSpopulationPressure, db.session, category="EtcData"
        )
    )
    admin.add_view(
        EtcDataSpopulationThreatModelView(
            EtcDataSpopulationThreat, db.session, category="EtcData"
        )
    )
    admin.add_view(
        EtcDicBiogeoregModelView(EtcDicBiogeoreg, db.session, category="EtcDic")
    )
    admin.add_view(
        EtcDicConclusionModelView(EtcDicConclusion, db.session, category="EtcDic")
    )
    admin.add_view(
        EtcDicDecisionModelView(EtcDicDecision, db.session, category="EtcDic")
    )
    admin.add_view(
        EtcDicHdHabitatModelView(EtcDicHdHabitat, db.session, category="EtcDic")
    )
    admin.add_view(EtcDicMethodModelView(EtcDicMethod, db.session, category="EtcDic"))
    admin.add_view(
        EtcDicPopulationUnitModelView(
            EtcDicPopulationUnit, db.session, category="EtcDic"
        )
    )
    admin.add_view(
        EtcDicSpeciesTypeModelView(EtcDicSpeciesType, db.session, category="EtcDic")
    )
    admin.add_view(EtcDicTrendModelView(EtcDicTrend, db.session, category="EtcDic"))
    admin.add_view(
        EtcQaErrorsHabitattypeManualCheckedModelView(
            EtcQaErrorsHabitattypeManualChecked, db.session, category="EtcQA"
        )
    )
    admin.add_view(
        EtcQaErrorsSpeciesManualCheckedModelView(
            EtcQaErrorsSpeciesManualChecked, db.session, category="EtcQA"
        )
    )
    admin.add_view(ConfigModelView(Config, db.session))
