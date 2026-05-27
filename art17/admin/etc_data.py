from .base import ProtectedModelView

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

