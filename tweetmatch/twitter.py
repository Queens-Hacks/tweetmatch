# -*- coding: utf-8 -*-
"""
http://packages.python.org/Flask-OAuth/
"""

import logging
from flask import request, session, redirect, url_for, flash
from flask.ext.oauth import OAuth
from flask.ext.login import login_required, login_user, logout_user, current_user
from tweetmatch import app
from tweetmatch.models import db, TwitterUser, Tweeter, Tweet


twitter = OAuth().remote_app('twitter',
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=app.config['TWITTER_CONSUMER_KEY'],
    consumer_secret=app.config['TWITTER_CONSUMER_SECRET'],
)


def redirect_url():
    return redirect(request.args.get('next') or request.referrer or '/')


@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')


@app.route('/login')
def login():
    return twitter.authorize(callback=url_for('oauth_authorized'))


@app.route('/logout')
def logout():
    session.clear()
    logout_user()
    flash('bye bye :(')
    return redirect_url()


@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('hello')
    if resp is None:
        flash('Could not sign in :(')
        return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )

    user_id = resp['user_id']
    me = TwitterUser.query.get(user_id)
    if me:
        flash('hello again {} :)'.format(me.name))

    else:
        response = twitter.get('users/show.json', data={
            'screen_name': resp['screen_name'],
            'include_entities': False,
        })
        if response.status != 200:
            loggint.warning
            for error in lists.data['errors']:
                logging.error('twitter {}: {}'.format(error['code'],
                                                      error['message']))
            flash('error...')

        me = TwitterUser(
            twitter_id=resp['user_id'],
            username=resp['screen_name'],
            name=response.data['name'],
            photo=response.data['profile_image_url'],
        )
        flash('welcome, {} :)'.format(me.name))
        db.session.add(me)
        db.session.commit()

    login_user(me)

    return redirect_url()


def load_timeline_tweets(from_list_id=None):
    """a user must be authenticated already
    https://dev.twitter.com/docs/api/1.1/get/statuses/home_timeline
    https://dev.twitter.com/docs/api/1.1/get/lists/statuses
    """
    me = current_user
    from_list_id = from_list_id or me.follow_list
    logging.info('gathering {}\'s timeline...', me.name)
    request_data = {
        'count': 200, # 200 is max
        # 'since_id': ...
    }
    if from_list_id:
        request_data.update({
            'list_id': from_list_id,
            'include_rts': False,
        })
        timeline = twitter.get('lists/statuses.json', data=request_data)
    else:
        request_data.update({
            'exclude_replies': True,
        })
        timeline = twitter.get('statuses/home_timeline.json', data=request_data)

    if timeline.status != 200:
        for error in lists.data['errors']:
            logging.error('twitter {}: {}'.format(error['code'],
                                                  error['message']))
        flash('twitter is being mean :(')
        # and do something about it....    

    logging.info('saving new timeline tweets and any new users...')
    num_added = 0
    for tweet_data in timeline.data:
        # first, see if we already have this tweet
        tweet = Tweet.query.get(tweet_data['id_str'])
        if tweet:
            continue

        # new tweet -- do we have its user yet?
        tweeter = Tweeter.query.get(tweet_data['user']['id_str'])
        if not tweeter:
            user_data = tweet_data['user']
            logging.info('new tweeter {}'.format(user_data['screen_name']))

            tweeter = Tweeter(
                id=user_data['id_str'],
                username=user_data['screen_name'],
                name=user_data['name'],
                pic_url=user_data['profile_image_url'],
            )
            db.session.add(tweeter)
            db.session.commit()


        logging.info('new tweet from {}'.format(tweeter.username))
        tweet = Tweet(
            id=tweet_data['id_str'],
            text=tweet_data['text'],
            timestamp=None,
            user=tweeter,
        )
        num_added += 1
        db.session.add(tweet)

    db.session.commit()

    flash('added {} new tweets'.format(num_added))


def get_lists():
    """return a list of lists a user subscribes to.
    and maybe suggest some popular lists...
    https://dev.twitter.com/docs/api/1.1/get/lists/list
    """
    lists = twitter.get('lists/list.json')
    if lists.status != 200:
        for error in lists.data['errors']:
            logging.error('twitter {}: {}'.format(error['code'],
                                                  error['message']))
        flash('twiter is being mean again :(')

    return lists.data


def set_list(list_id):
    """set the logged-in user's twitter list of people to pull tweets from"""
    me = current_user
    if not me:
        logging.error('could not get logged in user')
        flash('um... are you logged in?')

    me.follow_list = list_id
    db.session.add(me)
    db.session.commit()

