
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
@app.route("/new", methods=["GET", "POST"])
def new_user():
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        
        postgres_insert_query = """ WITH neighbor AS (
            INSERT INTO account (username, email, hashpass) VALUES (%s,%s,%s)
            RETURNING accountid, username), newaddress as (
            INSERT INTO customeraddress (accountid, line1, line2, city, state, zip) 
            SELECT accountid,%s,%s,%s,%s,%s from neighbor) 
            SELECT username from neighbor;
        """
        record_to_insert = ('test6', '6th@testemail.com', '998','48 Lois Lane', empty, 'Warwick','RI','02499')
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into account table")
        resp = jsonify(cursor.fetchall())
        return resp

    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into account table", error)
            resp = jsonify({"accountid":"-1"})
            return resp

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
        
        postgres_insert_query = """  SELECT username FROM account where username = %s AND hashpass = %s;
        """
        record_to_insert = ('test4', 'asdff')
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        if count == 0:
            resp = jsonify(success=False)
            return resp
        else:
            credentials = json.dumps(cursor.fetchall())
            resp = jsonify(success=True)
            print (credentials)
            return resp
            
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert record into account table", error)
            resp = jsonify(success=False)
            return resp

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

   

@app.route("/update", methods=["GET","POST"])
def update_user():
    try:
        try:
            connection = psycopg2.connect(DATABASE_URL, sslmode='require')
            cursor = connection.cursor()
            postgres_get_query = """ SELECT account.accountid, username, email, hashpass, 
            line1, line2, city, state, zip FROM account 
            INNER JOIN customeraddress on customeraddress.accountid = account.accountid 
            WHERE account.accountid = %s; """
            current_account = ('6')
            cursor.execute(postgres_get_query, current_account)
            connection.commit()
            count = cursor.rowcount
            credentials = json.dumps(cursor.fetchall())
            resp = jsonify(success=True)
            print (credentials)
            return resp
                
        except (Exception, psycopg2.Error) as error :
            if(connection):
                print("Failed to retrieve record", error)
                resp = jsonify(success=False)
                return resp

        finally:
            #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")
    except:
        print("Failed to connect")
        xconn = jsonify(success=False)
        return xconn

    try:        #Need to connect update status with pulled account information.
        try:
            connection = psycopg2.connect(DATABASE_URL, sslmode='require')
            cursor = connection.cursor()
            postgres_update_query =  """WITH updateneighbor AS (
                UPDATE account SET username = %s, email = %s, hashpass = %s WHERE Username = %s
                RETURNING accountid)
                UPDATE customeraddress SET line1 = %s, line2 = %s, city = %s, state = %s, zip = %s 
                WHERE accountid FROM updateneighbor = accountid;"""
            
            record_to_insert = ('test4', '6th@testemail.com', 'asdff', 'test4', '48 Lois Lane', empty, 'Warwick','RI','02499')
            cursor.execute(postgres_update_query, record_to_insert)
            connection.commit()
            count = cursor.rowcount
            credentials = json.dumps(cursor.fetchall())
            resp = jsonify(success=True)
            print (credentials)
            return resp
                
        except (Exception, psycopg2.Error) as error :
            if(connection):
                print("Failed to update record", error)
                resp = jsonify(success=False)
                return resp

        finally:
            #closing database connection.
            if(connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

@app.route("/find",methods=["GET","POST"])
def find_user():
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        postgres_get_query = """ SELECT account.accountid, username FROM account 
        INNER JOIN customeraddress on customeraddress.accountid = account.accountid 
        WHERE zip = %s; """
        search_zip = ('02201')
        cursor.execute(postgres_get_query, current_account)
        connection.commit()
        count = cursor.rowcount
        credentials = json.dumps(cursor.fetchall())
        resp = jsonify(success=True)
        print (credentials)
        return resp
            
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to find zip code", error)
            resp = jsonify(success=False)
            return resp

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
                
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

@app.route('/test')
def index():
    return "<h1>Testing Naybrr Server</h1>"

if __name__ == '__main__':
    app.run(threaded=True, port=5000)