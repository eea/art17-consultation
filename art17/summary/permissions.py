from art17.auth import current_user
from art17.common import admin_perm, etc_perm, sta_perm, nat_perm
from art17.summary import summary


@summary.app_template_global('can_delete')
def can_delete(record):
    if current_user.is_anonymous():
        return False

    if record.dataset.is_readonly:
        return False

    return admin_perm.can() or record.user_id == current_user.id


@summary.app_template_global('can_update_decision')
def can_update_decision():
    return etc_perm.can() or admin_perm.can()


@summary.app_template_global('can_view')
def can_view(record, countries):
    return (admin_perm.can() or etc_perm.can() or
            record.eu_country_code not in countries)


@summary.app_template_global('can_edit')
def can_edit(record):
    if current_user.is_anonymous():
        return False

    if record.deleted:
        return False

    if record.dataset.is_readonly:
        return False

    if record.user_id == current_user.id:
        return True

    return etc_perm.can() or admin_perm.can()


@summary.app_template_global('can_view_decision')
def can_view_decision(record):
    return etc_perm.can() or admin_perm.can()


@summary.app_template_global('can_add_conclusion')
def can_add_conclusion(dataset, zone, subject, region=None):
    """
    Zone: one of 'species', 'habitat'
    """
    from art17.summary.views import SpeciesSummary, HabitatSummary
    zone_cls_mapping = {'species': SpeciesSummary, 'habitat': HabitatSummary}
    if not dataset:
        return False
    record_exists = False
    if region and not current_user.is_anonymous():
        record_exists = zone_cls_mapping[zone].get_manual_record(
            dataset.id, subject, region, current_user.id)
    return (
        not dataset.is_readonly and
        (sta_perm.can() or admin_perm.can() or nat_perm.can()
         or etc_perm.can()) and not record_exists
    )


@summary.app_template_global('can_select_MS')
def can_select_MS():
    return sta_perm.can()


def can_touch(assessment):
    if current_user.is_anonymous():
        return False
    if not assessment:
        return admin_perm.can() or sta_perm.can() or nat_perm.can() \
            or etc_perm.can()
    else:
        return admin_perm.can() or etc_perm.can() or (
            assessment.user == current_user)


def must_edit_ref(assessment):
    if not current_user.is_authenticated() or not assessment:
        return False
    if assessment.user_id == current_user.id:
        return False

    return etc_perm.can() or admin_perm.can()
