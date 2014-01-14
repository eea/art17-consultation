from art17.models import (
    EtcDataSpeciesRegion,
    EtcDicBiogeoreg,
    EtcDataHabitattypeRegion,
    EtcDicHdHabitat,
    db,
)


class SpeciesMixin(object):

    model_cls = EtcDataSpeciesRegion
    subject_name = 'species'

    def objects_by_group(self, period, group):
        return self.model_cls.query.filter_by(group=group, dataset_id=period)

    def subjects_by_group(self, period, group):
        qs = db.session.query(self.model_cls.speciesname).\
            filter_by(group=group, dataset_id=period).distinct()
        return [row[0] for row in qs]

    @classmethod
    def get_groups(cls, period):
        group_field = EtcDataSpeciesRegion.group
        dataset_id_field = EtcDataSpeciesRegion.dataset_id
        groups = (
            EtcDataSpeciesRegion.query
            .filter(group_field != None, dataset_id_field == period)
            .with_entities(group_field, group_field)
            .distinct()
            .order_by(group_field)
            .all()
        )
        return [('', '-')] + groups

    @classmethod
    def get_subjects(cls, period, group):
        blank_option = [('', '-')]
        if group is None:
            return blank_option
        group_field = EtcDataSpeciesRegion.group
        dataset_id_field = EtcDataSpeciesRegion.dataset_id
        assesment_field = EtcDataSpeciesRegion.assesment_speciesname
        subjects = (
            EtcDataSpeciesRegion.query
            .filter(assesment_field != None)
            .filter(group_field == group)
            .filter(dataset_id_field == period)
            .with_entities(assesment_field, assesment_field)
            .distinct()
            .order_by(assesment_field)
            .all()
        )
        return blank_option + subjects

    @classmethod
    def get_regions(cls, period, species):
        blank_option = [('', 'All bioregions')]

        assesment_field = EtcDataSpeciesRegion.assesment_speciesname
        reg_field = EtcDataSpeciesRegion.region
        reg_code_field = EtcDicBiogeoreg.reg_code
        reg_name_field = EtcDicBiogeoreg.reg_name
        dataset_id_field = EtcDataSpeciesRegion.dataset_id

        regions = (
            EtcDicBiogeoreg.query
            .join(EtcDataSpeciesRegion, reg_code_field == reg_field)
            .filter(assesment_field == species)
            .filter(dataset_id_field == period)
            .with_entities(reg_field, reg_name_field)
            .distinct()
            .order_by(reg_field)
            .all()
        )
        return blank_option + regions


class HabitatMixin(object):

    model_cls = EtcDataHabitattypeRegion
    subject_name = 'habitat'

    @classmethod
    def get_groups(cls, period):
        group_field = EtcDicHdHabitat.group
        dataset_id_field = EtcDicHdHabitat.dataset_id
        groups = (
            EtcDicHdHabitat.query
            .filter(group_field != None, dataset_id_field == period)
            .with_entities(group_field, group_field)
            .distinct()
           .order_by(group_field)
           .all()
        )
        return [('', '-')] + groups

    @classmethod
    def get_subjects(cls, period, group):
        blank_option = [('', '-')]
        if group is None:
            return blank_option
        group_field = EtcDicHdHabitat.group
        dataset_id_field = EtcDicHdHabitat.dataset_id
        value_field = EtcDicHdHabitat.habcode
        assesment_field = EtcDicHdHabitat.name
        subjects = (
            EtcDicHdHabitat.query
            .filter(assesment_field != None)
            .filter(group_field == group)
            .filter(dataset_id_field == period)
            .with_entities(value_field, assesment_field)
            .distinct()
            .order_by(assesment_field)
            .all()
        )
        return blank_option + subjects

    @classmethod
    def get_regions(cls, period, subject):
        blank_option = [('', 'All bioregions')]

        assesment_field = EtcDataHabitattypeRegion.code
        reg_field = EtcDataHabitattypeRegion.region
        reg_code_field = EtcDicBiogeoreg.reg_code
        reg_name_field = EtcDicBiogeoreg.reg_name
        dataset_id_field = EtcDataHabitattypeRegion.dataset_id

        regions = (
            EtcDicBiogeoreg.query
            .join(EtcDataHabitattypeRegion, reg_code_field == reg_field)
            .filter(assesment_field == subject)
            .filter(dataset_id_field == period)
            .with_entities(reg_field, reg_name_field)
            .distinct()
            .order_by(reg_field)
            .all()
        )
        return blank_option + regions
