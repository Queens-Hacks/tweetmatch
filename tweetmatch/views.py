# -*- coding: utf-8 -*-
"""
    tweetmatch.views
    ~~~~~~~~~~~~~~~~~

    Blah blah blah

    :copyright: (c) 2013 by Queen's Haxx.
    :license: MIT, see the license file for more details.
"""


import random
from flask import render_template, session, redirect, url_for, request, flash
from flask.ext.login import login_required, current_user, logout_user
from tweetmatch import app
from tweetmatch.twitter import twitter, get_lists, set_list, load_timeline_tweets
from tweetmatch.models import TwitterUser, Tweeter, Tweet


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


@app.route('/login')
def login():
    """Log the user in with twitter
    See tweetmatch.twitter for the login handler, which calls login.login_user
    """
    return twitter.authorize(callback=url_for('oauth_authorized'))


@app.route('/logout')
def logout():
    session.clear()
    logout_user()
    flash(app.character.logout)
    return redirect(request.args.get('next') or request.referrer or '/')


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
            set_list(None)
        else:
            set_list(request.form['list'])

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
