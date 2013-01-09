import os
from auth import twitter
from flask import Flask, url_for

app = Flask(__name__)

app.secret_key = "laij3lifajl3ijalijf3liajw3lialw"

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/auth')
def login():
    return twitter.login()

if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
