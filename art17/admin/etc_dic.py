from flask import flash

from art17.models import EtcDicSpeciesType, db

from .base import ProtectedModelView


class DicCountryCodeModelView(ProtectedModelView):
    can_export = True
    form_columns = ("dataset_id", "code", "codeEU", "name")
    column_list = ("dataset_id", "code", "codeEU", "name")
    column_filters = ["dataset_id", "code", "codeEU", "name"]


class DicEunisCodeModelView(ProtectedModelView):
    form_columns = ("code", "level", "label", "description")
    column_list = ("code", "level", "label", "description")
    column_filters = ["code", "level"]


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
