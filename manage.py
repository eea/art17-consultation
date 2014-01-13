#!/usr/bin/env python

from art17.app import create_app, create_manager


app = create_app()
manager = create_manager(app)


if __name__ == "__main__":
    manager.run()
