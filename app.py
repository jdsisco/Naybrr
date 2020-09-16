
from flask import Flask, request, jsonify, make_response, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
import sys
import json
import os
import psycopg2
from psycopg2 import Error

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
empty = None
app = Flask(__name__)
@app.route("/new", methods=["GET, POST"])
def new_user():
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        
        postgres_insert_query = """ WITH neighbor AS (
            INSERT INTO account (username, email, hashpass) VALUES (%s,%s,%s)
            RETURNING accountid)
            INSERT INTO customeraddress (accountid, line1, line2, city, state, zip) 
            SELECT accountid,%s,%s,%s,%s,%s from neighbor;
        """
        record_to_insert = ('test4', '4th@email.com', 'asdff','3 NEIT Boulevard', empty, 'Providence','RI','02445')
        cursor.execute(postgres_insert_query, record_to_insert)

        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into account table")
        resp = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json')
        return resp

    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into account table", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

            
    """def get_current_user():
    return jsonify(
        username=g.user.username,
        email=g.user.email,
        id=g.user.id
    )
    
    {
    "username": "admin",
    "email": "admin@localhost",
    "id": 42
}"""

@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        
        postgres_insert_query = """  SELECT username FROM account where username = '%s' AND hashpass = '%s';
        """
        record_to_insert = ('test5', 'asdf4f')
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        if count == 0
            return "<h1>Count is 0</h1>"
        """
        print (count, "Record inserted successfully into account table")
        resp = app.response_class(
            response=json.dumps(data),
            status=200,
            mimetype='application/json')
        return resp"""

    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into account table", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

    resp = jsonify(success=True)
    return resp

@app.route("/update", methods=["GET"])
def update_user():
    resp = jsonify(success=True)
    return resp

@app.route("/find", methods=["POST"])
def find_user():
    resp = jsonify(success=True) #Return Account ID and username
    return resp

@app.route("/nearby",methods=["POST"])
def user_inventory():
    resp = jsonify(success=True) #Return itemID, name, description, price, quantity, imagePath
    return resp

@app.route("/insert",methods=["GET"])
def add_item():
    resp = jsonify(success=True)
    return resp

@app.route("/UpdateItem",methods=["POST"])
def update_item():
    resp = jsonify(success=True)
    return resp

@app.route("/delete",methods=["POST"])
def delete_item():
    resp = jsonify(success=True)
    return resp

@app.route("/item",methods=["GET"])
def find_item():
    resp = jsonify(success=True) #Return itemID, name, description, price, quantity, imagePath (single?)
    return resp
"""

@app.route("/submit", methods=["POST"])
def post_to_db():
    indata = DataTest(request.form['mydata'])
    data = copy(indata. __dict__ )
    del data["_sa_instance_state"]
    try:
        db.session.add(indata)
        db.session.commit()
    except Exception as e:
        print("\n FAILED entry: {}\n".format(json.dumps(data)))
        print(e)
        sys.stdout.flush()
    return 'Success! To enter more data, <a href="{}">click here!</a>'.format(url_for("enter_data"))
"""

@app.route('/test')
def index():
    return "<h1>Testing Naybrr Server</h1>"

if __name__ == '__main__':
    app.run(threaded=True, port=5000)