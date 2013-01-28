
import os
from functools import wraps
from datetime import datetime
from flask import Flask, url_for, render_template, flash, request, session, \
    redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask_oauth import OAuth
import config


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
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


oauth = OAuth()


twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=config.TWITTER_CONSUMER_KEY,
    consumer_secret=config.TWITTER_CONSUMER_SECRET,
)

def redirect_url():
    return request.args.get('next') or \
           request.referrer or \
           url_for('hello')

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = session.get('twitter_token')
        if token:
            print "already logged in: {}".format(token)
            session.pop('twitter_token')
            return f(*args, **kwargs)
        else:
            print "logging in, from {}".format(redirect_url())
            return twitter.authorize(callback=url_for('oauth_authorized',
                next=redirect_url()))
    return wrapper


@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')


@app.route('/')
def hello():
    flash('hello world')
    result = twitter.get('statuses/user_timeline.json', data={
        'screen_name': 'unicyclephil',
        'exclude_replies': 'true',
        'include_rts': 'false',
    })
    if result.status == 403:
        flash('tweet too long?')
    else:
        flash('{}'.format(result.status))
        flash('tweeted! {}'.format(result.data))
    content = {}
    return render_template('home.html', **content)


@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('hello')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )
    session['twitter_user'] = resp['screen_name']

    flash('You were signed in as %s' % resp['screen_name'])
    return redirect(next_url)


@app.route('/account')
@login_required
def account():
    """let a user manage their account"""
    return "account!"


@app.route('/account/<twitter_handle>')
def profile(twitter_handle):
    """see a user's account or something... maybe stats on how often people
    guess a famous person's tweets... """
    return "profile of {}.".format(twitter_handle)


@app.route('/tweet/<tweet_id>')
def tweet(tweet_id):
    """ show a particular tweets, and maybe some stats about it? """
    return "tweet id: {}".format(tweet_id)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__ == '__main__':
    app.secret_key = config.SECRET_KEY
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
