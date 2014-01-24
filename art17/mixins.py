from art17.models import (
    EtcDataSpeciesRegion,
    EtcDicBiogeoreg,
    EtcDataHabitattypeRegion,
    EtcDicHdHabitat,
    db,
    EtcDataSpeciesAutomaticAssessment,
    HabitattypesManualAssessment,
    EtcDataHabitattypeAutomaticAssessment,
    SpeciesManualAssessment,
    DicCountryCode,
)


class SpeciesMixin(object):

    model_cls = EtcDataSpeciesRegion
    model_auto_cls = EtcDataSpeciesAutomaticAssessment
    model_manual_cls = SpeciesManualAssessment
    subject_name = 'species'
    subject_field = 'assesment_speciesname'

    def objects_by_group(self, period, group):
        return self.model_cls.query.filter_by(group=group, dataset_id=period)

    def subjects_by_group(self, period, group):
        qs = db.session.query(self.model_cls.speciesname).\
            filter_by(group=group, dataset_id=period).distinct()
        return [row[0] for row in qs]

    def flatten_form(self, form, subject):
        data = dict(form.data)
        for k, v in data.iteritems():
            if hasattr(subject, k):
                setattr(subject, k, v)
        return subject

    def parse_object(self, subject, form):
        data = {}
        for field in form:
            name = field.name
            if hasattr(subject, name):
                data[name] = getattr(subject, name)
        return data

    @classmethod
    def get_groups(cls, period):
        group_field = cls.model_cls.group
        dataset_id_field = cls.model_cls.dataset_id
        groups = (
            cls.model_cls.query
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
        group_field = cls.model_cls.group
        dataset_id_field = cls.model_cls.dataset_id
        assesment_field = cls.model_cls.assesment_speciesname
        subjects = (
            cls.model_cls.query
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
    def get_regions(cls, period, species, short=False):
        blank_option = [('', 'All bioregions')]

        assesment_field = cls.model_cls.assesment_speciesname
        reg_field = cls.model_cls.region
        reg_code_field = EtcDicBiogeoreg.reg_code
        if not short:
            reg_name_field = EtcDicBiogeoreg.reg_name
        else:
            reg_name_field = EtcDicBiogeoreg.reg_code
        dataset_id_field = cls.model_cls.dataset_id

        regions = (
            EtcDicBiogeoreg.query
            .join(cls.model_cls, reg_code_field == reg_field)
            .filter(assesment_field == species, dataset_id_field == period)
            .with_entities(reg_field, reg_name_field)
            .distinct()
            .order_by(reg_field)
            .all()
        )
        return blank_option + regions

    @classmethod
    def get_countries(cls, period):
        blank_option = [('', 'All MS')]
        countries = (
            DicCountryCode.query
            .with_entities(DicCountryCode.codeEU, DicCountryCode.name)
            .filter(DicCountryCode.dataset_id == period)
            .all()
        )
        return blank_option + countries


class HabitatMixin(object):

    model_cls = EtcDataHabitattypeRegion
    model_auto_cls = EtcDataHabitattypeAutomaticAssessment
    model_manual_cls = HabitattypesManualAssessment
    subject_name = 'habitat'
    subject_field = 'code'

    def subjects_by_group(self, period, group):
        qs = db.session.query(self.model_cls.habitatcode).\
            filter_by(group=group, dataset_id=period).distinct()
        return [row[0] for row in qs]

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
        code_field = EtcDicHdHabitat.habcode
        name_field = code_field.concat(' ' + EtcDicHdHabitat.name)
        subjects = (
            EtcDicHdHabitat.query
            .filter(name_field != None, group_field == group,
                    dataset_id_field == period)
            .with_entities(code_field, name_field)
            .distinct()
            .order_by(name_field)
            .all()
        )
        return blank_option + subjects

    @classmethod
    def get_regions(cls, period, subject, short=False):
        blank_option = [('', 'All bioregions')]

        assesment_field = cls.model_cls.code
        reg_field = cls.model_cls.region
        reg_code_field = EtcDicBiogeoreg.reg_code
        reg_name_field = EtcDicBiogeoreg.reg_name
        dataset_id_field = cls.model_cls.dataset_id
        regions = (
            EtcDicBiogeoreg.query
            .join(cls.model_cls, reg_code_field == reg_field)
            .filter(assesment_field == subject)
            .filter(dataset_id_field == period)
            .with_entities(reg_field, reg_name_field)
            .distinct()
            .order_by(reg_field)
            .all()
        )
        return blank_option + regions
