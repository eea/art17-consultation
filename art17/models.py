# coding: utf-8
import argparse
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer,\
    LargeBinary, SmallInteger, String, Table, Text, Boolean
from sqlalchemy.dialects.mysql.base import MEDIUMBLOB
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.security import UserMixin, RoleMixin


db = SQLAlchemy()
Base = db.Model
metadata = db.Model.metadata
alembic_ignore_tables = ['species_name', 'species_group', 'habitat_group']


class Dataset(Base):
    __tablename__ = 'datasets'

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(255), nullable=False)
    schema = Column(String(4))


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
    user = Column(String(25), nullable=False)
    MS = Column(String(4), nullable=False, server_default=u"'EU25'")
    comment = Column(String)
    author_id = Column('author', String(25), nullable=False)
    post_date = Column(String(16), nullable=False)
    deleted = Column(Integer)
    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )

    record = relationship(
        'SpeciesManualAssessment',
        primaryjoin=(
            "and_(SpeciesManualAssessment.assesment_speciesname=="
            "Comment.assesment_speciesname,"
            "SpeciesManualAssessment.region==Comment.region,"
            "SpeciesManualAssessment.user_id==Comment.user,"
            "SpeciesManualAssessment.MS==Comment.MS)"),
        foreign_keys=[assesment_speciesname, region, user, MS],
        backref='comments',
    )
    author = relationship(
        'RegisteredUser',
        primaryjoin="Comment.author_id==RegisteredUser.id",
        foreign_keys=author_id,
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

    code = Column(String(2), primary_key=True)
    codeEU = Column(String(2), server_default=u"''")
    name = Column(String(40))

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )


class EtcDataHabitattypeAutomaticAssessment(Base):
    __tablename__ = 'etc_data_habitattype_automatic_assessment'

    assessment_method = Column(String(3), primary_key=True, nullable=False)
    habitatcode = Column(String(4), primary_key=True, nullable=False)
    region = Column(String(4), primary_key=True, nullable=False)
    order = Column(Integer)
    range_surface_area = Column(String(100))
    percentage_range_surface_area = Column(String(100))
    range_trend = Column(String(100))
    range_yearly_magnitude = Column(String(100))
    complementary_favourable_range = Column(String(100))
    coverage_surface_area = Column(String(100))
    percentage_coverage_surface_area = Column(String(100))
    coverage_trend = Column(String(100))
    coverage_yearly_magnitude = Column(String(100))
    complementary_favourable_area = Column(String(100))
    conclusion_range = Column(String(3))
    conclusion_range_gis = Column(String(3))
    conclusion_coverage = Column(String(3))
    conclusion_coverage_gis = Column(String(3))
    percentage_structure = Column(String(100))
    conclusion_structure = Column(String(3))
    percentage_future = Column(String(100))
    conclusion_future = Column(String(3))
    percentage_assessment = Column(String(100))
    conclusion_assessment = Column(String(3))
    percentage_assessment_trend = Column(String(100))
    conclusion_assessment_trend = Column(String(1))
    percentage_assessment_change = Column(String(100))
    conclusion_assessment_change = Column(String(2))
    range_grid_area = Column(String(100))
    percentage_range_grid_area = Column(String(100))
    distribution_grid_area = Column(String(100))
    percentage_distribution_grid_area = Column(String(100))
    assessment_needed = Column(Integer)

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )


class EtcDataHabitattypeRegion(Base):
    __tablename__ = 'etc_data_habitattype_regions'

    country = Column(String(3), primary_key=True, nullable=False)
    eu_country_code = Column(String(2), nullable=False)
    delivery = Column(Integer, nullable=False)
    envelope = Column(String(50), nullable=False)
    filename = Column(String(60), nullable=False)
    region = Column(String(4), primary_key=True, nullable=False)
    region_ms = Column(String(4))
    region_changed = Column(Integer)
    group = Column(String(21))
    annex = Column(String(11))
    annex_I = Column(String(2))
    priority = Column(String(1))
    code = Column(String(4))
    habitatcode = Column(String(4), primary_key=True)
    habitattype_type = Column(String(10))
    habitattype_type_asses = Column(Integer)
    range_surface_area = Column(Float(asdecimal=True))
    range_change_reason = Column(String(150))
    percentage_range_surface_area = Column(Float(asdecimal=True))
    range_trend = Column(String(1))
    range_yearly_magnitude = Column(Float(asdecimal=True))
    complementary_favourable_range_q = Column(String(2))
    complementary_favourable_range = Column(Float(asdecimal=True))
    coverage_surface_area = Column(Float(asdecimal=True))
    coverage_change_reason = Column(String(150))
    percentage_coverage_surface_area = Column(Float(asdecimal=True))
    coverage_trend = Column(String(1))
    coverage_yearly_magnitude = Column(Float(asdecimal=True))
    complementary_favourable_area_q = Column(String(2))
    complementary_favourable_area = Column(Float(asdecimal=True))
    conclusion_range = Column(String(3))
    conclusion_area = Column(String(3))
    conclusion_structure = Column(String(3))
    conclusion_future = Column(String(3))
    conclusion_assessment = Column(String(3))
    conclusion_assessment_trend = Column(String(1))
    conclusion_assessment_prev = Column(String(3))
    conclusion_assessment_change = Column(String(2))
    range_quality = Column(String(13))
    coverage_quality = Column(String(13))
    complementary_other_information = Column(Text)
    complementary_other_information_english = Column(Text)
    range_grid_area = Column(Float(asdecimal=True))
    percentage_range_grid_area = Column(Float(asdecimal=True))
    distribution_grid_area = Column(Float(asdecimal=True))
    percentage_distribution_grid_area = Column(Float(asdecimal=True))

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )
    dataset = relationship(Dataset)

    habitat = relationship(
        'EtcDicHdHabitat',
        primaryjoin='EtcDicHdHabitat.habcode==EtcDataHabitattypeRegion.subject',
        foreign_keys=[habitatcode]
    )

    habitattype_type_details = relationship(
        'EtcDicSpeciesType',
        primaryjoin='EtcDataHabitattypeRegion.habitattype_type==EtcDicSpeciesType.abbrev',
        foreign_keys=habitattype_type,
    )

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
                         server_default=u"'0'")
    pressure = Column(String(3), primary_key=True, nullable=False,
                      server_default=u"''")

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
                         server_default=u"'0'")
    threat = Column(String(3), primary_key=True, nullable=False,
                    server_default=u"''")

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )


class EtcDataSpeciesAutomaticAssessment(Base):
    __tablename__ = 'etc_data_species_automatic_assessment'

    assessment_method = Column(String(3), primary_key=True, nullable=False)
    order = Column(Integer)
    assesment_speciesname = Column(String(60), primary_key=True,
                                   nullable=False)
    region = Column(String(4), primary_key=True, nullable=False)
    range_surface_area = Column(String(100))
    percentage_range_surface_area = Column(String(100))
    range_trend = Column(String(100))
    range_yearly_magnitude = Column(String(100))
    complementary_favourable_range = Column(String(100))
    population_size = Column(String(100))
    percentage_population_mean_size = Column(String(100))
    population_trend = Column(String(100))
    population_yearly_magnitude = Column(String(100))
    complementary_favourable_population = Column(String(100))
    habitat_surface_area = Column(String(100))
    percentage_habitat_surface_area = Column(String(100))
    habitat_trend = Column(String(100))
    complementary_suitable_habitat = Column(String(100))
    percentage_future = Column(String(100))
    conclusion_range = Column(String(3))
    conclusion_range_gis = Column(String(3))
    conclusion_population = Column(String(3))
    conclusion_population_gis = Column(String(3))
    conclusion_habitat = Column(String(3))
    conclusion_habitat_gis = Column(String(3))
    conclusion_future = Column(String(3))
    percentage_assessment = Column(String(100))
    conclusion_assessment = Column(String(3))
    percentage_assessment_trend = Column(String(100))
    conclusion_assessment_trend = Column(String(1))
    percentage_assessment_change = Column(String(100))
    conclusion_assessment_change = Column(String(2))
    range_grid_area = Column(String(100))
    percentage_range_grid_area = Column(String(100))
    distribution_grid_area = Column(String(100))
    percentage_distribution_grid_area = Column(String(100))
    assessment_needed = Column(Integer)

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )


class EtcDataSpeciesRegion(Base):
    __tablename__ = 'etc_data_species_regions'

    country = Column(String(3), primary_key=True, nullable=False)
    eu_country_code = Column(String(2), nullable=False)
    delivery = Column(Integer, nullable=False)
    envelope = Column(String(50), nullable=False)
    filename = Column(String(60), nullable=False)
    region = Column(String(4), primary_key=True, nullable=False)
    region_ms = Column(String(4))
    region_was_changed = Column(Integer)
    group = Column(String(21))
    tax_group = Column(String(20))
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
    assesment_speciesname = Column(String(60))
    assesment_speciesname_changed = Column(Integer)
    grouped_assesment = Column(Integer)
    species_type = Column(String(10))
    species_type_asses = Column(Integer)
    range_surface_area = Column(Float(asdecimal=True))
    range_change_reason = Column(String(150))
    percentage_range_surface_area = Column(Float(asdecimal=True))
    range_trend = Column(String(1))
    range_yearly_magnitude = Column(Float(asdecimal=True))
    complementary_favourable_range_q = Column(String(2))
    complementary_favourable_range = Column(Float(asdecimal=True))
    population_minimum_size = Column(Float(asdecimal=True))
    percentage_population_minimum_size = Column(Float(asdecimal=True))
    population_maximum_size = Column(Float(asdecimal=True))
    percentage_population_maximum_size = Column(Float(asdecimal=True))
    filled_population = Column(String(3))
    population_size_unit = Column(String(6))
    population_units_agreed = Column(String(50))
    population_units_other = Column(String(50))
    population_change_reason = Column(String(150))
    number_of_different_population_units = Column(Integer)
    different_population_percentage = Column(Integer)
    percentage_population_mean_size = Column(Float(asdecimal=True))
    population_trend = Column(String(1))
    population_yearly_magnitude = Column(Float(asdecimal=True))
    complementary_favourable_population_q = Column(String(2))
    complementary_favourable_population = Column(Float(asdecimal=True))
    filled_complementary_favourable_population = Column(String(3))
    habitat_surface_area = Column(Float(asdecimal=True))
    habitat_change_reason = Column(String(150))
    percentage_habitat_surface_area = Column(Float(asdecimal=True))
    habitat_trend = Column(String(1))
    complementary_suitable_habitat = Column(Float(asdecimal=True))
    future_prospects = Column(String(4))
    conclusion_range = Column(String(3))
    conclusion_population = Column(String(3))
    conclusion_habitat = Column(String(3))
    conclusion_future = Column(String(3))
    conclusion_assessment = Column(String(3))
    conclusion_assessment_trend = Column(String(1))
    conclusion_assessment_prev = Column(String(3))
    conclusion_assessment_change = Column(String(2))
    range_quality = Column(String(13))
    population_quality = Column(String(13))
    habitat_quality = Column(String(13))
    complementary_other_information = Column(Text)
    complementary_other_information_english = Column(Text)
    range_grid_area = Column(Float(asdecimal=True))
    percentage_range_grid_area = Column(Float(asdecimal=True))
    distribution_grid_area = Column(Float(asdecimal=True))
    percentage_distribution_grid_area = Column(Float(asdecimal=True))


    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )
    dataset = relationship(Dataset)

    species_type_details = relationship(
        'EtcDicSpeciesType',
        primaryjoin="EtcDataSpeciesRegion.species_type==EtcDicSpeciesType.abbrev",
        foreign_keys=species_type,
    )

    @property
    def is_assesm(self):
        return self.species_type_asses == 0

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
                                server_default=u"'0'")
    assesment_speciesname = Column(String(60), nullable=False)
    pressure = Column(String(3), primary_key=True, nullable=False,
                      server_default=u"''")

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
                                server_default=u"'0'")
    assesment_speciesname = Column(String(60), nullable=False)
    threat = Column(String(3), primary_key=True, nullable=False,
                    server_default=u"''")

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
    def get_region_name(cls, reg_code):
        return (
            cls.query.with_entities(cls.reg_name)
            .filter(cls.reg_code == reg_code)
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
    name = Column(String(155), nullable=False)
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
    method = Column(String(3), primary_key=True)
    details = Column(String(125))

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )

    @classmethod
    def all(cls, dataset_id):
        return (
            cls.query.filter(
                (cls.method.startswith('1') | cls.method.startswith('2')))
            .filter(cls.method != '2XA')
            .filter_by(dataset_id=dataset_id)
            .with_entities(cls.method)
            .order_by(cls.method)
        )


class EtcDicPopulationUnit(Base):
    __tablename__ = 'etc_dic_population_units'

    order = Column(Integer)
    population_units = Column(String(6), primary_key=True)
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
            cls.query.with_entities(cls.population_units)
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
    suspect_value = Column(String(150), nullable=False, server_default=u"''")
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
    suspect_value = Column(String(150), nullable=False, server_default=u"''")
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
    user = Column(String(25), nullable=False)
    MS = Column(String(4), nullable=False, server_default=u"'EU27'")
    comment = Column(String)
    author_id = Column('author', String(25), nullable=False)
    post_date = Column(String(16), nullable=False)
    deleted = Column(Integer)
    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )

    record = relationship(
        'HabitattypesManualAssessment',
        primaryjoin=(
            "and_(HabitattypesManualAssessment.habitatcode=="
            "HabitatComment.habitat,"
            "HabitattypesManualAssessment.region==HabitatComment.region,"
            "HabitattypesManualAssessment.user_id==HabitatComment.user,"
            "HabitattypesManualAssessment.MS==HabitatComment.MS)"),
        foreign_keys=[habitat, region, user, MS],
        backref='comments',
    )
    author = relationship(
        'RegisteredUser',
        primaryjoin="HabitatComment.author_id==RegisteredUser.id",
        foreign_keys=author_id,
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
                server_default=u"'EU27'")
    region = Column(String(4), primary_key=True, nullable=False)
    habitatcode = Column(String(50), primary_key=True, nullable=False)
    range_surface_area = Column(String(23))
    range_trend = Column(String(3))
    range_yearly_magnitude = Column(String(23))
    complementary_favourable_range = Column(String(23))
    coverage_surface_area = Column(String(23))
    coverage_trend = Column(String(3))
    coverage_yearly_magnitude = Column(String(23))
    complementary_favourable_area = Column(String(23))
    method_range = Column(String(3))
    conclusion_range = Column(String(2))
    method_area = Column(String(3))
    conclusion_area = Column(String(2))
    method_structure = Column(String(3))
    conclusion_structure = Column(String(2))
    method_future = Column(String(3))
    conclusion_future = Column(String(2))
    method_assessment = Column(String(3))
    conclusion_assessment = Column(String(2))
    conclusion_assessment_trend = Column(String(1))
    conclusion_assessment_prev = Column(String(3))
    conclusion_assessment_change = Column(String(2))
    method_target1 = Column(String(3))
    conclusion_target1 = Column(String(3))
    user_id = Column('user', String(25), primary_key=True, nullable=False,
                     server_default=u"''")
    last_update = Column(String(16))
    deleted = Column('deleted_record', Integer)
    decision = Column(String(3))
    user_decision_id = Column('user_decision', String(25))
    last_update_decision = Column(String(16))

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

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )

    def comments_count_unread(self, user):
        if not self.comments:
            return 0
        return len(
            db.session.query(HabitatComment.id)
            .join(t_habitat_comments_read)
            .filter(HabitatComment.habitat == self.habitatcode)
            .filter(HabitatComment.region == self.region)
            .filter(HabitatComment.MS == self.MS)
            .filter(HabitatComment.user == self.user_id)
            .filter('habitat_comments_read.reader_user_id="%s"' % user)
            .all()
        )

    @hybrid_property
    def subject(self):
        return self.habitatcode

    @subject.setter
    def subject(self, value):
        self.habitatcode = value


class LuHdHabitat(Base):
    __tablename__ = 'lu_hd_habitats'

    habcode = Column(String(4), primary_key=True)
    group = Column(String(40))
    priority = Column(Integer, nullable=False)
    name = Column(String(155), nullable=False)
    annex_I_comments = Column(String(30))
    marine = Column(Integer)

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )


class PhotoHabitat(Base):
    __tablename__ = 'photo_habitats'

    id = Column(Integer, primary_key=True)
    habitatcode = Column(String(4), nullable=False, server_default=u"''")
    description = Column(String(4096))
    photographer = Column(String(64))
    location = Column(String(64))
    content_type = Column(String(32))
    picture_date = Column(DateTime, nullable=False,
                          server_default=u'CURRENT_TIMESTAMP')
    picture_data = Column(MEDIUMBLOB)
    thumbnail = Column(MEDIUMBLOB)
    user = Column(String(50), nullable=False, server_default=u"''")

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )


class PhotoSpecy(Base):
    __tablename__ = 'photo_species'

    id = Column(Integer, primary_key=True)
    assessment_speciesname = Column(String(60), nullable=False,
                                    server_default=u"''")
    description = Column(String(255))
    photographer = Column(String(64))
    location = Column(String(64))
    karma = Column(Integer, nullable=False, server_default=u"'0'")
    content_type = Column(String(32))
    picture_date = Column(DateTime)
    picture_data = Column(LargeBinary)
    thumbnail = Column(LargeBinary)
    user = Column(String(50), nullable=False, server_default=u"''")

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )


roles_users = db.Table('roles_users',
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
    show_assessment = Column(Integer, nullable=False, server_default=u"'1'")
    active = Column(Boolean)
    confirmed_at = db.Column(db.DateTime())
    waiting_for_activation = db.Column(Boolean, nullable=False, server_default='0')
    is_ldap = db.Column(Boolean, nullable=False, server_default='0')
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic'),
    )
    password = db.Column(String(60))

    def has_role(self, role):
        return role in [r.name for r in self.roles]


class Role(Base, RoleMixin):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))


t_restricted_habitats = Table(
    'restricted_habitats', metadata,
    Column('habitatcode', String(4)),
    Column('eu_country_code', String(2), nullable=False, server_default=u"''"),
    Column('show_data', SmallInteger),
    Column('ext_dataset_id', ForeignKey('datasets.id')),
)


t_restricted_species = Table(
    'restricted_species', metadata,
    Column('assesment_speciesname', String(60), nullable=False,
           server_default=u"''"),
    Column('eu_country_code', String(2), nullable=False, server_default=u"''"),
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

    MS = Column(String(4), primary_key=True, nullable=False,
                server_default=u"'EU25'")
    region = Column(String(4), primary_key=True, nullable=False)
    assesment_speciesname = Column(String(60), primary_key=True,
                                   nullable=False)
    range_surface_area = Column(String(23))
    range_trend = Column(String(3))
    range_yearly_magnitude = Column(String(23))
    complementary_favourable_range = Column(String(23))
    population_size = Column(String(23))
    population_size_unit = Column(String(6))
    population_trend = Column(String(3))
    population_yearly_magnitude = Column(String(23))
    complementary_favourable_population = Column(String(23))
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
    conclusion_future = Column(String(2))
    method_assessment = Column(String(3))
    conclusion_assessment = Column(String(2))
    conclusion_assessment_trend = Column(String(1))
    conclusion_assessment_prev = Column(String(3))
    conclusion_assessment_change = Column(String(2))
    method_target1 = Column(String(3))
    conclusion_target1 = Column(String(3))
    user_id = Column('user', String(25), primary_key=True, nullable=False,
                  server_default=u"''")
    last_update = Column(String(16))
    deleted = Column('deleted_record', Integer)
    decision = Column(String(3))
    user_decision_id = Column('user_decision', String(25))
    last_update_decision = Column(String(16))

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

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )

    def comments_count_unread(self, user):
        if not self.comments:
            return 0
        return len(
            db.session.query(Comment.id)
            .join(t_comments_read)
            .filter(Comment.assesment_speciesname == self.assesment_speciesname)
            .filter(Comment.region == self.region)
            .filter(Comment.MS == self.MS)
            .filter(Comment.user == self.user_id)
            .filter('comments_read.reader_user_id="%s"' % user)
            .all()
        )

    @hybrid_property
    def subject(self):
        return self.assesment_speciesname

    @subject.setter
    def subject(self, value):
        self.assesment_speciesname = value


t_species_name = Table(
    'species_name', metadata,
    Column('priority', String(1)),
    Column('assesment_speciesname', String(60)),
    Column('ext_dataset_id', ForeignKey('datasets.id')),
)


class Wiki(Base):
    __tablename__ = 'wiki'

    id = Column(Integer, primary_key=True, unique=True)
    region = Column(String(4), nullable=False)
    assesment_speciesname = Column(String(60))
    habitatcode = Column(String(4))

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )


class WikiChange(Base):
    __tablename__ = 'wiki_changes'

    id = Column(Integer, primary_key=True)
    wiki_id = Column(ForeignKey('wiki.id'), nullable=False)
    body = Column(String(6000))
    editor = Column(String(60), nullable=False)
    changed = Column(DateTime, nullable=False,
                     server_default=u'CURRENT_TIMESTAMP')
    active = Column(Integer, server_default=u"'0'")

    wiki = relationship(u'Wiki')


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

    wiki = relationship(u'Wiki', backref='comments')

    author = relationship(
        'RegisteredUser',
        primaryjoin="WikiComment.author_id==RegisteredUser.id",
        foreign_keys=author_id,
    )

    readers = relationship("RegisteredUser",
                           secondary=t_wiki_comments_read,
                           backref='read_comments')


class WikiTrail(Base):
    __tablename__ = 'wiki_trail'

    id = Column(Integer, primary_key=True, unique=True)
    region = Column(String(4), nullable=False)
    assesment_speciesname = Column(String(60))
    habitatcode = Column(String(4))

    dataset_id = Column(
        'ext_dataset_id',
        ForeignKey('datasets.id'),
        primary_key=True,
    )


class WikiTrailChange(Base):
    __tablename__ = 'wiki_trail_changes'

    id = Column(Integer, primary_key=True)
    wiki_id = Column(ForeignKey('wiki_trail.id'), nullable=False)
    body = Column(String(6000))
    editor = Column(String(60), nullable=False)
    changed = Column(DateTime, nullable=False,
                     server_default=u'CURRENT_TIMESTAMP')
    active = Column(Integer, server_default=u"'0'")

    wiki = relationship(u'WikiTrail')


class WikiTrailComment(Base):
    __tablename__ = 'wiki_trail_comments'

    id = Column(Integer, primary_key=True)
    wiki_id = Column(ForeignKey('wiki_trail.id'), nullable=False)
    comment = Column(String, nullable=False)
    author = Column(String(60), nullable=False)
    deleted = Column(Integer)
    posted = Column(DateTime, nullable=False,
        server_default=u'CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')

    wiki = relationship(u'WikiTrail')


t_wiki_trail_comments_read = Table(
    'wiki_trail_comments_read', metadata,
    Column('comment_id', ForeignKey('wiki_trail_comments.id')),
    Column('reader_id', String(60))
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
