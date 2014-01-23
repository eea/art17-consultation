# coding=utf-8

from flask_wtf import Form as Form_base
from wtforms import SelectField, TextField
from art17.models import (
    Dataset,
    EtcDicMethod,
    EtcDicConclusion,
    EtcDicTrend,
    EtcDicPopulationUnit,
)


def all_fields(form):
    for field in form:
        if hasattr(field, 'form'):
            for subfield in all_fields(field.form):
                yield subfield
        else:
            yield field


class Form(Form_base):
    def validate(self):
        if not super(Form, self).validate():
            return False

        return self.custom_validate()

    def custom_validate(self):
        return True


class CommonFilterForm(Form):

    period = SelectField('Period...')
    group = SelectField('Group...')
    region = SelectField('Bio-region...')

    def __init__(self, *args, **kwargs):
        super(CommonFilterForm, self).__init__(*args, **kwargs)
        self.period.choices = [(d.id, d.name) for d in Dataset.query.all()]


class SummaryFilterForm(CommonFilterForm):

    subject = SelectField('Name...')


class ReportFilterForm(CommonFilterForm):

    country = SelectField('Country...')


class SummaryManualFormSpecies(Form):

    region = SelectField()

    range_surface_area = TextField(default=None)
    method_range = SelectField()
    conclusion_range = SelectField()
    range_trend = SelectField()
    complementary_favourable_range = TextField()

    population_size = TextField()
    population_size_unit = SelectField()
    method_population = SelectField()
    conclusion_population = SelectField()
    population_trend = SelectField()
    complementary_favourable_population = TextField()

    habitat_surface_area = TextField()
    method_habitat = SelectField()
    conclusion_habitat = SelectField()
    habitat_trend = SelectField()
    complementary_suitable_habitat = TextField()

    method_future = SelectField()
    conclusion_future = SelectField()
    method_assessment = SelectField()
    conclusion_assessment = SelectField()
    conclusion_assessment_trend = SelectField()
    conclusion_assessment_change = SelectField()

    method_target1 = SelectField()
    conclusion_target1 = SelectField()

    def __init__(self, *args, **kwargs):
        super(SummaryManualFormSpecies, self).__init__(*args, **kwargs)
        methods = [a[0] for a in EtcDicMethod.all()]
        methods = [('', '')] + zip(methods, methods)
        conclusions = [a[0] for a in EtcDicConclusion.all()]
        conclusions = zip(conclusions, conclusions)  # TODO filter acl
        trends = [a[0] for a in EtcDicTrend.all()]
        trends = zip(trends, trends)
        units = [a[0] for a in EtcDicPopulationUnit.all()]
        units = zip(units, units)

        for f in (self.method_range, self.method_population,
                  self.method_habitat, self.method_future,
                  self.method_assessment, self.method_target1):
            f.choices = methods

        for f in (self.conclusion_range, self.conclusion_population,
                  self.conclusion_habitat, self.conclusion_future,
                  self.conclusion_assessment, self.conclusion_target1):
            f.choices = conclusions

        for f in (self.range_trend, self.population_trend, self.habitat_trend,
                  self.conclusion_assessment_trend,
                  self.conclusion_assessment_change):
            f.choices = trends

        self.population_size_unit.choices = units

    def custom_validate(self):
        fields = [f for f in all_fields(self) if f != self.region]
        empty = [f for f in fields if not f.data]

        if empty and len(empty) == len(fields):
            fields[1].errors.append(u"Please fill at least one field")
            return False

        method_conclusions = [
            (self.method_range, self.conclusion_range),
            (self.method_population, self.conclusion_population),
            (self.method_habitat, self.conclusion_habitat),
            (self.method_future, self.conclusion_future),
            (self.method_assessment, self.conclusion_assessment),
            (self.method_target1, self.conclusion_target1),
        ]
        data = [(bool(m.data), bool(c.data)) for m, c in method_conclusions]
        if (True, False) in data or (False, True) in data:
            fields[1].errors.append(
                u"Both method and conclusion must be filled"
            )
        elif (True, True) not in data:
            fields[1].errors.append(
                u"At least one method and conclusion must be filled"
            )

        return True

    def all_errors(self):
        text = '<ul>'
        for field_name, field_errors in self.errors.iteritems():
            text += '<li>' + ', '.join(field_errors) + '</li>'
        text += '</ul>'
        return text


class SummaryManualFormHabitat(Form):

    region = SelectField()


class ProgressFilterForm(Form):

    period = SelectField('Period...')
    group = SelectField('Group...')
    conclusion = SelectField('Conclusion...')

    def __init__(self, *args, **kwargs):
        super(ProgressFilterForm, self).__init__(*args, **kwargs)
        self.period.choices = [(d.id, d.name) for d in Dataset.query.all()]
