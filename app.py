from flask import Flask, request, Response, jsonify, render_template
import io
import pymysql
from app import app
from db_config import mysql
from tables import Results
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    Username = request.args.get("name", None)

    # For debugging
    print(f"got Username {Username}")

    response = {}

    # Check if user sent a name at all
    if not Username:
        response["ERROR"] = "no Username found, please send a Username."
    # Check if the user entered a number not a name
    elif str(Username).isdigit():
        response["ERROR"] = "Username can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = f"Welcome {Username} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('Username')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": f"Welcome {Username} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no Username found, please send a Username."
        })

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True)