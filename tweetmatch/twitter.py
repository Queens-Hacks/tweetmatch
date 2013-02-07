# -*- coding: utf-8 -*-
"""
http://packages.python.org/Flask-OAuth/
"""

import logging
from datetime import datetime
from flask import request, session, redirect, url_for, flash
from flask.ext.oauth import OAuth
from flask.ext.login import login_user, current_user
from tweetmatch import app
from tweetmatch.models import db, TwitterUser, Tweeter, Tweet, \
                              URLEntity, HashtagEntity, UserMentionEntity


TIME_FORMAT = '%a %b %d %H:%M:%S +0000 %Y'


twitter = OAuth().remote_app('twitter',
    base_url='https://api.twitter.com/1.1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=app.config['TWITTER_CONSUMER_KEY'],
    consumer_secret=app.config['TWITTER_CONSUMER_SECRET'],
)


@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')


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

    me = TwitterUser.query.get(resp['user_id'])
    if me:
        flash(app.character.login.format(me.name))

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
            flash(app.character.twitter_error)

        me = TwitterUser(
            twitter_id=resp['user_id'],
            username=resp['screen_name'],
            name=response.data['name'],
            photo=response.data['profile_image_url'],
        )
        flash(app.character.login_first_time.format(me.name))
        db.session.add(me)
        db.session.commit()

    login_user(me)

    return redirect(request.args.get('next') or request.referrer or '/')


def load_timeline_tweets(from_list_id=None):
    """a user must be authenticated already
    https://dev.twitter.com/docs/api/1.1/get/statuses/home_timeline
    https://dev.twitter.com/docs/api/1.1/get/lists/statuses
    """
    from_list_id = from_list_id or current_user.follow_list
    logging.info('gathering {}\'s timeline...', current_user.name)
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
        flash(app.character.twitter_error)
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
            current_user.following.append(tweeter)
            db.session.add(tweeter)
            db.session.add(current_user)
            db.session.commit()


        logging.info('new tweet from {}'.format(tweeter.username))
        tweet = Tweet(
            id=tweet_data['id_str'],
            text=tweet_data['text'],
            timestamp=datetime.strptime(tweet_data['created_at'], TIME_FORMAT),
            user=tweeter,
        )
        db.session.add(tweet)

        for url in tweet_data['entities']['urls']:
            db.session.add(URLEntity(
                indices=url['indices'],
                tweet=tweet,
                expanded=url['expanded_url'],
                short=url['url'],
                display=url['display_url'],
            ))

        for hashtag in tweet_data['entities']['hashtags']:
            db.session.add(HashtagEntity(
                indices=hashtag['indices'],
                tweet=tweet,
                text=hashtag['text'],
            ))

        for mention in tweet_data['entities']['user_mentions']:
            db.session.add(UserMentionEntity(
                indices=mention['indices'],
                tweet=tweet,
                user_id=mention['id_str'],
                name=mention['name'],
                screen_name=mention['screen_name'],
            ))

        num_added += 1

    db.session.commit()

    flash(app.character.tweets_added.format(num_added))


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
        flash(app.character.twitter_error)

    return lists.data

