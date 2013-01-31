# -*- coding: utf-8 -*-
"""
    manage
    ~~~~~~

    Basic management stuff, like run, create_db, …
    http://flask-script.readthedocs.org/en/latest/

    Simple Packages pattern:
    http://flask.pocoo.org/docs/patterns/packages/#simple-packages

    :copyright: (c) 2013 by Queen's Haxx.
    :license: MIT, see the license file for more details.
"""


import logging

try:
    import imp
    imp.load_source('activate_this', 'venv/bin/activate_this.py')
except IOError:
    logging.warn('could not source virtualenv venv')
from flask.ext.script import Server, Manager

#from flask.ext.assets import ManageAssets
from tweetmatch import app


manager = Manager(app)


#manager.add_command('assets', ManageAssets())


@manager.command
def createdb():
    """Initialize the database"""
    from tweetmatch.models import db
    db.create_all()


class DebugServer(Server):
    """Run a local development server"""

    def handle(self, app, *args, **kwargs):
        app.config['DEBUG'] = self.use_debugger
        super(DebugServer, self).handle(app, *args, **kwargs)


server = Server(use_debugger=True)
manager.add_command('runserver', DebugServer(use_debugger=True))


@manager.command
def runproduction():
    """Run on production"""
    app.run()


if __name__ == '__main__':
    manager.run()
