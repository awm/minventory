#!/usr/bin/env python
from flask.ext.script import Manager
from flask.ext.script.commands import ShowUrls
from flask.ext.migrate import Migrate, MigrateCommand

from app import app, db

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('showurls', ShowUrls)
manager.add_command('db', MigrateCommand)

if __name__ == "__main__":
    manager.run()
