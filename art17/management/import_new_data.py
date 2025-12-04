import math

import click
from flask.cli import AppGroup
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.sqltypes import Boolean, Float, Integer

from art17.models import db
import pandas as pd


def get_model(self, name):
    return self.Model._sa_registry._class_registry.get(name, None)


SQLAlchemy.get_model = get_model

import_new_data = AppGroup("import_new_data")


def set_correct_values_for_boolean_fields(data, field):
    if field in data:
        if data[field] in [True, "true", "TRUE", "True", 1, "1"]:
            data[field] = True
        else:
            data[field] = False
    return data


def set_correct_values_for_float_fields(data, field):
    if field in data:
        if data[field] in [math.nan, "nan", "NaN", "NAN", None, ""]:
            data[field] = None
        else:
            try:
                data[field] = float(data[field])
            except ValueError:
                data[field] = None
    return data


def set_correct_values_for_integer_fields(data, field):
    if field in data:
        if data[field] in [math.nan, "nan", "NaN", "NAN", None, ""]:
            data[field] = None
        else:
            try:
                data[field] = int(data[field])
            except ValueError:
                data[field] = None
    return data


def clean_data(model, data):
    # Get the SQLAlchemy field type for each field in the model
    def get_field_type(model, field):
        lower_field = field.lower()
        if hasattr(model, "__table__") and lower_field in model.__table__.columns:
            return type(model.__table__.columns[lower_field].type)
        if hasattr(model, "__mapper__") and field in model.__mapper__.c:
            return type(model.__mapper__.c[field].type)
        return None

    for field in data:
        field_type = get_field_type(model, field)
        if field_type == Boolean:
            set_correct_values_for_boolean_fields(data, field)
        elif field_type == Float:
            set_correct_values_for_float_fields(data, field)
        elif field_type == Integer:
            set_correct_values_for_integer_fields(data, field)
        try:

            if math.isnan(data[field]):
                if type(data[field]) == float or type(data[field]) == int:
                    data[field] = None
                else:
                    data[field] = ""
        except:
            pass


@import_new_data.command("run")
@click.option("-f", "--file", "file")
@click.option("-m", "--model", "model")
@click.option(
    "-s",
    "--sheet",
    "sheet",
    default=0,
    required=False,
    help="Excel sheet name or index",
)
def run(**kwargs):
    """
    Model options:
        EtcDataSpeciesRegion
        EtcDataHabitattypeRegion
        EtcDataSpeciesAutomaticAssessment
        EtcDataHabitattypeAutomaticAssessment
        SpeciesManualAssessment
        HabitattypesManualAssessment
    """
    df = pd.read_excel(kwargs["file"], sheet_name=kwargs["sheet"])
    df = df.where(pd.notnull(df), "")  # Replace all NaN with None
    data = df.to_dict(orient="records")
    model_class = db.get_model(kwargs["model"])

    for data_object in data:
        # Filter data_object to only include keys that are actual model columns
        filtered_data = {k: v for k, v in data_object.items()}
        clean_data(model_class, filtered_data)

        try:
            # Fields to exclude from import
            # Use in development to exclude fields that are causing issues
            # pop_data = []
            # for field in pop_data:
            #     filtered_data.pop(field, None)
            new_object = model_class(**filtered_data)
            db.session.add(new_object)
            db.session.commit()
        except Exception as e:
            print(f"Error: {e}")
            print("Problematic data:")
            for k, v in filtered_data.items():
                print(f"  {k}: {v} ({type(v)})")
            raise
