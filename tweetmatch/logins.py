# -*- coding: utf-8 -*-
"""
    tweetmatch.logins
    ~~~~~~~~~~~~~~~~~

    manage all the user stuff in one place
    http://packages.python.org/Flask-Login

    :copyright: (c) 2013 by Queen's Haxx.
    :license: MIT, see the license file for more details.
"""

from flask.ext.login import LoginManager
from tweetmatch import app
from tweetmatch.models import TwitterUser


login_manager = LoginManager()
login_manager.setup_app(app)


@login_manager.user_loader
def load_user(userid):
    return TwitterUser.query.get(userid)

