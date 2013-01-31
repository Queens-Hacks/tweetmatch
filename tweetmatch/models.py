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


follows = db.Table('follows',
    db.Column('twitter_user_id', db.Integer, db.ForeignKey('twitter_user.id')),
    db.Column('tweeter_id', db.Integer, db.ForeignKey('tweeter.id'))
)


class TwitterUser(db.Model):
    """People who have registered with the site"""
    id = db.Column(db.Integer, primary_key=True)
    twitter_id = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(21))
    pic_url = db.Column(db.String(80))
    # bloom = 
    
    follows = db.relationship('Tweeter', secondary=follows,
        backref=db.backref('followers_here'))

    def __init__(self, twitter_id, username, name):
        self.twitter_id = twitter_id
        self.username = username
        self.name = name

    def __repr__(self):
        return '<TwitterUser @{}>'.format(self.username)


class Tweeter(db.Model):
    """twitter accounts"""
    id = db.Column(db.Integer, primary_key=True)
    twitter_id = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(21))
    pic_url = db.Column(db.String(80))


class Tweet(db.Model):
    """Local databse of collected tweets"""
    id = db.Column(db.Integer, primary_key=True)
    tweet_id = db.Column(db.String(64), unique=True)
    text = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('tweeter.id'))
    user = db.relationship('Tweeter',
        backref=db.backref('tweets', lazy='dynamic'))

    def __init__(self, tweet_id, text, timestamp):
        self.tweet_id = tweet_id
        self.text = text
        self.timestamp = timestamp

    def __repr__(self):
        return '<Tweet {:.12}>'.format(self.tweet)


class Challenge(db.Model):
    """gotta catch em all"""
    id = db.Column(db.Integer, primary_key=True)
    tweet_id = db.Column(db.Integer, db.ForeignKey('tweet.id'))
    tweet = db.relationship('Tweet',
        backref=db.backref('challenges', lazy='dynamic'))
    poser_id = db.Column(db.Integer, db.ForeignKey('tweeter.id'))
    poser = db.relationship('Tweeter',
        backref=db.backref('spoofs', lazy='dynamic'))


class Guess(db.Model):
    """who's the best"""
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Time)
    win = db.Column(db.Boolean)

    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'))
    challenge = db.relationship('Challenge',
        backref=db.backref('guesses', lazy='dynamic'))


