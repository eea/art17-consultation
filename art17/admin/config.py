from .base import ProtectedModelView


class ConfigModelView(ProtectedModelView):
    column_list = ("id", "start_date", "end_date", "admin_email", "default_dataset_id")
    column_filters = ("id", "default_dataset_id")
