from datetime import datetime, date
from flask import views, request, url_for, abort, jsonify
from werkzeug.datastructures import MultiDict
from werkzeug.utils import redirect
from functools import cmp_to_key
from art17.auth.security import current_user
from art17.common import (
    admin_perm,
    get_default_period,
    etc_perm,
    MixinView,
    DATE_FORMAT,
    consultation_ended,
)

from art17.models import db, Config, EtcDicMethod, EtcDicDecision, RegisteredUser
from art17.summary.permissions import (
    can_delete,
    can_update_decision,
    can_select_MS,
    must_edit_ref,
)
from art17.utils import validate_float
from instance.settings import EU_ASSESSMENT_MODE

CONC_METHODS = {
    # 'conclusion_range': 'method_range',
    # 'conclusion_population': 'method_population',
    # 'conclusion_habitat': 'method_habitat',
    # 'conclusion_future': 'method_future',
    # 'conclusion_assessment': 'method_assessment',
    # 'conclusion_target1': 'method_target1',
    # 'conclusion_area': 'method_area',
    # 'conclusion_structure': 'method_structure',
}

EXCLUDE_FIELDS = (
    "conclusion_future",
    "conclusion_assessment",
    "conclusion_structure",
    "conclusion_range",
    "conclusion_population",
    "conclusion_habitat",
    "conclusion_area",
)

SPLIT_FIELDS = [
    "complementary_favourable_range",
    "complementary_favourable_area",
    "complementary_favourable_population",
    "complementary_suitable_habitat",
    "range_surface_area",
    "coverage_surface_area",
    "population_size",
    "habitat_surface_area",
]

SIZE_FIELD = "population_size"


def split_semicolon(field, value):
    if value:
        if field in SPLIT_FIELDS:
            value = value.split(";")[0]
        if field == SIZE_FIELD:
            value = " ".join(value.split(" ")[:-1])
    return value


def cmp(a, b):
    return (a > b) - (a < b)


class ConclusionView(object):
    def get_default_values(self):
        period = request.args.get("period") or get_default_period()
        subject = request.args.get("subject")
        region = request.args.get("region")
        if consultation_ended() and (etc_perm.can() or admin_perm.can()):
            best = self.model_manual_cls.query.filter_by(
                dataset_id=period,
                subject=subject,
                region=region,
                decision="OK",
            ).first()
            if best:
                return best.__dict__

        best = (
            self.model_auto_cls.query.filter_by(
                dataset_id=period, subject=subject, region=region
            ).join(
                EtcDicMethod,
                self.model_auto_cls.assessment_method == EtcDicMethod.method,
            )
        ).all()
        cmpf = lambda x, y: -1 if x.assessment_method == "00" else cmp(x.order, y.order)
        best.sort(key=cmp_to_key(cmpf))
        values = {}
        # for f in all_fields(self.manual_form_cls()):
        #     attr = f.name
        #     for ass in filter(lambda a: getattr(a, attr, None), best):
        #         if attr not in EXCLUDE_FIELDS:
        #             values[attr] = split_semicolon(attr, getattr(ass, attr))
        #         if attr in CONC_METHODS:
        #             method = getattr(ass, 'assessment_method')
        #             values[CONC_METHODS[attr]] = method
        #         break
        # Special case: conclusion_assessment_prev
        prev_lu = self.prev_lu_cls.query.filter_by(
            subject=subject, region=region, dataset_id=period
        ).first()

        if prev_lu:
            if period == "3":
                values["conclusion_assessment_prev"] = prev_lu.conclusion_assessment
            if period == "5":
                values[
                    "conclusion_assessment_prev"
                ] = prev_lu.conclusion_assessment_prev
                values[
                    "conclusion_assessment_trend_prev"
                ] = prev_lu.conclusion_assessment_trend_prev
                values["backcasted_2007"] = prev_lu.backcasted_2007
        return values

    def get_form_cls(self):
        if not can_select_MS():
            return self.manual_form_cls, self.manual_form_ref_cls
        return self.manual_form_sta_cls, self.manual_form_ref_sta_cls

    def clean_complementary_fields(self, data):
        area = data.get("complementary_favourable_area")
        population = data.get("complementary_favourable_population")
        range = data.get("complementary_favourable_range")
        if area and not validate_float(area):
            data["complementary_favourable_area"] = ""

        if population and not validate_float(population):
            data["complementary_favourable_population"] = ""

        if range and not validate_float(range):
            data["complementary_favourable_range"] = ""

        return data

    def get_manual_form(self, data=None, period=None, action=None):
        manual_form_cls, manual_form_ref_cls = self.get_form_cls()
        if action == "edit":
            filters = {
                "region": request.args.get("edit_region"),
                "user_id": request.args.get("edit_user"),
                "subject": request.args.get("subject"),
                "dataset_id": period,
            }
            manual_assessment = self.model_manual_cls.query.filter_by(
                **filters
            ).first_or_404()
        else:
            manual_assessment = None
            data = data or MultiDict(self.get_default_values())
        if data:
            data = self.clean_complementary_fields(data)

        if not must_edit_ref(manual_assessment):
            form = manual_form_cls(formdata=data, obj=manual_assessment)
        else:
            form = manual_form_ref_cls(formdata=data, obj=manual_assessment)
        form.setup_choices(dataset_id=period)
        return form, manual_assessment

    def check_conclusion(self, conclusion):
        start_date = Config.query.first().start_date
        dataset_id = Config.query.first().default_dataset_id
        if conclusion.dataset.id == dataset_id and not conclusion.dataset.is_readonly:
            if not start_date or start_date > date.today():
                return False
        return conclusion.decision in ["OK", "END"]

    def filter_conclusions(self, conclusions):
        if admin_perm.can() or etc_perm.can():
            return conclusions
        conclusions = list(conclusions)
        ok_conclusions = [
            conclusion
            for conclusion in conclusions
            if self.check_conclusion(conclusion)
        ]
        user_or_expert = (
            lambda c: not c.user.has_role("admin")
            and not c.user.has_role("etc")
            and c not in ok_conclusions
            if c.user
            else False
        )
        user_iurmax = lambda c: not c.user.has_role("etc") if c.user else False
        if ok_conclusions:
            return ok_conclusions + list(filter(user_or_expert, conclusions))
        else:
            return filter(user_iurmax, conclusions)


class ConclusionDelete(MixinView, views.View):
    def dispatch_request(self):
        period = request.args.get("period")
        subject = request.args.get("subject")
        region = request.args.get("region")
        delete_region = request.args.get("delete_region")
        delete_user = request.args.get("delete_user")
        delete_ms = request.args.get("delete_ms")
        permanently = request.args.get("perm", 0)
        record = self.mixin.get_manual_record(
            period, subject, delete_region, delete_user, delete_ms
        )
        if not record:
            abort(404)
        if not can_delete(record):
            abort(403)

        if permanently:
            db.session.delete(record)
        else:
            if record.deleted:
                record.deleted = 0
            else:
                record.deleted = 1
            db.session.add(record)
        db.session.commit()

        return redirect(
            url_for(
                self.mixin.summary_endpoint,
                period=period,
                subject=subject,
                region=region,
            )
        )


class UpdateDecision(MixinView, views.View):

    methods = ["GET", "POST"]

    def dispatch_request(self, period, subject, region, user):
        ms = request.args.get("ms")
        self.record = self.mixin.get_manual_record(period, subject, region, user, ms)
        if not self.record:
            abort(404)

        if not can_update_decision(self.record):
            abort(403)

        if not request.form.get("decision"):
            abort(401)

        decision = request.form["decision"]
        result = self.validate(decision, period)
        if result["success"]:
            self.record.decision = decision
            self.record.last_update = (
                self.record.last_update_decision
            ) = datetime.now().strftime(DATE_FORMAT)
            if EU_ASSESSMENT_MODE:
                user = RegisteredUser.query.filter_by(
                    id="test_for_eu_assessment"
                ).first()
            else:
                user = current_user
            self.record.user_decision = user
            db.session.commit()
        return jsonify(result)

    def validate(self, decision, period):
        validation_values = ["OK", "END"]
        valid_decisions = [
            d.decision for d in EtcDicDecision.query.filter_by(dataset_id=period).all()
        ]
        if decision not in valid_decisions:
            return {
                "success": False,
                "error": "'{0}' is not a valid decision.".format(decision),
            }
        elif decision == "OK?":
            return {
                "success": False,
                "error": "You are not allowed to select 'OK?'"
                + "Please select another value.",
            }
        elif decision in validation_values:
            for r in self.get_sister_records(self.record):
                if r.decision in validation_values:
                    return {
                        "success": False,
                        "error": "Another final decision already exists",
                    }

        return {"success": True}

    def get_sister_records(self, record):
        return self.mixin.model_manual_cls.query.filter_by(
            subject=record.subject, region=record.region, dataset_id=record.dataset_id
        ).filter(~(self.mixin.model_manual_cls.user == record.user))
