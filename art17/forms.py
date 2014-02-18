# coding=utf-8

from flask_wtf import Form as Form_base
from wtforms import SelectField, TextField, TextAreaField, DateField
from wtforms.validators import Optional
from art17.models import (
    Dataset,
    EtcDicMethod,
    EtcDicConclusion,
    EtcDicTrend,
    EtcDicPopulationUnit,
)
from art17.utils import validate_field
from art17.auth import current_user

EMPTY_FORM = "Please fill at least one field"
NOT_NUMERIC_VALUES = (
    "Only numeric values with not more than two decimals are accepted!"
)
METH_CONCL_MANDATORY = "At least one method and conclusion must be filled!"
METH_CONCL_PAIR_MANDATORY = "You cannot add a conclusion without a method, " \
    "nor a method without a conclusion"

NATURE_CHOICES = [('yes', 'yes'), ('no', 'no'), ('nc', 'nc')]
CONTRIB_METHODS = [
    ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'),
]
CONTRIB_TYPE = [
    ('+', '+'), ('-', '-'), ('=', '='), ('x', 'x')
]


def all_fields(form):
    for field in form:
        if hasattr(field, 'form'):
            for subfield in all_fields(field.form):
                yield subfield
        else:
            yield field


class OptionalSelectField(SelectField):

    def __init__(self, validators=None, default=None, **kwargs):
        validators = validators or [Optional()]
        default = default or ''
        super(OptionalSelectField, self).__init__(validators=validators,
                                                  default=default, **kwargs)


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


class OptionsBase(object):

    def get_method_options(self, methods):
        return [
            (a, b)
            for (a, b) in methods
            if not a or a.startswith('1') or (a.startswith('2') and a != '2XA')
        ]

    def get_sf_options(self, methods):
        return [
            (a, b)
            for (a, b) in methods
            if not a or (a.startswith('2') and a != '2XA')
        ]

    def get_assesm_options(self, methods):
        return [
            (a, b)
            for (a, b) in methods
            if not a or (a.startswith('3') and a != '3XA') or a == 'MTX'
        ]

    def filter_conclusions(self, conclusions):
        output = []
        for conclusion, value in conclusions:
            if conclusion.strip() == 'XU':
                continue
            elif not conclusion.endswith('?') and not conclusion == 'NA':
                output.append((conclusion, value))
        return output


class SummaryManualFormSpecies(Form, OptionsBase):

    region = SelectField(default='')

    range_surface_area = TextField(default=None)
    method_range = OptionalSelectField()
    conclusion_range = OptionalSelectField()
    range_trend = OptionalSelectField()
    complementary_favourable_range = TextField()

    population_size = TextField()
    population_size_unit = OptionalSelectField()
    method_population = OptionalSelectField()
    conclusion_population = OptionalSelectField()
    population_trend = OptionalSelectField()
    complementary_favourable_population = TextField()

    habitat_surface_area = TextField()
    method_habitat = OptionalSelectField()
    conclusion_habitat = OptionalSelectField()
    habitat_trend = OptionalSelectField()
    complementary_suitable_habitat = TextField()

    method_future = OptionalSelectField()
    conclusion_future = OptionalSelectField()

    method_assessment = OptionalSelectField()
    conclusion_assessment = OptionalSelectField()
    conclusion_assessment_trend = OptionalSelectField()
    conclusion_assessment_prev = OptionalSelectField()
    conclusion_assessment_change = OptionalSelectField()

    method_target1 = OptionalSelectField()
    conclusion_target1 = OptionalSelectField()

    def setup_choices(self, dataset_id):
        empty = [('', '')]
        methods = [a[0] for a in EtcDicMethod.all(dataset_id)]
        methods = empty + zip(methods, methods)
        conclusions = [a[0] for a in EtcDicConclusion.all(dataset_id) if a[0]]
        conclusions = empty + zip(conclusions, conclusions)
        conclusions = self.filter_conclusions(conclusions)
        trends = [a[0] for a in EtcDicTrend.all(dataset_id) if a[0]]
        trends = empty + zip(trends, trends)
        units = [a[0] for a in EtcDicPopulationUnit.all(dataset_id) if a[0]]
        units = empty + zip(units, units)

        self.region.choices = empty

        self.method_range.choices = self.get_method_options(methods)
        self.method_population.choices = self.get_method_options(methods)
        self.method_habitat.choices = self.get_sf_options(methods)
        self.method_future.choices = self.get_sf_options(methods)
        self.method_assessment.choices = self.get_assesm_options(methods)
        self.method_target1.choices = empty + CONTRIB_METHODS

        for f in (self.range_trend, self.population_trend, self.habitat_trend,
                  self.conclusion_assessment_trend):
            f.choices = trends
        for f in (self.conclusion_range, self.conclusion_population,
                  self.conclusion_habitat, self.conclusion_future,
                  self.conclusion_assessment, self.conclusion_assessment_prev):
            f.choices = conclusions
        self.conclusion_assessment_change.choices = empty + NATURE_CHOICES
        self.population_size_unit.choices = units
        self.conclusion_target1.choices = empty + CONTRIB_TYPE

    def custom_validate(self):
        fields = [f for f in all_fields(self) if f != self.region]
        empty = [f for f in fields if not f.data]

        if empty and len(empty) == len(fields):
            fields[1].errors.append(EMPTY_FORM)
            return False

        method_conclusions = [
            (self.method_range, self.conclusion_range),
            (self.method_population, self.conclusion_population),
            (self.method_habitat, self.conclusion_habitat),
            (self.method_future, self.conclusion_future),
            (self.method_assessment, self.conclusion_assessment),
            (self.method_target1, self.conclusion_target1),
        ]
        one = False
        for m, c in method_conclusions:
            mc, cc = m.data, c.data
            if mc and not cc:
                c.errors.append(METH_CONCL_PAIR_MANDATORY)
            elif cc and not mc:
                m.errors.append(METH_CONCL_PAIR_MANDATORY)
            elif mc and cc:
                one = True
        if not one:
            fields[1].errors.append(METH_CONCL_MANDATORY)

        numeric_values = [
            self.range_surface_area, self.complementary_favourable_range,
            # self.range_yearly_magnitude
            self.population_size, self.complementary_favourable_population,
            # self.population_yearly_magnitude
            self.habitat_surface_area, self.complementary_suitable_habitat
        ]
        for f in numeric_values:
            if not validate_field(f.data):
                f.errors.append(NOT_NUMERIC_VALUES)

        return not self.errors

    def all_errors(self):
        text = '<ul>'
        for field_name, field_errors in self.errors.iteritems():
            text += '<li>' + ', '.join(field_errors) + '</li>'
        text += '</ul>'
        return text


class SummaryManualFormHabitat(Form, OptionsBase):

    region = SelectField()

    range_surface_area = TextField()
    method_range = OptionalSelectField()
    conclusion_range = OptionalSelectField()
    range_trend = OptionalSelectField()
    range_yearly_magnitude = TextField()
    complementary_favourable_range = TextField()

    coverage_surface_area = TextField()
    method_area = OptionalSelectField()
    conclusion_area = OptionalSelectField()
    coverage_trend = OptionalSelectField()
    coverage_yearly_magnitude = TextField()
    complementary_favourable_area = TextField()

    method_structure = OptionalSelectField()
    conclusion_structure = OptionalSelectField()

    method_future = OptionalSelectField()
    conclusion_future = OptionalSelectField()

    method_assessment = OptionalSelectField()
    conclusion_assessment = OptionalSelectField()
    conclusion_assessment_trend = OptionalSelectField()
    conclusion_assessment_prev = OptionalSelectField()
    conclusion_assessment_change = OptionalSelectField()

    method_target1 = OptionalSelectField()
    conclusion_target1 = OptionalSelectField()

    def setup_choices(self, dataset_id):
        empty = [('', '')]
        methods = [a[0] for a in EtcDicMethod.all(dataset_id)]
        methods = empty + zip(methods, methods)
        conclusions = [a[0] for a in EtcDicConclusion.all(dataset_id) if a[0]]
        conclusions = empty + zip(conclusions, conclusions)
        conclusions = self.filter_conclusions(conclusions)
        trends = [a[0] for a in EtcDicTrend.all(dataset_id) if a[0]]
        trends = empty + zip(trends, trends)

        self.region.choices = empty

        self.method_range.choices = self.get_method_options(methods)
        self.method_area.choices = self.get_method_options(methods)
        self.method_structure.choices = self.get_sf_options(methods)
        self.method_future.choices = self.get_sf_options(methods)
        self.method_assessment.choices = self.get_assesm_options(methods)
        self.method_target1.choices = empty + CONTRIB_METHODS

        for f in (self.range_trend, self.coverage_trend,
                  self.conclusion_assessment_trend):
            f.choices = trends
        for f in (self.conclusion_range, self.conclusion_area,
                  self.conclusion_structure, self.conclusion_future,
                  self.conclusion_assessment,
                  self.conclusion_assessment_prev):
            f.choices = conclusions
        self.conclusion_assessment_change.choices = empty + NATURE_CHOICES
        self.conclusion_target1.choices = empty + CONTRIB_TYPE

    def custom_validate(self):
        fields = [f for f in all_fields(self) if f != self.region]
        empty = [f for f in fields if not f.data]

        if empty and len(empty) == len(fields):
            fields[1].errors.append(EMPTY_FORM)
            return False

        method_conclusions = [
            (self.method_range, self.conclusion_range),
            (self.method_area, self.conclusion_area),
            (self.method_structure, self.conclusion_structure),
            (self.method_future, self.conclusion_future),
            (self.method_assessment, self.conclusion_assessment),
            (self.method_target1, self.conclusion_target1),
        ]
        one = False
        for m, c in method_conclusions:
            mc, cc = m.data, c.data
            if mc and not cc:
                c.errors.append(METH_CONCL_PAIR_MANDATORY)
            elif cc and not mc:
                m.errors.append(METH_CONCL_PAIR_MANDATORY)
            elif mc and cc:
                one = True
        if not one:
            fields[1].errors.append(METH_CONCL_MANDATORY)

        numeric_values = [
            self.range_surface_area, self.complementary_favourable_range,
            self.coverage_surface_area, self.complementary_favourable_area,
        ]
        for f in numeric_values:
            if not validate_field(f.data):
                f.errors.append(NOT_NUMERIC_VALUES)

        return not self.errors

    def all_errors(self):
        text = '<ul>'
        for field_name, field_errors in self.errors.iteritems():
            text += '<li>' + ', '.join(field_errors) + '</li>'
        text += '</ul>'
        return text


class SummaryManualFormSpeciesRef(Form):

    region = SelectField()

    complementary_favourable_range = TextField()
    complementary_favourable_population = TextField()

    def setup_choices(self, dataset_id):
        pass


class SummaryManualFormHabitatRef(Form):

    region = SelectField()
    
    complementary_favourable_range = TextField()
    complementary_favourable_area = TextField()

    def setup_choices(self, dataset_id):
        pass


class ProgressFilterForm(Form):

    period = SelectField('Period...')
    group = SelectField('Group...')
    conclusion = SelectField('Conclusion...')

    def __init__(self, *args, **kwargs):
        super(ProgressFilterForm, self).__init__(*args, **kwargs)
        self.period.choices = [(d.id, d.name) for d in Dataset.query.all()]


class WikiEditForm(Form):

    text = TextAreaField()


class CommentForm(Form):

    comment = TextAreaField()


class ConfigForm(Form):
    start_date = DateField(label="Start date (YYYY-MM-DD)",
                           validators=[Optional()])
    end_date = DateField(label="End date (YYYY-MM-DD)",
                         validators=[Optional()])
    admin_email = TextField(label="Administrator email (space separated list)",
                            validators=[Optional()])
    default_dataset_id = SelectField(label="Default period")

    def __init__(self, *args, **kwargs):
        super(ConfigForm, self).__init__(*args, **kwargs)
        dataset_qs = Dataset.query.with_entities(Dataset.id, Dataset.name).all()
        self.default_dataset_id.choices = [
            (str(ds_id), name) for ds_id, name in dataset_qs
        ]
