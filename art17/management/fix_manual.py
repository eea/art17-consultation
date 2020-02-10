from flask_script import Manager, Option
from flask_security.script import Command

from art17 import models


class FixManualCommand(Command):

    def translation(self, value):
        if value == 'n':
            return 'nong'
        if value == 'nc':
            return 'nc'
        if value == 'g':
            return 'gen'
        return ''

    def run(self, **kwargs):
        species = models.SpeciesManualAssessment.query.filter_by(dataset_id=5)
        for specie in species:
            specie.conclusion_assessment_change = self.translation(specie.conclusion_assessment_change)
            specie.conclusion_assessment_trend_change = self.translation(specie.conclusion_assessment_trend_change)
            models.db.session.add(specie)
            models.db.session.commit()
        habitats = models.HabitattypesManualAssessment.query.filter_by(dataset_id=5)
        for habitat in habitats:
            habitat.conclusion_assessment_change = self.translation(habitat.conclusion_assessment_change)
            habitat.conclusion_assessment_trend_change = self.translation(habitat.conclusion_assessment_trend_change)
            models.db.session.add(habitat)
            models.db.session.commit()


fix_manual = Manager()
fix_manual.add_command('run', FixManualCommand())