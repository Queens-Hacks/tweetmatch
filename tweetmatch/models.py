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


import random
from datetime import datetime
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin
from tweetmatch import app
db = SQLAlchemy(app)


follows = db.Table('follows',
    db.Column('twitter_user_id', db.String(64), db.ForeignKey('twitter_user.id')),
    db.Column('tweeter_id', db.String(64), db.ForeignKey('tweeter.id'))
)


class TwitterUser(db.Model, UserMixin):
    """People who have registered with the site"""
    id = db.Column(db.String(64), primary_key=True) # from twitter
    username = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(21))
    pic_url = db.Column(db.String(250))
    bloom = db.Column(db.Binary(length=2000))
    follow_list = db.Column(db.String(64))
    
    following = db.relationship('Tweeter', secondary=follows,
        backref=db.backref('following_here'))

    def __init__(self, twitter_id, username, name, photo):
        self.id = twitter_id
        self.username = username
        self.name = name
        self.pic_url = photo

    def __repr__(self):
        return '<TwitterUser @{}>'.format(self.username)


class Tweeter(db.Model):
    """twitter accounts"""
    id = db.Column(db.String(64), primary_key=True)
    username = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(21))
    pic_url = db.Column(db.String(250))

    def __init__(self, id, username, name=None, pic_url=None):
        self.id = id
        self.username = username
        self.name = name
        self.pic_url = pic_url

    def __repr__(self):
        return '<Tweeter @{}>'.format(self.username)


class Tweet(db.Model):
    """Local databse of collected tweets"""
    id = db.Column(db.String(64), primary_key=True)
    text = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime)

    user_id = db.Column(db.String(64), db.ForeignKey('tweeter.id'))
    user = db.relationship('Tweeter',
        backref=db.backref('tweets', lazy='dynamic'))

    def __init__(self, id, text, timestamp, user):
        self.id = id
        self.text = text
        self.timestamp = timestamp
        self.user = user

    def __repr__(self):
        return '<Tweet {:.9}...>'.format(self.text)


class Challenge(db.Model):
    """gotta catch em all"""
    id = db.Column(db.Integer, primary_key=True)
    impostor_first = db.Column(db.Boolean(0))
    
    impostor_id = db.Column(db.String(64), db.ForeignKey('tweeter.id'))
    impostor = db.relationship('Tweeter',
        backref=db.backref('impostors', lazy='dynamic'))

    tweet_id = db.Column(db.String(64), db.ForeignKey('tweet.id'))
    tweet = db.relationship('Tweet',
        backref=db.backref('challenges', lazy='dynamic'))

    def __init__(self, tweet, impostor):
        self.tweet = tweet
        self.impostor = impostor
        self.impostor_first = random.choice([True, False])

    def suspects(self):
        if self.impostor_first:
            return (self.impostor, self.tweet.user)
        else:
            return (self.tweet.user, self.impostor)

    def slug(self):
        return '-'.join(s.username.lower() for s in self.suspects())

    def __repr__(self):
        return '<Challenge {}>'.format(self.id)


class Guess(db.Model):
    """who's the best"""
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.String(64), db.ForeignKey('twitter_user.id'))
    user = db.relationship('TwitterUser',
        backref=db.backref('guesses', lazy='dynamic'))

    challenge_id = db.Column(db.Integer, db.ForeignKey('challenge.id'))
    challenge = db.relationship('Challenge',
        backref=db.backref('guesses', lazy='dynamic'))

    tweeter_id = db.Column(db.String(64), db.ForeignKey('tweeter.id'))
    charges = db.relationship('Tweeter',
        backref=db.backref('charges', lazy='dynamic'))

    def __init__(self, user, challenge, charges):
        self.user = user
        self.challenge = challenge
        self.charges = charges

    def judge(self):
        return self.charges is self.challenge.tweet.user

    def __repr__(self):
        return '<Guess for {} by {}>'.format(self.challenge, self.id)


