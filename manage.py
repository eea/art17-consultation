#!/usr/bin/env python

import logging
from art17.app import create_app, create_cli_commands

app = create_app()

def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('werkzeug').setLevel(logging.INFO)
    logging.getLogger('alembic').setLevel(logging.INFO)
    if app.config.get('DEBUG_SQL'):
        logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    manager = create_cli_commands(app)
    manager.run()


if __name__ == "__main__":
    main()
