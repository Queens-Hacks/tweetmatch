# -*- coding: utf-8 -*-
"""
    tweetmatch.views
    ~~~~~~~~~~~~~~~~~

    Blah blah blah

    :copyright: (c) 2013 by Queen's Haxx.
    :license: MIT, see the license file for more details.
"""


from flask import render_template
from tweetmatch import app, models


@app.route('/')
def hello():
    challenge = {
        'tweet': {
            'text': '.@BarackObama modern baby monitors have night vision technology did babies kill bin laden ,',
            'time': '30 Jan 2013',
            'id': 404838304,
        },
        'suspects': [
            {
                'username': '@BarackObama',
                'name': 'Barack Obama',
                'photo': 'url',
            },
            {
                'username': '@robdalaney',
                'name': 'rob delany',
                'photo': 'url',
            },
        ]
    }
    context = {
        'challenge': challenge,
    }
    return render_template('home.html', **context)

