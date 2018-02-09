from flask.ext.script import Manager, Option
from flask.ext.security.script import (
    CreateUserCommand as BaseCreateUserCommand
)

from art17 import models


class ImportGreeceCommand(BaseCreateUserCommand):

    option_list = BaseCreateUserCommand.option_list + (
        Option('-i', '--id', dest='id', default=None),
        Option('-l', '--ldap', dest='is_ldap', action='store_true'),
        Option('-n', '--name', dest='name'),
    )

    def run(self, **kwargs):
        habitatcodes = [
            data.habitatcode for data in
            models.EtcDataHabitattypeAutomaticAssessment.query.all()
            if data.dataset_id == 4
        ]
        for habitatcode in habitatcodes:
            hdhabitat = models.EtcDicHdHabitat.query.filter_by(
                habcode=habitatcode
            ).first()
            if not models.EtcDicHdHabitat.query.filter_by(
                    habcode=hdhabitat.habcode, dataset_id=4).all():
                new_hdhabitat = models.EtcDicHdHabitat(
                    habcode=hdhabitat.habcode,
                    group=hdhabitat.group,
                    priority=hdhabitat.priority,
                    name=hdhabitat.name,
                    shortname=hdhabitat.shortname,
                    annex_I_comments=hdhabitat.annex_I_comments,
                    marine=hdhabitat.marine,
                    dataset_id=4,
                )
                models.db.session.add(new_hdhabitat)
                models.db.session.commit()
import_greece = Manager()
import_greece.add_command('run', ImportGreeceCommand())
