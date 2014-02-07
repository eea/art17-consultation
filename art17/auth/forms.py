from flask_wtf import Form as Form_base
from wtforms import SelectField, TextField
from art17.dataset import IMPORT_SCHEMA


SCHEMAS = IMPORT_SCHEMA.keys()


class DatasetForm(Form_base):
    name = TextField()
    schema = SelectField(choices=zip(SCHEMAS, SCHEMAS))
