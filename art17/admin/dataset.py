from .base import ProtectedModelView


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
