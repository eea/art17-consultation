from flask_wtf import Form
from wtforms import SelectField
from art17.models import Dataset


class SummaryFilterForm(Form):

    period = SelectField('Period...')
    group =  SelectField('Group...')
    subject = SelectField('Name...')
    region = SelectField('Bio-region...')

    def __init__(self, *args, **kwargs):
        super(SummaryFilterForm, self).__init__(*args, **kwargs)
        self.period.choices = [(d.id, d.name) for d in Dataset.query.all()]
