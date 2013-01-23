
import os
from flask import Flask, url_for, render_template, flash, request
from flask_oauth import OAuth
import config


app = Flask(__name__)

oauth = OAuth()

twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key='tM3lu6kav7EFzljmXjhHFg',
    consumer_secret='4kBX7EfbBp7agsKfkgF1S5luiG0pHrlOgWWLbYzqqY'
)


@app.route('/')
def hello():
    flash('hello world')
    content = {}
    return render_template('home.html', **content)


@app.route('/login')
def login():
    #try:
    return twitter.authorize(callback=url_for('oauth_authorized',
        next=request.referrer))
    #except Exception as e:
    #    return "500 error: {}".format(e), 500


@app.route('/account')
@twitter.authorized_handler
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
