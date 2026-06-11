from .base import AnonymizationMixin, ProtectedModelView


class RegisteredUserModelView(AnonymizationMixin, ProtectedModelView):
    can_export = True
    export_types = ["csv", "xlsx"]
    column_list = (
        "id",
        "email",
        "name",
        "institution",
        "abbrev",
        "MS",
        "qualification",
        "account_date",
        "show_assessment",
        "active",
        "confirmed_at",
        "is_ldap",
    )
    form_columns = (
        "email",
        "name",
        "institution",
        "abbrev",
        "MS",
        "qualification",
        "show_assessment",
        "active",
    )


class RoleModelView(ProtectedModelView):
    can_export = True
    export_types = ["csv", "xlsx"]
    column_list = ("id", "name", "description")
    column_filters = ("name", "description")
