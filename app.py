
from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:pmUQjdnk3sQbMsmosJE9@naybrr.ctwclmh06vdt.us-east-2.rds.amazonaws.com:3306/Naybrr'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Testing Naybrr Server</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)