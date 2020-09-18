
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
        username = request.args.get("username")
        email = request.args.get("email")
        password = request.args.get("password")
        line1 = request.args.get("line1")
        line2 = request.args.get("line2")
        city = request.args.get("city")
        state = request.args.get("state")
        zip = request.args.get("zip")
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        
        postgres_insert_query = """ WITH neighbor AS (
            INSERT INTO account (username, email, hashpass) VALUES (%s,%s,%s)
            RETURNING accountid, username), newaddress as (
            INSERT INTO customeraddress (accountid, line1, line2, city, state, zip) 
            SELECT accountid,%s,%s,%s,%s,%s from neighbor) 
            SELECT username from neighbor;
        """
        record_to_insert = (username, email, password, line1, line2, city,state,zip)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into account table")
        resp = jsonify(success=True())
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
        username = request.args.get("username")
        password = request.args.get("password")
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        
        postgres_insert_query = """  SELECT username FROM account where username = %s AND hashpass = %s;
        """
        record_to_insert = (username, password)
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
            username = request.args.get("username")
            email = request.args.get("email")
            password = request.args.get("password")
            line1 = request.args.get("line1")
            line2 = request.args.get("line2")
            city = request.args.get("city")
            state = request.args.get("state")
            zip = request.args.get("zip")
            connection = psycopg2.connect(DATABASE_URL, sslmode='require')
            cursor = connection.cursor()
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
            record_to_update = (username, email, password, line1, line2, city,state,zip)
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
        username = request.args.get("search")
        zip = request.args.get("zip")
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        postgres_get_query = """ SELECT account.accountid, username FROM account 
        INNER JOIN customeraddress on customeraddress.accountid = account.accountid 
        WHERE username ilike %s and zip = %s; """
        search_zip = (username, zip)
        cursor.execute(postgres_get_query, search_zip)
        connection.commit()
        count = cursor.rowcount
        credentials = json.dumps(cursor.fetchall())
        resp = jsonify(credentials)
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
        zip = request.args.get("zip")
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        postgres_get_query = """ SELECT username, accountid FROM account
        INNER JOIN customeraddress USING (accountid) 
        WHERE customeraddress.zip = %s; """
        search_zip = (zip,)
        cursor.execute(postgres_get_query, search_zip)
        connection.commit()
        count = cursor.rowcount
        credentials = json.dumps(cursor.fetchall())
        resp = jsonify(credentials)
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
        search_user = ('Jam',)
        cursor.execute(postgres_get_query, search_user)
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
        postgres_get_query = """Select zip, account.accountid, itemname, itemid, price, quantity, imagepath, description from account
        inner join inventory using (accountid)
        inner join customeraddress using (accountid)
        where (itemname ILIKE %s or description ILIKE %s) AND zip = %s;"""
        search_item = ('su','su','02201')
        ilike_pattern = "%{}%".format(search_item)
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
    try:
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        postgres_order_query = """with current_order as (
        INSERT INTO orders (accountid) values (%s)
        RETURNING *), newquantity as (
        UPDATE inventory SET quantity = quantity - %s where itemid = %s and itemname ilike %s
        returning *) 
        INSERT into ordereditems (itemid, orderid, quantity) values
        ((select itemid from newquantity), (select orderid from current_order),
        (%s))
        WHERE orderid = (select orderid from current_order);"""
        order_item = ('3','su')
        cursor.execute(postgres_order_query, order_item)
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


if __name__ == '__main__':
    app.run(threaded=True, port=5000)

    #To-do:
    #Search Item 
    #Order Item
    #add to cart