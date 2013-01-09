from flask_oauth import OAuth
from flask import Flask, url_for, request

oauth = OAuth()
twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key='tM3lu6kav7EFzljmXjhHFg',
    consumer_secret='4kBX7EfbBp7agsKfkgF1S5luiG0pHrlOgWWLbYzqqY'
)

def login():
    try:
        return twitter.authorize(request.referrer)
    except Exception as e:
        print "[Error] %s" % e
    return "500 Internal error"
