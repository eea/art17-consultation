import click
import json
import os
import sys

from datetime import datetime
from flask.cli import AppGroup
from sqlalchemy import inspect
from sqlalchemy.ext.hybrid import hybrid_property

from art17 import models
dumpdata = AppGroup("dumpdata")

@dumpdata.command("run")
@click.option("-m", "--model", "model")
def run(**kwargs):
    model = kwargs["model"]
    thismodule = sys.modules[__name__]
    base_class = getattr(models, model)

    relationship_fields = [
        rfield for rfield, _ in inspect(base_class).relationships.items()
    ]
    model_fields = [
        field
        for field in inspect(base_class).attrs.keys()
        if field not in relationship_fields
    ]

    objects = []
    primary_keys = []

    for field in model_fields:
        value = getattr(inspect(base_class).attrs, field)

        if value.columns[0].primary_key:
            primary_keys.append(field)
    entries = base_class.query.all()
    for entry in entries:
        kwargs = {
            "model": model,
            "filter_fields": ",".join(primary_keys),
            "fields": {},
        }

        for field in model_fields:
            value = getattr(entry, field)

            if type(value) == datetime:
                value = value.isoformat()

            kwargs["fields"][field] = value

        for rfield in relationship_fields:
            class_field = getattr(entry, rfield)

            if isinstance(class_field, sqlalchemy.orm.collections.InstrumentedList):
                kwargs["fields"][rfield] = []
                for subfield in class_field:
                    kwargs["fields"][rfield].append(subfield.id)
            else:
                try:
                    kwargs["fields"][rfield] = class_field.id
                except AttributeError:
                    pass

        app_json = json.dumps(kwargs)
        objects.append(app_json)

    json_dir = os.path.abspath(os.path.dirname("manage.py"))
    json_name = model + ".json"

    with open(os.path.join(json_dir, json_name), "w") as f:
        f.write("[" + ",".join(objects) + "]")




