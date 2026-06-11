from wtforms import IntegerField

from .base import ProtectedModelView


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
    column_filters = [
        "dataset_id",
        "group",
        "country",
        "region",
        "speciescode",
        "assessment_speciesname",
        "use_for_statistics",
        "presence_new",
    ]
    form_excluded_columns = (
        "dataset",
        "habitat",
        "species_type_details",
        "lu_factsheets",
    )

    def scaffold_form(self):
        form_class = super().scaffold_form()
        form_class.dataset_id = IntegerField("Dataset ID")
        return form_class


class EtcDataHabitattypeRegionModelView(ProtectedModelView):
    can_export = True
    column_list = (
        "dataset_id",
        "country",
        "group",
        "region",
        "habitatcode",
        "use_for_statistics",
        "habitattype_type_asses",
    )
    column_filters = [
        "dataset_id",
        "country",
        "group",
        "region",
        "habitatcode",
        "use_for_statistics",
        "habitattype_type_asses",
    ]

    form_excluded_columns = (
        "dataset",
        "habitat",
        "habitattype_type_details",
        "lu_factsheets",
    )

    def scaffold_form(self):
        form_class = super().scaffold_form()
        form_class.dataset_id = IntegerField("Dataset ID")
        return form_class
