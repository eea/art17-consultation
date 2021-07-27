from art17.auth.security import current_user
from art17.common import (
    admin_perm,
    etc_perm,
    sta_perm,
    nat_perm,
    sta_cannot_change,
    consultation_ended,
)
from instance.settings import EU_ASSESSMENT_MODE
from art17.summary import summary


@summary.app_template_global("can_delete")
def can_delete(record):
    if EU_ASSESSMENT_MODE:
        return True
    if current_user.is_anonymous:
        return False

    if record.dataset.is_readonly:
        return False

    if record.user_id == current_user.id:
        return not sta_cannot_change()


@summary.app_template_global("can_update_decision")
def can_update_decision(conclusion):
    if conclusion.deleted:
        return False
    return etc_perm.can() or admin_perm.can() or EU_ASSESSMENT_MODE


@summary.app_template_global("can_view")
def can_view(record, countries):
    return admin_perm.can() or etc_perm.can() or record.eu_country_code not in countries


@summary.app_template_global("can_edit")
def can_edit(record):
    if EU_ASSESSMENT_MODE:
        return True
    if current_user.is_anonymous:
        return False

    if record.deleted:
        return False

    if record.dataset.is_readonly:
        return False

    if record.user_id == current_user.id:
        if sta_cannot_change():
            return False
        return True

    return etc_perm.can() or admin_perm.can()


@summary.app_template_global("can_view_decision")
def can_view_decision():
    return etc_perm.can() or admin_perm.can() or EU_ASSESSMENT_MODE


@summary.app_template_global("can_add_conclusion")
def can_add_conclusion(dataset, zone, subject, region=None):
    """
    Zone: one of 'species', 'habitat'
    """
    from art17.summary.views import SpeciesSummary, HabitatSummary

    zone_cls_mapping = {"species": SpeciesSummary, "habitat": HabitatSummary}

    can_add = False
    warning_message = ""

    if not dataset:
        warning_message = (
            "Please select a valid dataset in order to add " + "a conclusion."
        )
    elif dataset.is_readonly:
        warning_message = (
            "The current dataset is readonly, so you cannot " + "add a conclusion."
        )
    elif not region:
        warning_message = "Please select a Bioregion in order to add a " + "conclusion."
    elif not (
        admin_perm.can()
        or sta_perm.can()
        or nat_perm.can()
        or etc_perm.can()
        or EU_ASSESSMENT_MODE
    ):
        warning_message = "You do not have permission to add conclusions."
    elif sta_cannot_change():
        warning_message = (
            "The consultation period has ended; you cannont "
            + "add conclusions anymore."
        )
    else:
        if not EU_ASSESSMENT_MODE:
            record_exists = zone_cls_mapping[zone].get_manual_record(
                dataset.id, subject, region, current_user.id
            )
            if record_exists:
                warning_message = (
                    "You have already added a conclusion for "
                    + "the selected subject and region."
                )
            else:
                can_add = True
        else:
            can_add = True
    return can_add, warning_message


@summary.app_template_global("can_select_MS")
def can_select_MS():
    return admin_perm.can() or sta_perm.can() or nat_perm.can() or etc_perm.can()


def can_touch(assessment):
    if current_user.is_anonymous and not EU_ASSESSMENT_MODE:
        return False
    if not assessment:
        return (
            EU_ASSESSMENT_MODE
            or admin_perm.can()
            or nat_perm.can()
            or etc_perm.can()
            or (sta_perm.can() and not consultation_ended())
        )
    return (
        EU_ASSESSMENT_MODE
        or admin_perm.can()
        or etc_perm.can()
        or (assessment.user == current_user and not sta_cannot_change())
    )


def must_edit_ref(assessment):
    if not current_user.is_authenticated or not assessment:
        return False
    if assessment.user_id == current_user.id:
        return False

    return etc_perm.can() or admin_perm.can()
