# WSGI entry point, loaded by uWSGI as "manage:app" (see docker-entrypoint.sh).
# Use "python -m flask" for the command line commands.
from art17.app import create_app

app = create_app()
