# -*- coding: utf-8 -*-
"""
    tweetmatch.config
    ~~~~~~~~~~~~~~~~~

    Sensible development defaults are defined here, overridden by environment
    variables, if they exist. Heroku likes environmet variables for
    configuration, so this is convenient.

    :copyright: (c) 2013 by Queen's Haxx.
    :license: MIT, see the license file for more details.
"""


import os
import logging
from tweetmatch import app


if str(os.environ.get('DEBUG')).lower() in ['true', 'on', 'yes', 'debug']:
    logging.warning('Debug turned on from envrionment variable!')
    app.config['DEBUG'] = True

# try to import twitter keys
twitter_keys_file = os.path.join('..', app.instance_path)
app.config.from_pyfile(twitter_keys_file, silent=True)
# override with environment config...
environ_twitter_key = os.environ.get('TWITTER_CONSUMER_KEY')
environ_twitter_secret = os.environ.get('TWITTER_CONSUMER_SECRET')
if environ_twitter_key and environ_twitter_secret:
    app.config.update(TWITTER_CONSUMER_KEY=environ_twitter_key,
                      TWITTER_CONSUMER_SECRET=environ_twitter_secret)

app.config.update(
    SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI',
                                           'sqlite:///../dev-db.sqlite3'),
    SECRET_KEY=os.environ.get('SECRET_KEY', 'so secure'),
    HOST=os.environ.get('IP', '127.0.0.1'),
    PORT=os.environ.get('PORT', 5000),
)
