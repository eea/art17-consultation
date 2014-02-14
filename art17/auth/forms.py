from flask_wtf import Form as Form_base
from wtforms import SelectField, TextField
from wtforms.widgets import HiddenInput
from flask.ext.security.forms import (
    Required,
)
from art17.dataset import IMPORT_SCHEMA
from art17.models import DicCountryCode, Dataset


SCHEMAS = IMPORT_SCHEMA.keys()


class DatasetForm(Form_base):
    name = TextField()
    schema = SelectField(choices=zip(SCHEMAS, SCHEMAS))


class Art17RegisterFormMixin(object):

    name = TextField('Full name',
        validators=[Required("Full name is required")])
    institution = TextField('Institution',
        validators=[Required("Institution name is required")])
    abbrev = TextField('Abbrev.')
    MS = TextField(widget=HiddenInput())
    country_options = SelectField('Member State')
    other_country = TextField('Other country')
    qualification = TextField('Qualification')

    def __init__(self, *args, **kwargs):
        super(Art17RegisterFormMixin, self).__init__(*args, **kwargs)
        dataset = (Dataset.query.order_by(Dataset.id.desc()).first())
        countries = (DicCountryCode.query
            .with_entities(DicCountryCode.codeEU, DicCountryCode.name)
            .filter(DicCountryCode.dataset_id == dataset.id)
            .distinct()
            .order_by(DicCountryCode.name)
            .all())
        self.country_options.choices = countries + [('', 'Other country')]

