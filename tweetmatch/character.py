# -*- coding: utf-8 -*-
"""
    tweetmatch.character
    ~~~~~~~~~~~~~~~~~~~~

    flash(app.character.login.first_time.format(current_user.name))
    Check templates/character.yaml to see the actual strings.

    :copyright: (c) 2013 by Queen's Haxx.
    :license: MIT, see the license file for more details.
"""


from tweetmatch import app


class messages(object):

    login = 'Welcome back {}.'
    login_first_time = 'Hello {}.'
    login_fail = 'Could not log you in :('
    logout = 'bye'

    twitter_rate_limited = 'slow down'
    twitter_unauthorized = 'twitter says no'
    twitter_not_found = 'not found'
    twitter_error = 'twitter error'

    tweets_added = 'added {} new tweets'

    guess_right = 'yeah.'
    guess_wrong = 'nope.'


app.character = messages
