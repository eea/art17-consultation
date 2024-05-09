import click
from flask.cli import AppGroup

from art17 import models

generate_new_period = AppGroup("generate_new_period")


@generate_new_period.command("run")
@click.option("-s", "--schema", "schema")
@click.option("-n", "--name", "name")
def run(**kwargs):

    dataset = models.Dataset.query.filter_by(schema=kwargs["schema"]).first()

    if not dataset:
        dataset = models.Dataset(
            schema=kwargs["schema"],
            name=kwargs["name"],
        )
        models.db.session.add(dataset)
        models.db.session.commit()

    print("Importing EtcDicMethod...")
    etc_dic_methods = models.EtcDicMethod.query.all()
    for method in etc_dic_methods:
        if not models.EtcDicMethod.query.filter_by(
            method=method.method, dataset_id=dataset.id
        ).all():
            new_method = models.EtcDicMethod(
                order=method.order,
                method=method.method,
                details=method.details,
                dataset_id=dataset.id,
            )
            models.db.session.add(new_method)
            models.db.session.commit()

    print("Importing EtcDicBiogeoregs...")
    etc_dic_biogeoregs = models.EtcDicBiogeoreg.query.all()
    for biogeoreg in etc_dic_biogeoregs:
        if not models.EtcDicBiogeoreg.query.filter_by(
            reg_code=biogeoreg.reg_code, dataset_id=dataset.id
        ).all():
            new_biogeoreg = models.EtcDicBiogeoreg(
                reg_code=biogeoreg.reg_code,
                reg_name=biogeoreg.reg_name,
                ordine=biogeoreg.ordine,
                order=biogeoreg.order,
                dataset_id=dataset.id,
            )
            models.db.session.add(new_biogeoreg)
            models.db.session.commit()

    print("Importing EtcDicConclusions...")
    etc_dic_conclusions = models.EtcDicConclusion.query.all()
    for conclusion in etc_dic_conclusions:
        if not models.EtcDicConclusion.query.filter_by(
            conclusion=conclusion.conclusion, dataset_id=dataset.id
        ).all():
            new_conclusion = models.EtcDicConclusion(
                order=conclusion.order,
                conclusion=conclusion.conclusion,
                details=conclusion.details,
                dataset_id=dataset.id,
            )
            models.db.session.add(new_conclusion)
            models.db.session.commit()

    print("Importing EtcDicDecision...")
    etc_dic_decisions = models.EtcDicDecision.query.all()
    for decision in etc_dic_decisions:
        if not models.EtcDicDecision.query.filter_by(
            decision=decision.decision, dataset_id=dataset.id
        ).all():
            new_decision = models.EtcDicDecision(
                order=decision.order,
                decision=decision.decision,
                details=decision.details,
                dataset_id=dataset.id,
            )
            models.db.session.add(new_decision)
            models.db.session.commit()

    print("Importing EtcDicPopulationUnit...")
    etc_dic_population_units = models.EtcDicPopulationUnit.query.all()
    for unit in etc_dic_population_units:
        if not models.EtcDicPopulationUnit.query.filter_by(
            population_units=unit.population_units, dataset_id=dataset.id
        ).all():
            new_unit = models.EtcDicPopulationUnit(
                order=unit.order,
                population_units=unit.population_units,
                details=unit.details,
                code=unit.code,
                dataset_id=dataset.id,
            )
            models.db.session.add(new_unit)
            models.db.session.commit()

    print("Importing EtcDicSpeciesType...")
    etc_dic_species_types = models.EtcDicSpeciesType.query.all()
    for type in etc_dic_species_types:
        if not models.EtcDicSpeciesType.query.filter_by(
            SpeciesTypeID=type.SpeciesTypeID, dataset_id=dataset.id
        ).all():
            new_type = models.EtcDicSpeciesType(
                SpeciesTypeID=type.SpeciesTypeID,
                SpeciesType=type.SpeciesType,
                Assesment=type.Assesment,
                Note=type.Note,
                abbrev=type.abbrev,
                dataset_id=dataset.id,
            )
            models.db.session.add(new_type)
            models.db.session.commit()

    print("Importing EtcDicTrend...")
    etc_dic_trends = models.EtcDicTrend.query.all()
    for trend in etc_dic_trends:
        if not models.EtcDicTrend.query.filter_by(
            id=trend.id, dataset_id=dataset.id
        ).all():
            new_trend = models.EtcDicTrend(
                id=trend.id,
                trend=trend.trend,
                details=trend.details,
                dataset_id=dataset.id,
            )
            models.db.session.add(new_trend)
            models.db.session.commit()

    habitatcodes = [
        data.habitatcode
        for data in models.EtcDataHabitattypeRegion.query.all()
        if data.dataset_id == dataset.id
    ]

    print("Importing EtcDicHdHabitat...")
    for habitatcode in habitatcodes:
        hdhabitat = models.EtcDicHdHabitat.query.filter_by(habcode=habitatcode).first()
        if not models.EtcDicHdHabitat.query.filter_by(
            habcode=hdhabitat.habcode, dataset_id=dataset.id
        ).all():
            new_hdhabitat = models.EtcDicHdHabitat(
                habcode=hdhabitat.habcode,
                group=hdhabitat.group,
                priority=hdhabitat.priority,
                name=hdhabitat.name,
                shortname=hdhabitat.shortname,
                annex_I_comments=hdhabitat.annex_I_comments,
                marine=hdhabitat.marine,
                dataset_id=dataset.id,
            )
            models.db.session.add(new_hdhabitat)
            models.db.session.commit()

    print("Importing DicCountryCode...")
    countries = models.DicCountryCode.query.all()
    for country in countries:
        if not models.DicCountryCode.query.filter_by(
            code=country.code, dataset_id=dataset.id
        ).all():
            new_country = models.DicCountryCode(
                code=country.code,
                codeEU=country.codeEU,
                name=country.name,
                dataset_id=dataset.id,
            )
            models.db.session.add(new_country)
            models.db.session.commit()

    habitatcodes = [
        data.habitatcode
        for data in models.EtcDataHabitattypeRegion.query.all()
        if data.dataset_id == dataset.id
    ]
