# -*- coding: utf-8 -*-
"""
    tweetmatch.__init__
    ~~~~~~~~~~~~~~~~~~~

    The structure of tweetmatch follows the Simple Packages pattern:
    http://flask.pocoo.org/docs/patterns/packages/#simple-packages

    The components here require the app instance, so there is a circular import
    back to tweetmatch (__init__) to get app. This is ok.

    :copyright: (c) 2013 by Queen's Haxx.
    :license: MIT, see the license file for more details.
"""

# Set up the application first…
from flask import Flask
app = Flask(__name__)

# …then import the components.
import tweetmatch.config
import tweetmatch.twitter
import tweetmatch.logins
import tweetmatch.character
import tweetmatch.views
#import tweetmatch.assets

