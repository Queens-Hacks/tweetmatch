# -*- coding: utf-8 -*-
"""
    tweetmatch.views
    ~~~~~~~~~~~~~~~~~

    Blah blah blah

    :copyright: (c) 2013 by Queen's Haxx.
    :license: MIT, see the license file for more details.
"""


import random
from flask import render_template, session, redirect, url_for, request
from flask.ext.login import login_required, current_user
from tweetmatch import app
from tweetmatch.twitter import get_lists, load_timeline_tweets
from tweetmatch.models import db, TwitterUser, Tweeter, Tweet


@app.route('/')
@app.route('/challenge')
def hello(challenge=None):
    try:
        tweet = Tweet.query[random.randrange(Tweet.query.count())]
        impostor = Tweeter.query[random.randrange(Tweeter.query.count())]
        suspects = [tweet.user, impostor]
        random.shuffle(suspects)
    except ValueError:
        # no tweets imported yet
        tweet = 'blah blah blah'
        suspects = ['a', 'b']
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


@app.route('/load-tweets')
@login_required
def moar():
    load_timeline_tweets()
    return redirect(url_for('hello'))




@app.route('/account', methods=['GET', 'POST'])
@login_required
def me():
    if request.method == 'POST' and 'list' in request.form:
        if request.form['list'] == 'none':
            current_user.follow_list = None
        else:
            current_user.follow_list = request.form['list']
        db.session.add(current_user)
        db.session.commit()

    lists = get_lists()
    lists.append({'name': 'don\'t use a list', 'id_str': None})

    current_list_id = current_user.follow_list
    try:
        current_list = [l for l in lists if l['id_str'] == current_list_id][0]
    except IndexError:
        current_list = lists[-1]

    return render_template('account.html', lists=lists, current_list=current_list)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
