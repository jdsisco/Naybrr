import os
from flask import Flask


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


@app.route('/')
def credentials():
    return "Hello World!"


@app.route('/<name>')
def login(name):
    return "Hello {}!".format(name)

if __name__ == '__main__':
    app.run()
