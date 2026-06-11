from .base import AnonymizationMixin, ProtectedModelView


class WikiTrailModelView(ProtectedModelView):
    can_export = True
    export_types = ["csv", "xlsx"]
    column_list = (
        "id",
        "region_code",
        "assessment_speciesname",
        "habitatcode",
        "dataset_id",
    )
    column_filters = (
        "dataset_id",
        "region_code",
        "assessment_speciesname",
        "habitatcode",
    )


class WikiTrailChangeModelView(AnonymizationMixin, ProtectedModelView):
    can_export = True
    export_types = ["csv", "xlsx"]
    column_list = ("id", "wiki_id", "body", "editor", "changed", "active", "dataset_id")
    column_filters = ("wiki_id", "editor", "changed", "active", "dataset_id")
    anonymized_fields = ["editor"]


class WikiTrailChangeCombinedWithWikiModelView(AnonymizationMixin, ProtectedModelView):
    can_export = True
    export_types = ["csv", "xlsx"]
    column_list = (
        "id",
        "wiki.id",
        "wiki.region_code",
        "wiki.assessment_speciesname",
        "wiki.habitatcode",
        "wiki_id",
        "body",
        "editor",
        "changed",
        "active",
        "dataset_id",
    )
    column_filters = ("wiki_id", "editor", "changed", "active", "dataset_id")
    anonymized_fields = ["editor"]


class WikiTrailCommentModelView(AnonymizationMixin, ProtectedModelView):
    can_export = True
    export_types = ["csv", "xlsx"]
    column_list = (
        "id",
        "wiki_id",
        "comment",
        "author",
        "deleted",
        "posted",
        "dataset_id",
    )
    column_filters = ("wiki_id", "comment", "author", "deleted", "posted", "dataset_id")
    anonymized_fields = ["author"]
