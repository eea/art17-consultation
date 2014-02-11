from datetime import datetime
from factory.alchemy import SQLAlchemyModelFactory

from art17 import models


class DatasetFactory(SQLAlchemyModelFactory):

    FACTORY_FOR = models.Dataset
    FACTORY_SESSION = models.db.session

    id = 1
    name = 'import-from-2006'


class EtcDataSpeciesRegionFactory(SQLAlchemyModelFactory):

    FACTORY_FOR = models.EtcDataSpeciesRegion
    FACTORY_SESSION = models.db.session

    dataset_id = 1
    eu_country_code = 'AT'
    delivery = 2
    envelope = 'http://'
    filename = 'filename'
    region = 'ALP'


class EtcDicBiogeoregFactory(SQLAlchemyModelFactory):

    FACTORY_FOR = models.EtcDicBiogeoreg
    FACTORY_SESSION = models.db.session

    dataset_id = 1
    reg_code = 'ALP'
    reg_name = 'Alpine'


class EtcDicHdHabitat(SQLAlchemyModelFactory):

    FACTORY_FOR = models.EtcDicHdHabitat
    FACTORY_SESSION = models.db.session

    dataset_id = 1
    habcode = 1110
    group = 'coastal habitats'
    priority = 0
    name = 'Sandbanks which are slightly covered by sea water all the time'
    shortname = 'Sandbanks slightly covered by sea water all time'


class EtcDataHabitattypeRegionFactory(SQLAlchemyModelFactory):

    FACTORY_FOR = models.EtcDataHabitattypeRegion
    FACTORY_SESSION = models.db.session

    dataset_id = 1
    country = 'AT2'
    eu_country_code = 'AT'
    delivery = 2
    envelope = 'http://'
    filename = 'filename'
    region = 'ALP'

    code = 1110


class EtcDicMethodFactory(SQLAlchemyModelFactory):

    FACTORY_FOR = models.EtcDicMethod
    FACTORY_SESSION = models.db.session

    dataset_id = 1
    method = '1'


class SpeciesManualAssessmentFactory(SQLAlchemyModelFactory):

    FACTORY_FOR = models.SpeciesManualAssessment
    FACTORY_SESSION = models.db.session

    dataset_id = 1


class EtcDataSpeciesAutomaticAssessmentFactory(SQLAlchemyModelFactory):

    FACTORY_FOR = models.EtcDataSpeciesAutomaticAssessment
    FACTORY_SESSION = models.db.session

    dataset_id = 1


class EtcDataHabitattypeAutomaticAssessmentFactory(SQLAlchemyModelFactory):

    FACTORY_FOR = models.EtcDataHabitattypeAutomaticAssessment
    FACTORY_SESSION = models.db.session

    dataset_id = 1


class HabitattypesManualAssessmentsFactory(SQLAlchemyModelFactory):

    FACTORY_FOR = models.HabitattypesManualAssessment
    FACTORY_SESSION = models.db.session

    dataset_id = 1


class WikiFactory(SQLAlchemyModelFactory):

    FACTORY_FOR = models.Wiki
    FACTORY_SESSION = models.db.session

    id = 1
    region_code = ''
    assesment_speciesname = 'Canis lupus'
    dataset_id = 1


class WikiChangeFactory(SQLAlchemyModelFactory):

    FACTORY_FOR = models.WikiChange
    FACTORY_SESSION = models.db.session

    id = 1
    wiki_id = 1
    body = "The wolf was the world's most widely distributed mammal."
    editor = 'testuser'
    changed = datetime.strptime('10-02-2014 14:22:23', '%d-%m-%Y %H:%M:%S')
    active = 1


class WikiTrailFactory(SQLAlchemyModelFactory):

    FACTORY_FOR = models.WikiTrail
    FACTORY_SESSION = models.db.session

    id = 1
    region_code = 'CON'
    assesment_speciesname = 'Canis lupus'
    dataset_id = 1


class WikiTrailChangeFactory(SQLAlchemyModelFactory):

    FACTORY_FOR = models.WikiTrailChange
    FACTORY_SESSION = models.db.session

    id = 1
    wiki_id = 1
    body = 'For Poland: present range, population and habitat'
    editor = 'testuser'
    changed = datetime.strptime('10-02-2014 14:22:23', '%d-%m-%Y %H:%M:%S')
    active = 1


class WikiCommentFactory(SQLAlchemyModelFactory):

    FACTORY_FOR = models.WikiComment
    FACTORY_SESSION = models.db.session

    id = 1
    wiki_id = 1
    comment = 'This is a comment'
    author_id = 'testuser'
    posted = datetime.now()
