
from flask import Flask, request, jsonify, make_response, render_template, url_for, json
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
import sys
import json
import os
import psycopg2
from psycopg2 import Error
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.environ['DATABASE_URL']

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
        zipcode = request.args.get("zip")
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        
        postgres_insert_query = """ WITH neighbor AS (
            INSERT INTO account (username, email, hashpass) VALUES (%s,%s,%s)
            RETURNING accountid, username), newaddress as (
            INSERT INTO customeraddress (accountid, line1, line2, city, state, zip) 
            SELECT accountid,%s,%s,%s,%s,%s from neighbor) 
            SELECT username from neighbor;
        """
        record_to_insert = (username, email, password, line1, line2, city,state,zipcode)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print (count, "Record inserted successfully into account table")
        credentials = cursor.fetchall()
        resp = jsonify(success=True)
        return jsonify(credentials)

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
            zipcode = request.args.get("zip")
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
            record_to_update = (username, email, password, line1, line2, city,state,zipcode)
            cursor.execute(postgres_update_query, record_to_update)
            connection.commit()
            count = cursor.rowcount
            resp = jsonify(success=True)
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
    except:
        print("Failed to connect")
        xconn = jsonify(success=False)
        return xconn
                
@app.route("/find", methods=["GET","POST"])
def find():
    try:
        username = request.args.get("search")
        zipcode = request.args.get("zip")
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        postgres_get_query = """SELECT account.accountid, username FROM account 
        INNER JOIN customeraddress on customeraddress.accountid = account.accountid 
        WHERE account.username ilike %s and customeraddress.zip = %s; """
        search_zip = (username, zipcode)
        cursor.execute(postgres_get_query, search_zip)
        connection.commit()
        count = cursor.rowcount
        credentials = cursor.fetchall()
        resp = jsonify(credentials)
        return resp
            
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to find users in zip code", error)
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
        zipcode = request.args.get("zip")
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        postgres_get_query = """ SELECT accountid, username FROM account
        INNER JOIN customeraddress USING (accountid) 
        WHERE customeraddress.zip = %s; """
        search_zip = (zipcode,)
        cursor.execute(postgres_get_query, search_zip)
        connection.commit()
        count = cursor.rowcount
        credentials = cursor.fetchall()
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
        accountid = request.args.get("accountId")
        itemname = request.args.get("itemName")
        price = request.args.get("Price")
        quantity = request.args.get("quantity")
        imagepath = request.args.get("imgPath")
        description = request.args.get("description")
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        
        postgres_item_query = """ WITH newitem AS (
            INSERT INTO inventory (accountid, itemname, price, quantity, imagepath, description) 
            VALUES (%s,%s,%s,%s,%s,%s)
            RETURNING itemid, accountid)
            SELECT itemid, accountid from newitem;
        """
        insert_item = (accountid, itemname, price, quantity, imagepath, description)
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
        username = request.args.get("username")
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        postgres_get_query = """ SELECT itemid, itemname, price, quantity, imagepath, description FROM account 
        INNER JOIN inventory USING (accountid)
        INNER JOIN customeraddress USING (accountid) 
        WHERE account.username ilike %s; """
        search_user = (username,)
        cursor.execute(postgres_get_query, search_user)
        connection.commit()
        count = cursor.rowcount
        credentials = cursor.fetchall()
        resp = jsonify(credentials)
        print (credentials)
        return resp
            
    except (Exception, psycopg2.Error) as error :
        if(connection):
            print("Failed to find person", error)
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
        accountid = request.args.get("accountId")
        itemid = request.args.get("itemId")
        itemname = request.args.get("itemName")
        price = request.args.get("Price")
        quantity = request.args.get("quantity")
        imagepath = request.args.get("imgPath")
        description = request.args.get("description")
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        
        postgres_update_query =  """UPDATE inventory SET itemname = %s, price = %s, quantity = %s,
            imagepath = %s, description = %s 
            WHERE accountid = %s and itemid = %s;"""
        insert_item = (itemname, price, quantity, imagepath, description, accountid, itemid)
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
        itemid = request.args.get("itemId")
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor()
        postgres_delete_query = """DELETE FROM inventory WHERE itemid = %s;"""
        delete_item = (itemid,)
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
        itemid = request.args.get("itemId")
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        postgres_get_query = """ SELECT itemid, itemname, price, quantity, imagepath, description FROM account 
        INNER JOIN inventory USING (accountid)
        INNER JOIN customeraddress USING (accountid) 
        WHERE inventory.itemid = %s; """
        search_zip = (itemid,)
        cursor.execute(postgres_get_query, search_zip)
        connection.commit()
        count = cursor.rowcount
        credentials = cursor.fetchall()
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

@app.route('/search',methods=["GET","POST"])
def search_item():
    try:
        itemname = request.args.get("search")
        description = request.args.get("search")
        zipcode = request.args.get("zip")
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        postgres_get_query = """Select zip, account.accountid, itemname, itemid, price, quantity, imagepath, description from account
        inner join inventory using (accountid)
        inner join customeraddress using (accountid)
        where (itemname ILIKE %s or description ILIKE %s) AND zip = %s;"""
        search_item = (itemname, description, zipcode)
        cursor.execute(postgres_get_query, search_item)
        connection.commit()
        count = cursor.rowcount
        credentials = cursor.fetchall()
        resp = jsonify(credentials)
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

@app.route('/order',methods=["GET","POST"])
def order_item():
    try:
        accountid = request.args.get("accountId")
        itemid = request.args.get("itemId")
        quantity = request.args.get("quantity")
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        postgres_order_query = """with current_order as (
        INSERT INTO orders (accountid) values (%s)
        RETURNING *), newquantity as (
        UPDATE inventory SET quantity = quantity - %s where itemid = %s returning *) 
        INSERT into ordereditems (itemid, orderid, quantity) values
        ((select itemid from newquantity), (select orderid from current_order),
        (%s)) returning orderid, itemid, %s as quantity;"""
        order_item = (accountid,quantity,itemid,quantity,quantity)
        cursor.execute(postgres_order_query, order_item)
        connection.commit()
        count = cursor.rowcount
        credentials = cursor.fetchall()
        resp = jsonify(credentials)
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

@app.route('/status',methods=["GET","POST"])
def order_info():
    try:
        orderid = request.args.get("orderId")
        connection = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        postgres_order_query = """select orderid, itemid, itemname, price, ordereditems.quantity, orders.accountid, dateordered from ordereditems
        inner join orders using (orderid)
        inner join inventory using (itemid) where orderid = %s;"""
        order_item = (orderid,)
        cursor.execute(postgres_order_query, order_item)
        connection.commit()
        count = cursor.rowcount
        credentials = cursor.fetchall()
        resp = jsonify(success=True)
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
    #Order Item