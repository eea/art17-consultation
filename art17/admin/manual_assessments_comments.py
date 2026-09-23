from art17.admin.base import ProtectedModelView

from flask_admin.contrib.sqla.filters import BaseSQLAFilter
from sqlalchemy import or_


class DeletedFilter(BaseSQLAFilter):
    def apply(self, query, value, alias=None):
        if value == "yes":
            return query.filter(self.column.is_(True))

        if value == "no":
            return query.filter(
                or_(
                    self.column.is_(False),
                    self.column.is_(None),
                )
            )

        return query

    def operation(self):
        return self.name

    def get_options(self, view):
        self.model = view.model
        return [
            ("yes", "Yes"),
            ("no", "No"),
        ]


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
        DeletedFilter("deleted", "Deleted"),
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

    def get_column_filters(self, view):
        filters = super().get_column_filters(view)

        filters.append(DeletedFilter(self.model.deleted, "Deleted"))

        return filters


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
        DeletedFilter("deleted", "Deleted"),
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

    def get_column_filters(self, view):
        filters = super().get_column_filters(view)

        filters.append(DeletedFilter(self.model.deleted, "Deleted"))

        return filters
