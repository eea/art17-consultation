import ConfigParser

from fabric.decorators import task
from fabric.operations import require, run
from fabric.context_managers import cd, prefix
from fabric.api import env

from path import Path


LOCAL_PATH = Path(__file__).abspath().parent
USED_FOR_MSG = """deployment. You need to prefix the task with the location,
    i.e: fab staging deploy."""


def enviroment(location='staging'):
    config = ConfigParser.RawConfigParser()
    config.read(LOCAL_PATH / 'env.ini')
    env.update(config.items(section=location))
    env.sandbox_activate = Path(env.sandbox) / 'bin' / 'activate'
    env.deployment_location = location


@task
def staging():
    enviroment('staging')


@task
def production():
    enviroment('production')


@task
def deploy():
    require('deployment_location', used_for=USED_FOR_MSG)
    require('project_root', provided_by=[enviroment])

    with cd(env.project_root), prefix('source %(sandbox_activate)s' % env):
        run('git pull --rebase')
        run('pip install -r requirements.txt')
        run('python manage.py db upgrade')
        run('supervisorctl -c %(supervisord_conf)s restart flask' % env)
        for doc_type in ('overview', 'user'):
            with cd(Path('docs') / doc_type):
                run('make html')
