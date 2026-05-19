
from wtforms import IntegerField
from art17.admin.base import ProtectedModelView


class CommentModelView(ProtectedModelView):
    can_export = True
    export_types = ["csv", "xlsx"]
    column_filters = [
        "dataset_id",
        "MS",
        "assessment_speciesname",
        "region",
        "user_id",
        "author_id",
        "post_date",
        "deleted",

    ]
    column_list = [
        "id",
        "dataset_id",
        "MS",
        "assessment_speciesname",
        "region",
        "user_id",
        "comment",
        "author_id",
        "post_date",
        "deleted",
    ]


class HabitatCommentModelView(ProtectedModelView):
    can_export = True
    export_types = ["csv", "xlsx"]
    column_filters = [
        "dataset_id",
        "MS",
        "habitat",
        "region",
        "user_id",
        "comment",
        "author_id",
        "post_date",
        "deleted",
    ]
    column_list = [
        "id",
        "dataset_id",
        "MS",
        "habitat",
        "region",
        "user_id",
        "comment",
        "author_id",
        "post_date",
        "deleted",
    ]
