# coding=utf-8
from flask_wtf import Form as Form_base
from wtforms import SelectField, TextField, TextAreaField, DateField
from wtforms.validators import Optional, ValidationError
from art17.models import (
    Dataset,
    EtcDicMethod,
    EtcDicConclusion,
    EtcDicPopulationUnit,
    EtcDataSpeciesRegion,
    EtcDataHabitattypeRegion,
)
from art17.utils import validate_field

EMPTY_FORM = "Please fill at least one field"
NOT_NUMERIC_VALUES = (
    "Only numeric values with not more than two decimals are accepted!"
)
METH_CONCL_MANDATORY = "At least one method and conclusion must be filled!"
METH_CONCL_PAIR_MANDATORY = "You cannot add a conclusion without a method, " \
    "nor a method without a conclusion"
INVALID_MS_REGION_PAIR = "Please select an MS country code that is available " \
    "for the selected region"

NATURE_CHOICES = [('yes', 'yes'), ('no', 'no'), ('nc', 'nc')]
CONTRIB_METHODS = [
    ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'),
]
CONTRIB_TYPE = [
    ('+', '+'), ('-', '-'), ('=', '='), ('x', 'x')
]
CONCL_TYPE = [
    ('+', '+'), ('-', '-'), ('0', '0'), ('x', 'x')
]
ZERO_METHODS = [('00', '00'), ('0', '0')]


def all_fields(form):
    for field in form:
        if hasattr(field, 'form'):
            for subfield in all_fields(field.form):
                yield subfield
        else:
            yield field


def numeric_validation(form, field):
    """ Default validation in previous app
    """
    if not validate_field(field.data):
        raise ValidationError(NOT_NUMERIC_VALUES)


def species_ms_validator(form, field):
    species_record = (
        EtcDataSpeciesRegion.query
        .filter_by(
            eu_country_code=field.data, region=form.region.data,
            subject=form.kwargs['subject'],
            dataset_id=form.kwargs['period'])
        .all())
    if not species_record:
        raise ValidationError(INVALID_MS_REGION_PAIR)


def habitat_ms_validator(form, field):
    habitat_record = (
        EtcDataHabitattypeRegion.query
        .filter_by(
            eu_country_code=field.data, region=form.region.data,
            subject=form.kwargs['subject'],
            dataset_id=form.kwargs['period'])
        .all())
    if not habitat_record:
        raise ValidationError(INVALID_MS_REGION_PAIR)


class OptionalSelectField(SelectField):

    def __init__(self, validators=None, default=None, **kwargs):
        validators = validators or [Optional()]
        default = default or ''
        super(OptionalSelectField, self).__init__(validators=validators,
                                                  default=default, **kwargs)


class Form(Form_base):
    def validate(self, **kwargs):
        if not super(Form, self).validate():
            return False

        return self.custom_validate(**kwargs)

    def custom_validate(self, **kwargs):
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


class _OptionsBase(object):

    def get_method_options(self, methods):
        return [
            (a, b)
            for (a, b) in methods
            if not a or a.startswith('1') or (a.startswith('2') and a !=
                                              self.EXCLUDE2)
        ]

    def get_sf_options(self, methods):
        return [
            (a, b)
            for (a, b) in methods
            if not a or (a.startswith('2') and a != self.EXCLUDE2) or a == '1'
        ]

    def get_assesm_options(self, methods):
        return [
            (a, b)
            for (a, b) in methods
            if not a or (a.startswith('3') and a != self.EXCLUDE3) or a == 'MTX'
        ]

    def filter_conclusions(self, conclusions):
        output = []
        for conclusion, value in conclusions:
            if conclusion.strip() == 'XU':
                continue
            elif not conclusion.endswith('?') and not conclusion == 'NA':
                output.append((conclusion, value))
        return output


class OptionsBaseSpecies(_OptionsBase):

    EXCLUDE2 = '2XA'
    EXCLUDE3 = '3XA'


class OptionsBaseHabitat(_OptionsBase):

    EXCLUDE2 = '2XP'
    EXCLUDE3 = '3XP'


class SummaryFormMixin(object):

    def setup_choices(self, dataset_id):
        pass

    def all_errors(self):
        errors = []
        for field_name, field_errors in self.errors.iteritems():
            errors.extend(field_errors)
        errors = set(errors)
        text = '<ul>'
        for error in errors:
            text += '<li>' + error + '</li>'
        text += '</ul>'
        return text


class SummaryManualFormSpecies(Form, OptionsBaseSpecies, SummaryFormMixin):

    region = SelectField(default='')

    range_surface_area = TextField(default=None,
                                   validators=[numeric_validation])
    method_range = OptionalSelectField()
    conclusion_range = OptionalSelectField()
    range_trend = OptionalSelectField()
    complementary_favourable_range = TextField()

    population_size = TextField(validators=[numeric_validation])
    population_size_unit = OptionalSelectField()
    method_population = OptionalSelectField()
    conclusion_population = OptionalSelectField()
    population_trend = OptionalSelectField()
    complementary_favourable_population = TextField()

    habitat_surface_area = TextField(validators=[numeric_validation])
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
        #trends = [a[0] for a in EtcDicTrend.all(dataset_id) if a[0]]
        #trends = empty + zip(trends, trends)
        trends = empty + CONCL_TYPE
        units = [a[0] for a in EtcDicPopulationUnit.all(dataset_id) if a[0]]
        units = empty + zip(units, units)

        self.region.choices = empty

        self.method_range.choices = (
            ZERO_METHODS + self.get_method_options(methods)
        )
        self.method_population.choices = (
            ZERO_METHODS + self.get_method_options(methods)
        )
        self.method_habitat.choices = (
            ZERO_METHODS + self.get_sf_options(methods)
        )

        self.method_future.choices = ZERO_METHODS + self.get_sf_options(methods)
        self.method_assessment.choices = self.get_assesm_options(methods)
        self.method_target1.choices = empty + CONTRIB_METHODS

        for f in (self.range_trend, self.population_trend, self.habitat_trend):
            f.choices = trends
        for f in (self.conclusion_range, self.conclusion_population,
                  self.conclusion_habitat, self.conclusion_future,
                  self.conclusion_assessment, self.conclusion_assessment_prev):
            f.choices = conclusions
        self.conclusion_assessment_change.choices = empty + NATURE_CHOICES
        self.population_size_unit.choices = units
        self.conclusion_assessment_trend.choices = empty + CONTRIB_TYPE
        self.conclusion_target1.choices = empty + CONTRIB_TYPE

    def custom_validate(self, **kwargs):
        excluded = [self.region]
        if hasattr(self, 'MS'):
            excluded.append(self.MS)
        fields = [f for f in all_fields(self) if f not in excluded]
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

        return not self.errors


class SummaryManualFormSpeciesSTA(SummaryManualFormSpecies):

    MS = SelectField(default='', validators=[Optional(), species_ms_validator])


class SummaryManualFormHabitat(Form, OptionsBaseHabitat, SummaryFormMixin):

    region = SelectField()

    range_surface_area = TextField(validators=[numeric_validation])
    method_range = OptionalSelectField()
    conclusion_range = OptionalSelectField()
    range_trend = OptionalSelectField()
    range_yearly_magnitude = TextField()
    complementary_favourable_range = TextField()

    coverage_surface_area = TextField(validators=[numeric_validation])
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
        #trends = [a[0] for a in EtcDicTrend.all(dataset_id) if a[0]]
        #trends = empty + zip(trends, trends)
        trends = empty + CONCL_TYPE

        self.region.choices = empty

        self.method_range.choices = (
            ZERO_METHODS + self.get_method_options(methods)
        )
        self.method_area.choices = (
            ZERO_METHODS + self.get_method_options(methods)
        )

        self.method_structure.choices = self.get_sf_options(methods)
        self.method_future.choices = ZERO_METHODS + self.get_sf_options(methods)
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
        self.conclusion_assessment_trend.choices = empty + CONTRIB_TYPE
        self.conclusion_target1.choices = empty + CONTRIB_TYPE

    def custom_validate(self, **kwargs):
        excluded = [self.region]
        if hasattr(self, 'MS'):
            excluded.append(self.MS)
        fields = [f for f in all_fields(self) if f not in excluded]
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

        return not self.errors


class SummaryManualFormHabitatSTA(SummaryManualFormHabitat):

    MS = SelectField(default='', validators=[Optional(), habitat_ms_validator])


class SummaryManualFormSpeciesRef(Form, SummaryFormMixin):

    region = SelectField()

    complementary_favourable_range = TextField()
    complementary_favourable_population = TextField()


class SummaryManualFormSpeciesRefSTA(SummaryManualFormSpeciesRef):

    MS = SelectField(default='', validators=[Optional(), species_ms_validator])


class SummaryManualFormHabitatRef(Form, SummaryFormMixin):

    region = SelectField()

    complementary_favourable_range = TextField()
    complementary_favourable_area = TextField()


class SummaryManualFormHabitatRefSTA(SummaryManualFormHabitatRef):

    MS = SelectField(default='', validators=[Optional(), habitat_ms_validator])


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
