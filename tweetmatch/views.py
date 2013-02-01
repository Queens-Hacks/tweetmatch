# -*- coding: utf-8 -*-
"""
    tweetmatch.views
    ~~~~~~~~~~~~~~~~~

    Blah blah blah

    :copyright: (c) 2013 by Queen's Haxx.
    :license: MIT, see the license file for more details.
"""


import random
from flask import render_template
from tweetmatch import app
from tweetmatch.models import Tweeter, Tweet


@app.route('/')
@app.route('/challenge')
def hello(challenge=None):
    tweet = Tweet.query[random.randrange(Tweet.query.count())]
    impostor = Tweeter.query[random.randrange(Tweeter.query.count())]
    suspects = [tweet.user, impostor]
    random.shuffle(suspects)
    challenge = {
        'id': 1,
        'tweet': tweet,
        'suspects': suspects,
    }
    return render_template('home.html', challenge=challenge)


@app.route('/challenge/<int:challenge_id>')
@app.route('/challenge/<int:challenge_id>/<challenge_slug>')
def challenge(challenge_id, challenge_slug=None):
    return 'hey'


@app.route('/account')
def me():
    return 'you'


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
