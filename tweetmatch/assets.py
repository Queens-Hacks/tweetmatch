# -*- coding: utf-8 -*-
"""
    tweetmatch.assets
    ~~~~~~~~~~~~~~~~~

    Manage static stuff.
    http://elsdoerfer.name/docs/flask-assets/

    :copyright: (c) 2013 by Queen's Haxx.
    :license: MIT, see the license file for more details.
"""


from flask.ext.assets import Environment, Bundle
from tweetmatch import app


assets = Environment(app)
