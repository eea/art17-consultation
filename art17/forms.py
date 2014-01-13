from flask_wtf import Form
from wtforms import SelectField


class SummaryFilterForm(Form):

    group =  SelectField('Group...')
    species = SelectField('Name...')
    region = SelectField('Bio-region...')
