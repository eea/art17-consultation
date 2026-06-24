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
        "is_readonly",
    )
    column_list = ("id", "name", "schema", "latest", "is_readonly")
    column_filters = ["id", "schema", "is_readonly"]
