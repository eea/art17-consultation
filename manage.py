#!/usr/bin/env python

import logging
from art17.app import create_app, create_manager

app = create_app()


def main():
    logging.basicConfig(loglevel=logging.DEBUG)
    logging.getLogger('alembic').setLevel(logging.INFO)
    manager = create_manager(app)
    manager.run()


if __name__ == "__main__":
    main()
