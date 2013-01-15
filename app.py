
import os
from flask import Flask, url_for, render_template, flash
from auth import twitter
import config


app = Flask(__name__)

# TODO: move secret key to config
app.secret_key = "laij3lifajl3ijalijf3liajw3lialw"


@app.route('/')
def hello():
    flash('hello world')
    content = {}
    return render_template('home.html', **content)


@app.route('/auth')
def login():
    return twitter.login()


@app.route('/account')
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
    # todo: get these from config
    port = int(os.environ.get('PORT', 5000)) 
    app.run(host='0.0.0.0', port=port, debug=config.DEBUG)
