# coding: utf-8
import argparse
import json
import ldap
import os
from sqlalchemy import (
    Column, DateTime, Float,
    ForeignKey, Integer, LargeBinary,
    SmallInteger, String, Table, Text, Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import or_, inspect
from flask import current_app as app
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.security import UserMixin, RoleMixin

import sys
from datetime import datetime


DEFAULT_MS = 'EU28'

db = SQLAlchemy()
Base = db.Model
metadata = db.Model.metadata
alembic_ignore_tables = ['species_name', 'species_group', 'habitat_group']


def get_ldap_connection():
    ldap_url = "{}://{}:{}".format(
        app.config['EEA_LDAP_PROTOCOL'],
        app.config['EEA_LDAP_SERVER'],
        app.config['EEA_LDAP_PORT']
    )
    conn = ldap.initialize(ldap_url)
    return conn

class Dataset(Base):
    __tablename__ = 'datasets'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(255), nullable=False)
    schema = Column(String(4))

    @property
    def is_readonly(self):
        return (
            self.schema == '2006' or
            self.schema == '2012' or
            self.schema == '2012bis'
        )


    @property
    def stats(self):
        return {
            'species_content': (
                EtcDataSpeciesRegion.query
                .filter_by(dataset_id=self.id).count()
            ),
            'species_auto': (
                EtcDataSpeciesAutomaticAssessment.query
                .filter_by(dataset_id=self.id).count()
            ),
            'species_manual': (
                SpeciesManualAssessment.query
                .filter_by(dataset_id=self.id).count()
            ),
            'habitat_content': (
                EtcDataHabitattypeRegion.query
                .filter_by(dataset_id=self.id).count()
            ),
            'habitat_auto': (
                EtcDataHabitattypeAutomaticAssessment.query
                .filter_by(dataset_id=self.id).count()
            ),
            'habitat_manual': (
                HabitattypesManualAssessment.query
                .filter_by(dataset_id=self.id).count()
            ),
        }


t_comments_read = Table(
    'comments_read', metadata,
    Column('id_comment', ForeignKey('comments.id'), nullable=False),
    Column('reader_user_id', String(25), ForeignKey('registered_users.user')),
)


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, unique=True)
    region = Column(String(4), nullable=False)
    assesment_speciesname = Column(String(50), nullable=False)
    user_id = Column('user', String(25), nullable=False)
    MS = Column(String(4), nullable=False, default=DEFAULT_MS)
    comment = Column(String)
    author_id = Column('author', String(25), nullable=False)
    post_date = Column(String(16), nullable=False)
    deleted = Column(Integer)
    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
    )

    record = relationship(
        'SpeciesManualAssessment',
        primaryjoin=(
            "and_(SpeciesManualAssessment.assesment_speciesname=="
            "Comment.assesment_speciesname,"
            "SpeciesManualAssessment.region==Comment.region,"
            "SpeciesManualAssessment.user_id==Comment.user_id,"
            "SpeciesManualAssessment.dataset_id==Comment.dataset_id,"
            "SpeciesManualAssessment.MS==Comment.MS)"),
        foreign_keys=[assesment_speciesname, region, user_id, MS],
        backref='comments',
    )
    author = relationship(
        'RegisteredUser',
        primaryjoin="Comment.author_id==RegisteredUser.id",
        foreign_keys=author_id,
    )
    user = relationship(
        'RegisteredUser',
        primaryjoin="Comment.user_id==RegisteredUser.id",
        foreign_keys=user_id,
    )
    readers = relationship("RegisteredUser",
                           secondary=t_comments_read,
                           backref='read_species_comments')

    def read_for(self, user):
        return user in self.readers

    @hybrid_property
    def subject(self):
        return self.assesment_speciesname

    @subject.setter
    def subject(self, value):
        self.assesment_speciesname = value


class DicCountryCode(Base):
    __tablename__ = 'dic_country_codes'

    code = Column(String(3), primary_key=True)
    codeEU = Column(String(3), default='')
    name = Column(String(40))

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )


class EtcDataHabitattypeAutomaticAssessment(Base):
    __tablename__ = 'etc_data_habitattype_automatic_assessment'

    country = Column(String(4))
    assessment_method = Column(String(10), primary_key=True, nullable=False)
    order = Column(Integer)
    habitatcode = Column(String(4), primary_key=True, nullable=False)
    region = Column(String(4), primary_key=True, nullable=False)
    range_surface_area = Column(String(100))
    percentage_range_surface_area = Column(String(100))
    range_trend = Column(String(100))
    percentage_range_trend = Column(String(100))
    range_yearly_magnitude = Column(String(100))
    complementary_favourable_range = Column(String(100))
    coverage_surface_area_min = Column(String(100))
    coverage_surface_area_max = Column(String(100))
    coverage_surface_area = Column(String(100))
    coverage_estimate_type = Column(String(50))
    coverage_method = Column(String(50))
    percentage_coverage_surface_area = Column(String(100))
    coverage_trend = Column(String(100))
    percentage_coverage_trend = Column(String(100))
    coverage_yearly_magnitude = Column(String(100))
    complementary_favourable_area = Column(String(100))
    hab_condition_good = Column(String(50))
    hab_condition_notgood = Column(String(50))
    hab_condition_unknown = Column(String(50))
    hab_condition_trend = Column(String(10))
    percentage_hab_condition_trend = Column(String(100))
    conclusion_range = Column(String(3))
    conclusion_range_gis = Column(String(3))
    conclusion_area = Column('conclusion_coverage', String(3))
    conclusion_area_gis = Column('conclusion_coverage_gis', String(3))
    percentage_structure = Column(String(100))
    conclusion_structure = Column(String(3))
    future_range = Column(String(100))
    future_area = Column(String(100))
    future_structure = Column(String(100))
    percentage_future = Column(String(100))
    conclusion_future = Column(String(3))
    percentage_assessment = Column(String(100))
    conclusion_assessment = Column(String(3))
    percentage_assessment_trend = Column(String(100))
    conclusion_assessment_trend = Column(String(1))
    percentage_assessment_trend_unfavourable = Column(String(100))
    conclusion_assessment_change = Column(String(2))
    conclusion_assessment_prev = Column(String(3))
    conclusion_assessment_trend_prev = Column(String(20))
    range_grid_area = Column(String(100))
    percentage_range_grid_area = Column(String(100))
    distribution_grid_area = Column(String(100))
    percentage_distribution_grid_area = Column(String(100))
    percentage_assessment_change = Column(String(100))
    percentage_assessment_trend_change = Column(String(100))
    assessment_needed = Column(Integer)
    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        default=4,
        primary_key=True,
    )
    use_for_statistics = Column(Boolean)

    @hybrid_property
    def subject(self):
        return self.habitatcode


class EtcDataHabitattypeRegion(Base):
    __tablename__ = 'etc_data_habitattype_regions'

    country = Column(String(3), primary_key=True, nullable=False)
    eu_country_code = Column(String(2))
    delivery = Column(Integer, nullable=False)
    envelope = Column(String(50), nullable=False)
    filename = Column(String(300), nullable=False)
    region = Column(String(4), primary_key=True, nullable=False)
    region_ms = Column(String(4)) # region_orig for period 2018
    region_changed = Column(Integer)
    group = Column(String(21))
    annex = Column(String(11))
    annex_I = Column(String(2))
    priority = Column(String(1))
    code = Column(String(4))
    habitatcode = Column(String(4), primary_key=True)
    presence_new = Column(String(60)) # presence
    habitattype_type = Column(String(10))
    habitattype_type_asses = Column(Integer)
    range_surface_area = Column(Float(asdecimal=True))
    range_change_reason = Column(String(150))
    percentage_range_surface_area = Column(Float(asdecimal=True))
    range_trend = Column(String(10))
    range_trend_method = Column(String(50))
    range_yearly_magnitude = Column(Float(asdecimal=True))
    complementary_favourable_range_q = Column(String(2))
    complementary_favourable_range = Column(Float(asdecimal=True))
    coverage_surface_area_min = Column(Float(asdecimal=True))
    coverage_surface_area_max = Column(Float(asdecimal=True))
    coverage_surface_area = Column(Float(asdecimal=True))
    coverage_etc = Column(Float(asdecimal=True))
    coverage_estimate_type = Column(String(50))
    coverage_method = Column(String(50))
    coverage_change_reason = Column(String(150))
    percentage_coverage_surface_area = Column(Float(asdecimal=True))
    coverage_trend = Column(String(1))
    coverage_trend_method = Column(String(50))
    coverage_yearly_magnitude = Column(Float(asdecimal=True))
    complementary_favourable_area_q = Column(String(2))
    complementary_favourable_area = Column(Float(asdecimal=True))
    hab_condition_good_min = Column(Float(asdecimal=True))
    hab_condition_good_max = Column(Float(asdecimal=True))
    hab_condition_notgood_min = Column(Float(asdecimal=True))
    hab_condition_notgood_max = Column(Float(asdecimal=True))
    hab_condition_unknown_min = Column(Float(asdecimal=True))
    hab_condition_unknown_max = Column(Float(asdecimal=True))
    hab_condition_method = Column(String(50))
    hab_condition_good = Column(Float(asdecimal=True))
    hab_condition_notgood = Column(Float(asdecimal=True))
    hab_condition_unknown = Column(Float(asdecimal=True))
    percentage_hab_condition_good = Column(Float(asdecimal=True))
    hab_condition_trend = Column(String(50))
    hab_condition_trend_method = Column(String(50))
    future_range = Column(String(20))
    future_area = Column(String(20))
    future_structure = Column(String(20))
    conclusion_range = Column(String(3))
    conclusion_area = Column(String(3))
    conclusion_structure = Column(String(3))
    conclusion_future = Column(String(3))
    conclusion_assessment = Column(String(3))
    conclusion_assessment_trend = Column(String(1))
    conclusion_assessment_prev = Column(String(3))
    conclusion_assessment_trend_prev = Column(String(20))
    conclusion_assessment_change = Column(String(20))
    conclusion_assessment_trend_change = Column(String(20))
    range_quality = Column(String(13))
    coverage_quality = Column(String(13))
    complementary_other_information = Column(Text)
    complementary_other_information_english = Column(Text)
    range_grid_area = Column(Float(asdecimal=True))
    percentage_range_grid_area = Column(Float(asdecimal=True))
    distribution_grid_area = Column(Float(asdecimal=True))
    distribution_method = Column(String(50))
    percentage_distribution_grid_area = Column(Float(asdecimal=True))
    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        default=4,
        primary_key=True,
    )
    dataset = relationship(Dataset)

    remote_url_2006 = Column(String(350), nullable=True)
    remote_url_2012 = Column(String(350), nullable=True)

    use_for_statistics = Column(Boolean)

    habitat = relationship(
        'EtcDicHdHabitat',
        primaryjoin='EtcDicHdHabitat.habcode==EtcDataHabitattypeRegion.subject',
        foreign_keys=[habitatcode]
    )

    habitattype_type_details = relationship(
        'EtcDicSpeciesType',
        primaryjoin=
        'EtcDataHabitattypeRegion.habitattype_type==EtcDicSpeciesType.abbrev',
        foreign_keys=habitattype_type,
    )

    lu_factsheets = relationship(
        'LuHdHabitatFactsheet',
        primaryjoin=
        'LuHdHabitatFactsheet.habcode==EtcDataHabitattypeRegion.subject',
        foreign_keys=[habitatcode]
    )

    @property
    def is_assesm(self):
        return self.habitattype_type_asses == 0

    @hybrid_property
    def subject(self):
        return self.habitatcode

    @hybrid_property
    def presence(self):
        return self.habitattype_type_asses


class EtcDataHcoveragePressure(Base):
    __tablename__ = 'etc_data_hcoverage_pressures'

    eu_country_code = Column(String(2), primary_key=True, nullable=False)
    region = Column(String(4), primary_key=True, nullable=False)
    habitatcode = Column(String(4), primary_key=True, nullable=False,
                         default='0')
    pressure = Column(String(3), primary_key=True, nullable=False,
                      default='')

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )


class EtcDataHcoverageThreat(Base):
    __tablename__ = 'etc_data_hcoverage_threats'

    eu_country_code = Column(String(2), primary_key=True, nullable=False)
    region = Column(String(4), primary_key=True, nullable=False)
    habitatcode = Column(String(4), primary_key=True, nullable=False,
                         default='0')
    threat = Column(String(3), primary_key=True, nullable=False, default='')

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )


class EtcDataSpeciesAutomaticAssessment(Base):
    __tablename__ = 'etc_data_species_automatic_assessment'

    country = Column(String(10))
    assessment_method = Column(String(3), primary_key=True, nullable=False)
    order = Column(Integer)
    assessment_speciescode = Column(Integer)
    assesment_speciesname = Column(String(60), primary_key=True, nullable=False)
    region = Column(String(4), primary_key=True, nullable=False)
    range_surface_area = Column(String(100))
    percentage_range_surface_area = Column(String(100))
    range_trend = Column(String(100))
    percentage_range_trend = Column(String(100))
    range_yearly_magnitude = Column(String(100))
    complementary_favourable_range = Column(String(100))
    population_minimum_size = Column(String(100))
    population_maximum_size = Column(String(100))
    population_size = Column(String(100))
    population_size_unit = Column(String(20))
    population_estimate_type = Column(String(50))
    population_method = Column(String(50))
    percentage_population_mean_size = Column(String(100))
    population_trend = Column(String(100))
    percentage_population_trend = Column(String(100))
    population_yearly_magnitude = Column(String(100))
    complementary_favourable_population = Column(String(100))
    complementary_favourable_population_unit = Column(String(20))
    habitat_surface_area = Column(String(100))
    percentage_habitat_surface_area = Column(String(100))
    habitat_trend = Column(String(100))
    complementary_suitable_habitat = Column(String(100))
    habitat_sufficiency_occupied = Column(String(20))
    habitat_sufficiency_unoccupied = Column(String(20))
    percentage_habitat_sufficiency = Column(String(100))
    percentage_future = Column(String(100))
    conclusion_range = Column(String(3))
    conclusion_range_gis = Column(String(3))
    conclusion_population = Column(String(3))
    conclusion_population_gis = Column(String(3))
    conclusion_habitat = Column(String(3))
    conclusion_habitat_gis = Column(String(3))
    future_range = Column(String(200))
    future_population = Column(String(200))
    future_habitat = Column(String(200))
    conclusion_future = Column(String(3))
    percentage_assessment = Column(String(100))
    conclusion_assessment = Column(String(3))
    percentage_assessment_trend = Column(String(100))
    percentage_assessment_trend_unfavourable = Column(String(100))
    conclusion_assessment_trend = Column(String(1))
    conclusion_assessment_change = Column(String(20))
    conclusion_assessment_prev = Column(String(3))
    conclusion_assessment_trend_prev = Column(String(20))
    range_grid_area = Column(String(100))
    percentage_range_grid_area = Column(String(100))
    distribution_grid_area = Column(String(100))
    percentage_distribution_grid_area = Column(String(100))
    assessment_needed = Column(Integer)
    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        default=4,
        primary_key=True,
    )
    percentage_assessment_change = Column(String(100))
    percentage_assessment_trend_change = Column(String(200))
    use_for_statistics = Column(Boolean)

    @hybrid_property
    def subject(self):
        return self.assesment_speciesname


class EtcDataSpeciesRegion(Base):
    __tablename__ = 'etc_data_species_regions'

    country = Column(String(3), primary_key=True, nullable=False)
    eu_country_code = Column(String(2), nullable=False)
    delivery = Column(Integer, nullable=False)
    envelope = Column(String(50), nullable=False)
    filename = Column(String(300), nullable=False)
    region = Column(String(4), primary_key=True, nullable=False)
    region_ms = Column(String(4)) # region_orig for period 2018
    region_was_changed = Column(Integer)
    group_old = Column('group', String(21))
    group = Column('tax_group', String(20))
    tax_order = Column(Integer)
    upper_group = Column(String(30))
    mid_group = Column(String(20))
    family = Column(String(30))
    annex = Column(String(11))
    annex_II = Column(String(2))
    annex_II_exception = Column(Integer)
    priority = Column(String(1))
    annex_IV = Column(String(2))
    annex_IV_exception = Column(Integer)
    annex_V = Column(String(1))
    annex_V_addition = Column(Integer)
    code = Column(String(50))
    speciescode = Column(String(32), primary_key=True)
    speciesname = Column(String(50))
    species_name_different = Column(Integer)
    eunis_species_code = Column(Integer)
    valid_speciesname = Column(String(50))
    n2000_species_code = Column(Integer) 
    speciescode_IRM =Column(String(10)) # 2018 n2000_species_code
    assessment_speciescode =  Column(Integer)
    assesment_speciesname = Column(String(60))
    assessment_speciesname_changed = Column(Integer)
    presence_new = Column(String(60)) # presence
    grouped_assesment = Column(Integer)
    species_type = Column(String(10))
    species_type_asses = Column(Integer)
    range_surface_area = Column(Float(asdecimal=True))
    range_change_reason = Column(String(150))
    range_trend = Column(String(1))
    range_trend_method = Column(String(50))
    range_yearly_magnitude = Column(Float(asdecimal=True))
    complementary_favourable_range_q = Column(String(2))
    complementary_favourable_range = Column(Float(asdecimal=True))
    population_minimum_size = Column(Float(asdecimal=True))
    population_maximum_size = Column(Float(asdecimal=True))
    population_size_unit = Column(String(10))
    population_size = Column(Float(asdecimal=True)) # best value
    percentage_range_surface_area = Column(Float(asdecimal=True))
    population_estimate_type = Column(String(50))
    population_method = Column(String(50))
    population_alt_size = Column(Float(asdecimal=True))
    population_alt_size_min = Column(Float(asdecimal=True))
    population_alt_size_max = Column(Float(asdecimal=True))
    population_alt_size_unit = Column(String(10))
    population_alt_estimate_type = Column(String(50))
    percentage_population_minimum_size = Column(Float(asdecimal=True))
    percentage_population_maximum_size = Column(Float(asdecimal=True))
    filled_population = Column(String(3))
    population_units_agreed = Column(String(50))
    population_units_change = Column(Boolean)
    population_units_other = Column(String(50))
    population_change_reason = Column(String(150))
    number_of_different_population_units = Column(Integer)
    different_population_percentage = Column(Integer)
    percentage_population_mean_size = Column(Float(asdecimal=True))
    popsize_etc = Column(Float(asdecimal=True))
    population_trend = Column(String(1))
    population_trend_method = Column(String(50))
    population_yearly_magnitude = Column(Float(asdecimal=True))
    complementary_favourable_population_q = Column(String(4))
    complementary_favourable_population = Column(Float(asdecimal=True))
    complementary_favourable_population_unit = Column(String(50))
    filled_complementary_favourable_population = Column(String(3))
    habitat_surface_area = Column(Float(asdecimal=True))
    habitat_change_reason = Column(String(150))
    habitat_sufficiency_occupied = Column(String(20))
    habitat_sufficiency_method = Column(String(20))
    habitat_sufficiency_unoccupied = Column(String(20))
    percentage_habitat_surface_area = Column(Float(asdecimal=True))
    habitat_trend = Column(String(1))
    habitat_trend_method = Column(String(50))
    complementary_suitable_habitat = Column(Float(asdecimal=True))
    future_range = Column(String(20))
    future_population = Column(String(20))
    future_habitat = Column(String(20))
    future_prospects = Column(String(4))
    conclusion_range = Column(String(3))
    conclusion_population = Column(String(3))
    conclusion_habitat = Column(String(3))
    conclusion_future = Column(String(3))
    conclusion_assessment = Column(String(3))
    conclusion_assessment_trend = Column(String(4))
    conclusion_assessment_prev = Column(String(3))
    conclusion_assessment_trend_prev = Column(String(20))
    conclusion_assessment_change = Column(String(20))
    conclusion_assessment_trend_change = Column(String(20))
    range_quality = Column(String(13))
    population_quality = Column(String(13))
    habitat_quality = Column(String(13))
    complementary_other_information = Column(Text)
    complementary_other_information_english = Column(Text)
    range_grid_area = Column(Float(asdecimal=True))
    percentage_range_grid_area = Column(Float(asdecimal=True))
    distribution_grid_area = Column(Float(asdecimal=True))
    distribution_method = Column(String(50))
    percentage_distribution_grid_area = Column(Float(asdecimal=True))
    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        default=4,
        primary_key=True,
    )
    dataset = relationship(Dataset)
    use_for_statistics = Column(Boolean)
    population_unit = Column(String(20)) # this is actually population_size_unit

    remote_url_2006 = Column(String(350), nullable=True)
    remote_url_2012 = Column(String(350), nullable=True)
    species_type_details = relationship(
        'EtcDicSpeciesType',
        primaryjoin=(
            "and_(EtcDataSpeciesRegion.species_type==EtcDicSpeciesType.abbrev,"
            "EtcDataSpeciesRegion.dataset_id==EtcDicSpeciesType.dataset_id)"),
        foreign_keys=species_type,
    )

    @property
    def is_assesm(self):
        return self.species_type_asses == 0

    @property
    def mapcode(self):
        if self.speciescode in ('1033', '1763', '2016', '2527'):
            return self.speciescode
        return unicode(self.n2000_species_code)

    @hybrid_property
    def subject(self):
        return self.assesment_speciesname

    @hybrid_property
    def presence(self):
        return self.species_type_asses


class EtcDataSpopulationPressure(Base):
    __tablename__ = 'etc_data_spopulation_pressures'

    eu_country_code = Column(String(2), primary_key=True, nullable=False)
    region = Column(String(4), primary_key=True, nullable=False)
    n2000_species_code = Column(Integer, primary_key=True, nullable=False,
                                default=0)
    assesment_speciesname = Column(String(60), nullable=False)
    pressure = Column(String(3), primary_key=True, nullable=False, default='')

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )


class EtcDataSpopulationThreat(Base):
    __tablename__ = 'etc_data_spopulation_threats'

    eu_country_code = Column(String(2), primary_key=True, nullable=False)
    region = Column(String(4), primary_key=True, nullable=False)
    n2000_species_code = Column(Integer, primary_key=True, nullable=False,
                                default=0)
    assesment_speciesname = Column(String(60), nullable=False)
    threat = Column(String(3), primary_key=True, nullable=False, default='')

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )


class EtcDicBiogeoreg(Base):
    __tablename__ = 'etc_dic_biogeoreg'

    reg_code = Column(String(4), primary_key=True)
    reg_name = Column(String(60))
    ordine = Column(Integer)
    order = Column(Integer)

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )

    @classmethod
    def get_region_name(cls, reg_code, dataset_id):
        return (
            cls.query.with_entities(cls.reg_name)
            .filter(cls.reg_code == reg_code,
                    cls.dataset_id == dataset_id)
            .first()
        )


class EtcDicConclusion(Base):
    __tablename__ = 'etc_dic_conclusion'

    order = Column(Integer)
    conclusion = Column(String(3), primary_key=True)
    details = Column(String(90))

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )

    @classmethod
    def all(cls, dataset_id):
        return cls.query.with_entities(cls.conclusion)\
            .filter_by(dataset_id=dataset_id).order_by(cls.conclusion)


class EtcDicDecision(Base):
    __tablename__ = 'etc_dic_decision'

    order = Column(Integer)
    decision = Column(String(4), primary_key=True)
    details = Column(String(70))

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )


class EtcDicHdHabitat(Base):
    __tablename__ = 'etc_dic_hd_habitats'

    habcode = Column(String(4), primary_key=True)
    group = Column(String(40))
    priority = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)
    shortname = Column(String(70))
    annex_I_comments = Column(String(30))
    marine = Column(Integer)

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )


class EtcDicMethod(Base):
    __tablename__ = 'etc_dic_method'

    order = Column(Integer)
    method = Column(String(10), primary_key=True)
    details = Column(String(125))

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )

    @classmethod
    def all(cls, dataset_id):
        return (
            cls.query
            .filter(cls.method != '')
            .filter_by(dataset_id=dataset_id)
            .with_entities(cls.method)
            .order_by(cls.method)
        )


class EtcDicPopulationUnit(Base):
    __tablename__ = 'etc_dic_population_units'

    order = Column(Integer)
    population_units = Column(String(16), primary_key=True)
    details = Column(String(40))
    code = Column(String(16))

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )

    @classmethod
    def all(cls, dataset_id):
        return (
            cls.query.with_entities(cls.population_units, cls.details)
            .filter_by(dataset_id=dataset_id)
            .order_by(cls.order)
        )


class EtcDicSpeciesType(Base):
    __tablename__ = 'etc_dic_species_type'

    SpeciesTypeID = Column(Integer, primary_key=True)
    SpeciesType = Column(String(50))
    Assesment = Column(String(50))
    Note = Column(String(255))
    abbrev = Column(String(5))

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )


class EtcDicTrend(Base):
    __tablename__ = 'etc_dic_trend'

    id = Column(Integer, primary_key=True)
    trend = Column(String(3))
    details = Column(String(125))

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )

    @classmethod
    def all(cls, dataset_id):
        return cls.query.with_entities(cls.trend) \
            .filter_by(dataset_id=dataset_id).all()


class EtcQaErrorsHabitattypeManualChecked(Base):
    __tablename__ = 'etc_qa_errors_habitattype_manual_checked'

    country = Column(String(3), primary_key=True, nullable=False)
    eu_country_code = Column(String(2))
    filename = Column(String(60), primary_key=True, nullable=False)
    region = Column(String(4), primary_key=True, nullable=False)
    habitatcode = Column(String(50))
    suspect_value = Column(String(150), nullable=False, default='')
    error_code = Column(Integer, primary_key=True, nullable=False)
    error_description = Column(Text)
    field = Column('FlagField', String(40))
    text = Column('FlagText', String(65))

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )

    @hybrid_property
    def subject(self):
        return self.habitatcode


class EtcQaErrorsSpeciesManualChecked(Base):
    __tablename__ = 'etc_qa_errors_species_manual_checked'

    country = Column(String(3), primary_key=True, nullable=False)
    eu_country_code = Column(String(2))
    filename = Column(String(60), primary_key=True, nullable=False)
    region = Column(String(4), primary_key=True, nullable=False)
    assesment_speciesname = Column(String(60))
    suspect_value = Column(String(150), nullable=False, default='')
    error_code = Column(Integer, primary_key=True, nullable=False)
    error_description = Column(Text)
    field = Column('FlagField', String(40))
    text = Column('FlagText', String(65))

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )

    @hybrid_property
    def subject(self):
        return self.assesment_speciesname


t_habitat_comments_read = Table(
    'habitat_comments_read', metadata,
    Column('id_comment', ForeignKey('habitat_comments.id'), nullable=False),
    Column('reader_user_id', String(25), ForeignKey('registered_users.user'))
)


class HabitatComment(Base):
    __tablename__ = 'habitat_comments'

    id = Column(Integer, primary_key=True, unique=True)
    region = Column(String(4), nullable=False)
    habitat = Column(String(50), nullable=False)
    user_id = Column('user', String(25), nullable=False)
    MS = Column(String(4), nullable=False, default=DEFAULT_MS)
    comment = Column(String)
    author_id = Column('author', String(25), nullable=False)
    post_date = Column(String(16), nullable=False)
    deleted = Column(Integer)
    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
    )

    record = relationship(
        'HabitattypesManualAssessment',
        primaryjoin=(
            "and_(HabitattypesManualAssessment.habitatcode=="
            "HabitatComment.habitat,"
            "HabitattypesManualAssessment.region==HabitatComment.region,"
            "HabitattypesManualAssessment.user_id==HabitatComment.user_id,"
            "HabitattypesManualAssessment.dataset_id==HabitatComment.dataset_id,"
            "HabitattypesManualAssessment.MS==HabitatComment.MS)"),
        foreign_keys=[habitat, region, user_id, MS],
        backref='comments',
    )
    author = relationship(
        'RegisteredUser',
        primaryjoin="HabitatComment.author_id==RegisteredUser.id",
        foreign_keys=author_id,
    )
    user = relationship(
        'RegisteredUser',
        primaryjoin="HabitatComment.user_id==RegisteredUser.id",
        foreign_keys=user_id,
    )
    readers = relationship("RegisteredUser",
                           secondary=t_habitat_comments_read,
                           backref='read_habitat_comments')

    def read_for(self, user):
        return user in self.readers

    @hybrid_property
    def subject(self):
        return self.habitat

    @subject.setter
    def subject(self, value):
        self.habitat = value


t_habitat_group = Table(
    'habitat_group', metadata,
    Column('habitatcode', String(4)),
    Column('group', String(21)),
    Column('ext_dataset_id', ForeignKey('datasets.id')),
)


class HabitattypesManualAssessment(Base):
    __tablename__ = 'habitattypes_manual_assessment'

    MS = Column(String(4), primary_key=True, nullable=False,
                default=DEFAULT_MS)
    region = Column(String(4), primary_key=True, nullable=False)
    habitatcode = Column(String(50), primary_key=True, nullable=False)
    range_surface_area = Column(String(23))
    range_trend = Column(String(3))
    range_yearly_magnitude = Column(String(23))
    complementary_favourable_range = Column(String(23))
    complementary_favourable_range_q = Column(String(2))
    coverage_surface_area = Column(String(23))
    coverage_surface_area_min = Column(String(23))
    coverage_surface_area_max = Column(String(23))
    coverage_trend = Column(String(3))
    coverage_yearly_magnitude = Column(String(23))
    complementary_favourable_area = Column(String(23))
    complementary_favourable_area_q = Column(String(2))
    method_range = Column(String(3))
    conclusion_range = Column(String(2))
    method_area = Column(String(3))
    conclusion_area = Column(String(2))
    hab_condition_good_min = Column(String(23))
    hab_condition_good_max = Column(String(23))
    hab_condition_good_best = Column(String(23))
    hab_condition_notgood_min = Column(String(23))
    hab_condition_notgood_max = Column(String(23))
    hab_condition_notgood_best = Column(String(23))
    hab_condition_unknown_min = Column(String(23))
    hab_condition_unknown_max = Column(String(23))
    hab_condition_unknown_best = Column(String(23))
    hab_condition_trend =  Column(String(5))
    method_structure = Column(String(3))
    conclusion_structure = Column(String(2))
    method_future = Column(String(3))
    future_range = Column(String(20))
    future_area = Column(String(20))
    future_structure = Column(String(20))
    conclusion_future = Column(String(2))
    method_assessment = Column(String(3))
    conclusion_assessment = Column(String(2))
    conclusion_assessment_trend = Column(String(1))
    conclusion_assessment_prev = Column(String(3))
    conclusion_assessment_trend_prev = Column(String(20))
    conclusion_assessment_change = Column(String(20))
    conclusion_assessment_trend_change = Column(String(20))
    method_target1 = Column(String(3))
    conclusion_target1 = Column(String(3))
    backcasted_2007 = Column(String(4))
    user_id = Column('user', String(25), primary_key=True, nullable=False,
                     default='')
    last_update = Column(String(16))
    deleted = Column('deleted_record', Integer)
    decision = Column(String(3))
    user_decision_id = Column('user_decision', String(25))
    last_update_decision = Column(String(16))
    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )

    user = relationship(
        'RegisteredUser',
        primaryjoin="HabitattypesManualAssessment.user_id==RegisteredUser.id",
        foreign_keys=user_id,
    )
    user_decision = relationship(
        'RegisteredUser',
        primaryjoin="HabitattypesManualAssessment.user_decision_id==RegisteredUser.id",
        foreign_keys=user_decision_id,
    )
    dataset = relationship(Dataset)

    def comments_count_read(self, user):
        if not self.comments:
            return 0
        return (db.session.query(HabitatComment.id)
                .join(t_habitat_comments_read)
                .filter(HabitatComment.habitat == self.habitatcode)
                .filter(HabitatComment.region == self.region)
                .filter(HabitatComment.MS == self.MS)
                .filter(HabitatComment.user_id == self.user_id)
                .filter(HabitatComment.dataset_id == self.dataset_id)
                .filter('habitat_comments_read.reader_user_id="%s"' % user)
                .filter(or_(HabitatComment.deleted == 0,
                            HabitatComment.deleted == None))
                .count())

    @hybrid_property
    def subject(self):
        return self.habitatcode

    @subject.setter
    def subject(self, value):
        self.habitatcode = value

    def undeleted_comments(self, user_id):
        user = RegisteredUser.query.filter_by(id=user_id).first()
        return [c for c in self.comments if not c.deleted or
                c.author_id == user_id or (user and user.has_role('admin'))]


class LuHdHabitat(Base):
    __tablename__ = 'lu_hd_habitats'

    habcode = Column(String(4), primary_key=True)
    group = Column(String(40))
    priority = Column(Integer, nullable=False)
    name = Column(String(160), nullable=False)
    annex_I_comments = Column(String(30))
    marine = Column(Integer)

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )


class LuHdHabitatFactsheet(Base):
    __tablename__ = 'lu_hd_habitats_factsheets'

    habcode = Column(String(4), primary_key=True)
    group = Column(String(40))
    priority = Column(Integer, nullable=False)
    name = Column(String(155), nullable=False)
    shortname = Column(String(155), nullable=False)
    annex_I_comments = Column(String(30))
    marine = Column(Integer)
    nameheader = Column(String(155), nullable=False)


class PhotoHabitat(Base):
    __tablename__ = 'photo_habitats'

    id = Column(Integer, primary_key=True)
    habitatcode = Column(String(4), nullable=False, default='')
    description = Column(String(4096))
    photographer = Column(String(64))
    location = Column(String(64))
    content_type = Column(String(32))
    picture_date = Column(DateTime, nullable=False,
                          server_default=u'CURRENT_TIMESTAMP')
    picture_data = Column(db.BLOB())
    thumbnail = Column(db.BLOB())
    user = Column(String(50), nullable=False, default='')

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )


class PhotoSpecy(Base):
    __tablename__ = 'photo_species'

    id = Column(Integer, primary_key=True)
    assessment_speciesname = Column(String(60), nullable=False, default='')
    description = Column(String(255))
    photographer = Column(String(64))
    location = Column(String(64))
    karma = Column(Integer, nullable=False, default=0)
    content_type = Column(String(32))
    picture_date = Column(DateTime)
    picture_data = Column(LargeBinary)
    thumbnail = Column(LargeBinary)
    user = Column(String(50), nullable=False, default='')

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )


roles_users = db.Table(
    'roles_users',
    db.Column('registered_users_user', db.String(50),
              db.ForeignKey('registered_users.user')),
    db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')),
)


class RegisteredUser(Base, UserMixin):
    __tablename__ = 'registered_users'

    id = Column('user', String(50), primary_key=True)
    name = Column(String(255))
    institution = Column(String(45))
    abbrev = Column(String(10))
    MS = Column(String(255))
    email = Column(String(255))
    qualification = Column(String(255))
    account_date = Column(String(16), nullable=False)
    show_assessment = Column(Integer, nullable=False, default=1)
    active = Column(Boolean)
    confirmed_at = db.Column(db.DateTime())
    is_ldap = db.Column(Boolean, nullable=False, default=False)
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic'),
    )
    password = db.Column(String(60))

    def has_role(self, role):
        return role in [r.name for r in self.roles]

    @staticmethod
    def try_login(username, password):
        conn = get_ldap_connection()
        conn.simple_bind_s(
            'uid=%s,ou=Users,o=EIONET,l=Europe' % username,password
        )

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

class Role(Base, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=False, unique=True)


t_restricted_habitats = Table(
    'restricted_habitats', metadata,
    Column('habitatcode', String(4)),
    Column('eu_country_code', String(2), nullable=False, default=''),
    Column('show_data', SmallInteger),
    Column('ext_dataset_id', ForeignKey('datasets.id')),
)


t_restricted_species = Table(
    'restricted_species', metadata,
    Column('assesment_speciesname', String(60), nullable=False, default=''),
    Column('eu_country_code', String(2), nullable=False, default=''),
    Column('show_data', SmallInteger),
    Column('ext_dataset_id', ForeignKey('datasets.id')),
)


t_species_group = Table(
    'species_group', metadata,
    Column('assesment_speciesname', String(60)),
    Column('group', String(21)),
    Column('ext_dataset_id', ForeignKey('datasets.id')),
)


class SpeciesManualAssessment(Base):
    __tablename__ = 'species_manual_assessment'

    MS = Column(String(4), primary_key=True, nullable=False, default=DEFAULT_MS)
    region = Column(String(4), primary_key=True, nullable=False)
    assesment_speciesname = Column(String(60), primary_key=True,
                                   nullable=False)
    range_surface_area = Column(String(23))
    range_trend = Column(String(3))
    range_yearly_magnitude = Column(String(23))
    complementary_favourable_range = Column(String(23))
    complementary_favourable_range_q = Column(String(2))
    population_size = Column(String(23))
    population_size_unit = Column(String(6))
    population_minimum_size = Column(String(23))
    population_maximum_size = Column(String(23))
    population_best_value = Column(String(23))
    population_unit = Column(String(20))
    population_trend = Column(String(3))
    population_yearly_magnitude = Column(String(23))
    complementary_favourable_population = Column(String(23))
    complementary_favourable_population_q = Column(String(2))
    complementary_favourable_population_unit = Column(String(20))
    habitat_surface_area = Column(String(23))
    habitat_trend = Column(String(3))
    complementary_suitable_habitat = Column(String(23))
    method_range = Column(String(3))
    conclusion_range = Column(String(2))
    method_population = Column(String(3))
    conclusion_population = Column(String(2))
    method_habitat = Column(String(3))
    conclusion_habitat = Column(String(2))
    method_future = Column(String(3))
    future_range = Column(String(20))
    future_population = Column(String(20))
    future_habitat = Column(String(20))
    conclusion_future = Column(String(2))
    method_assessment = Column(String(3))
    conclusion_assessment = Column(String(2))
    conclusion_assessment_trend = Column(String(1))
    conclusion_assessment_prev = Column(String(3))
    conclusion_assessment_trend_prev = Column(String(20))
    conclusion_assessment_change = Column(String(2))
    conclusion_assessment_trend_change = Column(String(20))
    method_target1 = Column(String(3))
    conclusion_target1 = Column(String(3))
    backcasted_2007 = Column(String(4))

    user_id = Column('user', String(25), primary_key=True, nullable=False,
                     default='')
    last_update = Column(String(16))
    deleted = Column('deleted_record', Integer)
    decision = Column(String(3))
    user_decision_id = Column('user_decision', String(25))
    last_update_decision = Column(String(16))
    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )

    user = relationship(
        'RegisteredUser',
        primaryjoin="SpeciesManualAssessment.user_id==RegisteredUser.id",
        foreign_keys=user_id,
    )
    user_decision = relationship(
        'RegisteredUser',
        primaryjoin="SpeciesManualAssessment.user_decision_id==RegisteredUser.id",
        foreign_keys=user_decision_id,
    )
    dataset = relationship(Dataset)

    def comments_count_read(self, user):
        if not self.comments:
            return 0
        return (db.session.query(Comment.id)
                .join(t_comments_read)
                .filter(Comment.assesment_speciesname == self.assesment_speciesname)
                .filter(Comment.region == self.region)
                .filter(Comment.MS == self.MS)
                .filter(Comment.user_id == self.user_id)
                .filter(Comment.dataset_id == self.dataset_id)
                .filter('comments_read.reader_user_id="%s"' % user)
                .filter(or_(Comment.deleted == 0, Comment.deleted == None))
                .count())

    @hybrid_property
    def subject(self):
        return self.assesment_speciesname

    @subject.setter
    def subject(self, value):
        self.assesment_speciesname = value

    def undeleted_comments(self, user_id):
        user = RegisteredUser.query.filter_by(id=user_id).first()
        return [c for c in self.comments if not c.deleted or
                c.author_id == user_id or (user and user.has_role('admin'))]


t_species_name = Table(
    'species_name', metadata,
    Column('priority', String(1)),
    Column('assesment_speciesname', String(60)),
    Column('ext_dataset_id', ForeignKey('datasets.id')),
)


class Wiki(Base):
    __tablename__ = 'wiki'

    id = Column(Integer, primary_key=True)
    region_code = Column('region', String(4), nullable=False)
    assesment_speciesname = Column(String(60))
    habitatcode = Column(String(4))

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
    )

    @hybrid_property
    def subject(self):
        return self.assesment_speciesname or self.habitatcode


class WikiChange(Base):
    __tablename__ = 'wiki_changes'

    id = Column(Integer, primary_key=True)
    wiki_id = Column(ForeignKey('wiki.id'), nullable=False)
    body = Column(String(6000), nullable=False)
    editor = Column(String(60), nullable=False)
    changed = Column(DateTime, nullable=False,
                     server_default=u'CURRENT_TIMESTAMP')
    active = Column(Integer, default=0)
    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
    )
    dataset = relationship(Dataset)
    wiki = relationship(
        u'Wiki',
        primaryjoin="and_(WikiChange.wiki_id==Wiki.id,"
        "WikiChange.dataset_id==Wiki.dataset_id)",
        foreign_keys=[wiki_id, dataset_id],
        backref='changes',
    )


t_wiki_comments_read = Table(
    'wiki_comments_read', metadata,
    Column('comment_id', ForeignKey('wiki_comments.id')),
    Column('reader_id', String(60), ForeignKey('registered_users.user'))
)


class WikiComment(Base):
    __tablename__ = 'wiki_comments'

    id = Column(Integer, primary_key=True)
    wiki_id = Column(ForeignKey('wiki.id'), nullable=False)
    comment = Column(String, nullable=False)
    author_id = Column('author', String(60), nullable=False)
    deleted = Column(Integer)
    posted = Column(
        DateTime, nullable=False,
        server_default=u'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')
    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
    )

    wiki = relationship(
        u'Wiki',
        primaryjoin="and_(WikiComment.wiki_id==Wiki.id,"
        "WikiComment.dataset_id==Wiki.dataset_id)",
        foreign_keys=[wiki_id, dataset_id],
        backref='comments',
    )

    author = relationship(
        'RegisteredUser',
        primaryjoin="WikiComment.author_id==RegisteredUser.id",
        foreign_keys=author_id,
    )

    readers = relationship("RegisteredUser",
                           secondary=t_wiki_comments_read,
                           backref='read_comments')

    def read_for(self, user):
        return user in self.readers or user == self.author


class WikiTrail(Base):
    __tablename__ = 'wiki_trail'

    id = Column(Integer, primary_key=True)
    region_code = Column('region', String(4), nullable=False)
    assesment_speciesname = Column(String(60))
    habitatcode = Column(String(4))
    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
    )

    region = relationship(
        'EtcDicBiogeoreg',
        primaryjoin="and_(WikiTrail.region_code==EtcDicBiogeoreg.reg_code,"
        "WikiTrail.dataset_id==EtcDicBiogeoreg.dataset_id)",
        foreign_keys=[region_code, dataset_id],
    )

    @hybrid_property
    def subject(self):
        return self.assesment_speciesname or self.habitatcode


class WikiTrailChange(Base):
    __tablename__ = 'wiki_trail_changes'

    id = Column(Integer, primary_key=True)
    wiki_id = Column(ForeignKey('wiki_trail.id'), nullable=False)
    body = Column(String(6000), nullable=False)
    editor = Column(String(60), nullable=False)
    changed = Column(DateTime, nullable=False,
                     server_default=u'CURRENT_TIMESTAMP')
    active = Column(Integer, default=0)
    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
    )
    dataset = relationship(Dataset)
    wiki = relationship(
        u'WikiTrail',
        primaryjoin="and_(WikiTrailChange.wiki_id==WikiTrail.id,"
        "WikiTrailChange.dataset_id==WikiTrail.dataset_id)",
        foreign_keys=[wiki_id, dataset_id],
        backref='changes',
    )


class WikiTrailComment(Base):
    __tablename__ = 'wiki_trail_comments'

    id = Column(Integer, primary_key=True)
    wiki_id = Column(ForeignKey('wiki_trail.id'), nullable=False)
    comment = Column(String, nullable=False)
    author = Column(String(60), nullable=False)
    deleted = Column(Integer)
    posted = Column(DateTime, nullable=False, server_default=
                    u'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
    )

    wiki = relationship(
        u'WikiTrail',
        primaryjoin="and_(WikiTrailComment.wiki_id==WikiTrail.id,"
        "WikiTrailComment.dataset_id==WikiTrail.dataset_id)",
        foreign_keys=[wiki_id, dataset_id],
        backref='comments',
    )


t_wiki_trail_comments_read = Table(
    'wiki_trail_comments_read', metadata,
    Column('comment_id', ForeignKey('wiki_trail_comments.id')),
    Column('reader_id', String(60))
)


class Config(Base):
    __tablename__ = 'config'

    id = Column(Integer, primary_key=True)
    start_date = Column(db.Date)
    end_date = Column(db.Date)
    admin_email = Column(db.String(255))
    default_dataset_id = Column(Integer, default=1)
    species_map_url = Column(db.String(255))
    sensitive_species_map_url = Column(db.String(255))
    habitat_map_url = Column(db.String(255))


class LuSpeciesManual2007(Base):
    __tablename__ = 'lu_species_manual_assessments_2007'

    subject = Column('assesment_speciesname', String(60), primary_key=True)
    region = Column(String(4), primary_key=True)
    conclusion_assessment = Column(String(2), nullable=True)
    conclusion_assessment_prev = Column(String(3), nullable=True) # used for period 2013
    conclusion_assessment_trend_prev = Column(String(20), nullable=True) # used for period 2013
    backcasted_2007 = Column(String(4), nullable=True) # used for period 2013
    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )


class LuHabitatManual2007(Base):
    __tablename__ = 'lu_habitattypes_manual_assessments_2007'

    subject = Column('habitatcode', String(50), primary_key=True)
    region = Column(String(4), primary_key=True)
    conclusion_assessment = Column(String(2), nullable=True) # used for period 2007
    conclusion_assessment_prev = Column(String(3), nullable=True) # used for period 2013
    conclusion_assessment_trend_prev = Column(String(20), nullable=True) # used for period 2013
    backcasted_2007 = Column(String(4), nullable=True) # used for period 2013
    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )


restricted_species_2013 = Table(
    'restricted_species_2013',
    metadata,
    Column('eu_country_code', String(2), nullable=False),
    Column('speciescode', String(20), nullable=False),
)


db_manager = Manager()


@db_manager.option('alembic_args', nargs=argparse.REMAINDER)
def alembic(alembic_args):
    from alembic.config import CommandLine
    CommandLine().main(argv=alembic_args)


@db_manager.command
def revision(message=None):
    if message is None:
        message = raw_input('revision name: ')
    return alembic(['revision', '--autogenerate', '-m', message])


@db_manager.command
def upgrade(revision='head'):
    return alembic(['upgrade', revision])


@db_manager.command
def downgrade(revision):
    return alembic(['downgrade', revision])


def get_fixture_objects(file):
    with open(file) as f:
        import json
        return json.loads(f.read())


@db_manager.command
def loaddata(fixture):
    session = db.session
    if not os.path.isfile(fixture):
        print("Please provide a fixture file name")
    else:
        objects = get_fixture_objects(fixture)
        for object in objects:
            filter_fields = object['filter_fields'].split(",")
            kwargs = {}
            for filter_field in filter_fields:
                kwargs.update({filter_field: object['fields'][filter_field]})
            database_objects = eval(object['model']).query.filter_by(**kwargs)
            if not database_objects.first():
                session.add(eval(object['model'])(**object['fields']))
                session.commit()
            else:
                for database_object in database_objects:
                    for (field, value) in object['fields'].iteritems():
                        setattr(database_object, field, value)
                    session.add(database_object)
        session.commit()


@db_manager.command
def dumpdata(model):
    thismodule = sys.modules[__name__]
    base_class = getattr(thismodule, model)

    relationship_fields = [
        rfield for rfield, _ in inspect(base_class).relationships.items()]
    model_fields = [
        field for field in inspect(base_class).attrs.keys() if field not in relationship_fields]

    objects = []
    primary_keys = []

    for field in model_fields:
        value = getattr(inspect(base_class).attrs, field)

        if value.columns[0].primary_key:
            primary_keys.append(field)
    entries = base_class.query.all()
    for entry in entries:
        kwargs = {
            "model": model,
            "filter_fields": ",".join(primary_keys),
            "fields": {}
        }

        for field in model_fields:
            value = getattr(entry, field)

            if type(value) == datetime:
                value = value.isoformat()

            kwargs["fields"][field] = value

        for rfield in relationship_fields:
            class_field = getattr(entry, rfield)

            if isinstance(class_field, sqlalchemy.orm.collections.InstrumentedList):
                kwargs["fields"][rfield] = []
                for subfield in class_field:
                    kwargs["fields"][rfield].append(subfield.id)
            else:
                try:
                    kwargs["fields"][rfield] = class_field.id
                except AttributeError:
                    pass

        app_json = json.dumps(kwargs)
        objects.append(app_json)

    json_dir = os.path.abspath(os.path.dirname('manage.py'))
    json_name = model + '.json'

    with open(os.path.join(json_dir, json_name), 'w') as f:
        f.write('[' + ','.join(objects) + ']')
