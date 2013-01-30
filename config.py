"""
On Heroku, all app-specific configuration is done with environment variables.
Environment variables are guaranteed to persist as well.

So... this file could put together all the app's configuration settings, first
checking for an environment variable, and then falling back to something
sensible for a development environment.

so for example,

    import os
    PORT = os.environ.get('PORT', 5000)
    DEBUG = os.environ.get('DEBUG', True)

Please make a note in the (or something) of all variables that need to be set
in a production environment (since we'll have to do that on heroku.)
"""
import os
env = os.environ.get

try:
	import twitter_keys
	DEBUG = True
except ImportError:
	DEBUG = False

TWITTER_CONSUMER_KEY = env('TWITTER_CONSUMER_KEY', twitter_keys.TWITTER_CONSUMER_KEY) # get from dev.twitter.com
TWITTER_CONSUMER_SECRET = env('TWITTER_CONSUMER_SECRET', twitter_keys.TWITTER_CONSUMER_SECRET)



SQLALCHEMY_DATABASE_URI = 'sqlite:///dev-db.sqlite3'

HOST = env('IP', '127.0.0.1') # set to 0.0.0.0 on heroku
PORT = env('PORT', 5000) # set automatically by heroku

SECRET_KEY = env('SECRET_KEY', 'so secure')
