
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

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:pmUQjdnk3sQbMsmosJE9@naybrr.ctwclmh06vdt.us-east-2.rds.amazonaws.com:3306/Naybrr'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app)

try:
    """connection = psycopg2.connect(user="tpjfsrbkxqwbln",
                                  password="4710d90b684d897948315dcb66a50d659b585bd6e13906152dc1d4cdd13b9bc5",
                                  host="ec2-52-200-134-180.compute-1.amazonaws.com",
                                  port="5432",
                                  database="dcfp0d6kcu6bnh")"""
    connection = psycopg2.connect(DATABASE_URL, sslmode='require')
    cursor = connection.cursor()

    #postgres_insert_query = """ INSERT INTO account (username, email, hashpass) VALUES (%s,%s,%s)"""
    postgres_insert_query = """ WITH data (username, email, hashpass, line1, line2, city, state, zip) AS 
    (
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s)), 
        neighbor AS (
        INSERT INTO account (username, email, hashpass) 
        SELECT username, email, hashpass FROM data
        RETURNING accountid AS account_id),
        address AS (
        INSERT INTO customeraddress(accountid, line1, line2, city, state, zip)
        SELECT line1, line2, city, state, zip FROM data
        JOIN neighbor USING (account_id)
        ));

    """
    record_to_insert = ('test2', 'test@email.com', '12345','1 NEIT Boulevard','suite 150', 'East Greenwich','RI','04345')
    cursor.execute(postgres_insert_query, record_to_insert)

    connection.commit()
    count = cursor.rowcount
    print (count, "Record inserted successfully into account table")

except (Exception, psycopg2.Error) as error :
    if(connection):
        print("Failed to insert record into account table", error)

finally:
    #closing database connection.
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")

"""
class DataTest(db.Model):
    __tablename__ = "test"
    id = db.Column(db.Integer, primary_key=True)
    mydata = db.Column(db.Text())

    def __init__ (self, mydata):
        self.mydata = mydata


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

@app.route("/")
def enter_data(): 
    return render_template("data.html")"""

@app.route('/test')
def index():
    return "<h1>Testing Naybrr Server</h1>"

if __name__ == '__main__':
    app.run(threaded=True, port=5000)