import os

from flask import abort, current_app, flash, redirect, request, session, url_for
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from werkzeug.utils import secure_filename

from art17.common import admin_perm


class ProtectedModelView(ModelView):

    def is_accessible(self):
        return admin_perm.can()

    def inaccessible_callback(self, name, **kwargs):
        return abort(404)


class AnonymizationMixin(ProtectedModelView):
    anonymized_fields = []
    anonymization_session_key = "admin_export_anonymize"
    list_template = "admin/model/list_with_anonymize_toggle.html"
    anonymization_default = True

    def is_anonymization_enabled(self):
        val = request.args.get("anonymize")
        if val is not None:
            session[self.anonymization_session_key] = val in ("1", "true", "on", "yes")
        return session.get(self.anonymization_session_key, self.anonymization_default)

    @expose("/toggle-anonymization/<state>")
    def toggle_anonymization(self, state):
        session[self.anonymization_session_key] = state == "on"
        return redirect(request.referrer or self.get_url(".index_view"))

    def _reset_export_anonymization(self):
        self._anonymized_aliases = {field: {} for field in self.anonymized_fields}
        self._anonymized_fields_counter = {field: 0 for field in self.anonymized_fields}

    def _anonymized_field_alias(self, field, value):
        if not value:
            return ""

        # stable key per real value
        key = str(value)

        if key not in self._anonymized_aliases[field]:
            self._anonymized_fields_counter[field] += 1
            self._anonymized_aliases[field][
                key
            ] = f"{field}{self._anonymized_fields_counter[field]}"

        return self._anonymized_aliases[field][key]

    def _export_data(self):
        # reset map for each export file
        self._reset_export_anonymization()
        return super()._export_data()

    def get_export_value(self, model, name):
        if name in self.anonymized_fields and self.is_anonymization_enabled():
            return self._anonymized_field_alias(name, getattr(model, name, None))
        return super().get_export_value(model, name)


class FileUploadView(BaseView):

    @expose("/", methods=("GET", "POST"))
    def index(self):
        if not admin_perm.can():
            return abort(404)

        if request.method == "POST" and "file" in request.files:
            f = request.files["file"]
            if f.filename == "":
                flash("No file selected", "error")
                return redirect(url_for(".index"))

            filename = secure_filename(f.filename)
            upload_dir = current_app.config.get("UPLOAD_FOLDER", "uploads")
            os.makedirs(upload_dir, exist_ok=True)
            filepath = os.path.join(upload_dir, filename)
            f.save(filepath)
            flash(f"File uploaded to {filepath}", "success")
            return redirect(url_for(".index"))

        return self.render("admin/upload.html")
