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
    Comment,
    HabitatComment,
    LuSpeciesManual2007, LuHabitatManual2007)


class MixinsCommon(object):

    @classmethod
    def get_manual_record(cls, period, subject, region, user, MS=None):
        filters = {'dataset_id': period, 'subject': subject, 'region': region,
                   'user_id': user, 'MS': MS}
        if not MS:
            del filters['MS']
        return cls.model_manual_cls.query.filter_by(**filters).first()

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

    @classmethod
    def _get_regions_query(cls, period, short=False):
        dataset_id_field = cls.model_cls.dataset_id
        reg_field = cls.model_cls.region
        reg_code_field = EtcDicBiogeoreg.reg_code
        if not short:
            reg_name_field = EtcDicBiogeoreg.reg_name
        else:
            reg_name_field = EtcDicBiogeoreg.reg_code

        regions = (
            EtcDicBiogeoreg.query
            .join(cls.model_cls, reg_code_field == reg_field)
            .filter(dataset_id_field == period)
            .with_entities(reg_field, reg_name_field)
            .distinct()
            .order_by(reg_field)
        )
        return regions

    @classmethod
    def get_regions_by_country(cls, period, country, short=False):
        blank_option = [('', 'All bioregions')]
        country_field = cls.model_cls.eu_country_code
        regions = (
            cls._get_regions_query(period, short)
            .filter(country_field == country).all()
        )
        return blank_option + regions

    @classmethod
    def get_group_for_subject(cls, subject):
        record = (
            cls.model_cls.query
            .filter_by(subject=subject).first()
        )
        return record.group if record else ''

    @classmethod
    def get_MS(cls, subject, region, period):
        ms_qs = cls.model_cls.query.filter_by(subject=subject,
                                              dataset_id=period)
        if region:
            ms_qs = ms_qs.filter_by(region=region)
        ms_qs = ms_qs.with_entities(cls.model_cls.eu_country_code,
                                    cls.model_cls.eu_country_code)
        if not region:
            ms_qs = ms_qs.distinct(cls.model_cls.eu_country_code)

        return ms_qs.order_by(cls.model_cls.presence,
                              cls.model_cls.eu_country_code).all()


class SpeciesMixin(MixinsCommon):

    model_cls = EtcDataSpeciesRegion
    model_auto_cls = EtcDataSpeciesAutomaticAssessment
    model_manual_cls = SpeciesManualAssessment
    model_comment_cls = Comment
    prev_lu_cls = LuSpeciesManual2007
    subject_name = 'species'
    summary_endpoint = 'summary.species-summary'

    def objects_by_group(self, period, group):
        return self.model_cls.query.filter_by(group=group, dataset_id=period)

    def subjects_by_group(self, period, group):
        qs = (
            db.session.query(self.model_cls.speciesname)
            .filter_by(group=group, dataset_id=period).distinct()
            .order_by(self.model_cls.speciesname)
        )
        return [(row[0], row[0]) for row in qs if row[0]]

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
        assesment_field = cls.model_cls.subject
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
        assesment_field = cls.model_cls.subject
        regions = (
            cls._get_regions_query(period, short)
            .filter(assesment_field == species).all()
        )
        return blank_option + regions


class HabitatMixin(MixinsCommon):

    model_cls = EtcDataHabitattypeRegion
    model_auto_cls = EtcDataHabitattypeAutomaticAssessment
    model_manual_cls = HabitattypesManualAssessment
    model_comment_cls = HabitatComment
    prev_lu_cls = LuHabitatManual2007
    subject_name = 'habitat'
    summary_endpoint = 'summary.habitat-summary'

    def subjects_by_group(self, period, group):
        qs = (
            db.session.query(EtcDicHdHabitat)
            .with_entities(EtcDicHdHabitat.habcode, EtcDicHdHabitat.shortname)
            .filter_by(group=group, dataset_id=period).distinct()
        )
        return [(row[0], ' - '.join(row)) for row in qs if row[0]]

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
        groups = [(a.capitalize(), b.capitalize()) for (a, b) in groups]
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

    @classmethod
    def get_subject_details(cls, subject):
        return EtcDicHdHabitat.query.filter_by(habcode=subject).first()
