from datetime import datetime

from factory.alchemy import SQLAlchemyModelFactory

from art17 import models

DATE_FORMAT = "%Y-%m-%d"


class DatasetFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.Dataset
        sqlalchemy_session = models.db.session

    id = 5
    schema = "2018"
    name = "import-from-2006"
    habitat_map_url = ""
    species_map_url = ""
    sensitive_species_map_url = ""


class EtcDataSpeciesRegionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.EtcDataSpeciesRegion
        sqlalchemy_session = models.db.session

    speciescode = 1110
    dataset_id = 5
    country = "AT"
    eu_country_code = "AT"
    delivery = False
    envelope = "http://"
    filename = "filename"
    region = "ALP"


class EtcDicBiogeoregFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.EtcDicBiogeoreg
        sqlalchemy_session = models.db.session

    dataset_id = 5
    reg_code = "ALP"
    reg_name = "Alpine"


class EtcDicHdHabitat(SQLAlchemyModelFactory):
    class Meta:
        model = models.EtcDicHdHabitat
        sqlalchemy_session = models.db.session

    dataset_id = 5
    habcode = 1110
    group = "coastal habitats"
    priority = 0
    name = "Sandbanks which are slightly covered by sea water all the time"
    shortname = "Sandbanks slightly covered by sea water all time"


class EtcDataHabitattypeRegionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.EtcDataHabitattypeRegion
        sqlalchemy_session = models.db.session

    habitatcode = 1110
    dataset_id = 5
    country = "AT2"
    eu_country_code = "AT"
    delivery = False
    envelope = "http://"
    filename = "filename"
    region = "ALP"

    code = 1110


class EtcDicMethodFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.EtcDicMethod
        sqlalchemy_session = models.db.session

    dataset_id = 5
    method = "1"


class SpeciesManualAssessmentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.SpeciesManualAssessment
        sqlalchemy_session = models.db.session

    dataset_id = 5
    assesment_speciesname = "Canis lupus"
    region = "BOR"
    user_id = "someuser"
    MS = "EU27"


class EtcDataSpeciesAutomaticAssessmentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.EtcDataSpeciesAutomaticAssessment
        sqlalchemy_session = models.db.session

    dataset_id = 5


class EtcDataHabitattypeAutomaticAssessmentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.EtcDataHabitattypeAutomaticAssessment
        sqlalchemy_session = models.db.session

    dataset_id = 5


class HabitattypesManualAssessmentsFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.HabitattypesManualAssessment
        sqlalchemy_session = models.db.session

    dataset_id = 5
    habitatcode = "1110"
    region = "MATL"
    user_id = "someuser"
    MS = "EU27"


class WikiFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.Wiki
        sqlalchemy_session = models.db.session

    id = 1
    region_code = ""
    assesment_speciesname = "Canis lupus"
    dataset_id = 5


class WikiChangeFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.WikiChange
        sqlalchemy_session = models.db.session

    id = 1
    wiki_id = 1
    body = "The wolf was the world's most widely distributed mammal."
    editor = "testuser"
    changed = datetime.strptime("10-02-2014 14:22:23", "%d-%m-%Y %H:%M:%S")
    active = 1
    dataset_id = 5


class WikiTrailFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.WikiTrail
        sqlalchemy_session = models.db.session

    id = 1
    region_code = "CON"
    assesment_speciesname = "Canis lupus"
    dataset_id = 5


class WikiTrailChangeFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.WikiTrailChange
        sqlalchemy_session = models.db.session

    id = 1
    wiki_id = 1
    body = "For Poland: present range, population and habitat"
    editor = "testuser"
    changed = datetime.now()
    active = 1
    dataset_id = 5


class WikiCommentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.WikiComment
        sqlalchemy_session = models.db.session

    id = 1
    wiki_id = 1
    comment = "This is a comment"
    author_id = "testuser"
    posted = datetime.now()
    dataset_id = 5


class CommentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.Comment
        sqlalchemy_session = models.db.session

    id = 1
    comment = "This is a comment"
    author_id = "testuser"
    assesment_speciesname = "Canis lupus"
    region = "BOR"
    user_id = "someuser"
    MS = "EU27"
    post_date = datetime.now().strftime(DATE_FORMAT)
    dataset_id = 5


class HabitatCommentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.HabitatComment
        sqlalchemy_session = models.db.session

    id = 1
    comment = "This is a comment"
    author_id = "testuser"
    habitat = "1110"
    region = "MATL"
    user_id = "someuser"
    MS = "EU27"
    post_date = datetime.now().strftime(DATE_FORMAT)
    dataset_id = 5


class EtcDicConclusionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.EtcDicConclusion
        sqlalchemy_session = models.db.session

    order = 1
    conclusion = "FV"
    dataset_id = 5


class EtcDicDecisionFactory(SQLAlchemyModelFactory):
    class Meta:
        model = models.EtcDicDecision
        sqlalchemy_session = models.db.session

    order = 1
    decision = "CO"
    dataset_id = 5
