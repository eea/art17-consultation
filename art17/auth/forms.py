from flask_wtf import Form as Form_base
from wtforms import SelectField, TextField, PasswordField
from wtforms.validators import Optional, InputRequired
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


class CustomEmailTextField(TextField):

    def process_formdata(self, valuelist):
        super(CustomEmailTextField, self).process_formdata(valuelist)
        # if comma or semicolon addresses are provided, consider the first one
        if self.data:
            self.data = self.data.replace(',', ' ').replace(';', ' ').split()[0]


class Art17RegisterFormBase(object):

    name = TextField('Full name',
                     validators=[Required("Full name is required")])
    institution = TextField('Institution', validators=[Optional()])
    abbrev = TextField('Abbrev.')
    MS = TextField(widget=HiddenInput())
    country_options = SelectField('Member State')
    other_country = TextField('Other country')
    qualification = TextField('Qualification', validators=[Optional()])

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
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
