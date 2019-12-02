from flask_wtf import FlaskForm as Form_base
from wtforms import SelectField, StringField, PasswordField
from wtforms.validators import Optional, InputRequired
from wtforms.widgets import HiddenInput
from flask_security.forms import (
    Required,
)
from art17.dataset import IMPORT_SCHEMA
from art17.models import DicCountryCode, Dataset


SCHEMAS = IMPORT_SCHEMA.keys()


class DatasetForm(Form_base):
    name = StringField()
    schema = SelectField(choices=zip(SCHEMAS, SCHEMAS))
    species_map_url = StringField(label="URL for species map",
                                validators=[Optional()])
    sensitive_species_map_url = StringField(
        label="URL for sensitive species map", validators=[Optional()])
    habitat_map_url = StringField(label="URL for habitat map",
                                validators=[Optional()])


class CustomEmailStringField(StringField):

    def process_formdata(self, valuelist):
        super(CustomEmailStringField, self).process_formdata(valuelist)
        # if comma or semicolon addresses are provided, consider the first one
        if self.data:
            self.data = self.data.replace(',', ' ').replace(';', ' ').split()[0]


class Art17RegisterFormBase(object):

    name = StringField('Full name',
                     validators=[Required("Full name is required")])
    institution = StringField('Institution', validators=[Optional()])
    abbrev = StringField('Abbrev.')
    MS = StringField(widget=HiddenInput())
    country_options = SelectField('Member State')
    other_country = StringField('Other country')
    qualification = StringField('Qualification', validators=[Optional()])

    def __init__(self, *args, **kwargs):
        super(Art17RegisterFormBase, self).__init__(*args, **kwargs)
        dataset = (Dataset.query.order_by(Dataset.id.desc()).first())
        countries = (DicCountryCode.query
                     .with_entities(DicCountryCode.codeEU, DicCountryCode.name)
                     .filter(DicCountryCode.dataset_id == dataset.id)
                     .distinct()
                     .order_by(DicCountryCode.name)
                     .all())
        self.country_options.choices = (
            [('', '')] + countries + [('--', 'Choose another country ...')]
        )
        self.obj = kwargs.get('obj', None)

class LoginForm(Form_base):
    username = StringField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])

    class Meta:
         csrf = True
