"""
http://packages.python.org/Flask-OAuth/
"""


from flask import request, session, redirect, url_for, flash
from flask.ext.oauth import OAuth
from tweetmatch import app


#oauth = OAuth()
twitter = OAuth().remote_app('twitter',
    base_url='https://api.twitter.com/1/',
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
    if session.get('twitter_token'):
        # already logged in
        return redirect_url()
    return twitter.authorize(callback=url_for('oauth_authorized'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect_url()


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

    flash('signed in as %s' % resp['screen_name'])
    return redirect_url()



