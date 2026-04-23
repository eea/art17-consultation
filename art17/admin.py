import os

from flask import abort, flash, current_app, request, redirect, url_for
from flask_admin import Admin, AdminIndexView, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from art17.common import admin_perm
from art17.models import (
    Config,
    Dataset,
    DicCountryCode,
    EtcDataSpeciesRegion,
    EtcDataHabitattypeRegion,
    EtcDataSpeciesAutomaticAssessment,
    EtcDataHabitattypeAutomaticAssessment,
    SpeciesManualAssessment,
    HabitattypesManualAssessment,
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
from werkzeug.utils import secure_filename


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


class EtcDataSpeciesRegionModelView(ProtectedModelView):
    can_export = True
    column_list = (
        "dataset_id",
        "group",
        "country",
        "region",
        "speciescode",
        "assessment_speciesname",
        "use_for_statistics",
    )
    column_filters = ["dataset_id", "group","country", "region", "speciescode", "assessment_speciesname", "use_for_statistics"]


class EtcDataHabitattypeRegionModelView(ProtectedModelView):
    can_export = True
    column_list = ("dataset_id", "country", "group", "region", "habitatcode", "use_for_statistics",         "habitattype_type_asses",)
    column_filters = ["dataset_id", "country", "group", "region", "habitatcode", "use_for_statistics", "habitattype_type_asses"]


class EtcDataSpeciesAutomaticAssessmentModelView(ProtectedModelView):
    can_export = True
    column_list = (
        "dataset_id",
        "assessment_method",
        "assessment_speciescode",
        "assessment_speciesname",
        "region",
        "country",
    )
    column_filters = [
        "dataset_id",
        "assessment_method",
        "assessment_speciescode",
        "assessment_speciesname",
        "region",
        "country",
    ]


class EtcDataHabitattypeAutomaticAssessmentModelView(ProtectedModelView):
    can_export = True
    column_list = (
        "dataset_id",
        "assessment_method",
        "habitatcode",
        "region",
        "country",
    )
    column_filters = [
        "dataset_id",
        "assessment_method",
        "habitatcode",
        "region",
        "country",
    ]


class SpeciesManualAssessmentModelView(ProtectedModelView):
    can_export = True

    column_filters = [
        "MS",
        "region",
        "assessment_speciesname",
        "user_id",
        "last_update",
        "deleted",
        "user_decision_id",
        "dataset_id",
        "decision",
    ]

    column_list = (
        "MS",
        "region",
        "assessment_speciesname",
        "range_surface_area",
        "range_trend",
        "range_yearly_magnitude",
        "complementary_favourable_range",
        "complementary_favourable_range_q",
        "derived_perc_range_FRR",
        "derived_population_size_trend_magnitude",
        "derived_perc_population_FRP",
        "population_size",
        "population_size_unit",
        "population_minimum_size",
        "population_maximum_size",
        "population_best_value",
        "population_unit",
        "population_trend",
        "population_yearly_magnitude",
        "complementary_favourable_population",
        "complementary_favourable_population_q",
        "complementary_favourable_population_unit",
        "habitat_surface_area",
        "habitat_trend",
        "complementary_suitable_habitat",
        "method_range",
        "conclusion_range",
        "method_population",
        "conclusion_population",
        "method_habitat",
        "conclusion_habitat",
        "method_future",
        "future_range",
        "future_population",
        "future_habitat",
        "conclusion_future",
        "method_assessment",
        "conclusion_assessment",
        "conclusion_assessment_trend",
        "conclusion_assessment_prev",
        "conclusion_assessment_trend_prev",
        "conclusion_assessment_change",
        "conclusion_assessment_trend_change",
        "method_target1",
        "conclusion_target1",
        "backcasted_2007",
        "user_id",
        "last_update",
        "deleted",
        "decision",
        "user_decision_id",
        "last_update_decision",
        "dataset_id",
        "user",
        "user_decision",
        "dataset",
    )


class HabitattypesManualAssessmentModelView(ProtectedModelView):
    can_export = True
    column_filters = [
        "MS",
        "region",
        "habitatcode",
        "user_id",
        "last_update",
        "deleted",
        "decision",
        "user_decision_id",
        "last_update_decision",
        "dataset_id",
    ]
    column_list = (
        "MS",
        "region",
        "habitatcode",
        "range_surface_area",
        "range_trend",
        "range_yearly_magnitude",
        "complementary_favourable_range",
        "complementary_favourable_range_q",
        "derived_perc_range_FRR",
        "coverage_surface_area",
        "coverage_surface_area_min",
        "coverage_surface_area_max",
        "coverage_trend",
        "coverage_yearly_magnitude",
        "complementary_favourable_area",
        "complementary_favourable_area_q",
        "derived_perc_area_FRA",
        "method_range",
        "conclusion_range",
        "method_area",
        "conclusion_area",
        "hab_condition_good",
        "hab_condition_good_min",
        "hab_condition_good_max",
        "hab_condition_good_best",
        "hab_condition_notgood",
        "hab_condition_notgood_min",
        "hab_condition_notgood_max",
        "hab_condition_notgood_best",
        "hab_condition_unknown",
        "hab_condition_unknown_min",
        "hab_condition_unknown_max",
        "hab_condition_unknown_best",
        "hab_condition_trend",
        "method_structure",
        "conclusion_structure",
        "method_future",
        "future_range",
        "future_area",
        "future_structure",
        "conclusion_future",
        "method_assessment",
        "conclusion_assessment",
        "conclusion_assessment_trend",
        "conclusion_assessment_prev",
        "conclusion_assessment_trend_prev",
        "conclusion_assessment_change",
        "conclusion_assessment_trend_change",
        "method_target1",
        "conclusion_target1",
        "backcasted_2007",
        "user_id",
        "last_update",
        "deleted",
        "decision",
        "user_decision_id",
        "last_update_decision",
        "dataset_id",
        "user",
        "user_decision",
        "dataset",
    )


class DatasetModelView(ProtectedModelView):
    can_export = True
    form_columns = (
        # "id",
        "name",
        "schema",
        "species_map_url",
        "sensitive_species_map_url",
        "habitat_map_url",
        "latest",
    )
    column_list = (
        "id",
        "name",
        "schema",
        "species_map_url",
        "sensitive_species_map_url",
        "habitat_map_url",
        "latest",
    )
    column_filters = ["id", "schema"]


class DicCountryCodeModelView(ProtectedModelView):
    can_export = True
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
        "assessment_speciesname",
        "pressure",
    )
    column_list = (
        "dataset_id",
        "eu_country_code",
        "region",
        "n2000_species_code",
        "assessment_speciesname",
        "pressure",
    )
    column_filters = ["dataset_id", "eu_country_code", "region", "n2000_species_code"]


class EtcDataSpopulationThreatModelView(ProtectedModelView):
    form_columns = (
        "dataset_id",
        "eu_country_code",
        "region",
        "n2000_species_code",
        "assessment_speciesname",
        "threat",
    )
    column_list = (
        "dataset_id",
        "eu_country_code",
        "region",
        "n2000_species_code",
        "assessment_speciesname",
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
        "SpeciesType",
        "Assessment",
        "Note",
        "abbrev",
    )
    column_list = (
        "dataset_id",
        "SpeciesTypeID",
        "SpeciesType",
        "Assessment",
        "Note",
        "abbrev",
    )
    column_filters = ("dataset_id", "SpeciesTypeID", "SpeciesType", "Assessment")

    def create_model(self, form):
        try:
            model = self.model()
            form.populate_obj(model)

            # Auto-generate SpeciesTypeID as the next available ID for this dataset
            max_id = (
                db.session.query(db.func.max(EtcDicSpeciesType.SpeciesTypeID))
                .filter(EtcDicSpeciesType.dataset_id == model.dataset_id)
                .scalar()
            )
            model.SpeciesTypeID = (max_id or 0) + 1

            self.session.add(model)
            self._on_model_change(form, model, True)
            self.session.commit()
            return model
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(f"Failed to create record. {str(ex)}", "error")
            self.session.rollback()
            return False


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
        "assessment_speciesname",
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
        "assessment_speciesname",
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
        "assessment_speciesname",
        "field",
    )


class ConfigModelView(ProtectedModelView):
    column_list = ("id", "start_date", "end_date", "admin_email", "default_dataset_id")
    column_filters = ("id", "default_dataset_id")


class FileUploadView(BaseView):

    @expose("/", methods=("GET", "POST"))
    def index(self):
        if not admin_perm.can():
            return abort(404)

        if request.method == "POST" and "file" in request.files:
            f = request.files["file"]
            if f.filename == "":
                flash("No file selected", "error")
                return redirect(url_for(".index"))

            filename = secure_filename(f.filename)
            upload_dir = current_app.config.get("UPLOAD_FOLDER", "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            filepath = os.path.join(upload_dir, filename)
            f.save(filepath)
            flash(f"File uploaded to {filepath}", "success")
            return redirect(url_for(".index"))

        return self.render("admin/upload.html")


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
        EtcDataSpeciesRegionModelView(
            EtcDataSpeciesRegion, db.session, category="RegionsData"
        )
    )
    admin.add_view(
        EtcDataHabitattypeRegionModelView(
            EtcDataHabitattypeRegion, db.session, category="RegionsData"
        )
    )
    admin.add_view(
        EtcDataSpeciesAutomaticAssessmentModelView(
            EtcDataSpeciesAutomaticAssessment, db.session, category="AutomaticData"
        )
    )
    admin.add_view(
        EtcDataHabitattypeAutomaticAssessmentModelView(
            EtcDataHabitattypeAutomaticAssessment, db.session, category="AutomaticData"
        )
    )
    admin.add_view(
        SpeciesManualAssessmentModelView(
            SpeciesManualAssessment, db.session, category="ManualData"
        )
    )
    admin.add_view(
        HabitattypesManualAssessmentModelView(
            HabitattypesManualAssessment, db.session, category="ManualData"
        )
    )

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
    # register non-model upload view
    admin.add_view(
        FileUploadView(name="Upload File", endpoint="file_upload", category="Utilities")
    )
