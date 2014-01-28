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

    reg_code = 'ALP'
    reg_name = 'Alpine'


class EtcDicHdHabitat(SQLAlchemyModelFactory):

    FACTORY_FOR = models.EtcDicHdHabitat
    FACTORY_SESSION = models.db.session

    dataset_id = 1
    habcode = 1110
    group = 'coastals habitat'
    priority = 0
    name = 'Sandbanks which are slightly covered by sea water all the time'


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
