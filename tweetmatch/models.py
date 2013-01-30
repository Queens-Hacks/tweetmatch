# -*- coding: utf-8 -*-
"""
    tweetmatch.models
    ~~~~~~~~~~~~~~~~~

    Persistent storage of objects used by tweetmatch.
    http://packages.python.org/Flask-SQLAlchemy/
    http://docs.sqlalchemy.org/en/rel_0_8/orm/tutorial.html

    :copyright: (c) 2013 by Queen's Haxx.
    :license: MIT, see the license file for more details.
"""

from flask.ext.sqlalchemy import SQLAlchemy
from tweetmatch import app
db = SQLAlchemy(app)


class TwitterUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    twitter_id = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(21))
    # pic = 

    def __init__(self, twitter_id, username, name):
        self.twitter_id = twitter_id
        self.username = username
        self.name = name

    def __repr__(self):
        return '<TwitterUser @{}>'.format(self.username)


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tweet_id = db.Column(db.String(64), unique=True)
    text = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('twitter_user.id'))
    user = db.relationship('TwitterUser',
        backref=db.backref('tweets', lazy='dynamic'))
    # entities =

    def __init__(self, tweet_id, text, timestamp):
        self.tweet_id = tweet_id
        self.text = text
        self.timestamp = timestamp

    def __repr__(self):
        return '<Tweet {:.12}>'.format(self.tweet)

