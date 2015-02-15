#!/usr/bin/env python
from flask.ext.script import Manager
from flask.ext.script.commands import ShowUrls
from flask.ext.migrate import Migrate, MigrateCommand

from app import app, db
from app.modules.auth.models import User

@MigrateCommand.command
def sampledata(output=True):
    """Populate the database with some sample data"""
    db.create_all()
    user = User(name="Administrator", username="admin", email="admin@example.com", password="1234")
    if output:
        print(user)
    db.session.add(user)
    db.session.commit()

@MigrateCommand.command
def dropall():
    """Drop all database tables"""
    db.drop_all()

def main():
    migrate = Migrate(app, db)
    
    manager = Manager(app)
    manager.add_command('showurls', ShowUrls)
    manager.add_command('db', MigrateCommand)

    manager.run()

if __name__ == "__main__":
    main()
