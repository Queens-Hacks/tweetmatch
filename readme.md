# Secret project codename "tweetmatch"

Who tweeted that? Given a tweet, guess between two Twitter accounts for where you think that tweet came from. Connect your own account to add the list of people you follow to the list of Twitter accounts.

Lastest build available for playing with at [tweetmatch2.herokuapp.com](tweetmatch2.herokuapp.com).

Better install information coming soon. Here are the basic steps (for unix... the painful process of getting anything ever to work on windows will be documented soon):


## Tools

you will need...

* Python 2.7 with pip
* git


## Twitter

Go to [dev.twitter.com/apps](https://dev.twitter.com/apps) and create a new application.

Name
    call it anything

Description
    whatever you want

Website
    again arbitrary, but it has to be valid (including starting with `http://`)

Callback URL:
    use `http://127.0.0.1:5000`


Create your app. Leave the page open, you'll need the `consumer key` and `consumer secret` in a minute.


## Source

Clone the repository somewhere

Make a file in the root directory called `twitter_keys.py`. Edit it so that it contains the keys you got from twitter:

    TWITTER_CONSUMER_KEY = 'the key you got from twitter'
    TWITTER_CONSUMER_SECRET = 'the secret you got from twitter'


## Environment

* get virtualenv if you don't have it: `$ sudo pip install virtualenv`
* create a virtualenv: `$ virtualenv venv`
* activate your new virtal environment: `$ . venv/bin/activate`
* get the packages for tweetmatch: `$ pip install -r dev-requirements.txt`


## Set up

* create the database: `$ ./manage.py createdb`


## Go!

* start the server: `$ ./manage.py runserver`
* open in a web browser: [127.0.0.1:5000](http://127.0.0.1:5000)
