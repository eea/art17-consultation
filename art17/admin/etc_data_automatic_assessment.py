from .base import ProtectedModelView


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
