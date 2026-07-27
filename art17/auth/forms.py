from flask_wtf import FlaskForm as Form_base
from wtforms import PasswordField, SelectField, StringField
from wtforms.validators import Optional, DataRequired, Length
from wtforms.widgets import HiddenInput

from art17.dataset import IMPORT_SCHEMA
from art17.models import Dataset, DicCountryCode

SCHEMAS = IMPORT_SCHEMA.keys()


class DatasetForm(Form_base):
    name = StringField()
    schema = SelectField(choices=zip(SCHEMAS, SCHEMAS))
    species_map_url = StringField(label="URL for species map", validators=[Optional()])
    sensitive_species_map_url = StringField(
        label="URL for sensitive species map", validators=[Optional()]
    )
    habitat_map_url = StringField(label="URL for habitat map", validators=[Optional()])


class CustomEmailStringField(StringField):
    def process_formdata(self, valuelist):
        super(CustomEmailStringField, self).process_formdata(valuelist)
        # if comma or semicolon addresses are provided, consider the first one
        if self.data:
            self.data = self.data.replace(",", " ").replace(";", " ").split()[0]


class Art17RegisterFormBase(object):

    name = StringField(
        "Full name",
        validators=[
            DataRequired("Full name is required"),
            Length(max=255, message="Full name cannot exceed 255 characters"),
        ],
    )
    institution = StringField(
        "Institution",
        validators=[
            Optional(),
            Length(max=45, message="Institution cannot exceed 45 characters"),
        ],
    )
    abbrev = StringField("Abbrev.")
    MS = StringField(widget=HiddenInput())
    country_options = SelectField("Member State")
    other_country = StringField("Other country")
    qualification = StringField("Qualification", validators=[Optional()])

    def __init__(self, *args, **kwargs):
        super(Art17RegisterFormBase, self).__init__(*args, **kwargs)
        dataset = Dataset.query.order_by(Dataset.id.desc()).first()
        countries = (
            DicCountryCode.query.with_entities(
                DicCountryCode.codeEU, DicCountryCode.name
            )
            .filter(DicCountryCode.dataset_id == dataset.id)
            .distinct()
            .order_by(DicCountryCode.name)
            .all()
        )
        self.country_options.choices = (
            [("", "")] + countries + [("--", "Choose another country ...")]
        )
        if hasattr(self, "password"):
            self.password.flags.required = True
        self.obj = kwargs.get("obj", None)


class LoginForm(Form_base):
    username = StringField("Username", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])

    class Meta:
        csrf = True
