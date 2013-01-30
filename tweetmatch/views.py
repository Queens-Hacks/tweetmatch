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
    return render_template('home.html')

