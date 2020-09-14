import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    USER = 'root'
    ENDPOINT = 'naybrr.ctwclmh06vdt.us-east-2.rds.amazonaws.com'
    PASSWORD = 'pmUQjdnk3sQbMsmosJE9'
    DATABASE = 'Naybrr'