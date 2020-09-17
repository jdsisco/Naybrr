
from flask import Flask, request, jsonify, make_response, render_template, url_for, json
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
            WHERE account.username = %s; """
            current_account = ('test4',)
            cursor.execute(postgres_get_query, current_account)
            connection.commit()
            count = cursor.rowcount
            credentials = json.dumps(cursor.fetchall())
            postgres_update_query =  """WITH update_values (username, email, hashpass, line1, line2, city, state, zip) AS (
            values (%s,%s,%s,%s,%s,%s,%s,%s)),
            updateneighbor as (
            UPDATE account SET username = (Select username from update_values), 
            email = (Select email from update_values), 
            hashpass = (select hashpass from update_values) WHERE Username = 
            (select username from update_values) 
            RETURNING *)
            UPDATE customeraddress SET line1 = (select line1 from update_values), 
            line2 = (select line2 from update_values), city = (select city from update_values), 
            state = (select state from update_values), zip = (select zip from update_values)
            WHERE accountid = (select accountid from updateneighbor);"""
            record_to_update = ('test4', '6th@testemail.com', 'asdff', '48 Lois Lane', empty, 'Warwick','RI','02499')
            cursor.execute(postgres_update_query, record_to_update)
            connection.commit()
            count = cursor.rowcount
            resp = jsonify(success=True)
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
                
@app.route("/find", methods=["GET","POST"])
def find():
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        postgres_get_query = """ SELECT account.accountid, username FROM account 
        INNER JOIN customeraddress on customeraddress.accountid = account.accountid 
        WHERE zip = %s; """
        search_zip = ('02201',)
        cursor.execute(postgres_get_query, search_zip)
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

@app.route("/nearby",methods=["GET","POST"])
def find_user():
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        postgres_get_query = """ SELECT username, accountid FROM account
        INNER JOIN customeraddress USING (accountid) 
        WHERE customeraddress.zip = %s; """
        search_zip = ('02201',)
        cursor.execute(postgres_get_query, search_zip)
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

@app.route("/newItem",methods=["GET","POST"])
def add_item():
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        
        postgres_item_query = """ WITH newitem AS (
            INSERT INTO inventory (accountid, itemname, price, quantity, imagepath, description) 
            VALUES (%s,%s,%s,%s,%s,%s)
            RETURNING itemid, accountid)
            SELECT itemid, accountid from newitem;
        """
        insert_item = ('3', 'Salt', '1.50','2', empty, 'This is salt.')
        cursor.execute(postgres_item_query, insert_item)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted as new item")
        credentials = json.dumps(cursor.fetchall())
        print (credentials)
        resp = jsonify(success=True)
        return resp

    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to insert new item", error)
            resp = jsonify(success=False)
            return resp

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

@app.route("/neighbor",methods=["GET","POST"])
def neighbor():
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        postgres_get_query = """ SELECT itemid, itemname, price, quantity, imagepath, description FROM account 
        INNER JOIN inventory USING (accountid)
        INNER JOIN customeraddress USING (accountid) 
        WHERE account.username = %s; """
        search_zip = ('Jam',)
        cursor.execute(postgres_get_query, search_zip)
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

@app.route("/updateItem",methods=["GET","POST"])
def update_item():
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        
        postgres_update_query =  """UPDATE inventory SET itemname = %s, price = %s, quantity = %s,
            imagepath = %s, description = %s 
            WHERE accountid = %s and itemid = %s;"""
        insert_item = ('Ketchup', '4.28', '1','https://cat.chup', 'Red sauce', '3','7')
        cursor.execute(postgres_update_query, insert_item)
        connection.commit()
        count = cursor.rowcount
        print (count, "Updated item")
        resp = jsonify(success=True)
        return resp

    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to update item", error)
            resp = jsonify(success=False)
            return resp

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

@app.route("/delete",methods=["GET","POST"])
def delete_item():
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        postgres_delete_query = """DELETE FROM inventory WHERE itemid = %s;"""
        delete_item = ('3')
        cursor.execute(postgres_delete_query, delete_item)
        connection.commit()
        count = cursor.rowcount
        print (count, "Item deleted")
        resp = jsonify(success=True)
        return resp

    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to delete item", error)
            resp = jsonify(success=False)
            return resp

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

@app.route("/item",methods=["GET", "POST"])
def find_item():
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        postgres_get_query = """ SELECT username, itemid, itemname, price, quantity, imagepath, description FROM account 
        INNER JOIN inventory USING (accountid)
        INNER JOIN customeraddress USING (accountid) 
        WHERE customeraddress.zip = %s; """
        search_zip = ('02201',)
        cursor.execute(postgres_get_query, search_zip)
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

@app.route('/search',methods=["GET","POST"])
def search_item():
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        postgres_get_query = """Select account.accountid, itemname, itemid, price, quantity, imagepath, description from account
        inner join inventory using (accountid)
        inner join customeraddress using (accountid)
        where itemname ILIKE %s or description ILIKE %s;"""
        search_item = ('su','su')
        ilike_pattern = "%%{}%%".format(search_item)
        cursor.execute(postgres_get_query, ilike_pattern)
        connection.commit()
        count = cursor.rowcount
        credentials = json.dumps(cursor.fetchall())
        resp = jsonify(success=True)
        print (credentials)
        return resp
            
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to find item", error)
            resp = jsonify(success=False)
            return resp

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

@app.route('/order')
def order_item():
    return "Order Item here"

if __name__ == '__main__':
    app.run(threaded=True, port=5000)

    #To-do:
    #Update Item database call
    #Order Item