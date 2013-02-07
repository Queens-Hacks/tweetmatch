# -*- coding: utf-8 -*-
"""
    tweetmatch.views
    ~~~~~~~~~~~~~~~~~

    Blah blah blah

    :copyright: (c) 2013 by Queen's Haxx.
    :license: MIT, see the license file for more details.
"""


import random
import logging
from flask import render_template, session, redirect, url_for, request, flash
from flask.ext.login import login_required, current_user, logout_user
from tweetmatch import app
from tweetmatch.logins import login_manager
from tweetmatch.twitter import twitter, get_lists, load_timeline_tweets
from tweetmatch.models import db, TwitterUser, Tweeter, Tweet, Challenge, Guess


def get_challenge(challenge_id=None):
    if challenge_id:
        return Challenge.query.get(challenge_id)

    tweet = Tweet.query[random.randrange(Tweet.query.count())]
    
    impostor = tweet.user
    while tweet.user is impostor:
        impostor = Tweeter.query[random.randrange(Tweeter.query.count())]

    challenge = Challenge.query.filter_by(tweet_id=tweet.id,
                                          impostor_id=impostor.id).first()
    if not challenge:
        challenge = Challenge(tweet, impostor)
        db.session.add(challenge)
        db.session.commit()

    return challenge


@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        lastchallenge = Challenge.query.get(session['last_challenge_id'])
        if not lastchallenge:
            flash('ERRRRRR')
        else:
            accuse = Tweeter.query.get(request.form['suspect'])
            if not accuse:
                flash('ERRRRRRRRRRRRRRRRRRR')
            else:
                guess = Guess(current_user, lastchallenge, accuse)
                db.session.add(guess)
                db.session.commit()

                correct = guess.judge()
                if correct:
                    session['streak'] += 1
                    if session['streak'] > 1:
                        flash(app.character.guess_streak.format(
                                                            session['streak']))
                    else:
                        flash(app.character.guess_right)
                else:
                    session['streak'] = 0
                    flash(app.character.guess_wrong)

    try:
        challenge = get_challenge()
        return redirect(url_for('vs', challenge_id=challenge.id,
                                challenge_slug=challenge.slug()))
    except ValueError as e:
        logging.error(e)
        return '<a href="{}">{}</a>'.format(url_for('moar'), 'login/load')


@login_manager.unauthorized_handler
@app.route('/login')
def login():
    """Log the user in with twitter
    See tweetmatch.twitter for the login handler, which calls login.login_user
    """
    session.clear()
    session['streak'] = 0
    return twitter.authorize(callback=url_for('oauth_authorized'))


@app.route('/logout')
def logout():
    session.clear()
    logout_user()
    flash(app.character.logout)
    return redirect(request.args.get('next') or request.referrer or '/')


@app.route('/vs/<int:challenge_id>')
@app.route('/vs/<int:challenge_id>/<challenge_slug>')
def vs(challenge_id, challenge_slug=None):
    challenge = Challenge.query.get(challenge_id)
    if not challenge:
        return redirect(url_for('hello')) # WARNING infinite redirect possible?
    session['last_challenge_id'] = challenge.id
    return render_template('home.html', challenge=challenge)


@app.route('/load-tweets')
@login_required
def moar():
    load_timeline_tweets()
    return redirect(request.args.get('next') or request.referrer or '/')


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

    guesses_query = Guess.query.filter(Guess.user == current_user)
    total_guesses = guesses_query.count()
    correct_guesses = sum([1 for g in guesses_query.all() if
        g.challenge.tweet.user is g.charges])
    guesses = {'total': total_guesses, 'correct': correct_guesses}

    return render_template('account.html', lists=lists,
        current_list=current_list, guesses=guesses)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.errorhandler(503)
def no_db(error):
    if app.config['DEBUG']:
        return "Couldn't connect to the db. Did you run manage.py creatdb?"
    else:
        return render_template('server_error.html'), 503
