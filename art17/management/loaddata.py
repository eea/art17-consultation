import click
import os

from flask.cli import AppGroup


def get_model(self, name):
    return self.Model._decl_class_registry.get(name, None)


loaddata = AppGroup("loaddata")


@loaddata.command("run")
@click.option("-f", "--fixture", "fixture")
def run(**kwargs):
    fixture = kwargs["fixture"]
    session = db.session
    if not os.path.isfile(fixture):
        print("Please provide a fixture file name")
    else:
        objects = get_fixture_objects(fixture)
        for object in objects:
            filter_fields = object["filter_fields"].split(",")
            kwargs = {}
            for filter_field in filter_fields:
                kwargs.update({filter_field: object["fields"][filter_field]})
            database_objects = eval(object["model"]).query.filter_by(**kwargs)
            if not database_objects.first():
                session.add(eval(object["model"])(**object["fields"]))
                session.commit()
            else:
                for database_object in database_objects:
                    for field, value in object["fields"].items():
                        setattr(database_object, field, value)
                    session.add(database_object)
        session.commit()
