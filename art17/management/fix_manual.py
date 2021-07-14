from art17 import models

from flask.cli import AppGroup
from art17 import models

fix_manual = AppGroup('fix_manual')

def translation(value):
    if value == 'n':
        return 'nong'
    if value == 'nc':
        return 'nc'
    if value == 'g':
        return 'gen'
    return ''

@fix_manual.command("run")
def run(**kwargs):
    species = models.SpeciesManualAssessment.query.filter_by(dataset_id=5)
    for specie in species:
        specie.conclusion_assessment_change = translation(specie.conclusion_assessment_change)
        specie.conclusion_assessment_trend_change = translation(specie.conclusion_assessment_trend_change)
        models.db.session.add(specie)
        models.db.session.commit()
    habitats = models.HabitattypesManualAssessment.query.filter_by(dataset_id=5)
    for habitat in habitats:
        habitat.conclusion_assessment_change = translation(habitat.conclusion_assessment_change)
        habitat.conclusion_assessment_trend_change = translation(habitat.conclusion_assessment_trend_change)
        models.db.session.add(habitat)
        models.db.session.commit()
