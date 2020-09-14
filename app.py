from flask import Flask

app = Flask(__name__)
app.secret_key = "secret key"

if __name__ == '__main__':
    app.run()