from pytest import fixture

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
